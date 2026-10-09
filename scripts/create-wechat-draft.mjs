import { access, mkdtemp, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { getWechatConfig } from "../lib/wechat/config.mjs";
import { createWechatClient, WechatApiError } from "../lib/wechat/client.mjs";
import { prepareWechatArticleImage } from "../lib/wechat/image.mjs";
import { parseWechatArticle, renderWechatHtml, validateWechatHtml } from "../lib/wechat/markdown.mjs";

const repositoryRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const defaultArticle = "content/wechat/05-tools-skills-and-protocols/beginner-main.md";

function parseArguments(argv) {
  const result = { file: defaultArticle, sideFile: null, theme: "orange", dryRun: false, upsert: false };
  let hasExplicitMainFile = false;
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--file") {
      result.file = argv[++index];
      hasExplicitMainFile = true;
    } else if (argv[index] === "--side-file") result.sideFile = argv[++index];
    else if (argv[index] === "--theme") result.theme = argv[++index];
    else if (argv[index] === "--dry-run") result.dryRun = true;
    else if (argv[index] === "--upsert") result.upsert = true;
    else throw new Error(`Unknown argument: ${argv[index]}`);
  }
  if (!result.file) throw new Error("--file requires an article path");
  if (argv.includes("--side-file") && !result.sideFile) throw new Error("--side-file requires an article path");
  if (result.sideFile && !hasExplicitMainFile) throw new Error("--side-file requires --file for the main article");
  if (result.sideFile && path.resolve(repositoryRoot, result.file) === path.resolve(repositoryRoot, result.sideFile)) {
    throw new Error("Main and side articles must be different files");
  }
  if (!["green", "orange"].includes(result.theme)) {
    throw new Error("--theme must be green or orange");
  }
  return result;
}

async function loadArticle(file) {
  const markdownPath = path.resolve(repositoryRoot, file);
  const markdown = await readFile(markdownPath, "utf8");
  const article = parseWechatArticle(markdown, markdownPath);
  for (const image of article.images) await access(image.absolutePath);
  return article;
}

function summarizeArticle(article, theme) {
  // Reserve room for WeChat's longer uploaded image URLs before any upload begins.
  const placeholderUrl = `https://mmbiz.qpic.cn/${"x".repeat(180)}`;
  const placeholderUrls = new Map(article.images.slice(1).map((image) => [
    image.source,
    placeholderUrl,
  ]));
  const content = renderWechatHtml(article, placeholderUrls, { theme });
  const contentSize = validateWechatHtml(content);
  return {
    title: article.title,
    theme,
    titleCharacters: [...article.title].length,
    author: article.author,
    authorCharacters: [...article.author].length,
    digest: article.digest,
    digestCharacters: [...article.digest].length,
    contentSourceUrl: article.contentSourceUrl,
    cover: path.relative(repositoryRoot, article.cover.absolutePath),
    inlineImages: article.images.slice(1).map((image) => path.relative(repositoryRoot, image.absolutePath)),
    htmlCharacters: contentSize.characters,
    htmlBytes: contentSize.bytes,
    imagesRequireWechatUpload: true,
  };
}

function validatePair(mainArticle, sideArticle) {
  for (const field of ["topic", "content_level", "submodule", "series_order"]) {
    const mainValue = mainArticle.metadata[field];
    const sideValue = sideArticle.metadata[field];
    if (mainValue != null && sideValue != null && mainValue !== sideValue) {
      throw new Error(`Main and side articles have different ${field} values`);
    }
  }
  if (mainArticle.order && sideArticle.order && mainArticle.order >= sideArticle.order) {
    throw new Error("Main article order must precede side article order");
  }
}

function draftTitles(item) {
  const articles = item?.content?.news_item ?? item?.news_item;
  if (!Array.isArray(articles)) throw new Error("WeChat returned a draft without news_item; refusing to guess its identity");
  return articles.map((article) => article.title);
}

function sameTitles(actual, expected) {
  return actual.length === expected.length && actual.every((title, index) => title === expected[index]);
}

async function findMatchingDraft(client, titles) {
  const matches = [];
  let offset = 0;
  while (true) {
    const page = await client.batchGetDrafts({ offset, count: 20 });
    if (!Array.isArray(page.item)) throw new Error("WeChat draft list is missing item; refusing to create a duplicate");
    if (!Number.isInteger(page.total_count) || page.total_count < 0) {
      throw new Error("WeChat draft list is missing total_count; refusing to create a duplicate");
    }
    for (const item of page.item) {
      if (sameTitles(draftTitles(item), titles)) matches.push(item.media_id);
    }
    offset += page.item.length;
    if (offset >= page.total_count) break;
    if (page.item.length === 0) throw new Error("WeChat draft list stopped before total_count; refusing to create a duplicate");
  }
  if (matches.length > 1) throw new Error(`Found ${matches.length} drafts with the same ordered titles; refusing ambiguous overwrite`);
  if (!matches.length) return null;
  const mediaId = matches[0];
  const existing = await client.getDraft(mediaId);
  if (!sameTitles(draftTitles(existing), titles)) throw new Error("Draft changed during lookup; refusing to overwrite it");
  return mediaId;
}

