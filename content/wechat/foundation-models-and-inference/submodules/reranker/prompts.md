# 重排序模型子模块配图提示词

版本：0.2.0；修订时间：2026-09-28 17:26 CST；依据提交：`47c0ee0`（`main`，修订前 clean）。

统一规格：1536x1024 PNG，暖白背景，橙色、青绿和深灰点缀，中文清晰，无水印、无 Logo。原有成片使用 `gpt-image-2`；本轮纠错图 `reranker-two-stage.png` 和 `reranker-evaluation.png` 由 `scripts/render-foundation-figure-fixes.py` 确定性绘制。

1. `reranker-cover.png`：封面，一叠候选资料被精细排序，标题“重排序模型”，副标题“先广泛找，再认真挑”。
2. `reranker-two-stage.png`：先召回候选，再逐对比较并改变候选顺序；用旧版、新版、异地条款展示排序变化。不要展示没有来源的数值分数；在图中注明先后次序只是示意，不是概率。
3. `reranker-cross-encoder.png`：查询和段落共同进入模型，标签“查询 + 段落”“联合阅读”“相关性分数”。
4. `reranker-policy.png`：排序前后的业务筛子，标签“权限”“生效日期”“来源质量”“相关性”。
5. `reranker-evaluation.png`：同一组相关性标注问题同时评测基线与新排序；质量看 MRR/NDCG，代价看 p95 时延和调用成本。没有实测数据时不画上升曲线或数值柱图。
6. `reranker-principle.png`：原理图。依据 [Passage Re-ranking with BERT](https://arxiv.org/abs/1901.04085) 第 2 节改绘。保留 `[CLS] 查询 [SEP] 候选段落 [SEP] → BERT → 相关性分数`；说明每个查询—候选对单独计算，分数只用于排序。图注：“依据 Nogueira 与 Cho，第 2 节改绘。”

复核：已目视检查新图的示意排序、评测指标和无虚构分数。
