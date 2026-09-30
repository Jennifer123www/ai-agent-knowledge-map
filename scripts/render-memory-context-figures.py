"""Render source-traceable Chinese PNG diagrams for the memory/context series.

Pillow is an authoring dependency only. The published assets are PNG files.
Run: python3 scripts/render-memory-context-figures.py
"""

from pathlib import Path
from math import atan2, cos, sin
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1] / "content/wechat/03-memory-and-context-engineering"
FONT_CANDIDATES = [
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
]
FONT = next((str(p) for p in FONT_CANDIDATES if p.exists()), None)
if not FONT:
    raise RuntimeError("A Chinese font is required")

W, H = 1536, 1024
PAPER, WHITE, INK, MUTED = "#FAF8F4", "#FFFFFF", "#27373C", "#637379"
PURPLE, LILAC, TEAL, MINT, ORANGE, PEACH, RED = (
    "#754D78", "#F0E7F2", "#187B76", "#E0EFEC", "#BB7747", "#F8E9DB", "#A95662"
)


def font(size):
    return ImageFont.truetype(FONT, size)


def txt(d, xy, label, size=30, color=INK, anchor=None):
    d.text(xy, label, font=font(size), fill=color, anchor=anchor)


def wrap(d, label, max_width, size):
    lines, current = [], ""
    for ch in label:
        if ch == "\n":
            lines.append(current)
            current = ""
        elif d.textbbox((0, 0), current + ch, font=font(size))[2] > max_width and current:
            lines.append(current)
            current = ch
        else:
            current += ch
    if current:
        lines.append(current)
    return lines


def block(d, xy, label, max_width, size=28, color=INK, line_gap=13):
    for index, line in enumerate(wrap(d, label, max_width, size)):
        txt(d, (xy[0], xy[1] + index * (size + line_gap)), line, size, color)


def panel(d, box, fill=WHITE, outline="#D9CFD9", radius=24):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=3)


def arrow(d, start, end, color=PURPLE, width=6):
    d.line((start, end), fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    a = atan2(y2 - y1, x2 - x1)
    tip = 19
    wing = 10
    d.polygon([
        (x2, y2),
        (x2 - tip * cos(a) + wing * sin(a), y2 - tip * sin(a) - wing * cos(a)),
        (x2 - tip * cos(a) - wing * sin(a), y2 - tip * sin(a) + wing * cos(a)),
    ], fill=color)


def base(title, subtitle, tag="图解"):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 23, H), fill=PURPLE)
    txt(d, (85, 74), tag, 25, PURPLE)
    title_size = 59 if len(title) < 17 else 51
    txt(d, (85, 129), title, title_size)
    txt(d, (88, 223), subtitle, 29, MUTED)
    d.line((85, 280, 1450, 280), fill="#D9CFD9", width=3)
    return im, d


def footer(d, note):
    d.line((86, 890, 1450, 890), fill="#D9CFD9", width=2)
    block(d, (90, 920), note, 1360, 25, MUTED)


def save(im, rel):
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, optimize=True)


def cover(rel, title, subtitle, steps, note):
    im, d = base(title, subtitle, "记忆与上下文工程 · 系列配图")
    colors = [LILAC, MINT, PEACH]
    for i, (head, detail) in enumerate(steps):
        x = 90 + i * 462
        panel(d, (x, 400, x + 424, 748), colors[i])
        txt(d, (x + 29, 435), f"0{i + 1}", 45, PURPLE if i == 0 else TEAL)
        block(d, (x + 30, 520), head, 358, 39)
        block(d, (x + 30, 605), detail, 360, 27, MUTED)
    footer(d, note)
    save(im, rel)


