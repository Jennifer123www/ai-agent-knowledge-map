# 版本、实验与发布：配图提示词

## 文档元数据

- 版本：`0.1.0`
- 阶段：第七模块公众号推文初稿
- Git 状态：基线 `6c272f0`（`main`；第七模块文件未提交，另有 Word 临时锁文件未跟踪）
- 修改时间：`2026-09-29 20:04 CST`

## 封面

无文字编辑插画底图：暖白实验台，新旧两条路径经过版本包、影子、灰度、A/B 和回滚开关；青绿主色、橙色风险强调。确定性叠字分别为“版本、实验与发布 / 变好不能只凭感觉”和“版本发布面试题 / Agent 怎样灰度与回滚”。禁止营销火箭、机器人、乱码、水印。

## 正文图

1. `release-experiment.png`：候选版本经随机分流形成 A/B 两组，比较主要指标与护栏指标，再作发布决策。依据 [Online Experimentation at Microsoft](https://www.microsoft.com/en-us/research/publication/online-experimentation-at-microsoft/)的随机对照思想重绘；保留随机分流、对照、结果比较，不复刻论文图。
2. `release-version-bundle.png`：模型、提示、知识索引、工具、规则、流程和评测器组成版本包。
3. `release-rollout.png`：离线 → 影子 → 灰度 → A/B → 分阶段全量。
4. `release-guardrails.png`：主要指标、质量护栏、安全硬门槛与停止条件。
5. `release-rollback.png`：切流、状态、缓存、索引、在途任务和业务补偿的回滚清单。

统一要求：`1536 × 1024`，中文准确，箭头只表示真实控制关系，示例指标标明“示例”，无水印。
