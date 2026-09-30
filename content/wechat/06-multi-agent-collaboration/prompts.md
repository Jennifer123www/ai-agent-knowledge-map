# 多智能体协作总览配图提示词

版本：0.1.1；修订时间：2026-09-29 20:20 CST；依据提交：`ee5f838`（`main`；修订时本系列尚未提交，另有 Word 临时锁文件未跟踪）。

正文配图为 1536×1024 PNG；公众号封面图为 900×383 PNG。统一使用暖白纸张背景、深灰文字、梅红主强调、青绿与橙色辅助。封面由内置图像生成工具生成；正文图由 `scripts/render-multi-agent-figures.mjs` 确定性绘制，确保中文、箭头和案例字段准确。无水印、无 Logo、无密集小字。

1. `orchestration-cover-main-wechat.png`：主文封面。标题“大话多智能体协作”“三支小队怎样合成一份报告”；市场、技术、财务三路调研汇入带引用的供应商选型报告。
2. `orchestration-cover-interview-wechat.png`：面试副文封面。标题“面试题：多智能体怎样分工而不变成群聊”；展示三名专家、任务契约和验收清单。
3. `orchestration-choice.png`：比较“单 Agent”“固定工作流”“多智能体”，分别标出任务短且耦合高、路径稳定、子任务可独立验收三类条件。
4. `orchestration-task-contract.png`：任务契约字段：目标、输入、交付格式、证据、权限、预算、停止条件。
5. `orchestration-patterns.png`：顺序、并行、主管—专家、交接四种协作拓扑及控制权位置。
6. `orchestration-failure-budget.png`：错误传播与预算闸门；专家结论必须带证据，经验证后才进入总报告，并限制委派深度、并发和总调用量。
7. `orchestration-principle.png`：依据 Anthropic《Building Effective AI Agents》的“orchestrator-workers”与 OpenAI Agents SDK orchestration 文档改绘。保留“总任务 → 编排器动态拆分 → 多个专门执行者 → 结构化结果 → 编排器综合与验收”，并明确代码编排与模型编排可以混合。图注：“依据 Anthropic orchestrator-workers 模式及 OpenAI Agents SDK orchestration 文档改绘。”

复核要求：封面标题逐字检查；正文图确认控制权、证据方向、预算闸门和单 Agent 基线。正文不重复插入封面。
