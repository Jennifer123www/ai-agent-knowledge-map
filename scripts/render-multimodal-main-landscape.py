"""Render the multimodal beginner article's five landscape teaching diagrams.

Run with the bundled Python that includes Pillow. Precise Chinese labels, invoice
facts, and arrow directions are drawn deterministically rather than generated.
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
W, H = 1536, 1024
BG, INK, MUTED = "#FBF8F3", "#28383C", "#53656B"
TEAL, TEAL_BG = "#187A78", "#E3F0ED"
PLUM, PLUM_BG = "#795069", "#F2E9EF"
ORANGE, ORANGE_BG = "#C47738", "#F9EBDD"
LINE = "#CBD8D4"


def font(size):
    return ImageFont.truetype(FONT, size)


def text(draw, x, y, value, size=50, fill=INK, anchor=None):
    draw.text((x, y), value, font=font(size), fill=fill, anchor=anchor)


def box(draw, xy, fill="white", outline=LINE, radius=20):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=3)


def arrow(draw, x1, y, x2, fill=ORANGE):
    draw.line((x1, y, x2-20, y), fill=fill, width=8)
    draw.polygon(((x2, y), (x2-31, y-18), (x2-31, y+18)), fill=fill)


def base(kicker, title):
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    text(draw, 72, 38, kicker, 35, PLUM)
    text(draw, 72, 91, title, 59)
    draw.line((72, 194, 1464, 194), fill=LINE, width=3)
    return image, draw


def footer(draw, message):
    box(draw, (70, 905, 1466, 981), "white", "white", 15)
    text(draw, 105, 920, message, 43)


def save(image, name):
    image.save(ASSETS / name, optimize=True)


def encoding():
    image, draw = base("输入编码 · 主文", "图片、声音、文字并不共用一个入口")
    lanes = (
        (248, "发票照片", "视觉编码器", "图像特征", TEAL, TEAL_BG),
        (449, "语音录音", "音频编码器", "声音特征", PLUM, PLUM_BG),
        (650, "文字提问", "文本编码", "文字表示", ORANGE, ORANGE_BG),
    )
    for y, source, encoder, feature, accent, wash in lanes:
        box(draw, (73, y, 383, y+154), "white", accent)
        box(draw, (562, y, 964, y+154), wash, accent)
        box(draw, (1135, y, 1458, y+154), "white", accent)
        if source == "发票照片":
            draw.rectangle((104, y+39, 165, y+111), outline=accent, width=4)
            for offset in (57, 76, 95):
                draw.line((113, y+offset, 154, y+offset), fill=accent, width=3)
        elif source == "语音录音":
            for i, height in enumerate((26, 65, 95, 45)):
                xx = 104+i*17
                draw.line((xx, y+75-height//2, xx, y+75+height//2), fill=accent, width=5)
        else:
            text(draw, 108, y+40, "?", 61, accent)
        text(draw, 183, y+43, source, 43)
        text(draw, 602, y+43, encoder, 49)
        text(draw, 1168, y+43, feature, 47)
        arrow(draw, 401, y+77, 545, accent)
        arrow(draw, 981, y+77, 1118, accent)
    footer(draw, "本例只走图片与文字两路；是否支持音频取决于具体模型。")
    save(image, "multimodal-encoding.png")


def principle():
    image, draw = base("LLaVA 原理 · 主文", "图像特征怎样接进语言模型")
    stages = (
        (70, 250, 345, 550, "发票照片", "像素输入", "white", TEAL),
        (439, 250, 723, 550, "视觉编码器", "提取图像特征", TEAL_BG, TEAL),
        (817, 250, 1118, 550, "可训练投影层", "映射到语言表示", PLUM_BG, PLUM),
    )
    for x1, y1, x2, y2, title, detail, fill, accent in stages:
        box(draw, (x1, y1, x2, y2), fill, accent)
        text(draw, x1+25, y1+78, title, 45, accent)
        text(draw, x1+25, y1+172, detail, 38, MUTED)
    arrow(draw, 359, 398, 423, TEAL)
    arrow(draw, 738, 398, 800, PLUM)
    box(draw, (1210, 250, 1471, 794), ORANGE_BG, ORANGE)
    text(draw, 1241, 338, "语言模型", 49)
    text(draw, 1241, 470, "接收两路", 41, MUTED)
    text(draw, 1241, 541, "生成候选", 41, MUTED)
    arrow(draw, 1130, 398, 1195, ORANGE)
    box(draw, (547, 657, 1118, 794), "white", LINE)
    text(draw, 582, 691, "提问：含税金额？", 46)
    arrow(draw, 1130, 725, 1195, ORANGE)
    footer(draw, "原理图依据 LLaVA 第 4.1 节；字段正确与否仍须核对原图。")
    save(image, "multimodal-principle.png")


def document():
    image, draw = base("单据版面 · 主文", "在原图上同时看读数、标签和位置")
    box(draw, (69, 245, 792, 852), "white", LINE)
    text(draw, 105, 278, "酒店发票（教学示意）", 50)
    draw.line((105, 362, 747, 362), fill=LINE, width=3)
    rows = (
        (392, "开票日期", "9/3", PLUM),
        (507, "含税金额", "680.00", TEAL),
        (622, "税额", "38.49", ORANGE),
    )
    for y, label, value, accent in rows:
        text(draw, 121, y, label, 45)
        text(draw, 472, y, value, 49, accent)
        draw.line((116, y+80, 743, y+80), fill=LINE, width=2)
    text(draw, 122, 773, "小字 / 印章在其他区域", 35, MUTED)
    callouts = (
        (275, "日期栏", "9/3；年份未知", PLUM_BG, PLUM, 434),
        (480, "金额栏", "680.00 对应含税金额", TEAL_BG, TEAL, 552),
        (685, "税额栏", "38.49 对应税额", ORANGE_BG, ORANGE, 666),
    )
    for y, heading, finding, fill, accent, source_y in callouts:
        box(draw, (911, y, 1462, y+156), fill, accent)
        text(draw, 943, y+17, heading, 39, accent)
        text(draw, 943, y+76, finding, 40)
        arrow(draw, 807, source_y, 895, accent)
    footer(draw, "数值要连同旁边标签核对；9/3 没有年份，不能补猜。")
    save(image, "multimodal-document.png")


def field_trace():
    image, draw = base("字段溯源 · 主文", "三个草稿字段分别指回哪块原图")
    box(draw, (71, 246, 570, 855), "white", LINE)
    box(draw, (1027, 246, 1464, 855), "white", LINE)
    text(draw, 112, 273, "发票原图", 47, TEAL)
    text(draw, 1066, 273, "报销草稿", 47, ORANGE)
    rows = (
        (383, "A", "含税金额", "680.00", TEAL),
        (559, "B", "税额", "38.49", PLUM),
        (735, "C", "日期", "9/3 · 年份未知", ORANGE),
    )
    for y, mark, field, value, accent in rows:
        draw.ellipse((101, y-11, 165, y+53), fill=accent)
        text(draw, 133, y+21, mark, 40, "white", "mm")
        text(draw, 187, y, field, 42)
        text(draw, 397 if mark != "A" else 385, y, value.split(" · ")[0], 42, accent)
        text(draw, 1066, y, field, 42)
        if mark == "C":
            text(draw, 1195, y-13, "9/3", 40, accent)
            text(draw, 1195, y+38, "年份未知", 32, accent)
        else:
            text(draw, 1195 if mark == "B" else 1278, y, value, 40, accent)
        arrow(draw, 587, y+27, 1011, accent)
    footer(draw, "A / B / C 是教学标记，不是实测坐标；缺失的年份不能出现。")
    save(image, "multimodal-field-trace-main.png")


def validation():
    image, draw = base("字段验证 · 主文", "同一张发票，分开核对读数与缺项")
    box(draw, (71, 247, 567, 853), "white", LINE)
    text(draw, 110, 288, "原图已知", 47, INK)
    for y, label, value in (
        (401, "含税金额", "680.00"),
        (535, "税额", "38.49"),
        (669, "日期", "9/3"),
    ):
        text(draw, 110, y, label, 44, MUTED)
        text(draw, 365, y, value, 46)
        draw.line((105, y+89, 530, y+89), fill=LINE, width=2)
    box(draw, (750, 253, 1464, 521), TEAL_BG, TEAL)
    text(draw, 791, 287, "金额与税额：可解析", 49, TEAL)
    text(draw, 791, 366, "仍要回原图核对标签和区域", 43)
    box(draw, (750, 576, 1464, 845), ORANGE_BG, ORANGE)
    text(draw, 791, 611, "日期 9/3：年份缺失", 49, ORANGE)
    text(draw, 791, 692, "草稿保留未知，不补成完整日期", 42)
    arrow(draw, 585, 399, 734, TEAL)
    arrow(draw, 585, 706, 734, ORANGE)
    footer(draw, "图像读数不是报销结论；是否通过另查制度与记录。")
    save(image, "multimodal-validation.png")


if __name__ == "__main__":
    for render in (encoding, principle, document, field_trace, validation):
        render()
