"""Draw mobile-first, source-checkable figures for the multimodal WeChat pair.

Run with the bundled Python that includes Pillow. These figures are deliberately
drawn from exact labels and case facts; image generation is used only for covers.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ASSETS = (Path(__file__).resolve().parents[1] /
          "content/wechat/01-foundation-models-and-inference/submodules/02-multimodal/assets")
FONT = next(str(p) for p in (
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
) if p.exists())
W, H = 1000, 1450
BG, INK, MUTED = "#FBF8F3", "#28383C", "#53656B"
TEAL, TEAL_BG = "#187A78", "#E3F0ED"
PLUM, PLUM_BG = "#795069", "#F2E9EF"
ORANGE, ORANGE_BG = "#C47738", "#F9EBDD"
LINE = "#CBD8D4"


def ft(size):
    return ImageFont.truetype(FONT, size)


def text(d, x, y, value, size=42, fill=INK, anchor=None):
    d.text((x, y), value, font=ft(size), fill=fill, anchor=anchor)


def base(title, kicker):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    text(d, 70, 58, kicker, 35, PLUM)
    text(d, 70, 112, title, 55)
    d.line((70, 208, 930, 208), fill=LINE, width=3)
    return im, d


def card(d, y, h, heading, lines=(), color="white", x=70, w=860):
    d.rounded_rectangle((x, y, x+w, y+h), radius=24, fill=color, outline=LINE, width=3)
    text(d, x+34, y+27, heading, 45, INK)
    for index, line in enumerate(lines):
        text(d, x+34, y+91+index*54, line, 39, MUTED)


def arrow(d, y1, y2, label=None, x=500, fill=ORANGE):
    d.line((x, y1, x, y2-14), fill=fill, width=8)
    d.polygon(((x, y2), (x-16, y2-26), (x+16, y2-26)), fill=fill)
    if label:
        text(d, x+33, (y1+y2)//2, label, 35, MUTED, "lm")


def ribbon(d, y, lines, fill=ORANGE_BG):
    h = 76 + 56*(len(lines)-1)
    d.rounded_rectangle((70, y, 930, y+h), radius=20, fill=fill)
    for i, line in enumerate(lines):
        text(d, 102, y+19+i*55, line, 39, INK)


def save(im, name):
    # The outer margin is intentionally bare: no decorative left stripe.
    if im.crop((0, 0, 40, H)).getpixel((0, H//2)) != Image.new("RGB", (1, 1), BG).getpixel((0, 0)):
        raise ValueError(f"Unexpected mark at left edge: {name}")
    im.save(ASSETS / name, optimize=True)


def h_arrow(d, x1, y, x2, fill=ORANGE):
    d.line((x1, y, x2-16, y), fill=fill, width=7)
    d.polygon(((x2, y), (x2-24, y-14), (x2-24, y+14)), fill=fill)


def box(d, xy, fill="white", outline=LINE, radius=18):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=3)


def invoice(d, x, y, w, h, readable=True):
    box(d, (x, y, x+w, y+h), "#fffdf9", "#869895", 12)
    d.line((x+18, y+66, x+w-18, y+66), fill=LINE, width=3)
    text(d, x+24, y+17, "发票" if readable else "单据", 35, INK)
    for i in range(3):
        ry = y+98+i*68
        d.line((x+24, ry+47, x+w-24, ry+47), fill=LINE, width=2)
        if readable:
            label, value = (("日期", "9/3"), ("含税金额", "680.00"), ("税额", "38.49"))[i]
            text(d, x+27, ry, label, 33, MUTED)
            text(d, x+w-222, ry, value, 35, INK)
        else:
            d.rounded_rectangle((x+26, ry+8, x+w-35, ry+28), radius=7, fill=LINE)


def encoding():
    im, d = base("不同输入，先各自编码", "输入编码 · 主文")
    lanes = (
        (275, "发票照片", "视觉编码器", "图像特征", TEAL_BG, TEAL),
        (570, "语音录音", "音频编码器", "声音特征", PLUM_BG, PLUM),
        (865, "文字提问", "文本编码", "文字表示", ORANGE_BG, ORANGE),
    )
    for y, source, encoder, feature, fill, accent in lanes:
        box(d, (75, y, 270, y+200), "white")
        box(d, (365, y+32, 645, y+164), fill, accent)
        box(d, (735, y+32, 925, y+164), "white", accent)
        if source == "发票照片":
            d.rectangle((120, y+40, 225, y+130), outline=accent, width=4)
            for i in range(3):
                d.line((135, y+62+i*23, 207, y+62+i*23), fill=accent, width=4)
        elif source == "语音录音":
            for i, ht in enumerate((28, 55, 91, 48, 76, 32)):
                xx = 115+i*23
                d.line((xx, y+106-ht//2, xx, y+106+ht//2), fill=accent, width=6)
        else:
            text(d, 108, y+57, "金额？", 42, accent)
        text(d, 103, y+157, source, 33, INK)
        text(d, 402, y+73, encoder, 39)
        text(d, 764, y+73, feature, 36)
        h_arrow(d, 279, y+100, 354, accent)
        h_arrow(d, 654, y+100, 725, accent)
    ribbon(d, 1190, ("本例只用图片和文字两路；", "可用模态取决于具体模型。"), TEAL_BG)
    save(im, "multimodal-encoding.png")


def principle():
    im, d = base("图像怎样接入语言模型", "LLaVA 原理 · 主文")
    card(d, 264, 160, "发票照片", ("像素输入",), "white")
    arrow(d, 425, 468)
    card(d, 485, 160, "视觉编码器", ("提取图像特征",), TEAL_BG)
    arrow(d, 647, 690)
    card(d, 705, 160, "可训练投影层", ("图像特征转为语言表示",), PLUM_BG, x=70, w=520)
    card(d, 705, 160, "文字提问", ("含税金额？",), "white", x=625, w=305)
    arrow(d, 867, 919, x=330)
    arrow(d, 867, 919, x=777)
    card(d, 934, 198, "语言模型", ("同时接收文字提问：", "“含税金额是多少？”"), ORANGE_BG)
    arrow(d, 1134, 1182)
    ribbon(d, 1198, ("输出候选答案；字段是否正确，", "还要回原图核对。"), TEAL_BG)
    save(im, "multimodal-principle.png")


def document():
    im, d = base("一张发票，四类线索", "单据版面 · 主文")
    card(d, 260, 905, "酒店发票（教学示意）", (), "white")
    d.line((104, 346, 896, 346), fill=LINE, width=3)
    text(d, 108, 386, "版面：标题、日期所在区域", 42, PLUM)
    text(d, 135, 460, "开票日期   9/3", 43)
    text(d, 135, 520, "年份未标", 39, ORANGE)
    d.rounded_rectangle((105, 604, 895, 858), radius=18, fill=TEAL_BG)
    text(d, 135, 628, "表格：列名决定数值含义", 42, TEAL)
    text(d, 140, 706, "含税金额     680.00", 45)
    text(d, 140, 776, "税额             38.49", 45)
    text(d, 108, 899, "小字：需放大查看原文", 42, PLUM)
    text(d, 108, 981, "印章：另一区域，不能替代金额", 39, PLUM)
    ribbon(d, 1210, ("数值要连同旁边的标签核对；", "9/3 没有年份，不能补猜。"))
    save(im, "multimodal-document.png")


def field_trace():
    im, d = base("每个字段都能指回原图", "字段溯源 · 主副文共用")
    text(d, 90, 265, "原图区域", 37, TEAL)
    text(d, 386, 265, "识别读数", 37, PLUM)
    text(d, 690, 265, "草稿字段", 37, ORANGE)
    rows = (
        (333, "A", "含税金额", "680.00", "含税金额", "680.00", TEAL_BG),
        (642, "B", "税额", "38.49", "税额", "38.49", PLUM_BG),
        (951, "C", "日期", "9/3", "日期", "年份未知", ORANGE_BG),
    )
    for y, region, source, value, target, status, fill in rows:
        box(d, (75, y, 326, y+218), "white")
        box(d, (378, y+27, 600, y+191), fill)
        box(d, (660, y+5, 923, y+213), "white")
        d.ellipse((95, y+20, 151, y+76), fill=ORANGE)
        text(d, 123, y+48, region, 35, "white", "mm")
        text(d, 106, y+107, source, 35)
        text(d, 106, y+155, value, 39, TEAL)
        text(d, 403, y+89, value, 42, PLUM)
        text(d, 688, y+78, target, 35)
        text(d, 688, y+135, status, 38, ORANGE if region == "C" else TEAL)
        h_arrow(d, 332, y+109, 370)
        h_arrow(d, 607, y+109, 650)
    ribbon(d, 1281, ("A / B / C 仅为示意区域；", "每个草稿字段都要能回溯。"), TEAL_BG)
    save(im, "multimodal-field-trace.png")


def validation():
    im, d = base("能读到，不等于能通过", "字段验证 · 主文")
    invoice(d, 275, 265, 450, 322)
    text(d, 97, 635, "同一张原图，分两条校验路径", 41, MUTED)
    d.line((500, 695, 500, 746), fill=ORANGE, width=7)
    d.line((265, 745, 735, 745), fill=ORANGE, width=7)
    d.line((265, 745, 265, 787), fill=ORANGE, width=7)
    d.line((735, 745, 735, 787), fill=ORANGE, width=7)
    box(d, (72, 800, 473, 1129), TEAL_BG, TEAL)
    box(d, (527, 800, 928, 1129), ORANGE_BG, ORANGE)
    text(d, 106, 846, "金额 / 税额", 42, TEAL)
    text(d, 106, 920, "读数可解析", 37)
    text(d, 106, 974, "标签与区域须复核", 37)
    text(d, 561, 846, "日期 9/3", 42, ORANGE)
    text(d, 561, 920, "年份缺失", 37)
    text(d, 561, 974, "保持未知，不补猜", 37)
    ribbon(d, 1211, ("图像读数不是报销结论；", "是否通过还要核对制度与记录。"), PLUM_BG)
    save(im, "multimodal-validation.png")


def alignment():
    im, d = base("缩掉的小字，连接层救不回", "视觉连接 · 面试")
    text(d, 100, 257, "A  整页缩小", 41, ORANGE)
    text(d, 563, 257, "B  金额栏放大", 41, TEAL)
    box(d, (70, 325, 456, 710), ORANGE_BG, ORANGE)
    box(d, (544, 325, 930, 710), TEAL_BG, TEAL)
    invoice(d, 138, 359, 250, 288, readable=False)
    text(d, 124, 663, "标签、小数点可能丢失", 30, ORANGE)
    box(d, (572, 396, 903, 626), "#fffdf9", TEAL)
    text(d, 599, 425, "含税金额  680.00", 36)
    d.line((593, 499, 883, 499), fill=LINE, width=3)
    text(d, 599, 529, "税额      38.49", 36)
    text(d, 594, 656, "标签和读数一起保留", 30, TEAL)
    box(d, (90, 809, 431, 1000), "white")
    box(d, (569, 809, 910, 1000), "white")
    text(d, 118, 855, "视觉编码器", 38)
    text(d, 118, 921, "输入已残缺", 36, ORANGE)
    text(d, 599, 855, "视觉编码器", 38)
    text(d, 599, 921, "可见两组字段", 36, TEAL)
    arrow(d, 722, 798, x=260)
    arrow(d, 722, 798, x=740)
    d.line((260, 1007, 260, 1080), fill=ORANGE, width=6)
    d.line((740, 1007, 740, 1080), fill=TEAL, width=6)
    box(d, (185, 1090, 815, 1220), PLUM_BG, PLUM)
    text(d, 256, 1132, "连接层只能映射已有特征", 41, PLUM)
    ribbon(d, 1281, ("丢失的小字不能在连接层补回。",), "white")
    save(im, "multimodal-alignment.png")


def ocr_vlm():
    im, d = base("认出字符 ≠ 填对字段", "OCR 与 VLM · 面试")
    invoice(d, 275, 260, 450, 322)
    d.line((500, 590, 500, 650), fill=ORANGE, width=7)
    d.line((265, 650, 735, 650), fill=ORANGE, width=7)
    d.line((265, 650, 265, 700), fill=ORANGE, width=7)
    d.line((735, 650, 735, 700), fill=ORANGE, width=7)
    box(d, (70, 710, 470, 1092), PLUM_BG, PLUM)
    box(d, (530, 710, 930, 1092), TEAL_BG, TEAL)
    text(d, 98, 746, "OCR：读字与位置", 39, PLUM)
    for i, value in enumerate(("9/3", "680.00", "38.49")):
        y = 819+i*77
        box(d, (108, y, 406, y+57), "white", PLUM, 8)
        text(d, 136, y+6, value, 37)
    text(d, 556, 746, "VLM：提出归属", 39, TEAL)
    text(d, 557, 828, "含税金额 ← 680.00", 34)
    text(d, 557, 905, "税额 ← 38.49", 34)
    text(d, 557, 982, "日期 ← 9/3", 34)
    ribbon(d, 1178, ("最终按原图标签、位置复核；", "两路一致也不能补出年份。"), ORANGE_BG)
    save(im, "multimodal-ocr-vlm.png")


def diagnosis():
    im, d = base("错在看不清，还是配不对", "错误诊断 · 面试")
    rows = (
        (273, "看不清", "680.0?", ("放大金额栏",), PLUM_BG, PLUM),
        (635, "配不对", "金额错填税额", ("核对标签", "与行列"), TEAL_BG, TEAL),
        (997, "原图缺项", "9/3  +  ?年", ("年份标未知",), ORANGE_BG, ORANGE),
    )
    text(d, 91, 238, "错误现象", 35, MUTED)
    text(d, 636, 238, "定位后的动作", 35, MUTED)
    for y, title, sample, actions, fill, accent in rows:
        box(d, (70, y, 530, y+280), fill, accent)
        box(d, (620, y+31, 930, y+249), "white", accent)
        text(d, 102, y+39, title, 42, accent)
        text(d, 102, y+131, sample, 47)
        h_arrow(d, 544, y+140, 606, accent)
        for i, action in enumerate(actions):
            text(d, 652, y+98+i*51, action, 36)
    save(im, "multimodal-document-diagnosis.png")


def evaluation():
    im, d = base("把三类错误分开评", "分层评测 · 面试")
    box(d, (91, 258, 909, 379), "white")
    text(d, 131, 286, "同一批样本，拆成三项统计", 42, INK)
    d.line((126, 390, 126, 1100), fill=LINE, width=6)
    rows = (
        (454, "字符读错", "680.0?", "字符准确率", PLUM_BG, PLUM),
        (728, "字段填反", "金额填入税额栏", "字段归属率", TEAL_BG, TEAL),
        (1002, "无据补年", "9/3 被补成年份", "缺项保留率", ORANGE_BG, ORANGE),
    )
    for y, title, sample, metric, fill, accent in rows:
        d.ellipse((105, y+80, 147, y+122), fill=accent)
        box(d, (175, y, 570, y+215), fill, accent)
        box(d, (683, y+32, 924, y+185), "white", accent)
        text(d, 204, y+28, title, 40, accent)
        text(d, 204, y+105, sample, 35)
        h_arrow(d, 583, y+109, 672, accent)
        text(d, 704, y+79, metric, 37, accent)
    ribbon(d, 1280, ("还要分别核对原图区域与标签；", "不拿字符正确率代替字段正确率。"), "white")
    save(im, "multimodal-evaluation.png")


if __name__ == "__main__":
    for make in (encoding, principle, document, field_trace, validation,
                 alignment, ocr_vlm, diagnosis, evaluation):
        make()
