# 具身智能体配图提示词与校验记录

- 版本：0.1.0
- 阶段：第十模块公众号推文初稿
- Git 状态：基于 5d31161（main；本模块文件尚未提交，另有编辑器临时文件未跟踪）
- 修改时间：2026-09-29 20:41 CST

## 封面

封面底图由图像模型生成无文字编辑插画，再用确定性 SVG 排版叠加中文标题。底图保持暖白纸张、橙色与深青色点缀，右侧用与“具身智能体”有关的抽象场景，左侧留出标题空间。禁止水印、乱码、伪文字和品牌标识。主文与面试文分别输出 900×383 PNG。

## 原理图：embodied-principle.png

- 用途：解释“从语言目标到安全物理动作的闭环”。
- 资料来源：
- RT-2：Vision-Language-Action Models Transfer Web Knowledge to Robotic Control：https://robotics-transformer2.github.io/assets/rt2.pdf
- RT-1：Robotics Transformer for Real-World Control at Scale：https://arxiv.org/abs/2212.06817
- Do As I Can, Not As I Say：Grounding Language in Robotic Affordances：https://arxiv.org/abs/2204.01691
- 保留节点：感知环境（图像、位置、力与状态）；理解目标（对象、约束和完成条件）；选择高层动作（VLA 或策略提出技能序列）；低层控制（轨迹、抓取和执行反馈）；安全监督（限速、碰撞、急停和人工接管）。
- 箭头语义：前一步向后一步提供事实、控制或任务状态；不表示所有步骤都同步，也不表示必须使用同一产品。
- 简化项：省略厂商 API、部署拓扑和异常分支，只保留初学者理解核心机制所需节点。
- 生成方式：程序化 SVG 转 PNG，确保中文、箭头和来源文字准确。
- 人工核验：逐项核对节点顺序、中文、箭头和来源；不得用生成式图片替代机制推理。

## 其他正文图

- embodied-inputs.png：五类输入——观测、语言目标、技能与可供性、控制约束、反馈。
- embodied-failure.png：三类失效——训练场景识别正确但真实光照下误判；高层计划可读却不具备物理可执行性；把模型置信度当作独立安全保证。
- embodied-controls.png：控制组合——多传感器与状态估计、技能可供性和分层控制、独立碰撞、限速、急停安全控制器、仿真、回放、真实小步试验和人工接管。
- embodied-verification.png：验证闭环与指标——真实任务成功率、每千次动作安全事件、人工接管和急停率、环境变化下性能退化。

所有正文图为 1536×1024 PNG，必须包含准确中文；颜色用于分组，不替代文字语义。正文图不兼作封面，封面不计入每篇至少五张正文图。
