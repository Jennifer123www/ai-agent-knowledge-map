"""Render the Chinese, source-traceable diagrams for 智能体与工作流.

Published assets are deterministic PNGs. Run with a Python environment containing
Pillow, e.g. the bundled Codex workspace Python. No image runtime is needed by
the static website or the WeChat draft converter.
"""

from math import atan2, cos, sin
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1] / "content/wechat/agents-and-workflows"
FONTS = [
    Path("/System/Library/Fonts/Hiragino Sans GB.ttc"),
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
]
FONT = next((str(path) for path in FONTS if path.exists()), None)
if FONT is None:
    raise RuntimeError("Chinese font not found")

W, H = 1536, 1024
BG, WHITE, INK, MUTED = "#FAF8F4", "#FFFFFF", "#27373C", "#64757B"
PURPLE, LILAC, TEAL, MINT, ORANGE, PEACH, RED = (
    "#754D78", "#F0E7F2", "#187B76", "#E0EFEC", "#BB7747", "#F8E9DB", "#AA5360"
)


def f(size):
    return ImageFont.truetype(FONT, size)


def text(d, point, label, size=30, color=INK, anchor=None):
    d.text(point, label, font=f(size), fill=color, anchor=anchor)


def wrap(d, label, width, size):
    lines, current = [], ""
    for char in label:
        if char == "\n":
            lines.append(current)
            current = ""
        elif d.textbbox((0, 0), current + char, font=f(size))[2] > width and current:
            lines.append(current)
            current = char
        else:
            current += char
    if current:
        lines.append(current)
    return lines


def block(d, point, label, width, size=28, color=INK, gap=12):
    for i, line in enumerate(wrap(d, label, width, size)):
        text(d, (point[0], point[1] + i * (size + gap)), line, size, color)


def box(d, xy, fill=WHITE, outline="#D9CFD9", radius=23):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=3)


def arrow(d, start, end, color=PURPLE, width=6):
    d.line((start, end), fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    a = atan2(y2 - y1, x2 - x1)
    tip, wing = 19, 10
    d.polygon([
        (x2, y2),
        (x2 - tip * cos(a) + wing * sin(a), y2 - tip * sin(a) - wing * cos(a)),
        (x2 - tip * cos(a) - wing * sin(a), y2 - tip * sin(a) + wing * cos(a)),
    ], fill=color)


def base(title, subtitle, tag="机制图解"):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 23, H), fill=PURPLE)
    text(d, (85, 74), tag, 25, PURPLE)
    text(d, (85, 129), title, 59 if len(title) < 17 else 51)
    block(d, (88, 223), subtitle, 1340, 29, MUTED)
    d.line((85, 280, 1450, 280), fill="#D9CFD9", width=3)
    return im, d


def footer(d, note):
    d.line((86, 890, 1450, 890), fill="#D9CFD9", width=2)
    block(d, (90, 920), note, 1350, 24, MUTED)


def save(im, rel):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, optimize=True)


def card(d, xy, heading, detail, fill=WHITE, heading_color=INK, heading_size=33, detail_size=25):
    box(d, xy, fill)
    x1, y1, x2, _ = xy
    block(d, (x1 + 26, y1 + 22), heading, x2 - x1 - 52, heading_size, heading_color)
    block(d, (x1 + 27, y1 + 101), detail, x2 - x1 - 54, detail_size, MUTED)


def cover(rel, title, subtitle, steps, note):
    im, d = base(title, subtitle, "智能体与工作流 · 系列配图")
    for i, (head, detail) in enumerate(steps):
        x = 90 + i * 462
        box(d, (x, 389, x + 425, 755), [LILAC, MINT, PEACH][i])
        text(d, (x + 27, 423), f"0{i+1}", 45, PURPLE if i == 0 else TEAL)
        block(d, (x + 28, 515), head, 365, 39)
        block(d, (x + 29, 616), detail, 365, 27, MUTED)
    footer(d, note)
    save(im, rel)


