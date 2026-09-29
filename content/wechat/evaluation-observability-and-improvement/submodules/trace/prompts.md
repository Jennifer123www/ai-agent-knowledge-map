# 链路追踪：配图提示词

## 文档元数据

- 版本：`0.1.0`
- 阶段：第七模块公众号推文初稿
- Git 状态：基线 `6c272f0`（`main`；第七模块文件未提交，另有 Word 临时锁文件未跟踪）
- 修改时间：`2026-09-29 20:04 CST`

## 封面

无文字编辑插画底图：暖白画布，一条售后任务轨迹从用户请求分叉到订单、检索、模型、工具再汇合，像严谨的案件时间线；青绿、深蓝与橙色。确定性叠字分别为“链路追踪 / 一句错答从哪里开始”和“链路追踪面试题 / 一条 Trace 应记录什么”。禁止大脑、机器人、乱码、水印。

## 正文图

1. `trace-tree.png`：一个 Trace 下的工作流、检索、工具和模型 Span 父子树，并在下方画时间轴。依据 [OpenTelemetry Trace semantic conventions](https://opentelemetry.io/docs/specs/semconv/general/trace/)和 [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)改绘；保留 Trace、Span、父子关系、开始结束时间，不照搬仪表盘。
2. `trace-span-fields.png`：模型、检索、工具、状态四类 Span 的必要字段卡。
3. `trace-diagnosis.png`：投诉 → 锁定 Trace → 比较证据与版本 → 根因假设 → 回归验证。
4. `trace-sampling.png`：随机样本、错误与慢请求、高风险写入三档采样。
5. `trace-privacy.png`：采集前删除密钥，摘要/哈希，受控原文，访问审计与到期删除。

统一要求：`1536 × 1024`，暖白底、青绿主色、橙色异常，字段真实，箭头清楚，无水印。
