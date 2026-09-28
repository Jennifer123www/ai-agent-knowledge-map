"""Render reproducible Chinese teaching diagrams for the retrieval/RAG WeChat series.

Requires Pillow for authoring only; generated PNGs are the publishable assets.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1] / "content/wechat/knowledge-retrieval-and-rag"
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


def network(path, title, subtitle, center, leaves, note):
    im, d = base(title, subtitle, "关系图")
    cx, cy = 767, 575
    coords = [(290, 435), (1220, 435), (290, 715), (1220, 715)]
    for (label, detail), (x, y) in zip(leaves, coords):
        panel(d, (x-185, y-67, x+185, y+67), "#FFFFFF")
        text(d, (x, y-18), label, 34, INK, "mm")
        text(d, (x, y+28), detail, 23, MUTED, "mm")
        arrow(d, (x+190 if x < cx else x-190, y), (cx-195 if x < cx else cx+195, cy-30 if y < cy else cy+30), TEAL, 5)
    panel(d, (cx-190, cy-87, cx+190, cy+87), LIGHT, TEAL, 31)
    text(d, (cx, cy), center, 40, TEAL, "mm")
    footer(d, note)
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, optimize=True)


def principle(path, title, subtitle, kind, note):
    im, d = base(title, subtitle, "论文机制改绘")
    if kind == "rag":
        boxes = [(105, 415, 305, 575, "问题"), (378, 415, 612, 575, "查询编码"),
                 (685, 415, 916, 575, "文档索引"), (987, 415, 1200, 575, "候选证据"),
                 (1240, 415, 1450, 575, "生成回答")]
        for x0, y0, x1, y1, label in boxes:
            panel(d, (x0, y0, x1, y1), LIGHT if label in ("候选证据", "生成回答") else "#FFFFFF")
            text(d, ((x0+x1)//2, (y0+y1)//2), label, 33, INK, "mm")
        for (x0, _, x1, _, _), (xx0, _, _, _, _) in zip(boxes, boxes[1:]):
            arrow(d, (x1+7, 495), (xx0-9, 495), ORANGE)
        panel(d, (668, 667, 943, 773), "#FFF2E5")
        text(d, (805, 720), "来源文档", 32, ORANGE, "mm")
        arrow(d, (805, 661), (805, 585), ORANGE)
        text(d, (1100, 690), "出处随证据传递", 29, TEAL)
    elif kind == "kb":
        flow_boxes = [(100, "来源文档", "权威原文"), (455, "解析记录", "文本与版面"), (810, "文档索引", "可被查找"), (1165, "查询取回", "回到原文")]
        for x, h, sub in flow_boxes:
            panel(d, (x, 432, x+260, 641), LIGHT if x == 810 else "#FFFFFF")
            text(d, (x+24, 483), h, 31)
            text(d, (x+24, 554), sub, 25, MUTED)
            if x < 1165: arrow(d, (x+270, 535), (x+333, 535), ORANGE)
        text(d, (292, 735), "版本 · 权限 · 出处：工程扩展，伴随记录流转", 30, TEAL)
    elif kind == "kg":
        for x, h in [(108, "源文本"), (410, "实体关系图"), (735, "社区划分"), (1040, "社区摘要")]:
            panel(d, (x, 397, x+240, 567), LIGHT if x == 410 else "#FFFFFF")
            text(d, (x+120, 480), h, 31, INK, "mm")
            if x < 1040: arrow(d, (x+250, 480), (x+290, 480), ORANGE)
        panel(d, (547, 680, 1015, 800), "#FFF2E5")
        text(d, (780, 740), "问题相关摘要 → 汇总回答", 31, ORANGE, "mm")
        arrow(d, (1160, 580), (932, 671), ORANGE)
        text(d, (132, 723), "具体条款另回原文核对", 29, TEAL)
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
            arrow(d, (x+103, 611), (417, 550), TEAL, 4)
        for x in (152, 300, 451, 599):
            panel(d, (x, 735, x+105, 788), "#FFFFFF")
            text(d, (x+52, 761), "片段", 20, MUTED, "mm")
            arrow(d, (x+52, 728), (269 if x < 450 else 559, 699), TEAL, 3)
        panel(d, (911, 467, 1325, 548), "#FFFFFF")
        text(d, (1118, 507), "父条款：条件完整", 26, ORANGE, "mm")
        for x, h in [(862, "子片段 1"), (1174, "子片段 2")]:
            panel(d, (x, 640, x+230, 715), "#FFFFFF")
            text(d, (x+115, 677), h, 25, INK, "mm")
            arrow(d, (x+115, 627), (1118, 557), ORANGE, 4)
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
        ("assets/overview-evaluation.png", "系统验收看四件事", "不能用一句答对了掩盖中间错误", [("来源", "权威且更新"), ("检索", "证据进候选"), ("生成", "断言有支持"), ("治理", "权限不越界")], "分别记录错误，才能知道应修哪一段"),
        ("submodules/knowledgebase/assets/kb-cover.png", "知识库：先管好资料", "文件进库不等于问题就能答对", [("定来源", "谁负责发布"), ("留版本", "何时生效"), ("建索引", "可查可回溯")], "把制度当作有生命周期的知识资产"),
        ("submodules/knowledgebase/assets/kb-source.png", "源头先说清", "每份资料都要有可追究的身份", [("原始来源", "文件或业务表"), ("资料责任人", "谁批准更新"), ("可用范围", "谁能看到")], "导入时间不等于生效时间"),
        ("submodules/knowledgebase/assets/kb-version.png", "制度按生效日判断", "旧版和新版同时存在，并非只留最新一份", [("旧版", "上限 450 元"), ("9 月 1 日", "新版生效"), ("新版", "上限 500 元")], "示意数值；查询还需匹配地点、职级和日期"),
        ("submodules/knowledgebase/assets/kb-refresh.png", "更新与撤回同样重要", "索引不能比原文多活一辈子", [("发布", "记录版本"), ("更新", "重建索引"), ("撤回", "停止返回")], "回看审计日志，确认旧数据是否仍可被查到"),
        ("submodules/knowledgegraph/assets/kg-cover.png", "知识图谱：把关系讲明白", "有些问题不缺片段，缺的是连接线", [("识别实体", "员工与部门"), ("连接关系", "适用何制度"), ("核对原文", "落到哪一条")], "图谱给路径，原文给证据"),
        ("submodules/knowledgegraph/assets/kg-query.png", "沿关系找适用条款", "多跳查询要把每一步的出处带回来", [("员工", "属于研发部"), ("研发部", "适用差旅规"), ("条款", "北京住宿")], "任何一条边过期，路径都可能失效"),
        ("submodules/knowledgegraph/assets/kg-provenance.png", "关系也需要证据", "一条边不仅有方向，还要有出处和有效期", [("关系", "部门适用制度"), ("出处", "发布文件位置"), ("状态", "已核或待核")], "抽取得到的边不能自动升级为权威事实"),
        ("submodules/rag/assets/rag-cover.png", "RAG：先查再答", "把外部证据带进当前回答", [("提出问题", "要判断什么"), ("取回证据", "哪个版本适用"), ("生成回答", "每句可核验")], "RAG 并不保证检索和理解永远正确"),
        ("submodules/rag/assets/rag-question.png", "先拆问题，再下结论", "“能报吗”至少包含四个待核事实", [("票据", "金额与日期"), ("员工", "职级和部门"), ("制度", "地区与生效期"), ("状态", "审批是否完成")], "缺失的事实要追问或停判，不要靠语气补齐"),
        ("submodules/rag/assets/rag-context.png", "证据包不能只放原文", "检索片段要带上约束条件", [("条款正文", "金额上限"), ("适用范围", "职级与地点"), ("版本来源", "生效日与链接")], "旧版与新版冲突时，先判适用性再概括"),
        ("submodules/rag/assets/rag-abstain.png", "何时应该停下", "没有证据的完成声明最危险", [("证据足够", "给有限结论"), ("证据冲突", "指出冲突"), ("条件缺失", "追问或拒答")], "拒答不是失败；编造肯定结论才是失败"),
        ("submodules/chunking/assets/chunk-cover.png", "分段：别把例外切丢", "切开前先看文档的骨架", [("识别结构", "标题与表格"), ("保存条件", "例外与脚注"), ("形成片段", "能回原文")], "块太小会丢条件，块太大不易定位"),
        ("submodules/chunking/assets/chunk-document.png", "先解析，再分段", "文档顺序比固定字数更重要", [("版面", "页眉表格脚注"), ("结构", "章节与条款"), ("证据", "条件完整片段")], "跨页表格的标题不能留在上一页"),
        ("submodules/chunking/assets/chunk-metadata.png", "片段的随身证件", "正文之外，还要保存检索与审计信息", [("来源", "文档与页码"), ("适用", "时间与权限"), ("定位", "条款与父节点")], "元数据丢失后，检索相似度无法补救"),
        ("submodules/chunking/assets/chunk-test.png", "分段怎样验收", "从真实问法回看证据单元", [("可召回", "命中目标条款"), ("可理解", "条件不缺失"), ("可定位", "回原文核对")], "用普通、冲突、缺值、新增四类问题抽检"),
        ("submodules/retrieval/assets/retrieval-cover.png", "检索：找得到，也要选得对", "让当前有效的证据走到前面", [("广泛召回", "别漏目标"), ("硬过滤", "排除不适用"), ("精细排序", "优先有用片段")], "最相似不一定最适用"),
        ("submodules/retrieval/assets/retrieval-candidates.png", "两条召回路", "精确词与近义问法各有长处", [("关键词", "编号与专名"), ("稠密向量", "近义表达"), ("合并候选", "去重后再排")], "混合召回先看漏检率，再看最终排序"),
        ("submodules/retrieval/assets/retrieval-filter.png", "硬条件先过闸", "分数高也不能越过权限和生效期", [("权限", "此人可见"), ("适用", "地点与职级"), ("时间", "当日已生效")], "过滤条件要随查询身份进入日志与评测"),
        ("submodules/retrieval/assets/retrieval-citation.png", "引用回到原文", "片段 ID 不等于可供读者核对的地址", [("候选片段", "保存稳定 ID"), ("来源定位", "文档页码条款"), ("展示引用", "读者可打开")], "引用打开后须与回答中的断言相匹配"),
        ("submodules/retrieval/assets/retrieval-metrics.png", "分开衡量召回与排序", "不要只看最终回答是否好听", [("候选召回", "正确条款在吗"), ("前列排序", "是否排得够前"), ("引用核验", "能否定位出处")], "每项指标都要有问题集、证据标注和分母"),
    ]
    for spec in flows:
        flow(*spec)
    compares = [
        ("assets/overview-boundary.png", "三种常见失效", "错误来自资料、权限与信息缺口，不是一种毛病", ("旧版制度", ["先比生效日期", "再看适用地区", "不可误用旧规则"]), ("无权或缺值", ["权限不足就不泄露", "关键字段缺失就追问", "不能假装已核验"]), "把错误分开记录，修复才会落到正确环节"),
        ("submodules/knowledgebase/assets/kb-access.png", "看得见由谁决定", "知识库记录要保留访问范围", ("资料侧", ["来源标注权限域", "撤回时连索引失效", "保留审计记录"]), ("查询侧", ["按当前身份过滤", "结果只含可见资料", "不把权限交给模型猜"]), "权限控制发生在检索之前，不靠生成模型遮掩"),
        ("submodules/knowledgegraph/assets/kg-sources.png", "三类知识源", "不同资料适合回答不同问题", ("原文与业务表", ["原文给完整条款", "业务表给当前状态", "都要有责任来源"]), ("知识图谱", ["记录实体间关系", "适合多跳路径", "结论仍回原文"]), "向量索引是查找结构，不是另一份权威事实"),
        ("submodules/knowledgegraph/assets/kg-contrast.png", "语义相近与关系成立", "两种证据路线不能互相冒充", ("向量索引", ["找相似措辞", "适合模糊问法", "相似不等于适用"]), ("关系图谱", ["走实体与关系", "适合多跳问法", "边需要出处与时间"]), "选型看问题类型，不看哪个名词更新潮"),
        ("submodules/rag/assets/rag-citation.png", "断言逐条挂证据", "引用不是放在段末的装饰", ("能证实", ["480 元来自票据", "500 元来自新版条款", "日期满足生效条件"]), ("尚待核", ["发票真伪未知", "审批状态未知", "不能写已提交"]), "回答边界不超过证据边界"),
        ("submodules/chunking/assets/chunk-error.png", "错误切法与正确切法", "把例外与主条款拆散，会改变读者看到的含义", ("错误：分离", ["片段 A：上限 500", "片段 B：仅 A 职级", "单看 A 会过度概括"]), ("正确：连贯", ["同一证据单元", "或有父条款链接", "查询时补足条件"]), "目标不是最大限度切碎，而是让每块可用于判断"),
    ]
    for spec in compares:
        compare(*spec)
    network("assets/overview-sources.png", "证据从不同来源来", "汇合之前先保留自己的身份", "可追溯资料", [("制度文件", "版本与条款"), ("业务表", "当前状态"), ("关系图", "关联路径"), ("检索索引", "查找入口")], "索引不是权威来源；答案应指回原文或业务系统")
    principles = [
        ("assets/overview-principle.png", "问题怎样借外部资料回答", "原始 RAG：检索结果影响当前生成", "rag", "依据 Lewis 等 Figure 1 改绘；出处绑定为工程补充"),
        ("submodules/knowledgebase/assets/kb-principle.png", "外部资料如何成为可查索引", "资料治理补在原始 RAG 文档索引之前", "kb", "依据 Lewis 等 Figure 1 的文档索引部分改绘"),
        ("submodules/knowledgegraph/assets/kg-principle.png", "GraphRAG 怎样做全局归纳", "图与社区摘要适合跨材料主题问题", "kg", "依据 Edge 等 Figure 1 改绘；具体条款需回原文"),
        ("submodules/rag/assets/rag-principle.png", "检索候选怎样影响生成", "问题与证据共同进入回答生成", "rag", "依据 Lewis 等 Figure 1 改绘；引用是工程扩展"),
        ("submodules/chunking/assets/chunk-principle.png", "长文怎样保留不同尺度", "分层摘要与父子定位是两种不同策略", "chunk", "左侧依据 RAPTOR Figure 1 改绘；右侧父子定位为另一路线"),
        ("submodules/retrieval/assets/retrieval-principle.png", "先快找，再细排", "双编码器召回与联合编码重排并不相同", "retrieval", "依据 DPR §2.1 与 Passage Re-ranking with BERT §2 改绘"),
    ]
    for spec in principles:
        principle(*spec)


if __name__ == "__main__":
    main()
