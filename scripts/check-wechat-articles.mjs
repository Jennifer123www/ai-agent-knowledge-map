import { access, readFile, readdir } from "node:fs/promises";
import path from "node:path";
import { parseWechatArticle, renderWechatHtml } from "../lib/wechat/markdown.mjs";

const root = process.cwd();
const contentRoot = path.join(root, "content", "wechat");
const articleNames = new Set(["beginner-main.md", "interview-side.md"]);
const verbose = process.argv.slice(2).includes("--verbose");
const unknownArguments = process.argv.slice(2).filter((argument) => argument !== "--verbose");
if (unknownArguments.length) throw new Error(`Unknown arguments: ${unknownArguments.join(", ")}`);

const failures = [];
const statistics = [];
const interviewQuestions = new Map();
const registeredArticles = new Map();
const expectedArticlePaths = new Set();
const groupImageUsage = new Map();
let groupCount = 0;

async function collectFiles(directory, predicate) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await collectFiles(fullPath, predicate));
    else if (predicate(entry.name)) files.push(fullPath);
  }
  return files;
}

function chineseCharacterCount(value) {
  return [...value].filter((character) => /\p{Script=Han}/u.test(character)).length;
}

function repositoryPath(filePath) {
  return path.relative(root, filePath).split(path.sep).join("/");
}

function seriesPath(seriesRoot, relativePath) {
  return path.resolve(seriesRoot, relativePath);
}

function fail(label, message) {
  failures.push(`${label}: ${message}`);
}

const manifestPaths = await collectFiles(contentRoot, (name) => name === "series.json");
if (manifestPaths.length === 0) fail("content/wechat", "no series.json manifest found");

