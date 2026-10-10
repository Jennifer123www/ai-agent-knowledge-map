"""Render source-checked figures for the 1.3 embedding WeChat article pair.

All positions, scores and ranked examples are teaching constructions, not model
measurements. The paired prompts.md records the papers and figure boundaries.
"""

from math import atan2, cos, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1] / "content/wechat/01-foundation-models-and-inference/submodules/03-embedding/assets"
FONT = next(str(p) for p in (
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
) if p.exists())
W, H = 1536, 1024
BG = "#FBF9F4"
INK = "#243039"
MUTED = "#657078"
LINE = "#D3D9D5"
TEAL = "#177C78"
TEAL_L = "#E5F1EE"
PLUM = "#815368"
PLUM_L = "#F2EAF0"
ORANGE = "#C96C37"
ORANGE_L = "#FFF0E3"
RED = "#B85C54"
BLUE = "#416D9A"


def font(size):
    return ImageFont.truetype(FONT, size)


def text(d, x, y, value, size=35, color=INK, anchor="la"):
    d.text((x, y), value, font=font(size), fill=color, anchor=anchor)


def card(d, box, fill="white", outline=LINE, radius=18, width=3):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(d, a, b, color=TEAL, width=5, head=16):
    d.line((a, b), fill=color, width=width)
    angle = atan2(b[1]-a[1], b[0]-a[0])
    d.polygon([b,
        (b[0]-head*cos(angle)+9*sin(angle), b[1]-head*sin(angle)-9*cos(angle)),
        (b[0]-head*cos(angle)-9*sin(angle), b[1]-head*sin(angle)+9*cos(angle))], fill=color)


def base(title, kicker):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    text(d, 78, 65, kicker, 30, TEAL)
    text(d, 78, 109, title, 57, INK)
    d.line((78, 191, 1458, 191), fill=LINE, width=2)
    return im, d


def save(im, name):
    ROOT.mkdir(parents=True, exist_ok=True)
    im.save(ROOT / name, optimize=True)


def dot(d, x, y, color, r=16):
    d.ellipse((x-r, y-r, x+r, y+r), fill=color, outline="white", width=3)


def vector_space():
    im, d = base("旧版和新版都近，近不等于适用", "二维投影 / 语义相近与业务条件")
    d.line((168, 824, 1250, 824), fill=LINE, width=4)
    d.line((168, 824, 168, 287), fill=LINE, width=4)
    text(d, 1187, 860, "语义方向 1", 29, MUTED)
    text(d, 169, 267, "语义方向 2", 29, MUTED)
    q = (511, 548)
    old = (732, 445)
    new = (789, 591)
    printer = (1163, 365)
    for x,y in ((291,690),(345,505),(909,690),(1015,455),(1172,687),(685,730)):
        dot(d,x,y,"#DEE8E5",8)
    d.line((q, old), fill=RED, width=4)
    d.line((q, new), fill=TEAL, width=4)
    dot(d, *q, BLUE, 23)
    dot(d, *old, RED, 23)
    dot(d, *new, TEAL, 23)
    dot(d, *printer, PLUM, 23)
    card(d, (194, 385, 547, 483), "white", BLUE, 15)
    text(d, 370, 435, "口语问句：酒店能报多少", 32, INK, "mm")
    card(d, (700, 315, 1072, 409), PLUM_L, RED, 15)
    text(d, 887, 362, "旧版 450 元", 38, RED, "mm")
    card(d, (805, 626, 1220, 720), TEAL_L, TEAL, 15)
    text(d, 1012, 673, "新版 500 元", 38, TEAL, "mm")
    card(d, (1135, 247, 1445, 335), "white", PLUM, 15)
    text(d, 1290, 290, "打印机维修", 34, PLUM, "mm")
    save(im, "embedding-neighborhood-v2.png")


