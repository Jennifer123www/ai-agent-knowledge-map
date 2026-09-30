import { execFile as execFileCallback } from "node:child_process";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";

// SVG is only an intermediate; public WeChat assets are PNG files.
const root = path.resolve(import.meta.dirname, "..");
const outRoot = path.join(root, "content/wechat/07-evaluation-observability-and-improvement");
const execFile = promisify(execFileCallback);
const W = 1536; const H = 1024;
const paper = "#fffdf8"; const ink = "#252a2d"; const muted = "#66727a";
const teal = "#267b78"; const orange = "#c96f35"; const blue = "#426f8c"; const plum = "#7b5068"; const rose = "#a65d5d";
const paleTeal = "#edf6f4"; const paleOrange = "#fff3e8"; const paleBlue = "#edf3f7"; const palePlum = "#f6eef2";
const font = "'Noto Sans CJK SC','PingFang SC','Hiragino Sans GB',sans-serif";
const colors = [blue, teal, orange, plum, rose];
const fills = [paleBlue, paleTeal, paleOrange, palePlum, "#faeeee"];
const esc = (v) => String(v).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
const text = (x, y, v, size = 28, color = ink, anchor = "middle", weight = 500) => `<text x="${x}" y="${y}" fill="${color}" text-anchor="${anchor}" font-family="${font}" font-size="${size}" font-weight="${weight}">${esc(v)}</text>`;
const rect = (x, y, w, h, fill = "#fff", stroke = "#c1cccf", radius = 12, width = 2) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${fill}" stroke="${stroke}" stroke-width="${width}"/>`;
const arrowHead = (x, y, fx, fy, color = muted) => { const a = Math.atan2(y - fy, x - fx); const rx = x - 17 * Math.cos(a); const ry = y - 17 * Math.sin(a); const sx = 8 * Math.sin(a); const sy = 8 * Math.cos(a); return `<path d="M${x} ${y}L${rx + sx} ${ry - sy}L${rx - sx} ${ry + sy}Z" fill="${color}"/>`; };
const line = (x1, y1, x2, y2, color = muted, width = 3, dash = "") => `<path d="M${x1} ${y1}L${x2} ${y2}" fill="none" stroke="${color}" stroke-width="${width}" ${dash ? `stroke-dasharray="${dash}"` : ""}/>` + arrowHead(x2, y2, x1, y1, color);
const box = (x, y, w, h, title, sub = "", color = teal, fill = "#fff") => rect(x, y, w, h, fill, color) + `<rect x="${x}" y="${y}" width="8" height="${h}" rx="4" fill="${color}"/>` + text(x + w / 2 + 4, y + (sub ? h / 2 - 8 : h / 2 + 10), title, 28, ink, "middle", 700) + (sub ? text(x + w / 2 + 4, y + h / 2 + 34, sub, 20, muted) : "");
const note = (x, y, v, color = muted) => text(x, y, v, 22, color, "middle", 500);
const canvas = (title, eyebrow, body, source) => `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="${paper}"/><path d="M76 170H1460" stroke="#d3dcdd" stroke-width="2"/>${text(76, 76, eyebrow, 22, teal, "start", 700)}${text(76, 139, title, 48, ink, "start", 760)}${body}<path d="M76 920H1460" stroke="#d3dcdd" stroke-width="2"/>${text(76, 957, source, 18, muted, "start", 450)}</svg>`;

