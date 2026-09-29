import { access, mkdtemp, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { getWechatConfig } from "../lib/wechat/config.mjs";
import { createWechatClient, WechatApiError } from "../lib/wechat/client.mjs";
import { prepareWechatArticleImage } from "../lib/wechat/image.mjs";
import { parseWechatArticle, renderWechatHtml, validateWechatHtml } from "../lib/wechat/markdown.mjs";

const repositoryRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const defaultArticle = "content/wechat/tools-skills-and-protocols/beginner-main.md";
// Layouts inspired by public theme galleries; no third-party CSS or image assets are copied.
const sampleThemes = [
  { theme: "warm-paper", label: "A 暖陶米白", prefix: "【A 暖陶米白】", signature: "#FFFCF8" },
  { theme: "simple-elegant", label: "B 简洁优雅", prefix: "【B 简洁优雅】", signature: "#39735C" },
  { theme: "tech-blue", label: "C 技术蓝", prefix: "【C 技术蓝】", signature: "#EAF3F9" },
];

function parseArguments(argv) {
  const result = { file: defaultArticle, sideFile: null, theme: "green", dryRun: false, sampleThemes: false };
  let hasExplicitMainFile = false;
  let hasExplicitTheme = false;
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--file") {
      result.file = argv[++index];
      hasExplicitMainFile = true;
    } else if (argv[index] === "--side-file") {
      result.sideFile = argv[++index];
    } else if (argv[index] === "--theme") {
      result.theme = argv[++index];
      hasExplicitTheme = true;
    } else if (argv[index] === "--sample-themes") {
      result.sampleThemes = true;
    } else if (argv[index] === "--dry-run") {
      result.dryRun = true;
    } else {
      throw new Error(`Unknown argument: ${argv[index]}`);
    }
  }
  if (!result.file) throw new Error("--file requires an article path");
  if (argv.includes("--side-file") && !result.sideFile) throw new Error("--side-file requires an article path");
  if (result.sideFile && !hasExplicitMainFile) throw new Error("--side-file requires --file for the main article");
  if (result.sideFile && path.resolve(repositoryRoot, result.file) === path.resolve(repositoryRoot, result.sideFile)) {
    throw new Error("Main and side articles must be different files");
  }
  if (!["green", "orange", ...sampleThemes.map((sample) => sample.theme)].includes(result.theme)) {
    throw new Error("--theme must be green, orange, warm-paper, simple-elegant, or tech-blue");
  }
  if (result.sampleThemes && hasExplicitTheme) throw new Error("--sample-themes cannot be combined with --theme");
  if (result.sampleThemes && !result.sideFile) throw new Error("--sample-themes requires --side-file");
  return result;
}

async function loadArticle(file) {
  const markdownPath = path.resolve(repositoryRoot, file);
  const markdown = await readFile(markdownPath, "utf8");
  const article = parseWechatArticle(markdown, markdownPath);
  for (const image of article.images) await access(image.absolutePath);
  return article;
}

function draftTitle(article, variant) {
  const title = `${variant.prefix || ""}${article.title}`;
  if ([...title].length > 32) throw new Error(`Sample draft title exceeds 32 characters: ${title}`);
  return title;
}

function draftDigest(article, variant) {
  const digest = variant.prefix ? `排版样稿，请勿发布。${article.digest}` : article.digest;
  if ([...digest].length > 120) throw new Error(`Sample draft digest exceeds 120 characters: ${draftTitle(article, variant)}`);
  return digest;
}

function summarizeArticle(article, variant) {
  // Reserve room for WeChat's longer uploaded image URLs before any upload begins.
  const placeholderUrl = `https://mmbiz.qpic.cn/${"x".repeat(180)}`;
  const placeholderUrls = new Map(article.images.slice(1).map((image) => [
    image.source,
    placeholderUrl,
  ]));
  const content = renderWechatHtml(article, placeholderUrls, { theme: variant.theme });
  const contentSize = validateWechatHtml(content);
  const title = draftTitle(article, variant);
  const digest = draftDigest(article, variant);
  return {
    title,
    theme: variant.theme,
    titleCharacters: [...title].length,
    author: article.author,
    authorCharacters: [...article.author].length,
    digest,
    digestCharacters: [...digest].length,
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

async function main() {
  const options = parseArguments(process.argv.slice(2));
  const variants = options.sampleThemes ? sampleThemes : [{ theme: options.theme, prefix: "" }];
  const articles = [await loadArticle(options.file)];
  if (options.sideFile) {
    articles.push(await loadArticle(options.sideFile));
    validatePair(articles[0], articles[1]);
  }

  const previews = variants.map((variant) => ({
    theme: variant.theme,
    label: variant.label,
    articleCount: articles.length,
    articles: articles.map((article) => summarizeArticle(article, variant)),
  }));
  if (options.dryRun) {
    console.log(JSON.stringify(options.sampleThemes
      ? { sampleCount: previews.length, drafts: previews }
      : options.sideFile ? previews[0] : previews[0].articles[0], null, 2));
    return;
  }

  const config = getWechatConfig({ requireCredentials: true });
  const client = createWechatClient(config);
  const temporaryDirectory = await mkdtemp(path.join(os.tmpdir(), "wechat-draft-"));
  try {
    const uploadedBodyImages = new Map();
    const preparedArticles = [];
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

      preparedArticles.push({ article, cover, uploadedImageUrls });
    }
    for (const variant of variants) {
      const draftArticles = preparedArticles.map(({ article, cover, uploadedImageUrls }) => ({
        article_type: article.articleType,
        title: draftTitle(article, variant),
        author: article.author || config.author,
        digest: draftDigest(article, variant),
        content: renderWechatHtml(article, uploadedImageUrls, { theme: variant.theme }),
        content_source_url: article.contentSourceUrl || config.contentSourceUrl,
        thumb_media_id: cover.media_id,
        need_open_comment: article.needOpenComment,
        only_fans_can_comment: article.onlyFansCanComment,
      }));
      const result = await client.addDraft(draftArticles);
      console.log(`Draft created successfully. theme=${variant.theme} articles=${draftArticles.length} media_id=${result.media_id}`);
      if (options.sampleThemes) {
        try {
          const saved = await client.getDraft(result.media_id);
          const savedArticles = saved.news_item;
          const correctOrder = Array.isArray(savedArticles)
            && savedArticles.length === draftArticles.length
            && savedArticles.every((item, index) => item.title === draftArticles[index].title);
          const signatureRetained = correctOrder
            && savedArticles.every((item) => item.content?.includes(variant.signature));
          if (!correctOrder || !signatureRetained) {
            console.warn(`Draft readback needs visual inspection. theme=${variant.theme} order=${correctOrder} style=${signatureRetained}`);
          } else {
            console.log(`Draft readback verified. theme=${variant.theme} articles=${savedArticles.length} style=retained`);
          }
        } catch (error) {
          console.warn(`Draft created, but readback failed. theme=${variant.theme} media_id=${result.media_id} reason=${error.message}`);
        }
      }
    }
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
