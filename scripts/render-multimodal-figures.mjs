import { execFile as execFileCallback } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";

// Exact-label teaching diagrams. The photographed ticket is an explicitly
// constructed teaching prop, never a model output or a real financial record.
const root = path.resolve(import.meta.dirname, "..");
const assets = path.join(root, "content/wechat/01-foundation-models-and-inference/submodules/02-multimodal/assets");
const execFile = promisify(execFileCallback);
const photo = (await readFile(path.join(assets, "multimodal-scene-invoice.png"))).toString("base64");
const W = 1536, H = 1024;
const C = {
  bg: "#fbf8f3", paper: "#fffdf9", ink: "#28383c", muted: "#53656b",
  line: "#cdd9d5", teal: "#187a78", tealBg: "#e4f1ed",
  orange: "#c47738", orangeBg: "#fbefdf", plum: "#795069",
  plumBg: "#f3eaf0", blue: "#426b8b", blueBg: "#e8f0f5",
};
const esc = (s) => String(s).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
const txt = (x, y, s, n = 54, color = C.ink, weight = 500, anchor = "start") =>
  `<text x="${x}" y="${y}" font-size="${n}" font-weight="${weight}" fill="${color}" text-anchor="${anchor}">${esc(s)}</text>`;
const rect = (x, y, w, h, fill = C.paper, stroke = C.line, r = 18, sw = 3) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
const line = (x1, y1, x2, y2, color = C.line, sw = 4, dash = "") =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${sw}" ${dash ? `stroke-dasharray="${dash}"` : ""}/>`;
const arrow = (x1, y1, x2, y2, color = C.teal, sw = 6) => {
  const a = Math.atan2(y2-y1, x2-x1), l = 22;
  const p1 = [x2-l*Math.cos(a-0.48), y2-l*Math.sin(a-0.48)];
  const p2 = [x2-l*Math.cos(a+0.48), y2-l*Math.sin(a+0.48)];
  return line(x1,y1,x2,y2,color,sw)+`<polygon points="${x2},${y2} ${p1[0]},${p1[1]} ${p2[0]},${p2[1]}" fill="${color}"/>`;
};
const photoAt = (x,y,w,h) =>
  `<image href="data:image/png;base64,${photo}" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="xMidYMid meet"/>`;
const header = (kicker, title) => `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <rect width="${W}" height="${H}" fill="${C.bg}"/>
  <g font-family="PingFang SC,Hiragino Sans GB,Source Han Sans SC,sans-serif">
  ${txt(70,71,kicker,30,C.teal,600)}
  ${txt(70,142,title,57,C.ink,700)}
  ${line(70,177,1466,177,C.line,3)}`;
