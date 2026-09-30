# 记忆写入与更新配图说明

- 版本：`0.1.0`；阶段：写入更新配图已绘制；Git 基线：`7378a4f`（`main`；绘制前 clean）；修改时间：`2026-09-28 CST`。
- 渲染：`scripts/render-memory-context-figures.py`；1536×1024 PNG；确定性绘制中文、版本线和箭头。
- `memorywrite-cover.png`：新说法、核实意图、更新记录。
- `memorywrite-gate.png`：来源、用途、敏感、范围四道写入门槛。
- `memorywrite-conflict.png`：事件追加与当前值覆盖并列，避免双活动值。
- `memorywrite-version.png`：v1、新请求、v2、迟到事件；版本先后不能被到达顺序替代。
- `memorywrite-test.png`：明确变更、随口提及、消息乱序、撤销请求四类测试。
- `memorywrite-principle.png`：旧值、新消息输入替换操作，当前值指向新称呼；旧值只保留在历史，不再作为有效称呼。

## 原理图来源与改绘边界

- 原论文：[MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)，Figure 4 与 §2.3。论文示例使用 `working_context.replace` 更新工作区里的信息。
- 保留：旧记录、新消息、替换操作、当前值以及替换方向；不要把旧值画成仍然可同时作为当前值读取。
- 简化：把论文中的私人关系变化替换为无敏感内容的称呼变化；企业系统需要的来源校验、版本竞争、授权和审计是工程补充，不能说论文已保证。
- 图注：依据 MemGPT Figure 4 改绘；是否允许替换仍需外部校验。
