# 记忆类型与用户画像配图说明

- 版本：`0.1.0`；阶段：类型配图已绘制；Git 基线：`7378a4f`（`main`；绘制前 clean）；修改时间：`2026-09-28 CST`。
- 渲染：`scripts/render-memory-context-figures.py`；1536×1024 PNG；文字和分类边界逐项核对。
- `memorytypes-cover.png`：任务、经历、偏好三种提问并列。
- `memorytypes-taxonomy.png`：工作、情景、语义记忆与用户画像四类并列；不画成互相排斥的数据库表。
- `memorytypes-profile.png`：一次经历与受控画像对照。
- `memorytypes-routing.png`：候选信息经用途、来源判断，再决定去向。
- `memorytypes-test.png`：临时城市、退单经历、制度上限、语言偏好四个反例。
- `memorytypes-principle.png`：观察记录与高层反思作为不同来源，进入记忆流并按当前情境检索。画像分类在图注标明是教学延伸。

## 原理图来源与改绘边界

- 原论文：[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)，Figure 5–6 与 §4.1–4.2。
- 保留：观察、反思、记忆流、检索、行动之间的依赖与方向；当前输入只取相关子集，不搬入全部经历。
- 简化和区分：论文并未定义本文的“工作／情景／语义／用户画像”四格分类，也未给出企业画像授权规则；分类借助 [LangMem 概念说明](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/) 作为工程教学框架。
- 图注：依据 Generative Agents Figure 5；记忆类型与画像分类为教学延伸。
