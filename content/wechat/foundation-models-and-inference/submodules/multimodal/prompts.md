# 多模态模型子模块配图提示词

统一规格：`gpt-image-2`，1536x1024 PNG，暖白背景，青绿、梅红、蓝色点缀，图像、声音、文字采用不同图标，中文清晰，无水印、无 Logo。

1. `multimodal-cover.png`：封面，发票、图表、语音波形和文字汇入模型，标题“多模态模型”，副标题“让 Agent 不只会读字”。
2. `multimodal-encoding.png`：输入编码流程，标签“图像”“音频”“文字”“特征表示”。
3. `multimodal-alignment.png`：视觉特征通过桥接层进入语言模型，标签“视觉编码器”“连接层”“语言模型”“回答”。
4. `multimodal-document.png`：一页复杂单据被拆成“版面”“表格”“小字”“印章”四类观察对象。
5. `multimodal-validation.png`：识别结果进入复核链，标签“模型提取”“格式校验”“业务规则”“人工复核”。
6. `multimodal-principle.png`：原理图。依据 [Visual Instruction Tuning / LLaVA](https://arxiv.org/abs/2304.08485) 第 3 节改绘。保留“图像 → 视觉编码器 → 投影层 → 语言模型”，文字指令另一路进入语言模型；省略训练目标与完整参数细节。图注：“依据 Liu 等，LLaVA 第 3 节改绘。”
