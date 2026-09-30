# 评测、可观测性与持续优化：配图提示词

## 文档元数据

- 版本：`0.1.0`
- 阶段：第七模块公众号推文初稿
- Git 状态：基线 `6c272f0`（`main`；第七模块文件未提交，另有 Word 临时锁文件未跟踪）
- 修改时间：`2026-09-29 20:04 CST`

## 封面

两张封面先由 imagegen 生成无文字编辑插画底图，再以确定性排版叠加中文，最终裁切为 `900 × 383` PNG。

- 主文：暖白技术杂志风，青绿、深蓝与少量橙色；中心是由轨迹线、评分卡、监控曲线和版本标签组成的证据控制台。文字必须为“评测、可观测性与持续优化”“智能体到底把事情办成了吗”。
- 面试：同一视觉语言，重点换成检查清单与证据闸门。文字必须为“评测、可观测性与持续优化”“怎样证明智能体真的可靠”。
- 禁止：机器人头像、抽象大脑、霓虹科技感、英文乱码、水印和无关装饰。

## 正文图

1. `evaluation-loop.png`：Trace → 离线评测 → 受控发布 → 线上监控 → 反馈回流的闭环，中间标“可验证任务成功”。依据 [OpenTelemetry Observability primer](https://opentelemetry.io/docs/concepts/observability-primer/) 与 [OpenAI Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) 重绘。保留单次轨迹、多次评测、线上反馈三种尺度；不照搬产品界面。
2. `evaluation-metric-layers.png`：结果、过程、风险、资源四层，不合并成总分。
3. `evaluation-failure-attribution.png`：用户投诉反向追到检索、模型、工具和状态版本。
4. `evaluation-evidence-gate.png`：硬安全门槛、关键能力、质量收益、成本时延四道发布关口。
5. `evaluation-baseline.png`：规则方案、单次调用、旧 Agent、新 Agent 同台比较。

统一要求：`1536 × 1024`，暖白底，中文大字号，青绿主色、橙色强调，箭头有方向，图中文字逐字校对，无水印。
