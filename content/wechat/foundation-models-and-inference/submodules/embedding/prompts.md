# 向量嵌入子模块配图提示词

版本：0.3.0；修订时间：2026-09-29 16:22 CST；依据提交：`549c2cc`（`main`；修订前仅有 Word 临时锁文件未跟踪）。

正文配图统一为 1536×1024 PNG；公众号封面图统一为 900×383 PNG。暖白背景，青绿、蓝色和橙色点缀，中文清晰，无水印、无 Logo。封面图使用内置图像生成工具；结构图 `embedding-chunking.png`、`embedding-evaluation.png` 与 `embedding-metric-comparison.png` 由 `scripts/render-foundation-figure-fixes.py` 确定性绘制。

1. `embedding-cover-main-wechat.png`：主文封面图。标题“大话向量嵌入”“同一个意思为何找不到”；将口语提问和正式制度标题画成向量空间中的两点，并保留“年份、地区、职级”条件卡。
2. `embedding-cover-interview-wechat.png`：面试副文封面图。标题“面试题：向量相似为何找错住宿条款”；展示查询向量、候选条款和难负样本。
3. `embedding-space.png`：二维语义地图，标签“差旅报销”“住宿标准”“产品故障”“账号登录”，相近主题成簇。
4. `embedding-retrieval.png`：双塔检索，标签“查询向量”“文档向量”“近邻搜索”“候选资料”。
5. `embedding-chunking.png`：制度原文按条款切片后明确经过嵌入模型，形成“向量 + 片段 ID”并建立索引；来源、版本和适用范围随片段保存，查询时再按身份、日期过滤。不能漏掉嵌入模型，也不能把权限过滤画成一次入库操作。
6. `embedding-evaluation.png`：测试问题进入嵌入检索得前 K 个结果；人工标注的相关资料是独立标准答案，两者对照计算 Recall@K。不得画成“相关资料生成召回结果”。
7. `embedding-metric-comparison.png`：度量对比图。分别用方向、投影与几何间距解释余弦、点积和欧氏距离，并标注“归一化后余弦与点积排序可能等价”“分数不是正确率”。
8. `embedding-principle.png`：原理图。依据 [Sentence-BERT](https://arxiv.org/abs/1908.10084) Figure 2（推理阶段）改绘，不能错标为 Figure 1（分类训练结构）。保留查询与文档两条独立编码路径、向量 `q/d` 和相似度计算；强调文档向量可预计算，相似度不是事实证明。图注：“依据 Reimers 与 Gurevych，Figure 2 改绘。”

复核：已目视检查中文、箭头、三种度量边界及封面图中央安全区；正文不重复插入封面图。
