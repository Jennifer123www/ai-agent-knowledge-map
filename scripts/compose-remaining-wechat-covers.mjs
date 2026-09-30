import { execFile as execFileCallback } from "node:child_process";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";
import { modules } from "./generate-remaining-wechat-series.mjs";

const root = path.resolve(import.meta.dirname, "..");
const execFile = promisify(execFileCallback);
const sources = Object.fromEntries(process.argv.slice(2).map((argument) => {
  const index = argument.indexOf("=");
  if (index < 1) throw new Error(`Expected module=/absolute/background.png, got ${argument}`);
  return [argument.slice(0, index), argument.slice(index + 1)];
}));
const tempRoot = await mkdtemp(path.join(tmpdir(), "remaining-wechat-covers-"));
const esc = (value) => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
const splitTitle = (value, max = 12) => {
  const clean = value.replace(/^大话/, "").replace(/^面试题[：:]?/, "");
  const parts = clean.split(/[：:]/).filter(Boolean);
  if (parts.length > 1 && [...parts[0]].length <= max && [...parts.slice(1).join("：")].length <= max + 2) {
    return [parts[0], parts.slice(1).join("：")];
  }
  const chars = [...clean]; const lines = [];
  while (chars.length && lines.length < 3) lines.push(chars.splice(0, max).join(""));
  if (chars.length) lines[2] += chars.join("");
  return lines;
};
const groupDirectory = (module, group) => group.id === "overview"
  ? ""
  : `submodules/${String(module.groups.indexOf(group)).padStart(2, "0")}-${group.id}`;

for (const module of modules) {
  const source = sources[module.slug];
  if (!source) continue;
  const data = (await readFile(source)).toString("base64");
  for (const [index, group] of module.groups.entries()) {
    for (const kind of ["main", "interview"]) {
      const titleValue = kind === "main" ? group.mainTitle : group.interviewTitle;
      const lines = splitTitle(titleValue);
      const accent = kind === "main" ? "#ce6d2d" : "#2f7d78";
      const kicker = kind === "main" ? `大话系列 · ${module.title}` : `面试题 · ${module.title}`;
      const fontSize = lines.some((line) => [...line].length > 12) ? 38 : 44;
      const titleSvg = lines.map((line, lineIndex) => `<text x="54" y="${142 + lineIndex * 56}" font-family="PingFang SC,Noto Sans CJK SC,sans-serif" font-size="${fontSize}" font-weight="760" fill="#24292c">${esc(line)}</text>`).join("");
      const subtitleY = Math.min(330, 142 + lines.length * 56 + 34);
      const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="900" height="383" viewBox="0 0 900 383">
        <defs>
          <linearGradient id="shade" x1="0" x2="1"><stop offset="0" stop-color="#fffdf8" stop-opacity="0.99"/><stop offset="0.54" stop-color="#fffdf8" stop-opacity="0.88"/><stop offset="0.75" stop-color="#fffdf8" stop-opacity="0.08"/><stop offset="1" stop-color="#fffdf8" stop-opacity="0"/></linearGradient>
        </defs>
        <image href="data:image/png;base64,${data}" x="${-index * 9}" y="${-(index % 3) * 6}" width="${930 + index * 4}" height="395" preserveAspectRatio="xMidYMid slice"/>
        <rect width="900" height="383" fill="url(#shade)"/>
        <rect x="54" y="43" width="8" height="35" rx="4" fill="${accent}"/>
        <text x="78" y="69" font-family="PingFang SC,Noto Sans CJK SC,sans-serif" font-size="20" font-weight="700" fill="${accent}">${esc(kicker)}</text>
        ${titleSvg}
        <path d="M54 ${subtitleY - 18}H330" stroke="${accent}" stroke-width="3"/>
        <text x="54" y="${subtitleY + 18}" font-family="PingFang SC,Noto Sans CJK SC,sans-serif" font-size="20" font-weight="520" fill="#4f5b61">${esc(group.id === "overview" ? "一级模块总览" : `子模块 ${String(index).padStart(2, "0")} · ${group.name}`)}</text>
      </svg>`;
      const svgPath = path.join(tempRoot, `${module.slug}-${group.id}-${kind}.svg`);
      const output = path.join(root, "content", "wechat", module.directory, groupDirectory(module, group), "assets", `${group.prefix}-cover-${kind}-wechat.png`);
      await mkdir(path.dirname(output), { recursive: true });
      await writeFile(svgPath, svg);
      await execFile("sips", ["-s", "format", "png", svgPath, "--out", output]);
      console.log(path.relative(root, output));
    }
  }
}

await rm(tempRoot, { recursive: true, force: true });
