# 线上监控：配图提示词

## 文档元数据

- 版本：`0.1.0`
- 阶段：第七模块公众号推文初稿
- Git 状态：基线 `6c272f0`（`main`；第七模块文件未提交，另有 Word 临时锁文件未跟踪）
- 修改时间：`2026-09-29 20:04 CST`

## 封面

无文字编辑插画底图：暖白运行控制台，表面绿色成功灯下方出现长尾延迟和用户重开信号，突出“技术成功但业务失败”；青绿、深蓝、橙色。确定性叠字分别为“线上监控 / 系统没报错为何用户仍不满”和“线上监控面试题 / Agent 线上监控看什么”。无机器人、乱码、水印。

## 正文图

1. `monitoring-signals.png`：在 Google SRE 延迟、流量、错误、饱和基础上，增加 Agent 的任务结果、执行过程与风险信号。依据 [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)改绘；明确哪些是传统服务信号，哪些是 Agent 补充信号。
2. `monitoring-slices.png`：平均值、P95/P99 和任务切片的关系。
3. `monitoring-alert.png`：异常 → 影响范围 → 版本与 Trace → 处置责任人。
4. `monitoring-degrade.png`：限流、缓存、只读、人工接管、回滚五条受控路径。
5. `monitoring-slo.png`：SLI → SLO → 错误预算 → 发布/修复决策。

统一要求：`1536 × 1024`，暖白底，图表不伪造真实观测值，示例数字标明“示例”，无水印。
