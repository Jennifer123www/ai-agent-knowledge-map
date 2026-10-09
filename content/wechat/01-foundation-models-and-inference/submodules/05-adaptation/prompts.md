# 模型适配子模块配图提示词

版本：0.4.1；修订时间：2026-10-09 21:41 CST；依据提交：`226782f`（`main`；修订前另有未提交的 1.4 配图工作）。

正文配图统一为 1536×1024 PNG；公众号封面图统一为 900×383 PNG。暖白背景，梅红、橙色和青绿色点缀，中文清晰，无水印、无 Logo。封面图使用内置图像生成工具；结构图 `adaptation-lora.png`、`adaptation-distillation.png`、`adaptation-diagnosis-matrix.png`、`adaptation-qlora-comparison.png` 与 `adaptation-version-bundle.png` 由 `scripts/render-foundation-figure-fixes.py` 确定性绘制。

1. `adaptation-cover-main-wechat-v3.png`：主文封面图。使用内置 imagegen 重新生成，以 1.1、1.2、1.3 主文封面作为**风格参考**：暖白纸张、轻水彩、细线连线、顶部居中宋体双行标题，横向教学场景铺满中部。标题逐字为“大话模型适配”“旧政策答错了要微调吗”；画面从“旧版 7 天”转到“现行 3 天”，中部答复仍写“7 天”，再分出“更新资料”“调整行为”两条处理路径。底部 15% 仅留可遮挡纸纹；不要左侧大标题、巨型放大镜、悬浮 3D 卡片、厚重阴影、口号、免责声明和水印。成片等比例整理为 900×383，核对标题、四处标签、数字、箭头、底部遮罩区。这张图只表示旧事实与固定行为应先分开诊断，不表示训练能自动更新政策。完整生成提示词见文末。
2. `adaptation-cover-interview-wechat-v2.png`：面试副文封面图。沿用 1.1—1.3 副文封面轻水彩纸张质感，中央正方形安全区以一枚放大镜并置两张纸：短标签“旧资料”与“漏提醒”，前者有时钟和叉号，后者有空复选框。没有文章全标题和周边小卡片；两处标签在约 128×128 居中裁切中仍须可辨。使用内置 imagegen 生成，再整理为 900×383；逐字检查标签、图标和中心裁切。
3. `adaptation-decision.png`：选择树，标签“缺最新知识”“缺稳定格式”“缺领域行为”“缺低成本部署”，分支对应“检索”“规则”“微调”“蒸馏”。
4. `adaptation-lora.png`：冻结基础权重 `W`，训练低秩参数 `BA`，组合计算后得到任务输出；另标独立题集评测，不能用一条无数据的上升曲线暗示适配后必然改善。
5. `adaptation-distillation.png`：沿本文退款政策案例，教师模型生成示例、人工抽检后训练学生模型；独立评测新版、旧版与缺条件问题。原图猫狗车样例与本文案例无关，已撤换。
6. `adaptation-release.png`：发布闭环，标签“数据版本”“训练实验”“离线评测”“灰度发布”“回滚”。
7. `adaptation-diagnosis-matrix.png`：故障诊断图。把“最新事实缺失、固定格式不稳、领域行为不稳、部署成本过高”分别映射到“RAG、模板或规则、SFT/LoRA、蒸馏”，强调先判断病因。
8. `adaptation-principle.png`：原理图。依据 [LoRA](https://arxiv.org/abs/2106.09685) 第 4 节与 Figure 1 改绘。保留冻结基础权重 `W`、可训练低秩矩阵 `A/B`、增量 `BA` 与输出相加；说明 QLoRA 还会量化冻结底座。图注：“依据 Hu 等，第 4 节与 Figure 1 改绘。”
9. `adaptation-qlora-comparison.png`：面试副文专用横版对照图。依据 [QLoRA 原论文](https://arxiv.org/abs/2305.14314) 的方法说明：左右对照 LoRA 与 QLoRA，共同保留可训练低秩增量；QLoRA 一侧明确标注冻结底座低比特存放、计算时反量化。不把框面积画成实测显存占比，也不声称性能必然更好。
10. `adaptation-version-bundle.png`：面试副文专用横版版本图。对照已验证组合“底座 v1＋分词器 v1＋适配器 a1＋提示 p1”和更换底座后的待验证组合；箭头表示版本变更导致兼容性与质量需要重新验收，不是已测结果。

复核：已目视检查新版主封面 900×383 原图、标题与标签、底部遮罩区；副文封面保持原版。正文不重复插入封面图。后台真实卡片及手机预览仍需确认。

### 本轮主文封面完整提示词

> Use case: infographic-diagram. Asset type: WeChat Official Account lead-story horizontal cover, about 2.35:1 aspect ratio. Generate a NEW image; the three input images are STYLE REFERENCES ONLY, not content or edit targets. Match their shared visual language closely: warm ivory handmade paper, restrained low-saturation watercolor illustration, fine hand-drawn connectors, delicate translucent color washes, crisp dark Chinese Song/Ming serif centered title across the top, explanatory subtitle centered just beneath, a single coherent horizontal teaching scene across the middle. The 1.1 and 1.2 references are especially important for typography scale and composition. Subject: the article's customer-service case about model adaptation. At left show an old refund-policy paper labeled '旧版 7 天' beside a newer paper labeled '现行 3 天'; at center show a small customer-service reply paper that wrongly cites 7 days and misses a required reminder; from it two delicate distinct arrows branch to '更新资料' (small current-policy document) and '调整行为' (small reply checklist). Make it visually understandable at a glance; use fewer objects than the previous cover. Text exact, verbatim, no other text: top line '大话模型适配'; second line '旧政策答错了要微调吗'; four small labels '旧版 7 天', '现行 3 天', '更新资料', '调整行为'. If exact small labels cannot be rendered confidently, favor clear symbols and omit those small labels rather than invent characters. Preserve adequate dark ink contrast. Main illustration occupies most of the canvas below the title; bottom 15% contains only unobtrusive paper texture because WeChat overlays the title there. No left-aligned title, giant magnifying glass, 3D floating cards, giant shadows, saturated color blocks, vertical left-side decorative bar, watermark, logo, extra slogans, or disclaimer strip. Output a polished, readable 2.35:1 cover image.
