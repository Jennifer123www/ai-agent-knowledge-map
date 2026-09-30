# 模型适配子模块配图提示词

版本：0.3.0；修订时间：2026-09-29 16:22 CST；依据提交：`549c2cc`（`main`；修订前仅有 Word 临时锁文件未跟踪）。

正文配图统一为 1536×1024 PNG；公众号封面图统一为 900×383 PNG。暖白背景，梅红、橙色和青绿色点缀，中文清晰，无水印、无 Logo。封面图使用内置图像生成工具；结构图 `adaptation-lora.png`、`adaptation-distillation.png` 与 `adaptation-diagnosis-matrix.png` 由 `scripts/render-foundation-figure-fixes.py` 确定性绘制。

1. `adaptation-cover-main-wechat.png`：主文封面图。标题“大话模型适配”“旧政策答错了要微调吗”；围绕通用模型分出“更新证据、提示与规则、LoRA 适配器、蒸馏后的小模型”，底部写“先找病因，再决定怎么改”。
2. `adaptation-cover-interview-wechat.png`：面试副文封面图。标题“面试题：旧政策答错了该不该微调”；用故障清单、方法卡和验收清单表现诊断过程。
3. `adaptation-decision.png`：选择树，标签“缺最新知识”“缺稳定格式”“缺领域行为”“缺低成本部署”，分支对应“检索”“规则”“微调”“蒸馏”。
4. `adaptation-lora.png`：冻结基础权重 `W`，训练低秩参数 `BA`，组合计算后得到任务输出；另标独立题集评测，不能用一条无数据的上升曲线暗示适配后必然改善。
5. `adaptation-distillation.png`：沿本文退款政策案例，教师模型生成示例、人工抽检后训练学生模型；独立评测新版、旧版与缺条件问题。原图猫狗车样例与本文案例无关，已撤换。
6. `adaptation-release.png`：发布闭环，标签“数据版本”“训练实验”“离线评测”“灰度发布”“回滚”。
7. `adaptation-diagnosis-matrix.png`：故障诊断图。把“最新事实缺失、固定格式不稳、领域行为不稳、部署成本过高”分别映射到“RAG、模板或规则、SFT/LoRA、蒸馏”，强调先判断病因。
8. `adaptation-principle.png`：原理图。依据 [LoRA](https://arxiv.org/abs/2106.09685) 第 4 节与 Figure 1 改绘。保留冻结基础权重 `W`、可训练低秩矩阵 `A/B`、增量 `BA` 与输出相加；说明 QLoRA 还会量化冻结底座。图注：“依据 Hu 等，第 4 节与 Figure 1 改绘。”

复核：已目视检查主案例、训练与评测边界、`BA` 矩阵顺序和封面图中央安全区；正文不重复插入封面图。
