# 向量嵌入子模块配图记录

版本：0.7.0；修订时间：2026-10-10 13:15 CST；Git 状态：基于 `58f13b6`（`main`；本轮文章修改尚未提交）。

本轮按 1.4 的配图标准重绘正文图：画面必须说明一个具体机制、差别或排障步骤，不能仅把正文口号放大。技术图的文字、箭头、数值要准确，所以使用 `scripts/render-embedding-figures.py` 以确定性绘图生成 1536×1024 横版 PNG。论文来源和教学算例边界写在紧邻图注，不放在图底白条；保留既有的主、副封面，不把封面计入正文图片数。

## 主文配图

1. `embedding-neighborhood-v2.png`：教学用二维向量空间。问句靠近旧版和新版制度，远离打印机维修；它说明主题相近不等于版本适用。点位不是模型实测，不给轴赋予“日期”“职级”等固定含义。
2. `embedding-training-pairs-v2.png`：同一条含住宿日期的查询，对应新版正例、旧版难负例、打印机流程易负例；用相对得分关系表达对比训练，不杜撰分数。日期改变，正负标签也要复核。训练思想参照 [Sentence-BERT 第 3 节](https://arxiv.org/pdf/1908.10084) 与 [E5 第 4 节](https://arxiv.org/pdf/2212.03533)。
3. `embedding-dual-encoder-v2.png`：主文原理图。参照 [Sentence-BERT Figure 2](https://arxiv.org/pdf/1908.10084)，问句、条款分路编码与 pooling、共享参数、得到 `q/d` 再比较相似度；文档向量可预先计算。不把 DPR 的独立参数结构画成 Sentence-BERT。
4. `embedding-chunk-evidence-v2.png`：左侧制度原文含地区、职级、生效日、金额；右侧对照过短片段和完整条款片段，突出输入缺字段与来源追溯的差别。
5. `embedding-recall-audit-v2.png`：按当前住宿日期标注新版为唯一正例，示意旧版第 1、新版第 2、异地第 3，因此 `Recall@1=0/1`、`Recall@3=1/1`、单题倒数名次 `1/2`。排序为教学构造，不是检索实测。

## 副文配图

1. `embedding-pooling-choice-v2.png`：参照 [Sentence-BERT 第 3 节](https://arxiv.org/pdf/1908.10084)，表示每个输入位置编码后可取 `[CLS]` 位置或平均汇总；两条路是可选方法，不是串行步骤。
2. `embedding-encoder-variants-v2.png`：对照 [Sentence-BERT](https://arxiv.org/pdf/1908.10084)、[DPR 第 3.1 节](https://arxiv.org/pdf/2004.04906)、[E5 第 4.1 节](https://arxiv.org/pdf/2212.03533)：共享参数、独立参数、共享参数但使用 `query:`/`passage:` 前缀。左右输入互相对照，不能用指向箭头误画为问句流入文档。
3. `embedding-metric-geometry-v2.png`：精确教学算例 `q=(1,0)`、`A=(0.8,0.6)`、`B=(1.5,1.5)`；余弦为 `A=0.8 > B≈0.707`，未归一化点积为 `B=1.5 > A=0.8`，展示候选长度可使排名反转。三者均归一化后，余弦、点积与欧氏距离对同一查询的排序等价。
4. `embedding-fragment-input-v2.png`：把同一制度原文、截断输入、过短片段、完整条款并列，指出各自丢失金额或适用条件；“知识库里有文件”和“编码器见到完整条件”是两回事。
5. `embedding-index-diagnostic-v2.png`：依据 [Faiss 官方索引说明](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes) 区分 Flat 精确搜索与 ANN 近似索引。固定同一批向量、查询与过滤条件，教学设定中精确搜索第 3 名有新版而线上索引缺失，用于引导核查索引新鲜度、搜索参数和过滤顺序，不指称任何具体索引一定如此。
第九题改用 8 月和 9 月两道查询解释正例随日期变化，以及逐题平均与整体汇总的区别；不再复用主文的单题召回图。副文其余五图各承担独立讲解任务。

## 视觉复核

全部正文图为横版、暖白底、低饱和青绿／橙色点缀；逐张检查中文、数字、箭头、溢出和下方独立免责声明。旧版图片保留作历史素材，不再由当前文章和 `series.json` 引用。公众号草稿更新后仍需在手机端检查缩图可读性与封面裁切。
