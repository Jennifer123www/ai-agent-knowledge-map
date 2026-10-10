"""Render a deterministic paired-test diagram for the LLM interview article."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parents[1] / "content/wechat/01-foundation-models-and-inference/submodules/01-llm/assets/llm-paired-invariance.png"
FONT = next(str(path) for path in (
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
) if path.exists())
W, H = 1536, 1024
PAPER, INK, MUTED, LINE = "#FBF8F3", "#273941", "#65757A", "#D0DBD8"
TEAL, TEAL_PALE = "#147B7A", "#E2F0ED"
PLUM, PLUM_PALE = "#774660", "#F1E7EC"
ORANGE, ORANGE_PALE = "#C4773F", "#FBF0E4"


def font(size):
    return ImageFont.truetype(FONT, size)


def write(draw, xy, value, size=34, color=INK, anchor="la"):
    draw.text(xy, value, font=font(size), fill=color, anchor=anchor)


def box(draw, bounds, fill="white", outline=LINE):
    draw.rounded_rectangle(bounds, radius=18, fill=fill, outline=outline, width=3)


image = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(image)
write(d, (82, 57), "面试评测 / 成对样本", 29, PLUM)
write(d, (82, 111), "只改一个条件，检查应变与不应变", 54)
d.line((82, 195, 1454, 195), fill=LINE, width=2)

rows = [
    (245, TEAL, TEAL_PALE, "只改会议时间", "时间字段改为新值", "方式、链接、草稿状态不变"),
    (474, ORANGE, ORANGE_PALE, "只补真实链接", "链接由空值变为已核实地址", "不能顺带写成已发送"),
    (703, PLUM, PLUM_PALE, "只改动作授权", "动作状态按授权和回执更新", "时间、方式与链接不变"),
]
for y, color, pale, change, should, must_not in rows:
    box(d, (91, y, 1445, y + 183), "white")
    box(d, (112, y + 23, 480, y + 159), pale, color)
    write(d, (296, y + 91), change, 35, color, "mm")
    write(d, (532, y + 46), "应变", 29, TEAL)
    write(d, (532, y + 110), should, 34)
    write(d, (1042, y + 46), "不应变", 29, PLUM)
    write(d, (1042, y + 110), must_not, 32)

OUT.parent.mkdir(parents=True, exist_ok=True)
image.save(OUT, optimize=True)
