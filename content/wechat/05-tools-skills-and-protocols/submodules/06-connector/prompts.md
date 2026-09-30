# 连接器子模块配图提示词

共 7 张图，使用 `gpt-image-2`、1536x1024 PNG、暖白背景、中文大标签和克制二维技术插画。

1. `connector-cover.png`：封面，外部 CRM、工单、日历经过连接器转换成统一能力，标题“连接器与插件：把外部系统翻译成 Agent 能用的能力”。
2. `connector-adapter.png`：外部字段、枚举、分页和错误经过适配层，输出领域能力，标签“外部系统”“字段映射”“领域能力”。
3. `connector-auth.png`：模型与凭据隔离，连接器从密钥库取得短期令牌访问系统，标签“模型”“连接器”“短期凭据”“外部系统”。
4. `connector-reliability.png`：分页、限流、幂等和部分成功四项可靠性处理。
5. `connector-errors.png`：供应商错误进入归一层，输出“参数”“权限”“限流”“超时”“冲突”。
6. `connector-evolution.png`：旧接口经过兼容映射、回归和灰度到新接口，保留回滚。
7. `connector-plugin.png`：插件安装前检查“来源”“权限”“版本”“依赖”，通过后进入受控运行环境。
8. `connector-principle.png`：原理图。依据 [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) 第 2–4 节的 OAuth 2.0 安全建议改绘。保留“模型意图 → 连接器 → 业务 API”，凭据服务只向连接器提供受限令牌，响应只返回允许字段；省略具体授权报文。图注：“依据 RFC 9700 改绘。”