def flow(rel, title, subtitle, steps, note):
    im, d = base(title, subtitle, "机制路线")
    n = len(steps)
    gap = 40
    width = (1360 - gap * (n - 1)) // n
    for i, (head, detail) in enumerate(steps):
        x = 90 + i * (width + gap)
        panel(d, (x, 395, x + width, 727), MINT if i == n - 1 else WHITE)
        txt(d, (x + 26, 421), str(i + 1).zfill(2), 32, PURPLE)
        block(d, (x + 26, 500), head, width - 50, 34)
        block(d, (x + 26, 592), detail, width - 50, 25, MUTED)
        if i != n - 1:
            arrow(d, (x + width + 4, 565), (x + width + gap - 10, 565), ORANGE)
    footer(d, note)
    save(im, rel)


def compare(rel, title, subtitle, left, right, note):
    im, d = base(title, subtitle, "并列辨析")
    for i, (heading, lines) in enumerate((left, right)):
        x = 90 if i == 0 else 780
        color = PURPLE if i == 0 else TEAL
        panel(d, (x, 365, x + 646, 814), LILAC if i == 0 else MINT)
        block(d, (x + 35, 402), heading, 565, 40, color)
        for j, line in enumerate(lines):
            y = 525 + j * 87
            d.ellipse((x + 38, y + 11, x + 50, y + 23), fill=color)
            block(d, (x + 71, y), line, 535, 27)
    footer(d, note)
    save(im, rel)


