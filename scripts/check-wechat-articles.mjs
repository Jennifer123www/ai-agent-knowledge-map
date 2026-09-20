import { access, readFile, readdir } from "node:fs/promises";
import path from "node:path";
import { parseWechatArticle, renderWechatHtml } from "../lib/wechat/markdown.mjs";

const root = process.cwd();
const contentRoot = path.join(root, "content", "wechat");
const articleNames = new Set(["beginner-main.md", "interview-side.md"]);
const failures = [];
const articleGroups = new Map();

async function collectArticles(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await collectArticles(fullPath));
    else if (articleNames.has(entry.name)) files.push(fullPath);
  }
  return files;
}

function chineseCharacterCount(value) {
  return [...value].filter((character) => /\p{Script=Han}/u.test(character)).length;
}

for (const articlePath of await collectArticles(contentRoot)) {
  const relativePath = path.relative(root, articlePath);
  try {
    const markdown = await readFile(articlePath, "utf8");
    const article = parseWechatArticle(markdown, articlePath);
    const topic = String(article.metadata.topic || "").trim();
    const contentLevel = String(article.metadata.content_level || "").trim();
    const submodule = String(article.metadata.submodule || "").trim();
    const seriesOrder = Number(article.metadata.series_order);
    if (!topic) throw new Error("YAML front matter must declare topic");
    if (!new Set(["overview", "submodule"]).has(contentLevel)) {
      throw new Error("content_level must be overview or submodule");
    }
    if (contentLevel === "overview" && submodule) {
      throw new Error("Overview articles must use an empty submodule value");
    }
    if (contentLevel === "submodule" && !submodule) {
      throw new Error("Submodule articles must declare a stable submodule id");
    }
    if (!Number.isInteger(seriesOrder) || seriesOrder < 0) {
      throw new Error("series_order must be a non-negative integer");
    }
    const groupKey = `${topic}:${contentLevel}:${submodule}`;
    const group = articleGroups.get(groupKey) || { files: new Set(), orders: new Set() };
    group.files.add(path.basename(articlePath));
    group.orders.add(seriesOrder);
    articleGroups.set(groupKey, group);
    for (const image of article.images) {
      await access(image.absolutePath);
      if (!/\.(?:png|jpe?g)$/i.test(image.absolutePath)) {
        throw new Error(`WeChat article images must use JPG or PNG: ${image.source}`);
      }
    }
    if (article.images.length < 5) {
      throw new Error(`At least 5 local images are required, including the cover (${article.images.length}/5)`);
    }

    const source = article.lines.join("\n");
    const referenceLinks = [...source.matchAll(/\]\((https?:\/\/[^)]+)\)/g)].map((match) => match[1]);
    if (!/^##\s+参考资料/m.test(source) || referenceLinks.length === 0) {
      throw new Error("Article must include a '参考资料' section with at least one HTTP(S) link");
    }

    const chineseCharacters = chineseCharacterCount(article.lines.join("\n"));
    if (chineseCharacters < 3000 || chineseCharacters > 5000) {
      throw new Error(`Article must contain 3000-5000 Chinese characters (${chineseCharacters})`);
    }

    const uploadedUrls = new Map(article.images.slice(1).map((image) => [
      image.source,
      `https://mmbiz.qpic.cn/placeholder/${encodeURIComponent(path.basename(image.source))}`,
    ]));
    const html = renderWechatHtml(article, uploadedUrls);
    const htmlCharacters = [...html].length;
    const htmlBytes = Buffer.byteLength(html, "utf8");
    console.log(
      `${relativePath}: title=${[...article.title].length}/32, author=${[...article.author].length}/16, `
      + `digest=${[...article.digest].length}/120, Chinese=${chineseCharacters}, images=${article.images.length}, `
      + `references=${referenceLinks.length}, HTML=${htmlCharacters}/20000 chars, ${htmlBytes}/1048576 bytes`,
    );
  } catch (error) {
    failures.push(`${relativePath}: ${error.message}`);
  }
}

for (const [groupKey, group] of articleGroups) {
  for (const requiredName of articleNames) {
    if (!group.files.has(requiredName)) {
      failures.push(`${groupKey}: missing paired article ${requiredName}`);
    }
  }
  if (group.orders.size !== 1) {
    failures.push(`${groupKey}: paired articles must use the same series_order`);
  }
}

if (failures.length) {
  console.error("WeChat article check failed:");
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log("WeChat article check passed.");
