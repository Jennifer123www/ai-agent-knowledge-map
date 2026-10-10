"""Render system-level interview diagrams for the foundation-model overview.

All receipt, policy, and version labels are teaching constructions from the
paired articles. No score in these figures represents a measured model result.
"""

from math import atan2, cos, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1] / "content/wechat/01-foundation-models-and-inference/assets"
FONT = next(str(path) for path in (
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
) if path.exists())
W, H = 1536, 1024
PAPER = "#FBF8F3"
INK = "#273941"
MUTED = "#65757A"
LINE = "#D0DBD8"
PLUM = "#774660"
PLUM_PALE = "#F1E7EC"
TEAL = "#147B7A"
TEAL_PALE = "#E2F0ED"
ORANGE = "#C4773F"
ORANGE_PALE = "#FBF0E4"


def font(size):
    return ImageFont.truetype(FONT, size)


def write(draw, xy, value, size=34, color=INK, anchor="la"):
    draw.text(xy, value, font=font(size), fill=color, anchor=anchor)


def card(draw, bounds, fill="white", outline=LINE, radius=18):
    draw.rounded_rectangle(bounds, radius=radius, fill=fill, outline=outline, width=3)


def arrow(draw, start, end, color=TEAL, width=5):
    draw.line((start, end), fill=color, width=width)
    angle = atan2(end[1] - start[1], end[0] - start[0])
    draw.polygon([
        end,
        (end[0] - 17*cos(angle) + 10*sin(angle), end[1] - 17*sin(angle) - 10*cos(angle)),
        (end[0] - 17*cos(angle) - 10*sin(angle), end[1] - 17*sin(angle) + 10*cos(angle)),
    ], fill=color)


def base(kicker, title):
    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    write(draw, (82, 58), kicker, 29, PLUM)
    write(draw, (82, 111), title, 57)
    draw.line((82, 197, 1454, 197), fill=LINE, width=2)
    return image, draw


def save(image, name):
    ROOT.mkdir(parents=True, exist_ok=True)
    image.save(ROOT / name, optimize=True)


def architecture_ablation():
    image, draw = base("架构选择 / 控制变量", "两套方案先考同一张卷")
    card(draw, (94, 253, 1442, 364), "white")
    write(draw, (768, 307), "固定：票据样本 · 制度快照 · 权限 · 草稿字段", 36, INK, "mm")

    card(draw, (96, 424, 727, 692), PLUM_PALE, PLUM)
    write(draw, (135, 462), "方案 A  单模型", 38, PLUM)
    write(draw, (135, 533), "图片、问题、制度一起输入", 34)
    write(draw, (135, 595), "一次生成待核对草稿", 34)

    card(draw, (808, 424, 1439, 692), TEAL_PALE, TEAL)
    write(draw, (847, 462), "方案 B  分段处理", 38, TEAL)
    write(draw, (847, 533), "字段提取 → 候选资料 → 核适用", 34)
    write(draw, (847, 595), "再生成待核对草稿", 34)

    write(draw, (770, 744), "同一验收口径", 33, MUTED, "mm")
    labels = ["正确草稿", "无依据断言", "误提交", "尾部时延与成本"]
    for index, label in enumerate(labels):
        x0 = 98 + index * 355
        card(draw, (x0, 796, x0 + 316, 907), "white")
        write(draw, (x0 + 158, 851), label, 34, INK, "mm")
    save(image, "foundation-architecture-ablation.png")


def oracle_replay():
    image, draw = base("端到端评测 / 单点替换", "正确值从哪一站开始丢失")
    write(draw, (98, 255), "原回放", 33, PLUM)
    actual = [
        (98, "候选：含新版 500", TEAL_PALE, TEAL),
        (552, "上下文：仅旧版 450", PLUM_PALE, PLUM),
        (1006, "草稿：写成 450", PLUM_PALE, PLUM),
    ]
    for x0, label, fill, outline in actual:
        card(draw, (x0, 322, x0 + 426, 490), fill, outline)
        write(draw, (x0 + 213, 405), label, 35, INK, "mm")
    arrow(draw, (526, 405), (548, 405), PLUM)
    arrow(draw, (980, 405), (1002, 405), PLUM)

    draw.line((760, 510, 760, 588), fill=ORANGE, width=5)
    draw.polygon([(760, 598), (747, 574), (773, 574)], fill=ORANGE)
    card(draw, (327, 610, 1209, 711), ORANGE_PALE, ORANGE)
    write(draw, (768, 660), "只替换上下文：送入新版 500", 38, INK, "mm")

    card(draw, (105, 776, 715, 920), TEAL_PALE, TEAL)
    write(draw, (410, 823), "草稿变对", 38, TEAL, "mm")
    write(draw, (410, 873), "先查装配为何漏了新版", 31, INK, "mm")
    card(draw, (822, 776, 1431, 920), PLUM_PALE, PLUM)
    write(draw, (1126, 823), "草稿仍错", 38, PLUM, "mm")
    write(draw, (1126, 873), "继续查生成与结论校验", 31, INK, "mm")
    save(image, "foundation-oracle-replay.png")


def release_bundle():
    image, draw = base("组合发布 / 相容性", "技术版本成套，制度按日期适用")
    card(draw, (91, 261, 1444, 387), "white")
    write(draw, (226, 323), "8 月住宿", 36, PLUM, "mm")
    arrow(draw, (391, 323), (531, 323), PLUM)
    write(draw, (647, 323), "旧版 450", 36, PLUM, "mm")
    write(draw, (900, 323), "9 月住宿", 36, TEAL, "mm")
    arrow(draw, (1050, 323), (1160, 323), TEAL)
    write(draw, (1300, 323), "新版 500", 36, TEAL, "mm")

    card(draw, (94, 463, 717, 848), TEAL_PALE, TEAL)
    write(draw, (135, 505), "可联测的技术组合", 37, TEAL)
    write(draw, (135, 582), "查询编码器 E2  配  文档索引 I2", 33)
    write(draw, (135, 651), "制度快照 D2  配  生效规则 B2", 33)
    write(draw, (135, 749), "同一请求固定组合标识", 33, TEAL)

    card(draw, (816, 463, 1439, 848), PLUM_PALE, PLUM)
    write(draw, (857, 505), "不能直接混用", 37, PLUM)
    write(draw, (857, 582), "查询编码器 E2  配  旧索引 I1", 33)
    write(draw, (857, 651), "新制度 D2  配  旧规则 B1", 33)
    write(draw, (857, 749), "先回归，再决定能否切流", 33, PLUM)
    save(image, "foundation-release-bundle.png")


if __name__ == "__main__":
    architecture_ablation()
    oracle_replay()
    release_bundle()
