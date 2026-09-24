# 基础模型与推理总览配图提示词

统一规格：`gpt-image-2`，1536x1024 PNG，暖白纸张背景，深灰线条，梅红、青绿、橙色少量点缀，中文编辑型信息图。文字必须逐字准确，字号大，留白充足，无水印、无 Logo、无长段落。当前清单中的 5 张总览图均为框架/流程图；下一次重绘本组主文时，必须新增至少 1 张论文依据的原理示意图。

1. `foundation-cover.png`：封面。五个岗位围绕一个 AI Agent 工作台协作，标题“基础模型与推理”，标签“大语言模型”“多模态”“向量嵌入”“重排序”“模型适配”。
2. `foundation-model-team.png`：五类模型像五位专业队员，标签“生成”“感知”“召回”“精排”“适配”，中央标签“Agent”。
3. `foundation-data-flow.png`：从用户问题、图片或文档进入，依次经过“理解输入”“寻找证据”“筛选证据”“生成结果”“规则验证”。
4. `foundation-selection.png`：模型选型三角，三个角分别为“质量”“时延”“成本”，中央标签“任务风险”。
5. `foundation-production.png`：生产闭环，标签“离线评测”“灰度发布”“线上监控”“失败回退”“版本记录”。

原理图候选：`foundation-model-principle.png`。依据 [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) Figure 1，重新绘制查询编码器、文档索引、检索证据与生成模型的关系；若加入重排序，应在图中标明“工程扩展”，不得声称它是原论文 Figure 1 的必备部件。图注写“依据 Lewis 等，Figure 1 改绘，并加入重排序扩展”。
