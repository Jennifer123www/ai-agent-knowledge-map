"""Draw source-checked, mobile-readable teaching figures for reranking articles.

The diagrams deliberately distinguish model relevance from permission and policy
validity. Example ranks and scores are illustrative, never presented as measured
model output. See the paired prompts.md for sources and figure roles.
"""

from math import atan2, cos, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1] / "content/wechat/01-foundation-models-and-inference/submodules/04-reranker/assets"
FONT = next(str(p) for p in (
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
) if p.exists())
W, H = 1536, 1024
BG = "#FBF9F4"
INK = "#243039"
MUTED = "#647078"
LINE = "#D3D9D5"
TEAL = "#177C78"
TEAL_L = "#E5F1EE"
PLUM = "#815368"
PLUM_L = "#F2EAF0"
ORANGE = "#C96C37"
ORANGE_L = "#FFF0E3"
RED = "#B85C54"


def f(size):
    return ImageFont.truetype(FONT, size)


def txt(d, x, y, s, size=35, color=INK, anchor="la"):
    d.text((x, y), s, font=f(size), fill=color, anchor=anchor)


def rect(d, xy, fill="white", outline=LINE, radius=20, width=3):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def arr(d, a, b, color=TEAL, width=5, head=16):
    d.line((a, b), fill=color, width=width)
    ang = atan2(b[1]-a[1], b[0]-a[0])
    pts = [b, (b[0]-head*cos(ang)+9*sin(ang), b[1]-head*sin(ang)-9*cos(ang)),
           (b[0]-head*cos(ang)-9*sin(ang), b[1]-head*sin(ang)+9*cos(ang))]
    d.polygon(pts, fill=color)


def canvas(title, kicker):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    txt(d, 78, 65, kicker, 30, TEAL)
    txt(d, 78, 109, title, 57, INK)
    d.line((78, 191, 1458, 191), fill=LINE, width=2)
    return im, d


def save(im, name):
    ROOT.mkdir(parents=True, exist_ok=True)
    im.save(ROOT / name, optimize=True)


def document(d, x, y, title, lines, accent=TEAL, width=285):
    rect(d, (x, y, x+width, y+410), "#FFFFFF", LINE, 16)
    d.rectangle((x+16, y+19, x+24, y+75), fill=accent)
    txt(d, x+42, y+30, title, 37, INK)
    d.line((x+25, y+95, x+width-25, y+95), fill=LINE, width=2)
    for i, (field, value, marked) in enumerate(lines):
        yy = y+135+i*82
        txt(d, x+29, yy, field, 27, MUTED)
        txt(d, x+width-26, yy, value, 34, accent if marked else INK, "ra")
        if i < len(lines)-1:
            d.line((x+25, yy+54, x+width-25, yy+54), fill="#E9ECE9", width=2)


def case_evidence():
    im, d = canvas("四份条款：差别藏在限定条件里", "同题候选 / 案例证据")
    rect(d, (88, 225, 1448, 322), ORANGE_L, None, 17, 0)
    txt(d, 116, 263, "问：北京 · 四级 · 2026-09-15 · 住宿上限？", 42, INK)
    documents = [
        (100, "现行北京", [("地区", "北京", True), ("职级", "四级", True), ("版本", "现行", True)], TEAL),
        (447, "北京三级", [("地区", "北京", True), ("职级", "三级", False), ("版本", "现行", True)], PLUM),
        (794, "上海四级", [("地区", "上海", False), ("职级", "四级", True), ("版本", "现行", True)], ORANGE),
        (1141, "旧版北京", [("地区", "北京", True), ("职级", "四级", True), ("版本", "旧版", False)], RED),
    ]
    for x, title, rows, accent in documents:
        document(d, x, 390, title, rows, accent, 290)
    d.line((245, 824, 1285, 824), fill=LINE, width=3)
    for x, color, text in ((245, TEAL, "条件吻合"), (592, PLUM, "职级冲突"), (939, ORANGE, "地区冲突"), (1286, RED, "另核效期")):
        d.ellipse((x-12, 812, x+12, 836), fill=color)
        txt(d, x, 860, text, 34, color, "ma")
    save(im, "reranker-case-evidence-v3.png")