def training_pairs():
    im, d = base("正负例会随提问日期改变", "对比训练 / 难负样本")
    card(d, (100, 260, 1430, 377), ORANGE_L, ORANGE, 18)
    text(d, 765, 320, "查询：北京 · A 职级 · 2026-09-15 · 住宿上限？", 40, INK, "mm")
    rows = [
        (460, TEAL, "正例", "新版：9 月 1 日起 · 500 元", "p+"),
        (625, RED, "难负例", "旧版：条件相近 · 450 元", "p-"),
        (790, PLUM, "易负例", "打印机维修流程", "p-"),
    ]
    d.line((274, 382, 274, 846), fill=LINE, width=4)
    for y, col, tag, sentence, symbol in rows:
        card(d, (374, y, 1408, y+112), "white", LINE, 15)
        d.ellipse((402, y+28, 460, y+86), fill=col)
        text(d, 431, y+57, symbol, 28, "white", "mm")
        text(d, 488, y+57, tag, 35, col, "lm")
        text(d, 722, y+57, sentence, 38, INK, "lm")
        arrow(d, (274, y+56), (355, y+56), col, 4, 12)
    text(d, 93, 434, "同一查询", 34, MUTED)
    text(d, 1374, 408, "目标：s(q,p+) > s(q,p-)", 35, TEAL, "ra")
    save(im, "embedding-training-pairs-v2.png")


def dual_encoder():
    im, d = base("两路各自编码，再比较向量", "Sentence-BERT / 推理原理")
    rows = [
        (333, BLUE, "查询", "住酒店最多报多少", "q"),
        (640, ORANGE, "条款", "北京 A 职级条款", "d"),
    ]
    for y, color, kind, phrase, vec in rows:
        card(d, (90, y, 413, y+130), "white", color, 18)
        text(d, 251, y+42, kind, 35, color, "mm")
        text(d, 251, y+94, phrase, 29, INK, "mm")
        card(d, (495, y, 776, y+130), TEAL_L, TEAL, 18)
        text(d, 635, y+44, "BERT 编码器", 36, TEAL, "mm")
        text(d, 635, y+95, "共享参数", 29, MUTED, "mm")
        card(d, (857, y+15, 1051, y+115), "white", LINE, 14)
        text(d, 954, y+65, "Pooling", 31, INK, "mm")
        card(d, (1132, y+17, 1267, y+113), PLUM_L, PLUM, 14)
        text(d, 1199, y+65, vec, 47, PLUM, "mm")
        arrow(d, (425, y+65), (484, y+65), color)
        arrow(d, (788, y+65), (846, y+65), TEAL)
        arrow(d, (1063, y+65), (1121, y+65), PLUM)
    d.line((635, 480, 635, 621), fill=TEAL, width=4)
    text(d, 670, 548, "同一组编码器参数", 29, TEAL)
    arrow(d, (1280, 397), (1380, 542), PLUM)
    arrow(d, (1280, 704), (1380, 570), PLUM)
    text(d, 1396, 555, "相似度", 36, PLUM, "mm")
    text(d, 1130, 817, "文档向量 d 可离线预计算", 33, ORANGE, "ma")
    save(im, "embedding-dual-encoder-v2.png")


def chunk_evidence():
    im, d = base("切片时，不能只留下“500 元”", "建索引 / 输入与来源")
    card(d, (92, 273, 644, 837), "white", LINE, 19)
    text(d, 132, 332, "《差旅住宿费限额》", 39, PLUM)
    d.line((132, 389, 604, 389), fill=LINE, width=3)
    fields = [("地区", "北京"), ("职级", "A"), ("生效", "9 月 1 日起"), ("上限", "500 元")]
    for i, (key, val) in enumerate(fields):
        y=437+i*88
        text(d, 137, y, key, 30, MUTED)
        text(d, 565, y, val, 37, TEAL if i<3 else ORANGE, "ra")
        d.line((132, y+44, 604, y+44), fill="#E5E9E6", width=2)
    arrow(d, (663, 548), (729, 548), ORANGE)
    card(d, (746, 284, 1444, 522), PLUM_L, PLUM, 20)
    text(d, 780, 347, "过短片段", 35, PLUM)
    text(d, 781, 419, "“上限 500 元”", 41, INK)
    text(d, 781, 482, "北京 / 职级 / 日期不在输入里", 32, RED)
    card(d, (746, 585, 1444, 840), TEAL_L, TEAL, 20)
    text(d, 780, 648, "完整条款片段", 35, TEAL)
    text(d, 781, 714, "北京 · A 职级 · 9 月 1 日起 · 500 元", 32, INK)
    text(d, 781, 792, "片段 ID → 原文、版本、生效区间", 31, TEAL)
    save(im, "embedding-chunk-evidence-v2.png")


