# 向量嵌入子模块配图提示词

版本：0.2.0；修订时间：2026-09-28 17:26 CST；依据提交：`47c0ee0`（`main`，修订前 clean）。

统一规格：1536x1024 PNG，暖白背景，青绿、蓝色和橙色点缀，中文清晰，无水印、无 Logo。原有成片使用 `gpt-image-2`；本轮纠错图 `embedding-chunking.png` 和 `embedding-evaluation.png` 由 `scripts/render-foundation-figure-fixes.py` 确定性绘制。

1. `embedding-cover.png`：封面，不同措辞的相近问题在向量空间靠近，标题“向量嵌入”，副标题“把意思变成可以计算的距离”。
2. `embedding-space.png`：二维语义地图，标签“差旅报销”“住宿标准”“产品故障”“账号登录”，相近主题成簇。
3. `embedding-retrieval.png`：双塔检索，标签“查询向量”“文档向量”“近邻搜索”“候选资料”。
4. `embedding-chunking.png`：制度原文按条款切片后明确经过嵌入模型，形成“向量 + 片段 ID”并建立索引；来源、版本和适用范围随片段保存，查询时再按身份、日期过滤。不能漏掉嵌入模型，也不能把权限过滤画成一次入库操作。
5. `embedding-evaluation.png`：测试问题进入嵌入检索得前 K 个结果；人工标注的相关资料是独立标准答案，两者对照计算 Recall@K。不得画成“相关资料生成召回结果”。
6. `embedding-principle.png`：原理图。依据 [Sentence-BERT](https://arxiv.org/abs/1908.10084) Figure 2（推理阶段）改绘，不能错标为 Figure 1（分类训练结构）。保留查询与文档两条独立编码路径、向量 `q/d` 和相似度计算；强调文档向量可预计算，相似度不是事实证明。图注：“依据 Reimers 与 Gurevych，Figure 2 改绘。”

复核：已目视检查两张新图的中文、箭头及“检索结果／标注答案”边界。
