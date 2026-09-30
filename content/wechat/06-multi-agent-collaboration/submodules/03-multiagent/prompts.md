# 多智能体系统子模块配图提示词

版本：0.1.1；修订时间：2026-09-29 20:20 CST；依据提交：`ee5f838`（`main`；修订时本系列尚未提交，另有 Word 临时锁文件未跟踪）。

正文图 1536×1024，封面 900×383；暖白底、深灰文字、梅红/青绿/橙色区分角色。封面使用内置图像生成工具，正文由确定性脚本绘制。

1. `multiagent-cover-main-wechat.png`：标题“大话多智能体”“三个人一起做就一定更好吗”；市场、技术、财务三名专家各交一份带证据的报告。
2. `multiagent-cover-interview-wechat.png`：标题“面试题：多 Agent 何时值得用”；展示质量收益与协调成本的天平。
3. `multiagent-fit.png`：适合与不适合多 Agent 的任务条件对照。
4. `multiagent-parallel.png`：三路独立调研并行，依赖项顺序执行，最后显式汇合。
5. `multiagent-evidence.png`：每个专家交付结论、证据、假设、未解决项；无证据结论不得进入总报告。
6. `multiagent-evaluation.png`：单 Agent 与多 Agent 对照，比较任务成功、证据覆盖、时延、token、重复工作和人工返工。
7. `multiagent-principle.png`：依据 AutoGen 论文的 conversable agents 与 conversation patterns 改绘，并吸收 Anthropic 并行和 orchestrator-workers 模式。保留“角色配置/工具权限 → 消息或结构化产物 → 交互协议 → 终止条件”，强调多 Agent 收益来自分工和验证，不来自角色数量。图注：“依据 AutoGen 与 Anthropic agent patterns 改绘。”

复核：不得暗示 Agent 数量越多质量越高；所有分支都有交付物和汇合点。
