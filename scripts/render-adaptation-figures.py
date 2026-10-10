"""Render source-checked 1.5 model-adaptation article diagrams.

The refund-policy examples, scores, and matrices below are teaching constructions.
See the paired prompts.md for source boundaries and figure roles.
"""

from math import atan2, cos, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1] / "content/wechat/01-foundation-models-and-inference/submodules/05-adaptation/assets"
FONT = next(str(p) for p in (
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
) if p.exists())
W, H = 1536, 1024
BG = "#FBF9F4"
INK = "#253139"
MUTED = "#68737B"
LINE = "#D4DAD6"
TEAL = "#147D79"
TEAL_L = "#E6F1EE"
PLUM = "#81556B"
PLUM_L = "#F2EAF0"
ORANGE = "#CA6C39"
ORANGE_L = "#FFF0E3"
BLUE = "#44739F"
BLUE_L = "#E8F0F6"
RED = "#B85F58"
RED_L = "#F8EDEB"


def font(size):
    return ImageFont.truetype(FONT, size)


def txt(d, x, y, s, size=34, color=INK, anchor="la"):
    d.text((x, y), s, font=font(size), fill=color, anchor=anchor)


def card(d, box, fill="white", outline=LINE, radius=17, width=3):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(d, a, b, color=TEAL, width=5, head=15):
    d.line((a, b), fill=color, width=width)
    angle = atan2(b[1] - a[1], b[0] - a[0])
    d.polygon([b,
               (b[0] - head*cos(angle) + 9*sin(angle), b[1] - head*sin(angle) - 9*cos(angle)),
               (b[0] - head*cos(angle) - 9*sin(angle), b[1] - head*sin(angle) + 9*cos(angle))], fill=color)


def base(title, kicker):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    txt(d, 78, 61, kicker, 29, TEAL)
    txt(d, 78, 109, title, 55, INK)
    d.line((78, 191, 1458, 191), fill=LINE, width=2)
    return im, d


def save(im, name):
    ROOT.mkdir(parents=True, exist_ok=True)
    im.save(ROOT / name, optimize=True)


def case_split():
    im, d = base("同叫“答错”，先查的地方不同", "退款客服 / 两种故障")
    rows = [
        (275, PLUM, PLUM_L, "仍回答：七天内可退", "现行政策：三天内可退", "先核对政策版本与检索证据"),
        (591, TEAL, TEAL_L, "已回答：三天内可退", "却漏掉：退回原支付渠道", "先核对提示、模板与输出约束"),
    ]
    for y, col, fill, answer, conflict, action in rows:
        card(d, (91, y, 1445, y+249), "white", LINE, 20)
        card(d, (117, y+27, 708, y+130), fill, col, 15)
        txt(d, 412, y+79, answer, 40, INK, "mm")
        txt(d, 765, y+77, conflict, 36, col, "lm")
        d.line((126, y+153, 1407, y+153), fill=LINE, width=2)
        txt(d, 139, y+195, "第一步", 31, MUTED, "lm")
        arrow(d, (260, y+195), (352, y+195), col, 4)
        txt(d, 384, y+195, action, 36, INK, "lm")
    save(im, "adaptation-case-split-v2.png")


def sft_objective():
    im, d = base("监督微调怎样学会固定提醒", "SFT / 输入、目标答复与损失")
    card(d, (88, 274, 721, 437), BLUE_L, BLUE, 20)
    txt(d, 123, 310, "输入给模型", 32, BLUE)
    txt(d, 123, 350, "证据：三天内可退", 33)
    txt(d, 123, 391, "要求：说明退款去向", 33)
    arrow(d, (733, 355), (824, 355), BLUE)
    card(d, (839, 274, 1446, 437), TEAL_L, TEAL, 20)
    txt(d, 877, 326, "人工核对的目标答复", 32, TEAL)
    txt(d, 877, 387, "三天内可退；退回原支付渠道", 36)
    txt(d, 97, 522, "训练时沿目标答复逐位置预测", 36, INK)
    chips = [(100, 626, "三天内可退", ORANGE), (579, 626, "退回原支付渠道", TEAL)]
    for x, y, label, col in chips:
        card(d, (x, y, x+391, y+121), "white", col, 16)
        txt(d, x+195, y+60, label, 39, col, "mm")
    arrow(d, (505, 686), (565, 686), MUTED, 4)
    arrow(d, (984, 686), (1183, 686), PLUM)
    card(d, (1198, 617, 1439, 764), PLUM_L, PLUM, 17)
    txt(d, 1318, 663, "预测误差", 35, PLUM, "mm")
    txt(d, 1318, 719, "更新参数", 35, PLUM, "mm")
    save(im, "adaptation-sft-objective-v2.png")


