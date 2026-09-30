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


def encoding():
    im, d = base("不同输入，先各自编码", "输入编码 · 主文")
    for y, name, route, result, fill in (
        (260, "发票照片", "视觉编码器", "图像特征", TEAL_BG),
        (574, "语音录音", "音频编码器", "声音特征", PLUM_BG),
        (888, "文字提问", "文本编码", "文字表示", ORANGE_BG),
    ):
        card(d, y, 235, name, (f"{route}  →  {result}",), fill)
    arrow(d, 1134, 1192, "按任务对齐或融合")
    ribbon(d, 1210, ("这张发票只使用图片和文字两路；", "并非每个模型都支持全部输入。"), TEAL_BG)
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
    ribbon(d, 1210, ("只读出 680.00 和 38.49，", "还不能确定各自属于哪个字段。"))
    save(im, "multimodal-document.png")


def field_trace():
    im, d = base("每个字段都能指回原图", "字段溯源 · 主副文共用")
    items = (
        (258, "A · 含税金额", "原图标签 + 680.00", "草稿：含税金额 680.00", TEAL_BG),
        (584, "B · 税额", "原图标签 + 38.49", "草稿：税额 38.49", PLUM_BG),
        (910, "C · 开票日期", "原图只写 9/3", "草稿：9/3；年份未知", ORANGE_BG),
    )
    for y, heading, source, target, color in items:
        card(d, y, 274, heading, (source, "↓", target), color)
    ribbon(d, 1254, ("A / B / C 是示意区域，", "不是实测坐标；草稿仍需复核。"), TEAL_BG)
    save(im, "multimodal-field-trace.png")


def validation():
    im, d = base("能读到，不等于能通过", "字段验证 · 主文")
    card(d, 270, 397, "金额与税额", ("680.00 / 38.49 可以解析", "核对各自标签与原图区域", "→ 保留读数，等待复核"), TEAL_BG)
    card(d, 720, 397, "开票日期", ("原图只有 9/3", "缺少年份，不能补成完整日期", "→ 保留 9/3；年份未知"), ORANGE_BG)
    ribbon(d, 1196, ("能否报销，还要依据制度和记录；", "图片本身不能证明审批通过。"), PLUM_BG)
    save(im, "multimodal-validation.png")


def alignment():
    im, d = base("缩掉的小字，连接层救不回", "视觉连接 · 面试")
    ribbon(d, 258, ("同一张发票：680.00、38.49", "以及旁边的字段标签。"), "white")
    card(d, 428, 329, "路径 A：整页缩得过小", ("小字或小数点可能消失", "视觉编码器得到残缺特征", "连接层不能补回丢失像素"), ORANGE_BG)
    card(d, 807, 329, "路径 B：金额栏局部放大", ("同时保留数字与字段标签", "视觉编码器取得更清晰特征", "接入语言模型后仍需复核"), TEAL_BG)
    ribbon(d, 1208, ("连接层映射已有特征；", "原图信息损失须在输入端处理。"), PLUM_BG)
    save(im, "multimodal-alignment.png")


def ocr_vlm():
    im, d = base("认出字符 ≠ 填对字段", "OCR 与 VLM · 面试")
    ribbon(d, 257, ("同一张发票：680.00、38.49、9/3" ,), "white")
    card(d, 390, 242, "OCR（光学字符识别）", ("读出字符和文字框位置", "检查：数字是否读对？"), PLUM_BG)
    card(d, 680, 242, "VLM（视觉语言模型）", ("给出字段关系候选", "检查：金额和税额是否填反？"), TEAL_BG)
    arrow(d, 934, 991)
    ribbon(d, 1010, ("合并证据，回到原图复核；", "两者一致也不能补出年份。"), ORANGE_BG)
    save(im, "multimodal-ocr-vlm.png")


def diagnosis():
    im, d = base("错在看不清，还是配不对", "错误诊断 · 面试")
    for y, title, lines, fill in (
        (258, "缩图过度", ("小字或小数点丢失", "处理：放大原图金额栏"), PLUM_BG),
        (609, "标签与数值拆开", ("680.00 失去“含税金额”标签", "处理：连同行列与坐标复核"), TEAL_BG),
        (960, "日期缺项", ("9/3 没写年份", "处理：年份标未知，不补猜"), ORANGE_BG),
    ):
        card(d, y, 288, title, lines, fill)
    save(im, "multimodal-document-diagnosis.png")


def evaluation():
    im, d = base("把三类错误分开评", "分层评测 · 面试")
    for y, title, lines, fill in (
        (258, "字符读错", ("看：金额字符准确率", "查：原图质量与识别区域"), PLUM_BG),
        (609, "字段填反", ("看：字段归属与区域定位", "查：标签、行列与坐标"), TEAL_BG),
        (960, "无据补年份", ("看：缺项保留是否正确", "查：9/3 是否仍为年份未知"), ORANGE_BG),
    ):
        card(d, y, 288, title, lines, fill)
    save(im, "multimodal-evaluation.png")


if __name__ == "__main__":
    for make in (encoding, principle, document, field_trace, validation,
                 alignment, ocr_vlm, diagnosis, evaluation):
        make()
