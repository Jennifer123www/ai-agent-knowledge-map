import { execFile as execFileCallback } from "node:child_process";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";

// These SVGs are only drawing intermediates. Public assets are PNG files.
const root = path.resolve(import.meta.dirname, "..");
const outRoot = path.join(root, "content/wechat/multi-agent-collaboration");
const execFile = promisify(execFileCallback);
const W = 1536;
const H = 1024;
const paper = "#fffdf8";
const ink = "#252a2d";
const muted = "#647078";
const teal = "#267b78";
const orange = "#c96f35";
const plum = "#7b5068";
const blue = "#426f8c";
const rose = "#a65d5d";
const paleTeal = "#edf6f4";
const paleOrange = "#fff3e8";
const palePlum = "#f6eef2";
const paleBlue = "#edf3f7";
const font = "'Noto Sans CJK SC','PingFang SC','Hiragino Sans GB',sans-serif";

const esc = (value) => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;");
const text = (x, y, value, size = 28, color = ink, anchor = "middle", weight = 500) =>
  `<text x="${x}" y="${y}" fill="${color}" text-anchor="${anchor}" font-family="${font}" font-size="${size}" font-weight="${weight}">${esc(value)}</text>`;
const rect = (x, y, w, h, fill = "#fff", stroke = "#bcc8cc", radius = 12, width = 2) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${fill}" stroke="${stroke}" stroke-width="${width}"/>`;
const arrowHead = (x, y, fromX, fromY, color = muted) => {
  const angle = Math.atan2(y - fromY, x - fromX);
  const rearX = x - 17 * Math.cos(angle);
  const rearY = y - 17 * Math.sin(angle);
  const spreadX = 8 * Math.sin(angle);
  const spreadY = 8 * Math.cos(angle);
  return `<path d="M${x} ${y}L${rearX + spreadX} ${rearY - spreadY}L${rearX - spreadX} ${rearY + spreadY}Z" fill="${color}"/>`;
};
const line = (x1, y1, x2, y2, color = muted, width = 3, dash = "") =>
  `<path d="M${x1} ${y1}L${x2} ${y2}" fill="none" stroke="${color}" stroke-width="${width}" ${dash ? `stroke-dasharray="${dash}"` : ""}/>` + arrowHead(x2, y2, x1, y1, color);
const pathArrow = (d, x, y, fromX, fromY, color = muted, width = 3, dash = "") =>
  `<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" ${dash ? `stroke-dasharray="${dash}"` : ""}/>` + arrowHead(x, y, fromX, fromY, color);
const box = (x, y, w, h, title, subtitle = "", color = teal, fill = "#fff") => {
  const titleY = y + (subtitle ? h / 2 - 8 : h / 2 + 10);
  return rect(x, y, w, h, fill, color) +
    `<rect x="${x}" y="${y}" width="8" height="${h}" rx="4" fill="${color}"/>` +
    text(x + w / 2 + 4, titleY, title, 29, ink, "middle", 700) +
    (subtitle ? text(x + w / 2 + 4, y + h / 2 + 35, subtitle, 21, muted) : "");
};
const note = (x, y, value, color = muted, anchor = "middle") => text(x, y, value, 22, color, anchor, 500);
const pill = (x, y, value, color = teal, fill = paleTeal) => {
  const w = Math.max(150, 42 + value.length * 27);
  return rect(x - w / 2, y - 27, w, 54, fill, color, 27, 2) + text(x, y + 9, value, 22, color, "middle", 650);
};

