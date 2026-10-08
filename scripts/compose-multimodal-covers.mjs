import { execFile as execFileCallback } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";

const root = path.resolve(import.meta.dirname, "..");
const assets = path.join(root, "content/wechat/01-foundation-models-and-inference/submodules/02-multimodal/assets");
const execFile = promisify(execFileCallback);
const temp = await mkdtemp(path.join(tmpdir(), "multimodal-cover-"));
const specs = [
  {
    art: "multimodal-cover-main-art.png",
    output: "multimodal-cover-main-wechat.png",
    overlay: `<rect x="0" y="0" width="431" height="139" rx="0" fill="#fffaf2" opacity="0.82"/>
      <text x="40" y="70" font-family="Songti SC,STSongti-SC-Black,PingFang SC,sans-serif" font-size="58" font-weight="900" fill="#26393b">多模态模型</text>
      <text x="43" y="115" font-family="Songti SC,STSongti-SC-Black,PingFang SC,sans-serif" font-size="30" font-weight="800" fill="#42565a">发票读数为何填错栏</text>
      <rect x="0" y="325" width="900" height="58" fill="#fbf8f2" opacity="0.7"/>`,
  },
  {
    art: "multimodal-cover-interview-art.png",
    output: "multimodal-cover-interview-wechat.png",
    overlay: `<rect x="329" y="70" width="106" height="45" rx="14" fill="#fffaf2" opacity="0.91"/>
      <rect x="465" y="70" width="106" height="45" rx="14" fill="#fffaf2" opacity="0.91"/>
      <text x="382" y="102" text-anchor="middle" font-family="PingFang SC,Source Han Sans SC,sans-serif" font-size="34" font-weight="800" fill="#1f686c">认字</text>
      <text x="518" y="102" text-anchor="middle" font-family="PingFang SC,Source Han Sans SC,sans-serif" font-size="34" font-weight="800" fill="#a45632">归栏</text>`,
  },
];

try {
  for (const spec of specs) {
    const image = (await readFile(path.join(assets, spec.art))).toString("base64");
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="900" height="383" viewBox="0 0 900 383">
      <image href="data:image/png;base64,${image}" x="0" y="0" width="900" height="383" preserveAspectRatio="xMidYMid slice"/>
      ${spec.overlay}
    </svg>`;
    const source = path.join(temp, spec.output.replace(/\.png$/, ".svg"));
    const target = path.join(assets, spec.output);
    await writeFile(source, svg);
    await execFile("sips", ["-s", "format", "png", source, "--out", target]);
    console.log(path.relative(root, target));
  }
} finally {
  await rm(temp, { recursive: true, force: true });
}
