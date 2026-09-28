# 大语言模型子模块配图提示词

统一规格：`gpt-image-2`，1536x1024 PNG，暖白背景，梅红与深灰为主，少量青绿，简洁中文信息图，无水印、无 Logo、无小字说明。

1. `llm-cover.png`：封面，像接龙一样逐个生成 token，标题“大语言模型”，副标题“会续写，才有了会表达”。
2. `llm-token-generation.png`：生成循环，标签“输入 token”“概率分布”“选择下一个”“继续生成”。
3. `llm-sampling.png`：解码策略对比，标签“贪心解码”“低温度”“高温度”“Top-k”“Top-p”，说明候选概率差距与候选范围怎样变化；不要把温度画成“准确率”或“语气”旋钮。当前成片只有“低温度”“高温度”“Top-p”，下次按此说明重绘。
4. `llm-reliability.png`：可靠性护栏，标签“检索证据”“工具结果”“结构校验”“人工确认”。

5. `llm-principle.png`：原理图。依据 [Attention Is All You Need](https://arxiv.org/abs/1706.03762) Figure 2 与第 3.2.3 节改绘。保留 `Q`、`K`、`V`、缩放点积、`softmax`、对 `V` 加权汇总和因果掩码说明。图注：“依据 Vaswani 等，Figure 2 与第 3.2.3 节改绘。”
6. `llm-rnn-comparison.png`：原理对比图。依据同一论文第 4 节与 Table 1。左侧展示 RNN 隐藏状态依次依赖，右侧展示自注意力层在训练阶段并行处理各输入位置；明确“自回归生成仍逐步产生下一个 token”。

`llm-token-generation.png` 已按正文术语重绘；主文和面试副文现在共用 `llm-principle.png` 解释自注意力机制。
