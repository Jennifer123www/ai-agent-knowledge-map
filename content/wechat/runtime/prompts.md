# 系统设计、运行时与成本总览配图提示词与校验记录

- 版本：0.1.0
- 阶段：第九模块公众号推文初稿
- Git 状态：基于 9b4282c（main；本模块文件尚未提交，另有编辑器临时文件未跟踪）
- 修改时间：2026-09-29 20:38 CST

## 封面

封面底图由图像模型生成无文字编辑插画，再用确定性 SVG 排版叠加中文标题。底图保持暖白纸张、橙色与深青色点缀，右侧用与“系统设计、运行时与成本总览”有关的抽象场景，左侧留出标题空间。禁止水印、乱码、伪文字和品牌标识。主文与面试文分别输出 900×383 PNG。

## 原理图：runtime-system-principle.png

- 用途：解释“生产级智能体系统的运行骨架”。
- 资料来源：
- Kubernetes：Observability：https://kubernetes.io/docs/concepts/cluster-administration/observability/
- Kubernetes：Horizontal Pod Autoscaling：https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
- A2A Protocol Specification：https://a2a-protocol.org/latest/specification/
- 保留节点：入口与触发（请求、定时或业务事件）；运行时（任务状态、检查点和取消）；能力执行（模型网关、工具和沙箱）；可靠基础（队列、存储、缓存与幂等）；交付治理（扩缩、发布、观测和成本）。
- 箭头语义：前一步向后一步提供事实、控制或任务状态；不表示所有步骤都同步，也不表示必须使用同一产品。
- 简化项：省略厂商 API、部署拓扑和异常分支，只保留初学者理解核心机制所需节点。
- 生成方式：程序化 SVG 转 PNG，确保中文、箭头和来源文字准确。
- 人工核验：逐项核对节点顺序、中文、箭头和来源；不得用生成式图片替代机制推理。

## 其他正文图

- runtime-system-inputs.png：五类输入——任务契约、执行策略、状态、事件、资源。
- runtime-system-failure.png：三类失效——进程重启后从头执行并重复写入；只按 CPU 扩容却忽略队列和供应商配额；跨智能体调用只有聊天文本没有任务状态。
- runtime-system-controls.png：控制组合——持久任务状态和检查点、隔离沙箱与统一模型网关、事件幂等、背压和死信、版本化发布、预算和端到端观测。
- runtime-system-verification.png：验证闭环与指标——任务完成与恢复率、重复副作用事件数、队列等待和长尾时延、单个成功任务总成本。

所有正文图为 1536×1024 PNG，必须包含准确中文；颜色用于分组，不替代文字语义。正文图不兼作封面，封面不计入每篇至少五张正文图。
