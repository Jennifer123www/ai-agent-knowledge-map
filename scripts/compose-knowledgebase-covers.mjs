import { execFile as execFileCallback } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";

const [mainSource, interviewSource] = process.argv.slice(2);
if (!mainSource || !interviewSource) {
  throw new Error("Usage: node scripts/compose-knowledgebase-covers.mjs <main-background.png> <interview-background.png>");
}

const root = path.resolve(import.meta.dirname, "..");
const outputRoot = path.join(
  root,
  "content/wechat/02-knowledge-retrieval-and-rag/submodules/01-knowledgebase/assets",
);
const execFile = promisify(execFileCallback);
const tempRoot = await mkdtemp(path.join(tmpdir(), "knowledgebase-covers-"));

const specs = [
  {
    source: mainSource,
    output: "kb-cover-main-wechat.png",
    svg: ({ image }) => `<svg xmlns="http://www.w3.org/2000/svg" width="900" height="383" viewBox="0 0 900 383">
      <rect x="0" y="0" width="900" height="383" fill="#fbf8f0"/>
      <image href="data:image/png;base64,${image}" x="0" y="70" width="900" height="383" preserveAspectRatio="xMidYMid slice"/>
      <rect x="0" y="0" width="900" height="124" fill="#fffaf2" opacity="0.46"/>
      <rect x="0" y="325" width="900" height="58" fill="#fbf8f0" opacity="0.97"/>
      <text x="450" y="59" text-anchor="middle" font-family="Songti SC,STSongti-SC-Black,PingFang SC,sans-serif" font-size="58" font-weight="900" fill="#22272a">知识<tspan fill="#1c756b">库</tspan></text>
      <text x="450" y="105" text-anchor="middle" font-family="Songti SC,STSongti-SC-Black,PingFang SC,sans-serif" font-size="30" font-weight="760" fill="#2b3033">资料进库之后，谁保证它还管用</text>
    </svg>`,
  },
  {
    source: interviewSource,
    output: "kb-cover-interview-wechat.png",
    svg: ({ image }) => `<svg xmlns="http://www.w3.org/2000/svg" width="900" height="383" viewBox="0 0 900 383">
      <image href="data:image/png;base64,${image}" x="0" y="0" width="900" height="383" preserveAspectRatio="xMidYMid slice"/>
      <text x="343" y="325" text-anchor="middle" font-family="PingFang SC,Source Han Sans SC,Noto Sans CJK SC,sans-serif" font-size="34" font-weight="800" fill="#9d2d2d">旧版</text>
      <text x="558" y="325" text-anchor="middle" font-family="PingFang SC,Source Han Sans SC,Noto Sans CJK SC,sans-serif" font-size="34" font-weight="800" fill="#24674f">有效版</text>
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