def recall_audit():
    im, d = base("新版进了前三，旧版仍排第一", "案例评测 / Recall 与名次")
    text(d, 95, 260, "标注正例：新版 500 元", 39, TEAL)
    ranks = [("1", "旧版 450 元", RED, "不适用"),
             ("2", "新版 500 元", TEAL, "正例"),
             ("3", "异地条款", ORANGE, "不适用")]
    for i, (rank, name, col, tag) in enumerate(ranks):
        y = 361+i*142
        card(d, (102, y, 930, y+111), "white", LINE, 16)
        d.ellipse((126, y+25, 184, y+83), fill=col)
        text(d, 155, y+54, rank, 30, "white", "mm")
        text(d, 225, y+55, name, 38, INK, "lm")
        text(d, 883, y+55, tag, 31, col, "rm")
    d.line((975, 331, 975, 842), fill=LINE, width=3)
    text(d, 1033, 425, "Recall@1", 35, PLUM)
    text(d, 1365, 425, "0/1", 44, RED, "ra")
    text(d, 1033, 553, "Recall@3", 35, TEAL)
    text(d, 1365, 553, "1/1", 44, TEAL, "ra")
    text(d, 1033, 681, "单题 RR", 35, PLUM)
    text(d, 1365, 681, "1/2", 44, PLUM, "ra")
    save(im, "embedding-recall-audit-v2.png")


def pooling_choice():
    im, d = base("一个句子，怎样汇总成一个向量", "面试原理 / Sentence-BERT Pooling")
    words = [("[CLS]", PLUM_L), ("北京", TEAL_L), ("酒店", TEAL_L), ("上限", TEAL_L)]
    xs = [105, 430, 755, 1080]
    for x,(word,fill) in zip(xs,words):
        card(d,(x,280,x+270,360),fill,LINE,13)
        text(d,x+135,320,word,36,INK,"mm")
        arrow(d,(x+135,374),(x+135,451),TEAL,4)
        card(d,(x+40,469,x+230,545),"white",LINE,13)
        text(d,x+135,507,"h"+str(xs.index(x)),38,TEAL,"mm")
    d.line((240,570,240,635),fill=PLUM,width=5)
    arrow(d,(240,635),(475,746),PLUM)
    for x in (565,890,1215):
        d.line((x,570,x,628),fill=TEAL,width=4)
        arrow(d,(x,628),(1024,746),TEAL,4)
    card(d,(290,766,672,872),PLUM_L,PLUM,17)
    text(d,481,818,"取 [CLS] 位置",39,PLUM,"mm")
    card(d,(842,766,1380,872),TEAL_L,TEAL,17)
    text(d,1111,818,"平均各位置表示",39,TEAL,"mm")
    save(im,"embedding-pooling-choice-v2.png")


def encoder_variants():
    im, d = base("同为双塔，参数和输入约定不同", "面试比较 / SBERT · DPR · E5")
    rows=[
        (278,"SBERT","问句","条款","共享参数",TEAL,TEAL_L),
        (481,"DPR","问题","段落","参数独立",BLUE,"#E9F0F7"),
        (684,"E5","query: 问句","passage: 条款","共享参数 + 前缀",ORANGE,ORANGE_L),
    ]
    for y,model,left,right,note,col,fill in rows:
        card(d,(88,y,1448,y+171),"white",LINE,18)
        text(d,118,y+84,model,44,col,"lm")
        card(d,(330,y+35,644,y+135),fill,col,13)
        card(d,(768,y+35,1082,y+135),fill,col,13)
        text(d,487,y+85,left,33,INK,"mm")
        text(d,925,y+85,right,33,INK,"mm")
        text(d,707,y+85,"对照",29,col,"mm")
        text(d,1392,y+85,note,33,col,"rm")
    save(im,"embedding-encoder-variants-v2.png")


