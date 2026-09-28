# 知识源、知识图谱与 GraphRAG 配图说明

统一 1536×1024 PNG，中文短标签，暖白底，青绿/梅红表示关系与证据，不放虚构“脑网络”。

1. `kg-cover.png`：封面“知识图谱：把关系讲明白”；节点“员工”“地区”“制度”“条款”。
2. `kg-sources.png`：文档原文、业务表、图谱三类来源并列；标出“原文证据”“当前状态”“关系路径”。
3. `kg-principle.png`：原理图，依据 Edge 等 [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130) Figure 1 与 §3 改绘。保留“源文本→实体关系图→社区划分→社区摘要→全局问题的局部回答→汇总”。另加一条“具体条款问题回到原文”的校验支线，明确它是工程补充，不把论文的全局摘要任务说成所有 GraphRAG 的默认用法。图注：依据 Edge 等 Figure 1 改绘；原文核验支线为工程补充。
4. `kg-query.png`：局部多跳路径“员工→部门→适用制度→条款”，旁边标“回原文核对”。
5. `kg-contrast.png`：向量索引找语义相近片段，图谱走明确关系；两条路线用途不同。
6. `kg-provenance.png`：每条关系挂来源位置和有效期，未经原文核实的边标“待确认”。