function flow(nodes, footer = "", y = 350) {
  const gap = 46; const x0 = 82; const total = 1372; const w = (total - gap * (nodes.length - 1)) / nodes.length;
  let body = "";
  nodes.forEach((n, i) => { const x = x0 + i * (w + gap); body += box(x, y, w, 150, n[0], n[1], colors[i % colors.length], fills[i % fills.length]); if (i < nodes.length - 1) body += line(x + w, y + 75, x + w + gap, y + 75, colors[(i + 1) % colors.length]); });
  if (footer) body += rect(210, 700, 1116, 90, paleTeal, "#a7c9c7") + note(768, 756, footer, ink);
  return body;
}
function cycle(nodes, center, footer) {
  const pos = [[768, 245], [1190, 410], [1025, 710], [510, 710], [345, 410]];
  let body = box(626, 400, 284, 140, center[0], center[1], plum, palePlum);
  nodes.forEach((n, i) => { const [cx, cy] = pos[i]; body += box(cx - 130, cy - 52, 260, 104, n[0], n[1], colors[i], fills[i]); const [nx, ny] = pos[(i + 1) % pos.length]; const dx = nx - cx; const dy = ny - cy; const len = Math.hypot(dx, dy); body += line(cx + dx / len * 140, cy + dy / len * 62, nx - dx / len * 140, ny - dy / len * 62, colors[i], 2); });
  body += note(768, 858, footer, ink); return body;
}
function table(header, rows, footer = "") {
  let body = rect(170, 235, 1196, 555, "#fff", "#b9c6ca", 14, 2) + rect(170, 235, 1196, 80, paleBlue, blue, 14, 0) + text(768, 287, header, 30, blue, "middle", 750);
  rows.forEach((r, i) => { const y = 315 + i * 92; body += `<path d="M170 ${y}H1366" stroke="#dbe3e4" stroke-width="2"/>` + text(230, y + 56, r[0], 24, colors[i % colors.length], "start", 700) + text(520, y + 56, r[1], 22, ink, "start", 500); });
  if (footer) body += note(768, 850, footer, ink); return body;
}
function compare(left, right, footer) {
  let body = text(385, 235, left.title, 32, plum, "middle", 750) + text(1150, 235, right.title, 32, teal, "middle", 750) + `<path d="M768 205V800" stroke="#d7dfe0" stroke-width="2" stroke-dasharray="8 8"/>`;
  left.items.forEach((n, i) => { body += box(105, 295 + i * 150, 555, 108, n[0], n[1], plum, palePlum); });
  right.items.forEach((n, i) => { body += box(875, 295 + i * 150, 555, 108, n[0], n[1], teal, paleTeal); });
  body += rect(220, 790, 1096, 78, paleOrange, "#e4b692") + note(768, 840, footer, ink); return body;
}
function lanes(cols, rows, footer) {
  const x0 = 235; const y0 = 255; const cw = 245; const rh = 112; let body = "";
  cols.forEach((c, i) => body += rect(x0 + i * cw, y0, cw, 78, paleBlue, "#bdcdd4", 0) + text(x0 + i * cw + cw / 2, y0 + 50, c, 22, blue, "middle", 700));
  rows.forEach((r, i) => { body += rect(75, y0 + 78 + i * rh, 160, rh, paleOrange, "#e5c3a9", 0) + text(155, y0 + 78 + i * rh + 65, r[0], 21, orange, "middle", 700); r.slice(1).forEach((v, j) => body += rect(x0 + j * cw, y0 + 78 + i * rh, cw, rh, "#fff", "#d8e0e1", 0) + text(x0 + j * cw + cw / 2, y0 + 78 + i * rh + 64, v, 21, ink, "middle", 550)); });
  body += note(768, 855, footer, ink); return body;
}
function tree(rootNode, branches, footer) {
  let body = box(610, 230, 316, 110, rootNode[0], rootNode[1], plum, palePlum);
  const xs = [80, 370, 660, 950, 1240];
  branches.forEach((b, i) => { body += box(xs[i], 520, 220, 118, b[0], b[1], colors[i], fills[i]); body += line(768, 340, xs[i] + 110, 520, colors[i], 2); });
  body += note(768, 825, footer, ink); return body;
}

