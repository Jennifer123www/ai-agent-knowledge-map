# MCP 协议子模块配图提示词

共 6 张图，使用 `gpt-image-2`、1536x1024 PNG、暖白背景、少量大字号中文标签和清楚连接线。

1. `mcp-cover.png`：封面，多个 AI 应用通过统一连接规则接入外部能力，标题“MCP：给 AI 应用一套共同的连接规则”。
2. `mcp-layers.png`：数据层与传输层两层结构，标签“数据层”“传输层”。
3. `mcp-discovery.png`：连接建立与能力发现，标签“连接”“身份”“版本”“能力目录”。
4. `mcp-local-remote.png`：本地进程和远程服务对比，标签“本地”“远程”“标准输入输出”“HTTP”。
5. `mcp-security.png`：协议连接外侧与业务授权内侧的边界，标签“认证”“授权”“参数校验”“审计”。
6. `mcp-compatibility.png`：版本升级与兼容回归，标签“旧版本”“能力变化”“兼容测试”“灰度”“回滚”。
7. `mcp-principle.png`：原理图。依据 [MCP 2025-06-18 Basic / Lifecycle](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle) 改绘。严格保留 `initialize` 请求、版本与能力响应、`notifications/initialized`，之后才进入能力发现或调用。图注：“依据 MCP 2025-06-18 Lifecycle 规范改绘。”