def metric_geometry():
    im, d = base("归一化之前，点积和余弦可能排反", "面试算例 / 相似度度量")
    # Exact toy vectors: q=(1,0), a=(0.8,0.6), b=(1.5,1.5).
    ox,oy=342,625
    d.line((112,oy,635,oy),fill=LINE,width=3)
    d.line((ox,860,ox,318),fill=LINE,width=3)
    arrow(d,(ox,oy),(ox+250,oy),BLUE,7)
    arrow(d,(ox,oy),(ox+200,oy-150),TEAL,7)
    arrow(d,(ox,oy),(ox+278,oy-278),ORANGE,7)
    text(d,608,oy+5,"q=(1,0)",34,BLUE)
    text(d,492,421,"A=(0.8,0.6)",31,TEAL)
    text(d,547,319,"B=(1.5,1.5)",31,ORANGE)
    d.arc((ox+54,oy-54,ox+204,oy+96), 275, 324, fill=TEAL,width=5)
    card(d,(742,299,1440,553),TEAL_L,TEAL,19)
    text(d,785,361,"按余弦看方向",38,TEAL)
    text(d,785,427,"A = 0.80  ＞  B ≈ 0.71",39,INK)
    text(d,785,493,"A 比 B 更接近查询方向",32,MUTED)
    card(d,(742,605,1440,859),ORANGE_L,ORANGE,19)
    text(d,785,667,"按点积还看长度",38,ORANGE)
    text(d,785,733,"B = 1.50  ＞  A = 0.80",39,INK)
    text(d,785,799,"B 的模长改变了排序",32,MUTED)
    save(im,"embedding-metric-geometry-v2.png")


def fragment_input():
    im, d = base("同一条款，模型可能只看到一部分", "面试诊断 / 实际编码输入")
    card(d,(87,274,1449,391),TEAL_L,TEAL,18)
    text(d,769,333,"原文：北京 · A 职级 · 9 月 1 日起 · 上限 500 元",39,INK,"mm")
    inputs=[
        (472,RED,"截断","北京 · A 职级 · 9 月 1 日起 · …","上限金额缺失"),
        (632,ORANGE,"片段太短","上限 500 元","适用条件缺失"),
        (792,TEAL,"保留条款","北京 · A 职级 · 9 月 1 日起 · 500 元","条件与金额齐全"),
    ]
    for y,col,label,seen,loss in inputs:
        card(d,(191,y,1428,y+114),"white",LINE,16)
        d.rectangle((214,y+20,224,y+94),fill=col)
        text(d,249,y+55,label,37,col,"lm")
        text(d,529,y+55,seen,33,INK,"lm")
        text(d,1390,y+55,loss,30,col,"rm")
    save(im,"embedding-fragment-input-v2.png")


def index_diagnostic():
    im, d = base("精确搜索有，近似搜索没有：查哪一步", "面试排障 / 固定语料与查询")
    text(d,99,267,"同一批向量 · 同一查询 · 同一过滤条件",37,INK)
    lists=[
        (91,PLUM,PLUM_L,"Flat 精确搜索",[("1","旧版 450"),("2","异地条款"),("3","新版 500")]),
        (820,TEAL,TEAL_L,"ANN 线上索引",[("1","旧版 450"),("2","异地条款"),("3","其他条款")]),
    ]
    for x,col,fill,title,items in lists:
        card(d,(x,342,x+622,793),"white",LINE,20)
        text(d,x+311,398,title,39,col,"mm")
        for i,(rank,name) in enumerate(items):
            yy=464+i*104
            highlight = name=="新版 500"
            card(d,(x+33,yy,x+588,yy+80),TEAL_L if highlight else fill,LINE,13)
            text(d,x+67,yy+40,rank,31,col,"mm")
            text(d,x+132,yy+40,name,36,TEAL if highlight else INK,"lm")
    arrow(d,(730,570),(802,570),ORANGE,6)
    text(d,770,861,"核查：索引新鲜度 · 搜索参数 · 过滤顺序",35,ORANGE,"ma")
    save(im,"embedding-index-diagnostic-v2.png")


if __name__ == "__main__":
    for draw in (vector_space, training_pairs, dual_encoder, chunk_evidence,
                 recall_audit, pooling_choice, encoder_variants, metric_geometry,
                 fragment_input, index_diagnostic):
        draw()