const D = [
  ["assets/evaluation-loop.png", "从单次轨迹到持续优化闭环", "原理示意图", "OpenTelemetry；OpenAI agent evals；教学改绘", () => cycle([["链路追踪", "还原一次任务"], ["离线评测", "固定条件比较"], ["受控发布", "影子、灰度、A/B"], ["线上监控", "观察真实分布"], ["反馈回流", "形成新样本"]], ["可验证成功", "结果 + 过程 + 风险"], "每一轮改进都要留下版本、证据和回退路径。")],
  ["assets/evaluation-metric-layers.png", "Agent 评测不能只看一个总分", "指标分层", "任务结果、过程、安全与资源的分层评测", () => table("四层指标分别回答四个问题", [["结果", "任务是否办成，业务状态与事实是否正确"], ["过程", "检索、工具、状态和交接是否合理"], ["风险", "是否越权、泄露、错误写入或绕过审批"], ["资源", "时延、token、调用次数和费用是否值得"]], "安全硬门槛不能被平均分抵消。")],
  ["assets/evaluation-failure-attribution.png", "一次错误怎样定位到具体环节", "归因图", "Agent trace grading 与故障归因；教学简化", () => flow([["用户投诉", "十五天政策答成七天"], ["锁定 Trace", "关联任务与版本"], ["逐段核对", "检索、模型、工具、状态"], ["提出根因", "活动标签导致漏召回"], ["回归验证", "同类样本稳定通过"]], "相关性只用于缩小范围，根因还要靠复现与对照。")],
  ["assets/evaluation-evidence-gate.png", "候选版本要连续通过四道证据门", "发布门槛", "离线评测与生产发布门槛", () => flow([["安全硬门槛", "越权、泄露、错误写入"], ["关键能力", "高风险切片不退化"], ["目标收益", "任务成功有意义提升"], ["资源预算", "时延与成本可接受"], ["受控上线", "影子、灰度、可回滚"]], "通过离线门槛，只代表获得进入线上小流量验证的资格。")],
  ["assets/evaluation-baseline.png", "复杂 Agent 必须与简单基线比较", "对照图", "工程基线与增量收益比较", () => lanes(["规则流程", "单次调用", "旧 Agent", "新 Agent", "人工"], [["质量", "稳定窄域", "语言灵活", "已知基线", "待验证", "专业复核"], ["时延", "低", "较低", "中", "可能更高", "高"], ["成本", "低", "较低", "中", "需核算", "高"], ["风险", "可预测", "无行动", "已有记录", "需灰度", "可追责"]], "新方案要证明增量价值，而不是只证明它更复杂。")],

  ["submodules/01-trace/assets/trace-tree.png", "一次售后任务的 Trace 与 Span 树", "原理示意图", "OpenTelemetry Trace 语义；OpenAI Agents SDK Tracing；教学改绘", () => tree(["Trace：退货申请", "统一 Trace ID 与任务版本"], [["订单 Span", "读取订单与商品"], ["检索 Span", "召回并重排政策"], ["模型 Span", "生成资格判断"], ["工具 Span", "创建退货草稿"], ["状态 Span", "完成或转人工"]], "Span 有开始、结束、状态与父子关系；跨服务仍携带同一上下文。")],
  ["submodules/01-trace/assets/trace-span-fields.png", "不同 Span 应保留哪些关键字段", "字段图", "OpenTelemetry 与 Agent tracing 字段模型", () => table("必要字段按操作类型补充", [["通用", "Trace/Span ID、父子关系、时间、状态、服务"], ["模型", "模型与提示版本、token、停止原因、响应标识"], ["检索", "查询摘要、索引版本、候选与排序结果"], ["工具", "工具版本、参数摘要、错误码、业务回执"], ["状态", "转移前后、分支理由、人工决定与版本"]], "记录决定结果的事实，不复制无关敏感原文。")],
  ["submodules/01-trace/assets/trace-diagnosis.png", "沿 Trace 从投诉定位根因", "诊断图", "分布式追踪与故障归因流程", () => flow([["确认业务失败", "期望十五天，实际七天"], ["查看模型输入", "只有通用政策"], ["查看检索候选", "活动条款被过滤"], ["比较成功样本", "活动标签缺失"], ["建立回归题", "验证修复不复发"]], "不要把第一个红色节点或最慢 Span 直接当根因。")],
  ["submodules/01-trace/assets/trace-sampling.png", "追踪采样按风险与诊断价值分层", "采样图", "OpenTelemetry 采样原则；Agent 风险分层", () => compare({title:"常态流量",items:[["随机样本","保持总体代表性"],["低风险成功","较低采样率"],["稳定旧版本","控制存储成本"]]},{title:"重点保留",items:[["错误与慢请求","尾部规则保留"],["高风险写入","尽量完整留证"],["新版本灰度","提高采样率"]]},"只采报错会漏掉‘快速但答错’的隐性失败。")],
  ["submodules/01-trace/assets/trace-privacy.png", "Trace 数据也要经过治理", "隐私边界", "NIST AI RMF；OpenTelemetry 数据治理实践", () => flow([["采集前最小化", "密钥和令牌直接删除"], ["摘要与引用", "订单号散列、原文受控"], ["角色访问", "按租户与职责授权"], ["查看审计", "高敏导出留下记录"], ["到期删除", "索引、缓存与副本联动"]], "展示端打码不能代替采集前删除和存储层授权。")],

  ["submodules/02-offlineeval/assets/offlineeval-harness.png", "Agent 离线评测的运行原理", "原理示意图", "OpenAI evaluation best practices；AgentBench；GAIA；教学改绘", () => flow([["版本化题集", "输入、风险、合格条件"], ["固定环境", "知识、工具、时间、权限"], ["运行候选版本", "保存答案与完整轨迹"], ["多类评分器", "规则、执行、模型、人工"], ["分层报告", "切片、门槛、不确定性"]], "题目与考场同时固定，版本比较才有意义。")],
  ["submodules/02-offlineeval/assets/offlineeval-dataset.png", "评测集由四类样本共同组成", "数据集图", "任务特定评测集设计", () => tree(["版本化评测集", "每题含环境与验收标准"], [["真实流量", "保持主要分布"], ["边界长尾", "缺值、冲突、复杂组合"], ["历史事故", "防止已知故障复发"], ["安全对抗", "注入、越权、泄露"], ["保留测试", "检查未知样本泛化"]], "历史答案要由领域人员校验，不能天然当金标准。")],
  ["submodules/02-offlineeval/assets/offlineeval-graders.png", "不同评分器各管一类问题", "评分器图", "OpenAI graders；LLM-as-a-judge 研究", () => lanes(["规则检查", "环境执行", "模型裁判", "人工复核", "业务结果"], [["适合", "格式数值", "工具与状态", "开放文本", "高风险分歧", "最终真值"], ["优点", "稳定便宜", "贴近任务", "覆盖规模", "专业判断", "真实影响"], ["风险", "忽略语义", "环境成本", "偏差与注入", "慢且昂贵", "结果延迟"], ["用法", "能规则先规则", "动作必须执行", "人工校准", "抽样和争议", "成熟后回填"]], "一个总分不能替代各评分器的证据与边界。")],
  ["submodules/02-offlineeval/assets/offlineeval-slices.png", "总分上涨仍可能掩盖关键退化", "切片图", "示例数据；非真实生产统计", () => lanes(["旧版", "新版", "变化", "结论"], [["总体成功", "78%", "81%", "+3", "看似改善"], ["普通退换", "80%", "86%", "+6", "明显改善"], ["优惠订单", "72%", "55%", "-17", "严重退化"], ["错误写入", "0 次", "2 次", "+2", "停止发布"]], "示例：先看安全与关键切片，再看整体平均。")],
  ["submodules/02-offlineeval/assets/offlineeval-release-gate.png", "离线评测只发放线上验证资格", "门槛图", "持续评测与受控发布流程", () => flow([["硬门槛", "越权、泄露、错误写入"], ["回归门槛", "已知关键能力不退化"], ["目标收益", "目标切片达到改善"], ["稳定性", "重复运行与成本合格"], ["线上资格", "影子或小流量灰度"]], "离线高分不能替代真实流量和外部依赖验证。")],

  ["submodules/03-monitoring/assets/monitoring-signals.png", "Agent 线上监控的四类信号", "原理示意图", "Google SRE 四个黄金信号；结合 Agent 任务与风险改绘", () => table("普通服务信号 + Agent 特有信号", [["业务结果", "任务完成、重开、返工、最终业务状态"], ["执行过程", "工具、重试、循环、交接、护栏"], ["资源健康", "流量、延迟、错误、饱和、token 与费用"], ["安全风险", "越权、错误写入、敏感数据、审批"], ["关联诊断", "按任务、版本和依赖切片，并可跳转 Trace"]], "HTTP 200 只说明系统回了话，不说明任务办成。")],
  ["submodules/03-monitoring/assets/monitoring-slices.png", "平均值、分位数与切片各回答什么", "分布图", "Google SRE 延迟与分位数原则", () => compare({title:"整体聚合",items:[["平均值","看总体但易被稀释"],["P95 / P99","看长尾是否扩大"],["成功与失败","延迟应分别统计"]]},{title:"业务切片",items:[["任务类型","退款与物流分开"],["版本与依赖","定位局部退化"],["语言与租户","看谁受到影响"]]},"高基数身份不要放进指标标签，具体个案用 Trace 查询。")],
  ["submodules/03-monitoring/assets/monitoring-alert.png", "告警要直接指向影响与行动", "告警图", "Google SRE 高信噪比告警原则", () => flow([["检测异常", "阈值、变化率、SLO"], ["确认影响", "哪些任务与用户"], ["关联上下文", "版本、依赖、代表 Trace"], ["选择处置", "降级、熔断、回滚"], ["验证恢复", "业务与技术指标回稳"]], "只是‘曲线有点怪’不应自动叫醒人。")],
  ["submodules/03-monitoring/assets/monitoring-degrade.png", "不同故障需要不同降级路径", "处置图", "Agent 生产故障处置；教学简化", () => lanes(["限流", "缓存", "只读", "人工接管", "回滚"], [["模型拥塞", "适合", "部分", "适合", "可用", "看版本"], ["检索失效", "有限", "可信快照", "待确认", "适合", "可用"], ["写入不明", "熔断", "不适合", "必须", "适合", "看回执"], ["护栏异常", "暂停", "不适合", "必须", "适合", "立即"]], "降级要明确能力变弱，不能用模型记忆冒充最新权威资料。")],
  ["submodules/03-monitoring/assets/monitoring-slo.png", "SLI、SLO 与错误预算怎样连接决策", "可靠性图", "Google SRE SLI/SLO/error budget；结合 Agent 任务成功", () => flow([["定义 SLI", "十秒内正确完成或升级"], ["设定 SLO", "按业务风险定目标"], ["计算错误预算", "允许未达标空间"], ["观察消耗", "按版本与任务切片"], ["约束发布", "暂停、修复或继续"]], "安全事件单独设硬门槛，不与普通可用性共享宽松预算。")],

  ["submodules/04-release/assets/release-experiment.png", "随机对照实验怎样建立因果证据", "原理示意图", "Kohavi et al., Online Experimentation at Microsoft；教学改绘", () => flow([["合格流量", "明确纳入与排除条件"], ["随机分流", "按用户、会话或租户"], ["A：基线版本", "固定其他关键组件"], ["B：候选版本", "只改变目标变量"], ["比较结果", "主要指标 + 护栏 + 区间"]], "随机化减少混杂；样本、干扰和观察窗口仍需检查。")],
  ["submodules/04-release/assets/release-version-bundle.png", "Agent 版本是一个组合包", "版本图", "Agent 版本清单与可复现运行", () => tree(["发布版本 2026.09.29", "写入每次 Trace 的组合标识"], [["模型与参数", "模型、采样、路由"], ["提示与规则", "模板、政策、护栏"], ["知识与索引", "文档、嵌入、重排"], ["工具与流程", "schema、代码、状态图"], ["评测与开关", "题集、评分器、特性开关"]], "只记录模型名，无法复现一次 Agent 运行。")],
  ["submodules/04-release/assets/release-rollout.png", "不同发布阶段解决不同问题", "发布阶梯", "离线、影子、灰度与在线实验", () => flow([["离线回归", "可重复比较"], ["影子流量", "不影响用户看行为"], ["灰度发布", "限制真实影响范围"], ["随机 A/B", "验证业务因果"], ["分阶段全量", "持续监控可回滚"]], "影子看表现，灰度控风险，A/B 问因果。")],
  ["submodules/04-release/assets/release-guardrails.png", "实验指标分层与停止条件", "护栏图", "在线实验与 Agent 安全发布", () => table("实验前写清，不在结果出来后改口径", [["主要指标", "活动政策引用正确与任务完成"], ["质量护栏", "人工重开、无依据承诺、关键切片"], ["资源护栏", "P95 延迟、单任务费用、调用次数"], ["安全硬门槛", "越权、泄露、错误退款立即停止"], ["停止规则", "触发人、切流方式、稳定目标版本"]], "收益不能抵消安全失败。")],
  ["submodules/04-release/assets/release-rollback.png", "真正的回滚不只切换代码", "回滚图", "生产发布与状态迁移实践", () => flow([["停止扩大", "冻结高风险新动作"], ["切回稳定版本", "流量、模型、索引"], ["处理状态", "在途任务与 schema"], ["核对副作用", "缓存、写入、补偿"], ["验证恢复", "业务、技术与安全指标"]], "回滚路径必须预演；不可逆动作只能补偿或人工处理。")],

  ["submodules/05-feedback/assets/feedback-loop.png", "反馈怎样进入可验证改进闭环", "原理示意图", "OpenAI continuous evals；NIST AI RMF Measure/Manage；教学改绘", () => cycle([["收集信号", "评分、改稿、业务结果"], ["关联轨迹", "任务、Trace、版本"], ["归因复核", "找到故障层与证据"], ["形成样本", "去敏、验真、版本化"], ["评测与实验", "离线回归、灰度、回滚"]], ["持续改进", "不是自动训练"], "反馈先变问题，问题再变样本，样本通过实验才进入发布。")],
  ["submodules/05-feedback/assets/feedback-signals.png", "三类反馈信号不能混成一个分数", "信号图", "用户反馈、行为反馈与业务结果", () => table("同一个动作可能有不同含义", [["显式反馈", "点赞、差评、原因选择、文字意见"], ["人工纠正", "字段改稿、审批修改、专业复核"], ["行为信号", "重试、追问、放弃、转人工、复制"], ["业务结果", "申请成功、撤销、重开、再次联系"], ["关联信息", "任务、版本、Trace、时间与必要上下文"]], "点赞不等于正确，沉默也不等于成功。")],
  ["submodules/05-feedback/assets/feedback-attribution.png", "表面差评要定位到可修复层", "归因图", "Agent 失败分类与反馈归因", () => tree(["人工修改：退款 129 → 实付 109", "先核对证据和订单字段"], [["数据输入", "优惠拆分缺失"], ["检索知识", "退款规则未进入"], ["模型使用", "选错金额字段"], ["工具流程", "schema 或校验缺失"], ["产品界面", "关键差异未展示"]], "不要把所有事实错误都装进‘提示词不好’。")],
  ["submodules/05-feedback/assets/feedback-sample.png", "一条反馈怎样成为高质量评测样本", "样本加工", "持续评测数据治理", () => flow([["原始反馈", "改稿、原因、业务结果"], ["去敏去重", "移除无关身份与重复"], ["领域验真", "确认政策、事实、正确结果"], ["结构化样本", "环境、必须、禁止、风险"], ["分集入库", "开发、回归、保留测试"]], "用于优化的样本不能继续冒充独立测试。")],
  ["submodules/05-feedback/assets/feedback-prioritization.png", "反馈问题按频率与严重度排序", "优先级图", "风险优先级与持续改进", () => lanes(["低频", "中频", "高频", "处理原则"], [["低影响", "观察", "排期", "批量优化", "体验改进"], ["中影响", "复现", "优先处理", "专项修复", "业务损失"], ["高影响", "立即调查", "立即停止", "立即停止", "安全与资金"], ["证据", "补 Trace", "建立样本", "统计切片", "都需验证"]], "低频高风险不应被高频文风问题挤到后面。")],
];

const requested = new Set(process.argv.slice(2));
const tempRoot = await mkdtemp(path.join(tmpdir(), "evaluation-figures-"));
for (const [file, title, eyebrow, source, draw] of D) {
  if (requested.size && !requested.has(file)) continue;
  const output = path.join(outRoot, file);
  await mkdir(path.dirname(output), { recursive: true });
  const svgFile = path.join(tempRoot, file.replaceAll("/", "-").replace(/\.png$/, ".svg"));
  await writeFile(svgFile, canvas(title, eyebrow, draw(), source));
  await execFile("sips", ["-s", "format", "png", svgFile, "--out", output]);
  console.log(path.relative(root, output));
}
await rm(tempRoot, { recursive: true, force: true });
