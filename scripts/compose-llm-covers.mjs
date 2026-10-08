import { execFile as execFileCallback } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";

const [mainSource, interviewSource] = process.argv.slice(2);
if (!mainSource || !interviewSource) {
  throw new Error("Usage: node scripts/compose-llm-covers.mjs <main-background.png> <interview-background.png>");
}

const root = path.resolve(import.meta.dirname, "..");
const outputRoot = path.join(
  root,
  "content/wechat/01-foundation-models-and-inference/submodules/01-llm/assets",
);
const execFile = promisify(execFileCallback);
const tempRoot = await mkdtemp(path.join(tmpdir(), "llm-covers-"));

const specs = [
  {
    source: mainSource,
    output: "llm-cover-wechat-horizontal-v2.png",
    svg: ({ image }) => `<svg xmlns="http://www.w3.org/2000/svg" width="900" height="383" viewBox="0 0 900 383">
      <rect x="0" y="0" width="900" height="383" fill="#fbf8f0"/>
      <image href="data:image/png;base64,${image}" x="0" y="70" width="900" height="383" preserveAspectRatio="xMidYMid slice"/>
      <rect x="0" y="0" width="900" height="124" fill="#fffaf2" opacity="0.46"/>
      <rect x="0" y="325" width="900" height="58" fill="#fbf8f0" opacity="0.97"/>
      <text x="450" y="59" text-anchor="middle" font-family="Songti SC,STSongti-SC-Black,PingFang SC,sans-serif" font-size="58" font-weight="900" fill="#22272a">大语言<tspan fill="#1c756b">模型</tspan></text>
      <text x="450" y="105" text-anchor="middle" font-family="Songti SC,STSongti-SC-Black,PingFang SC,sans-serif" font-size="30" font-weight="760" fill="#2b3033">它为什么能一句接一句</text>
    </svg>`,
  },
  {
    source: interviewSource,
    output: "llm-cover-interview-wechat.png",
    svg: ({ image }) => `<svg xmlns="http://www.w3.org/2000/svg" width="900" height="383" viewBox="0 0 900 383">
      <image href="data:image/png;base64,${image}" x="0" y="0" width="900" height="383" preserveAspectRatio="xMidYMid slice"/>
      <text x="342" y="325" text-anchor="middle" font-family="PingFang SC,Source Han Sans SC,Noto Sans CJK SC,sans-serif" font-size="34" font-weight="800" fill="#a14e2d">原理</text>
      <text x="558" y="325" text-anchor="middle" font-family="PingFang SC,Source Han Sans SC,Noto Sans CJK SC,sans-serif" font-size="34" font-weight="800" fill="#24674f">验证</text>
    </svg>`,
  },
];

for (const spec of specs) {
  const image = (await readFile(spec.source)).toString("base64");
  const svgPath = path.join(tempRoot, spec.output.replace(/\.png$/, ".svg"));
  const outputPath = path.join(outputRoot, spec.output);
  await writeFile(svgPath, spec.svg({ image }));
  await execFile("sips", ["-s", "format", "png", svgPath, "--out", outputPath]);
  console.log(path.relative(root, outputPath));
}

await rm(tempRoot, { recursive: true, force: true });
