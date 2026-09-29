# 主管调度与 Agent 通信子模块配图提示词

版本：0.1.1；修订时间：2026-09-29 20:20 CST；依据提交：`ee5f838`（`main`；修订时本系列尚未提交，另有 Word 临时锁文件未跟踪）。

正文图 1536×1024，封面 900×383；暖白底、深灰文字、梅红主管、青绿/橙色专家。封面使用内置图像生成工具，正文由确定性脚本绘制。

1. `supervisor-cover-main-wechat.png`：标题“大话主管调度”“组长不能只会转发消息”；主管分派市场、技术、财务任务并验收证据。
2. `supervisor-cover-interview-wechat.png`：标题“面试题：Supervisor 怎样委派”“又不陷入循环”；突出任务契约、预算和停止条件。
3. `supervisor-contract.png`：主管发出的子任务含目标、输入、证据、输出模式、权限、期限。
4. `supervisor-routing.png`：按任务类型和权限选择专家；无匹配、超预算或高风险时升级。
5. `supervisor-conflict.png`：两个专家结论冲突，主管要求补证或交给独立验证者，不直接投票。
6. `supervisor-budget.png`：最大深度、最大并发、调用预算、超时和重复任务指纹。
7. `supervisor-principle.png`：依据 Anthropic orchestrator-workers 模式与 OpenAI Agents SDK manager pattern 改绘。保留“主管保留最终控制 → 专家作为受限执行者 → 结构化结果 → 验收/补问/停止”，并与 handoff 的控制权转移区分。图注：“依据 Anthropic orchestrator-workers 与 OpenAI manager pattern 改绘。”

复核：主管必须有验收和停止节点；专家不能直接共享生产写权限。
