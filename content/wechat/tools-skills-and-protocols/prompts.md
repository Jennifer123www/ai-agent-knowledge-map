# 工具、技能与协议: 微信文章配图提示词

## 文档元数据

| 项目 | 值 |
| --- | --- |
| 版本 | `0.2.0` |
| 阶段 | 文章试点: 10 张 `gpt-image-2` PNG 已渲染并完成图中文字目视检查，等待文章正文引用 |
| Git 基线 | `b9fa9c8`（`main`；更新本文档时工作区含未跟踪的 `content/`） |
| 修改时间 | `2026-09-20 10:56 CST` |

## 使用说明

本清单为“工具、技能与协议”试点文章准备 10 张 PNG 配图。每张图只保留少量、大字号的中文标签；`Skill`、`Tool`、`MCP` 是保留的英文专有名词。图像生成后应逐字检查图中文字，若有错别字、漏字或英文拼写错误，重新渲染该图，不能用近似字替代。

- 目标模型：`gpt-image-2`，通过 `zcode-image` 插件渲染。
- 风格：研究型中文知识插画，暖白纸张底色，深墨绿正文，青绿、橙色、梅红作分组强调；二维平面编辑插画，线条清楚、留白充足。
- 共通限制：不出现水印、品牌标志、无关英文、人物脸部特写、花哨渐变、密集小字或伪代码；画面中的文字必须是下文给出的逐字文本，且不要额外添加任何文字。
- 文件策略：不覆盖现有的 `beginner-cover.png` 草图；10 张 `gpt-image-2` 成片已存为带 `-image-2` 后缀的 PNG，待文章引用确认后再清理草图。

## 主文: 面向初学者与“大话”结合

文章标题：**从会回答到能办事：把 AI Agent 的工具、技能与 MCP 讲明白**

### B0. 首页大图

- 建议文件：`assets/beginner-cover-image-2.png`
- 尺寸：`1536x1024`

```text
Use case: scientific-educational
Asset type: 微信公众号文章首页大图
Primary request: 为一篇中文 AI Agent 入门文章绘制编辑型知识插画，表现“语言模型从回答问题到受控地完成真实动作”的转变。画面主体是一张暖白色工作台：中央是一位没有具体面孔的简洁 AI 助手形象，面前有三条清楚的能力轨道，分别通向步骤清单、工具箱、连接器；最右端是带绿色勾选的业务结果回执。用箭头表现从理解任务到执行确认的流动。
Scene/backdrop: 暖白纸张质感背景，少量细网格和细线，不要真实办公室照片。
Style/medium: 高级但克制的二维中文知识插画，像科技杂志的编辑配图，扁平图形结合轻微纸张纹理。
Composition/framing: 横向 3:2，标题在上方居中，主体在下方居中，视觉层级明确，留白充足。
Color palette: 暖白、深墨绿、青绿、橙色、梅红，避免蓝紫渐变。
Text (verbatim): "从会回答到能办事"、"工具、技能与 MCP"
Constraints: 两行标题必须逐字准确、字号大且清晰；三条轨道可使用无文字图标，不要生成其他文字；无水印、无 Logo、无额外英文。
Avoid: 赛博霓虹、密集电路板、卡通人物、复杂背景、错误中文。
```

### B1. 从意图到真实动作

- 建议文件：`assets/beginner-intent-to-action-image-2.png`
- 尺寸：`1536x1024`

```text
Use case: scientific-educational
Asset type: 微信文章正文知识图解
Primary request: 绘制一张横向流程图，面向初学者解释 AI Agent 的工具调用链。四个等宽的大模块由粗箭头连接：用户提出任务，模型选择能力，执行层进行校验，系统回读真实结果。每一模块用单一具象图标辅助理解：任务单、路线选择、盾牌与钥匙、带勾的状态回执。强调模型并不直接越过执行层操作外部系统。
Scene/backdrop: 暖白纯净背景，顶部是简短标题，主体是一条居中的四步流程线。
Style/medium: 二维中文信息图，线条清楚，边框与箭头统一，适合手机屏幕阅读。
Composition/framing: 横向 3:2，大字号，四个模块之间的箭头有足够留白。
Color palette: 墨绿为主线，青绿表示理解，橙色表示校验，梅红表示外部风险提示。
Text (verbatim): "任务"、"选择能力"、"执行校验"、"结果回读"
Constraints: 四个标签必须逐字准确且是画面中仅有的文字；每个标签独占一行；不出现步骤编号、不出现英文、不出现段落说明；无水印。
Avoid: 小字说明、密集表格、程序代码、箭头交叉、错误中文。
```

### B2. Skill、Tool 与 MCP 的分工

- 建议文件：`assets/beginner-skill-tool-mcp-image-2.png`
- 尺寸：`1536x1024`

