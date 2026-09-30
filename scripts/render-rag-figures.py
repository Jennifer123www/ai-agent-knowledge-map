"""Render reproducible Chinese teaching diagrams for the retrieval/RAG WeChat series.

Requires Pillow for authoring only; generated PNGs are the publishable assets.
"""

from math import atan2, cos, sin
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1] / "content/wechat/02-knowledge-retrieval-and-rag"
FONT_CANDIDATES = [
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
]
FONT_PATH = next((str(path) for path in FONT_CANDIDATES if path.exists()), None)
if FONT_PATH is None:
    raise RuntimeError("Install a Chinese font and add it to FONT_CANDIDATES before rendering")
W, H = 1536, 1024
PAPER, INK, MUTED = "#FAF8F3", "#22343A", "#64777B"
TEAL, LIGHT, ORANGE, ROSE = "#137B78", "#DFEEEA", "#D28642", "#A85F69"


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def text(draw, xy, value, size=32, color=INK, anchor=None):
    draw.text(xy, value, font=font(size), fill=color, anchor=anchor)


def panel(draw, box, fill="#FFFFFF", outline="#CADAD8", radius=22):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=3)


def arrow(draw, a, b, color=TEAL, width=6):
    draw.line((a, b), fill=color, width=width)
    x1, y1 = a
    x2, y2 = b
    if abs(x2-x1) > abs(y2-y1):
        sign = 1 if x2 > x1 else -1
        draw.polygon([(x2, y2), (x2-16*sign, y2-10), (x2-16*sign, y2+10)], fill=color)
    else:
        sign = 1 if y2 > y1 else -1
        draw.polygon([(x2, y2), (x2-10, y2-16*sign), (x2+10, y2-16*sign)], fill=color)


def diagonal_arrow(draw, a, b, color=TEAL, width=6):
    draw.line((a, b), fill=color, width=width)
    x1, y1 = a
    x2, y2 = b
    angle = atan2(y2-y1, x2-x1)
    head, wing = 17, 10
    draw.polygon([
        (x2, y2),
        (x2-head*cos(angle)+wing*sin(angle), y2-head*sin(angle)-wing*cos(angle)),
        (x2-head*cos(angle)-wing*sin(angle), y2-head*sin(angle)+wing*cos(angle)),
    ], fill=color)


def base(title, subtitle, tag):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 22, H), fill=TEAL)
    text(d, (86, 78), tag, 26, TEAL)
    text(d, (86, 130), title, 61)
    text(d, (88, 224), subtitle, 31, MUTED)
    d.line((86, 280, 1450, 280), fill="#C8DBD7", width=3)
    return im, d


def footer(d, note):
    d.line((86, 887, 1450, 887), fill="#C8DBD7", width=2)
    text(d, (90, 918), note, 28, MUTED)


def flow(path, title, subtitle, nodes, note, tag="结构图"):
    im, d = base(title, subtitle, tag)
    n = len(nodes)
    gap = 37
    x0, x1 = 90, 1445
    width = int((x1-x0-gap*(n-1))/n)
    for i, (head, detail) in enumerate(nodes):
        left = x0+i*(width+gap)
        panel(d, (left, 385, left+width, 685), LIGHT if i == n-1 else "#FFFFFF")
        d.ellipse((left+25, 411, left+73, 459), fill=TEAL if i<n-1 else ORANGE)
        text(d, (left+49, 436), str(i+1), 25, "#FFFFFF", "mm")
        text(d, (left+25, 510), head, 34)
        text(d, (left+25, 575), detail, 25, MUTED)
        if i < n-1:
            arrow(d, (left+width+5, 538), (left+width+gap-7, 538), ORANGE)
    footer(d, note)
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, optimize=True)


def compare(path, title, subtitle, left, right, note):
    im, d = base(title, subtitle, "并列对照")
    for i, (head, details) in enumerate([left, right]):
        x = 90 if i == 0 else 780
        panel(d, (x, 363, x+645, 806), LIGHT if i == 0 else "#FFF2E5")
        text(d, (x+34, 402), head, 43, TEAL if i == 0 else ORANGE)
        for j, line in enumerate(details):
            d.ellipse((x+41, 508+j*80, x+53, 520+j*80), fill=TEAL if i == 0 else ORANGE)
            text(d, (x+72, 487+j*80), line, 29)
    footer(d, note)
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, optimize=True)


