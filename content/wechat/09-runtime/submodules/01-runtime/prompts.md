# 智能体运行时配图提示词与校验记录

- 版本：0.1.0
- 阶段：第九模块公众号推文初稿
- Git 状态：基于 9b4282c（main；本模块文件尚未提交，另有编辑器临时文件未跟踪）
- 修改时间：2026-09-29 20:38 CST

## 封面

封面底图由图像模型生成无文字编辑插画，再用确定性 SVG 排版叠加中文标题。底图保持暖白纸张、橙色与深青色点缀，右侧用与“智能体运行时”有关的抽象场景，左侧留出标题空间。禁止水印、乱码、伪文字和品牌标识。主文与面试文分别输出 900×383 PNG。

## 原理图：runtime-principle.png

- 用途：解释“长任务生命周期与检查点怎样配合”。
- 资料来源：
- Kubernetes：Observability：https://kubernetes.io/docs/concepts/cluster-administration/observability/
- A2A Protocol Specification：https://a2a-protocol.org/latest/specification/
- Kubernetes：Deployments：https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- 保留节点：创建任务（记录输入、版本和幂等键）；运行步骤（每步有明确开始与结果）；保存检查点（状态与外部回执持久化）；暂停或恢复（等待人、配额或事件）；完成与清理（确认输出、释放租约与资源）。
- 箭头语义：前一步向后一步提供事实、控制或任务状态；不表示所有步骤都同步，也不表示必须使用同一产品。
- 简化项：省略厂商 API、部署拓扑和异常分支，只保留初学者理解核心机制所需节点。
- 生成方式：程序化 SVG 转 PNG，确保中文、箭头和来源文字准确。
- 人工核验：逐项核对节点顺序、中文、箭头和来源；不得用生成式图片替代机制推理。

## 其他正文图

- runtime-inputs.png：五类输入——任务标识、当前状态、检查点、控制信号、资源租约。
- runtime-failure.png：三类失效——把内存中的对话当唯一状态；恢复后重复执行不可逆工具；取消只停止前端却不停止后台任务。
- runtime-controls.png：控制组合——显式状态机和持久检查点、副作用前后记录意图与回执、租约、心跳与超时接管、可传播取消和补偿流程。
- runtime-verification.png：验证闭环与指标——检查点恢复成功率、任务重复执行率、取消传播时延、僵尸任务与租约超时数。

所有正文图为 1536×1024 PNG，必须包含准确中文；颜色用于分组，不替代文字语义。正文图不兼作封面，封面不计入每篇至少五张正文图。