def cards(rel, title, subtitle, items, note, tag="四项核对"):
    im, d = base(title, subtitle, tag)
    for i, (heading, detail) in enumerate(items):
        x = 90 + (i % 2) * 690
        y = 350 + (i // 2) * 245
        panel(d, (x, y, x + 645, y + 205), LILAC if i % 3 == 0 else (MINT if i % 3 == 1 else WHITE))
        txt(d, (x + 29, y + 24), heading, 35, PURPLE if i % 2 == 0 else TEAL)
        block(d, (x + 29, y + 104), detail, 575, 27, MUTED)
    footer(d, note)
    save(im, rel)


def timeline(rel, title, subtitle, moments, note):
    im, d = base(title, subtitle, "时间与版本")
    d.line((150, 542, 1300, 542), fill=PURPLE, width=8)
    for i, (when, detail) in enumerate(moments):
        x = 155 + i * 348
        d.ellipse((x - 17, 525, x + 17, 559), fill=PURPLE if i != 2 else ORANGE)
        txt(d, (x - 15, 395), when, 34, PURPLE)
        panel(d, (x - 15, 596, x + 305, 773), LILAC if i % 2 == 0 else MINT)
        block(d, (x + 10, 625), detail, 270, 27)
    footer(d, note)
    save(im, rel)


GROUPS = {
    "overview": {
        "dir": "assets", "prefix": "overview", "title": "记忆与上下文工程", "subtitle": "该记的能再取出；该忘的别继续用",
        "cover": [("任务进度", "中断后知道做到哪一步"), ("长期信息", "只保留确有价值的事实"), ("当前输入", "按权限和预算挑选")],
        "figures": [
            ("map", "flow", "六个环节怎样接力", "状态、记忆、上下文各做一段工作", [("短期状态", "记下进度"), ("写入判断", "筛掉噪声"), ("外部记忆", "按需取回"), ("上下文", "给模型看")], "类型分类与治理贯穿链路，不是排在最后的可选步骤"),
            ("handoff", "cards", "同一条信息去向不同", "关键在用途、时间和权限，不在字面相似", [("任务进度", "等待费用政策校验"), ("用户偏好", "希望中文、简洁回答"), ("业务事实", "以当日系统记录为准"), ("当前证据", "新版制度的适用条款")], "不要把报销进度写进用户画像，也不要把偏好当作制度依据"),
            ("boundary", "compare", "存着和看见是两件事", "外部存储能持久，模型本轮只能处理已送入的内容", ("外部记录", ["可跨会话保留", "需要来源、版本与权限", "不会自动出现在模型眼前"]), ("当前上下文", ["只含本轮选择的材料", "受 token 预算约束", "可信资料与指令要分开"]), "能检索不等于应该读取；读到也不等于可以执行"),
            ("evaluation", "cards", "连续性要分开验收", "最终回答好听，不能掩盖中间环节错误", [("恢复", "中断后不重复提交"), ("写入", "旧偏好能被更正"), ("读取", "只取当前相关内容"), ("治理", "删除后不再回流")], "每项分别测普通、冲突、缺值和变更样本"),
        ],
    },
    "shortterm": {
        "dir": "submodules/01-shortterm/assets", "prefix": "shortterm", "title": "短期状态", "subtitle": "任务停一半，也要知道从哪里继续",
        "cover": [("识别票据", "留下识别结果"), ("等待校验", "记住当前节点"), ("恢复任务", "避免重复动作")],
        "figures": [
            ("state", "cards", "检查点需要哪些字段", "保存可恢复的状态，不保存一团含糊摘要", [("任务标识", "谁的哪一笔报销"), ("当前节点", "已识别，待政策校验"), ("关键输出", "票据字段和来源"), ("动作状态", "未提交、待确认")], "原始票据可用稳定引用保存，不必把整张图塞入状态"),
            ("checkpoint", "flow", "检查点何时落盘", "先有已确认输出，再进入下一个可重放节点", [("节点执行", "识别票据"), ("结果校验", "字段有来源"), ("保存状态", "版本加时间"), ("继续任务", "政策校验")], "保存频率取决于重做成本与一致性要求"),
            ("replay", "compare", "重放与重复执行", "外部动作必须单独检查，不能只恢复对话", ("安全重放", ["检查是否已有结果", "使用幂等键", "从未完成节点继续"]), ("危险重做", ["重复创建报销单", "重复发送通知", "把草稿说成已提交"]), "中断发生在外部调用后，恢复前先查询真实结果"),
            ("test", "timeline", "四个中断点要测", "不同时间断开，恢复路径不一样", [("识别前", "无字段，可重新识别"), ("识别后", "复用已验字段"), ("调用后", "先查外部动作"), ("完成后", "不再继续提交")], "故障注入覆盖执行前、执行中和执行后"),
        ],
    },
    "longterm": {
        "dir": "submodules/02-longterm/assets", "prefix": "longterm", "title": "长期记忆", "subtitle": "跨会话沿用有用信息，也允许更正",
        "cover": [("候选偏好", "反复要求中文"), ("受控保存", "有来源和范围"), ("下次取回", "当前任务确实需要")],
        "figures": [
            ("vs-history", "compare", "记忆不是聊天录像", "原始历史保留发生过什么；记忆供未来任务使用", ("聊天历史", ["长而杂", "含一次性内容", "适合复盘原话"]), ("受控记忆", ["经过筛选", "附来源与时效", "可更正与删除"]), "不要把整段聊天摘要成一个永久不变的用户结论"),
            ("retrieval", "flow", "长期信息怎样进入这一轮", "只有匹配当前任务，才被带回模型输入", [("任务来了", "写报销说明"), ("检索候选", "按用户范围"), ("过滤冲突", "比对当前要求"), ("注入上下文", "只放必要偏好")], "模型不能仅因外部库有记录就自动使用它"),
            ("conflict", "compare", "旧偏好遇到新要求", "本轮明确表达要优先于陈旧推断", ("过去的记录", ["偏好中文", "来源：用户自述", "记录时间较早"]), ("本轮的要求", ["这次请用英文", "只影响当前请求", "不必永久覆盖偏好"]), "临时例外与永久变更是两种不同的更新"),
            ("test", "cards", "长期记忆怎样验收", "分开观察收益、误用和泄漏", [("适用", "跨会话仍能用"), ("冲突", "新要求不被旧值压住"), ("误记", "偶然推断不固化"), ("隔离", "别人的偏好进不来")], "错误记住一次，可能影响许多后续任务"),
        ],
    },
    "memorytypes": {
        "dir": "submodules/03-memorytypes/assets", "prefix": "memorytypes", "title": "记忆类型与用户画像", "subtitle": "先看用途，再决定放进哪个抽屉",
        "cover": [("任务", "这次报销到哪步"), ("经历", "上次为何退回"), ("偏好", "只记必要的习惯")],
        "figures": [
            ("taxonomy", "cards", "四种信息不要混放", "这里按用途讲，分类不是固定数据库表名", [("工作记忆", "当前任务状态"), ("情景记忆", "可复盘的经历"), ("语义记忆", "已核的稳定事实"), ("用户画像", "受控偏好与约束")], "一条内容可能跨类，但用途与保留规则要说清"),
            ("profile", "compare", "画像与经历不同", "一次行为不足以推出长期偏好", ("一次经历", ["上次报销被退回", "有具体时间与事件", "可用于排查"]), ("受控画像", ["明确希望中文简洁", "有范围和删除入口", "按任务最小化使用"]), "不能从一次投诉推断性格，更不能存敏感猜测"),
            ("routing", "flow", "候选信息如何分类", "先问以后拿它做什么，再问能否保存", [("候选", "取自对话"), ("用途", "状态或经历"), ("来源", "是否确认"), ("去向", "保存或丢弃")], "分类是写入判断的输入，不替代授权与治理"),
            ("test", "cards", "四个反例测边界", "能分类，不等于都应该长期保存", [("临时城市", "通常留在本次任务"), ("退单经历", "保留事件与出处"), ("制度上限", "回权威资料核对"), ("语言偏好", "明确且可撤销")], "混淆类别会改变保留期、读取范围和答案依据"),
        ],
    },
    "memorywrite": {
        "dir": "submodules/04-memorywrite/assets", "prefix": "memorywrite", "title": "记忆写入与更新", "subtitle": "新称呼来了，旧称呼不能假装没看见",
        "cover": [("新说法", "请改叫小林"), ("核实意图", "仅本次还是以后"), ("更新记录", "覆盖旧值有版本")],
        "figures": [
            ("gate", "cards", "写入前过四道门", "候选信息不等于已确认的长期记忆", [("来源", "用户明确说了什么"), ("用途", "未来任务是否需要"), ("敏感", "是否应当保存"), ("范围", "本次还是持续适用")], "任何一道门不过，都可以选择不写入"),
            ("conflict", "compare", "覆盖还是追加", "称呼是当前值，不该并排保留两个互斥答案", ("追加事件", ["记录何时说过", "保留历史供审计", "不直接作为当前值"]), ("覆盖当前值", ["新称呼成为有效值", "旧值不再读取", "记录版本与来源"]), "活动值与变更历史分开存，避免旧称呼回流"),
            ("version", "timeline", "称呼变更的版本线", "乱序消息不能把新偏好改回旧值", [("v1", "称呼：小王"), ("新请求", "请改叫小林"), ("v2", "当前：小林"), ("迟到事件", "不能覆盖 v2")], "比较版本和来源，不凭消息到达顺序猜意图"),
            ("test", "cards", "写入错误怎么发现", "正常更新与错误污染要分开测", [("明确变更", "旧值退出读取"), ("随口提及", "不误写入"), ("消息乱序", "新值不回退"), ("撤销请求", "相关记录能失效")], "还要测用户否认系统推断时是否真能撤销"),
        ],
    },
    "contextbuild": {
        "dir": "submodules/05-contextbuild/assets", "prefix": "contextbuild", "title": "上下文构造", "subtitle": "窗口有边界，放进去的东西要有用又可信",
        "cover": [("先筛", "权限、时间、来源"), ("再排", "任务与关键证据"), ("后核", "没有把网页当命令")],
        "figures": [
            ("selection", "flow", "上下文选择顺序", "先做硬过滤，再比较相关性", [("候选材料", "旧新制度"), ("硬过滤", "权限与生效"), ("排优先级", "与问题相关"), ("构造输入", "标来源与边界")], "分数高的旧制度不能越过生效期"),
            ("budget", "cards", "窗口预算给谁", "下面是预算类别，不是固定比例", [("硬约束", "任务与安全边界"), ("当前状态", "已确认的关键字段"), ("证据", "有出处的必要片段"), ("输出余量", "为回答留空间")], "token 预算应由真实样本和模型接口决定"),
            ("injection", "compare", "网页内容不是系统命令", "不可信资料可以被引用，不能升级为高优先级指令", ("网页中的文字", ["可作证据候选", "需要来源与过滤", "夹带指令要隔离"]), ("系统与用户任务", ["规定可执行动作", "控制权限与目标", "不可被网页覆盖"]), "模型可以读材料；工具权限仍由外部系统决定"),
            ("test", "cards", "上下文四种压力测试", "把问题拆成可判的失败条件", [("旧新冲突", "能找到最新适用版"), ("证据居中", "不因位置漏读"), ("恶意注入", "不执行网页指令"), ("缓存过期", "制度更新后失效")], "不能用一次答对证明长上下文策略稳定"),
        ],
    },
    "memorygovernance": {
        "dir": "submodules/06-memorygovernance/assets", "prefix": "memorygovernance", "title": "记忆治理", "subtitle": "能保存，也要能限制、改正和删除",
        "cover": [("明确用途", "为什么要记"), ("限制读取", "谁能看"), ("删除闭环", "副本一起处理")],
        "figures": [
            ("access", "cards", "读取权限分四层", "记忆可检索，不等于所有 Agent 都能用", [("用户", "只能读本人范围"), ("租户", "组织之间隔离"), ("用途", "当前任务必要"), ("日志", "不泄露原文")], "在检索前过滤，不依赖模型承诺保密"),
            ("lifecycle", "timeline", "一条偏好的生命周期", "每个阶段都应可解释、可撤销", [("提出", "明确用途"), ("保存", "来源与权限"), ("使用", "按任务读取"), ("退出", "过期或删除")], "保留期限由实际用途与适用规则决定，图中不设统一天数"),
            ("delete", "flow", "删除不止删主表", "衍生副本要逐层失效并能核对", [("接收请求", "定位用户和范围"), ("主记录", "标失效并删除"), ("衍生副本", "索引和缓存"), ("回查", "确认不再返回")], "备份与审计另按系统策略处理，不得让其重新进入线上读取"),
            ("test", "cards", "治理验收要做反例", "测试要用不同身份、不同时间和删除后重试", [("越权", "跨租户不返回"), ("过期", "旧值不注入"), ("删除", "索引缓存不回流"), ("审计", "能查操作不曝内容")], "这里只讲工程控制；具体法律义务需按地区和场景核对"),
        ],
    },
}


def labeled_box(d, box, heading, sub="", fill=WHITE, size=30):
    panel(d, box, fill)
    block(d, (box[0] + 20, box[1] + 19), heading, box[2] - box[0] - 40, size, INK)
    if sub:
        block(d, (box[0] + 20, box[1] + 76), sub, box[2] - box[0] - 40, 23, MUTED)


def principle(group, rel):
    titles = {
        "overview": ("有限窗口与外部记忆", "外部存储要经读取动作，才进入这一轮输入"),
        "shortterm": ("当前窗口怎样容纳状态", "工作区与消息队列都占用有限输入窗口"),
        "longterm": ("经历如何影响下一次行动", "记录、检索与反思在论文中形成循环"),
        "memorytypes": ("从经历到可复用认识", "观察记录与高层反思，不是一份混合长文本"),
        "memorywrite": ("新消息怎样替换旧值", "旧值保留在历史里，不再作为当前有效称呼"),
        "contextbuild": ("证据位置会影响利用", "同一份证据移到输入中间，部分模型更容易漏用"),
        "memorygovernance": ("从数据处理到受控退出", "把隐私治理要求落到记忆读取与删除链路"),
    }
    im, d = base(*titles[group], "原理／规范依据改绘")
    if group == "overview":
        labeled_box(d, (90, 358, 870, 767), "模型当前输入窗口", "系统约束 ｜ 工作区 ｜ 当前消息", LILAC, 39)
        labeled_box(d, (1000, 380, 1440, 528), "历史记录", "窗口之外，可查可取", WHITE)
        labeled_box(d, (1000, 610, 1440, 758), "长期存储", "窗口之外，按需读取", MINT)
        arrow(d, (1000, 455), (880, 455), TEAL)
        arrow(d, (1000, 682), (880, 682), TEAL)
        txt(d, (895, 400), "读取", 24, TEAL)
        txt(d, (895, 722), "读取", 24, TEAL)
        txt(d, (126, 641), "固定容量", 28, PURPLE)
        footer(d, "依据 MemGPT Figure 3 简化；权限与写入门槛由工程系统补充")
    elif group == "shortterm":
        panel(d, (90, 352, 1440, 775), LILAC)
        txt(d, (125, 380), "有限上下文窗口", 37, PURPLE)
        for x, head, detail in [
            (140, "系统指令", "相对固定"), (540, "工作区", "本轮重要状态"), (940, "消息队列", "近期交互滚动"),
        ]:
            labeled_box(d, (x, 486, x + 350, 666), head, detail, WHITE)
        arrow(d, (900, 576), (929, 576), TEAL)
        txt(d, (575, 704), "超过窗口时，旧消息可移到外部记录并按需取回", 25, MUTED)
        footer(d, "依据 MemGPT Figure 3；任务检查点是另加的工程持久化机制")
    elif group == "longterm":
        labeled_box(d, (105, 480, 345, 644), "观察", "新经历", WHITE)
        labeled_box(d, (445, 480, 760, 644), "记忆流", "带时间的记录", LILAC)
        labeled_box(d, (865, 480, 1120, 644), "检索", "按当前情境", MINT)
        labeled_box(d, (1220, 480, 1440, 644), "行动", "使用相关信息", WHITE)
        for a, b in [((355, 562), (435, 562)), ((770, 562), (855, 562)), ((1130, 562), (1210, 562))]:
            arrow(d, a, b, TEAL)
        labeled_box(d, (672, 735, 1006, 836), "反思：生成更高层认识", "", PEACH, 27)
        arrow(d, (990, 654), (990, 724), ORANGE)
        arrow(d, (663, 784), (590, 657), ORANGE)
        footer(d, "依据 Generative Agents Figure 5；企业偏好写入还需另设门槛")
    elif group == "memorytypes":
        labeled_box(d, (90, 380, 550, 540), "观察记录", "例：上次报销被退回", WHITE)
        labeled_box(d, (90, 640, 550, 800), "高层反思", "例：常见退回原因", PEACH)
        labeled_box(d, (705, 470, 1115, 706), "记忆流与检索", "根据当下情境取相关记录，而非全量塞入", LILAC, 35)
        labeled_box(d, (1250, 504, 1445, 665), "行动", "形成回应", MINT, 30)
        arrow(d, (560, 460), (693, 555), TEAL)
        arrow(d, (560, 720), (693, 627), ORANGE)
        arrow(d, (1125, 585), (1238, 585), TEAL)
        footer(d, "依据 Generative Agents Figure 5；工作／情景／语义／画像分类是教学延伸")
    elif group == "memorywrite":
        labeled_box(d, (110, 392, 465, 560), "原记录", "称呼：小王", LILAC)
        labeled_box(d, (110, 678, 465, 836), "新消息", "请改叫小林", WHITE)
        labeled_box(d, (630, 515, 945, 705), "替换操作", "工作区旧值退出", PEACH, 30)
        labeled_box(d, (1100, 515, 1440, 705), "当前值", "称呼：小林", MINT)
        arrow(d, (475, 478), (617, 573), ORANGE)
        arrow(d, (475, 752), (617, 651), ORANGE)
        arrow(d, (955, 610), (1088, 610), TEAL)
        footer(d, "依据 MemGPT Figure 4；是否允许替换，仍需外部校验和用户意图判断")
    elif group == "contextbuild":
        # Qualitative U-shaped curve, deliberately not copied as measured values.
        d.line((185, 776, 1380, 776), fill=INK, width=5)
        d.line((185, 776, 185, 372), fill=INK, width=5)
        txt(d, (90, 337), "任务表现", 29, INK)
        points = [(245, 446), (430, 524), (620, 654), (790, 708), (960, 656), (1150, 522), (1340, 440)]
        d.line(points, fill=PURPLE, width=10, joint="curve")
        for x, y in [points[0], points[3], points[-1]]:
            d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=ORANGE)
        txt(d, (185, 811), "开头", 30, PURPLE)
        txt(d, (750, 811), "中间", 30, PURPLE)
        txt(d, (1270, 811), "末尾", 30, PURPLE)
        txt(d, (570, 368), "相同证据放在不同位置", 31, MUTED)
        footer(d, "依据 Lost in the Middle Figure 1 作定性示意；不是所有模型的实测曲线")
    elif group == "memorygovernance":
        # NIST Control-P motivates controllable data processing; this topology is
        # an explicitly labeled engineering application, not an original NIST figure.
        labeled_box(d, (90, 504, 420, 684), "删除请求", "定位本人记录", LILAC)
        labeled_box(d, (555, 504, 875, 684), "失效标记", "先阻断新读取", PEACH)
        labeled_box(d, (1010, 353, 1437, 493), "主记录", "删除或取消可读", WHITE)
        labeled_box(d, (1010, 532, 1437, 672), "检索索引", "清理相关条目", MINT)
        labeled_box(d, (1010, 711, 1437, 851), "缓存副本", "同步失效", WHITE)
        arrow(d, (430, 594), (543, 594), PURPLE)
        d.line((885, 594, 940, 594), fill=TEAL, width=6)
        d.line((940, 423, 940, 781), fill=TEAL, width=6)
        for y in (423, 602, 781):
            arrow(d, (940, y), (998, y), TEAL)
        footer(d, "依据 NIST Privacy Framework 的 Control-P 目标设计；传播拓扑是工程示意")
    save(im, rel)


