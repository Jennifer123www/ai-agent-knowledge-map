import { execFile as execFileCallback } from "node:child_process";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";

// SVG is an intermediate drawing format. The publication assets are PNGs.
const root = path.resolve(import.meta.dirname, "..");
const outRoot = path.join(root, "content/wechat");
const execFile = promisify(execFileCallback);
const W = 1536;
const H = 1024;
const ink = "#222b32";
const muted = "#55636b";
const teal = "#0f7874";
const plum = "#723e59";
const orange = "#b65e2e";
const blue = "#316591";
const paper = "#fffdf9";
const font = "'PingFang SC','Hiragino Sans GB','Heiti SC',sans-serif";

const esc = (s) => String(s).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
const text = (x, y, s, size = 28, color = ink, anchor = "middle", weight = 500) =>
  `<text x="${x}" y="${y}" fill="${color}" text-anchor="${anchor}" font-family="${font}" font-size="${size}" font-weight="${weight}">${esc(s)}</text>`;
const rect = (x, y, w, h, fill = "white", stroke = "#bfcbd0", r = 8, sw = 2) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
const arrow = (x, y, fromX, fromY, color) => {
  const angle = Math.atan2(y - fromY, x - fromX);
  const rearX = x - 16 * Math.cos(angle);
  const rearY = y - 16 * Math.sin(angle);
  const spreadX = 7 * Math.sin(angle);
  const spreadY = 7 * Math.cos(angle);
  return `<path d="M${x} ${y}L${rearX + spreadX} ${rearY - spreadY}L${rearX - spreadX} ${rearY + spreadY}Z" fill="${color}"/>`;
};
const line = (x1, y1, x2, y2, color = muted, width = 3, dash = "") =>
  `<path d="M${x1} ${y1}L${x2} ${y2}" fill="none" stroke="${color}" stroke-width="${width}" ${dash ? `stroke-dasharray="${dash}"` : ""}/>` + arrow(x2, y2, x1, y1, color);
function pathLine(d, color = muted, width = 3, dash = "") {
  const tokens = d.match(/[MLHVQ]|-?\d+(?:\.\d+)?/g) || [];
  let x = 0;
  let y = 0;
  let fromX = 0;
  let fromY = 0;
  for (let i = 0; i < tokens.length;) {
    const op = tokens[i++];
    if (op === "M" || op === "L") {
      fromX = x; fromY = y;
      x = Number(tokens[i++]); y = Number(tokens[i++]);
    } else if (op === "H") {
      fromX = x; fromY = y; x = Number(tokens[i++]);
    } else if (op === "V") {
      fromX = x; fromY = y; y = Number(tokens[i++]);
    } else if (op === "Q") {
      fromX = Number(tokens[i++]); fromY = Number(tokens[i++]);
      x = Number(tokens[i++]); y = Number(tokens[i++]);
    } else throw new Error(`Unsupported path command in ${d}`);
  }
  return `<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" ${dash ? `stroke-dasharray="${dash}"` : ""}/>` + arrow(x, y, fromX, fromY, color);
}
const box = (x, y, w, h, label, sub = "", color = teal) =>
  rect(x, y, w, h, "#fff", color) + `<rect x="${x}" y="${y}" width="8" height="${h}" rx="4" fill="${color}"/>` +
  text(x + w / 2, y + (sub ? h / 2 - 6 : h / 2 + 11), label, 30, ink, "middle", 650) +
  (sub ? text(x + w / 2, y + h / 2 + 39, sub, 22, muted) : "");
const note = (x, y, label, color = muted) => text(x, y, label, 23, color);
const badge = (x, y, n, color = teal) => `<circle cx="${x}" cy="${y}" r="25" fill="${color}"/>` + text(x, y + 9, n, 25, "white", "middle", 700);
const eq = (x, y, label, color = ink) => text(x, y, label, 31, color, "middle", 600);

