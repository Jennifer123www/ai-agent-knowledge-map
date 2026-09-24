# 向量嵌入子模块配图提示词

统一规格：`gpt-image-2`，1536x1024 PNG，暖白背景，青绿、蓝色和橙色点缀，用点阵和空间距离表现语义，中文清晰，无水印、无 Logo。

1. `embedding-cover.png`：封面，不同措辞的相近问题在向量空间靠近，标题“向量嵌入”，副标题“把意思变成可以计算的距离”。
2. `embedding-space.png`：二维语义地图，标签“差旅报销”“住宿标准”“产品故障”“账号登录”，相近主题成簇。
3. `embedding-retrieval.png`：双塔检索，标签“查询向量”“文档向量”“近邻搜索”“候选资料”。
4. `embedding-chunking.png`：长文档被按标题和条款切分，标签“语义切分”“来源元数据”“权限过滤”“向量索引”。
5. `embedding-evaluation.png`：召回评测漏斗，标签“测试问题”“相关资料”“召回结果”“Recall@K”。
6. `embedding-principle.png`：原理图。依据 [Sentence-BERT](https://arxiv.org/abs/1908.10084) Figure 2（推理阶段）改绘，不能错标为 Figure 1（分类训练结构）。保留查询与文档两条独立编码路径、向量 `q/d` 和相似度计算；强调文档向量可预计算，相似度不是事实证明。图注：“依据 Reimers 与 Gurevych，Figure 2 改绘。”
