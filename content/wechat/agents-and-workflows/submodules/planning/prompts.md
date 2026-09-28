# 任务规划配图稿

- 版本：`0.1.0`；阶段：配图方案已定；Git 基线：`7369612`（main，启动前 clean）；修改时间：`2026-09-28 CST`。
- 1536×1024 中文 PNG；依赖箭头方向写清先后，不把实际业务动作与论文中的“thought”节点混为一个概念。
- `planning-cover.png`：会议目标分成收集约束、查空闲、查会议室、比较候选、草拟通知。
- `planning-dependency.png`：团队空闲可并行查，房间核验依赖候选时段，草稿依赖已核对结果。
- `planning-critical.png`：标出少一个团队空闲就无法确认最终时段的关键依赖。
- `planning-replan.png`：房间被占后只重排相关候选，不从头重复所有查询。
- `planning-test.png`：正常、依赖缺失、结果变化、预算耗尽四类规划样本。
- `planning-principle.png`：依据 ToT Figure 1 的“候选分支 → 评价 → 保留／回退”机制，改成会议候选时间的教学树；节点只代表备选方案，不声称复刻论文的具体任务与得分。

## 原理图依据与改绘边界

- [Tree of Thoughts](https://arxiv.org/abs/2305.10601) Figure 1、§3：保留生成候选、评价候选、搜索与回退的结构；该论文中的“thought”是中间语言步骤，本图把搜索思想应用于会议方案，不将业务任务图误称原论文原图。
- 依赖图另参照 [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) 的 “Orchestrator-workers” 与 “Prompt chaining” 工程模式。
- 图注建议：“依据 ToT Figure 1 的分支搜索思想改绘；会议依赖与权限为本案例应用。”