def main():
    cover_notes = {
        "overview": "一笔中断的报销草稿，串起六个环节",
        "shortterm": "恢复前先核对任务节点和外部动作状态",
        "longterm": "跨会话偏好要有来源、范围和失效条件",
        "memorytypes": "相同的聊天内容，按用途可能走不同去向",
        "memorywrite": "新称呼生效后，旧值不能继续作为当前答案",
        "contextbuild": "本轮输入应保留最新有效条款和来源",
        "memorygovernance": "删除请求应覆盖主记录、索引与缓存",
    }
    for group_id, group in GROUPS.items():
        directory, prefix = group["dir"], group["prefix"]
        cover(f"{directory}/{prefix}-cover.png", group["title"], group["subtitle"], group["cover"],
              cover_notes[group_id])
        for name, kind, title, subtitle, a, *rest in group["figures"]:
            rel = f"{directory}/{prefix}-{name}.png"
            if kind == "flow":
                flow(rel, title, subtitle, a, rest[0])
            elif kind == "cards":
                cards(rel, title, subtitle, a, rest[0])
            elif kind == "timeline":
                timeline(rel, title, subtitle, a, rest[0])
            elif kind == "compare":
                compare(rel, title, subtitle, a, rest[0], rest[1])
        principle(group_id, f"{directory}/{prefix}-principle.png")


if __name__ == "__main__":
    main()
