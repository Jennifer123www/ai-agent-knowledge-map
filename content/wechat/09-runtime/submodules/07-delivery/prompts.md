# 部署、扩缩容与发布配图提示词与校验记录

- 版本：0.1.0
- 阶段：第九模块公众号推文初稿
- Git 状态：基于 9b4282c（main；本模块文件尚未提交，另有编辑器临时文件未跟踪）
- 修改时间：2026-09-29 20:38 CST

## 封面

封面底图由图像模型生成无文字编辑插画，再用确定性 SVG 排版叠加中文标题。底图保持暖白纸张、橙色与深青色点缀，右侧用与“部署、扩缩容与发布”有关的抽象场景，左侧留出标题空间。禁止水印、乱码、伪文字和品牌标识。主文与面试文分别输出 900×383 PNG。

## 原理图：delivery-principle.png

- 用途：解释“从构建到扩缩与回滚的交付闭环”。
- 资料来源：
- Kubernetes：Horizontal Pod Autoscaling：https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
- Kubernetes：Deployments：https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Kubernetes：Observability：https://kubernetes.io/docs/concepts/cluster-administration/observability/
- 保留节点：构建版本（代码、提示、规则、模型与 schema）；部署验证（探针、影子和离线门槛）；受控放量（灰度、流量和任务分组）；容量调节（队列、并发、配额和成本）；回滚与收尾（在途任务、缓存和状态迁移）。
- 箭头语义：前一步向后一步提供事实、控制或任务状态；不表示所有步骤都同步，也不表示必须使用同一产品。
- 简化项：省略厂商 API、部署拓扑和异常分支，只保留初学者理解核心机制所需节点。
- 生成方式：程序化 SVG 转 PNG，确保中文、箭头和来源文字准确。
- 人工核验：逐项核对节点顺序、中文、箭头和来源；不得用生成式图片替代机制推理。

## 其他正文图

- delivery-inputs.png：五类输入——容量信号、版本组合、任务属性、发布门槛、回滚对象。
- delivery-failure.png：三类失效——只看 CPU 扩容忽略外部配额；新旧任务状态不兼容仍混跑；回滚只切镜像却遗漏缓存和在途写入。
- delivery-controls.png：控制组合——业务和队列指标驱动扩缩、并发上限、背压和优先级、版本化灰度与可观察门槛、状态迁移、在途任务策略和回滚演练。
- delivery-verification.png：验证闭环与指标——队列年龄与任务完成时间、扩容后 429 放大系数、灰度版本错误预算、单成功任务的边际成本。

所有正文图为 1536×1024 PNG，必须包含准确中文；颜色用于分组，不替代文字语义。正文图不兼作封面，封面不计入每篇至少五张正文图。
