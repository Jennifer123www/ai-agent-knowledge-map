import { execFile as execFileCallback } from "node:child_process";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";
import { modules } from "./generate-remaining-wechat-series.mjs";

const root = path.resolve(import.meta.dirname, "..");
const execFile = promisify(execFileCallback);
const requestedModules = new Set(process.argv.slice(2));
const tempRoot = await mkdtemp(path.join(tmpdir(), "remaining-wechat-figures-"));
const W = 1536; const H = 1024;
const paper = "#fffdf8"; const ink = "#272a2d"; const muted = "#667178";
const orange = "#ce6d2d"; const teal = "#2f7d78"; const blue = "#47738d"; const plum = "#76546f"; const rose = "#a75f55";
const colors = [orange, teal, blue, plum, rose];
const fills = ["#fff1e6", "#ecf6f3", "#edf3f7", "#f5eef3", "#faeeee"];
const font = "'PingFang SC','Noto Sans CJK SC','Hiragino Sans GB',sans-serif";
const esc = (value) => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
const rect = (x, y, w, h, fill = "#fff", stroke = "#cad3d5", radius = 16, width = 2) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${fill}" stroke="${stroke}" stroke-width="${width}"/>`;
const text = (x, y, value, size = 28, color = ink, anchor = "middle", weight = 500) => `<text x="${x}" y="${y}" fill="${color}" text-anchor="${anchor}" font-family="${font}" font-size="${size}" font-weight="${weight}">${esc(value)}</text>`;
const wrap = (value, maxChars) => {
  const chars = [...String(value)]; const lines = [];
  while (chars.length) lines.push(chars.splice(0, maxChars).join(""));
  return lines.length ? lines : [""];
};
const multi = (x, y, value, maxChars, size = 24, color = ink, anchor = "middle", weight = 500, lineHeight = 1.4) => {
  const lines = wrap(value, maxChars);
  return lines.map((line, index) => text(x, y + index * size * lineHeight, line, size, color, anchor, weight)).join("");
};
const arrowHead = (x, y, fx, fy, color = muted) => {
  const angle = Math.atan2(y - fy, x - fx); const rx = x - 16 * Math.cos(angle); const ry = y - 16 * Math.sin(angle);
  const sx = 8 * Math.sin(angle); const sy = 8 * Math.cos(angle);
  return `<path d="M${x} ${y}L${rx + sx} ${ry - sy}L${rx - sx} ${ry + sy}Z" fill="${color}"/>`;
};
const line = (x1, y1, x2, y2, color = muted, width = 3) => `<path d="M${x1} ${y1}L${x2} ${y2}" fill="none" stroke="${color}" stroke-width="${width}"/>${arrowHead(x2, y2, x1, y1, color)}`;
const canvas = (title, eyebrow, body, source) => `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <rect width="${W}" height="${H}" fill="${paper}"/>
  <path d="M72 170H1464" stroke="#d7dfe0" stroke-width="2"/>
  ${text(72, 76, eyebrow, 22, orange, "start", 700)}
  ${text(72, 138, title, 46, ink, "start", 760)}
  ${body}
  <path d="M72 922H1464" stroke="#d7dfe0" stroke-width="2"/>
  ${multi(72, 958, source, 78, 18, muted, "start", 450, 1.25)}
</svg>`;

function nodeBox(x, y, w, h, name, detail, color, fill) {
  return rect(x, y, w, h, fill, color) + `<rect x="${x}" y="${y}" width="8" height="${h}" rx="4" fill="${color}"/>`
    + multi(x + w / 2 + 4, y + 49, name, 7, 25, ink, "middle", 720, 1.25)
    + multi(x + w / 2 + 4, y + 103, detail, 9, 19, muted, "middle", 500, 1.25);
}

function drawPrinciple(group) {
  const gap = 34; const x0 = 65; const total = 1406; const width = (total - gap * 4) / 5; const y = 335; let body = "";
  group.nodes.forEach(([name, detail], index) => {
    const x = x0 + index * (width + gap);
    body += nodeBox(x, y, width, 220, name, detail, colors[index], fills[index]);
    if (index < 4) body += line(x + width, y + 110, x + width + gap, y + 110, colors[index + 1], 3);
  });
  body += rect(210, 690, 1116, 94, "#fff6ec", "#e4b690", 14) + multi(768, 734, group.tagline, 36, 22, ink, "middle", 600, 1.25);
  return body;
}

function drawInputs(group) {
  let body = rect(145, 224, 1246, 610, "#fff", "#c7d1d3", 14);
  body += rect(145, 224, 1246, 76, "#edf3f7", blue, 14, 0) + text(768, 274, "字段不仅要有值，还要有来源、版本与缺失处理", 26, blue, "middle", 720);
  group.inputs.forEach(([name, detail], index) => {
    const y = 300 + index * 106;
    body += `<path d="M145 ${y}H1391" stroke="#dce3e4" stroke-width="2"/>`;
    body += rect(180, y + 20, 230, 65, fills[index], colors[index], 12) + text(295, y + 62, name, 23, colors[index], "middle", 720);
    body += multi(470, y + 55, detail, 38, 23, ink, "start", 520, 1.25);
  });
  return body;
}