def two_stage():
    im, d = canvas("召回决定候选，重排只改变座次", "两阶段检索 / 排名变化")
    txt(d, 96, 251, "召回顺序", 39, PLUM)
    txt(d, 1120, 251, "逐对评分后", 39, TEAL)
    left = [("旧版北京四级", RED), ("北京三级", PLUM), ("现行北京四级", TEAL), ("上海四级", ORANGE)]
    right = [("现行北京四级", TEAL), ("北京三级", PLUM), ("旧版北京四级", RED), ("上海四级", ORANGE)]
    ys = [335, 473, 611, 749]
    for side, items in ((112, left), (1054, right)):
        for n, ((name, color), y) in enumerate(zip(items, ys), 1):
            rect(d, (side, y, side+363, y+103), "white", LINE, 15)
            d.ellipse((side+16, y+22, side+75, y+81), fill=color)
            txt(d, side+46, y+50, str(n), 33, "white", "mm")
            txt(d, side+92, y+53, name, 33, INK, "lm")
    txt(d, 760, 285, "交叉编码器逐对评分", 34, INK, "ma")
    for i, (src, dst, color) in enumerate(((0, 2, RED), (1, 1, PLUM), (2, 0, TEAL), (3, 3, ORANGE))):
        y1, y2 = ys[src]+52, ys[dst]+52
        d.line((488, y1, 566, y1, 986, y2, 1040, y2), fill=color, width=5, joint="curve")
        arr(d, (1017, y2), (1042, y2), color, 5, 12)
    save(im, "reranker-two-stage-v3.png")


def cross_encoder():
    im, d = canvas("交叉编码器：一对文本一起编码", "原理图 / BERT 段落重排序")
    txt(d, 90, 245, "联合输入", 36, PLUM)
    tokens = [("[CLS]", PLUM_L), ("北京", ORANGE_L), ("四级", ORANGE_L), ("[SEP]", PLUM_L),
              ("北京", TEAL_L), ("三级", TEAL_L), ("上限", TEAL_L), ("[SEP]", PLUM_L)]
    x = 90
    for token, fill in tokens:
        width = 164 if token.startswith("[") else 142
        rect(d, (x, 308, x+width, 381), fill, LINE, 12, 2)
        txt(d, x+width/2, 346, token, 35, INK, "mm")
        x += width+14
    # The grid depicts permitted cross-token interactions, not measured weights.
    txt(d, 90, 440, "跨段交互位置", 35, INK)
    q = ["北京", "四级"]
    p = ["北京", "三级", "上限"]
    for j, token in enumerate(p):
        txt(d, 340+j*155, 512, token, 34, TEAL, "ma")
    for i, token in enumerate(q):
        txt(d, 115, 592+i*111, token, 34, ORANGE)
        for j in range(3):
            xx, yy = 295+j*155, 570+i*111
            fill = TEAL_L if (i, j) == (0, 0) else ORANGE_L if (i, j) == (1, 1) else "#FFFFFF"
            rect(d, (xx, yy, xx+90, yy+68), fill, LINE, 10, 2)
            if (i, j) == (0, 0): txt(d, xx+45, yy+35, "同", 35, TEAL, "mm")
            if (i, j) == (1, 1): txt(d, xx+45, yy+35, "异", 35, ORANGE, "mm")
    arr(d, (726, 657), (815, 657), ORANGE)
    rect(d, (835, 520, 1160, 784), "white", TEAL, 20)
    txt(d, 997, 591, "BERT 编码层", 40, TEAL, "mm")
    for yy in (638, 680, 722):
        d.line((894, yy, 1101, yy), fill=TEAL if yy == 680 else LINE, width=9)
    arr(d, (1176, 657), (1248, 657), ORANGE)
    rect(d, (1261, 526, 1450, 783), ORANGE_L, ORANGE, 18)
    txt(d, 1355, 590, "[CLS]", 41, INK, "mm")
    txt(d, 1355, 658, "分类头", 37, INK, "mm")
    txt(d, 1355, 726, "相关分", 37, ORANGE, "mm")
    txt(d, 91, 855, "换一段候选 → 重新联合编码这一对", 35, PLUM)
    save(im, "reranker-cross-encoder-v3.png")


