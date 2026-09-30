# 智能体执行循环配图稿

- 版本：`0.1.0`；阶段：配图方案已定；Git 基线：`7369612`（main，启动前 clean）；修改时间：`2026-09-28 CST`。
- 1536×1024 中文 PNG；箭头要区分“本轮继续”“等待用户”“终止”，不得画成无条件无限循环。
- `loop-cover.png`：读状态、选动作、执行与观察三卡，结尾标“完成／暂停／失败”。
- `loop-state.png`：会议目标、当前候选、工具结果、重试次数四项状态。
- `loop-transition.png`：观察到空闲、冲突或超时分别进入不同状态。
- `loop-stop.png`：完成草稿、等待确认、预算用尽、工具异常四种终态。
- `loop-test.png`：正常、工具失败、重复回调、用户中断四种轨迹测试。
- `loop-principle.png`：依据 ReAct Figure 1(1d) 的动作—观察反复交替，加一个显式状态寄存与停止判断；“思考”不画成对外可读的内部思维链。

## 原理图依据与改绘边界

- [ReAct](https://arxiv.org/abs/2210.03629) Figure 1(1d)、§2–3：保留外部行动、观察和更新下一步选择的循环关系。
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) 的 “Agents” 图用于核对循环、环境反馈和停止条件。持久化状态、幂等重试及人工暂停是工程实现的附加部分。
- 图注建议：“依据 ReAct Figure 1 的行动—观察交替改绘；状态、预算和暂停是工程约束。”
