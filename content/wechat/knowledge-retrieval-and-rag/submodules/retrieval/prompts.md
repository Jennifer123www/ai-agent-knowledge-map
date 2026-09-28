# 召回、重排序与引用子模块配图说明

版本：0.2.0；修订时间：2026-09-28 17:26 CST；依据提交：`47c0ee0`（`main`，修订前 clean）。

统一 1536×1024 PNG、暖白底、深灰字、青绿与橙色重点，无水印，中文标签需逐字检查。

1. `retrieval-cover.png`：封面“检索：找得到，也要选得对”。
2. `retrieval-candidates.png`：同一问题并行进入关键词召回与向量召回，两路候选再合并去重；不能画成关键词检索结果先送入向量检索。
3. `retrieval-principle.png`：原理对照图，依据 Karpukhin 等 [Dense Passage Retrieval](https://arxiv.org/abs/2004.04906) Figure 1 / §2.1 的双编码器检索，以及 Nogueira 与 Cho [Passage Re-ranking with BERT](https://arxiv.org/abs/1901.04085) §2 的查询—候选联合编码重排序重新绘制。左边问题与文档分别编码、向量匹配选 Top-k；右边对少量候选逐对联合打分。硬过滤是图外工程约束。图注：依据 DPR §2.1 与 Passage Re-ranking with BERT §2 改绘。
4. `retrieval-filter.png`：权限、适用地区、日期先筛；相似度不能越过硬条件。
5. `retrieval-citation.png`：候选片段与文档 ID、页码、版本和条款链接绑定。
6. `retrieval-metrics.png`：分别查看“正确证据是否在候选”“是否排进前列”“引用能否定位”三项。
