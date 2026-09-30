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
      <image href="data:image/png;base64,${image}" x="0" y="0" width="900" height="383" preserveAspectRatio="xMidYMid slice"/>
      <rect x="0" y="0" width="900" height="132" fill="#fffaf2" opacity="0.28"/>
      <text x="450" y="61" text-anchor="middle" font-family="Songti SC,STSongti-SC-Black,PingFang SC,sans-serif" font-size="54" font-weight="900" fill="#22272a">知识<tspan fill="#1c756b">库</tspan></text>
      <text x="450" y="108" text-anchor="middle" font-family="Songti SC,STSongti-SC-Black,PingFang SC,sans-serif" font-size="29" font-weight="760" fill="#2b3033">资料进库之后，谁保证它还管用</text>
    </svg>`,
  },
  {
    source: interviewSource,
    output: "kb-cover-interview-wechat.png",
    svg: ({ image }) => `<svg xmlns="http://www.w3.org/2000/svg" width="900" height="383" viewBox="0 0 900 383">
      <image href="data:image/png;base64,${image}" x="0" y="0" width="900" height="383" preserveAspectRatio="xMidYMid slice"/>
      <rect x="0" y="0" width="900" height="132" fill="#fffaf2" opacity="0.32"/>
      <text x="450" y="59" text-anchor="middle" font-family="Songti SC,STSongti-SC-Black,PingFang SC,sans-serif" font-size="48" font-weight="900" fill="#b01849">面试题：知识库</text>
      <text x="450" y="106" text-anchor="middle" font-family="Songti SC,STSongti-SC-Black,PingFang SC,sans-serif" font-size="30" font-weight="780" fill="#1b6558">怎样避免旧资料答新问题</text>
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