def criteria(path, title, subtitle, items, note, tag="并列核对"):
    """Show independent fields or decision branches without false time arrows."""
    im, d = base(title, subtitle, tag)
    count = len(items)
    gap = 30
    left, right = 90, 1445
    width = (right-left-gap*(count-1))//count
    for i, (heading, detail) in enumerate(items):
        x = left+i*(width+gap)
        panel(d, (x, 392, x+width, 735), LIGHT if i == count-1 else "#FFFFFF")
        d.rectangle((x+26, 430, x+35, 490), fill=TEAL if i < count-1 else ORANGE)
        text(d, (x+55, 425), heading, 38 if count == 3 else 34)
        text(d, (x+55, 573), detail, 29 if count == 3 else 25, MUTED)
    footer(d, note)
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, optimize=True)


def source_map():
    im, d = base("证据与查找结构不是一回事", "原文是依据；图与索引帮助找到它", "来源关系")
    for box, label, fill in [
        ((90, 380, 370, 500), "制度原文", "#FFFFFF"),
        ((90, 590, 370, 710), "业务系统", "#FFFFFF"),
        ((555, 460, 945, 630), "可核验的来源", LIGHT),
        ((1110, 380, 1440, 500), "关系图：关联路径", "#FFFFFF"),
        ((1110, 590, 1440, 710), "检索索引：查找入口", "#FFFFFF"),
    ]:
        panel(d, box, fill)
        text(d, ((box[0]+box[2])//2, (box[1]+box[3])//2), label, 31, INK, "mm")
    for a, b in [((381, 440), (544, 515)), ((381, 650), (544, 580)),
                 ((956, 520), (1099, 440)), ((956, 570), (1099, 650))]:
        diagonal_arrow(d, a, b, TEAL)
    text(d, (1030, 781), "右侧是衍生结构，不替代原始来源", 28, ORANGE)
    footer(d, "回答中的断言应回到制度原文或业务系统核对")
    im.save(ROOT / "assets/overview-sources.png", optimize=True)


def parallel_retrieval():
    im, d = base("两条召回路并行", "关键词保留精确字面，向量寻找近义表达", "合并候选")
    for box, label, fill in [
        ((90, 515, 340, 645), "检索问题", "#FFFFFF"),
        ((500, 365, 815, 495), "关键词召回", LIGHT),
        ((500, 670, 815, 800), "向量召回", LIGHT),
        ((1005, 515, 1440, 645), "合并去重 → 候选集", "#FFF2E5"),
    ]:
        panel(d, box, fill)
        text(d, ((box[0]+box[2])//2, (box[1]+box[3])//2), label, 33, INK, "mm")
    d.line((351, 580, 420, 580, 420, 430), fill=TEAL, width=5)
    d.line((420, 580, 420, 735), fill=TEAL, width=5)
    arrow(d, (420, 430), (489, 430), TEAL)
    arrow(d, (420, 735), (489, 735), TEAL)
    d.line((826, 430, 925, 430, 925, 580), fill=ORANGE, width=5)
    d.line((826, 735, 925, 735, 925, 580), fill=ORANGE, width=5)
    arrow(d, (925, 580), (994, 580), ORANGE)
    footer(d, "候选合并后，再判断权限、有效期与最终排序")
    out = ROOT / "submodules/05-retrieval/assets/retrieval-candidates.png"
    im.save(out, optimize=True)


def citation_map():
    im, d = base("每句话各找自己的证据", "制度链接不能证明票据金额，更不能证明审批状态", "断言—证据")
    rows = [
        ("票面是 480 元", "票据字段", TEAL),
        ("新版上限 500 元", "生效条款", TEAL),
        ("已完成审批", "尚无证据 · 待核", ROSE),
    ]
    for i, (claim, source, color) in enumerate(rows):
        y = 362+i*160
        panel(d, (95, y, 650, y+115), "#FFFFFF")
        panel(d, (900, y, 1435, y+115), LIGHT if i < 2 else "#FFF2E5")
        text(d, (370, y+57), claim, 32, INK, "mm")
        text(d, (1165, y+57), source, 32, color, "mm")
        arrow(d, (660, y+57), (890, y+57), color)
    footer(d, "没有独立证据的断言只能标待核，不能写成已完成")
    out = ROOT / "submodules/03-rag/assets/rag-citation.png"
    im.save(out, optimize=True)


def principle(path, title, subtitle, kind, note):
    im, d = base(title, subtitle, "论文机制改绘")
    if kind == "overview":
        # Figure 1: the query feeds both retrieval and generation; retrieved
        # documents are external memory, while the generator has parameters.
        for box, label, fill in [
            ((91, 389, 305, 525), "问题 x", "#FFFFFF"),
            ((390, 389, 660, 525), "查询编码器", "#FFFFFF"),
            ((745, 389, 1015, 525), "文档向量索引", LIGHT),
            ((1100, 389, 1445, 525), "Top-k 候选文档", LIGHT),
            ((670, 670, 1100, 790), "生成模型（参数知识）", "#FFF2E5"),
            ((1205, 670, 1445, 790), "回答", "#FFFFFF"),
        ]:
            panel(d, box, fill)
            text(d, ((box[0]+box[2])//2, (box[1]+box[3])//2), label, 31, INK, "mm")
        for a, b in [((315, 457), (379, 457)), ((670, 457), (734, 457)),
                     ((1025, 457), (1089, 457)), ((1110, 729), (1194, 729))]:
            arrow(d, a, b, ORANGE)
        d.line((198, 535, 198, 727, 652, 727), fill=TEAL, width=5)
        arrow(d, (615, 727), (659, 727), TEAL)
        d.line((1273, 535, 1273, 618, 885, 618), fill=TEAL, width=5)
        arrow(d, (885, 618), (885, 659), TEAL)
        text(d, (91, 825), "同一问题进入检索器和生成器；候选文档在生成前参与回答。", 28, TEAL)
    elif kind == "rag":
        # RAG-Sequence: document-conditioned predictions are weighted by
        # retrieval probabilities. This is not the generic prompt-stuffing flow.
        for box, label, fill in [
            ((100, 339, 325, 435), "问题 x", "#FFFFFF"),
            ((405, 339, 665, 435), "查询编码器", "#FFFFFF"),
            ((755, 339, 1100, 435), "Top-k 候选", LIGHT),
            ((1165, 339, 1430, 435), "文档向量索引", "#FFFFFF"),
            ((110, 515, 432, 605), "x + 候选片段 z1", "#FFFFFF"),
            ((110, 643, 432, 733), "x + 候选片段 z2", "#FFFFFF"),
            ((527, 515, 815, 605), "生成模型", LIGHT),
            ((527, 643, 815, 733), "生成模型", LIGHT),
            ((915, 515, 1385, 605), "输出概率 1 × 检索权重 1", "#FFFFFF"),
            ((915, 643, 1385, 733), "输出概率 2 × 检索权重 2", "#FFFFFF"),
            ((915, 781, 1385, 860), "按检索概率加权合并", "#FFF2E5"),
        ]:
            panel(d, box, fill)
            text(d, ((box[0]+box[2])//2, (box[1]+box[3])//2), label, 28, INK, "mm")
        for a, b in [((336, 387), (394, 387)), ((676, 387), (744, 387)),
                     ((1154, 387), (1111, 387)), ((443, 560), (516, 560)),
                     ((443, 688), (516, 688)), ((826, 560), (904, 560)),
                     ((826, 688), (904, 688))]:
            arrow(d, a, b, ORANGE)
        d.line((885, 445, 885, 476, 80, 476, 80, 688), fill=TEAL, width=5)
        arrow(d, (80, 560), (99, 560), TEAL)
        arrow(d, (80, 688), (99, 688), TEAL)
        d.line((1398, 560, 1435, 560, 1435, 817), fill=ORANGE, width=5)
        d.line((1398, 688, 1435, 688), fill=ORANGE, width=5)
        arrow(d, (1435, 817), (1395, 817), ORANGE)
        text(d, (115, 803), "原论文 RAG-Sequence", 26, TEAL)
        text(d, (115, 840), "工程常见的证据拼接是相关实现，不等于此公式。", 24, MUTED)
    elif kind == "kb":
        text(d, (100, 330), "离线：把资料编码并建立索引", 29, TEAL)
        text(d, (100, 580), "在线：把问题编码后比较取回", 29, ORANGE)
        for box, label, fill in [
            ((100, 384, 336, 515), "文档片段 z", "#FFFFFF"),
            ((428, 384, 680, 515), "文档编码器", "#FFFFFF"),
            ((788, 364, 1408, 535), "向量索引：d(z) + 文档 ID", LIGHT),
            ((100, 628, 336, 754), "查询问题 x", "#FFFFFF"),
            ((428, 628, 680, 754), "查询编码器", "#FFFFFF"),
            ((788, 628, 1090, 754), "相似度 → Top-k", "#FFF2E5"),
            ((1182, 628, 1435, 754), "取回原文位置", "#FFFFFF"),
        ]:
            panel(d, box, fill)
            text(d, ((box[0]+box[2])//2, (box[1]+box[3])//2), label, 29, INK, "mm")
        for a, b in [((347, 449), (417, 449)), ((691, 449), (777, 449)),
                     ((347, 690), (417, 690)), ((691, 690), (777, 690)),
                     ((1101, 690), (1171, 690)), ((1098, 544), (1098, 617))]:
            arrow(d, a, b, ORANGE)
        text(d, (110, 819), "工程补充：文档 ID 还应关联版本、权限与出处。", 26, TEAL)
    elif kind == "kg":
        text(d, (102, 327), "离线建图与预生成摘要", 26, TEAL)
        for box, label in [((100, 363, 312, 457), "源文本"),
                           ((395, 363, 664, 457), "实体关系图"),
                           ((750, 363, 1019, 457), "社区划分")]:
            panel(d, box, LIGHT if label == "实体关系图" else "#FFFFFF")
            text(d, ((box[0]+box[2])//2, 410), label, 29, INK, "mm")
        arrow(d, (323, 410), (384, 410), ORANGE)
        arrow(d, (675, 410), (739, 410), ORANGE)
        for box, label in [((445, 530, 735, 615), "社区 A 摘要"),
                           ((845, 530, 1135, 615), "社区 B 摘要"),
                           ((91, 687, 342, 785), "全局问题"),
                           ((445, 687, 735, 785), "局部回答 A"),
                           ((845, 687, 1135, 785), "局部回答 B"),
                           ((1220, 687, 1450, 785), "汇总回答")]:
            panel(d, box, "#FFF2E5" if label == "汇总回答" else "#FFFFFF")
            text(d, ((box[0]+box[2])//2, (box[1]+box[3])//2), label, 28, INK, "mm")
        d.line((884, 466, 884, 490, 590, 490), fill=TEAL, width=5)
        d.line((884, 490, 990, 490), fill=TEAL, width=5)
        arrow(d, (590, 490), (590, 519), TEAL)
        arrow(d, (990, 490), (990, 519), TEAL)
        diagonal_arrow(d, (590, 625), (620, 676), ORANGE)
        diagonal_arrow(d, (990, 625), (1020, 676), ORANGE)
        arrow(d, (353, 736), (434, 736), TEAL)
        d.line((216, 676, 216, 650, 900, 650), fill=TEAL, width=5)
        text(d, (560, 618), "同题分发", 22, TEAL)
        arrow(d, (900, 650), (900, 676), TEAL)
        d.line((746, 736, 779, 736, 779, 822, 1185, 822, 1185, 736), fill=ORANGE, width=5)
        arrow(d, (1146, 736), (1209, 736), ORANGE)
        text(d, (105, 829), "工程补充：具体条款仍要回原文核验。", 25, TEAL)
    elif kind == "chunk":
        panel(d, (90, 355, 745, 824), LIGHT)
        panel(d, (790, 355, 1445, 824), "#FFF2E5")
        text(d, (122, 386), "RAPTOR：分层摘要", 32, TEAL)
        text(d, (822, 386), "工程策略：父子定位", 32, ORANGE)
        panel(d, (288, 468, 545, 540), "#FFFFFF")
        text(d, (417, 504), "上层主题摘要", 26, TEAL, "mm")
        for x, h in [(166, "主题 A"), (456, "主题 B")]:
            panel(d, (x, 622, x+207, 689), "#FFFFFF")
            text(d, (x+103, 655), h, 25, INK, "mm")
            diagonal_arrow(d, (x+103, 611), (417, 550), TEAL, 4)
        for x in (152, 300, 451, 599):
            panel(d, (x, 735, x+105, 788), "#FFFFFF")
            text(d, (x+52, 761), "片段", 20, MUTED, "mm")
            diagonal_arrow(d, (x+52, 728), (269 if x < 450 else 559, 699), TEAL, 3)
        panel(d, (911, 467, 1325, 548), "#FFFFFF")
        text(d, (1118, 507), "父条款：条件完整", 26, ORANGE, "mm")
        for x, h in [(862, "子片段 1"), (1174, "子片段 2")]:
            panel(d, (x, 640, x+230, 715), "#FFFFFF")
            text(d, (x+115, 677), h, 25, INK, "mm")
            diagonal_arrow(d, (x+115, 627), (1118, 557), ORANGE, 4)
        text(d, (862, 757), "命中子片段 → 返回父条款", 25, ORANGE)
    elif kind == "retrieval":
        panel(d, (90, 360, 722, 787), LIGHT)
        panel(d, (814, 360, 1445, 787), "#FFF2E5")
        text(d, (125, 396), "双编码器：先广泛召回", 32, TEAL)
        text(d, (850, 396), "联合编码：再细读候选", 32, ORANGE)
        for x, h in [(158, "问题"), (450, "文档")]:
            panel(d, (x, 501, x+210, 584), "#FFFFFF")
            text(d, (x+105, 542), h, 28, INK, "mm")
            arrow(d, (x+105, 593), (x+105, 648), TEAL)
        text(d, (215, 694), "问题向量", 29, TEAL)
        text(d, (512, 694), "文档向量", 29, TEAL)
        text(d, (273, 746), "相似度选 Top-k", 23, TEAL)
        panel(d, (882, 501, 1374, 590), "#FFFFFF")
        text(d, (1128, 545), "问题 + 候选片段", 30, INK, "mm")
        arrow(d, (1128, 598), (1128, 650), ORANGE)
        text(d, (970, 701), "逐对评分 → 排序", 30, ORANGE)
    footer(d, note)
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, optimize=True)


def main():
    flows = [
        ("assets/overview-cover.png", "知识检索与 RAG", "先找证据，再组织回答", [("业务问题", "480 元能报吗"), ("找到资料", "新版与旧版"), ("有限结论", "附出处待核验")], "示意案例：制度与金额均为虚构"),
        ("assets/overview-route.png", "五段接力怎样走", "资料进入回答之前，要经过选择与核对", [("知识库", "原文与版本"), ("分段", "可定位证据"), ("检索", "选适用条款"), ("生成", "回答附出处")], "知识图谱按需加入，不是每个问题的必经站"),
        ("submodules/01-knowledgebase/assets/kb-cover.png", "知识库：先管好资料", "文件进库不等于问题就能答对", [("定来源", "谁负责发布"), ("留版本", "何时生效"), ("建索引", "可查可回溯")], "把制度当作有生命周期的知识资产"),
        ("submodules/01-knowledgebase/assets/kb-version.png", "制度按生效日判断", "旧版和新版同时存在，并非只留最新一份", [("旧版", "上限 450 元"), ("9 月 1 日", "新版生效"), ("新版", "上限 500 元")], "示意数值；查询还需匹配地点、职级和日期"),
        ("submodules/01-knowledgebase/assets/kb-refresh.png", "更新与撤回同样重要", "索引不能比原文多活一辈子", [("发布", "记录版本"), ("更新", "重建索引"), ("撤回", "停止返回")], "回看审计日志，确认旧数据是否仍可被查到"),
        ("submodules/02-knowledgegraph/assets/kg-cover.png", "知识图谱：把关系讲明白", "有些问题不缺片段，缺的是连接线", [("识别实体", "员工与部门"), ("连接关系", "适用何制度"), ("核对原文", "落到哪一条")], "图谱给路径，原文给证据"),
        ("submodules/02-knowledgegraph/assets/kg-query.png", "沿关系找适用条款", "多跳查询要把每一步的出处带回来", [("员工", "属于研发部"), ("研发部", "适用差旅规"), ("条款", "北京住宿")], "任何一条边过期，路径都可能失效"),
        ("submodules/03-rag/assets/rag-cover.png", "RAG：先查再答", "把外部证据带进当前回答", [("提出问题", "要判断什么"), ("取回证据", "哪个版本适用"), ("生成回答", "每句可核验")], "RAG 并不保证检索和理解永远正确"),
        ("submodules/04-chunking/assets/chunk-cover.png", "分段：别把例外切丢", "切开前先看文档的骨架", [("识别结构", "标题与表格"), ("保存条件", "例外与脚注"), ("形成片段", "能回原文")], "块太小会丢条件，块太大不易定位"),
        ("submodules/04-chunking/assets/chunk-document.png", "先解析，再分段", "文档顺序比固定字数更重要", [("版面", "页眉表格脚注"), ("结构", "章节与条款"), ("证据", "条件完整片段")], "跨页表格的标题不能留在上一页"),
        ("submodules/05-retrieval/assets/retrieval-cover.png", "检索：找得到，也要选得对", "让当前有效的证据走到前面", [("广泛召回", "别漏目标"), ("硬过滤", "排除不适用"), ("精细排序", "优先有用片段")], "最相似不一定最适用"),
        ("submodules/05-retrieval/assets/retrieval-filter.png", "硬条件先过闸", "分数高也不能越过权限和生效期", [("权限", "此人可见"), ("适用", "地点与职级"), ("时间", "当日已生效")], "过滤条件要随查询身份进入日志与评测"),
        ("submodules/05-retrieval/assets/retrieval-citation.png", "引用回到原文", "片段 ID 不等于可供读者核对的地址", [("候选片段", "保存稳定 ID"), ("来源定位", "文档页码条款"), ("展示引用", "读者可打开")], "引用打开后须与回答中的断言相匹配"),
        ("submodules/05-retrieval/assets/retrieval-metrics.png", "分开衡量召回与排序", "不要只看最终回答是否好听", [("候选召回", "正确条款在吗"), ("前列排序", "是否排得够前"), ("引用核验", "能否定位出处")], "每项指标都要有问题集、证据标注和分母"),
    ]
    for spec in flows:
        flow(*spec)
    compares = [
        ("assets/overview-boundary.png", "三种常见失效", "错误来自资料、权限与信息缺口，不是一种毛病", ("旧版制度", ["先比生效日期", "再看适用地区", "不可误用旧规则"]), ("无权或缺值", ["权限不足就不泄露", "关键字段缺失就追问", "不能假装已核验"]), "把错误分开记录，修复才会落到正确环节"),
        ("submodules/01-knowledgebase/assets/kb-access.png", "看得见由谁决定", "知识库记录要保留访问范围", ("资料侧", ["来源标注权限域", "撤回时连索引失效", "保留审计记录"]), ("查询侧", ["按当前身份过滤", "结果只含可见资料", "不把权限交给模型猜"]), "权限控制发生在检索之前，不靠生成模型遮掩"),
        ("submodules/02-knowledgegraph/assets/kg-sources.png", "三类知识源", "不同资料适合回答不同问题", ("原文与业务表", ["原文给完整条款", "业务表给当前状态", "都要有责任来源"]), ("知识图谱", ["记录实体间关系", "适合多跳路径", "结论仍回原文"]), "向量索引是查找结构，不是另一份权威事实"),
        ("submodules/02-knowledgegraph/assets/kg-contrast.png", "语义相近与关系成立", "两种证据路线不能互相冒充", ("向量索引", ["找相似措辞", "适合模糊问法", "相似不等于适用"]), ("关系图谱", ["走实体与关系", "适合多跳问法", "边需要出处与时间"]), "选型看问题类型，不看哪个名词更新潮"),
        ("submodules/03-rag/assets/rag-citation.png", "断言逐条挂证据", "引用不是放在段末的装饰", ("能证实", ["480 元来自票据", "500 元来自新版条款", "日期满足生效条件"]), ("尚待核", ["发票真伪未知", "审批状态未知", "不能写已提交"]), "回答边界不超过证据边界"),
        ("submodules/04-chunking/assets/chunk-error.png", "错误切法与正确切法", "把例外与主条款拆散，会改变读者看到的含义", ("错误：分离", ["片段 A：上限 500", "片段 B：仅 A 职级", "单看 A 会过度概括"]), ("正确：连贯", ["同一证据单元", "或有父条款链接", "查询时补足条件"]), "目标不是最大限度切碎，而是让每块可用于判断"),
    ]
    for spec in compares:
        compare(*spec)
    criteria("assets/overview-evaluation.png", "系统验收看四件事", "四项分别评测，不能用最终答案遮住中间错误", [("来源", "权威且更新"), ("检索", "证据进候选"), ("生成", "断言有支持"), ("治理", "权限不越界")], "各项有独立指标和失败记录")
    criteria("submodules/01-knowledgebase/assets/kb-source.png", "源头先说清", "每份资料同时记录三类信息", [("原始来源", "文件或业务表"), ("责任人", "谁批准更新"), ("可用范围", "谁能看到")], "这三项是并列字段，不是处理步骤", "资料档案")
    criteria("submodules/02-knowledgegraph/assets/kg-provenance.png", "关系也需要证据", "一条边同时保存关系、出处与审核状态", [("关系", "部门适用制度"), ("出处", "发布文件位置"), ("状态", "已核或待核")], "抽取得到的边不能自动升级为权威事实", "关系档案")
    criteria("submodules/03-rag/assets/rag-question.png", "先拆问题，再下结论", "“能报吗”至少包含四个待核事实", [("票据", "金额与日期"), ("员工", "职级和部门"), ("制度", "地区与生效期"), ("状态", "审批是否完成")], "四类事实分别找来源；缺失时追问或停判", "并列待核")
    criteria("submodules/03-rag/assets/rag-context.png", "证据包不能只放原文", "每个检索片段应附带适用条件和出处", [("条款正文", "金额上限"), ("适用范围", "职级与地点"), ("版本来源", "生效日与链接")], "旧版与新版冲突时，先判适用性再概括", "证据包字段")
    criteria("submodules/03-rag/assets/rag-abstain.png", "证据决定回答边界", "三种状态对应三种处理，彼此不是先后步骤", [("证据足够", "给有限结论"), ("证据冲突", "指出冲突"), ("条件缺失", "追问或停答")], "拒答不是失败；编造肯定结论才是失败", "分支判断")
    criteria("submodules/04-chunking/assets/chunk-metadata.png", "片段的随身证件", "每个片段同时保留三类元数据", [("来源", "文档与页码"), ("适用", "时间与权限"), ("定位", "条款与父节点")], "元数据丢失后，检索相似度无法补救", "片段字段")
    criteria("submodules/04-chunking/assets/chunk-test.png", "分段怎样验收", "三项分别检查，不能用一项替代另一项", [("可召回", "命中目标条款"), ("可理解", "条件不缺失"), ("可定位", "回原文核对")], "用普通、冲突、缺值、新增四类问题抽检")
    source_map()
    parallel_retrieval()
    citation_map()
    principles = [
        ("assets/overview-principle.png", "问题怎样借外部资料回答", "原始 RAG：问题既触发检索，也进入生成模型", "overview", "依据 Lewis 等 Figure 1 改绘；引用与权限是工程补充"),
        ("submodules/01-knowledgebase/assets/kb-principle.png", "外部资料如何成为可查索引", "资料治理补在原始 RAG 文档索引之前", "kb", "依据 Lewis 等 Figure 1 的文档索引部分改绘"),
        ("submodules/02-knowledgegraph/assets/kg-principle.png", "GraphRAG 怎样做全局归纳", "图与社区摘要适合跨材料主题问题", "kg", "依据 Edge 等 Figure 1 改绘；具体条款需回原文"),
        ("submodules/03-rag/assets/rag-principle.png", "候选文档怎样影响生成", "原论文 RAG-Sequence：按检索概率合并候选输出", "rag", "依据 Lewis 等 Figure 1、§2.1 改绘；引用是工程扩展"),
        ("submodules/04-chunking/assets/chunk-principle.png", "长文怎样保留不同尺度", "分层摘要与父子定位是两种不同策略", "chunk", "左侧依据 RAPTOR Figure 1 改绘；右侧父子定位为另一路线"),
        ("submodules/05-retrieval/assets/retrieval-principle.png", "先快找，再细排", "双编码器召回与联合编码重排并不相同", "retrieval", "依据 DPR §2.1 与 Passage Re-ranking with BERT §2 改绘"),
    ]
    for spec in principles:
        principle(*spec)


if __name__ == "__main__":
    main()
