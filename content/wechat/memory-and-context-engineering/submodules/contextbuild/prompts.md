# 上下文构造配图说明

- 版本：`0.1.0`；阶段：上下文配图已绘制；Git 基线：`7378a4f`（`main`；绘制前 clean）；修改时间：`2026-09-28 CST`。
- 渲染：`scripts/render-memory-context-figures.py`；1536×1024 PNG；文本、指标和数据边界人工复核。
- `contextbuild-cover.png`：先筛、再排、后核三卡。
- `contextbuild-selection.png`：候选材料经过权限时效硬过滤，再排序构造。
- `contextbuild-budget.png`：硬约束、当前状态、证据、输出余量并列；不写固定比例。
- `contextbuild-injection.png`：网页文字与系统／用户任务并列，不可信内容不可升级为指令。
- `contextbuild-test.png`：旧新冲突、证据居中、恶意注入、缓存过期四类专项测试。
- `contextbuild-principle.png`：横轴为证据位置，纵轴为任务表现；用定性 U 形说明部分模型的中间位置劣势，不填冒充论文的数字。

## 原理图来源与改绘边界

- 原论文：[Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)，Figure 1、Figure 3 与 §2.3。
- 保留：在相同问题与相关证据下移动证据位置，任务表现可能在开头／结尾较好、中间较弱；这是论文所测模型与任务的现象，不是所有模型的定律。
- 简化：曲线为定性教学示意，**没有实测百分比**；权限过滤、压缩、提示注入与缓存是后续工程策略，不是 Figure 1 的实验结论。
- 图注：依据 Lost in the Middle Figure 1 作定性示意；不是所有模型的实测曲线。
