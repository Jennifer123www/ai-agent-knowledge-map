# 角色与职责设定配图稿

- 版本：`0.1.0`；阶段：配图方案已定；Git 基线：`7369612`（main，启动前 clean）；修改时间：`2026-09-28 CST`。
- 全部为 1536×1024 中文 PNG，沿用系列暖白、梅紫、青绿；避免把“角色”画成漫画人物或把自然语言承诺误画成实际权限。
- `persona-cover.png`：会议助手“可查日历／可草拟通知／不可擅发邀请”三卡。
- `persona-contract.png`：服务对象、输入、交付物、失败交接四栏，填写具体会议案例。
- `persona-boundary.png`：读取、建议、写入、发送四级动作，发送位于用户确认之后。
- `persona-handoff.png`：权限不足、资料缺失、需要发送确认各走不同交接出口。
- `persona-test.png`：四个边界样本：正常草稿、他人日历越权、未经确认发送、时间冲突。
- `persona-principle.png`：候选动作先进入“允许动作集合”过滤，再进工具执行；不在集合内的动作只能拒绝或升级。以实际运行机制解释角色契约并非一句人设。

## 原理图依据与改绘边界

- [ReAct](https://arxiv.org/abs/2210.03629) §2 对环境动作空间与语言内部步骤作区分；本图只借用“候选动作进入环境前存在可执行动作集合”的思想。
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) 的 “Augmented LLM” 强调工具的明确接口。图中权限闸门、用户确认是工程加装，不是论文原图；必须在图注说明。
- 图注建议：“依据 ReAct §2 的环境动作空间改绘；权限与确认闸门是本案例的应用设计。”