```text
Use case: scientific-educational
Asset type: 微信文章正文知识图解
Primary request: 以“餐厅后厨协作”的抽象类比绘制三层分工图，但不要出现真实人物。左侧是一张做菜流程卡代表可复用的方法，中间是一把带标签的专用工具代表一次具体动作，右侧是接口与插头组成的连接台代表不同系统之间的共同语言。三个对象从左到右排列，底部用一条细线连接，表达它们相互配合但职责不同。
Scene/backdrop: 暖白背景，三栏等宽，宽边距，适合读者一眼比较。
Style/medium: 极简编辑插画与信息图结合；象征物比文字更重要，但标签必须准确。
Composition/framing: 横向 3:2，三栏居中，大图标在上、标签在下。
Color palette: 左栏墨绿，中央橙色，右栏青绿；深色文字。
Text (verbatim): "Skill"、"方法"、"Tool"、"动作"、"MCP"、"连接"
Constraints: 六个标签必须逐字准确，且是唯一文字；每栏只出现两个标签；不使用“插件”等容易混淆的词；无水印、无品牌标志。
Avoid: 错别字、小号英文、任何额外文字、拟人化厨师、杂乱装饰。
```

### B3. MCP 的对象关系

- 建议文件：`assets/beginner-mcp-architecture-image-2.png`
- 尺寸：`1536x1024`

```text
Use case: scientific-educational
Asset type: 微信文章正文知识图解
Primary request: 绘制 MCP 的极简架构图。左侧是一个 AI 应用中的 MCP Client，中间是 MCP Server，右侧纵向排列三种能力对象：可执行动作、可读取资料、可复用模板。箭头从 Client 指向 Server，再从 Server 分发到三个对象。Server 下方以一个小型安全闸门图标暗示认证和授权不由协议自动解决，但不要增加解释文字。
Scene/backdrop: 暖白背景，三列结构，连接线清楚。
Style/medium: 严谨、克制的技术知识插画，圆角轻微，扁平图标。
Composition/framing: 横向 3:2，右侧三个对象垂直堆叠；所有文字至少占画面高度的 5%。
Color palette: Client 为青绿，Server 为墨绿，三个对象以橙色、梅红、浅青区分。
Text (verbatim): "MCP Client"、"MCP Server"、"工具"、"资源"、"提示模板"
Constraints: 五个标签逐字准确；不要写缩写解释、段落、序号或其他文字；无水印、无 Logo。
Avoid: 网络拓扑密集线、云厂商品牌、错误英文拼写、细小文字。
```

### B4. 有副作用动作的安全闸门

- 建议文件：`assets/beginner-safe-action-image-2.png`
- 尺寸：`1536x1024`

```text
Use case: scientific-educational
Asset type: 微信文章正文知识图解
Primary request: 绘制一条从“模型建议”通往“真实写入”的受控通道。第一段是一张模型给出的操作卡片；第二段是一道带钥匙、额度刻度和参数检查符号的安全闸门；第三段是人工审批按钮；第四段是账本和状态回执。四段连续排列，用绿色通行和橙色拦截表达安全边界。重点表现“建议不等于放行”。
Scene/backdrop: 暖白背景，主流程在中间，足够留白。
Style/medium: 清楚、稳重的二维技术插画，不使用威胁或恐怖画面。
Composition/framing: 横向 3:2，四个模块相等，箭头从左到右。
Color palette: 墨绿、青绿、橙色、梅红；盾牌和钥匙图标醒目。
Text (verbatim): "模型建议"、"策略校验"、"人工审批"、"执行回读"
Constraints: 只出现四个大标签，逐字准确；无英文、无水印、无多余说明。
Avoid: 代码片段、锁屏界面、过多告警图标、错别字、小字。
```

## 副文: 面试答题训练

文章标题：**面试官问工具调用与 MCP：别只回答“它是插件协议”**

### I1. 面试回答骨架

- 建议文件：`assets/interview-answer-skeleton-image-2.png`
- 尺寸：`1536x1024`

```text
Use case: productivity-visual
Asset type: 微信文章正文答题框架图
Primary request: 为 AI Agent 面试题绘制一张四段式回答框架图。四张简洁大卡片依次排开，像演讲稿的四个段落：先给出定义，再说明运行机制，然后讨论方案取舍，最后落到生产治理。每张卡片有不同的抽象图标：边界框、流程箭头、天平、盾牌与记录本。视觉上表现“答案从概念走到上线”。
Scene/backdrop: 干净暖白背景，卡片不是悬浮 UI，而是编辑版式中的四个并列信息块。
Style/medium: 简洁、正式的中文面试知识图。
Composition/framing: 横向 3:2，四栏，标签大且位于每栏中央。
Color palette: 墨绿、青绿、橙色、梅红逐栏分配。
Text (verbatim): "定义"、"机制"、"取舍"、"治理"
Constraints: 只使用四个中文标签，逐字准确；不要题号、不要英文、不要细小说明；无水印。
Avoid: 真实面试官人物、聊天气泡、夸张奖杯、错误中文。
```

### I2. Tool Calling 的完整闭环

- 建议文件：`assets/interview-tool-calling-cycle-image-2.png`
- 尺寸：`1536x1024`

