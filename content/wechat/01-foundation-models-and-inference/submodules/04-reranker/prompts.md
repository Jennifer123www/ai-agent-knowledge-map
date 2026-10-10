# 重排序模型子模块配图设计记录

版本：0.5.0；修订时间：2026-10-10 12:01 CST；基线：`5a7a15e`（`main`；修改前工作区干净）。

本组封面沿用 `reranker-cover-main-wechat-v2.png` 与 `reranker-cover-interview-wechat-v2.png`。正文图改为 1536×1024 横版 PNG，由 [`render-reranker-figures.py`](../../../../../scripts/render-reranker-figures.py) 确定性绘制：准确的中文、名次、箭头与日期不交给生成式模型猜。两篇各五张正文图，仅共享一张 BERT 原理图；没有把封面重复充作首图。

## 资料与机制边界

- [Nogueira、Cho，Passage Re-ranking with BERT](https://arxiv.org/pdf/1901.04085)，第 2 节：先检索候选；每个查询—段落对独立输入 BERT；取 `[CLS]` 表示，经单层分类头估计文本相关性，再按得分排序。论文用二分类交叉熵训练。此机制不判断制度有效、权限或答案正确。
- [Sentence Transformers，Retrieve & Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)：双塔分别编码以检索，交叉编码器联合输入查询和候选，对前 K 条逐对打分；文档向量可预计算，但完整的查询—候选交叉表示不能预存复用。
- [Liu，Learning to Rank for Information Retrieval](https://www.microsoft.com/en-us/research/publication/learning-to-rank-for-information-retrieval/)：点式、成对和列表式监督信号的区分。图只讲训练单元，不暗示某一种编码器只能采用某一种损失。

## 主文图序

| 文件 | 读者要看见的关系 | 图型与必须保留的对象 | 简化、核对与相邻图注 |
| --- | --- | --- | --- |
| `reranker-two-stage-v3.png` | 召回只决定可排的候选；精排可改变名次，却不能创造漏召回的资料 | 四份同题候选的前后名次与交叉连线；现行北京由第 3 升至第 1 | 名次是教学排列，不是实测分数；旧版是否有效另查版本记录。线条只表示顺序映射，不等于候选之间互相编码。 |
| `reranker-case-evidence-v3.png` | 主题一样，差异落在地区、职级、版本 | 四份制度摘录的地区、职级、版本字段，与同一问题并排对照 | 以短字段代替完整制度，不写金额或未经核实的生效日；旧版只标“另核效期”。 |
| `reranker-cross-encoder-v3.png` | 查询与单段候选放进同一 BERT 输入后，怎样得到相关分 | `[CLS] 查询 [SEP] 段落 [SEP]`、跨段可交互的位置、BERT 编码层、`[CLS]` 分类头 | 依据 Nogueira、Cho 第 2 节改绘；省略层数与完整注意力矩阵。小格的“同/异”只是教材中的词面条件对照，不是模型实测权重，也不声称注意力必定这样分配。换候选须重新联合编码。 |
| `reranker-k-cutoff-v3.png` | 正确条款在第 3 位时，K 截断如何同时影响覆盖与计算量 | K=1…4 逐列扩展；K<3 漏掉现行条款；每个查询需 K 次联合编码 | 沿用本篇四份候选，只计算查询—候选对的次数；没有把调用时延说成严格随 K 线性。 |
| `reranker-validity-timeline-v3.png` | 模型相关分与制度生效日属于两种判断 | 旧版/现行版两条有效区间、同一版本切换点、2026-09-15 提问位置 | 切换点不标造出的具体生效日；真实生效日以制度元数据为准。此图画业务规则，不冒充模型内部原理。 |

## 面试副文图序

| 文件 | 追问与图型 | 来源、数值与图注口径 |
| --- | --- | --- |
| `reranker-encoder-comparison-v3.png` | 双塔与交叉编码器的输入结构、文档向量复用和逐对重算 | 依据 Sentence Transformers 官方 Retrieve & Re-Rank 文档；三个候选是计算方式示例，不是耗时测量。 |
| `reranker-cross-encoder-v3.png` | 追问联合输入与 `[CLS]` 分类头时复用主文已核实原理图 | 依据 Nogueira、Cho 第 2 节；图注说明交互格非实测注意力权重。 |
| `reranker-threshold-shift-v3.png` | 同一组标注样本从模型 A 换到 B，旧阈值为何失灵 | 0.83/0.75/0.36/0.28 与 0.61/0.55/0.30/0.22 均为教学算例；橙线 0.70。与正文相邻图注明确非实测，不把相关性阈值解释成业务批准率。 |
| `reranker-metric-lanes-v3.png` | 同一组有分级标签的候选前后移动；RR 与 NDCG 分别看什么 | 教学标注 3=能直接回答、2=例外条款、0=不相关；本题 RR 约定只认等级 3，故 1/2→1。多题平均才称 MRR；NDCG 才纳入等级 2 的位置。 |
| `reranker-learning-signals-v3.png` | 同一查询与候选，在点式、成对、列表式训练里分别交给模型什么标签 | 依据 Liu 的排序学习体系；没有把分类头、模型结构与训练损失混作一回事。 |

## 出图约束与复核

颜色固定：青绿=目标或相关，梅红/红=相似却冲突，橙=对照或阈值；不能仅靠颜色辨义。画面不设整幅左侧竖条、底部免责声明和泛化四格流程。关键字段字号约 29—42 px，标题约 57 px；需在 330—345 px 的手机正文宽度再核对。所有新图均由脚本导出、目视逐张核对中文、箭头、名次、日期、样本分数、RR 口径和无水印；如公众号真实预览中显得太密，应先缩短文字或拆图，不压小字号。
