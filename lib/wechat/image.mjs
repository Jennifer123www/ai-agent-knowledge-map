import { execFile } from "node:child_process";
import { stat } from "node:fs/promises";
import path from "node:path";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
export const WECHAT_ARTICLE_IMAGE_LIMIT = 1024 * 1024;

export async function prepareWechatArticleImage(filePath, outputDirectory) {
  const source = await stat(filePath);
  if (source.size <= WECHAT_ARTICLE_IMAGE_LIMIT) return filePath;

  if (process.platform !== "darwin") {
    throw new Error(
      `Article image exceeds 1 MB and needs compression before upload: ${filePath}`,
    );
  }

  const attempts = [
    { width: 1280, quality: 78 },
    { width: 1080, quality: 72 },
    { width: 960, quality: 68 },
  ];
  for (const attempt of attempts) {
    const outputPath = path.join(
      outputDirectory,
      `${path.parse(filePath).name}-${attempt.width}-${attempt.quality}.jpg`,
    );
    await execFileAsync("/usr/bin/sips", [
      "-s",
      "format",
      "jpeg",
      "-s",
      "formatOptions",
      String(attempt.quality),
      "--resampleWidth",
      String(attempt.width),
      filePath,
      "--out",
      outputPath,
    ]);
    if ((await stat(outputPath)).size <= WECHAT_ARTICLE_IMAGE_LIMIT) {
      return outputPath;
    }
  }

  throw new Error(`Unable to compress article image below 1 MB: ${filePath}`);
}