def lora_branches():
    im, d = base("输入分两路：原权重加低秩增量", "LoRA / Hu 等 Figure 1")
    card(d, (91, 475, 295, 604), BLUE_L, BLUE)
    txt(d, 193, 540, "输入 x", 43, BLUE, "mm")
    arrow(d, (307, 540), (418, 351), BLUE)
    arrow(d, (307, 540), (418, 718), BLUE)
    card(d, (431, 269, 810, 436), "white", MUTED, 20)
    txt(d, 620, 319, "W0 · x", 48, INK, "mm")
    txt(d, 620, 387, "预训练权重冻结", 33, MUTED, "mm")
    card(d, (431, 628, 605, 797), ORANGE_L, ORANGE, 17)
    txt(d, 518, 677, "A · x", 42, ORANGE, "mm")
    txt(d, 518, 744, "r × k", 33, MUTED, "mm")
    arrow(d, (617, 713), (703, 713), ORANGE)
    card(d, (716, 628, 890, 797), ORANGE_L, ORANGE, 17)
    txt(d, 803, 677, "B · (Ax)", 38, ORANGE, "mm")
    txt(d, 803, 744, "d × r", 33, MUTED, "mm")
    txt(d, 702, 842, "只训练 A、B；r 远小于 d、k", 30, ORANGE, "ma")
    arrow(d, (825, 351), (1035, 481), MUTED)
    arrow(d, (906, 713), (1035, 561), ORANGE)
    d.ellipse((1032, 477, 1119, 564), fill="white", outline=LINE, width=4)
    txt(d, 1075, 520, "+", 49, PLUM, "mm")
    arrow(d, (1130, 520), (1212, 520), PLUM)
    card(d, (1227, 429, 1447, 613), TEAL_L, TEAL, 19)
    txt(d, 1337, 487, "输出 h", 42, TEAL, "mm")
    txt(d, 1337, 553, "W0x + BAx", 32, INK, "mm")
    save(im, "adaptation-lora-branches-v2.png")


def distill_distribution():
    im, d = base("学生学的是教师的输出分布", "知识蒸馏 / 同一输入上的软目标")
    card(d, (88, 273, 1449, 389), BLUE_L, BLUE)
    txt(d, 769, 331, "输入：已提供现行三天政策，判断退款期限", 40, INK, "mm")
    labels = [("三天", 0.70, TEAL), ("七天", 0.20, RED), ("需核对", 0.10, PLUM)]
    txt(d, 119, 473, "教师模型：期限判断分布", 36, TEAL)
    txt(d, 828, 473, "学生模型：学习前的分布", 36, PLUM)
    arrow(d, (683, 474), (809, 474), ORANGE, 4)
    for i, (label, tval, col) in enumerate(labels):
        y = 564 + i*119
        txt(d, 118, y, label, 35, col, "lm")
        d.rectangle((255, y-22, 629, y+25), fill="#EBEFEC")
        d.rectangle((255, y-22, 255+int(374*tval), y+25), fill=col)
        txt(d, 666, y, f"{tval:.2f}", 34, INK, "rm")
        student = (0.30, 0.45, 0.25)[i]
        d.rectangle((832, y-22, 1210, y+25), fill="#EBEFEC")
        d.rectangle((832, y-22, 832+int(378*student), y+25), fill=PLUM)
        txt(d, 1297, y, f"{student:.2f}", 34, INK, "rm")
    save(im, "adaptation-distill-distribution-v2.png")


