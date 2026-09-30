# 重排序模型子模块配图提示词

版本：0.3.0；修订时间：2026-09-29 16:22 CST；依据提交：`549c2cc`（`main`；修订前仅有 Word 临时锁文件未跟踪）。

正文配图统一为 1536×1024 PNG；公众号封面图统一为 900×383 PNG。暖白背景，橙色、青绿和深灰点缀，中文清晰，无水印、无 Logo。封面图使用内置图像生成工具；结构图 `reranker-two-stage.png`、`reranker-evaluation.png` 与 `reranker-learning-objectives.png` 由 `scripts/render-foundation-figure-fixes.py` 确定性绘制。

1. `reranker-cover-main-wechat.png`：主文封面图。标题“大话重排序”“相似条款谁该排前面”；用北京四级现行、异地与旧版条款三张卡片表现“先召回，再精排”。
2. `reranker-cover-interview-wechat.png`：面试副文封面图。标题“面试题：相似制度怎样排出先后”；画面包含查询、候选对比较和排序结果。
3. `reranker-two-stage.png`：先召回候选，再逐对比较并改变候选顺序；用旧版、新版、异地条款展示排序变化。不要展示没有来源的数值分数；在图中注明先后次序只是示意，不是概率。
4. `reranker-cross-encoder.png`：查询和段落共同进入模型，标签“查询 + 段落”“联合阅读”“相关性分数”。
5. `reranker-policy.png`：排序前后的业务筛子，标签“权限”“生效日期”“来源质量”“相关性”。
6. `reranker-evaluation.png`：同一组相关性标注问题同时评测基线与新排序；质量看 MRR/NDCG，代价看 p95 时延和调用成本。没有实测数据时不画上升曲线或数值柱图。
7. `reranker-learning-objectives.png`：训练目标对比图。并列展示 Pointwise“单项打分”、Pairwise“成对比较”和 Listwise“整列排序”，同时标出监督信号与数据代价。
8. `reranker-principle.png`：原理图。依据 [Passage Re-ranking with BERT](https://arxiv.org/abs/1901.04085) 第 2 节改绘。保留 `[CLS] 查询 [SEP] 候选段落 [SEP] → BERT → 相关性分数`；说明每个查询—候选对单独计算，分数只用于排序。图注：“依据 Nogueira 与 Cho，第 2 节改绘。”

复核：已目视检查示意排序、评测指标、训练目标和封面图中央安全区；正文不重复插入封面图。
