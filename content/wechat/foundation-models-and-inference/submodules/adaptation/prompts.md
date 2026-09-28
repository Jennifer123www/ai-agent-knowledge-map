# 模型适配子模块配图提示词

版本：0.2.0；修订时间：2026-09-28 17:26 CST；依据提交：`47c0ee0`（`main`，修订前 clean）。

统一规格：1536x1024 PNG，暖白背景，梅红、橙色和青绿色点缀，中文清晰，无水印、无 Logo。原有成片使用 `gpt-image-2`；本轮纠错图 `adaptation-lora.png` 和 `adaptation-distillation.png` 由 `scripts/render-foundation-figure-fixes.py` 确定性绘制。

1. `adaptation-cover.png`：封面，通用模型经过不同调校方法服务具体任务，标题“模型适配”，副标题“先找病因，再决定怎么改”。
2. `adaptation-decision.png`：选择树，标签“缺最新知识”“缺稳定格式”“缺领域行为”“缺低成本部署”，分支对应“检索”“规则”“微调”“蒸馏”。
3. `adaptation-lora.png`：冻结基础权重 `W`，训练低秩参数 `BA`，组合计算后得到任务输出；另标独立题集评测，不能用一条无数据的上升曲线暗示适配后必然改善。
4. `adaptation-distillation.png`：沿本文退款政策案例，教师模型生成示例、人工抽检后训练学生模型；独立评测新版、旧版与缺条件问题。原图猫狗车样例与本文案例无关，已撤换。
5. `adaptation-release.png`：发布闭环，标签“数据版本”“训练实验”“离线评测”“灰度发布”“回滚”。
6. `adaptation-principle.png`：原理图。依据 [LoRA](https://arxiv.org/abs/2106.09685) 第 4 节与 Figure 1 改绘。保留冻结基础权重 `W`、可训练低秩矩阵 `A/B`、增量 `BA` 与输出相加；说明 QLoRA 还会量化冻结底座。图注：“依据 Hu 等，第 4 节与 Figure 1 改绘。”

复核：已目视检查新图的主案例、训练与评测边界。
