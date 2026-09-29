"""Render corrected auxiliary diagrams for the foundation-model WeChat series.

The PNGs are publishable assets. Keep all labels and arrows deterministic so a
future edit cannot silently reintroduce a misleading model relationship.
"""

from math import atan2, cos, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1] / "content/wechat/foundation-models-and-inference"
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
    d.rectangle((0, 0, 21, H), fill=PLUM)
    label(d, (88, 80), category, 27, PLUM)
    label(d, (88, 131), title, 59)
    label(d, (90, 228), subtitle, 30, MUTED)
    d.line((88, 282, 1450, 282), fill=OUTLINE, width=3)
    d.line((88, 894, 1450, 894), fill=OUTLINE, width=2)
    label(d, (91, 925), footnote, 27, MUTED)
    return im, d


def save(im, relative):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, optimize=True)


def embedding_chunking():
    im, d = base(
        "切好的片段怎样进入向量索引",
        "先保留条款条件，再编码；权限在查询时还要重新判断",
        "建索引与查询",
        "一个片段既要有向量，也要能回到原文和适用条件",
    )
    steps = [
        ((89, 384, 338, 534), "制度原文", "#FFFFFF"),
        ((414, 384, 687, 534), "按条款切片", PLUM_PALE),
        ((765, 384, 1026, 534), "嵌入模型", TEAL_PALE),
        ((1100, 384, 1444, 534), "向量 + 片段 ID", ORANGE_PALE),
    ]
    for bounds, name, fill in steps:
        box(d, bounds, name, fill)
    for a, b in [((348, 459), (403, 459)), ((697, 459), (754, 459)),
                 ((1036, 459), (1089, 459))]:
        arrow(d, a, b, ORANGE)
    box(d, (215, 674, 690, 795), "随片段保存：来源、版本、适用范围", "#FFFFFF", 27)
    box(d, (840, 674, 1320, 795), "查询时：按身份与日期过滤", "#FFFFFF", 28)
    arrow(d, (702, 735), (828, 735), TEAL)
    save(im, "submodules/embedding/assets/embedding-chunking.png")


def embedding_evaluation():
    im, d = base(
        "召回结果怎样算对",
        "模型先给候选；人工标注的相关资料只用于对照评测",
        "召回评测",
        "Recall@K：前 K 个结果覆盖了多少应找出的相关资料",
    )
    for bounds, name, fill in [
        ((90, 383, 336, 505), "测试问题", "#FFFFFF"),
        ((430, 383, 728, 505), "嵌入检索", TEAL_PALE),
        ((822, 383, 1100, 505), "前 K 个结果", "#FFFFFF"),
        ((430, 643, 1100, 765), "人工标注的相关资料（标准答案）", PLUM_PALE),
        ((1190, 500, 1445, 658), "比较集合\nRecall@K", ORANGE_PALE),
    ]:
        if "\n" in name:
            d.rounded_rectangle(bounds, radius=22, fill=fill, outline=OUTLINE, width=3)
            x0, y0, x1, y1 = bounds
            label(d, ((x0+x1)//2, y0+54), "比较集合", 28, INK, "mm")
            label(d, ((x0+x1)//2, y0+110), "Recall@K", 30, TEAL, "mm")
        else:
            box(d, bounds, name, fill, 29)
    for a, b in [((347, 444), (419, 444)), ((739, 444), (811, 444)),
                 ((1111, 444), (1179, 548)), ((1111, 704), (1179, 614))]:
        arrow(d, a, b, ORANGE)
    label(d, (484, 790), "标注资料不会“生成”召回结果", 28, PLUM)
    save(im, "submodules/embedding/assets/embedding-evaluation.png")


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
    save(im, "submodules/reranker/assets/reranker-two-stage.png")


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
    save(im, "submodules/reranker/assets/reranker-evaluation.png")


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
    save(im, "submodules/llm/assets/llm-sampling.png")


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
    save(im, "submodules/llm/assets/llm-evidence-audit.png")


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
    save(im, "submodules/llm/assets/llm-context-conflict.png")


def multimodal_field_trace():
    im, d = base(
        "读对字符后，怎样确认字段",
        "把字符、坐标、标签和最终字段连起来，才能回到原图复核",
        "字段溯源",
        "最终 JSON 只是结果；原图区域与字段关系才是可核对的证据",
    )
    box(d, (90, 390, 365, 675), "原图区域\n金额栏\n税额栏\n日期栏", "#FFFFFF", 28)
    box(d, (480, 390, 770, 675), "字符 + 坐标\n680.00\n38.49\n9/3", PLUM_PALE, 28)
    box(d, (885, 390, 1175, 675), "标签关系\n含税金额\n税额\n开票日期", TEAL_PALE, 28)
    box(d, (1290, 390, 1445, 675), "字段草稿\n待核对", ORANGE_PALE, 27)
    arrow(d, (376, 532), (469, 532), ORANGE)
    arrow(d, (781, 532), (874, 532), ORANGE)
    arrow(d, (1186, 532), (1279, 532), ORANGE)
    box(d, (390, 748, 1140, 835), "缺少年份：保留缺项，不自行补成完整日期", "#FFFFFF", 27)
    save(im, "submodules/multimodal/assets/multimodal-field-trace.png")


def embedding_metric_comparison():
    im, d = base(
        "三种距离比较的对象不同",
        "先确认模型怎样训练、向量是否归一化，再选择相似度计算",
        "距离度量",
        "距离公式不能脱离模型训练目标和索引配置单独决定",
    )
    cards = [
        ((90, 370, 475, 740), "余弦相似度", "比较方向\n弱化向量长度\n常配合归一化", TEAL_PALE),
        ((575, 370, 960, 740), "点积", "方向与长度都参与\n可直接用于最大内积检索\n分值受尺度影响", PLUM_PALE),
        ((1060, 370, 1445, 740), "欧氏距离", "比较空间距离\n对尺度敏感\n归一化后与余弦相关", ORANGE_PALE),
    ]
    for bounds, head, detail, fill in cards:
        d.rounded_rectangle(bounds, radius=22, fill=fill, outline=OUTLINE, width=3)
        x0, y0, x1, y1 = bounds
        label(d, ((x0+x1)//2, y0+76), head, 35, INK, "mm")
        for idx, line in enumerate(detail.split("\n")):
            label(d, ((x0+x1)//2, y0+168+idx*62), line, 27, MUTED, "mm")
    box(d, (350, 790, 1185, 865), "同一批候选必须使用同一套编码、归一化与距离配置", "#FFFFFF", 26)
    save(im, "submodules/embedding/assets/embedding-metric-comparison.png")


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
    save(im, "submodules/reranker/assets/reranker-learning-objectives.png")


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
    save(im, "submodules/adaptation/assets/adaptation-diagnosis-matrix.png")


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
    save(im, "submodules/adaptation/assets/adaptation-distillation.png")


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
    save(im, "submodules/adaptation/assets/adaptation-lora.png")


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
    save(im, "submodules/multimodal/assets/multimodal-encoding.png")


def main():
    for renderer in (
        embedding_chunking,
        embedding_evaluation,
        reranker_two_stage,
        reranker_evaluation,
        llm_sampling,
        llm_evidence_audit,
        llm_context_conflict,
        multimodal_field_trace,
        embedding_metric_comparison,
        reranker_learning_objectives,
        adaptation_diagnosis_matrix,
        adaptation_distillation,
        adaptation_lora,
        multimodal_encoding,
    ):
        renderer()


if __name__ == "__main__":
    main()
