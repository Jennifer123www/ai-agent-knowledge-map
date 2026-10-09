import { execFile as execFileCallback } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";

const root = path.resolve(import.meta.dirname, "..");
const assets = path.join(root, "content/wechat/01-foundation-models-and-inference/submodules/02-multimodal/assets");
const base = (await readFile(path.join(assets, "multimodal-scene-base.png"))).toString("base64");
const temp = await mkdtemp(path.join(tmpdir(), "multimodal-scene-"));
const execFile = promisify(execFileCallback);
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1024" viewBox="0 0 1536 1024">
  <image href="data:image/png;base64,${base}" x="0" y="0" width="1536" height="1024"/>
  <g font-family="PingFang SC,Hiragino Sans GB,Source Han Sans SC,sans-serif" fill="#34464a" opacity="0.9">
    <text x="222" y="240" font-size="66" font-weight="600">酒店住宿发票</text>
    <text x="225" y="432" font-size="52">开票日期</text>
    <text x="810" y="432" font-size="55">9/3</text>
    <text x="225" y="592" font-size="52">含税金额</text>
    <text x="810" y="592" font-size="55">680.00</text>
    <text x="225" y="753" font-size="52">税额</text>
    <text x="810" y="753" font-size="55">38.49</text>
  </g>
</svg>`;
try {
  const source = path.join(temp, "scene.svg");
  await writeFile(source, svg);
  await execFile("sips", ["-s", "format", "png", source, "--out", path.join(assets, "multimodal-scene-invoice.png")]);
} finally {
  await rm(temp, { recursive: true, force: true });
}
