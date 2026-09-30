# 模型网关与流量治理配图提示词与校验记录

- 版本：0.1.0
- 阶段：第九模块公众号推文初稿
- Git 状态：基于 9b4282c（main；本模块文件尚未提交，另有编辑器临时文件未跟踪）
- 修改时间：2026-09-29 20:38 CST

## 封面

封面底图由图像模型生成无文字编辑插画，再用确定性 SVG 排版叠加中文标题。底图保持暖白纸张、橙色与深青色点缀，右侧用与“模型网关与流量治理”有关的抽象场景，左侧留出标题空间。禁止水印、乱码、伪文字和品牌标识。主文与面试文分别输出 900×383 PNG。

## 原理图：gateway-principle.png

- 用途：解释“模型网关的请求治理链”。
- 资料来源：
- Kubernetes：Observability：https://kubernetes.io/docs/concepts/cluster-administration/observability/
- Kubernetes：Horizontal Pod Autoscaling：https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
- NIST AI RMF Core：https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- 保留节点：身份与租户（确认调用方和预算归属）；策略与配额（并发、速率、token 和费用）；能力路由（模型、区域、版本和任务需求）；弹性调用（超时、退避、熔断与回退）；用量与审计（时延、质量代理和成本）。
- 箭头语义：前一步向后一步提供事实、控制或任务状态；不表示所有步骤都同步，也不表示必须使用同一产品。
- 简化项：省略厂商 API、部署拓扑和异常分支，只保留初学者理解核心机制所需节点。
- 生成方式：程序化 SVG 转 PNG，确保中文、箭头和来源文字准确。
- 人工核验：逐项核对节点顺序、中文、箭头和来源；不得用生成式图片替代机制推理。

## 其他正文图

- gateway-inputs.png：五类输入——任务需求、租户策略、供应商状态、请求特征、回退规则。
- gateway-failure.png：三类失效——每个客户端自行重试形成重试风暴；回退到便宜模型却不告诉业务能力变化；公共 Key 让配额、成本和审计失去归属。
- gateway-controls.png：控制组合——集中认证和租户配额、带抖动的指数退避与重试预算、熔断、优先队列和能力感知回退、请求级用量、版本与成本归因。
- gateway-verification.png：验证闭环与指标——网关排队与上游 P95、429 后放大系数、回退触发及质量变化、每租户成功任务成本。

所有正文图为 1536×1024 PNG，必须包含准确中文；颜色用于分组，不替代文字语义。正文图不兼作封面，封面不计入每篇至少五张正文图。