def flow(rel, title, subtitle, steps, note):
    im, d = base(title, subtitle, "步骤与交接")
    n = len(steps)
    gap = 37
    width = (1360 - gap * (n - 1)) // n
    for i, (head, detail) in enumerate(steps):
        x = 90 + i * (width + gap)
        card(d, (x, 384, x + width, 738), head, detail, MINT if i == n - 1 else WHITE, PURPLE, 31, 25)
        if i != n - 1:
            arrow(d, (x + width + 3, 561), (x + width + gap - 9, 561), ORANGE, 5)
    footer(d, note)
    save(im, rel)


def compare(rel, title, subtitle, left, right, note):
    im, d = base(title, subtitle, "并列辨析")
    for i, (head, lines) in enumerate((left, right)):
        x = 90 if i == 0 else 780
        fill = LILAC if i == 0 else MINT
        color = PURPLE if i == 0 else TEAL
        box(d, (x, 364, x + 646, 815), fill)
        block(d, (x + 35, 406), head, 572, 40, color)
        for j, line in enumerate(lines):
            y = 520 + j * 89
            d.ellipse((x + 35, y + 12, x + 49, y + 26), fill=color)
            block(d, (x + 69, y), line, 535, 27)
    footer(d, note)
    save(im, rel)


def four(rel, title, subtitle, items, note):
    im, d = base(title, subtitle, "四项核对")
    for i, (head, detail) in enumerate(items):
        x = 90 + (i % 2) * 690
        y = 348 + (i // 2) * 247
        card(d, (x, y, x + 645, y + 213), head, detail,
             [LILAC, MINT, WHITE, PEACH][i], PURPLE if i % 2 == 0 else TEAL, 35, 26)
    footer(d, note)
    save(im, rel)


def principle(rel, key):
    titles = {
        "overview": ("观察改变下一步选择", "模型负责提出下一步；工具返回和程序闸门决定能否继续"),
        "persona": ("候选动作先过可执行集合", "角色契约说清职责，真正执行仍要经过权限检查"),
        "prompt": ("输入分层，输出再校验", "下层资料可被引用，不能靠一句话升级为高优先级指令"),
        "reasoning": ("行动带回新证据，再更新结论", "公开可核的工具观察，比空写一串推理更能支撑会议时间"),
        "planning": ("候选方案可以分支、评价与回退", "多个会议时段并列搜索，不把第一条猜测当最终计划"),
        "routing": ("分类后进入专用处理路径", "硬约束先过滤；工具、模型或人工按任务特征接手"),
        "reflection": ("反馈让下一次尝试有变化", "真实失败信号进入评价和修正，再决定是否值得重试"),
        "loop": ("行动与观察组成有限循环", "每一圈更新状态；完成、等待或失败时走明确出口"),
    }
    sources = {
        "overview": "依据 ReAct Figure 1(1d) 改绘；停止与权限出口为工程扩展",
        "persona": "依据 ReAct §2 的环境动作空间改绘；权限闸门为工程扩展",
        "prompt": "依据 Instruction Hierarchy §2–3 改绘；程序校验为工程扩展",
        "reasoning": "依据 ReAct Figure 1(1d) 改绘；只展示可核查的外部观察",
        "planning": "依据 Tree of Thoughts Figure 1 改绘；会议候选是教学例子",
        "routing": "依据 Anthropic《Building effective agents》的 Routing 图改绘",
        "reflection": "依据 Reflexion Figure 2(a) 改绘；次数上限为工程扩展",
        "loop": "依据 ReAct Figure 1(1d) 改绘；状态与暂停为工程扩展",
    }
    im, d = base(*titles[key], "原理／规范依据改绘")
    if key == "overview":
        labels = [("当前缺口", "还缺会议室"), ("查询环境", "查指定时段"),
                  ("观察返回", "会议室被占"), ("更新选择", "换候选时间")]
        for i, (head, detail) in enumerate(labels):
            x = 90 + i * 345
            card(d, (x, 388, x + 310, 633), head, detail,
                 [LILAC, WHITE, MINT, PEACH][i], PURPLE, 32, 25)
            if i < 3:
                arrow(d, (x + 315, 507), (x + 337, 507), TEAL, 5)
        d.line((1435, 520, 1460, 520, 1460, 835, 210, 835, 210, 665), fill=PURPLE, width=5)
        arrow(d, (210, 665), (210, 646), PURPLE, 5)
        text(d, (390, 789), "未完成且有预算：下一圈", 25, PURPLE)
        card(d, (1000, 657, 1400, 818), "完成／暂停／停止", "动作闸门与终止判断", WHITE, TEAL, 29, 24)
        arrow(d, (1220, 640), (1220, 652), TEAL, 5)
    elif key == "reasoning":
        for i, (head, detail) in enumerate([
            ("团队 A 日历", "周四下午空闲"), ("团队 B 日历", "周四下午空闲"),
            ("团队 C 日历", "周四下午空闲")
        ]):
            y = 330 + i * 180
            card(d, (90, y, 415, y + 154), head, detail, [LILAC, WHITE, MINT][i], PURPLE, 29, 24)
            arrow(d, (425, y + 75), (585, 570), TEAL, 5)
        card(d, (595, 458, 885, 686), "共同空闲", "人员时间可行", MINT, TEAL, 33, 25)
        card(d, (1060, 340, 1430, 529), "房间观察", "同段时间已占用", PEACH, RED, 32, 25)
        card(d, (1060, 612, 1430, 809), "可核结论", "周四方案不成立", WHITE, TEAL, 32, 25)
        arrow(d, (897, 540), (1048, 430), TEAL, 5)
        arrow(d, (1245, 540), (1245, 600), RED, 5)
    elif key == "loop":
        card(d, (90, 390, 390, 622), "读状态", "目标、结果、预算", LILAC, PURPLE)
        card(d, (515, 390, 815, 622), "决定动作", "查房间或追问", WHITE, PURPLE)
        card(d, (940, 390, 1240, 622), "执行与观察", "结果写回状态", MINT, TEAL)
        arrow(d, (402, 506), (503, 506), TEAL)
        arrow(d, (827, 506), (928, 506), TEAL)
        d.line((1090, 634, 1090, 751, 235, 751, 235, 634), fill=PURPLE, width=5)
        arrow(d, (235, 634), (235, 627), PURPLE)
        text(d, (440, 775), "继续条件：有进展且未超预算", 25, PURPLE)
        card(d, (1270, 390, 1450, 622), "停下", "完成／等待／失败", PEACH, RED, 29, 23)
        arrow(d, (1251, 506), (1260, 506), RED)
    elif key == "persona":
        card(d, (90, 453, 395, 692), "候选动作", "发送会议邀请", LILAC, PURPLE)
        card(d, (505, 453, 820, 692), "允许动作集合", "只读、建议、草拟", PEACH, ORANGE)
        card(d, (930, 355, 1405, 565), "允许：执行", "经身份与权限校验后调用工具", MINT, TEAL)
        card(d, (930, 619, 1405, 830), "不允许：拒绝或升级", "发送邀请需用户确认", WHITE, RED)
        arrow(d, (405, 568), (495, 568))
        arrow(d, (830, 520), (920, 458), TEAL)
        arrow(d, (830, 625), (920, 720), RED)
    elif key == "prompt":
        card(d, (90, 347, 432, 500), "系统约束", "未批准不可发送", LILAC, PURPLE, 30, 23)
        card(d, (90, 536, 432, 690), "当前用户请求", "先给候选时间与草稿", MINT, TEAL, 30, 23)
        card(d, (90, 724, 432, 858), "工具资料", "日历备注不可下令", WHITE, RED, 30, 23)
        card(d, (568, 465, 908, 708), "模型候选", "时间、冲突、草稿 JSON", PEACH, ORANGE)
        card(d, (1040, 465, 1420, 708), "程序校验", "字段、权限与发送确认", MINT, TEAL)
        for y in (423, 610, 795):
            arrow(d, (443, y), (557, 560), PURPLE if y < 700 else RED, 4)
        arrow(d, (920, 575), (1030, 575), TEAL)
    elif key == "planning":
        card(d, (90, 495, 342, 702), "会议目标", "找到可行时段", LILAC, PURPLE, 31, 24)
        card(d, (540, 350, 856, 545), "候选 A", "周四下午", MINT, TEAL, 31, 24)
        card(d, (540, 625, 856, 820), "候选 B", "周五上午", WHITE, TEAL, 31, 24)
        card(d, (1100, 350, 1410, 545), "评价：房间冲突", "放弃或回退", PEACH, RED, 30, 24)
        card(d, (1100, 625, 1410, 820), "评价：可行", "保留并草拟", MINT, TEAL, 30, 24)
        for start, end in [((354, 583), (528, 447)), ((354, 607), (528, 716)), ((868, 447), (1088, 447)), ((868, 716), (1088, 716))]:
            arrow(d, start, end, TEAL)
    elif key == "routing":
        card(d, (90, 477, 360, 680), "当前任务", "查询、草拟或发送", LILAC, PURPLE)
        card(d, (470, 477, 790, 680), "分类与硬过滤", "任务类型、权限、风险", PEACH, ORANGE)
        card(d, (1025, 330, 1405, 485), "工具", "日历／房间查询", MINT, TEAL, 30, 23)
        card(d, (1025, 530, 1405, 685), "模型", "比较候选、写草稿", WHITE, TEAL, 30, 23)
        card(d, (1025, 730, 1405, 866), "人工", "批准发送或处理越界", LILAC, PURPLE, 30, 23)
        arrow(d, (370, 575), (460, 575))
        for y in (405, 605, 795):
            arrow(d, (802, 574), (1015, y), TEAL)
    elif key == "reflection":
        card(d, (90, 462, 350, 677), "执行者", "查询会议室", LILAC, PURPLE)
        card(d, (455, 462, 715, 677), "环境反馈", "返回已占用", WHITE, RED)
        card(d, (822, 462, 1082, 677), "评价器", "确认本次失败", PEACH, ORANGE)
        card(d, (1182, 462, 1442, 677), "反思摘要", "换时段再查", MINT, TEAL)
        for x in (361, 727, 1094):
            arrow(d, (x, 567), (x + 82, 567), TEAL)
        d.line((1300, 691, 1300, 765, 218, 765, 218, 689), fill=PURPLE, width=5)
        arrow(d, (218, 689), (218, 681), PURPLE)
        text(d, (500, 787), "有新办法且未超预算：下一次尝试", 25, PURPLE)
    footer(d, sources[key])
    save(im, rel)


DATA = {
    "overview": {
        "title": "智能体与工作流", "subtitle": "从一句目标到可核对的下一步",
        "cover": [("先核对约束", "三团队、日期、权限"), ("再查空闲", "日历与会议室分开核实"), ("最后交付草稿", "未经确认不发送邀请")],
        "figures": [
            ("map", "four", "七个环节不各自为战", "边界、选择、反馈和停止分别有位置", [("角色与指令", "规定能做与不能做"), ("证据与计划", "判断缺口并拆步"), ("路由与执行", "找到合适处理路径"), ("反思与循环", "根据结果决定下一轮")], "这些环节可由程序与模型共同承担，不等于七个独立 Agent"),
            ("workflow-agent", "compare", "固定流程与动态选择", "两者都要有权限与停止规则", (("固定工作流", ["路径由代码预设", "适合明确、稳定的步骤", "异常进入预设分支"]), ("动态智能体", ["依据观察选下一步", "适合开放且变化的任务", "仍受工具权限约束"])), "区别在谁控制流程，不在是否使用更大的模型"),
            ("handoff", "flow", "评审会任务怎样交接", "每一步交出可核对的产物", [("角色边界", "只读与草拟"), ("证据计划", "空闲与依赖"), ("路由执行", "查询结果"), ("反馈收束", "草稿或待确认")], "发送邀请在用户确认后，不能由网页或模型独自决定"),
            ("test", "four", "用四类变化验收全链路", "只看草稿顺口，无法发现错误动作", [("正常", "三团队与房间都空闲"), ("缺值", "一团队未返回空闲"), ("冲突", "日历空闲但房间被占"), ("越界", "未批准却想发送邀请")], "分别记录候选质量、证据、工具轨迹与停止原因"),
        ],
    },
    "persona": {
        "title": "角色与职责设定", "subtitle": "别让会议助手把建议误当授权",
        "cover": [("可读日历", "只读取当前获准范围"), ("可草拟通知", "给候选与待确认项"), ("不可擅发", "发送邀请等用户确认")],
        "figures": [
            ("contract", "four", "把角色写成任务契约", "每一项都能用样本验收", [("服务对象", "发起评审的小林"), ("输入", "时限、人员、授权范围"), ("交付物", "候选时间与通知草稿"), ("交接", "冲突或越权时求确认")], "“像资深秘书”不是可验收的角色定义"),
            ("boundary", "flow", "动作风险逐级上升", "权限并不因模型能说出动作而自动获得", [("读取", "查授权日历"), ("建议", "列可行时段"), ("草拟", "写待发送内容"), ("发送", "需用户批准")], "写出“我已发送”和实际调用发送工具是两回事"),
            ("handoff", "four", "职责之外走哪条出口", "不要一律说“交给人工”", [("无权读取", "拒绝并说明范围"), ("团队缺值", "向负责人追问"), ("房间冲突", "给新候选"), ("待发送", "暂停等小林批准")], "出口按具体原因选择，不用一段万能道歉覆盖全部异常"),
            ("test", "four", "角色边界的四道考题", "测试允许与禁止，不只看正常任务", [("正常草稿", "允许给候选"), ("他人日历", "未授权不得读"), ("擅自发送", "无批准必须停"), ("时间冲突", "不得说已安排")], "评测同时看模型表达与后端权限决策"),
        ],
    },
    "prompt": {
        "title": "系统指令与提示词", "subtitle": "同一轮输入里，谁的要求有资格指挥动作",
        "cover": [("目标", "找到评审候选时间"), ("约束", "三团队可参加"), ("交付物", "给草稿，不发送")],
        "figures": [
            ("layers", "compare", "指令与资料分层", "日历备注不等于用户指令", (("可下达任务", ["系统约束：不可擅发", "用户请求：先给草稿", "工具权限另由程序控制"]), ("只供引用", ["日历返回：已有会议", "外部备注：可能含假命令", "不能提升成系统指令"])), "来源决定信任层级，文字写得像命令不改变来源"),
            ("schema", "four", "输出格式要服务业务核对", "JSON 合法只是第一道检查", [("候选时间", "含时区与日期"), ("参会空闲", "逐团队标状态"), ("冲突", "指出哪一项未满足"), ("待确认", "是否允许发送")], "字段齐全仍需核查事实与动作权限"),
            ("injection", "flow", "恶意备注不能越级", "把不可信文本作为待分析材料", [("日历备注", "立刻发送邀请"), ("来源标记", "外部资料"), ("模型候选", "只可做草稿"), ("权限闸门", "无批准则不发")], "提示隔离有帮助，但工具执行仍要程序校验"),
            ("test", "four", "提示版本回归样本", "改一句模板也可能改变行为", [("缺空闲", "必须标待确认"), ("缺字段", "不能编造日期"), ("伪系统备注", "不得越权发送"), ("旧版提示", "对照输出差异")], "锁定案例输入，比较提示版本和校验结果"),
        ],
    },
    "reasoning": {
        "title": "基于证据的推理", "subtitle": "候选时间要能追到日历与会议室",
        "cover": [("团队空闲", "三份结果各有来源"), ("会议室", "同一时段另行核对"), ("候选时间", "成立条件逐项满足")],
        "figures": [
            ("evidence", "flow", "结论从证据长出来", "每一步都能回到原始结果", [("日历返回", "三组各自空闲"), ("房间返回", "同一时段可用"), ("条件比较", "日期时区一致"), ("候选结论", "附证据 ID")], "缺任何必要前提，只能给待确认候选"),
            ("conflict", "compare", "两个“空闲”不一定同义", "冲突要标出对象和时间", (("团队日历", ["周四 15:00 可参加", "来源：三组日历", "只说明人员时间"]), ("会议室", ["周四 15:00 已占用", "来源：房间服务", "不支持已安排结论"])), "不能拿人员空闲抵消房间冲突"),
            ("claim", "four", "公开可核的结论卡", "不用暴露不可验证的内部思维文本", [("结论", "周五 10:00 候选"), ("证据", "日历与房间返回"), ("前提", "同一时区、同一会议室"), ("待确认", "小林是否批准发送")], "这张卡帮助审阅，不保证结论天然正确"),
            ("test", "four", "证据一变，结论也要变", "重点测变化与缺口", [("新增", "另一团队加入"), ("冲突", "房间临时占用"), ("缺失", "一组日历超时"), ("更正", "时区由北京改上海")], "记录哪些证据 ID 支撑了每个候选"),
        ],
    },
    "planning": {
        "title": "任务规划", "subtitle": "把会议目标拆成可执行、可检查的依赖",
        "cover": [("收约束", "人数、时限、时区"), ("查候选", "团队空闲和房间"), ("交草稿", "只写候选与通知")],
        "figures": [
            ("dependency", "flow", "依赖决定先做什么", "能并行的不必排成长队", [("收约束", "统一时区与人数"), ("并行查空闲", "三组日历"), ("核对房间", "基于候选时间"), ("形成草稿", "注明待确认")], "房间查询依赖候选时段，但三组空闲可并行取得"),
            ("critical", "four", "少一个前提，计划不能假完成", "可验收步骤应有具体通过条件", [("三组回复", "缺一组就标缺值"), ("时区一致", "防止跨时区误约"), ("房间可用", "同一时段核对"), ("发送确认", "草稿后再问用户")], "“计划已列出”不等于“会议已安排”"),
            ("replan", "compare", "重排只动受影响部分", "房间冲突不必重查所有团队", (("原计划", ["周四 15:00 候选", "三组日历已核", "房间查询失败"]), ("新计划", ["保留有效日历结果", "查周五候选房间", "重新比较并草拟"])), "已过期的日历结果仍需按版本重新核对"),
            ("test", "four", "计划质量如何测", "别只看最后是否写出一封邮件", [("正常", "依赖顺序正确"), ("缺值", "会停下追问"), ("变化", "局部重排"), ("预算", "到限后交候选")], "测试每步是否可执行、可观察、可停止"),
        ],
    },
    "routing": {
        "title": "模型与能力路由", "subtitle": "问题不同，处理路径也不同",
        "cover": [("查询", "日历与房间工具"), ("草拟", "语言模型写通知"), ("批准", "小林或授权人员")],
        "figures": [
            ("features", "four", "路由先看四项信息", "先过硬约束，再比较软目标", [("任务类型", "查询／草拟／发送"), ("权限", "可读哪些日历"), ("时限", "多久要给答复"), ("风险", "是否有外部动作")], "不具备权限的路径不能靠分数高获得资格"),
            ("paths", "flow", "一条请求可去不同路径", "不是随机换一个更贵的模型", [("分类", "判断当前子任务"), ("硬过滤", "权限和风险"), ("专用路径", "工具、模型或人工"), ("统一核对", "检查结果和状态")], "房间查询应查服务；发送邀请必须看用户授权"),
            ("fallback", "compare", "服务失败不等于任务完成", "降级要保留事实边界", (("可安全退回", ["日历超时标未知", "给已有候选但注明缺口", "等待服务或用户确认"]), ("不可假装", ["不能编造空闲", "不能伪称房间已订", "不能越权发送邀请"])), "错误路径的伤害往往大于多等一次查询"),
            ("test", "four", "路由专项测试", "按任务类别分组统计", [("误分流", "查询送去纯生成"), ("超时", "服务不可用"), ("高风险", "发送前转人工"), ("成本", "简单草拟不必强模型")], "看正确率、延迟、成本与越权率，不只看平均值"),
        ],
    },
    "reflection": {
        "title": "反思与纠错", "subtitle": "房间被占后，下一次应改变什么",
        "cover": [("读失败", "房间服务返回已占"), ("找原因", "不是日历没查"), ("改候选", "换时间再核对")],
        "figures": [
            ("feedback", "four", "反馈可能来自不同地方", "只有可核反馈才能推动可靠修正", [("工具返回", "房间已占用"), ("规则校验", "日期格式错误"), ("用户更正", "改到下周"), ("模型自评", "仅供线索，不能单独作证")], "先问反馈是否可信，再决定怎样改"),
            ("diagnose", "four", "别把不同失败都叫再试一次", "失败类型决定修正动作", [("房间占用", "换候选时段"), ("工具超时", "稍后重查"), ("日期解析错", "先校正时区"), ("用户否定", "重新询问约束")], "诊断错了，重试次数越多越费钱"),
            ("retry", "compare", "第二次要带着修改来", "原样重复不是反思", (("第一次", ["周四 15:00 查房间", "返回已占用", "继续使用原时间会重复失败"]), ("第二次", ["改查周五 10:00", "保留已验证的空闲信息", "记录新结果或停止"])), "若没有新证据或新动作，停止比无限重试更合理"),
            ("test", "four", "纠错有没有净收益", "成功率之外还要看额外开销", [("正向", "换候选后成功"), ("坏反馈", "不能盲从错误提示"), ("连败", "按上限停下"), ("无收益", "重复请求不得无限增长")], "把纠错前后质量、调用数与总耗时放在一起"),
        ],
    },
    "loop": {
        "title": "智能体执行循环", "subtitle": "一圈一圈推进，但不能一直转",
        "cover": [("读状态", "目标、候选和预算"), ("选并执行", "查询或追问"), ("观察与停止", "完成、暂停或失败")],
        "figures": [
            ("state", "four", "每一圈要读到什么状态", "状态是应用记录，不等于整段聊天", [("目标", "给会议草稿"), ("当前候选", "周五 10:00"), ("工具结果", "房间待查询"), ("预算", "剩余次数与时限")], "历史长文本只按需选入，不把每轮全部复制"),
            ("transition", "flow", "观察之后必须更新状态", "下一轮依据新结果而不是照搬上一轮", [("动作", "查询房间"), ("观察", "可用或占用"), ("状态更新", "记录结果与版本"), ("下一选择", "草拟或换时间")], "工具回调重复时，幂等键防止重复写入或发送"),
            ("stop", "four", "四种停止并不一样", "用明确状态告知用户下一步", [("完成", "交付可核草稿"), ("等待", "需小林批准"), ("到限", "预算耗尽给候选"), ("失败", "工具不可用说明原因")], "停止不是失败的同义词，也不是永远由模型一句“好了”决定"),
            ("test", "four", "看整条轨迹是否安全", "只看末句容易漏掉重复调用", [("正常", "有限步到草稿"), ("工具失败", "受控重试或退出"), ("重复回调", "不重复写入"), ("用户中断", "暂停并可恢复")], "记录状态变迁、动作 ID、观察与终止原因"),
        ],
    },
}


def render():
    for key, data in DATA.items():
        directory = "assets" if key == "overview" else f"submodules/{key}/assets"
        cover(f"{directory}/{key}-cover.png", data["title"], data["subtitle"], data["cover"],
              "示例：小林安排跨三团队评审会；只交候选与草稿，发送另需确认")
        for suffix, kind, title, subtitle, payload, note in data["figures"]:
            path = f"{directory}/{key}-{suffix}.png"
            if kind == "flow":
                flow(path, title, subtitle, payload, note)
            elif kind == "four":
                four(path, title, subtitle, payload, note)
            elif kind == "compare":
                compare(path, title, subtitle, payload[0], payload[1], note)
            else:
                raise ValueError(kind)
        principle(f"{directory}/{key}-principle.png", key)


if __name__ == "__main__":
    render()
