# 定时任务与事件触发配图提示词与校验记录

- 版本：0.1.0
- 阶段：第九模块公众号推文初稿
- Git 状态：基于 9b4282c（main；本模块文件尚未提交，另有编辑器临时文件未跟踪）
- 修改时间：2026-09-29 20:38 CST

## 封面

封面底图由图像模型生成无文字编辑插画，再用确定性 SVG 排版叠加中文标题。底图保持暖白纸张、橙色与深青色点缀，右侧用与“定时任务与事件触发”有关的抽象场景，左侧留出标题空间。禁止水印、乱码、伪文字和品牌标识。主文与面试文分别输出 900×383 PNG。

## 原理图：schedule-principle.png

- 用途：解释“定时与事件触发怎样进入可靠执行”。
- 资料来源：
- Kubernetes：CronJob：https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
- CloudEvents Specification：https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
- Kubernetes：Observability：https://kubernetes.io/docs/concepts/cluster-administration/observability/
- 保留节点：时间或事件（Cron、Webhook、对象变更）；触发过滤（租户、类型和条件）；生成业务键（周期、对象与版本）；并发与去重（允许、替换或禁止重叠）；提交任务（进入队列并记录触发原因）。
- 箭头语义：前一步向后一步提供事实、控制或任务状态；不表示所有步骤都同步，也不表示必须使用同一产品。
- 简化项：省略厂商 API、部署拓扑和异常分支，只保留初学者理解核心机制所需节点。
- 生成方式：程序化 SVG 转 PNG，确保中文、箭头和来源文字准确。
- 人工核验：逐项核对节点顺序、中文、箭头和来源；不得用生成式图片替代机制推理。

## 其他正文图

- schedule-inputs.png：五类输入——时间语义、事件语义、并发策略、补跑策略、业务幂等键。
- schedule-failure.png：三类失效——依赖 Cron 天然只执行一次；忽略时区和夏令时导致错跑；事件风暴为同一对象创建大量任务。
- schedule-controls.png：控制组合——显式时区和执行窗口、业务键去重与幂等、重叠、补跑和过期策略、触发记录、积压监控和手工补偿。
- schedule-verification.png：验证闭环与指标——漏触发与重复触发数、调度延迟、重叠任务占比、事件到任务的去重率。

所有正文图为 1536×1024 PNG，必须包含准确中文；颜色用于分组，不替代文字语义。正文图不兼作封面，封面不计入每篇至少五张正文图。