def validity_timeline():
    im, d = canvas("相关性高，也要核对生效时间", "业务边界 / 日期轴")
    txt(d, 96, 259, "旧版北京四级", 39, RED)
    txt(d, 96, 380, "现行北京四级", 39, TEAL)
    x0, split, x1 = 480, 914, 1400
    d.line((x0, 642, x1, 642), fill=INK, width=5)
    for x, value in ((x0, "过去"), (split, "版本切换"), (x1, "之后")):
        d.line((x, 626, x, 658), fill=INK, width=4)
        txt(d, x, 680, value, 33, MUTED, "ma")
    d.line((x0, 310, split, 310), fill=RED, width=34)
    d.ellipse((split-18, 292, split+18, 328), fill=RED)
    d.line((split, 430, x1, 430), fill=TEAL, width=34)
    d.ellipse((split-18, 412, split+18, 448), fill=TEAL)
    queryx = 1190
    d.line((queryx, 500, queryx, 808), fill=ORANGE, width=5)
    d.polygon([(queryx-17, 500), (queryx+17, 500), (queryx, 475)], fill=ORANGE)
    rect(d, (925, 750, 1430, 845), ORANGE_L, ORANGE, 15)
    txt(d, 1178, 798, "提问：2026-09-15", 38, INK, "mm")
    txt(d, 93, 855, "版本元数据可靠时，效期判断由规则完成", 35, PLUM)
    save(im, "reranker-validity-timeline-v3.png")


def k_cutoff():
    im, d = canvas("K 截在哪，决定正确条款能否入场", "候选规模 / 召回与计算")
    txt(d, 100, 271, "第一轮排序", 39, INK)
    names = [("旧版北京", RED), ("北京三级", PLUM), ("现行北京", TEAL), ("上海四级", ORANGE)]
    for i, (name, color) in enumerate(names):
        x = 205+i*308
        rect(d, (x, 363, x+267, 484), "white", LINE, 15)
        d.ellipse((x+15, 388, x+70, 443), fill=color)
        txt(d, x+43, 415, str(i+1), 30, "white", "mm")
        txt(d, x+78, 418, name, 32, INK, "lm")
        d.line((x+134, 505, x+134, 550), fill=color, width=5)
    for i, k in enumerate((1, 2, 3, 4)):
        x = 205+i*308
        rect(d, (x, 590, x+267, 781), TEAL_L if k>=3 else PLUM_L, LINE, 15)
        txt(d, x+133, 628, f"取前 {k} 段", 34, TEAL if k>=3 else PLUM, "mm")
        txt(d, x+133, 690, "包含现行条款" if k>=3 else "漏掉现行条款", 29, TEAL if k>=3 else RED, "mm")
        txt(d, x+133, 741, f"联合编码 {k} 次", 29, MUTED, "mm")
    save(im, "reranker-k-cutoff-v3.png")


def encoder_comparison():
    im, d = canvas("双塔能复用文档向量，交叉编码要逐对读", "面试对比 / 结构与成本")
    rect(d, (84, 252, 719, 820), "white", LINE, 22)
    rect(d, (817, 252, 1452, 820), "white", LINE, 22)
    txt(d, 400, 315, "双塔召回", 43, PLUM, "mm")
    txt(d, 1134, 315, "交叉编码重排", 43, TEAL, "mm")
    rect(d, (130, 410, 350, 495), ORANGE_L, ORANGE, 15)
    txt(d, 240, 452, "查询编码", 35, INK, "mm")
    rect(d, (130, 610, 350, 695), PLUM_L, PLUM, 15)
    txt(d, 240, 652, "文档预编码", 35, INK, "mm")
    arr(d, (365, 452), (558, 547), ORANGE)
    arr(d, (365, 652), (558, 559), PLUM)
    txt(d, 600, 558, "向量相似", 37, INK, "mm")
    txt(d, 399, 752, "文档向量可以复用", 35, PLUM, "mm")
    for i, name in enumerate(("候选甲", "候选乙", "候选丙")):
        yy = 408+i*118
        rect(d, (857, yy, 1170, yy+76), TEAL_L, TEAL, 12)
        txt(d, 1013, yy+38, "查询 + "+name, 34, INK, "mm")
        arr(d, (1184, yy+38), (1270, yy+38), ORANGE, 4, 13)
        txt(d, 1355, yy+38, "编码", 34, TEAL, "mm")
    txt(d, 1135, 752, "每个查询—候选对重算", 35, TEAL, "mm")
    save(im, "reranker-encoder-comparison-v3.png")