function canvas(title, eyebrow, body, source) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <rect width="${W}" height="${H}" fill="${paper}"/>
    <path d="M76 170H1460" stroke="#cbd7d7" stroke-width="2"/>
    ${text(76, 76, eyebrow, 22, teal, "start", 650)}
    ${text(76, 139, title, 48, ink, "start", 700)}
    ${body}
    <path d="M76 920H1460" stroke="#cbd7d7" stroke-width="2"/>
    ${text(76, 955, source, 18, muted, "start")}
  </svg>`;
}

const diagrams = [
  {
    file: "foundation-models-and-inference/assets/foundation-principle.png",
    source: "Lewis et al., RAG (2020), Figure 1；精排为工程扩展",
    title: "检索证据怎样进入生成模型",
    draw: () => {
      let s = box(85, 300, 245, 120, "用户问题", "北京住宿上限？", blue);
      s += box(475, 275, 260, 115, "查询编码器", "问题 → 查询向量", teal);
      s += box(475, 540, 260, 115, "文档索引", "资料 → 文档向量", teal);
      s += box(855, 375, 245, 145, "检索候选", "带来源的相关段落", orange);
      s += box(1190, 265, 245, 120, "生成模型", "依据证据回答", plum);
      s += rect(1190, 585, 245, 100, "#f1f7f4", teal) + text(1312, 645, "带引用的回答", 29, ink);
      s += line(330, 360, 475, 330) + line(735, 330, 855, 435) + line(735, 600, 855, 465);
      s += line(1100, 430, 1190, 340) + line(1312, 385, 1312, 585);
      s += rect(840, 655, 275, 112, "#fff7f2", orange) + text(977, 702, "重排序", 27, ink) + note(977, 741, "可选工程扩展", orange);
      s += pathLine("M965 520V655", orange, 2, "8 6");
      s += pathLine("M1115 710H1260V385", orange, 2, "8 6");
      s += note(770, 848, "先找到可追溯证据，再由生成模型组织答案；精排不是原论文的必备节点。", muted);
      return s;
    },
  },
  {
    file: "foundation-models-and-inference/submodules/llm/assets/llm-principle.png",
    source: "Vaswani et al., Attention Is All You Need (2017), Figure 2；因果掩码见 §3.2.3",
    title: "自注意力：从 Q/K/V 到当前表示",
    draw: () => {
      let s = box(76, 330, 260, 135, "输入 token", "带位置信息的表示", blue);
      for (const [i, label, c] of [[0, "Q · 查询", plum], [1, "K · 键", teal], [2, "V · 值", orange]]) {
        s += box(465, 230 + i * 190, 260, 105, label, "线性投影", c);
        s += line(336, 395, 465, 280 + i * 190);
      }
      s += rect(850, 325, 270, 140, "#fff", plum) + text(985, 373, "相关性权重", 29, ink, "middle", 650);
      s += text(985, 410, "Q × K^T / sqrt(dk)", 19, muted) + text(985, 441, "→ softmax", 20, muted);
      s += box(1200, 325, 265, 140, "加权汇总 V", "得到新表示", orange);
      s += line(725, 282, 850, 360) + line(725, 472, 850, 405) + line(1120, 395, 1200, 395);
      s += pathLine("M725 662H1145V440H1200", orange);
      s += rect(355, 745, 825, 87, "#f1f7f4", teal) + note(768, 800, "因果语言模型只看当前位置及以前的 token；不能偷看未来。", teal);
      return s;
    },
  },
  {
    file: "foundation-models-and-inference/submodules/llm/assets/llm-rnn-comparison.png",
    source: "Vaswani et al. (2017), §4 / Table 1；比较的是同层输入表示的计算",
    title: "RNN 与自注意力：同一层怎样处理输入",
    draw: () => {
      let s = text(390, 245, "循环层 RNN", 32, plum, "middle", 700) + text(1148, 245, "自注意力层", 32, teal, "middle", 700);
      s += line(768, 205, 768, 830, "#d7ddde", 2, "7 8");
      for (let i = 0; i < 4; i++) {
        const x = 105 + i * 172;
        s += box(x, 395, 140, 105, `h${i + 1}`, `输入 ${i + 1}`, plum);
        if (i) s += line(x - 33, 447, x, 447, plum);
      }
      for (let i = 0; i < 4; i++) {
        const x = 826 + i * 170;
        s += box(x, 395, 140, 105, `位置 ${i + 1}`, "并行计算", teal);
        if (i > 0) s += pathLine(`M${x + 65} 395Q${x - 130} ${325 - i * 25} ${x - 170 + 72} 395`, teal, 2);
      }
      s += note(395, 645, "前一步的隐藏状态 → 后一步", plum);
      s += note(1130, 645, "输入位置可在训练时并行建立关联", teal);
      s += rect(210, 735, 1115, 90, "#eef4f5", "#a9c7c6") + note(768, 793, "注意：Transformer 自回归生成输出时，仍逐个产生下一个 token。", ink);
      return s;
    },
  },
  {
    file: "foundation-models-and-inference/submodules/llm/assets/llm-token-generation.png",
    source: "自回归解码示意：每轮预测一个 token，直到结束标记或达到上限",
    title: "一次生成：预测下一个 token",
    draw: () => {
      let s = box(95, 320, 270, 145, "已有上下文", "请总结这份合同", blue);
      s += box(455, 320, 255, 145, "模型计算", "当前上下文表示", plum);
      s += box(800, 270, 280, 245, "候选概率", "例：摘要 0.52", orange);
      s += note(940, 455, "要点 0.31 / 其他 0.17", muted);
      s += box(1170, 320, 260, 145, "选出 token", "追加到上下文", teal);
      s += line(365, 392, 455, 392) + line(710, 392, 800, 392) + line(1080, 392, 1170, 392);
      s += pathLine("M1300 465V660H225V465", teal, 3);
      s += note(765, 705, "将新 token 放回上下文，再预测下一个", teal);
      s += rect(350, 765, 850, 75, "#f1f7f4", teal) + note(768, 814, "遇到结束标记或长度上限时停止", ink);
      return s;
    },
  },
  {
    file: "foundation-models-and-inference/submodules/multimodal/assets/multimodal-principle.png",
    source: "Liu et al., Visual Instruction Tuning / LLaVA (2023), §3；教学简化",
    title: "视觉特征怎样接入语言模型",
    draw: () => {
      let s = box(110, 290, 245, 135, "输入图像", "发票 / 截图", blue);
      s += box(460, 290, 260, 135, "视觉编码器", "提取图像特征", teal);
      s += box(845, 290, 250, 135, "投影层", "映射到语言表示", orange);
      s += box(1180, 290, 260, 135, "语言模型", "条件生成回答", plum);
      s += line(355, 357, 460, 357) + line(720, 357, 845, 357) + line(1095, 357, 1180, 357);
      s += box(500, 610, 330, 105, "文字指令", "例如：金额是多少？", blue);
      s += pathLine("M830 660H1310V425", blue);
      s += rect(275, 765, 1000, 78, "#eef4f5", "#a9c7c6") + note(775, 813, "图像特征与文字指令一起参与生成；关键字段仍需回到原图校验。", ink);
      return s;
    },
  },
  {
    file: "foundation-models-and-inference/submodules/embedding/assets/embedding-principle.png",
    source: "Reimers & Gurevych, Sentence-BERT (2019), Figure 2；双塔推理简化",
    title: "双塔编码：查询和文档在同一空间比较",
    draw: () => {
      let s = box(115, 260, 325, 105, "查询", "酒店费用能报多少？", blue);
      s += box(115, 600, 325, 105, "文档段落", "住宿报销限额", orange);
      s += box(570, 250, 260, 125, "查询编码器", "产生向量 q", teal);
      s += box(570, 590, 260, 125, "文档编码器", "产生向量 d", teal);
      s += box(1010, 390, 365, 170, "相似度计算", "余弦 / 点积等", plum);
      s += line(440, 313, 570, 313) + line(440, 653, 570, 653);
      s += pathLine("M830 313H930V435H1010", teal) + pathLine("M830 653H930V525H1010", teal);
      s += rect(380, 765, 780, 78, "#f1f7f4", teal) + note(770, 812, "文档向量可以预先计算；相似度只是召回依据，不是事实证明。", ink);
      return s;
    },
  },
  {
    file: "foundation-models-and-inference/submodules/reranker/assets/reranker-principle.png",
    source: "Nogueira & Cho, Passage Re-ranking with BERT (2019), §2；联合输入简化",
    title: "交叉编码器：查询与候选一起阅读",
    draw: () => {
      let s = box(95, 240, 300, 115, "查询", "北京四级住宿上限", blue);
      s += box(95, 550, 300, 115, "候选段落", "不同地区和职级", orange);
      s += rect(500, 355, 310, 165, "#fff7f2", orange) + text(655, 420, "[CLS] 查询 [SEP]", 27, ink) + text(655, 465, "候选段落 [SEP]", 27, ink);
      s += box(890, 365, 265, 145, "BERT 联合编码", "跨词细节交互", plum);
      s += box(1230, 365, 245, 145, "相关性分数", "仅作排序依据", teal);
      s += pathLine("M395 298H450V385H500") + pathLine("M395 610H450V490H500");
      s += line(810, 437, 890, 437) + line(1155, 437, 1230, 437);
      s += rect(205, 750, 1125, 90, "#eef4f5", "#a9c7c6") + note(767, 807, "每个查询—候选对都要单独计算；得分不等于权限或事实可信度。", ink);
      return s;
    },
  },
  {
    file: "foundation-models-and-inference/submodules/adaptation/assets/adaptation-principle.png",
    source: "Hu et al., LoRA (2021), §4 / Figure 1；低秩增量示意",
    title: "LoRA：冻结底座，只训练增量",
    draw: () => {
      let s = box(90, 375, 230, 125, "输入 x", "任务样本", blue);
      s += box(470, 235, 310, 140, "基础权重 W", "冻结，不参与更新", muted);
      s += box(470, 590, 310, 140, "低秩矩阵 A · B", "训练得到 ΔW = BA", orange);
      s += `<circle cx="940" cy="475" r="52" fill="#fff7f2" stroke="${orange}" stroke-width="3"/>` + eq(940, 487, "+", orange);
      s += box(1130, 400, 330, 145, "输出 h", "h = Wx + BAx", teal);
      s += pathLine("M320 435H390V303H470") + pathLine("M320 455H390V660H470");
      s += pathLine("M780 305H850V455H888") + pathLine("M780 660H850V495H888") + line(992, 475, 1130, 475);
      s += note(762, 815, "QLoRA 还会量化冻结的底座；它不是另一条知识检索链。", plum);
      return s;
    },
  },
  {
    file: "tools-skills-and-protocols/assets/capabilities-principle.png",
    source: "Yao et al., ReAct (2022), §3；工具执行与观察的循环示意",
    title: "Agent 的判断—行动—观察闭环",
    draw: () => {
      let s = box(95, 300, 270, 145, "当前任务与证据", "目标、约束、状态", blue);
      s += box(475, 300, 260, 145, "模型判断", "选择下一步", plum);
      s += box(850, 300, 240, 145, "提出行动", "工具名与参数", orange);
      s += box(1190, 300, 255, 145, "工具执行", "受控执行层", teal);
      s += line(365, 372, 475, 372) + line(735, 372, 850, 372) + line(1090, 372, 1190, 372);
      s += box(850, 620, 390, 115, "外部观察", "结果 / 错误 / 新证据", teal);
      s += pathLine("M1320 445V675H1240") + pathLine("M850 675H605V445", blue);
      s += rect(210, 795, 1115, 70, "#f1f7f4", teal) + note(768, 840, "观察后可继续、追问或停止；有副作用的动作必须通过权限与确认。", ink);
      return s;
    },
  },
  {
    file: "tools-skills-and-protocols/submodules/skill/assets/skill-principle.png",
    source: "Agent Skills specification, progressive disclosure / SKILL.md；技能发现机制",
    title: "技能按需加载：先识别，再读正文与资源",
    draw: () => {
      let s = box(105, 310, 300, 145, "任务", "生成月度对账报告", blue);
      s += box(495, 250, 265, 120, "技能元数据", "名称 + 适用描述", teal);
      s += box(495, 515, 265, 120, "SKILL.md", "步骤与边界", plum);
      s += box(915, 515, 265, 120, "按需资源", "模板 / 脚本 / 参考", orange);
      s += box(1200, 345, 250, 130, "执行与验收", "真实结果与检查", teal);
      s += line(405, 382, 495, 312) + line(628, 370, 628, 515) + line(760, 575, 915, 575);
      s += pathLine("M1180 575H1275V475");
      s += note(785, 785, "未匹配到的技能无需加载全文；脚本依然由受控环境执行。", muted);
      return s;
    },
  },
  {
    file: "tools-skills-and-protocols/submodules/toolcalling/assets/toolcalling-principle.png",
    source: "MCP specification (2025-06-18), server/tools；Tool Calling 通用执行边界",
    title: "工具调用：模型给出意图，应用负责执行",
    draw: () => {
      let s = box(70, 295, 260, 145, "用户请求", "查询最新订单", blue);
      s += box(405, 295, 275, 145, "模型输出", "工具名 + 参数", plum);
      s += box(755, 295, 280, 145, "应用校验", "模式 / 权限 / 状态", orange);
      s += box(1115, 295, 335, 145, "工具服务", "读取权威结果", teal);
      s += line(330, 367, 405, 367) + line(680, 367, 755, 367) + line(1035, 367, 1115, 367);
      s += box(1115, 590, 335, 105, "结构化结果", "与本次调用标识关联", teal);
      s += pathLine("M1282 440V590") + pathLine("M1115 645H542V440", blue);
      s += rect(245, 770, 1045, 78, "#fff7f2", orange) + note(768, 819, "模型不能直接运行函数；收到结果后才决定继续或结束。", ink);
      return s;
    },
  },
  {
    file: "tools-skills-and-protocols/submodules/execution/assets/execution-principle.png",
    source: "OpenAI Computer Use guide；观察—动作—再观察机制，按执行层边界改绘",
    title: "浏览器执行：一次动作必须有新观察",
    draw: () => {
      let s = box(90, 295, 270, 160, "页面状态 S₀", "截图 / 可访问性信息", blue);
      s += box(445, 295, 260, 160, "模型选动作", "点击 / 输入 / 等待", plum);
      s += box(790, 295, 270, 160, "执行层把关", "权限 / 坐标 / 审批", orange);
      s += box(1145, 295, 295, 160, "页面状态 S₁", "重新读取并验证", teal);
      s += line(360, 375, 445, 375) + line(705, 375, 790, 375) + line(1060, 375, 1145, 375);
      s += pathLine("M1300 455V660H580V455", teal);
      s += note(925, 700, "状态未变或出现错误 → 重新判断", teal);
      s += rect(195, 785, 1150, 80, "#fff7f2", orange) + note(768, 835, "点击提交不等于提交成功；最终结果以业务系统回执为准。", ink);
      return s;
    },
  },
  {
    file: "tools-skills-and-protocols/submodules/mcp/assets/mcp-principle.png",
    source: "MCP specification (2025-06-18), Basic / Lifecycle；初始化时序",
    title: "MCP 初始化：协商后再调用能力",
    draw: () => {
      let s = box(190, 220, 250, 100, "Client", "应用侧连接", blue);
      s += box(1090, 220, 250, 100, "Server", "能力提供方", teal);
      s += `<path d="M315 320V810M1215 320V810" stroke="#a9b8be" stroke-width="3" stroke-dasharray="8 8"/>`;
      s += line(315, 400, 1215, 400, blue) + note(765, 383, "initialize：协议版本与客户端能力", blue);
      s += line(1215, 530, 315, 530, teal) + note(765, 513, "响应：版本、服务端能力与信息", teal);
      s += line(315, 650, 1215, 650, blue) + note(765, 633, "notifications/initialized", blue);
      s += line(315, 770, 1215, 770, orange) + note(765, 753, "随后再发现 / 读取 / 调用具体能力", orange);
      return s;
    },
  },
  {
    file: "tools-skills-and-protocols/submodules/mcpobjects/assets/mcpobjects-principle.png",
    source: "MCP specification (2025-06-18), Architecture / Tools / Resources / Prompts",
    title: "MCP 三种对象：请求路径并不相同",
    draw: () => {
      let s = box(90, 330, 265, 125, "Host 内的 Client", "按权限选择能力", blue);
      s += box(500, 330, 245, 125, "MCP Server", "声明可用对象", teal);
      s += box(980, 205, 355, 115, "Tool", "调用可执行动作", orange);
      s += box(980, 365, 355, 115, "Resource", "读取内容或数据", teal);
      s += box(980, 525, 355, 115, "Prompt", "获取可复用模板", plum);
      s += line(355, 392, 500, 392);
      s += pathLine("M745 365H825V260H980", orange) + pathLine("M745 392H980", teal) + pathLine("M745 420H825V580H980", plum);
      s += rect(170, 745, 1190, 90, "#eef4f5", "#a9c7c6") + note(765, 802, "发现对象不等于获得权限；写操作和返回内容仍受应用策略约束。", ink);
      return s;
    },
  },
  {
    file: "tools-skills-and-protocols/submodules/connector/assets/connector-principle.png",
    source: "RFC 9700 (OAuth 2.0 Security BCP), §§2–4；授权委托与资源调用简化",
    title: "连接器：凭据停在服务端，模型只提业务意图",
    draw: () => {
      let s = box(90, 330, 275, 145, "模型意图", "读取本人订单", blue);
      s += box(470, 330, 315, 145, "连接器", "身份 / 字段 / 错误转换", teal);
      s += box(880, 210, 270, 120, "凭据服务", "受限访问令牌", plum);
      s += box(1180, 330, 275, 145, "业务 API", "资源级授权判断", orange);
      s += line(365, 402, 470, 402) + line(785, 402, 1180, 402);
      s += pathLine("M625 330V270H880", plum) + pathLine("M1015 330V365H785", plum);
      s += box(870, 620, 315, 110, "结构化响应", "只返回允许字段", teal);
      s += pathLine("M1320 475V665H1185") + pathLine("M870 675H625V475", teal);
      s += note(775, 815, "模型不接触令牌；连接器也不能跳过后端对资源的授权。", muted);
      return s;
    },
  },
  {
    file: "project-retrospective/assets/retrospective-principle.png",
    source: "本项目对话与 series.json / check-wechat-articles.mjs；共创反馈机制",
    title: "人机共创：一次反馈如何改变下一版产物",
    draw: () => {
      let s = box(100, 320, 265, 125, "初版产物", "文章 / 图解 / 页面", blue);
      s += box(455, 320, 260, 125, "人工审阅", "指出可复现问题", plum);
      s += box(805, 320, 260, 125, "规则与清单", "记下边界和路径", orange);
      s += box(1155, 320, 265, 125, "下一版产物", "按清单生成", teal);
      s += line(365, 382, 455, 382) + line(715, 382, 805, 382) + line(1065, 382, 1155, 382);
      s += box(970, 610, 290, 115, "自动校验", "配对 / 字数 / 图片", teal);
      s += pathLine("M1288 445V610") + pathLine("M970 665H585V445", blue);
      s += rect(255, 775, 1035, 80, "#eef4f5", "#a9c7c6") + note(768, 825, "反馈进入规则后才可复用；校验失败应回到具体问题，而非增加套话。", ink);
      return s;
    },
  },
];

const requested = new Set(process.argv.slice(2));
const tempRoot = await mkdtemp(path.join(tmpdir(), "ai-agent-principle-diagrams-"));
for (const item of diagrams) {
  if (requested.size && !requested.has(item.file)) continue;
  const output = path.join(outRoot, item.file);
  await mkdir(path.dirname(output), { recursive: true });
  const svg = canvas(item.title, "原理示意图", item.draw(), item.source);
  const svgFile = path.join(tempRoot, path.basename(output, ".png") + ".svg");
  await writeFile(svgFile, svg);
  await execFile("sips", ["-s", "format", "png", svgFile, "--out", output]);
  console.log(path.relative(root, output));
}
await rm(tempRoot, { recursive: true, force: true });