function drawFailures(group) {
  let body = text(768, 225, "同样的表面错误，可能来自完全不同的故障层", 27, muted, "middle", 600);
  const xs = [88, 540, 992];
  group.failures.forEach((failure, index) => {
    body += rect(xs[index], 300, 360, 400, fills[index === 0 ? 4 : index], colors[index === 0 ? 4 : index], 18, 3);
    body += text(xs[index] + 180, 365, `失效 ${index + 1}`, 27, colors[index === 0 ? 4 : index], "middle", 760);
    body += multi(xs[index] + 180, 440, failure, 12, 26, ink, "middle", 620, 1.45);
    body += multi(xs[index] + 180, 620, ["先找污染入口", "再查权限与规则", "最后核对状态回执"][index], 12, 21, muted, "middle", 500, 1.35);
  });
  body += rect(280, 755, 976, 82, "#fff6ec", "#e4b690", 14) + text(768, 807, "不要先把所有失败都归为“模型不稳定”", 23, ink, "middle", 650);
  return body;
}

function drawControls(group) {
  let body = "";
  group.controls.forEach((control, index) => {
    const x = 182 + index * 292; const y = 300 + (index % 2) * 80;
    body += rect(x, y, 250, 320, fills[index], colors[index], 22, 3);
    body += `<circle cx="${x + 125}" cy="${y + 72}" r="34" fill="${colors[index]}"/>` + text(x + 125, y + 82, String(index + 1), 28, "#fff", "middle", 760);
    body += multi(x + 125, y + 150, control, 8, 26, ink, "middle", 720, 1.35);
    body += multi(x + 125, y + 260, ["减少错误进入", "限制错误决定", "阻止危险执行", "支持追溯改进"][index], 8, 20, muted, "middle", 520, 1.3);
  });
  body += line(432, 460, 474, 460, teal, 3) + line(724, 540, 766, 540, blue, 3) + line(1016, 460, 1058, 460, plum, 3);
  return body;
}

function drawVerification(group) {
  const steps = [["正常样本", "任务能按合同完成"], ["边界样本", "缺值、冲突与极端输入"], ["故障注入", "超时、重复、权限变化"], ["受控灰度", "限制流量、权限与预算"], ["持续监控", "从指标回到任务证据"]];
  const gap = 34; const x0 = 65; const total = 1406; const width = (total - gap * 4) / 5; let body = "";
  steps.forEach(([name, detail], index) => {
    const x = x0 + index * (width + gap);
    body += nodeBox(x, 300, width, 205, name, detail, colors[index], fills[index]);
    if (index < 4) body += line(x + width, 402, x + width + gap, 402, colors[index + 1], 3);
  });
  body += rect(130, 655, 1276, 160, "#fff", "#c8d3d5", 14);
  body += text(180, 710, "关注指标", 24, orange, "start", 760);
  body += multi(180, 758, group.metrics.join("　｜　"), 52, 23, ink, "start", 560, 1.35);
  return body;
}

function groupRoot(module, group) {
  return path.join(root, "content", "wechat", module.slug, group.id === "overview" ? "" : `submodules/${group.id}`);
}

for (const module of modules) {
  if (requestedModules.size && !requestedModules.has(module.slug)) continue;
  for (const group of module.groups) {
    const assetRoot = path.join(groupRoot(module, group), "assets");
    await mkdir(assetRoot, { recursive: true });
    const figures = [
      ["principle", group.principleTitle, "原理示意图", drawPrinciple(group)],
      ["inputs", `${group.name}的关键输入`, "输入与契约", drawInputs(group)],
      ["failure", `${group.name}的典型失效`, "故障归因", drawFailures(group)],
      ["controls", `${group.name}的多层控制`, "控制组合", drawControls(group)],
      ["verification", `${group.name}怎样验证`, "验证闭环", drawVerification(group)],
    ];
    for (const [suffix, title, eyebrow, body] of figures) {
      const filename = `${group.prefix}-${suffix}.png`;
      const source = suffix === "principle"
        ? `资料：${group.sources.map(([label]) => label).join("；")}。教学改绘。`
        : `内容依据本文“${group.name}”案例整理；示意数据不代表真实生产统计。`;
      const svgPath = path.join(tempRoot, `${module.slug}-${group.id}-${suffix}.svg`);
      const output = path.join(assetRoot, filename);
      await writeFile(svgPath, canvas(title, eyebrow, body, source));
      await execFile("sips", ["-s", "format", "png", svgPath, "--out", output]);
      console.log(path.relative(root, output));
    }
  }
}

await rm(tempRoot, { recursive: true, force: true });
