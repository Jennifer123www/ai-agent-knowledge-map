# 反思与纠错配图稿

- 版本：`0.1.0`；阶段：配图方案已定；Git 基线：`7369612`（main，启动前 clean）；修改时间：`2026-09-28 CST`。
- 1536×1024 中文 PNG；必须画出真实反馈进入下一次尝试，不把“模型自己说我做得很好”画成验证。
- `reflection-cover.png`：会议室占用后，读失败原因、改候选时段、再查一次。
- `reflection-feedback.png`：工具错误、规则校验、用户更正三种反馈来源。
- `reflection-diagnose.png`：区分房间被占、查询超时、日期解析错三种故障。
- `reflection-retry.png`：前后两次请求显示改变了哪个字段，不画原样重试。
- `reflection-test.png`：正向修正、错误反馈、连续失败、无收益重试四类测试。
- `reflection-principle.png`：按 Reflexion Figure 2(a) 绘出 Actor（执行者）→ Evaluator（评价器）→ Self-reflection（反思摘要）→下一次尝试的关系，长期经验存储只作可选分支。

## 原理图依据与改绘边界

- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) Figure 2(a)、§3。保留行动轨迹被评价、反馈写成语言经验影响下一轮的方向；论文使用的评价器并非所有场景都可信，会议助手需优先依赖实际房间返回与用户更正。
- 次数限制和“交还用户”出口是工程边界，图注应写明不是原论文 Figure 2 的原样复制。
- 图注建议：“依据 Reflexion Figure 2(a) 改绘；本例以会议室返回作外部反馈，并加停止上限。”