for (const manifestPath of manifestPaths) {
  const manifestLabel = repositoryPath(manifestPath);
  const seriesRoot = path.dirname(manifestPath);
  let manifest;
  try {
    manifest = JSON.parse(await readFile(manifestPath, "utf8"));
  } catch (error) {
    fail(manifestLabel, `invalid JSON: ${error.message}`);
    continue;
  }

  const topic = String(manifest.topic || "").trim();
  const groups = Array.isArray(manifest.groups) ? manifest.groups : [];
  const outlinePlan = manifest.draftPlan?.outlineSections;
  const characterPlan = manifest.draftPlan?.targetChineseCharacters;
  if (manifest.schemaVersion !== 1) fail(manifestLabel, "schemaVersion must be 1");
  if (!topic) fail(manifestLabel, "topic is required");
  if (outlinePlan?.min !== 8 || outlinePlan?.max !== 10) {
    fail(manifestLabel, "draftPlan.outlineSections must be 8-10");
  }
  if (characterPlan?.min !== 3200 || characterPlan?.max !== 3500) {
    fail(manifestLabel, "draftPlan.targetChineseCharacters must be 3200-3500");
  }
  if (groups.length === 0) fail(manifestLabel, "groups must not be empty");

  const groupIds = new Set();
  const seriesOrders = new Set();
  for (const group of groups) {
    groupCount += 1;
    const groupLabel = `${manifestLabel}#${group.id || "unnamed"}`;
    const id = String(group.id || "").trim();
    const contentLevel = String(group.contentLevel || "").trim();
    const submodule = String(group.submodule || "").trim();
    const seriesOrder = Number(group.seriesOrder);
    if (!id) fail(groupLabel, "id is required");
    if (groupIds.has(id)) fail(groupLabel, `duplicate group id '${id}'`);
    groupIds.add(id);
    if (!new Set(["overview", "submodule"]).has(contentLevel)) {
      fail(groupLabel, "contentLevel must be overview or submodule");
    }
    if (contentLevel === "overview" && submodule) fail(groupLabel, "overview must have an empty submodule");
    if (contentLevel === "submodule" && !submodule) fail(groupLabel, "submodule id is required");
    if (!Number.isInteger(seriesOrder) || seriesOrder < 0) fail(groupLabel, "seriesOrder must be a non-negative integer");
    if (seriesOrders.has(seriesOrder)) fail(groupLabel, `duplicate seriesOrder ${seriesOrder}`);
    seriesOrders.add(seriesOrder);

    const promptFile = String(group.promptFile || "").trim();
    let promptMarkdown = "";
    if (!promptFile) fail(groupLabel, "promptFile is required");
    else {
      try { promptMarkdown = await readFile(seriesPath(seriesRoot, promptFile), "utf8"); }
      catch { fail(groupLabel, `missing prompt file ${promptFile}`); }
    }

    const imageNames = Array.isArray(group.images) ? group.images : [];
    const declaredImages = new Set(imageNames);
    const principleImage = String(group.principleImage || "").trim();
    groupImageUsage.set(groupLabel, { declaredImages, usedImages: new Set() });
    if (declaredImages.size < 5) fail(groupLabel, "at least 5 image names must be declared");
    if (!principleImage) fail(groupLabel, "principleImage is required");
    else {
      if (!declaredImages.has(principleImage)) fail(groupLabel, "principleImage must be declared in images");
      if (!promptMarkdown.includes(path.basename(principleImage))) {
        fail(groupLabel, `prompt file must document principle image ${path.basename(principleImage)}`);
      }
    }
    for (const imageName of declaredImages) {
      if (!/\.(?:png|jpe?g)$/i.test(imageName)) fail(groupLabel, `unsupported image type: ${imageName}`);
      try { await access(seriesPath(seriesRoot, imageName)); }
      catch { fail(groupLabel, `missing image ${imageName}`); }
    }

    const articles = group.articles || {};
    for (const role of ["beginner", "interview"]) {
      const entry = articles[role];
      if (!entry) {
        fail(groupLabel, `missing ${role} article declaration`);
        continue;
      }
      const relativePath = String(entry.path || "").trim();
      const outline = Array.isArray(entry.outline) ? entry.outline : [];
      if (!relativePath) {
        fail(groupLabel, `${role}.path is required`);
        continue;
      }
      if (!String(entry.focus || "").trim()) fail(groupLabel, `${role}.focus is required`);
      if (outline.length < 8 || outline.length > 10) {
        fail(groupLabel, `${role}.outline must contain 8-10 planned sections (${outline.length})`);
      }
      if (role === "interview") {
        const boundary = entry.questionBoundary;
        if (!Array.isArray(boundary?.include) || boundary.include.length === 0) {
          fail(groupLabel, "interview.questionBoundary.include is required");
        }
        if (!Array.isArray(boundary?.exclude) || boundary.exclude.length === 0) {
          fail(groupLabel, "interview.questionBoundary.exclude is required");
        }
      }

      const articlePath = seriesPath(seriesRoot, relativePath);
      const normalizedArticlePath = path.normalize(articlePath);
      if (registeredArticles.has(normalizedArticlePath)) {
        fail(groupLabel, `article path is declared more than once: ${relativePath}`);
      }
      expectedArticlePaths.add(normalizedArticlePath);
      registeredArticles.set(normalizedArticlePath, {
        manifestLabel,
        groupLabel,
        topic,
        contentLevel,
        submodule,
        seriesOrder,
        role,
        declaredImages,
        principleImage,
      });
    }
  }
}

const actualArticlePaths = await collectFiles(contentRoot, (name) => articleNames.has(name));
for (const articlePath of actualArticlePaths) {
  if (!expectedArticlePaths.has(path.normalize(articlePath))) {
    fail(repositoryPath(articlePath), "article is not registered in a series.json manifest");
  }
}
for (const articlePath of expectedArticlePaths) {
  try { await access(articlePath); }
  catch { fail(repositoryPath(articlePath), "manifest references a missing article"); }
}

