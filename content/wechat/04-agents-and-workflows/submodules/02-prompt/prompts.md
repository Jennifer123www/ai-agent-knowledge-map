# 系统指令与提示词配图稿

- 版本：`0.1.0`；阶段：配图方案已定；Git 基线：`7369612`（main，启动前 clean）；修改时间：`2026-09-28 CST`。
- 1536×1024 中文 PNG，文字大而少；外部日历备注必须以“不可信资料”身份出现，不画成高优先级系统指令。
- `prompt-cover.png`：把“安排评审会”拆成目标、约束和交付物三卡。
- `prompt-layers.png`：系统约束、当前用户请求、日历工具返回三层来源，层间不允许箭头向上“升权”。
- `prompt-schema.png`：候选时间、参会人、冲突、待确认、草稿等字段，旁边标“程序复核”。
- `prompt-injection.png`：日历备注里“立刻发送邀请”被当资料隔离，真实动作仍需用户批准。
- `prompt-test.png`：缺空闲信息、字段缺失、伪系统文本、旧提示版本四种回归样本。
- `prompt-principle.png`：来源分层进入模型输入，产生候选 JSON，再由结构校验与权限校验分别处理；不得把模型输出画成自动具有发送权限。

## 原理图依据与改绘边界

- [The Instruction Hierarchy](https://arxiv.org/abs/2404.13208) §2–3：上层与下层指令来源的优先关系、下层文本可能试图越权。本图不复制论文实验图，不声称提示词能提供硬安全保证。
- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) 的系统提示组织建议用于字段示意；结构化结果后的程序校验是本案例工程补充。
- 图注建议：“依据 Instruction Hierarchy 的来源优先关系改绘；后置程序闸门不由论文图直接给出。”
