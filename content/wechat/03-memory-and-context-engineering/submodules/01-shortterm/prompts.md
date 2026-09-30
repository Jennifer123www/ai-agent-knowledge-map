# 短期状态配图说明

- 版本：`0.1.0`；阶段：短期状态配图已绘制；Git 基线：`7378a4f`（`main`；绘制前 clean）；修改时间：`2026-09-28 CST`。
- 渲染：`scripts/render-memory-context-figures.py`；1536×1024 PNG，中文逐字校对；不用生成图代替状态与箭头的准确性。
- `shortterm-cover.png`：票据识别、等待校验、恢复任务三卡，说明任务停在哪一步。
- `shortterm-state.png`：任务标识、当前节点、关键输出、动作状态四个并列字段。
- `shortterm-checkpoint.png`：执行、结果校验、保存状态、继续任务；箭头只表示顺序。
- `shortterm-replay.png`：安全重放与危险重做的并列对照，不把草稿等同提交。
- `shortterm-test.png`：识别前、识别后、调用后、完成后四个故障注入点。
- `shortterm-principle.png`：系统指令、工作区、滚动消息队列位于有限窗口内；窗口之外另有可取回的记录。图内不把任务检查点冒充论文原结构。

## 原理图来源与改绘边界

- 原论文：[MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)，Figure 3、§2.1–2.2。
- 保留：固定容量窗口内的系统指令、可写工作区、滚动队列；旧消息迁至外部记录后，取回需要显式调用。
- 简化：省略队列阈值和函数执行器。任务状态的检查点、恢复粒度与幂等重放是本文讨论的工程机制，不是 Figure 3 的原始结论；主文另用检查点图说明。
- 图注：依据 MemGPT Figure 3；任务检查点是另加的工程持久化机制。
