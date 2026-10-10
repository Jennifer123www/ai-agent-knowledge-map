import { execFile as execFileCallback } from "node:child_process";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";

const root = path.resolve(import.meta.dirname, "..");
const base = path.join(root, "content/wechat/02-knowledge-retrieval-and-rag/submodules/01-knowledgebase/assets");
const execFile = promisify(execFileCallback);
const W = 1536;
const H = 1024;
const C = {
  paper: "#FBF9F4", white: "#FFFFFF", ink: "#26343A", muted: "#65767A",
  line: "#CFD9D5", teal: "#247C76", tealLight: "#E7F1ED", orange: "#C9783E",
  orangeLight: "#FFF0E3", rose: "#B95F60", roseLight: "#F7E9E7", blue: "#547895",
  blueLight: "#EAF0F3", green: "#3C8166", greenLight: "#E5F0E8",
};
const esc = (value) => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
const text = (x, y, value, size = 30, fill = C.ink, anchor = "middle", weight = 500) =>
  `<text x="${x}" y="${y}" fill="${fill}" text-anchor="${anchor}" font-family="PingFang SC,Hiragino Sans GB,Heiti SC,sans-serif" font-size="${size}" font-weight="${weight}">${esc(value)}</text>`;
const rect = (x, y, w, h, fill = C.white, stroke = C.line, radius = 14, sw = 2) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
const marker = (color) => `<marker id="arrow-${color.slice(1)}" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L12 6L0 12Z" fill="${color}"/></marker>`;
function arrowHead(x1, y1, x2, y2, color) {
  const angle = Math.atan2(y2 - y1, x2 - x1);
  const head = 14;
  const wing = 7;
  const bx = x2 - head * Math.cos(angle);
  const by = y2 - head * Math.sin(angle);
  const px = wing * Math.sin(angle);
  const py = wing * Math.cos(angle);
  return `<polygon points="${x2},${y2} ${bx + px},${by - py} ${bx - px},${by + py}" fill="${color}"/>`;
}
const line = (x1, y1, x2, y2, color = C.teal, width = 4, dash = "") =>
  `<path d="M${x1} ${y1}L${x2} ${y2}" fill="none" stroke="${color}" stroke-width="${width}" ${dash ? `stroke-dasharray="${dash}"` : ""}/>` + arrowHead(x1, y1, x2, y2, color);
