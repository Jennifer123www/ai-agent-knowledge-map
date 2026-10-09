# 向量嵌入子模块配图提示词

版本：0.5.0；修订时间：2026-10-09 18:40 CST；依据提交：`ea8f4f5`（`main`；修订前工作区干净）。

正文配图统一为 1536×1024 PNG；公众号封面图统一为 900×383 PNG。暖白背景，青绿、蓝色和橙色点缀，中文清晰，无水印、无 Logo。主封面是已有生成图；副封面和部分原理、诊断图保留可维护的 SVG／绘图脚本，成片仍为 PNG。`embedding-principle.png` 由 `scripts/render-principle-diagrams.mjs` 绘制；`embedding-chunking.png`、`embedding-evaluation.png` 与 `embedding-metric-comparison.png` 由 `scripts/render-foundation-figure-fixes.py` 确定性绘制。论文出处与教学示意边界放在图注，不放图底白条。

1. `embedding-cover-main-wechat.png`：主文封面图。标题“大话向量嵌入”“同一个意思为何找不到”；将“酒店最多报多少”和“差旅住宿费限额”放在向量空间两侧，说明不同说法需要语义连接。日期、地区、职级的适用性留到正文讲解，不在封面伪装成相似度已解决的问题。
2. `embedding-cover-interview-wechat.png`：面试副文封面图。中央放大镜里只保留旧版与现行版两张条款卡、450 与 500 两个示意金额，以及叉号与勾号；不重复完整文章标题。关键内容落在中央正方形缩略图安全区。源图：`scripts/figures/embedding/embedding-cover-interview-wechat.svg`。
3. `embedding-space.png`：二维语义地图，标签“差旅报销”“住宿标准”“产品故障”“账号登录”，相近主题成簇。
4. `embedding-retrieval.png`：双塔检索，标签“查询向量”“文档向量”“近邻搜索”“候选资料”。
5. `embedding-chunking.png`：示意制度原文完整保留“北京、A 职级、9 月 1 日起、上限 500 元”，按条款切片后经过嵌入模型，形成“向量 + 片段 ID”；片段 ID 仍能回到原文、版本和适用范围。图中不把查询过滤画成建索引时已经完成的动作。文末不加空泛总结白条。
6. `embedding-evaluation.png`：教学示意“旧版 450 元排第 1，新版 500 元排第 2，异地条款排第 3”；按 2026 年 9 月 15 日、北京、A 职级独立标注新版为唯一正例，因此 `Recall@3 = 1/1`，但旧版仍排在前面。排名不是实测，图注须写明。图形展示召回覆盖与排序质量不同，不能把标注画成检索结果的来源。
7. `embedding-metric-comparison.png`：在同一单位圆上绘制查询向量 `q` 和候选 `d1/d2`，画出方向与端点距离；图中只在单位向量条件下给出点积等于余弦、距离平方等于 `2 - 2 × 点积` 的关系，不把这组等价推广到未归一化向量。文字只留读图所需的短标签，无独立免责声明。
8. `embedding-principle.png`：原理图。依据 [Sentence-BERT](https://arxiv.org/html/1908.10084) Figure 2（推理阶段）改绘，不能错标为 Figure 1（分类训练结构）。保留查询与文档两条编码路径、共享参数、向量 `q/d`、相似度计算，以及文档向量可预计算。图内不放论文出处或“相似度不是事实证明”等图底总结；出处和边界在紧邻图注及正文说明。

9. `embedding-pooling.png`：面试题 1 的句向量汇总图。依据 [Sentence-BERT 第 3 节](https://arxiv.org/html/1908.10084) 说明输入位置经过编码后，可选择特殊位置或平均汇总得到固定长度表示；两条路径是备选，不画成先后两步。源图：`scripts/figures/embedding/embedding-pooling.png.svg`。
10. `embedding-encoder-variants.png`：面试题 3 的架构比较图。依据 [Sentence-BERT](https://arxiv.org/html/1908.10084)、[DPR](https://arxiv.org/html/2004.04906) 与 [E5](https://arxiv.org/html/2212.03533) 的编码约定，分别画共享参数、独立参数、共享参数加查询／段落前缀。只比较结构，不暗示效果排名。源图：`scripts/figures/embedding/embedding-encoder-variants.png.svg`。
11. `embedding-fragment-loss.png`：面试题 6 的输入诊断图。同一示意条款“北京、A 职级、9 月 1 日起、500 元”，并排展示截断丢金额、片段过短丢适用条件、保留完整条件三种送入模型的文字。图中数字是教学设定，不是制度实测。源图：`scripts/figures/embedding/embedding-fragment-loss.png.svg`。

本轮复核：已检查改绘图的中文、金额、箭头、共享参数、单位向量条件和底部无独立免责声明；副文专属图解释汇总方式、编码约定、距离度量和输入丢失，与主文只共用召回评测图。仍需在公众号真实卡片和手机端复核封面裁切与正文缩图。