def threshold_shift():
    im, d = canvas("模型一升级，旧阈值不能照搬", "面试诊断 / 分数校准")
    txt(d, 90, 262, "同一组标注样本", 38, INK)
    txt(d, 620, 262, "模型 A", 36, PLUM, "ma")
    txt(d, 1157, 262, "模型 B", 36, TEAL, "ma")
    # Pedagogical scores; factual qualifier belongs in the article caption.
    candidates = [("相关甲", TEAL, .83, .61), ("相关乙", TEAL, .75, .55),
                  ("无关丙", RED, .36, .30), ("无关丁", RED, .28, .22)]
    for i, (name, col, a, b) in enumerate(candidates):
        yy = 390+i*120
        rect(d, (96, yy-23, 338, yy+59), "white", LINE, 12)
        d.ellipse((110, yy-4, 149, yy+35), fill=col)
        txt(d, 170, yy+16, name, 35, INK, "lm")
        for x0, score in ((453, a), (989, b)):
            d.line((x0, yy+19, x0+390, yy+19), fill=LINE, width=12)
            cx = x0+390*score
            d.ellipse((cx-15, yy+4, cx+15, yy+34), fill=col)
            txt(d, cx, yy-17, f"{score:.2f}", 31, col, "ma")
    for x0 in (453, 989):
        xx = x0+390*.7
        d.line((xx, 333, xx, 823), fill=ORANGE, width=4)
    txt(d, 655, 890, "A 的阈值 0.70", 33, ORANGE, "ma")
    txt(d, 1189, 890, "照搬 0.70 会漏掉相关样本", 32, ORANGE, "ma")
    save(im, "reranker-threshold-shift-v3.png")


def metric_lanes():
    im, d = canvas("RR 看首个相关结果，NDCG 看整列顺序", "面试算例 / 排名指标")
    txt(d, 331, 284, "原顺序", 40, PLUM, "ma")
    txt(d, 1168, 284, "重排后", 40, TEAL, "ma")
    rows = [("三级条款", 0), ("现行四级", 3), ("例外条款", 2), ("异地条款", 0)]
    new = [("现行四级", 3), ("例外条款", 2), ("三级条款", 0), ("异地条款", 0)]
    for x, items in ((98, rows), (885, new)):
        for i, (name, rel) in enumerate(items):
            yy = 341+i*109
            color = TEAL if rel==3 else ORANGE if rel==2 else MUTED
            rect(d, (x, yy, x+551, yy+87), TEAL_L if rel==3 else ORANGE_L if rel==2 else "white", LINE, 14)
            txt(d, x+42, yy+43, str(i+1), 34, color, "mm")
            txt(d, x+93, yy+43, name, 36, INK, "lm")
            txt(d, x+515, yy+43, f"等级 {rel}", 32, color, "rm")
    arr(d, (676, 568), (855, 568), ORANGE, 6)
    txt(d, 373, 862, "首个充分相关在第 2 位 → RR = 1/2", 33, PLUM, "ma")
    txt(d, 1170, 862, "首个充分相关在第 1 位 → RR = 1", 33, TEAL, "ma")
    save(im, "reranker-metric-lanes-v3.png")


