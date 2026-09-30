# 工作流子模块配图提示词

版本：0.1.1；修订时间：2026-09-29 20:20 CST；依据提交：`ee5f838`（`main`；修订时本系列尚未提交，另有 Word 临时锁文件未跟踪）。

正文图 1536×1024，封面 900×383；暖白底、深灰文字、青绿主色、橙色分支、梅红风险标记。封面使用内置图像生成工具，正文由确定性脚本绘制。

1. `workflow-cover-main-wechat.png`：标题“大话工作流”“路已经画好，模型负责哪一段”；报销票据沿固定轨道经过识别、规则校验、异常审核和草稿。
2. `workflow-cover-interview-wechat.png`：标题“面试题：工作流怎样重试”“又不重复提交”；突出幂等键、回执和补偿路径。
3. `workflow-fixed-path.png`：报销案例固定主路径，标出模型节点与代码节点。
4. `workflow-branching.png`：票据缺失、超标准、正常三条条件分支及停止点。
5. `workflow-idempotency.png`：同一请求 ID 重试只产生一份草稿；无幂等键时可能重复写入。
6. `workflow-observability.png`：一次执行的节点状态、输入摘要、输出、耗时和回执。
7. `workflow-principle.png`：依据 Anthropic《Building Effective AI Agents》的 prompt chaining、routing 与 parallelization 模式改绘。保留“预先定义步骤、条件门、模型节点、工具节点、失败分支”，强调控制路径由应用代码决定。图注：“依据 Anthropic workflow patterns 改绘。”

复核：不把工作流画成多个 Agent 自由聊天；重试箭头必须回到幂等检查之前。
