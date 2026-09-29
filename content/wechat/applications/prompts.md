# 应用落地与项目实践总览配图提示词与校验记录

- 版本：0.1.0
- 阶段：第十模块公众号推文初稿
- Git 状态：基于 5d31161（main；本模块文件尚未提交，另有编辑器临时文件未跟踪）
- 修改时间：2026-09-29 20:41 CST

## 封面

封面底图由图像模型生成无文字编辑插画，再用确定性 SVG 排版叠加中文标题。底图保持暖白纸张、橙色与深青色点缀，右侧用与“应用落地与项目实践总览”有关的抽象场景，左侧留出标题空间。禁止水印、乱码、伪文字和品牌标识。主文与面试文分别输出 900×383 PNG。

## 原理图：applications-principle.png

- 用途：解释“从业务问题到可交付智能体的路径”。
- 资料来源：
- GAIA：A Benchmark for General AI Assistants：https://arxiv.org/abs/2311.12983
- WebArena：A Realistic Web Environment for Building Autonomous Agents：https://arxiv.org/abs/2307.13854
- SWE-bench：Can Language Models Resolve Real-World GitHub Issues?：https://arxiv.org/abs/2310.06770
- RT-2：Vision-Language-Action Models Transfer Web Knowledge to Robotic Control：https://robotics-transformer2.github.io/assets/rt2.pdf
- 保留节点：界定任务（对象、范围、完成条件）；建立基线（人工、规则或单次模型）；组合能力（知识、工具、流程和记忆）；设置责任门（权限、审批和安全回退）；真实验收（结果、过程、成本与反馈）。
- 箭头语义：前一步向后一步提供事实、控制或任务状态；不表示所有步骤都同步，也不表示必须使用同一产品。
- 简化项：省略厂商 API、部署拓扑和异常分支，只保留初学者理解核心机制所需节点。
- 生成方式：程序化 SVG 转 PNG，确保中文、箭头和来源文字准确。
- 人工核验：逐项核对节点顺序、中文、箭头和来源；不得用生成式图片替代机制推理。

## 其他正文图

- applications-inputs.png：五类输入——环境、证据、动作、风险、验收。
- applications-failure.png：三类失效——用漂亮演示替代真实任务完成率；所有场景共用一个提示和一套指标；没有简单基线便宣称多步智能体更好。
- applications-controls.png：控制组合——任务合同与明确完成条件、能力组合和最小权限、风险分级的人机协作、真实环境评测、灰度和成本核算。
- applications-verification.png：验证闭环与指标——端到端任务成功率、人工返工与接管率、错误副作用事件、相对基线的时间与成本收益。

所有正文图为 1536×1024 PNG，必须包含准确中文；颜色用于分组，不替代文字语义。正文图不兼作封面，封面不计入每篇至少五张正文图。
