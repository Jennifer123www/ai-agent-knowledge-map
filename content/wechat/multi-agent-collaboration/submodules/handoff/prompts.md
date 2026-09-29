# 交接与人工参与子模块配图提示词

版本：0.1.1；修订时间：2026-09-29 20:20 CST；依据提交：`ee5f838`（`main`；修订时本系列尚未提交，另有 Word 临时锁文件未跟踪）。

正文图 1536×1024，封面 900×383；暖白底、深灰文字、青绿客服、橙色退款专家、梅红人工审批。封面使用内置图像生成工具，正文由确定性脚本绘制。

1. `handoff-cover-main-wechat.png`：标题“大话任务交接”“换人以后别从头再问”；退款请求从客服 Agent 交给退款专家，再把高金额审批交给人。
2. `handoff-cover-interview-wechat.png`：标题“面试题：Handoff 怎样换人”“又不丢状态”；展示交接包、控制权和恢复点。
3. `handoff-package.png`：交接包字段：已确认事实、证据、已做动作、未决项、交接原因、允许动作。
4. `handoff-control.png`：比较 Agent-as-tool“调用后返回主管”和 Handoff“接收方取得当前控制权”。
5. `handoff-human.png`：高金额退款冻结动作，生成审批包，人工批准/修改/拒绝后重新校验。
6. `handoff-resume.png`：暂停状态序列化，审批结果写回同一任务，再从原节点恢复。
7. `handoff-principle.png`：依据 OpenAI Agents SDK Handoffs 与 Human-in-the-loop 文档改绘。保留“交接作为工具选择 → 可选结构化 input → 输入过滤 → 接收 Agent 成为活动 Agent”；人工环节保留“中断 → 保存 RunState → 决定 → 恢复”。图注：“依据 OpenAI Agents SDK Handoffs 与 Human-in-the-loop 文档改绘。”

复核：Handoff 必须画出控制权转移；人工拒绝不能沿批准路径继续；敏感历史须经过过滤。
