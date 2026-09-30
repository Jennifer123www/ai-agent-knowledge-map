# 离线评测：配图提示词

## 文档元数据

- 版本：`0.1.0`
- 阶段：第七模块公众号推文初稿
- Git 状态：基线 `6c272f0`（`main`；第七模块文件未提交，另有 Word 临时锁文件未跟踪）
- 修改时间：`2026-09-29 20:04 CST`

## 封面

无文字编辑插画底图：暖白模拟考场，新旧两条 Agent 轨迹经过同一组工单、同一沙盒和评分卡；青绿、深蓝、橙色。确定性叠字分别为“离线评测 / 先在模拟考场里见真章”和“离线评测面试题 / 怎样避免虚高”。禁止试卷卡通、机器人、英文乱码、水印。

## 正文图

1. `offlineeval-harness.png`：版本化题集与环境快照同时输入旧版和新版，经过规则、执行、模型和人工评分后生成分层报告。依据 [OpenAI Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)、[AgentBench](https://arxiv.org/abs/2308.03688)和 [GAIA](https://arxiv.org/abs/2311.12983)的环境评测原则重绘；保留任务、环境、轨迹与评分器，不复制论文截图。
2. `offlineeval-dataset.png`：真实流量、边界长尾、历史事故、安全对抗四类样本。
3. `offlineeval-graders.png`：规则、环境执行、LLM 裁判、人工复核的责任边界。
4. `offlineeval-slices.png`：总分上升但优惠订单和高风险退款退化的切片对比。
5. `offlineeval-release-gate.png`：硬门槛、关键能力、目标收益、影子/灰度资格。

统一要求：`1536 × 1024`，中文准确，所有示例数值明确标“示例”，不使用不可读小字，无水印。