const finish = (body) => body + "</g></svg>";
const figures = [
  {
    name: "multimodal-crop-contrast.png",
    svg: finish(header("图像预处理", "整页和局部图，各保留了什么") +
      photoAt(73,240,602,402) +
      rect(411,456,140,56,"none",C.orange,6,7) +
      txt(92,721,"同一张教学票据",45,C.muted) +
      arrow(686,429,804,322,C.plum) + arrow(686,528,804,719,C.teal) +
      rect(805,230,647,235,C.plumBg,C.plum) +
      txt(848,297,"整页缩小",51,C.plum,650) +
      txt(848,374,"保住布局",45,C.ink) +
      txt(848,431,"小字和小数点可能模糊",40,C.muted) +
      rect(805,568,647,252,C.tealBg,C.teal) +
      txt(848,632,"带标签的局部图",51,C.teal,650) +
      txt(848,710,"含税金额  680.00",51,C.ink) +
      txt(848,773,"裁切位置也要记住",40,C.muted)),
  },
  {
    name: "multimodal-query-region.png",
    svg: finish(header("图文配合", "同一张图，问题指向不同位置") +
      rect(515,237,512,635,C.paper,C.line,10) +
      txt(566,318,"酒店住宿票据",58,C.ink,650) +
      line(556,352,988,352) +
      rect(550,387,439,117,C.orangeBg,C.orange,8) +
      txt(580,466,"开票日期   9/3",57,C.ink) +
      rect(550,556,439,117,C.tealBg,C.teal,8) +
      txt(580,635,"含税金额   680.00",51,C.ink) +
      txt(82,333,"问：日期是什么？",48,C.orange,650) +
      txt(82,688,"问：金额是多少？",48,C.teal,650) +
      arrow(437,317,550,438,C.orange) +
      arrow(437,672,550,614,C.teal) +
      arrow(989,438,1112,317,C.orange) +
      arrow(989,614,1112,672,C.teal) +
      txt(1122,333,"9/3",62,C.orange,700) +
      txt(1122,390,"年份未写",41,C.muted) +
      txt(1122,688,"680.00",62,C.teal,700)),
  },
  {
    name: "multimodal-grounding-v2.png",
    svg: finish(header("证据定位", "答案中的数字，要能返回它旁边的标签") +
      rect(70,247,716,560,C.paper,C.line,12) +
      txt(110,326,"票面局部",50,C.ink,650) +
      line(107,358,748,358) +
      rect(118,437,590,135,C.tealBg,C.teal,10,6) +
      txt(157,523,"含税金额     680.00",54,C.ink,600) +
      rect(118,613,590,115,C.paper,C.line,10) +
      txt(157,688,"税额             38.49",50,C.muted) +
      arrow(708,504,888,504,C.teal,8) +
      rect(894,344,566,365,C.paper,C.teal,16,5) +
      txt(939,417,"草稿候选",51,C.teal,650) +
      txt(939,498,"字段：含税金额",49,C.ink) +
      txt(939,570,"数值：680.00",49,C.ink) +
      txt(939,642,"来源：同框标签与数字",42,C.muted)),
  },
  {
    name: "multimodal-visual-budget.png",
    svg: finish(header("分辨率与计算", "放大输入，不等于找回已经消失的笔画") +
      rect(75,247,406,485,C.paper,C.line) +
      txt(110,318,"假设原图过曝",43,C.ink,650) +
      rect(119,375,325,163,C.plumBg,C.plum) +
      txt(143,472,"680.0?",59,C.plum,700) +
      txt(108,622,"若原像素过曝",42,C.muted) +
      txt(108,682,"请补拍",51,C.plum,650) +
      arrow(497,485,595,485,C.plum) +
      rect(602,247,384,485,C.paper,C.line) +
      txt(638,318,"模型输入",48,C.ink,650) +
      rect(641,373,307,190,C.orangeBg,C.orange) +
      line(718,373,718,563,C.orange,3) + line(795,373,795,563,C.orange,3) + line(872,373,872,563,C.orange,3) +
      line(641,420,948,420,C.orange,3) + line(641,468,948,468,C.orange,3) + line(641,516,948,516,C.orange,3) +
      txt(638,635,"宽高各翻倍时",39,C.muted) +
      txt(638,688,"图块约为 4 倍",46,C.orange,650) +
      arrow(1000,485,1097,485,C.teal) +
      rect(1105,247,356,485,C.paper,C.line) +
      txt(1140,318,"取舍",48,C.ink,650) +
      txt(1140,424,"裁图保小字",45,C.teal) +
      txt(1140,503,"整页保位置",45,C.teal) +
      txt(1140,582,"两者一起测",45,C.teal)),
  },
  {
    name: "multimodal-architecture-contrast.png",
    svg: finish(header("架构比较", "三种接图方式，区别在中间那一步") +
      txt(90,276,"LLaVA",54,C.plum,700) +
      rect(336,225,235,123,C.paper,C.line) + txt(366,304,"图像特征",45) +
      arrow(578,287,671,287,C.plum) +
      rect(682,225,252,123,C.plumBg,C.plum) + txt(720,304,"投影层",46,C.plum,650) +
      arrow(944,287,1043,287,C.plum) +
      rect(1054,225,366,123,C.paper,C.line) + txt(1100,304,"语言模型",46) +
      txt(90,503,"Flamingo",54,C.teal,700) +
      rect(336,452,235,123,C.paper,C.line) + txt(366,531,"图像特征",45) +
      arrow(578,514,671,514,C.teal) +
      rect(682,452,252,123,C.tealBg,C.teal) + txt(703,531,"重采样器",43,C.teal,650) +
      arrow(944,514,1043,514,C.teal) +
      rect(1054,452,366,123,C.paper,C.line) + txt(1080,531,"层间交叉注意力",40) +
      txt(90,730,"Donut",54,C.orange,700) +
      rect(336,679,235,123,C.paper,C.line) + txt(366,758,"文档图像",45) +
      arrow(578,741,671,741,C.orange) +
      rect(682,679,252,123,C.orangeBg,C.orange) + txt(721,758,"图像编码",46,C.orange,650) +
      arrow(944,741,1043,741,C.orange) +
      rect(1054,679,366,123,C.paper,C.line) + txt(1100,758,"文本解码",46)),
  },
  {
    name: "multimodal-ocr-vlm-contrast.png",
    svg: finish(header("方案选择", "同一张票，先问要交付“答案”还是“位置”") +
      rect(76,292,349,425,C.paper,C.line) +
      txt(104,356,"输入",49,C.ink,650) +
      txt(107,453,"680.00",61,C.ink,700) +
      txt(107,532,"38.49",61,C.ink,700) +
      txt(107,635,"标签与行列",43,C.muted) +
      arrow(437,418,569,346,C.plum) +
      arrow(437,559,569,662,C.teal) +
      rect(575,230,827,256,C.plumBg,C.plum) +
      txt(612,308,"OCR + 版面规则",51,C.plum,650) +
      txt(612,383,"字符框与坐标可保存；字段规则需另写",43,C.ink) +
      rect(575,555,827,256,C.tealBg,C.teal) +
      txt(612,633,"VLM / 文档模型",51,C.teal,650) +
      txt(612,708,"可直接回答字段；原图定位能力需实测",43,C.ink)),
  },
  {
    name: "multimodal-coordinate-map.png",
    svg: finish(header("坐标回映", "局部图的框，怎样找回原照片") +
      rect(75,268,554,510,C.paper,C.line) +
      txt(108,335,"原图",51,C.ink,650) +
      rect(153,410,320,250,C.blueBg,C.blue,8) +
      txt(170,393,"裁切起点 (x₀, y₀)",38,C.blue) +
      rect(218,492,155,87,C.orangeBg,C.orange,4,5) +
      txt(232,549,"680.00",43,C.orange,650) +
      arrow(638,515,817,515,C.orange,8) +
      rect(828,268,630,510,C.paper,C.line) +
      txt(859,335,"裁出后放大",51,C.ink,650) +
      rect(920,418,470,260,C.blueBg,C.blue,8) +
      rect(1018,508,250,101,C.orangeBg,C.orange,5,5) +
      txt(1038,573,"680.00",58,C.orange,650) +
      txt(864,726,"局部点 (u, v)",43,C.muted) +
      rect(155,834,1231,113,C.tealBg,C.teal,10) +
      txt(198,907,"x = x₀ + u × w/W；y = y₀ + v × h/H",49,C.teal,650)),
  },
  {
    name: "multimodal-diagnosis-experiment.png",
    svg: finish(header("定位故障", "一次只换一种输入，才能找到故障层") +
      rect(82,267,648,539,C.paper,C.line) +
      txt(120,345,"对照 A：只换图像清晰度",51,C.plum,650) +
      rect(127,404,262,178,C.plumBg,C.plum) + txt(151,506,"680.0?",54,C.plum,650) +
      arrow(410,493,484,493,C.plum) +
      rect(500,404,179,178,C.tealBg,C.teal) + txt(523,506,"680.00",45,C.teal,650) +
      txt(123,675,"读数恢复？",44,C.ink) +
      txt(123,737,"先查图像阶段",39,C.muted) +
      rect(809,267,648,539,C.paper,C.line) +
      txt(847,345,"对照 B：只补标签位置",51,C.teal,650) +
      rect(853,404,228,178,C.orangeBg,C.orange) + txt(875,506,"680.00",47,C.orange,650) +
      arrow(1097,493,1174,493,C.teal) +
      rect(1190,404,217,178,C.tealBg,C.teal) + txt(1209,482,"含税金额",40,C.teal,650) + txt(1225,536,"680.00",40,C.teal) +
      txt(847,675,"字段归对？",44,C.ink) +
      txt(847,737,"再查版面阶段",39,C.muted)),
  },
  {
    name: "multimodal-evaluation-grid.png",
    svg: finish(header("分层评测", "把照片质量与输入方式交叉测试") +
      txt(113,319,"照片条件",45,C.muted,600) +
      txt(620,260,"整页缩图",49,C.plum,650,"middle") +
      txt(1170,260,"带标签局部图",49,C.teal,650,"middle") +
      txt(98,488,"清晰",52,C.ink,650) +
      txt(98,752,"反光",52,C.ink,650) +
      rect(334,325,510,247,C.paper,C.plum) +
      txt(373,405,"基线：看全页",49,C.plum,650) +
      txt(373,484,"记录读字与归栏",43,C.ink) +
      rect(905,325,510,247,C.paper,C.teal) +
      txt(944,405,"只改裁图",49,C.teal,650) +
      txt(944,484,"检查小字是否恢复",43,C.ink) +
      rect(334,619,510,247,C.paper,C.plum) +
      txt(373,699,"只换反光图",49,C.plum,650) +
      txt(373,778,"检查原像素是否缺失",41,C.ink) +
      rect(905,619,510,247,C.paper,C.teal) +
      txt(944,699,"反光图再裁切",49,C.teal,650) +
      txt(944,778,"验证裁图的边界",43,C.ink)),
  },
];

const temp = await mkdtemp(path.join(tmpdir(), "multimodal-figures-"));
try {
  for (const {name, svg} of figures) {
    const source = path.join(temp, name.replace(/\.png$/, ".svg"));
    await writeFile(source, svg);
    await execFile("sips", ["-s", "format", "png", source, "--out", path.join(assets, name)]);
    console.log(name);
  }
} finally {
  await rm(temp, {recursive: true, force: true});
}
