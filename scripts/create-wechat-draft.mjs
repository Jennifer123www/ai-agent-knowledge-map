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

function parseArguments(argv) {
  const result = { file: defaultArticle, theme: "green", dryRun: false };
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--file") result.file = argv[++index];
    else if (argv[index] === "--theme") result.theme = argv[++index];
    else if (argv[index] === "--dry-run") result.dryRun = true;
    else throw new Error(`Unknown argument: ${argv[index]}`);
  }
  if (!result.file) throw new Error("--file requires an article path");
  if (!["green", "orange"].includes(result.theme)) {
    throw new Error("--theme must be green or orange");
  }
  return result;
}

async function main() {
  const options = parseArguments(process.argv.slice(2));
  const markdownPath = path.resolve(repositoryRoot, options.file);
  const markdown = await readFile(markdownPath, "utf8");
  const article = parseWechatArticle(markdown, markdownPath);
  for (const image of article.images) await access(image.absolutePath);

  if (options.dryRun) {
    const placeholderUrls = new Map(article.images.slice(1).map((image) => [
      image.source,
      `https://mmbiz.qpic.cn/placeholder/${encodeURIComponent(path.basename(image.source))}`,
    ]));
    const content = renderWechatHtml(article, placeholderUrls, { theme: options.theme });
    const contentSize = validateWechatHtml(content);
    console.log(JSON.stringify({
      title: article.title,
      theme: options.theme,
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
    }, null, 2));
    return;
  }

  const config = getWechatConfig({ requireCredentials: true });
  const client = createWechatClient(config);
  const temporaryDirectory = await mkdtemp(path.join(os.tmpdir(), "wechat-draft-"));
  try {
    console.log(`Uploading cover: ${path.relative(repositoryRoot, article.cover.absolutePath)}`);
    const cover = await client.uploadImage(article.cover.absolutePath, { permanent: true });

    const uploadedImageUrls = new Map();
    for (const image of article.images.slice(1)) {
      const uploadPath = await prepareWechatArticleImage(image.absolutePath, temporaryDirectory);
      const compressed = uploadPath !== image.absolutePath ? " (compressed for WeChat)" : "";
      console.log(`Uploading article image: ${path.relative(repositoryRoot, image.absolutePath)}${compressed}`);
      const uploaded = await client.uploadImage(uploadPath);
      uploadedImageUrls.set(image.source, uploaded.url);
    }

    const content = renderWechatHtml(article, uploadedImageUrls, { theme: options.theme });
    const result = await client.addDraft({
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
    console.log(`Draft created successfully. media_id=${result.media_id}`);
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