function route(d, color = C.teal, width = 4, dash = "") {
  const tokens = d.match(/[MLHV]|-?\d+(?:\.\d+)?/g) || [];
  let x = 0;
  let y = 0;
  let fromX = 0;
  let fromY = 0;
  for (let i = 0; i < tokens.length;) {
    const command = tokens[i++];
    if (command === "M" || command === "L") {
      fromX = x; fromY = y; x = Number(tokens[i++]); y = Number(tokens[i++]);
    } else if (command === "H") {
      fromX = x; fromY = y; x = Number(tokens[i++]);
    } else if (command === "V") {
      fromX = x; fromY = y; y = Number(tokens[i++]);
    } else throw new Error(`Unsupported route command in ${d}`);
  }
  return `<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" ${dash ? `stroke-dasharray="${dash}"` : ""}/>` + arrowHead(fromX, fromY, x, y, color);
}
const circle = (cx, cy, r, fill, stroke = fill, sw = 2) => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
function node(x, y, w, h, title, detail = "", fill = C.white, stroke = C.line, titleColor = C.ink) {
  const titleY = y + (detail ? h * 0.44 : h * 0.56);
  const detailSvg = (detail ? detail.split("\n") : []).map((item, index) => text(x + w / 2, titleY + 42 + index * 28, item, 21, C.muted)).join("");
  return rect(x, y, w, h, fill, stroke) + text(x + w / 2, titleY, title, 30, titleColor, "middle", 650) + detailSvg;
}
function canvas(title, label, body) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <defs>${[...new Set(Object.values(C))].map(marker).join("")}</defs>
    <rect width="${W}" height="${H}" fill="${C.paper}"/>
    ${text(78, 57, label, 23, C.teal, "start", 650)}
    ${text(78, 105, title, 43, C.ink, "start", 700)}
    <path d="M78 137H1458" stroke="${C.line}" stroke-width="2"/>
    ${body}
  </svg>`;
}

function mainScene() {
  let s = text(768, 199, "同一条住宿规则的两个版本", 29, C.muted);
  s += node(150, 270, 520, 300, "旧版制度", "上限 450 元   ·   适用至 8 月 31 日", C.white, C.line, C.rose);
  s += node(866, 270, 520, 300, "新版制度", "上限 500 元   ·   9 月 1 日起生效", C.white, C.line, C.green);
  s += text(410, 505, "制度 V1", 24, C.rose, "middle", 650) + text(1126, 505, "制度 V2", 24, C.green, "middle", 650);
  s += line(675, 420, 854, 420, C.orange, 5);
  s += text(768, 647, "查询条件", 24, C.teal, "middle", 650);
  s += node(250, 690, 1036, 145, "9 月 15 日   ·   北京   ·   A 职级", "命中条件后，返回新版及其原文位置", C.tealLight, C.teal);
  s += circle(1318, 762, 28, C.orangeLight, C.orange) + text(1318, 771, "✓", 29, C.orange, "middle", 700);
  return canvas("先看版本条件，再看金额", "案例入口", s);
}

function mainPrinciple() {
  let s = text(105, 198, "离线：把原件整理成带来源的可查记录", 25, C.teal, "start", 650);
  s += node(90, 235, 250, 130, "正式发布源", "文件 + 发布编号", C.white, C.blue);
  s += node(415, 235, 260, 130, "原件版本", "稳定来源 ID + 校验和", C.white, C.teal);
  s += node(750, 235, 300, 130, "解析记录", "字段 + 页码 / 条款位置", C.white, C.orange);
  s += node(1130, 235, 330, 130, "可查索引", "来源 ID + 版本 + 权限", C.tealLight, C.teal);
  s += line(350, 300, 403, 300, C.blue) + line(685, 300, 738, 300, C.teal) + line(1060, 300, 1118, 300, C.orange);
  s += text(105, 493, "在线：按身份和业务日期取回可用记录", 25, C.orange, "start", 650);
  s += node(90, 540, 250, 142, "查询条件", "日期 / 地区 / 职级", C.white, C.blue);
  s += node(415, 540, 280, 142, "适用范围过滤", "有效期 + 当前权限", C.orangeLight, C.orange);
  s += node(780, 540, 280, 142, "证据记录", "版本 + 原文定位", C.tealLight, C.teal);
  s += node(1130, 540, 330, 142, "正式原文", "审核时可打开核对", C.white, C.blue);
  s += line(350, 612, 403, 612, C.blue) + line(705, 612, 768, 612, C.orange) + line(1070, 612, 1118, 612, C.teal);
  s += route("M1295 375V450H920V527", C.muted, 3, "8 8");
  s += text(1090, 440, "索引是派生查找入口", 22, C.muted);
  s += node(370, 765, 700, 100, "原件、解析结果与索引都保留同一条来源关系", "索引更新失败时，可定位到失败的版本和处理步骤", C.white, C.line);
  return canvas("从原件到可追溯记录", "知识库原理", s);
}

function mainVersion() {
  const x = [300, 650, 1000, 1350];
  let s = text(100, 218, "示例节点", 23, C.muted, "start");
  s += `<path d="M${x[0]} 250H${x[3]}" stroke="${C.line}" stroke-width="5"/>`;
  const dates = ["8 月 25 日", "9 月 1 日", "9 月 5 日", "9 月 15 日"];
  dates.forEach((date, i) => { s += circle(x[i], 250, 10, i === 1 ? C.orange : C.teal); s += text(x[i], 292, date, 22, C.muted); });
  s += text(100, 390, "业务效力", 26, C.teal, "start", 650);
  s += rect(300, 342, 320, 98, C.blueLight, C.blue, 12) + text(460, 383, "旧版 V1", 28, C.blue, "middle", 650) + text(460, 417, "8/1—8/31 · 450 元", 21, C.muted);
  s += rect(650, 342, 700, 98, C.greenLight, C.green, 12) + text(1000, 383, "新版 V2 生效", 28, C.green, "middle", 650) + text(1000, 417, "9/1 起 · 500 元", 21, C.muted);
  s += text(100, 553, "系统记录", 26, C.orange, "start", 650);
  s += rect(300, 505, 320, 98, C.blueLight, C.blue, 12) + text(460, 546, "系统已知 V1", 27, C.blue, "middle", 650) + text(460, 580, "8/25 收到并入库", 21, C.muted);
  s += rect(1000, 505, 350, 98, C.orangeLight, C.orange, 12) + text(1175, 546, "系统收到 V2", 27, C.orange, "middle", 650) + text(1175, 580, "9/5 才补录", 21, C.muted);
  s += route(`M${x[1]} 325V455H${x[2]}V490`, C.orange, 4, "9 8");
  s += node(430, 697, 680, 145, "查 9 月 15 日的住宿", "按业务生效日期匹配 V2", C.white, C.teal);
  s += route("M1175 612V655H1118V683", C.muted, 3, "7 8");
  return canvas("入库日期不替制度决定效力", "版本与时间", s);
}

function mainAccess() {
  let s = text(180, 208, "资料及其派生记录", 25, C.teal, "middle", 650);
  s += node(80, 250, 370, 150, "财务审批细则", "访问域：财务", C.roseLight, C.rose);
  s += node(80, 485, 370, 150, "解析记录 / 摘要", "继承来源访问域", C.white, C.teal);
  s += node(80, 720, 370, 150, "检索索引 / 缓存", "保留权限版本", C.white, C.blue);
  s += route("M265 410V470", C.rose, 4) + route("M265 645V705", C.rose, 4);
  s += text(756, 208, "按当前身份检查后再返回", 25, C.orange, "middle", 650);
  s += node(535, 340, 270, 180, "当前查询者", "普通员工", C.white, C.blue);
  s += node(900, 340, 250, 180, "访问检查", "身份 + 策略版本", C.orangeLight, C.orange);
  s += node(1240, 340, 230, 180, "返回结果", "仅可见资料", C.greenLight, C.green);
  s += line(815, 430, 888, 430, C.blue) + line(1160, 430, 1228, 430, C.green);
  s += route("M450 325H510V555H900", C.rose, 3, "8 7");
  s += circle(865, 555, 22, C.roseLight, C.rose) + text(865, 563, "×", 24, C.rose, "middle", 700);
  s += text(1085, 585, "无权资料不进入可回答结果", 22, C.rose, "middle", 600);
  s += node(585, 700, 760, 130, "人员调岗或权限撤销", "相关旧缓存失效，下一次查询按新身份重查", C.blueLight, C.blue);
  s += route("M1040 530V670", C.orange, 3, "8 7");
  return canvas("权限跟着资料和派生内容走", "访问控制", s);
}

function mainRefresh() {
  const xs = [95, 370, 650, 930, 1215];
  const titles = ["收到新版", "解析完成", "字段抽检", "构建索引", "切换可查"];
  const details = ["登记来源版本", "保留页码位置", "金额 / 适用条件", "独立构建 V2", "入口指向 V2"];
  let s = text(100, 218, "更新：验收通过后再切换", 25, C.teal, "start", 650);
  xs.forEach((x, i) => { s += node(x, 260, 220, 150, titles[i], details[i], i === 4 ? C.greenLight : C.white, i === 4 ? C.green : C.line); if (i < xs.length - 1) s += line(x + 225, 335, xs[i + 1] - 12, 335, C.orange); });
  s += route("M760 420V485H535V505", C.rose, 4);
  s += node(340, 515, 390, 125, "抽检失败", "V1 仍按原条件管理", C.roseLight, C.rose);
  s += node(875, 515, 390, 125, "修复后重试", "任务记录版本与失败步骤", C.white, C.teal);
  s += line(740, 578, 862, 578, C.teal);
  s += text(100, 735, "撤回：按来源 ID 找齐所有派生记录", 25, C.rose, "start", 650);
  s += node(95, 770, 285, 110, "撤回标记", "阻止新查询", C.roseLight, C.rose);
  s += node(495, 770, 360, 110, "清理解析与索引", "处理摘要和缓存", C.white, C.rose);
  s += node(975, 770, 420, 110, "反向查询验收", "原问题不再返回已撤回正文", C.greenLight, C.green);
  s += line(390, 825, 482, 825, C.rose) + line(865, 825, 962, 825, C.teal);
  return canvas("更新有验收，撤回有回查", "发布与维护", s);
}

function interviewProvenance() {
  let s = node(100, 265, 320, 190, "来源登记", "权威渠道 / 责任人\n发布状态 / 范围", C.blueLight, C.blue);
  s += node(610, 265, 320, 190, "源版本", "稳定 ID\n版本号 / 校验和", C.tealLight, C.teal);
  s += node(1120, 265, 320, 190, "发布决策", "确认可用\n或待核 / 撤回", C.orangeLight, C.orange);
  s += line(430, 360, 598, 360, C.blue) + line(940, 360, 1108, 360, C.teal);
  s += node(220, 605, 400, 180, "解析产物", "处理器版本\n字段 / 页码定位", C.white, C.teal);
  s += node(915, 605, 400, 180, "索引构建", "构建 ID\n包含哪些源版本", C.white, C.orange);
  s += line(630, 695, 902, 695, C.orange);
  s += route("M1275 470V530H420V592", C.muted, 3, "8 8");
  s += route("M785 470V555H1115V592", C.muted, 3, "8 8");
  s += rect(440, 850, 650, 54, C.paper, C.line, 10) + text(765, 885, "任一结果均可追到来源，并知道当前状态", 22, C.muted);
  return canvas("问一条记录从哪来、现在是否可用", "数据模型", s);
}

function interviewParser() {
  let s = text(225, 212, "抽样页面", 24, C.teal, "middle", 650);
  s += node(80, 250, 300, 145, "扫描页", "金额 / 日期", C.white, C.blue);
  s += node(80, 445, 300, 145, "跨页表格", "职级 / 地区表头", C.white, C.teal);
  s += node(80, 640, 300, 145, "脚注 / 修订页", "例外 / 生效条件", C.white, C.orange);
  s += text(746, 212, "两类结果分别核对", 24, C.orange, "middle", 650);
  s += node(525, 300, 390, 160, "字段值", "金额读成 500 元？", C.blueLight, C.blue);
  s += node(525, 565, 390, 160, "字段关系", "500 元属于北京 A 职级？", C.tealLight, C.teal);
  s += route("M385 322H470V350H512", C.blue, 3) + route("M385 517H470V640H512", C.teal, 3) + route("M385 712H470V680H512", C.orange, 3);
  s += node(1080, 320, 350, 135, "字段准确率", "正确字段 / 检查字段", C.white, C.blue);
  s += node(1080, 575, 350, 135, "关系准确率", "条件与条款正确绑定", C.white, C.teal);
  s += line(930, 380, 1068, 380, C.blue) + line(930, 645, 1068, 645, C.teal);
  s += text(1000, 820, "金额和适用条件单独设门槛", 23, C.rose, "middle", 650);
  return canvas("字符读对了，业务关系还可能错", "解析质量评测", s);
}

function interviewBitemporal() {
  let s = text(120, 212, "业务有效时间", 24, C.teal, "start", 650);
  s += `<path d="M340 253H1400" stroke="${C.line}" stroke-width="5"/>`;
  const xs = [420, 830, 1230];
  ["8 月 31 日", "9 月 1 日", "9 月 15 日"].forEach((d, i) => { s += circle(xs[i], 253, 9, i === 1 ? C.orange : C.teal); s += text(xs[i], 295, d, 21, C.muted); });
  s += rect(400, 335, 425, 95, C.blueLight, C.blue, 12) + text(612, 376, "V1 生效區間", 25, C.blue, "middle", 650) + text(612, 408, "至 8/31 · 上限 450 元", 21, C.muted);
  s += rect(830, 335, 530, 95, C.greenLight, C.green, 12) + text(1095, 376, "V2 生效區間", 25, C.green, "middle", 650) + text(1095, 408, "9/1 起 · 上限 500 元", 21, C.muted);
  s += text(120, 553, "系統記錄時間", 24, C.orange, "start", 650);
  s += `<path d="M340 595H1400" stroke="${C.line}" stroke-width="5"/>`;
  s += circle(690, 595, 11, C.blue) + circle(1040, 595, 11, C.orange);
  s += text(690, 642, "8/25 系統收到 V1", 22, C.blue);
  s += text(1040, 642, "9/5 系統補錄 V2", 22, C.orange);
  s += node(250, 735, 450, 125, "“9/2 當時系統知道什麼？”", "只看到已登記的版本", C.white, C.blue);
  s += node(830, 735, 450, 125, "“9/2 的業務日期適用什麼？”", "按有效時間回看 V2", C.white, C.green);
  return canvas("同一日期，业务时间与系统认知不同", "双时态建模", s);
}

function interviewAcl() {
  let s = node(80, 300, 270, 190, "查询主体", "普通员工\n当前策略版本 P7", C.blueLight, C.blue);
  s += node(475, 300, 320, 190, "授权过滤", "按当前身份\n筛除无权来源", C.orangeLight, C.orange);
  s += node(920, 245, 260, 155, "允许材料", "普通差旅制度", C.greenLight, C.green);
  s += node(920, 445, 260, 155, "受限材料", "财务审批细则", C.roseLight, C.rose);
  s += node(1270, 300, 190, 190, "缓存键", "身份范围\n资料版本\n策略版本", C.tealLight, C.teal);
  s += line(360, 395, 463, 395, C.blue) + line(805, 355, 908, 322, C.green) + line(805, 435, 908, 522, C.rose) + line(1190, 322, 1258, 365, C.teal);
  s += route("M1045 610V700H615V510", C.rose, 3, "8 8");
  s += text(820, 691, "权限变更：失效相关缓存，再按新身份查询", 22, C.rose, "middle", 600);
  return canvas("缓存命中也必须经过当前权限", "访问控制", s);
}

function interviewSync() {
  let s = node(80, 330, 290, 190, "变更事件", "source_id\nversion + checksum", C.blueLight, C.blue);
  s += node(500, 330, 290, 190, "幂等登记", "相同版本\n复用处理结果", C.tealLight, C.teal);
  s += node(920, 330, 250, 190, "任务步骤", "解析 → 校验\n持久化 → 检查点", C.white, C.orange);
  s += node(1290, 330, 180, 190, "索引", "一份有效版本", C.greenLight, C.green);
  s += line(380, 425, 488, 425, C.blue) + line(800, 425, 908, 425, C.teal) + line(1180, 425, 1278, 425, C.orange);
  s += route("M1060 535V650H650V535", C.rose, 3, "8 8");
  s += text(860, 698, "失败可重试；版本检查阻止旧任务覆盖新结果", 22, C.rose, "middle", 600);
  s += rect(500, 780, 670, 85, C.white, C.line, 12) + text(835, 833, "重复投递  ×  不重复建档", 27, C.ink, "middle", 650);
  return canvas("事件可以重放，处理结果保持唯一", "增量同步", s);
}

function interviewRelease() {
  let s = text(110, 218, "构建候选 V2", 24, C.teal, "start", 650);
  s += node(90, 265, 330, 170, "输入版本固定", "源版本 + 解析器版本", C.white, C.blue);
  s += node(600, 265, 330, 170, "候选索引 V2", "与线上版本隔离构建", C.tealLight, C.teal);
  s += node(1110, 265, 330, 170, "验收门槛", "关键字段 / 权限 / 样本查询", C.orangeLight, C.orange);
  s += line(430, 350, 588, 350, C.blue) + line(940, 350, 1098, 350, C.teal);
  s += node(250, 625, 450, 170, "活动入口", "仍指向 V1", C.blueLight, C.blue);
  s += node(850, 625, 450, 170, "候选通过", "原子切换入口至 V2", C.greenLight, C.green);
  s += route("M1275 445V535H1075V612", C.green, 4);
  s += route("M1260 445V520H480V612", C.rose, 3, "8 8");
  s += text(865, 555, "失败时保留 V1；不能发布半成品", 22, C.rose, "middle", 600);
  return canvas("索引验收与业务生效分开处理", "版本发布", s);
}

function interviewDelete() {
  let s = node(70, 350, 245, 180, "撤回事件", "稳定 source_id", C.roseLight, C.rose);
  s += node(410, 245, 270, 145, "解析记录", "标记不可用", C.white, C.rose);
  s += node(410, 470, 270, 145, "索引记录", "写入墓碑状态", C.white, C.rose);
  s += node(410, 695, 270, 145, "摘要 / 缓存", "按来源失效", C.white, C.rose);
  s += line(325, 440, 400, 320, C.rose) + line(325, 440, 400, 540, C.rose) + line(325, 440, 400, 765, C.rose);
  s += node(850, 385, 270, 180, "查询验证", "正文 / 摘要\n不同身份", C.orangeLight, C.orange);
  s += route("M690 320H760V425H838", C.rose, 3) + line(690, 540, 838, 485, C.rose) + route("M690 765H760V525H838", C.rose, 3);
  s += node(1220, 385, 250, 180, "完成状态", "所有派生物\n不可再返回", C.greenLight, C.green);
  s += line(1130, 475, 1208, 475, C.green);
  s += rect(850, 680, 620, 130, C.white, C.line, 12) + text(1160, 733, "未完成副本继续重试", 24, C.rose, "middle", 650) + text(1160, 774, "审计留必要记录，不留可检索正文", 21, C.muted);
  return canvas("删除源文件不等于撤回完成", "撤回与删除", s);
}

const diagrams = [
  ["kb-case-scene.png", mainScene],
  ["kb-principle.png", mainPrinciple],
  ["kb-version.png", mainVersion],
  ["kb-access.png", mainAccess],
  ["kb-refresh.png", mainRefresh],
  ["kb-interview-provenance.png", interviewProvenance],
  ["kb-interview-parser-test.png", interviewParser],
  ["kb-interview-bitemporal.png", interviewBitemporal],
  ["kb-interview-acl-cache.png", interviewAcl],
  ["kb-interview-sync.png", interviewSync],
  ["kb-interview-release.png", interviewRelease],
  ["kb-interview-deletion.png", interviewDelete],
];

const tempRoot = await mkdtemp(path.join(tmpdir(), "knowledgebase-figures-"));
try {
  for (const [name, draw] of diagrams) {
    const svgPath = path.join(tempRoot, `${name}.svg`);
    const pngPath = path.join(base, name);
    await mkdir(base, { recursive: true });
    await writeFile(svgPath, draw());
    await execFile("sips", ["-s", "format", "png", svgPath, "--out", pngPath]);
    console.log(path.relative(root, pngPath));
  }
} finally {
  await rm(tempRoot, { recursive: true, force: true });
}
