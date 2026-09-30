# 状态与任务图子模块配图提示词

版本：0.1.1；修订时间：2026-09-29 20:20 CST；依据提交：`ee5f838`（`main`；修订时本系列尚未提交，另有 Word 临时锁文件未跟踪）。

正文图 1536×1024，封面 900×383；暖白底、深灰文字、蓝绿状态、橙色转移、梅红异常。封面使用内置图像生成工具，正文由确定性脚本绘制。

1. `stategraph-cover-main-wechat.png`：标题“大话状态与任务图”“做到一半怎样接着跑”；研究任务在资料收集后中断，从检查点继续。
2. `stategraph-cover-interview-wechat.png`：标题“面试题：状态图怎样恢复任务”“又不重做危险动作”；突出检查点、版本和回执。
3. `stategraph-state-object.png`：状态对象包含任务 ID、当前节点、已核证据、外部动作状态、版本和更新时间。
4. `stategraph-transition.png`：明确节点、边和转移守卫，禁止从“待核对”直接跳到“已发布”。
5. `stategraph-checkpoint.png`：每个超级步形成检查点，并保留成功节点的待提交写入。
6. `stategraph-recovery.png`：安全重算、需要回读、禁止盲目重放三类恢复方式。
7. `stategraph-principle.png`：依据 Harel 1987 年 Statecharts 论文关于层级、并发与通信的思想，并结合 LangGraph checkpoint 文档改绘。保留“状态 → 受守卫的转移 → 新状态”“并行分支”“检查点序列”，不把具体框架 API 当成状态机定义。图注：“依据 Harel Statecharts 与 LangGraph checkpoint 概念改绘。”

复核：区分状态、聊天历史和长期记忆；恢复箭头不得绕过转移守卫。