def learning_signals():
    im, d = canvas("同一组候选，可给三种训练信号", "面试原理 / 排序学习")
    txt(d, 90, 261, "固定查询：北京四级住宿上限？", 38, INK)
    columns = [
        (93, "Pointwise · 点式", PLUM, PLUM_L),
        (575, "Pairwise · 成对", TEAL, TEAL_L),
        (1057, "Listwise · 列表", ORANGE, ORANGE_L),
    ]
    for x, title, color, fill in columns:
        rect(d, (x, 340, x+385, 837), "white", LINE, 20)
        txt(d, x+192, 400, title, 36, color, "mm")
        d.line((x+28, 445, x+357, 445), fill=LINE, width=2)
    x=93
    for i, (name, grade) in enumerate((("现行四级", "3"), ("例外条款", "2"), ("异地条款", "0"))):
        yy=480+i*101
        rect(d, (x+23, yy, x+361, yy+70), PLUM_L, LINE, 11)
        txt(d, x+47, yy+35, name, 31, INK, "lm")
        txt(d, x+338, yy+35, "等级 "+grade, 29, PLUM, "rm")
    x=575
    rect(d, (x+33, 496, x+352, 582), TEAL_L, TEAL, 12)
    rect(d, (x+33, 661, x+352, 747), "white", LINE, 12)
    txt(d, x+192, 540, "现行四级", 34, TEAL, "mm")
    txt(d, x+192, 704, "异地条款", 34, INK, "mm")
    arr(d, (x+192, 649), (x+192, 593), TEAL, 6)
    txt(d, x+342, 622, "应排在前", 27, TEAL, "ra")
    x=1057
    for i, (name, color) in enumerate((("1 现行四级", TEAL), ("2 例外条款", ORANGE), ("3 异地条款", MUTED))):
        yy=490+i*109
        rect(d, (x+35, yy, x+350, yy+76), ORANGE_L if i==0 else "white", LINE, 11)
        txt(d, x+192, yy+38, name, 32, color, "mm")
    save(im, "reranker-learning-signals-v3.png")


def condition_perturbation():
    im, d = canvas("一次只换一项，检验排序器读没读到条件", "面试诊断 / 输入扰动")
    rect(d, (91, 233, 1445, 372), "white", LINE, 19)
    txt(d, 125, 270, "固定候选", 33, PLUM)
    txt(d, 399, 269, "北京 · 四级员工 · 住宿上限", 39, INK)
    d.line((93, 420, 1442, 420), fill=LINE, width=2)
    rows = [
        (473, "基准", "北京四级，住宿上限？", "标注：条件吻合", TEAL_L, TEAL),
        (624, "只换地区", "上海四级，住宿上限？", "标注：地区不符", PLUM_L, PLUM),
        (775, "只改写问法", "北京四级，每晚限额？", "标注：仍应吻合", ORANGE_L, ORANGE),
    ]
    for y, tag, query, expected, fill, accent in rows:
        rect(d, (93, y, 1443, y+116), "white", LINE, 16)
        rect(d, (110, y+18, 342, y+98), fill, None, 11, 0)
        txt(d, 226, y+58, tag, 34, accent, "mm")
        txt(d, 376, y+58, query, 36, INK, "lm")
        txt(d, 1387, y+58, expected, 32, accent, "rm")
    save(im, "reranker-condition-perturbation.png")


def input_window():
    im, d = canvas("条款后半段被截掉，分数就只评价前半段", "面试诊断 / 输入范围")
    txt(d, 91, 239, "完整制度的四个位置", 34, MUTED)
    parts = [(93, "标题", PLUM_L, PLUM), (432, "适用条件", TEAL_L, TEAL),
             (771, "基础标准", ORANGE_L, ORANGE), (1110, "例外审批", PLUM_L, PLUM)]
    for x, name, fill, accent in parts:
        rect(d, (x, 307, x+303, 414), fill, accent, 15)
        txt(d, x+151, 360, name, 37, accent, "mm")
    txt(d, 93, 483, "同一查询 + 同一输入长度上限", 33, INK)
    rect(d, (93, 555, 1443, 694), "white", LINE, 17)
    txt(d, 124, 598, "只保留开头", 35, PLUM)
    txt(d, 476, 598, "标题 · 条件 · 基础标准", 36, INK)
    txt(d, 1399, 599, "例外没进入模型", 32, RED, "rm")
    rect(d, (93, 741, 1443, 880), "white", LINE, 17)
    txt(d, 124, 784, "按条件选窗口", 35, TEAL)
    txt(d, 476, 784, "条件 · 基础标准 · 例外审批", 36, INK)
    txt(d, 1399, 785, "保留限制条件", 32, TEAL, "rm")
    save(im, "reranker-input-window.png")


if __name__ == "__main__":
    for renderer in (case_evidence, two_stage, cross_encoder, validity_timeline,
                     k_cutoff, encoder_comparison, threshold_shift,
                     metric_lanes, learning_signals, condition_perturbation,
                     input_window):
        renderer()