function normalizedText(html) {
  return html.replace(/<[^>]*>/g, "").replace(/&(?:nbsp|amp|lt|gt|quot|#39);/gi, "").replace(/\s+/g, "");
}

async function verifyDraft(client, mediaId, expectedArticles) {
  const actual = (await client.getDraft(mediaId)).news_item;
  if (!Array.isArray(actual) || actual.length !== expectedArticles.length) {
    throw new Error(`Draft ${mediaId} has an unexpected article count after upload`);
  }
  for (let index = 0; index < expectedArticles.length; index += 1) {
    const expected = expectedArticles[index];
    const received = actual[index];
    const leadingText = normalizedText(expected.content).slice(0, 50);
    if (received.title !== expected.title || received.author !== expected.author ||
        !normalizedText(received.content || "").includes(leadingText)) {
      throw new Error(`Draft ${mediaId} article ${index + 1} does not match the submitted title, author, or opening text`);
    }
  }
}

async function main() {
  const options = parseArguments(process.argv.slice(2));
  const articles = [await loadArticle(options.file)];
  if (options.sideFile) {
    articles.push(await loadArticle(options.sideFile));
    validatePair(articles[0], articles[1]);
  }

  if (options.dryRun) {
    const summaries = articles.map((article) => summarizeArticle(article, options.theme));
    console.log(JSON.stringify(options.sideFile
      ? { theme: options.theme, articleCount: summaries.length, articles: summaries }
      : summaries[0], null, 2));
    return;
  }

  const config = getWechatConfig({ requireCredentials: true });
  const client = createWechatClient(config);
  const existingMediaId = options.upsert
    ? await findMatchingDraft(client, articles.map((article) => article.title))
    : null;
  if (options.upsert) console.log(existingMediaId
    ? `Updating matching draft in place: ${existingMediaId}`
    : "No matching draft found; creating one new draft");
  const temporaryDirectory = await mkdtemp(path.join(os.tmpdir(), "wechat-draft-"));
  try {
    const uploadedBodyImages = new Map();
    const draftArticles = [];
    for (const article of articles) {
      console.log(`Uploading cover: ${path.relative(repositoryRoot, article.cover.absolutePath)}`);
      const cover = await client.uploadImage(article.cover.absolutePath, { permanent: true });

      const uploadedImageUrls = new Map();
      for (const image of article.images.slice(1)) {
        let uploadedUrl = uploadedBodyImages.get(image.absolutePath);
        if (!uploadedUrl) {
          const uploadPath = await prepareWechatArticleImage(image.absolutePath, temporaryDirectory);
          const compressed = uploadPath !== image.absolutePath ? " (compressed for WeChat)" : "";
          console.log(`Uploading article image: ${path.relative(repositoryRoot, image.absolutePath)}${compressed}`);
          const uploaded = await client.uploadImage(uploadPath);
          uploadedUrl = uploaded.url;
          uploadedBodyImages.set(image.absolutePath, uploadedUrl);
        }
        uploadedImageUrls.set(image.source, uploadedUrl);
      }

      const content = renderWechatHtml(article, uploadedImageUrls, { theme: options.theme });
      draftArticles.push({
        article_type: article.articleType,
        title: article.title,
        author: article.author || config.author,
        digest: article.digest,
        content,
        content_source_url: article.contentSourceUrl || config.contentSourceUrl,
        thumb_media_id: cover.media_id,
        need_open_comment: article.needOpenComment,
        only_fans_can_comment: article.onlyFansCanComment,
      });
    }
    let mediaId = existingMediaId;
    if (mediaId) {
      for (let index = 0; index < draftArticles.length; index += 1) {
        try {
          await client.updateDraft(mediaId, index, draftArticles[index]);
        } catch (error) {
          throw new Error(`Draft ${mediaId} may be partially updated (failed at article ${index + 1}); inspect it before retrying`, { cause: error });
        }
      }
    } else {
      const result = await client.addDraft(draftArticles);
      mediaId = result.media_id;
    }
    await verifyDraft(client, mediaId, draftArticles);
    console.log(`Draft ${existingMediaId ? "updated" : "created"} and verified. articles=${draftArticles.length} media_id=${mediaId}`);
  } finally {
    await rm(temporaryDirectory, { recursive: true, force: true });
  }
}

main().catch((error) => {
  if (error instanceof WechatApiError && error.code === 40164) {
    console.error(`${error.message}\nAdd this machine or server's public egress IP to the WeChat API IP allowlist.`);
  } else {
    console.error(error.stack || error.message);
  }
  process.exitCode = 1;
});