function canvas(title, eyebrow, body, source) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <rect width="${W}" height="${H}" fill="${paper}"/>
    <path d="M76 170H1460" stroke="#d3dcdd" stroke-width="2"/>
    ${text(76, 76, eyebrow, 22, teal, "start", 700)}
    ${text(76, 139, title, 48, ink, "start", 750)}
    ${body}
    <path d="M76 920H1460" stroke="#d3dcdd" stroke-width="2"/>
    ${text(76, 957, source, 18, muted, "start", 450)}
  </svg>`;
}

function flow(nodes, noteText = "", colors = [blue, teal, orange, plum, rose]) {
  const count = nodes.length;
  const gap = 52;
  const total = 1370;
  const width = (total - gap * (count - 1)) / count;
  const x0 = 83;
  let body = "";
  nodes.forEach((node, index) => {
    const x = x0 + index * (width + gap);
    body += box(x, 340, width, 155, node[0], node[1], colors[index % colors.length]);
    if (index < count - 1) body += line(x + width, 418, x + width + gap, 418, colors[(index + 1) % colors.length]);
  });
  if (noteText) body += rect(220, 690, 1096, 92, paleTeal, "#a7c9c7") + note(768, 747, noteText, ink);
  return body;
}

function compare(left, right, footer) {
  let body = text(385, 235, left.title, 32, plum, "middle", 750) + text(1150, 235, right.title, 32, teal, "middle", 750);
  body += `<path d="M768 205V800" stroke="#d7dfe0" stroke-width="2" stroke-dasharray="8 8"/>`;
  left.items.forEach((item, i) => { body += box(120, 300 + i * 145, 530, 102, item[0], item[1], plum, palePlum); });
  right.items.forEach((item, i) => { body += box(885, 300 + i * 145, 530, 102, item[0], item[1], teal, paleTeal); });
  body += rect(250, 790, 1035, 75, paleOrange, "#e4b692") + note(768, 839, footer, ink);
  return body;
}

function contract(rows, footer, header = "字段清单") {
  let body = rect(178, 235, 1180, 545, "#fff", "#b7c5c9", 14, 2);
  body += rect(178, 235, 1180, 80, paleBlue, blue, 14, 0) + text(768, 288, header, 30, blue, "middle", 750);
  rows.forEach((row, i) => {
    const y = 315 + i * 92;
    const color = [blue, teal, orange, plum, rose][i % 5];
    body += `<path d="M178 ${y}H1358" stroke="#dce3e4" stroke-width="2"/>`;
    body += text(238, y + 56, row[0], 24, color, "start", 700);
    body += text(520, y + 56, row[1], 23, ink, "start", 500);
  });
  body += note(768, 852, footer, muted);
  return body;
}

function matrix(cols, rows, marks, footer) {
  const x0 = 330;
  const y0 = 275;
  const cw = 245;
  const rh = 115;
  let body = "";
  cols.forEach((col, i) => { body += rect(x0 + i * cw, y0, cw, 90, paleBlue, "#becdd4", 0) + text(x0 + i * cw + cw / 2, y0 + 56, col, 23, blue, "middle", 700); });
  rows.forEach((row, r) => {
    body += rect(90, y0 + 90 + r * rh, 240, rh, paleOrange, "#e5c3a9", 0) + text(210, y0 + 90 + r * rh + 68, row, 23, orange, "middle", 700);
    cols.forEach((_, c) => {
      const value = marks[r][c];
      body += rect(x0 + c * cw, y0 + 90 + r * rh, cw, rh, "#fff", "#d8e0e1", 0);
      body += text(x0 + c * cw + cw / 2, y0 + 90 + r * rh + 67, value, 25, value === "适合" ? teal : value === "慎用" ? orange : muted, "middle", 650);
    });
  });
  body += note(768, 850, footer, ink);
  return body;
}

function cycle(nodes, centerTitle, centerSub, footer) {
  const positions = [[768, 250], [1180, 410], [1025, 720], [510, 720], [355, 410]];
  let body = box(625, 405, 286, 140, centerTitle, centerSub, plum, palePlum);
  nodes.forEach((node, i) => {
    const [cx, cy] = positions[i];
    body += box(cx - 130, cy - 52, 260, 104, node[0], node[1], [blue, teal, orange, rose, plum][i], "#fff");
    const [nx, ny] = positions[(i + 1) % nodes.length];
    const vx = nx - cx; const vy = ny - cy; const length = Math.hypot(vx, vy);
    const sx = cx + vx / length * 135; const sy = cy + vy / length * 65;
    const ex = nx - vx / length * 135; const ey = ny - vy / length * 65;
    body += line(sx, sy, ex, ey, [blue, teal, orange, rose, plum][i], 2);
  });
  body += note(768, 860, footer, ink);
  return body;
}

function hub(center, workers, footer) {
  let body = box(630, 380, 276, 150, center[0], center[1], plum, palePlum);
  const positions = [[130, 245], [1130, 245], [130, 650], [1130, 650]];
  workers.forEach((worker, i) => {
    const [x, y] = positions[i];
    body += box(x, y, 275, 120, worker[0], worker[1], [blue, teal, orange, rose][i]);
    const workerCenterX = x + 137;
    const workerCenterY = y + 60;
    const dx = workerCenterX - 768;
    const dy = workerCenterY - 455;
    const centerScale = Math.min(138 / Math.abs(dx), 75 / Math.abs(dy));
    const workerScale = Math.min(137 / Math.abs(dx), 60 / Math.abs(dy));
    const startX = 768 + dx * centerScale;
    const startY = 455 + dy * centerScale;
    const endX = workerCenterX - dx * workerScale;
    const endY = workerCenterY - dy * workerScale;
    body += line(startX, startY, endX, endY, [blue, teal, orange, rose][i], 2);
  });
  body += note(768, 856, footer, ink);
  return body;
}

function stateMachine(states, transitions, footer) {
  const positions = [[100, 340], [455, 225], [455, 545], [875, 225], [875, 545], [1230, 340]];
  let body = "";
  states.forEach((state, i) => {
    const [x, y] = positions[i];
    body += box(x, y, 210, 112, state[0], state[1], [blue, teal, orange, plum, rose, teal][i], "#fff");
  });
  transitions.forEach(([from, to, label, color = muted]) => {
    const [fx, fy] = positions[from]; const [tx, ty] = positions[to];
    const sourceCenterX = fx + 105; const sourceCenterY = fy + 56;
    const targetCenterX = tx + 105; const targetCenterY = ty + 56;
    const dx = targetCenterX - sourceCenterX; const dy = targetCenterY - sourceCenterY;
    const sourceScale = Math.min(105 / Math.abs(dx), 56 / Math.abs(dy));
    const targetScale = Math.min(105 / Math.abs(dx), 56 / Math.abs(dy));
    const x1 = sourceCenterX + dx * sourceScale; const y1 = sourceCenterY + dy * sourceScale;
    const x2 = targetCenterX - dx * targetScale; const y2 = targetCenterY - dy * targetScale;
    body += line(x1, y1, x2, y2, color, 2);
    body += pill((x1 + x2) / 2, (y1 + y2) / 2 - 26, label, color, "#fff");
  });
  body += note(768, 855, footer, ink);
  return body;
}

function checkpoint(footer) {
  let body = box(80, 315, 250, 130, "读取资料", "完成，可重放", blue);
  body += box(430, 315, 250, 130, "生成提纲", "完成，可重放", teal);
  body += box(780, 315, 250, 130, "提交审批", "已发送，不可盲重放", orange);
  body += box(1130, 315, 250, 130, "发布报告", "尚未执行", plum);
  body += line(330, 380, 430, 380) + line(680, 380, 780, 380) + line(1030, 380, 1130, 380);
  body += rect(690, 585, 430, 135, paleOrange, orange) + text(905, 635, "检查点", 29, orange, "middle", 750) + note(905, 680, "状态 + 回执 + 下一步", ink);
  body += pathArrow("M905 585V445", 905, 445, 905, 585, orange, 3, "8 6");
  body += rect(235, 785, 1065, 68, paleTeal, "#a7c9c7") + note(768, 830, footer, ink);
  return body;
}

const diagrams = [
  // Overview
  {
    file: "assets/orchestration-choice.png", title: "先选最简单的协作结构", eyebrow: "选择图",
    source: "依据 Anthropic, Building Effective AI Agents；结合工程取舍改绘",
    draw: () => compare(
      { title: "任务越稳定，结构越固定", items: [["单次模型调用", "一步能完成"], ["固定工作流", "路径已知、便于测试"], ["少量分支", "条件清楚、异常可枚举"]] },
      { title: "不确定性越高，才增加自治", items: [["多智能体", "子问题独立且需专长"], ["主管调度", "分工需运行时决定"], ["任务交接", "控制权确实需要转移"]] },
      "能用一条稳定链路解决，就不必先组一支 Agent 战队。",
    ),
  },
  {
    file: "assets/orchestration-task-contract.png", title: "协作从任务契约开始", eyebrow: "结构图",
    source: "本项目任务契约模型；字段设计参考 OpenAI Agents SDK 与工程实践",
    draw: () => contract([
      ["目标", "完成供应商选型报告中的技术风险部分"],
      ["输入", "候选名单、需求清单、截至日期、可用资料"],
      ["输出", "结论、证据链接、未知项、置信说明"],
      ["权限", "只读公开资料；不得发送邮件或修改表格"],
      ["验收", "每项结论可追溯；未决问题明确列出"],
    ], "把“帮我查一下”改成可验收的交付，协作才有边界。", "任务契约：交付前先把边界写清楚"),
  },
  {
    file: "assets/orchestration-patterns.png", title: "四种常见协作结构", eyebrow: "模式图",
    source: "Anthropic workflow patterns；OpenAI Agents SDK orchestration / handoffs",
    draw: () => matrix(
      ["顺序", "并行", "主管", "交接"],
      ["路径预先知道", "子任务彼此独立", "分工运行时决定", "控制权需要转移"],
      [["适合", "慎用", "慎用", "慎用"], ["慎用", "适合", "可用", "慎用"], ["不适合", "不适合", "适合", "可用"], ["不适合", "不适合", "可用", "适合"]],
      "模式不是越复杂越高级，关键是任务依赖与控制权。",
    ),
  },
  {
    file: "assets/orchestration-failure-budget.png", title: "一次协作要同时管住四类预算", eyebrow: "控制图",
    source: "多智能体工程控制清单；结合延迟、成本、错误传播与权限边界",
    draw: () => hub(["协作预算", "超过任一上限就停"], [
      ["调用预算", "最多多少轮、多少次工具"],
      ["时间预算", "单步与总任务超时"],
      ["风险预算", "哪些动作必须人工确认"],
      ["错误预算", "连续失败几次转人工"],
    ], "停止条件必须写进运行时，不能只写在提示词里。"),
  },
  {
    file: "assets/orchestration-principle.png", title: "主管—专家协作：委派、交付、验收", eyebrow: "原理示意图",
    source: "Wu et al., AutoGen (2023)；OpenAI Agents SDK orchestration；教学简化",
    draw: () => cycle([
      ["拆分任务", "写清目标与验收"], ["选择专家", "按能力与权限路由"], ["返回结果", "结论 + 证据 + 未决项"], ["交叉验收", "检查冲突与缺口"], ["合并或补证", "满足标准才结束"],
    ], "主管 Agent", "维护目标、状态与预算", "协作不是自由群聊，而是带契约和验收的闭环。"),
  },

  // Workflow
  {
    file: "submodules/workflow/assets/workflow-fixed-path.png", title: "固定工作流：报销草稿沿着已知路径走", eyebrow: "流程图",
    source: "Anthropic prompt chaining / routing patterns；差旅报销案例改绘",
    draw: () => flow([["读取申请", "字段与票据"], ["校验规则", "金额、日期、标准"], ["模型写说明", "只组织文字"], ["人工确认", "核对异常"], ["提交草稿", "记录回执"]], "模型负责不确定的文字工作，规则与写操作交给确定性节点。"),
  },
  {
    file: "submodules/workflow/assets/workflow-branching.png", title: "条件分支：异常不能挤进同一条直线", eyebrow: "分支图",
    source: "工作流条件路由与异常处理；差旅报销案例",
    draw: () => stateMachine(
      [["读取申请", "入口"], ["资料齐全", "正常分支"], ["缺少票据", "退回补充"], ["金额合规", "继续"], ["超过标准", "人工审批"], ["生成草稿", "统一出口"]],
      [[0,1,"齐全",teal],[0,2,"缺失",orange],[1,3,"合规",teal],[1,4,"超标",orange],[3,5,"通过",teal],[4,5,"批准",plum]],
      "把异常画成明确分支，才能测试、统计和追责。",
    ),
  },
  {
    file: "submodules/workflow/assets/workflow-idempotency.png", title: "重试不等于再提交一次", eyebrow: "机制图",
    source: "幂等写入与补偿模式；报销提交案例",
    draw: () => compare(
      { title: "危险重试", items: [["第一次提交", "服务端已成功"], ["客户端超时", "没有收到回执"], ["再次提交", "可能生成两条申请"]] },
      { title: "幂等重试", items: [["生成幂等键", "同一业务请求同一键"], ["查询已有回执", "先确认是否成功"], ["复用结果", "不重复产生副作用"]] },
      "写操作先查状态，再决定重试；必要时进入人工核对。",
    ),
  },
  {
    file: "submodules/workflow/assets/workflow-observability.png", title: "一条工作流要留下哪些证据", eyebrow: "观测图",
    source: "工作流可观测性清单；节点、输入摘要、输出、回执与耗时",
    draw: () => contract([
      ["运行标识", "同一次报销任务使用统一 run_id"],
      ["节点记录", "开始、结束、输入摘要、输出摘要"],
      ["模型记录", "模型版本、提示词版本、token 与延迟"],
      ["工具回执", "请求标识、状态码、业务结果"],
      ["决策记录", "分支条件、人工审批人和时间"],
    ], "日志不是堆满原文；敏感数据要脱敏，关键回执要可追溯。", "一次运行应保存的关键证据"),
  },
  {
    file: "submodules/workflow/assets/workflow-principle.png", title: "工作流的核心：确定路径包住不确定模型", eyebrow: "原理示意图",
    source: "Anthropic, Building Effective AI Agents：prompt chaining、routing、parallelization",
    draw: () => flow([["确定性输入", "结构化字段"], ["代码校验", "规则与权限"], ["模型节点", "理解或生成"], ["代码验收", "格式与事实"], ["受控写入", "幂等并留回执"]], "模型节点可以不确定，但进入和离开它的边界必须可检查。"),
  },

  // State graph
  {
    file: "submodules/stategraph/assets/stategraph-state-object.png", title: "状态对象保存事实，不保存一句“做到一半”", eyebrow: "结构图",
    source: "LangGraph persistence / checkpoints；研究报告案例",
    draw: () => contract([
      ["目标", "完成三家模型平台的对比报告"],
      ["当前位置", "技术资料检索已完成，价格资料待补"],
      ["中间产物", "已确认来源、待核对数字、草稿路径"],
      ["动作回执", "哪些查询成功，哪些写操作已经发生"],
      ["下一步", "从价格核验继续；不得重复发送审批"],
    ], "聊天记录可以辅助理解，但不能替代可验证的任务状态。", "研究任务的显式状态"),
  },
  {
    file: "submodules/stategraph/assets/stategraph-transition.png", title: "状态转移要经过守卫条件", eyebrow: "状态图",
    source: "Harel, Statecharts (1987)；结合 Agent 任务图改绘",
    draw: () => stateMachine(
      [["待执行", "入口"], ["资料检索", "运行中"], ["等待补充", "人工输入"], ["事实核验", "运行中"], ["等待审批", "人工确认"], ["已完成", "终态"]],
      [[0,1,"开始",blue],[1,2,"缺资料",orange],[1,3,"资料齐",teal],[2,3,"已补充",plum],[3,4,"高风险",orange],[3,5,"低风险",teal],[4,5,"批准",plum]],
      "守卫条件阻止任务跳过必要验证，也让异常路径变得可解释。",
    ),
  },
  {
    file: "submodules/stategraph/assets/stategraph-checkpoint.png", title: "检查点必须同时保存状态与副作用回执", eyebrow: "恢复图",
    source: "LangGraph checkpoint persistence；结合幂等恢复语义改绘",
    draw: () => checkpoint("恢复时先读回执：可重放的计算继续，不可重放的写操作先确认。"),
  },
  {
    file: "submodules/stategraph/assets/stategraph-recovery.png", title: "故障恢复的三步判断", eyebrow: "决策图",
    source: "持久化执行与故障恢复工程实践；研究报告案例",
    draw: () => flow([["读取检查点", "最后一致状态"], ["核对外部回执", "写操作是否成功"], ["判定动作类型", "可重放 / 不可重放"], ["恢复或转人工", "保留原 run_id"]], "恢复不是“从最后一句继续”，而是从最后一个可信状态继续。"),
  },
  {
    file: "submodules/stategraph/assets/stategraph-principle.png", title: "状态图：状态、节点与转移共同约束任务", eyebrow: "原理示意图",
    source: "Harel, Statecharts (1987)；LangGraph persistence；教学简化",
    draw: () => cycle([
      ["读取状态", "目标与中间产物"], ["检查守卫", "是否允许进入节点"], ["执行节点", "模型或工具"], ["写入检查点", "状态与动作回执"], ["选择转移", "继续、暂停或结束"],
    ], "任务状态图", "显式状态驱动执行", "每一步都从状态出发，并把结果写回状态。"),
  },

  // Multi-agent
  {
    file: "submodules/multiagent/assets/multiagent-fit.png", title: "什么任务值得拆给多个 Agent", eyebrow: "判断图",
    source: "Anthropic parallelization / orchestrator-workers；多智能体工程实践",
    draw: () => matrix(
      ["能独立完成", "依赖很强", "需不同权限", "需同一口径"],
      ["市场调研", "技术验证", "财务核算", "最终定稿"],
      [["适合", "慎用", "可用", "慎用"], ["适合", "慎用", "适合", "慎用"], ["适合", "慎用", "适合", "慎用"], ["不适合", "适合", "慎用", "适合"]],
      "独立性高、验收清楚、并行收益明显，才值得拆分。",
    ),
  },
  {
    file: "submodules/multiagent/assets/multiagent-parallel.png", title: "并行协作：共享任务，不共享全部思考过程", eyebrow: "协作图",
    source: "Anthropic parallelization；三路产品调研案例",
    draw: () => hub(["统一任务单", "相同范围、截止时间与格式"], [
      ["市场 Agent", "份额、客户与生态"],
      ["技术 Agent", "架构、性能与风险"],
      ["财务 Agent", "价格、合同与成本"],
      ["评审 Agent", "交叉核对与缺口"],
    ], "各 Agent 只拿必要上下文，结果通过结构化交付汇合。"),
  },
  {
    file: "submodules/multiagent/assets/multiagent-evidence.png", title: "Agent 交付的不是一句结论", eyebrow: "交付图",
    source: "多智能体中间产物规范；证据、未知项与冲突字段",
    draw: () => contract([
      ["结论", "一句话说明发现，不用形容词代替判断"],
      ["证据", "来源、发布时间、摘录位置、访问时间"],
      ["适用范围", "结论覆盖哪些版本、地区或客户"],
      ["未知项", "缺少哪些资料，哪些数字尚未确认"],
      ["冲突项", "与其他 Agent 的哪条结论不一致"],
    ], "没有证据和边界的“专业意见”，只会把核验成本推给下一个人。", "结构化交付：结论之外还要交什么"),
  },
  {
    file: "submodules/multiagent/assets/multiagent-evaluation.png", title: "多 Agent 必须与更简单方案做对照", eyebrow: "评测图",
    source: "Agent evaluation engineering；单 Agent 与多 Agent 对照实验",
    draw: () => compare(
      { title: "单 Agent 基线", items: [["任务成功率", "同一案例集"], ["事实错误率", "同一验收口径"], ["成本与延迟", "完整链路统计"]] },
      { title: "多 Agent 方案", items: [["是否更准确", "提升是否稳定"], ["是否更可追溯", "证据链是否完整"], ["代价是否值得", "调用与协调开销"]] },
      "只比较“回答更长”没有意义；要比较同一任务的净收益。",
    ),
  },
  {
    file: "submodules/multiagent/assets/multiagent-principle.png", title: "多智能体：独立产出经共享状态汇合", eyebrow: "原理示意图",
    source: "Wu et al., AutoGen (2023), Figure 1；Anthropic orchestrator-workers；教学简化",
    draw: () => hub(["共享状态", "目标、任务单、证据与预算"], [
      ["Agent A", "独立上下文与工具"],
      ["Agent B", "独立上下文与工具"],
      ["Agent C", "独立上下文与工具"],
      ["验收器", "冲突、缺口与终止"],
    ], "Agent 之间交换可验证产物，不靠无限转发聊天记录维持协作。"),
  },

  // Supervisor
  {
    file: "submodules/supervisor/assets/supervisor-contract.png", title: "主管下发任务时必须带齐五件事", eyebrow: "任务单",
    source: "OpenAI Agents SDK manager pattern；任务契约工程实践",
    draw: () => contract([
      ["任务目标", "核对三家供应商的技术风险"],
      ["输入范围", "候选清单、版本、资料截止日期"],
      ["交付格式", "结论、证据、未知项、建议下一步"],
      ["权限边界", "只读资料；禁止外发和修改采购系统"],
      ["停止条件", "找到三条独立证据或明确资料不足"],
    ], "主管的第一份产物不是答案，而是可执行、可验收的任务单。", "主管下发的任务单"),
  },
  {
    file: "submodules/supervisor/assets/supervisor-routing.png", title: "专家路由看能力，也看权限和负载", eyebrow: "路由图",
    source: "OpenAI Agents SDK orchestration；动态路由工程实践",
    draw: () => matrix(
      ["能力匹配", "数据权限", "当前负载", "历史质量"],
      ["市场专家", "技术专家", "财务专家", "人工专家"],
      [["适合", "可用", "空闲", "稳定"], ["适合", "适合", "繁忙", "稳定"], ["适合", "适合", "空闲", "待观察"], ["兜底", "适合", "排队", "高"]],
      "只按关键词选专家，容易把任务送给“会说但没权限”的角色。",
    ),
  },
  {
    file: "submodules/supervisor/assets/supervisor-conflict.png", title: "结论冲突时，主管先补证再裁定", eyebrow: "冲突处理",
    source: "多智能体验收与冲突消解；供应商调研案例",
    draw: () => flow([["发现冲突", "同一指标两个答案"], ["核对口径", "版本、时间、范围"], ["要求补证", "回到一手来源"], ["记录分歧", "无法消除就明示"], ["人工裁定", "高风险结论"]], "主管不能用“多数票”替代事实核验。"),
  },
  {
    file: "submodules/supervisor/assets/supervisor-budget.png", title: "防循环：每次委派都消耗可见预算", eyebrow: "控制图",
    source: "Agent runtime budgets；防止重复委派和无效对话",
    draw: () => cycle([
      ["检查缺口", "是否真的需要继续"], ["扣减预算", "轮次、token、时间"], ["委派一次", "记录任务指纹"], ["验收增量", "是否增加新证据"], ["停止或升级", "无增量就转人工"],
    ], "主管循环", "每轮都要产生可验收增量", "同一任务指纹重复出现，应直接拦截而不是继续转发。"),
  },
  {
    file: "submodules/supervisor/assets/supervisor-principle.png", title: "主管模式：统一保留控制权，专家只交付结果", eyebrow: "原理示意图",
    source: "OpenAI Agents SDK manager pattern；Anthropic orchestrator-workers；教学简化",
    draw: () => hub(["主管 Agent", "拆分、路由、验收与合并"], [
      ["市场专家", "返回市场证据"],
      ["技术专家", "返回技术证据"],
      ["财务专家", "返回成本证据"],
      ["人工审批", "高风险决策"],
    ], "专家不直接接管会话；主管维护统一目标、状态和最终答案。"),
  },

  // Handoff
  {
    file: "submodules/handoff/assets/handoff-package.png", title: "一次合格交接需要一个最小上下文包", eyebrow: "交接包",
    source: "OpenAI Agents SDK handoffs；任务交接工程实践",
    draw: () => contract([
      ["用户目标", "申请订单退款，不是咨询退款政策"],
      ["已知事实", "订单号、金额、支付方式、当前状态"],
      ["已做动作", "身份已核验；尚未创建退款单"],
      ["未决问题", "退款原因需要用户补充"],
      ["权限与下一步", "退款 Agent 可建草稿；付款需人工批准"],
    ], "交接包越长不一定越好，关键是事实、状态、边界和下一步。", "最小交接包：接手后能继续工作"),
  },
  {
    file: "submodules/handoff/assets/handoff-control.png", title: "主管调用与任务交接的控制权不同", eyebrow: "对比图",
    source: "OpenAI Agents SDK orchestration / handoffs",
    draw: () => compare(
      { title: "主管调用专家", items: [["谁面对用户", "主管始终在场"], ["专家返回什么", "结构化结果"], ["谁生成最终答复", "主管"]] },
      { title: "任务交接 Handoff", items: [["谁面对用户", "新 Agent 接管"], ["原 Agent 做什么", "交出上下文与控制权"], ["谁继续后续步骤", "新 Agent"]] },
      "只是问专家一个问题，用调用；后续责任真的转移，才用交接。",
    ),
  },
  {
    file: "submodules/handoff/assets/handoff-human.png", title: "人工参与不是终点，而是受控暂停", eyebrow: "人工回路",
    source: "OpenAI Agents SDK human-in-the-loop；审批与恢复语义",
    draw: () => flow([["Agent 提议动作", "退款金额与理由"], ["运行时暂停", "冻结当前状态"], ["人工查看证据", "批准、拒绝或修改"], ["写回决定", "带审批人与时间"], ["从原状态恢复", "继续或安全结束"]], "审批结果必须进入状态，不能只留在聊天消息里。"),
  },
  {
    file: "submodules/handoff/assets/handoff-resume.png", title: "交接后恢复：新 Agent 先确认，再行动", eyebrow: "恢复图",
    source: "Handoff state transfer 与业务副作用控制；退款案例",
    draw: () => flow([["读取交接包", "目标与已知事实"], ["核对关键字段", "订单、身份、动作回执"], ["补问缺口", "只问未知信息"], ["声明下一步", "让用户知道谁在处理"], ["执行受控动作", "留业务回执"]], "新 Agent 不应重新盘问，也不能假装之前的动作已经完成。"),
  },
  {
    file: "submodules/handoff/assets/handoff-principle.png", title: "任务交接：上下文与控制权一起转移", eyebrow: "原理示意图",
    source: "OpenAI Agents SDK handoffs / human-in-the-loop；教学简化",
    draw: () => flow([["分诊 Agent", "识别退款意图"], ["准备交接包", "事实、状态、未决项"], ["退款 Agent", "接管会话与任务"], ["人工审批", "高风险动作"], ["恢复并回执", "同一任务继续"]], "Handoff 不是转发一句话，而是把责任、状态和权限边界交给下一位。"),
  },
];

const requested = new Set(process.argv.slice(2));
const tempRoot = await mkdtemp(path.join(tmpdir(), "multi-agent-figures-"));
for (const item of diagrams) {
  if (requested.size && !requested.has(item.file)) continue;
  const output = path.join(outRoot, item.file);
  await mkdir(path.dirname(output), { recursive: true });
  const svg = canvas(item.title, item.eyebrow, item.draw(), item.source);
  const svgFile = path.join(tempRoot, item.file.replaceAll("/", "-").replace(/\.png$/, ".svg"));
  await writeFile(svgFile, svg);
  await execFile("sips", ["-s", "format", "png", svgFile, "--out", output]);
  console.log(path.relative(root, output));
}
await rm(tempRoot, { recursive: true, force: true });
