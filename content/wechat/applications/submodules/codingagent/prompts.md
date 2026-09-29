# 编程智能体配图提示词与校验记录

- 版本：0.1.0
- 阶段：第十模块公众号推文初稿
- Git 状态：基于 5d31161（main；本模块文件尚未提交，另有编辑器临时文件未跟踪）
- 修改时间：2026-09-29 20:41 CST

## 封面

封面底图由图像模型生成无文字编辑插画，再用确定性 SVG 排版叠加中文标题。底图保持暖白纸张、橙色与深青色点缀，右侧用与“编程智能体”有关的抽象场景，左侧留出标题空间。禁止水印、乱码、伪文字和品牌标识。主文与面试文分别输出 900×383 PNG。

## 原理图：codingagent-principle.png

- 用途：解释“真实软件缺陷的修复闭环”。
- 资料来源：
- SWE-bench：Can Language Models Resolve Real-World GitHub Issues?：https://arxiv.org/abs/2310.06770
- SWE-agent：Agent-Computer Interfaces Enable Automated Software Engineering：https://arxiv.org/abs/2405.15793
- NIST AI 600-1：Generative AI Profile：https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- 保留节点：理解问题（重述现象、期望和边界）；检索代码（调用链、历史和测试）；复现失败（建立最小可执行样例）；修改与测试（最小补丁、针对性与回归）；审查交付（差异、风险、回滚与说明）。
- 箭头语义：前一步向后一步提供事实、控制或任务状态；不表示所有步骤都同步，也不表示必须使用同一产品。
- 简化项：省略厂商 API、部署拓扑和异常分支，只保留初学者理解核心机制所需节点。
- 生成方式：程序化 SVG 转 PNG，确保中文、箭头和来源文字准确。
- 人工核验：逐项核对节点顺序、中文、箭头和来源；不得用生成式图片替代机制推理。

## 其他正文图

- codingagent-inputs.png：五类输入——问题描述、仓库状态、证据、约束、验收。
- codingagent-failure.png：三类失效——未复现便凭猜测修改；覆盖用户未提交改动；测试只证明代码能运行而没覆盖缺陷。
- codingagent-controls.png：控制组合——隔离工作区和明确 Git 状态、搜索优先、最小补丁、缺陷测试加回归套件、依赖与命令沙箱、人工差异审查。
- codingagent-verification.png：验证闭环与指标——真实问题解决率、补丁通过且无回归比例、无关修改行数、人工返修和回滚率。

所有正文图为 1536×1024 PNG，必须包含准确中文；颜色用于分组，不替代文字语义。正文图不兼作封面，封面不计入每篇至少五张正文图。
