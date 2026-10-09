"""Render corrected auxiliary diagrams for the foundation-model WeChat series.

The PNGs are publishable assets. Keep all labels and arrows deterministic so a
future edit cannot silently reintroduce a misleading model relationship.
"""

from math import atan2, cos, sin
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1] / "content/wechat/01-foundation-models-and-inference"
FONT_CANDIDATES = [
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
]
FONT_PATH = next((str(path) for path in FONT_CANDIDATES if path.exists()), None)
if FONT_PATH is None:
    raise RuntimeError("Chinese font not found")

W, H = 1536, 1024
PAPER, INK, MUTED = "#FBF8F3", "#273941", "#65757A"
PLUM, PLUM_PALE = "#774660", "#F1E7EC"
TEAL, TEAL_PALE = "#147B7A", "#E2F0ED"
ORANGE, ORANGE_PALE = "#CE8847", "#FBF0E4"
OUTLINE = "#D0DBD8"


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def label(draw, xy, value, size=30, color=INK, anchor=None):
    draw.text(xy, value, font=font(size), fill=color, anchor=anchor)


def box(draw, bounds, value, fill="#FFFFFF", size=31, color=INK):
    draw.rounded_rectangle(bounds, radius=22, fill=fill, outline=OUTLINE, width=3)
    x0, y0, x1, y1 = bounds
    label(draw, ((x0+x1)//2, (y0+y1)//2), value, size, color, "mm")


def arrow(draw, start, end, color=TEAL, width=6):
    x1, y1 = start
    x2, y2 = end
    draw.line((start, end), fill=color, width=width)
    angle = atan2(y2-y1, x2-x1)
    size = 17
    wing = 10
    points = [
        (x2, y2),
        (x2-size*cos(angle)+wing*sin(angle), y2-size*sin(angle)-wing*cos(angle)),
        (x2-size*cos(angle)-wing*sin(angle), y2-size*sin(angle)+wing*cos(angle)),
    ]
    draw.polygon(points, fill=color)


def base(title, subtitle, category, footnote):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    # Keep the outer margin plain; a full-height decorative stripe adds no information.
    label(d, (88, 80), category, 27, PLUM)
    label(d, (88, 131), title, 59)
    label(d, (90, 228), subtitle, 30, MUTED)
    d.line((88, 282, 1450, 282), fill=OUTLINE, width=3)
    if footnote:
        d.line((88, 894, 1450, 894), fill=OUTLINE, width=2)
        label(d, (91, 925), footnote, 27, MUTED)
    return im, d


def save(im, relative):
    path = ROOT / relative
    paper_rgb = Image.new("RGB", (1, 1), PAPER).getpixel((0, 0))
    left_margin = im.crop((0, 0, 60, H))
    if left_margin.getextrema() != tuple((channel, channel) for channel in paper_rgb):
        raise ValueError(f"Decorative mark in the left margin: {relative}")
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, optimize=True)


def foundation_receipt_case():
    im, d = base(
        "先把票据上的三个字段看清楚",
        "练习场景：只整理可回看原图的草稿，不做报销审批",
        "场景复现",
        "",
    )
    d.rounded_rectangle((100, 350, 735, 850), radius=28, fill="#FFFFFF", outline=OUTLINE, width=3)
    label(d, (145, 413), "住宿票据", 44, PLUM)
    d.line((145, 478, 685, 478), fill=OUTLINE, width=3)
    for y, name, value in (
        (530, "住宿日期", "2026 年 9 月 15 日"),
        (628, "住宿地点", "北京"),
        (726, "票面金额", "480.00 元"),
    ):
        label(d, (145, y), name, 32, MUTED, "lm")
        label(d, (685, y), value, 35, INK, "rm")
        d.line((145, y+44, 685, y+44), fill=OUTLINE, width=2)
    arrow(d, (760, 602), (850, 602), ORANGE)
    d.rounded_rectangle((865, 360, 1440, 835), radius=28, fill=TEAL_PALE, outline=OUTLINE, width=3)
    label(d, (905, 425), "待核对的字段草稿", 42, TEAL)
    for y, value in (
        (530, "金额：480 元  ←  票面"),
        (622, "日期：9 月 15 日  ←  票面"),
        (714, "职级：A  ←  员工自述"),
    ):
        label(d, (905, y), value, 31, INK, "lm")
    label(d, (905, 787), "状态：未提交", 34, PLUM, "lm")
    save(im, "assets/foundation-receipt-case.png")


def foundation_role_boundary():
    im, d = base(
        "四种在线能力，一种离线改进",
        "模型适配不在每笔请求后现场训练；规则校验也不是模型输出",
        "能力分工",
        "",
    )
    stages = (
        (95, "多模态", "图片 → 字段候选", PLUM_PALE, PLUM),
        (462, "向量嵌入", "问题 → 召回候选", TEAL_PALE, TEAL),
        (829, "重排序", "候选 → 阅读顺序", ORANGE_PALE, ORANGE),
        (1196, "语言模型", "证据 → 草稿说明", PLUM_PALE, PLUM),
    )
    for x, name, detail, fill, color in stages:
        d.rounded_rectangle((x, 375, x+245, 582), radius=24, fill=fill, outline=OUTLINE, width=3)
        label(d, (x+123, 438), name, 33, color, "mm")
        label(d, (x+123, 514), detail, 23, INK, "mm")
    for x in (352, 719, 1086):
        arrow(d, (x, 482), (x+97, 482), ORANGE, 5)
    d.rounded_rectangle((95, 625, 1441, 716), radius=20, fill="#FFFFFF", outline=OUTLINE, width=3)
    label(d, (768, 670), "规则与业务系统：生效日期 · 身份 · 格式 · 动作权限", 31, INK, "mm")
    d.rounded_rectangle((225, 760, 1311, 867), radius=22, fill=TEAL_PALE, outline=OUTLINE, width=3)
    label(d, (768, 813), "模型适配：根据积累的失败样本调整提示、数据或模型", 31, TEAL, "mm")
    save(im, "assets/foundation-role-boundary.png")


def foundation_rag_case():
    im, d = base(
        "相关条款先找来，适用条件再核对",
        "旧版 450 元与新版 500 元都可能被检索到；排序第一不等于有效",
        "证据路径",
        "",
    )
    box(d, (90, 360, 405, 505), "问题与查询编码", PLUM_PALE, 31)
    box(d, (90, 675, 405, 820), "制度原文与索引", TEAL_PALE, 31)
    box(d, (515, 437, 820, 743), "", ORANGE_PALE)
    label(d, (668, 490), "召回候选", 38, ORANGE, "mm")
    label(d, (668, 565), "旧版 450 元", 30, INK, "mm")
    label(d, (668, 635), "新版 500 元", 30, INK, "mm")
    box(d, (920, 445, 1160, 735), "", TEAL_PALE)
    label(d, (1040, 515), "核适用", 36, TEAL, "mm")
    label(d, (1040, 590), "日期 · 职级", 26, INK, "mm")
    label(d, (1040, 650), "权限 · 版本", 26, INK, "mm")
    box(d, (1270, 474, 1448, 703), "", PLUM_PALE)
    label(d, (1359, 545), "生成", 34, PLUM, "mm")
    label(d, (1359, 615), "草稿", 31, INK, "mm")
    arrow(d, (415, 435), (504, 535), PLUM)
    arrow(d, (415, 745), (504, 645), TEAL)
    arrow(d, (832, 589), (909, 589), ORANGE)
    arrow(d, (1172, 589), (1259, 589), TEAL)
    save(im, "assets/foundation-rag-case.png")


def foundation_route_matrix():
    im, d = base(
        "问题不同，调用的能力也不同",
        "按输入、证据需求和动作风险选路径，不让所有请求排同一条队",
        "按需路由",
        "",
    )
    rows = (
        (365, "问报销入口", "查入口资料 → 回答", "不读票据", PLUM_PALE),
        (540, "只抄住宿日期", "看图 → 字段候选", "不判断可报", TEAL_PALE),
        (715, "生成报销草稿", "看图 → 查制度 → 核适用 → 草稿", "不调用提交", ORANGE_PALE),
    )
    for y, task, path, boundary, fill in rows:
        d.rounded_rectangle((95, y, 1440, y+138), radius=22, fill=fill, outline=OUTLINE, width=3)
        label(d, (125, y+70), task, 35, INK, "lm")
        label(d, (528, y+70), path, 31, INK, "lm")
        label(d, (1400, y+70), boundary, 30, PLUM, "rm")
    save(im, "assets/foundation-route-matrix.png")


def foundation_release_checks():
    im, d = base(
        "一张成功样张，证明不了整条链",
        "上线前把读图、找规、适用性和动作边界分别验收",
        "评测与发布",
        "",
    )
    cases = (
        (92, "读图", "反光时 480 会不会读成 430？", PLUM_PALE),
        (448, "召回", "新版 500 元是否进入候选？", TEAL_PALE),
        (804, "适用", "9 月 15 日是否用对生效版本？", ORANGE_PALE),
        (1160, "动作", "用户只要草稿，有没有误提交？", PLUM_PALE),
    )
    for x, name, question, fill in cases:
        d.rounded_rectangle((x, 390, x+280, 670), radius=23, fill=fill, outline=OUTLINE, width=3)
        label(d, (x+140, 458), name, 38, PLUM, "mm")
        first, second = question[:10], question[10:]
        label(d, (x+140, 550), first, 25, INK, "mm")
        label(d, (x+140, 595), second, 25, INK, "mm")
    d.rounded_rectangle((255, 750, 1280, 860), radius=22, fill="#FFFFFF", outline=OUTLINE, width=3)
    label(d, (767, 805), "发布记录：图像模型 + 索引快照 + 排序器 + 提示 + 规则", 30, TEAL, "mm")
    save(im, "assets/foundation-release-checks.png")


def foundation_answer_contract():
    im, d = base(
        "“可以报”至少要拆成四个前提",
        "每个关键字段带出处；没有证据的条件保持待核对",
        "面试答题",
        "",
    )
    evidence = (
        (105, "金额 480", "票面区域", PLUM_PALE),
        (463, "A 职级", "身份系统", TEAL_PALE),
        (821, "上限 500", "有效制度", ORANGE_PALE),
        (1179, "草稿状态", "工具回执", PLUM_PALE),
    )
    for x, claim, source, fill in evidence:
        d.rounded_rectangle((x, 410, x+255, 655), radius=23, fill=fill, outline=OUTLINE, width=3)
        label(d, (x+128, 475), claim, 32, INK, "mm")
        label(d, (x+128, 585), source, 30, TEAL, "mm")
        d.line((x+35, 530, x+220, 530), fill=OUTLINE, width=3)
    d.rounded_rectangle((350, 745, 1185, 850), radius=22, fill="#FFFFFF", outline=OUTLINE, width=3)
    label(d, (767, 795), "只证实金额未超上限 ≠ 整单审批通过", 34, PLUM, "mm")
    save(im, "assets/foundation-answer-contract.png")


def foundation_eval_board():
    im, d = base(
        "分段找错，整件任务验收",
        "同一批标注样本既看组件表现，也看最终草稿是否可信",
        "面试评测",
        "",
    )
    rows = (
        (365, "读图", "金额、日期与原图是否一致", PLUM_PALE),
        (480, "检索", "正确条款是否进入候选", TEAL_PALE),
        (595, "适用", "制度版本、日期与职级是否吻合", ORANGE_PALE),
        (710, "端到端", "正确草稿率、误提交数、人工接管率", PLUM_PALE),
    )
    for y, name, measure, fill in rows:
        d.rounded_rectangle((105, y, 1430, y+88), radius=18, fill=fill, outline=OUTLINE, width=2)
        label(d, (145, y+44), name, 31, PLUM, "lm")
        label(d, (425, y+44), measure, 30, INK, "lm")
    save(im, "assets/foundation-eval-board.png")


def foundation_debug_trace():
    im, d = base(
        "又答成 450 元，先查新版在哪一站丢了",
        "同一任务标识串起索引、过滤、排序、上下文与草稿",
        "故障定位",
        "",
    )
    checks = (
        (98, "① 索引", "新版已入库？", PLUM_PALE),
        (430, "② 过滤", "日期与权限挡住了？", TEAL_PALE),
        (762, "③ 排序", "新版排到哪里？", ORANGE_PALE),
        (1094, "④ 生成", "证据给了却没用？", PLUM_PALE),
    )
    for x, name, question, fill in checks:
        d.rounded_rectangle((x, 445, x+285, 680), radius=24, fill=fill, outline=OUTLINE, width=3)
        label(d, (x+143, 505), name, 32, PLUM, "mm")
        label(d, (x+143, 597), question, 25, INK, "mm")
    for x in (392, 724, 1056):
        arrow(d, (x, 560), (x+28, 560), ORANGE, 5)
    d.rounded_rectangle((280, 765, 1250, 860), radius=22, fill="#FFFFFF", outline=OUTLINE, width=3)
    label(d, (765, 810), "每一步都保留输入、输出和版本；不能只看最后一句错答", 30, TEAL, "mm")
    save(im, "assets/foundation-debug-trace.png")


def embedding_chunking():
    im, d = base(
        "版本条件也得跟着条款入库",
        "只存“上限 500 元”，会丢掉地区、职级和生效日期",
        "建索引",
        "",
    )
    d.rounded_rectangle((90, 365, 475, 670), radius=22, fill="#FFFFFF", outline=OUTLINE, width=3)
    label(d, (122, 423), "制度原文", 37, PLUM)
    label(d, (122, 485), "北京 · A 职级", 38)
    label(d, (122, 545), "9 月 1 日起", 38)
    label(d, (122, 605), "上限 500 元", 38)
    d.rounded_rectangle((570, 400, 955, 635), radius=22, fill=TEAL_PALE, outline=OUTLINE, width=3)
    label(d, (602, 468), "按条款切片", 39, TEAL)
    label(d, (602, 536), "四项条件保留完整", 34)
    d.rounded_rectangle((1050, 400, 1445, 635), radius=22, fill=ORANGE_PALE, outline=OUTLINE, width=3)
    label(d, (1082, 468), "嵌入模型", 39, ORANGE)
    label(d, (1082, 536), "向量 + 片段 ID", 34)
    arrow(d, (486, 518), (559, 518), ORANGE)
    arrow(d, (966, 518), (1039, 518), ORANGE)
    d.rounded_rectangle((310, 730, 1230, 845), radius=22, fill="#FFFFFF", outline=OUTLINE, width=3)
    label(d, (345, 790), "片段 ID 还能找到原文、版本和适用范围", 37, INK, "lm")
    arrow(d, (1200, 640), (1200, 716), TEAL)
    save(im, "submodules/03-embedding/assets/embedding-chunking.png")


def embedding_evaluation():
    im, d = base(
        "旧版排第一，召回率仍可能是满分",
        "同一道题：前三名里有新版，但旧版在它前面",
        "案例评测",
        "",
    )
    d.rounded_rectangle((90, 340, 735, 475), radius=22, fill="#FFFFFF", outline=OUTLINE, width=3)
    label(d, (122, 386), "测试问题", 31, PLUM)
    label(d, (122, 438), "北京 · A 职级 · 2026 年 9 月 15 日", 31)
    label(d, (90, 535), "检索前 3 名", 38, INK)
    ranked = [
        (570, "1  旧版 450 元", "日期不适用", PLUM_PALE, PLUM),
        (690, "2  新版 500 元", "本题正例", TEAL_PALE, TEAL),
        (810, "3  异地住宿条款", "地区不适用", ORANGE_PALE, ORANGE),
    ]
    for y, result, status, fill, color in ranked:
        d.rounded_rectangle((90, y, 735, y+94), radius=18, fill=fill, outline=OUTLINE, width=2)
        label(d, (120, y+47), result, 38, INK, "lm")
        label(d, (705, y+47), status, 28, color, "rm")
    d.rounded_rectangle((850, 370, 1445, 545), radius=24, fill="#FFFFFF", outline=OUTLINE, width=3)
    label(d, (885, 420), "人工标注的正例", 31, PLUM)
    label(d, (885, 492), "新版 500 元", 46, TEAL)
    d.rounded_rectangle((850, 615, 1445, 850), radius=24, fill=ORANGE_PALE, outline=OUTLINE, width=3)
    label(d, (885, 682), "Recall@3 = 1 / 1", 46, TEAL)
    label(d, (885, 746), "正确条款进了前三名", 31, INK)
    label(d, (885, 805), "但第一名仍是旧版", 31, PLUM)
    save(im, "submodules/03-embedding/assets/embedding-evaluation.png")


def reranker_two_stage():
    im, d = base(
        "先找候选，再细读排序",
        "重排序只改候选的先后，不负责从全集里找回漏掉的条款",
        "两阶段检索",
        "排序仅作示意；是否生效仍须规则校验，图中没有实测分数",
    )
    box(d, (90, 359, 440, 782), "", "#FFFFFF")
    box(d, (556, 478, 906, 658), "问题 + 候选\n逐对比较", PLUM_PALE)
    box(d, (1020, 359, 1444, 782), "", TEAL_PALE)
    label(d, (265, 404), "召回候选", 34, PLUM, "mm")
    for i, s in enumerate(("旧版北京条款", "新版北京条款", "异地住宿条款")):
        label(d, (130, 485+i*84), s, 29)
    label(d, (1230, 404), "重排后的前列", 34, TEAL, "mm")
    for i, s in enumerate(("1  新版北京条款", "2  旧版北京条款", "3  异地住宿条款")):
        label(d, (1063, 485+i*84), s, 28)
    arrow(d, (450, 570), (545, 570), ORANGE)
    arrow(d, (917, 570), (1009, 570), ORANGE)
    label(d, (729, 711), "只在已召回的集合内排序", 26, MUTED, "mm")
    save(im, "submodules/04-reranker/assets/reranker-two-stage.png")


def reranker_evaluation():
    im, d = base(
        "重排序怎样验收",
        "用同一组已标注问题，对照基线与新排序模型",
        "排序评测",
        "不画没有数据来源的上升曲线；质量和代价须分别报告",
    )
    box(d, (92, 368, 514, 505), "问题 + 相关性标注", "#FFFFFF", 28)
    box(d, (648, 345, 1028, 470), "基线排序", PLUM_PALE)
    box(d, (648, 565, 1028, 690), "新重排序", TEAL_PALE)
    box(d, (1152, 432, 1444, 602), "对照结果", ORANGE_PALE)
    arrow(d, (525, 435), (637, 408), ORANGE)
    arrow(d, (525, 435), (637, 625), ORANGE)
    arrow(d, (1039, 407), (1141, 485), ORANGE)
    arrow(d, (1039, 627), (1141, 550), ORANGE)
    label(d, (163, 649), "质量：MRR、NDCG", 31, TEAL)
    label(d, (163, 706), "代价：p95 时延、调用成本", 31, PLUM)
    label(d, (164, 788), "先定题集和基线，再谈是否改善", 28, MUTED)
    save(im, "submodules/04-reranker/assets/reranker-evaluation.png")


def llm_sampling():
    im, d = base(
        "下一个 token 怎样被选出",
        "温度调整概率分布；Top-p 缩小候选范围；两者可以组合",
        "生成参数",
        "参数影响随机性与候选范围，不会替模型核实事实",
    )
    items = [
        ((90, 392, 353, 591), "候选分数", "模型给出"),
        ((433, 392, 696, 591), "温度", "调整分布"),
        ((776, 392, 1039, 591), "Top-p", "保留候选"),
        ((1119, 392, 1444, 591), "抽样输出", "下一个 token"),
    ]
    for bounds, head, detail in items:
        d.rounded_rectangle(bounds, radius=22, fill=TEAL_PALE if head == "温度" else PLUM_PALE if head == "Top-p" else "#FFFFFF", outline=OUTLINE, width=3)
        x0, y0, x1, y1 = bounds
        label(d, ((x0+x1)//2, y0+72), head, 37, INK, "mm")
        label(d, ((x0+x1)//2, y0+138), detail, 28, MUTED, "mm")
    for a, b in [((364, 490), (422, 490)), ((707, 490), (765, 490)),
                 ((1050, 490), (1108, 490))]:
        arrow(d, a, b, ORANGE)
    box(d, (283, 708, 1248, 808), "可单独设置，也可同时设置；具体实现顺序以推理系统为准", "#FFFFFF", 27)
    save(im, "submodules/01-llm/assets/llm-sampling.png")


def llm_evidence_audit():
    im, d = base(
        "这句话，输入里有依据吗？",
        "把通知拆成事实陈述，再逐条决定保留、改写或删除",
        "事实核对",
        "核对单位是每一条事实陈述，不是整段文字读起来是否顺畅",
    )

    columns = (92, 610, 1120, 1444)
    header_y0, header_y1 = 338, 408
    d.rounded_rectangle(
        (columns[0], header_y0, columns[-1], header_y1),
        radius=18,
        fill=INK,
    )
    for x, text in (
        ((columns[0] + columns[1]) // 2, "模型写出的内容"),
        ((columns[1] + columns[2]) // 2, "输入中的依据"),
        ((columns[2] + columns[3]) // 2, "判断"),
    ):
        label(d, (x, (header_y0 + header_y1) // 2), text, 27, "#FFFFFF", "mm")

    rows = [
        ("改至 16:00—17:00", "最新要求：16:00—17:00", "保留", TEAL_PALE, TEAL),
        ("地点仍为 A302", "A302 只在旧日程中", "删除", PLUM_PALE, PLUM),
        ("会议链接稍后补充", "链接尚未生成", "保留", TEAL_PALE, TEAL),
        ("邀请已发出", "没有发送结果", "禁止写入", ORANGE_PALE, ORANGE),
    ]
    row_h = 86
    y = 423
    for statement, evidence, decision, fill, decision_color in rows:
        d.rounded_rectangle(
            (columns[0], y, columns[-1], y + row_h),
            radius=16,
            fill="#FFFFFF",
            outline=OUTLINE,
            width=2,
        )
        d.line((columns[1], y + 10, columns[1], y + row_h - 10), fill=OUTLINE, width=2)
        d.line((columns[2], y + 10, columns[2], y + row_h - 10), fill=OUTLINE, width=2)
        label(d, (118, y + row_h // 2), statement, 28, INK, "lm")
        label(d, (641, y + row_h // 2), evidence, 27, MUTED, "lm")
        chip = (1172, y + 18, 1388, y + row_h - 18)
        d.rounded_rectangle(chip, radius=22, fill=fill, outline=decision_color, width=2)
        label(d, ((chip[0] + chip[2]) // 2, (chip[1] + chip[3]) // 2), decision, 26, decision_color, "mm")
        y += row_h + 12

    d.rounded_rectangle((300, 820, 1236, 878), radius=20, fill=ORANGE_PALE)
    label(d, (768, 849), "流畅度看语言；事实是否成立，要看证据", 29, PLUM, "mm")
    save(im, "submodules/01-llm/assets/llm-evidence-audit.png")


def llm_context_conflict():
    im, d = base(
        "旧日程与新要求怎样避免串线",
        "先按来源和时间整理事实，再让模型只改动已经确认的字段",
        "上下文冲突",
        "上下文装得下两份记录，不代表模型会自动选对较新的那一份",
    )
    box(d, (90, 360, 430, 510), "旧日程\n14:00 · A302", PLUM_PALE, 29)
    box(d, (90, 625, 430, 775), "新要求\n16:00 · 线上", TEAL_PALE, 29)
    box(d, (575, 460, 955, 675), "按时间、来源和指令\n整理有效字段", "#FFFFFF", 30)
    box(d, (1100, 360, 1445, 510), "保留\n16:00 · 线上", TEAL_PALE, 29)
    box(d, (1100, 625, 1445, 775), "待补\n会议链接", ORANGE_PALE, 29)
    arrow(d, (441, 435), (564, 525), PLUM)
    arrow(d, (441, 700), (564, 610), TEAL)
    arrow(d, (966, 525), (1089, 435), TEAL)
    arrow(d, (966, 610), (1089, 700), ORANGE)
    label(d, (764, 745), "没有发送回执，就不写“邀请已发出”", 27, PLUM, "mm")
    save(im, "submodules/01-llm/assets/llm-context-conflict.png")


def multimodal_field_trace():
    im, d = base(
        "三个读数，怎样对应三个字段",
        "从原图位置逐项连到识别字符和字段草稿，缺失的年份保持未知",
        "字段溯源",
        "A / B / C 是图中区域标记，不是实测坐标；草稿仍须回到原图复核",
    )
    for x, heading in ((90, "发票原图（示意）"), (535, "字符与区域"), (1015, "字段草稿")):
        label(d, (x, 347), heading, 30, PLUM)

    rows = [
        (474, "A", "含税金额", "680.00", "含税金额 = 680.00", "可核对", TEAL_PALE),
        (604, "B", "税额", "38.49", "税额 = 38.49", "可核对", TEAL_PALE),
        (734, "C", "开票日期", "9/3", "开票日期 = 9/3", "年份未知", ORANGE_PALE),
    ]
    for y, region, source_label, value, field_value, status, fill in rows:
        d.rounded_rectangle((90, y-55, 445, y+55), radius=18, fill="#FFFFFF", outline=OUTLINE, width=3)
        d.rounded_rectangle((110, y-39, 152, y+3), radius=12, fill=PLUM_PALE)
        label(d, (131, y-18), region, 23, PLUM, "mm")
        label(d, (168, y-18), source_label, 27, INK, "lm")
        label(d, (168, y+22), value, 30, INK, "lm")

        d.rounded_rectangle((535, y-55, 925, y+55), radius=18, fill=PLUM_PALE, outline=OUTLINE, width=3)
        label(d, (562, y-18), f"区域 {region}  →  {value}", 29, INK, "lm")
        label(d, (562, y+24), "保留来源位置", 24, MUTED, "lm")

        d.rounded_rectangle((1015, y-55, 1445, y+55), radius=18, fill=fill, outline=OUTLINE, width=3)
        label(d, (1042, y-18), field_value, 28, INK, "lm")
        label(d, (1042, y+24), status, 24, TEAL if status == "可核对" else PLUM, "lm")

        arrow(d, (456, y), (524, y), ORANGE)
        arrow(d, (936, y), (1004, y), ORANGE)

    label(d, (768, 843), "读出字符只是第一步；标签、位置和缺项状态必须一并保存", 27, MUTED, "mm")
    save(im, "submodules/02-multimodal/assets/multimodal-field-trace.png")


def embedding_metric_comparison():
    im, d = base(
        "单位向量：三种度量怎样连起来",
        "看同一个查询与两份候选；先确认向量是否归一化",
        "距离度量",
        "",
    )
    center = (340, 670)
    radius = 240
    d.ellipse((center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius),
              outline=OUTLINE, width=3)
    label(d, (106, 359), "同一单位圆上的 q、d1、d2", 34, PLUM)
    endpoints = [((530, 525), "q", TEAL), ((462, 462), "d1", ORANGE), ((568, 745), "d2", PLUM)]
    for endpoint, name, color in endpoints:
        arrow(d, center, endpoint, color, 8)
        label(d, (endpoint[0]+10, endpoint[1]-28), name, 41, color)
    d.line((462, 462, 530, 525), fill=ORANGE, width=4)
    label(d, (110, 850), "圆周上每个向量的长度都等于 1", 31, MUTED)
    facts = [
        (390, "余弦", "比较夹角", TEAL_PALE, TEAL),
        (520, "点积", "此时数值等于余弦", PLUM_PALE, PLUM),
        (650, "欧氏距离", "比较向量端点的距离", ORANGE_PALE, ORANGE),
    ]
    for y, term, meaning, fill, color in facts:
        d.rounded_rectangle((730, y, 1445, y+105), radius=20, fill=fill, outline=OUTLINE, width=2)
        label(d, (765, y+52), term, 37, color, "lm")
        label(d, (1420, y+52), meaning, 31, INK, "rm")
    label(d, (758, 839), "长度均为 1：距离平方 = 2 - 2 × 点积", 34, INK)
    save(im, "submodules/03-embedding/assets/embedding-metric-comparison.png")


def reranker_learning_objectives():
    im, d = base(
        "排序模型可以从三种信号学习",
        "看单条、比一对或看整列，训练目标与标注成本并不相同",
        "排序学习",
        "训练样本应来自真实召回候选，尤其要包含主题相近但不适用的难负样本",
    )
    cards = [
        ((90, 375, 475, 745), "Pointwise", "单个候选\n预测相关等级\n数据容易构造", PLUM_PALE),
        ((575, 375, 960, 745), "Pairwise", "两个候选\n学习谁应靠前\n候选对数量较多", TEAL_PALE),
        ((1060, 375, 1445, 745), "Listwise", "整个列表\n贴近排序指标\n标注与训练更复杂", ORANGE_PALE),
    ]
    for bounds, head, detail, fill in cards:
        d.rounded_rectangle(bounds, radius=22, fill=fill, outline=OUTLINE, width=3)
        x0, y0, x1, y1 = bounds
        label(d, ((x0+x1)//2, y0+77), head, 35, INK, "mm")
        for idx, line in enumerate(detail.split("\n")):
            label(d, ((x0+x1)//2, y0+174+idx*62), line, 27, MUTED, "mm")
    save(im, "submodules/04-reranker/assets/reranker-learning-objectives.png")


def adaptation_diagnosis_matrix():
    im, d = base(
        "先按故障类型选办法",
        "旧事实、固定格式、稳定行为和部署成本，不该都交给微调",
        "适配诊断",
        "每条路线都要用独立样本验收，不能拿训练数据证明自己有效",
    )
    rows = [
        ("动态事实过期", "更新知识与检索", TEAL_PALE),
        ("固定字段遗漏", "模板或结构约束", ORANGE_PALE),
        ("稳定行为反复失误", "SFT / LoRA", PLUM_PALE),
        ("调用量大且任务清楚", "蒸馏小模型", TEAL_PALE),
    ]
    y = 350
    for problem, route, fill in rows:
        box(d, (120, y, 650, y+105), problem, "#FFFFFF", 28)
        arrow(d, (661, y+52), (825, y+52), ORANGE)
        box(d, (836, y, 1415, y+105), route, fill, 28)
        y += 125
    save(im, "submodules/05-adaptation/assets/adaptation-diagnosis-matrix.png")


def adaptation_distillation():
    im, d = base(
        "小模型怎样向大模型学习",
        "仍用“旧退款政策怎么答”这组问题，避免换案例看不出差别",
        "知识蒸馏",
        "教师示例须核验；学生是否学会，要用独立题集评测",
    )
    for bounds, head, fill in [
        ((92, 390, 345, 570), "退款政策问法", "#FFFFFF"),
        ((425, 390, 685, 570), "教师模型示例", PLUM_PALE),
        ((765, 390, 1025, 570), "人工抽检样本", "#FFFFFF"),
        ((1105, 390, 1445, 570), "学生模型训练", TEAL_PALE),
    ]:
        box(d, bounds, head, fill, 30)
    for a, b in [((356, 480), (414, 480)), ((696, 480), (754, 480)),
                 ((1036, 480), (1094, 480))]:
        arrow(d, a, b, ORANGE)
    box(d, (235, 687, 1300, 802), "另测：新版能否答对、旧版能否拒用、缺条件能否追问", ORANGE_PALE, 28)
    save(im, "submodules/05-adaptation/assets/adaptation-distillation.png")


def adaptation_lora():
    im, d = base(
        "LoRA 改的是一小部分可训练参数",
        "基础权重冻结，适配器参与计算；效果仍要靠任务测试确认",
        "参数高效适配",
        "训练完成 ≠ 新政策问题一定答对；资料过期仍应先检查检索链路",
    )
    box(d, (90, 387, 471, 530), "冻结的基础权重 W", "#FFFFFF")
    box(d, (90, 630, 471, 773), "训练的低秩参数 BA", PLUM_PALE)
    box(d, (680, 498, 1075, 660), "组合计算 Wx + BAx", TEAL_PALE)
    box(d, (1240, 498, 1444, 660), "任务输出", "#FFFFFF", 29)
    arrow(d, (482, 459), (669, 556), PLUM)
    arrow(d, (482, 701), (669, 604), PLUM)
    arrow(d, (1086, 578), (1229, 578), ORANGE)
    label(d, (755, 756), "再评测：新规、旧规、缺失条件", 29, TEAL)
    save(im, "submodules/05-adaptation/assets/adaptation-lora.png")


def adaptation_qlora_comparison():
    im, d = base(
        "QLoRA 比 LoRA 多压缩了哪一块",
        "两者都训练低秩增量；差别在冻结底座的存放与计算",
        "参数适配",
        "",
    )
    label(d, (405, 352), "LoRA", 43, PLUM, "mm")
    label(d, (1120, 352), "QLoRA", 43, TEAL, "mm")
    box(d, (115, 406, 690, 552), "冻结底座 W：常规精度", PLUM_PALE, 35)
    box(d, (845, 406, 1420, 552), "冻结底座 W：低比特存放", TEAL_PALE, 34)
    box(d, (115, 675, 690, 795), "训练低秩增量 A、B", "#FFFFFF", 34)
    box(d, (845, 675, 1420, 795), "训练低秩增量 A、B", "#FFFFFF", 34)
    label(d, (405, 610), "＋", 45, PLUM, "mm")
    label(d, (1120, 610), "＋", 45, TEAL, "mm")
    label(d, (1120, 525), "计算时反量化", 25, TEAL, "mm")
    label(d, (405, 855), "共同参与前向计算", 29, PLUM, "mm")
    label(d, (1120, 855), "共同参与前向计算", 29, TEAL, "mm")
    save(im, "submodules/05-adaptation/assets/adaptation-qlora-comparison.png")


def adaptation_version_bundle():
    im, d = base(
        "发布的不是一份适配器文件",
        "底座变化后，即使沿用同一适配器，也要重新验证组合",
        "版本验收",
        "",
    )
    box(d, (98, 380, 655, 710), "", PLUM_PALE)
    box(d, (880, 380, 1437, 710), "", TEAL_PALE)
    label(d, (375, 435), "已验证的组合", 36, PLUM, "mm")
    label(d, (375, 515), "底座 v1 + 分词器 v1", 31, INK, "mm")
    label(d, (375, 583), "适配器 a1 + 提示 p1", 31, INK, "mm")
    label(d, (375, 652), "配套回归结果", 31, INK, "mm")
    label(d, (1158, 435), "更换底座之后", 36, TEAL, "mm")
    label(d, (1158, 515), "底座 v2 + 分词器？", 31, INK, "mm")
    label(d, (1158, 583), "旧适配器 a1 能否用？", 31, INK, "mm")
    label(d, (1158, 652), "质量与兼容性待测", 31, INK, "mm")
    arrow(d, (670, 548), (865, 548), ORANGE, 8)
    label(d, (768, 736), "同名文件 ≠ 同一行为", 31, PLUM, "mm")
    save(im, "submodules/05-adaptation/assets/adaptation-version-bundle.png")


def multimodal_encoding():
    im, d = base(
        "不同输入先走各自的编码路径",
        "不是把图片、声音和文字直接倒进同一个特征袋里",
        "多模态输入",
        "具体模型可能只支持其中部分模态；融合方式也因架构而异",
    )
    rows = [
        ("图片", "视觉编码器", "视觉特征", 366),
        ("声音", "音频编码器", "音频特征", 531),
        ("文字", "文本编码器", "文本特征", 696),
    ]
    for source, encoder, features, y in rows:
        box(d, (90, y, 322, y+105), source, "#FFFFFF")
        box(d, (419, y, 742, y+105), encoder, PLUM_PALE)
        box(d, (845, y, 1138, y+105), features, TEAL_PALE)
        arrow(d, (333, y+52), (408, y+52), ORANGE)
        arrow(d, (753, y+52), (834, y+52), ORANGE)
    box(d, (1230, 489, 1450, 674), "按任务对齐\n或融合", ORANGE_PALE)
    d.line((1149, 418, 1189, 418, 1189, 749), fill=TEAL, width=5)
    d.line((1149, 583, 1189, 583), fill=TEAL, width=5)
    d.line((1149, 749, 1189, 749), fill=TEAL, width=5)
    arrow(d, (1189, 583), (1219, 583), TEAL)
    save(im, "submodules/02-multimodal/assets/multimodal-encoding.png")


def multimodal_document():
    im, d = base(
        "同一页发票，要同时读四种线索",
        "数值离开标签和所在区域，就可能填进错误字段",
        "单据版面",
        "发票为教学示意；字段数值沿用正文案例，不代表真实票据",
    )
    d.rounded_rectangle((370, 324, 1164, 857), radius=18, fill="#FFFFFF", outline=OUTLINE, width=3)
    label(d, (410, 355), "酒店发票（示意）", 33)
    label(d, (900, 355), "开票日期  9/3", 27)
    label(d, (900, 393), "年份未标", 24, PLUM)
    d.line((410, 435, 1125, 435), fill=OUTLINE, width=2)
    d.rounded_rectangle((410, 467, 1125, 614), radius=12, fill=TEAL_PALE, outline=OUTLINE, width=2)
    label(d, (438, 488), "项目", 26, MUTED)
    label(d, (722, 488), "数量", 26, MUTED)
    label(d, (893, 488), "含税金额", 26, MUTED)
    d.line((430, 533, 1105, 533), fill=OUTLINE, width=2)
    label(d, (438, 552), "住宿服务", 29)
    label(d, (727, 552), "1", 29)
    label(d, (908, 552), "680.00", 32, TEAL)
    label(d, (452, 663), "税额", 28)
    label(d, (940, 663), "38.49", 32, TEAL)
    d.line((410, 725, 1125, 725), fill=OUTLINE, width=2)
    label(d, (420, 762), "小字：开票信息以原件为准", 25, MUTED)
    d.ellipse((985, 759, 1105, 831), outline=PLUM, width=3)
    label(d, (1045, 795), "印章区", 23, PLUM, "mm")

    for bounds, title, detail, target in [
        ((90, 345, 336, 457), "版面", "标题与日期位置", (360, 382)),
        ((1200, 477, 1445, 589), "表格", "列名决定金额含义", (1175, 540)),
        ((90, 695, 336, 807), "小字", "说明不能略读", (360, 760)),
        ((1200, 731, 1445, 843), "印章", "独立区域核验", (1175, 786)),
    ]:
        d.rounded_rectangle(bounds, radius=15, fill=PLUM_PALE, outline=OUTLINE, width=2)
        label(d, (bounds[0]+20, bounds[1]+18), title, 30, PLUM)
        label(d, (bounds[0]+20, bounds[1]+68), detail, 23, INK)
        start = (bounds[2]+9, (bounds[1]+bounds[3])//2) if bounds[0] < 400 else (bounds[0]-9, (bounds[1]+bounds[3])//2)
        arrow(d, start, target, TEAL, 4)
    save(im, "submodules/02-multimodal/assets/multimodal-document.png")


def multimodal_validation():
    im, d = base(
        "同样是读数，为什么日期不能通过",
        "金额能解析，不等于缺少年份的日期也能补全",
        "字段校验",
        "业务规则还需制度和历史记录；图片本身不能证明可报销",
    )
    label(d, (92, 350), "模型读数", 29, PLUM)
    label(d, (535, 350), "格式与字段关系", 29, PLUM)
    label(d, (1070, 350), "可核对草稿", 29, PLUM)
    box(d, (90, 397, 431, 572), "含税金额  680.00\n税额  38.49", "#FFFFFF", 29)
    box(d, (535, 397, 945, 572), "金额格式可解析\n两项分别核对标签", TEAL_PALE, 28)
    box(d, (1060, 397, 1445, 572), "保留两项读数\n等待原图复核", TEAL_PALE, 28)
    arrow(d, (442, 485), (524, 485), ORANGE)
    arrow(d, (956, 485), (1049, 485), ORANGE)
    box(d, (90, 631, 431, 806), "开票日期  9/3", "#FFFFFF", 30)
    box(d, (535, 631, 945, 806), "缺少年份\n不能通过完整日期校验", ORANGE_PALE, 27)
    box(d, (1060, 631, 1445, 806), "保留 9/3\n年份 = 未知", ORANGE_PALE, 28)
    arrow(d, (442, 719), (524, 719), ORANGE)
    arrow(d, (956, 719), (1049, 719), ORANGE)
    save(im, "submodules/02-multimodal/assets/multimodal-validation.png")


def multimodal_alignment():
    im, d = base(
        "连接层能补回被缩掉的小字吗",
        "同一张发票的两种输入方式，决定语言模型能看到哪些线索",
        "面试原理",
        "连接层映射已有视觉特征，不能从缺失的像素中还原发票小字",
    )
    box(d, (90, 469, 376, 661), "同一张发票\n含税金额 680.00\n税额 38.49", "#FFFFFF", 26)
    label(d, (463, 347), "输入给视觉编码器", 27, PLUM)
    label(d, (1070, 347), "连接层送入语言模型", 27, PLUM)
    box(d, (485, 390, 954, 534), "整页缩得太小\n小字、小数点可能消失", ORANGE_PALE, 27)
    box(d, (1060, 390, 1445, 534), "只能映射残缺特征\n回答易漏字段", ORANGE_PALE, 27)
    box(d, (485, 609, 954, 753), "金额栏局部放大\n保留标签与 680.00", TEAL_PALE, 27)
    box(d, (1060, 609, 1445, 753), "映射较清晰的特征\n仍须回原图复核", TEAL_PALE, 27)
    arrow(d, (387, 554), (474, 462), ORANGE)
    arrow(d, (387, 568), (474, 681), TEAL)
    arrow(d, (965, 462), (1049, 462), ORANGE)
    arrow(d, (965, 681), (1049, 681), TEAL)
    label(d, (767, 825), "问题不在“说得不够流畅”，而在“看进去时已丢信息”", 27, MUTED, "mm")
    save(im, "submodules/02-multimodal/assets/multimodal-alignment.png")


def multimodal_ocr_vlm():
    im, d = base(
        "OCR 与视觉语言模型，各补哪块短板",
        "同一张发票：认出字符与判断字段归属是两项检查",
        "面试选型",
        "两条路线都要回到原图；结果一致，也不能补出不存在的年份",
    )
    box(d, (90, 354, 488, 520), "发票原图\n680.00 · 38.49 · 9/3", "#FFFFFF", 29)
    box(d, (655, 346, 1055, 492), "OCR\n给字符与文字框位置", PLUM_PALE, 27)
    box(d, (655, 599, 1055, 745), "视觉语言模型\n给字段关系候选", TEAL_PALE, 27)
    arrow(d, (499, 432), (644, 419), ORANGE)
    arrow(d, (499, 440), (644, 672), ORANGE)
    box(d, (1190, 353, 1445, 496), "字符是否读对？\n框在哪里？", "#FFFFFF", 24)
    box(d, (1190, 601, 1445, 744), "金额和税额\n是否填反？", "#FFFFFF", 24)
    arrow(d, (1066, 419), (1179, 419), PLUM)
    arrow(d, (1066, 672), (1179, 672), TEAL)
    box(d, (220, 775, 1295, 859), "组合：先定位字符，再判字段关系，最后按原图复核", ORANGE_PALE, 28)
    save(im, "submodules/02-multimodal/assets/multimodal-ocr-vlm.png")


def multimodal_document_diagnosis():
    im, d = base(
        "表格和小字，常在哪一步出错",
        "对同一张发票，分别定位输入损失与关系错误",
        "面试诊断",
        "先判断信息是没看见、看错了，还是看见后配错字段",
    )
    cases = [
        (395, "缩图过度", "小数点或小字消失", "保留原图，放大金额栏", PLUM_PALE),
        (570, "拆开行列", "680.00 离开含税金额标签", "连同列名和坐标复核", TEAL_PALE),
        (745, "日期缺项", "9/3 没写年份", "年份标未知，不自行补全", ORANGE_PALE),
    ]
    for y, source, failure, action, fill in cases:
        box(d, (90, y-53, 395, y+53), source, "#FFFFFF", 31)
        box(d, (520, y-53, 985, y+53), failure, fill, 29)
        box(d, (1110, y-53, 1445, y+53), action, "#FFFFFF", 26)
        arrow(d, (406, y), (509, y), ORANGE)
        arrow(d, (996, y), (1099, y), TEAL)
    save(im, "submodules/02-multimodal/assets/multimodal-document-diagnosis.png")


def multimodal_evaluation():
    im, d = base(
        "评测别只看最终字段有没有填对",
        "把错误拆到字符、字段归属与缺项处理，才知道怎么修",
        "面试评测",
        "只列评测维度与修复方向；图中没有虚构测试成绩",
    )
    cases = [
        (395, "字符读错", "金额字符准确率", "补拍或放大原图", PLUM_PALE),
        (570, "字段填反", "字段归属 + 区域定位", "核查标签与坐标", TEAL_PALE),
        (745, "无据补年份", "缺项保留率", "年份未知，交人工补证", ORANGE_PALE),
    ]
    for y, error, measure, response, fill in cases:
        box(d, (90, y-53, 395, y+53), error, "#FFFFFF", 31)
        box(d, (520, y-53, 985, y+53), measure, fill, 29)
        box(d, (1110, y-53, 1445, y+53), response, "#FFFFFF", 26)
        arrow(d, (406, y), (509, y), ORANGE)
        arrow(d, (996, y), (1099, y), TEAL)
    save(im, "submodules/02-multimodal/assets/multimodal-evaluation.png")


def main():
    # LLM assets and the mobile-first multimodal assets are curated separately.
    # Keep old renderers for history; do not overwrite the 1000×1450 mobile figures.
    selected = set(sys.argv[1:])
    for renderer in (
        foundation_receipt_case,
        foundation_role_boundary,
        foundation_rag_case,
        foundation_route_matrix,
        foundation_release_checks,
        foundation_answer_contract,
        foundation_eval_board,
        foundation_debug_trace,
        embedding_chunking,
        embedding_evaluation,
        reranker_two_stage,
        reranker_evaluation,
        embedding_metric_comparison,
        reranker_learning_objectives,
        adaptation_diagnosis_matrix,
        adaptation_distillation,
        adaptation_lora,
        adaptation_qlora_comparison,
        adaptation_version_bundle,
    ):
        if not selected or renderer.__name__ in selected:
            renderer()


if __name__ == "__main__":
    main()