def release_control():
    im, d = base("只换适配器，才能看清训练收益", "受控对照 / 发布前验收")
    rows = [
        (300, PLUM, PLUM_L, "原方案", "底座 b1 + 政策证据 r1 + 提示 p1"),
        (455, TEAL, TEAL_L, "候选方案", "底座 b1 + 政策证据 r1 + 提示 p1 + 适配器 a2"),
    ]
    for y, col, fill, name, detail in rows:
        card(d, (91, y, 1447, y+120), fill, col, 17)
        txt(d, 124, y+60, name, 36, col, "lm")
        txt(d, 405, y+60, detail, 34, INK, "lm")
    txt(d, 96, 654, "两组使用同一批独立测试题", 37, INK)
    tests = [(113, "现行政策", "查证据版本"), (466, "固定提醒", "查漏答"),
             (819, "旧任务", "查回归"), (1172, "拒答边界", "查安全")]
    for x, name, task in tests:
        card(d, (x, 732, x+268, 886), "white", LINE, 16)
        txt(d, x+134, 782, name, 34, TEAL, "mm")
        txt(d, x+134, 842, task, 28, MUTED, "mm")
    save(im, "adaptation-release-control-v2.png")


def diagnosis_ablation():
    im, d = base("先做三次对照，再决定是否训练", "面试排障 / 退款客服")
    tests = [
        (287, BLUE, BLUE_L, "只换现行政策证据", "旧期限随之消失？", "若是，先修检索与版本"),
        (482, ORANGE, ORANGE_L, "只加固定提醒模板", "漏提醒随之消失？", "若是，先用模板与校验"),
        (677, PLUM, PLUM_L, "证据与模板都固定", "漏答仍反复出现？", "再评估 SFT／LoRA"),
    ]
    for y, col, fill, change, question, result in tests:
        card(d, (91, y, 1446, y+160), "white", LINE, 18)
        card(d, (119, y+29, 533, y+129), fill, col, 14)
        txt(d, 326, y+79, change, 33, INK, "mm")
        txt(d, 585, y+78, question, 33, col, "lm")
        txt(d, 1398, y+78, result, 31, INK, "rm")
    save(im, "adaptation-diagnosis-ablation-v2.png")


def lora_parameters():
    im, d = base("一层矩阵：全量与低秩差多少参数", "面试算例 / d = k = 4096，r = 8")
    card(d, (91, 295, 718, 779), "white", LINE, 18)
    txt(d, 133, 354, "原权重 W", 40, PLUM)
    card(d, (158, 422, 531, 653), PLUM_L, PLUM, 14)
    txt(d, 344, 499, "4096 × 4096", 42, PLUM, "mm")
    txt(d, 344, 574, "16,777,216", 40, INK, "mm")
    txt(d, 134, 717, "全量更新：这一层都要训练", 31, MUTED)
    card(d, (818, 295, 1446, 779), "white", LINE, 18)
    txt(d, 862, 354, "LoRA：W 冻结，只训练 A、B", 38, TEAL)
    card(d, (861, 433, 1109, 592), ORANGE_L, ORANGE, 14)
    txt(d, 985, 482, "A：8 × 4096", 30, ORANGE, "mm")
    txt(d, 985, 544, "32,768", 35, INK, "mm")
    txt(d, 1145, 509, "+", 43, MUTED, "mm")
    card(d, (1177, 433, 1416, 592), ORANGE_L, ORANGE, 14)
    txt(d, 1296, 482, "B：4096 × 8", 29, ORANGE, "mm")
    txt(d, 1296, 544, "32,768", 35, INK, "mm")
    txt(d, 862, 690, "合计 65,536 · 约为全量的 0.39%", 35, TEAL)
    save(im, "adaptation-lora-count-v2.png")


