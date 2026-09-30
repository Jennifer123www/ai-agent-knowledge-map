# 智能体与工作流：总览配图稿

- 版本：`0.1.0`；阶段：配图方案已定；Git 基线：`7369612`（main，启动前 clean）；修改时间：`2026-09-28 CST`。
- 图片用于公众号总览双文，均为 1536×1024 PNG。用暖白底、梅紫与青绿强调，准确中文、大字、少量箭头；不使用脑袋、电路、伪 3D、无出处数字或水印。准确标签优先于写实装饰。
- `overview-cover.png`：标题“智能体与工作流”；三块写“先核对约束／再查空闲／最后交付草稿”；角注“未经确认，不发送邀请”。
- `overview-map.png`：七环节关系图。上方角色与指令给边界，中间证据、计划、路由给选择，底部反思与循环接收工具结果；不要画成七个彼此独立的机器人。
- `overview-workflow-agent.png`：并排比较固定工作流的预设路径与智能体依观察选择下一步；两侧都保留程序权限闸门。
- `overview-handoff.png`：会议案例的跨环节交接；每个节点只写交付物，不写抽象“赋能”。
- `overview-test.png`：正常、缺一团队空闲、会议室冲突、用户未批准发送四类端到端测试。
- `overview-principle.png`：ReAct 式“判断当前缺口 → 查询环境 → 观察返回 → 更新下一步”，另接“完成／停止／请人确认”出口。

## 原理图依据与改绘边界

- 原始研究：[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)，Figure 1(1d)、§2。保留动作与环境观察交错、观察改变后续判断的关系；不公开或声称复刻模型内部思维链。
- 工作流与智能体的区别参照 [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) 的 “Workflows vs. agents” 与 “Agents” 图。会议室查询、用户审批和停止条件是本案例的工程扩展，并非 ReAct 原图组件。
- 图注建议：“依据 ReAct Figure 1 的行动—观察结构改绘；权限与停止出口为会议助手的工程边界。”
