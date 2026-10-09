# 多模态模型子模块配图记录

版本：0.8.0；修订时间：2026-10-09 16:50 CST；依据提交：`0441f30`（`main`；本轮修改前工作区干净，当前有未提交改动）。阶段：主文首段加入教学票据场景图；主副文正文图按新文章结构重组。

主文用一张教学构造的票据照片建立共同场景，再用机制、裁图、提问区域和证据定位图解释“怎样读图、怎样答对”。副文沿用同一案例，但图片用于架构比较、故障诊断、坐标计算与评测设计。正文图都是 1536×1024 横版 PNG；按约 330—345px 的手机宽度检查文字、箭头和数值。两篇封面各自独立，正文不插封面图。用暖白、低饱和青绿、橙色与梅红；不放左侧通高竖条或图底免责句。

## 生成式底图与确定性文字

1. `multimodal-cover-main-art-v2.png`：内置图像生成工具绘制无字水彩底图。提示词要点：暖白纸面；左侧留题字空间，右侧从一张票据照片过渡到局部放大、视觉块和字段草稿；表现图片线索进入回答，不堆屏幕、机器人和勾号；低饱和青绿、暖橙、灰梅色；不生成中文、Logo、水印或边框。`scripts/compose-multimodal-covers.mjs` 叠加准确文字，输出 `multimodal-cover-main-wechat-v2.png`（900×383）：标题“多模态模型”，副标题“它怎样从图片里读出答案”。底部 15% 为微信标题遮罩安全区。封面不复述正文第一张照片。
2. `multimodal-cover-interview-wechat.png`：副文 900×383 封面，中央保留票据、金额栏与放大镜；“认字”“归栏”两个短标签构成一眼可认的对照。完整标题留给微信卡片；按中央方形缩略图复核。由 `scripts/compose-multimodal-covers.mjs` 从原有无字底图生成。
3. `multimodal-scene-base.png`：内置图像生成工具绘制无字摄影底图。提示词要点：俯视一张放在浅木桌上的简洁酒店发票教学道具；纸面平整，右上角有局部反光，其余区域仍可读；三行字段留足空间；不要真实发票代码、税务章、二维码、店名、姓名、Logo、水印、文字或数字。`scripts/compose-multimodal-scene.mjs` 确定性叠加“酒店住宿发票”“开票日期 9/3”“含税金额 680.00”“税额 38.49”，输出 `multimodal-scene-invoice.png`。这不是真实发票或模型截图；图注说明教学性质。照片上不出现年份。

## 正文机制图

除既有 `multimodal-principle.png` 外，下面的新图由 `scripts/render-multimodal-figures.mjs` 确定性绘制。票据数字是贯穿文章的教学案例，不是论文实测数据。

| 文件 | 文章 | 图要回答的问题 |
| --- | --- | --- |
| `multimodal-principle.png` | 主文 | 原始 LLaVA 中图像如何经视觉编码器、可训练投影层接入语言模型，文字问题从何处进入。依据 [LLaVA 原论文第 4.1 节与 Figure 1](https://arxiv.org/html/2304.08485#S4.SS1)。 |
| `multimodal-crop-contrast.png` | 主文 | 整页缩图留住布局、带标签局部图留住小字；裁块和位置信息对照 [UReader 第 3.1—3.2 节](https://arxiv.org/html/2310.05126)。 |
| `multimodal-query-region.png` | 主文 | 同一照片问日期与问金额应看不同区域；箭头是任务需要的证据路径，并非实测注意力。 |
| `multimodal-grounding-v2.png` | 主文 | 草稿字段如何回到票面上的标签与数字，不能只框孤立数值。 |
| `multimodal-visual-budget.png` | 副文 | 原图过曝与输入缩小是不同信息损失；固定块大小下，宽高各翻倍对应图块约四倍，不等于实际费用固定四倍。 |
| `multimodal-architecture-contrast.png` | 副文 | LLaVA 的投影、Flamingo 的重采样与层间交叉注意力、Donut 的文档编码—文本解码之别。依据 [LLaVA](https://arxiv.org/abs/2304.08485)、[Flamingo](https://arxiv.org/abs/2204.14198)、[Donut](https://arxiv.org/abs/2111.15664) 原论文。 |
| `multimodal-ocr-vlm-contrast.png` | 副文 | OCR+版面规则与 VLM/文档模型各交出什么中间结果，不预设谁更准确。 |
| `multimodal-diagnosis-experiment.png` | 副文 | 固定其他条件，分别只改图像清晰度、只补标签位置，判断错字与错栏来自哪一层。 |
| `multimodal-coordinate-map.png` | 副文 | 无旋转、无透视时，局部框怎样按裁切起点和缩放比例映回原图。 |
| `multimodal-evaluation-grid.png` | 副文 | 照片清晰度与整页/局部输入交叉成测试条件；不填虚构分数。 |

复核顺序：确认每图的具体任务；检查数字、字段名、箭头、公式和论文架构；检查主副图没有近似重复；按手机宽度逐张看；最后运行文章校验与双图文 dry-run。
