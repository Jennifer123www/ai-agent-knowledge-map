# 多模态模型子模块配图提示词

版本：0.2.0；修订时间：2026-09-28 17:26 CST；依据提交：`47c0ee0`（`main`，修订前 clean）。

统一规格：1536x1024 PNG，暖白背景，青绿、梅红、蓝色点缀，中文清晰，无水印、无 Logo。原有成片使用 `gpt-image-2`；本轮纠错图 `multimodal-encoding.png` 由 `scripts/render-foundation-figure-fixes.py` 确定性绘制。

1. `multimodal-cover.png`：封面，发票、图表、语音波形和文字汇入模型，标题“多模态模型”，副标题“让 Agent 不只会读字”。
2. `multimodal-encoding.png`：图片、声音、文字分别经视觉、音频、文本编码器得到各自特征，再按任务对齐或融合；具体模型可能只支持部分模态，不能暗示原始输入共用一个编码器。
3. `multimodal-alignment.png`：视觉特征通过桥接层进入语言模型，标签“视觉编码器”“连接层”“语言模型”“回答”。
4. `multimodal-document.png`：一页复杂单据被拆成“版面”“表格”“小字”“印章”四类观察对象。
5. `multimodal-validation.png`：识别结果进入复核链，标签“模型提取”“格式校验”“业务规则”“人工复核”。
6. `multimodal-principle.png`：原理图。依据 [Visual Instruction Tuning / LLaVA](https://arxiv.org/abs/2304.08485) 第 3 节改绘。保留“图像 → 视觉编码器 → 投影层 → 语言模型”，文字指令另一路进入语言模型；省略训练目标与完整参数细节。图注：“依据 Liu 等，LLaVA 第 3 节改绘。”

复核：已目视检查新图的中文、编码路径与箭头。