```text
Use case: scientific-educational
Asset type: 微信文章正文机制图解
Primary request: 绘制 Tool Calling 的闭环流程。用户任务输入进入模型，模型只输出结构化的调用建议；独立执行器做权限和参数校验；外部业务系统执行；结果沿一条回流线返回模型，帮助它给出回答、重试或升级。把“模型提议”和“执行器校验”用明显不同颜色区分。
Scene/backdrop: 暖白背景，一条主流程从左到右，底部有一条回流弧线。
Style/medium: 面向面试的严谨中文信息图，图标简单，结构关系优先。
Composition/framing: 横向 3:2，五个节点，末尾的回流线回到第二个节点。
Color palette: 墨绿主线，模型节点青绿，执行器节点橙色，外部系统梅红点缀。
Text (verbatim): "任务输入"、"模型提议"、"执行校验"、"外部系统"、"结果回流"
Constraints: 五个标签逐字准确；每个节点只放一个标签；不出现 Function Calling 等额外英文；无水印。
Avoid: 黑箱、代码、复杂接口字段、交叉箭头、错误中文。
```

### I3. MCP 架构与三类对象

- 建议文件：`assets/interview-mcp-objects-image-2.png`
- 尺寸：`1536x1024`

```text
Use case: scientific-educational
Asset type: 微信文章正文面试图解
Primary request: 面向技术面试，绘制 MCP 的对象关系和权限边界。左侧是使用方 MCP Client，中间是提供方 MCP Server，右侧是三种对象：工具、资源、提示模板。Client 与 Server 之间是一条受认证的连接线；Server 下方有一个醒目的边界围栏，标记业务系统自己的授权范围。画面应表达协议统一交互，但权限仍需独立治理。
Scene/backdrop: 暖白背景，三层横向结构，右侧对象纵向排列。
Style/medium: 严谨的技术杂志信息图，轻量的安全边界图标。
Composition/framing: 横向 3:2，所有模块留白，连线少而清楚。
Color palette: 深墨绿与青绿为主，橙色突出权限围栏。
Text (verbatim): "MCP Client"、"MCP Server"、"工具"、"资源"、"提示模板"、"授权边界"
Constraints: 六个标签完全准确；“授权边界”必须放在 Server 下方；不出现其他文字或品牌；无水印。
Avoid: 把 MCP 画成单一插件、云厂商品牌图标、复杂微服务图、错误英语。
```

### I4. 执行通道如何选择

- 建议文件：`assets/interview-execution-choice-image-2.png`
- 尺寸：`1536x1024`

```text
Use case: productivity-visual
Asset type: 微信文章正文方案比较图
Primary request: 绘制三列决策比较图，帮助回答“API、隔离代码执行和浏览器自动化怎么选”。左列表现一个稳定且可审计的接口插头，中列表现被围栏隔离的计算工作台，右列表现一个需要谨慎操作的浏览器窗口。三列从左到右表示优先级降低，但不要使用额外说明句。
Scene/backdrop: 暖白背景，三栏等宽，顶部可有一条无文字的优先级阶梯。
Style/medium: 冷静、实用的中文技术比较图，适合手机端阅读。
Composition/framing: 横向 3:2，大图标加大标签，列间对比清楚。
Color palette: 左列墨绿，中列青绿，右列橙色；梅红只用于风险提醒符号。
Text (verbatim): "API"、"隔离代码执行"、"浏览器自动化"
Constraints: 三个标签逐字准确，且是唯一文字；不要添加“首选”“最后”等额外文字；无水印。
Avoid: 浏览器品牌 Logo、代码段、错误中文、小字表格。
```

### I5. 超时后的可靠性恢复

- 建议文件：`assets/interview-failure-recovery-image-2.png`
- 尺寸：`1536x1024`

```text
Use case: scientific-educational
Asset type: 微信文章正文可靠性图解
Primary request: 绘制一次有副作用的工具调用超时后该如何处理。左边是一个带沙漏的“超时”节点，箭头先到“查询状态”，再分成三条明确分支：已完成、可重试、需要升级。已完成分支带绿色对勾，可重试分支带幂等钥匙图标，需要升级分支带人工桌面图标。核心意思是先确认真实状态，不能盲目重复执行。
Scene/backdrop: 暖白背景，从左到右的分支流程，分支线条不交叉。
Style/medium: 面向面试的简明故障恢复信息图。
Composition/framing: 横向 3:2，前两步居左，三条分支均衡地排在右侧。
Color palette: 橙色表示超时，青绿表示查询，绿色表示完成，梅红表示升级。
Text (verbatim): "超时"、"查询状态"、"已完成"、"可重试"、"人工升级"
Constraints: 五个标签逐字准确；不要把“可重试”写成“立即重试”；无英文、无水印、无其他文字。
Avoid: 报错堆栈、杂乱箭头、黑红恐怖风、错误中文。
```

## 渲染与验收顺序

1. 先渲染 B0，确认暖白底色、中文标题、配色与线条风格。
2. 以 B0 为风格基准，分别渲染 B1 至 B4 与 I1 至 I5；图与图之间不做拼图，便于文章单独排版。
3. 每张图以原尺寸检查：所有标签逐字正确、没有多余文字、箭头方向与文本含义一致、无水印。
4. 发现文字问题时，使用原提示词加上“仅修正文字，其余构图不变”的定向提示重新渲染；不能用 SVG 覆盖或手工叠加文字冒充生成图。