for (const [articlePath, registration] of registeredArticles) {
  const relativePath = repositoryPath(articlePath);
  let markdown;
  try {
    markdown = await readFile(articlePath, "utf8");
  } catch {
    continue;
  }

  try {
    const article = parseWechatArticle(markdown, articlePath);
    const topic = String(article.metadata.topic || "").trim();
    const contentLevel = String(article.metadata.content_level || "").trim();
    const submodule = String(article.metadata.submodule || "").trim();
    const seriesOrder = Number(article.metadata.series_order);
    if (topic !== registration.topic) throw new Error(`topic must match manifest value '${registration.topic}'`);
    if (contentLevel !== registration.contentLevel) {
      throw new Error(`content_level must match manifest value '${registration.contentLevel}'`);
    }
    if (submodule !== registration.submodule) {
      throw new Error(`submodule must match manifest value '${registration.submodule}'`);
    }
    if (seriesOrder !== registration.seriesOrder) {
      throw new Error(`series_order must match manifest value ${registration.seriesOrder}`);
    }

    const usedImages = new Set();
    const seriesRoot = path.dirname(path.join(root, registration.manifestLabel));
    for (const image of article.images) {
      await access(image.absolutePath);
      if (!/\.(?:png|jpe?g)$/i.test(image.absolutePath)) {
        throw new Error(`WeChat article images must use JPG or PNG: ${image.source}`);
      }
      const imageName = path.relative(seriesRoot, image.absolutePath).split(path.sep).join("/");
      usedImages.add(imageName);
      groupImageUsage.get(registration.groupLabel)?.usedImages.add(imageName);
      if (!registration.declaredImages.has(imageName)) {
        throw new Error(`image is not declared in series.json: ${imageName}`);
      }
    }
    if (article.images.length < 5) {
      throw new Error(`At least 5 local images are required, including the cover (${article.images.length}/5)`);
    }
    if (registration.role === "beginner" && !usedImages.has(registration.principleImage)) {
      throw new Error(`Beginner main article must use declared principle image: ${registration.principleImage}`);
    }

    const source = article.lines.join("\n");
    const referenceLinks = [...source.matchAll(/\]\((https?:\/\/[^)]+)\)/g)].map((match) => match[1]);
    if (!/^##\s+参考资料/m.test(source) || referenceLinks.length === 0) {
      throw new Error("Article must include a '参考资料' section with at least one HTTP(S) link");
    }

    const chineseCharacters = chineseCharacterCount(source);
    if (chineseCharacters < 3000 || chineseCharacters > 5000) {
      throw new Error(`Article must contain 3000-5000 Chinese characters (${chineseCharacters})`);
    }

    if (registration.role === "interview") {
      const topicQuestions = interviewQuestions.get(topic) || new Map();
      for (const match of markdown.matchAll(/^##\s+问题\s+\d+：(.+)$/gm)) {
        const title = match[1].trim();
        const normalized = title.toLowerCase().replace(/[\s，。？！、：“”‘’（）()《》]/g, "");
        const previous = topicQuestions.get(normalized);
        if (previous) fail(relativePath, `duplicate interview question '${title}' also appears in ${previous}`);
        else topicQuestions.set(normalized, relativePath);
      }
      interviewQuestions.set(topic, topicQuestions);
    }

    const uploadedUrls = new Map(article.images.slice(1).map((image) => [
      image.source,
      `https://mmbiz.qpic.cn/placeholder/${encodeURIComponent(path.basename(image.source))}`,
    ]));
    const html = renderWechatHtml(article, uploadedUrls);
    statistics.push(
      `${relativePath}: title=${[...article.title].length}/32, author=${[...article.author].length}/16, `
      + `digest=${[...article.digest].length}/120, Chinese=${chineseCharacters}, images=${article.images.length}, `
      + `references=${referenceLinks.length}, HTML=${[...html].length}/20000 chars, `
      + `${Buffer.byteLength(html, "utf8")}/1048576 bytes`,
    );
  } catch (error) {
    fail(relativePath, error.message);
  }
}

for (const [groupLabel, images] of groupImageUsage) {
  for (const imageName of images.declaredImages) {
    if (!images.usedImages.has(imageName)) {
      fail(groupLabel, `declared image is not used by either article: ${imageName}`);
    }
  }
}

if (failures.length) {
  console.error("WeChat article check failed:");
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

if (verbose) statistics.sort().forEach((line) => console.log(line));
console.log(
  `WeChat article check passed: ${manifestPaths.length} series, ${groupCount} groups, ${registeredArticles.size} articles.`,
);
