import { access, mkdtemp, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { getWechatConfig } from "../lib/wechat/config.mjs";
import { createWechatClient, WechatApiError } from "../lib/wechat/client.mjs";
import { prepareWechatArticleImage } from "../lib/wechat/image.mjs";
import { parseWechatArticle, renderWechatHtml } from "../lib/wechat/markdown.mjs";

const repositoryRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const defaultArticle = "content/wechat/tools-skills-and-protocols/beginner-main.md";

function parseArguments(argv) {
  const result = { file: defaultArticle, dryRun: false };
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--file") result.file = argv[++index];
    else if (argv[index] === "--dry-run") result.dryRun = true;
    else throw new Error(`Unknown argument: ${argv[index]}`);
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
    console.log(JSON.stringify({
      title: article.title,
      digest: article.digest,
      cover: path.relative(repositoryRoot, article.cover.absolutePath),
      inlineImages: article.images.slice(1).map((image) => path.relative(repositoryRoot, image.absolutePath)),
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

    const content = renderWechatHtml(article, uploadedImageUrls);
    const result = await client.addDraft({
      title: article.title,
      author: config.author,
      digest: article.digest,
      content,
      content_source_url: config.contentSourceUrl,
      thumb_media_id: cover.media_id,
      need_open_comment: 0,
      only_fans_can_comment: 0,
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
