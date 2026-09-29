import { execFile as execFileCallback } from "node:child_process";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";

const root = path.resolve(import.meta.dirname, "..");
const outRoot = path.join(root, "content/wechat/evaluation-observability-and-improvement");
const execFile = promisify(execFileCallback);
const sources = Object.fromEntries(process.argv.slice(2).map((arg) => {
  const index = arg.indexOf("=");
  if (index < 1) throw new Error(`Expected group=/absolute/image.png, got ${arg}`);
  return [arg.slice(0, index), arg.slice(index + 1)];
}));

const groups = {
  overview: {
    dir: "assets", prefix: "evaluation",
    main: ["第七模块", "评测、可观测性", "与持续优化", "智能体到底把事情办成了吗"],
    interview: ["面试题", "评测、可观测性", "与持续优化", "怎样证明智能体真的可靠"],
  },
  trace: {
    dir: "submodules/trace/assets", prefix: "trace",
    main: ["链路追踪", "一句错答", "从哪里开始", "从结果回到证据与版本"],
    interview: ["链路追踪 · 面试题", "一条 Trace", "应该记录什么", "Span、采样与隐私治理"],
  },
  offlineeval: {
    dir: "submodules/offlineeval/assets", prefix: "offlineeval",
    main: ["离线评测", "先在模拟考场", "里见真章", "同一题目，同一环境，再比版本"],
    interview: ["离线评测 · 面试题", "离线成绩", "怎样避免虚高", "数据集、评分器与发布门槛"],
  },
  monitoring: {
    dir: "submodules/monitoring/assets", prefix: "monitoring",
    main: ["线上监控", "系统没报错", "为何用户仍不满", "穿过 HTTP 200 看见真实任务"],
    interview: ["线上监控 · 面试题", "Agent 监控", "到底看什么", "信号、SLO、告警与降级"],
  },
  release: {
    dir: "submodules/release/assets", prefix: "release",
    main: ["版本、实验与发布", "变好不能", "只凭感觉", "让每次改动都能归因与回退"],
    interview: ["版本发布 · 面试题", "Agent 怎样", "灰度与回滚", "影子、A/B、护栏与在途任务"],
  },
  feedback: {
    dir: "submodules/feedback/assets", prefix: "feedback",
    main: ["反馈闭环", "把差评变成", "可验证问题", "先归因，再优化，最后实验"],
    interview: ["反馈闭环 · 面试题", "怎样让反馈", "真正推动改进", "信号、样本、优先级与隐私"],
  },
};

const esc = (value) => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
const tempRoot = await mkdtemp(path.join(tmpdir(), "evaluation-covers-"));
for (const [id, spec] of Object.entries(groups)) {
  const source = sources[id];
  if (!source) throw new Error(`Missing source image: ${id}=/absolute/image.png`);
  const data = (await readFile(source)).toString("base64");
  for (const kind of ["main", "interview"]) {
    const [kicker, line1, line2, subtitle] = spec[kind];
    const accent = kind === "main" ? "#c96f35" : "#7b5068";
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="900" height="383" viewBox="0 0 900 383">
      <defs>
        <linearGradient id="shade" x1="0" x2="1"><stop offset="0" stop-color="#fffdf8" stop-opacity="0.98"/><stop offset="0.52" stop-color="#fffdf8" stop-opacity="0.82"/><stop offset="0.72" stop-color="#fffdf8" stop-opacity="0.08"/><stop offset="1" stop-color="#fffdf8" stop-opacity="0"/></linearGradient>
      </defs>
      <image href="data:image/png;base64,${data}" x="0" y="0" width="900" height="383" preserveAspectRatio="xMidYMid slice"/>
      <rect width="900" height="383" fill="url(#shade)"/>
      <rect x="54" y="48" width="8" height="35" rx="4" fill="${accent}"/>
      <text x="78" y="73" font-family="PingFang SC,Noto Sans CJK SC,sans-serif" font-size="22" font-weight="700" fill="${accent}">${esc(kicker)}</text>
      <text x="54" y="147" font-family="PingFang SC,Noto Sans CJK SC,sans-serif" font-size="44" font-weight="750" fill="#24292c">${esc(line1)}</text>
      <text x="54" y="202" font-family="PingFang SC,Noto Sans CJK SC,sans-serif" font-size="44" font-weight="750" fill="#24292c">${esc(line2)}</text>
      <path d="M54 236H335" stroke="${accent}" stroke-width="3"/>
      <text x="54" y="281" font-family="PingFang SC,Noto Sans CJK SC,sans-serif" font-size="23" font-weight="500" fill="#4f5b61">${esc(subtitle)}</text>
    </svg>`;
    const svgPath = path.join(tempRoot, `${id}-${kind}.svg`);
    const output = path.join(outRoot, spec.dir, `${spec.prefix}-cover-${kind}-wechat.png`);
    await mkdir(path.dirname(output), { recursive: true });
    await writeFile(svgPath, svg);
    await execFile("sips", ["-s", "format", "png", svgPath, "--out", output]);
    console.log(path.relative(root, output));
  }
}
await rm(tempRoot, { recursive: true, force: true });