def qlora_path():
    im, d = base("QLoRA：低比特存底座，训练适配器", "面试原理 / QLoRA 数据与梯度路径")
    card(d, (91, 287, 598, 760), BLUE_L, BLUE, 19)
    txt(d, 134, 354, "冻结的基础权重", 39, BLUE)
    txt(d, 134, 440, "NF4 · 4 bit 存放", 38, INK)
    txt(d, 134, 507, "量化常数可再次量化", 31, MUTED)
    card(d, (142, 582, 548, 704), "white", BLUE, 14)
    txt(d, 345, 644, "计算时反量化", 36, BLUE, "mm")
    arrow(d, (613, 526), (725, 526), BLUE)
    card(d, (740, 367, 1053, 696), "white", LINE, 17)
    txt(d, 896, 433, "前向计算", 42, INK, "mm")
    txt(d, 896, 516, "底座路径", 35, BLUE, "mm")
    txt(d, 896, 598, "+ 低秩增量", 35, ORANGE, "mm")
    arrow(d, (1068, 526), (1166, 526), TEAL)
    card(d, (1181, 367, 1446, 696), TEAL_L, TEAL, 17)
    txt(d, 1314, 431, "参数更新", 42, TEAL, "mm")
    txt(d, 1314, 520, "只更新 A、B", 35, ORANGE, "mm")
    txt(d, 1314, 600, "底座不更新", 32, MUTED, "mm")
    save(im, "adaptation-qlora-path-v2.png")


def distill_soft_targets():
    im, d = base("硬标签只有一个答案，软目标还有分布", "面试原理 / Hinton 等知识蒸馏")
    labels = ["三天", "七天", "需核对"]
    hard = [1.0, 0.0, 0.0]
    soft = [0.70, 0.20, 0.10]
    configs = [(96, "硬标签", hard, PLUM, PLUM_L),
               (820, "教师软目标 · T > 1", soft, TEAL, TEAL_L)]
    for x, title, vals, col, fill in configs:
        card(d, (x, 279, x+619, 827), "white", LINE, 19)
        txt(d, x+309, 349, title, 39, col, "mm")
        for i, label in enumerate(labels):
            y=470+i*123
            txt(d, x+34, y, label, 33, INK, "lm")
            d.rectangle((x+174,y-25,x+506,y+24), fill="#EBEFEC")
            if vals[i] > 0:
                d.rectangle((x+174,y-25,x+174+int(332*vals[i]),y+24), fill=col)
            txt(d, x+576, y, f"{vals[i]:.2f}", 32, INK, "rm")
    save(im, "adaptation-distill-soft-targets-v2.png")


def forgetting_regression():
    im, d = base("新任务变好，不代表旧能力没退步", "面试验收 / 同一适配器的两套回归题")
    card(d, (91, 281, 1446, 415), ORANGE_L, ORANGE, 18)
    txt(d, 137, 345, "训练信号", 36, ORANGE, "lm")
    txt(d, 438, 345, "退款答复必须带“退回原支付渠道”", 40, INK, "lm")
    arrow(d, (765, 434), (765, 520), ORANGE)
    cards = [(104, TEAL, TEAL_L, "目标任务集", "固定提醒漏答率", "应下降"),
             (788, BLUE, BLUE_L, "旧能力回归集", "普通问答 · 拒答边界", "不能明显退化")]
    for x,col,fill,name,metric,expect in cards:
        card(d,(x,539,x+643,806),fill,col,19)
        txt(d,x+47,602,name,40,col)
        txt(d,x+47,680,metric,35,INK)
        txt(d,x+47,754,expect,32,col)
    save(im, "adaptation-forgetting-regression-v2.png")


def version_gate():
    im, d = base("同名适配器，换底座后仍要重验", "面试发布 / 可复现的版本组合")
    cols = [(97, PLUM, PLUM_L, "已验证组合"), (818, TEAL, TEAL_L, "更换底座后")]
    for x,col,fill,title in cols:
        card(d,(x,273,x+621,806),"white",LINE,19)
        txt(d,x+309,337,title,42,col,"mm")
        entries = (["底座 b1 + 分词器 t1", "适配器 a1 + 提示 p1", "独立回归：已通过"] if x<800 else
                   ["底座 b2 + 分词器 t2", "沿用适配器 a1？", "兼容性与质量：待验证"])
        for i,s in enumerate(entries):
            yy=422+i*113
            card(d,(x+36,yy,x+585,yy+81),fill,col,13)
            txt(d,x+309,yy+40,s,32,INK if i<2 else col,"mm")
    arrow(d,(733,548),(801,548),ORANGE,6)
    save(im,"adaptation-version-gate-v2.png")


if __name__ == "__main__":
    for draw in (case_split, sft_objective, lora_branches, distill_distribution,
                 release_control, diagnosis_ablation, lora_parameters, qlora_path,
                 distill_soft_targets, forgetting_regression, version_gate):
        draw()
