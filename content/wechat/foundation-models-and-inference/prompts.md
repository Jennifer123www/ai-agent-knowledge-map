# 基础模型与推理总览配图提示词

统一规格：1536x1024 PNG，暖白纸张背景，深灰线条，梅红、青绿、橙色少量点缀，中文编辑型信息图。文字必须逐字准确，字号大，留白充足，无水印、无 Logo、无长段落。框架图可使用 `gpt-image-2`；原理图优先使用可复现的结构图渲染。

1. `foundation-cover.png`：封面。五个岗位围绕一个 AI Agent 工作台协作，标题“基础模型与推理”，标签“大语言模型”“多模态”“向量嵌入”“重排序”“模型适配”。
2. `foundation-model-team.png`：五类模型像五位专业队员，标签“生成”“感知”“召回”“精排”“适配”，中央标签“Agent”。
3. `foundation-data-flow.png`：从用户问题、图片或文档进入，依次经过“理解输入”“寻找证据”“筛选证据”“生成结果”“规则验证”。
4. `foundation-selection.png`：模型选型三角，三个角分别为“质量”“时延”“成本”，中央标签“任务风险”。
5. `foundation-production.png`：生产闭环，标签“离线评测”“灰度发布”“线上监控”“失败回退”“版本记录”。

6. `foundation-principle.png`：原理图。依据 [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) Figure 1 改绘。保留“问题 → 查询编码器”“文档索引 → 检索候选”“候选 → 生成模型 → 带引用回答”；新增重排序时标明“可选工程扩展”。图注：“依据 Lewis 等，Figure 1 改绘；重排序为工程扩展。”
