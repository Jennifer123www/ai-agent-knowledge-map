# 长期记忆配图说明

- 版本：`0.1.0`；阶段：长期记忆配图已绘制；Git 基线：`7378a4f`（`main`；绘制前 clean）；修改时间：`2026-09-28 CST`。
- 渲染：`scripts/render-memory-context-figures.py`；1536×1024 PNG；中文标签、箭头和来源人工复核。
- `longterm-cover.png`：候选偏好、受控保存、下次取回。
- `longterm-vs-history.png`：原始聊天历史与经过筛选的记忆并列。
- `longterm-retrieval.png`：当前任务触发检索、冲突过滤、必要信息进入上下文。
- `longterm-conflict.png`：过去中文偏好与本轮英文要求并列，临时例外不等于永久改写。
- `longterm-test.png`：适用、冲突、误记、隔离四类专项样本。
- `longterm-principle.png`：观察进入记忆流，按当前情境检索后支持行动；反思可回写更高层认识。

## 原理图来源与改绘边界

- 原论文：[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)，Figure 5 与 §4.1–4.2。
- 保留：观察、记忆流、检索、行动、反思及反思回写的方向。不能把反思直接画成已核实的用户偏好。
- 简化：不复刻论文的小镇模拟情境与具体打分权重。企业记忆的用户确认、权限、保留期和删除是工程补充。
- 图注：依据 Generative Agents Figure 5 改绘；企业偏好写入还需另设门槛。
