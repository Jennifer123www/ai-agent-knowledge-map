# 微信公众号 API 接入与草稿生成

## 文档元数据

| 项目 | 值 |
| --- | --- |
| 版本 | `0.6.0` |
| 阶段 | 正式公众号文章完成后同步草稿；公网回调仍待部署 |
| Git 状态 | 基于 `de4fc4c`（`main`；修改前工作区干净） |
| 修改时间 | `2026-10-09 17:54 CST` |

## 1. 已实现链路

```text
微信公众号平台
  ├─ GET /api/wechat/callback  -> 验签并原样返回 echostr
  ├─ POST /api/wechat/callback -> 验签并返回 success
  └─ 微信 API
       ├─ stable_token         -> 获取并缓存 access_token
       ├─ material/add_material -> 上传永久封面素材
       ├─ media/uploadimg      -> 上传正文图片
       ├─ draft/add            -> 创建草稿
       ├─ draft/batchget、get  -> 查找并复核已有草稿
       └─ draft/update         -> 按篇原位更新草稿；不发布、不群发
```

当前回调使用明文模式完成首次接入。安全模式需要增加消息体 XML 解析和 AES 解密后再启用，不能只在后台切换配置。

## 2. 本地配置

复制 `.env.example` 为 `.env`，填写以下值：

```dotenv
WECHAT_APP_ID=公众号AppID
WECHAT_APP_SECRET=公众号AppSecret
WECHAT_TOKEN=与公众号服务器配置一致的随机字符串
WECHAT_CALLBACK_MODE=plain
WECHAT_AUTHOR=三色堇絮絮念
WECHAT_CONTENT_SOURCE_URL=
PORT=3000
```

`.env` 已加入 `.gitignore`。不要把 `AppSecret`、访问令牌或真实 `EncodingAESKey` 写进仓库、日志、浏览器前端代码或文章内容。

## 3. 本地校验

```sh
npm test
npm run wechat:draft -- --dry-run --theme orange --file content/wechat/01-foundation-models-and-inference/submodules/01-llm/beginner-main.md --side-file content/wechat/01-foundation-models-and-inference/submodules/01-llm/interview-side.md
npm run wechat:serve
```

本地回调地址是 `http://127.0.0.1:3000/wechat/callback`。微信公众号后台必须填写公网可访问的 HTTPS 地址，不能使用本机地址。

拿到凭证后验证微信 API：

```sh
npm run wechat:check
```

若返回错误码 `40164`，需把运行草稿脚本或服务端的公网出口 IP 加入微信公众号 API IP 白名单。

## 4. 部署

仓库包含 Vercel 风格的零依赖 Serverless Function：

- 健康检查：`/api/health`
- 微信回调：`/api/wechat/callback`

部署后在托管平台配置 `WECHAT_TOKEN`。公众号后台的服务器 URL 填写：

```text
https://<部署域名>/api/wechat/callback
```

公众号后台的 Token 必须与服务端 `WECHAT_TOKEN` 完全一致，加解密方式选择“明文模式”。验证成功后再启用服务器配置。

`WECHAT_APP_ID` 和 `WECHAT_APP_SECRET` 只用于服务端调用微信 API。若只部署回调，可暂时不在托管平台设置这两个值；创建草稿时运行脚本的环境必须设置。

## 5. 生成公众号双图文草稿

文章使用 UTF-8 Markdown 作为唯一内容源。内容精修后经 API 创建草稿，不再导出 Word 终稿或从 Word 导入公众号。文件开头使用 YAML Front Matter 描述草稿字段：

```yaml
---
title: "不超过 32 个字符的标题"
author: "不超过 16 个字符的作者"
digest: "不超过 120 个字符的摘要"
cover: "./assets/local-cover.png"
content_source_url: ""
article_type: "news"
need_open_comment: 0
only_fans_can_comment: 0
order: 1
---
```

导入前会强制校验：标题、作者和摘要长度；HTML 少于 20000 个字符且小于 1 MB；正文不含 JavaScript；封面和正文图片均为本地 JPG/PNG；文章包含“参考资料”小节和至少一个 HTTP(S) 文档链接。正文图片在创建草稿时先调用微信图片上传接口，HTML 只使用微信返回的 URL。若 `content_source_url` 为空，脚本会采用文末 `[阅读原文](...)` 的地址；两处都填写时必须一致。

当前脚本不带参数时会把 `content/wechat/05-tools-skills-and-protocols/beginner-main.md` 作为单篇、橙色主题草稿导入，只用于兼容旧命令和单篇烟测。正式主副文交付仍应显式指定两篇路径；`--theme orange` 可省略，若需要兼容旧稿可显式传入 `--theme green`。

该主题包含 1 组总概览和 6 组子模块，共 14 篇 Markdown。子模块文章位于 `content/wechat/05-tools-skills-and-protocols/submodules/<child>/`，其主副文路径以 `series.json` 为准。

项目复盘系列位于 `content/wechat/11-project-retrospective/`，在 `series.json` 标记为 `independent`，包含“我是如何引导 AI 生成一份 AI Agent 知识图谱的”主文和一篇非面试形式的踩坑指南。两篇仍作为一组接受校验和双图文 dry-run；独立专题可超过 5000 个中文字符，但不能超过公众号 HTML 限额。

基础模型系列位于 `content/wechat/01-foundation-models-and-inference/`，包含 1 组总概览和大语言模型、多模态模型、向量嵌入、重排序、模型适配 5 组子模块，共 12 篇 Markdown 与 30 张本地配图。各组文章路径、题目边界、提纲和配图以该目录的 `series.json` 为准。

同组主文和副文默认写入**同一份双图文草稿**：`--file` 的主文排第一篇，`--side-file` 的副文排第二篇，两篇各用自己的封面。`series.json` 登记的正式文章 Markdown 创建或修改并通过检查后，同组只执行一次双图文 dry-run 和一次草稿同步；只改其中一篇也更新整组，不等待单独的“导入草稿”指令。仅改规则、提示词或网站文件不触发。命令示例：

```sh
npm run wechat:draft -- --dry-run --theme orange --file content/wechat/01-foundation-models-and-inference/submodules/01-llm/beginner-main.md --side-file content/wechat/01-foundation-models-and-inference/submodules/01-llm/interview-side.md
npm run wechat:draft -- --upsert --theme orange --file content/wechat/01-foundation-models-and-inference/submodules/01-llm/beginner-main.md --side-file content/wechat/01-foundation-models-and-inference/submodules/01-llm/interview-side.md
```

裸命令调用 `draft/add`，会新建一份双图文草稿；正式文章交付流程不得用它制造重复草稿，应加 `--upsert`：脚本扫描草稿箱，按两篇**完整标题和顺序**精确匹配。恰好匹配一份时，通过 `draft/update` 分别更新主、副文，沿用原 `media_id`；没有匹配时调用 `draft/add` 新建；匹配多份或草稿结构异常时停止，不猜测目标。更新前后均用 `draft/get` 核对标题和内容开头。两篇更新是逐篇请求，若第二篇失败，草稿可能只更新了第一篇，需按报错中的 `media_id` 检查后重试。脚本不调用发布或群发接口。单篇排查可只传 `--file`，不作为同组正式交付的默认形式。

若两篇标题在本轮修改中变更，普通 `--upsert` 会因新旧标题不同而新建草稿。应先只读列出草稿、核对旧标题顺序、作者、来源链接和正文开头，确认唯一目标后，使用 `--replace-media-id <已核实的 media_id>`，并按主副文顺序各传一次 `--expect-current-title <旧标题>`；脚本会在上传前和更新前再次核对目标身份，也会检查是否已有另一份新标题草稿。核对不符即停止，不按相似标题猜测。

```sh
npm run wechat:draft -- --upsert --theme orange --file content/wechat/01-foundation-models-and-inference/submodules/02-multimodal/beginner-main.md --side-file content/wechat/01-foundation-models-and-inference/submodules/02-multimodal/interview-side.md
```

排版以 [项目规范 5.3.7 节](./project-specification.md) 为准：两篇共用白／暖白底、深色正文和橙色强调；主文连续讲解，面试副文便于逐题扫读，独立专题的非面试副文按内容设小标题；代码块、行内代码、加粗、居中灰色图注和参考链接必须保留。封面处理遵循 [项目规范 5.3.4 节](./project-specification.md)。公众号可能清理部分 HTML 样式或正文外链，创建后必须在后台和手机端核对，尤其检查“阅读原文”是否指向 `content_source_url`。

复盘文章示例：

```sh
npm run wechat:draft -- --dry-run --theme orange --file content/wechat/11-project-retrospective/beginner-main.md --side-file content/wechat/11-project-retrospective/interview-side.md
```

基础模型系列示例：

```sh
npm run wechat:draft -- --dry-run --theme orange --file content/wechat/01-foundation-models-and-inference/beginner-main.md --side-file content/wechat/01-foundation-models-and-inference/interview-side.md
```

微信正文图片按 1 MB 上限预检。本机 macOS 运行时，超限 PNG 会通过系统自带的 `sips` 临时压缩为 JPEG 后上传；临时文件在命令结束时删除，源图片不会改动。其他系统需要预先把正文图片压缩到 1 MB 以下。

可独立检查仓库内全部公众号文章：

```sh
npm run wechat:articles:check
```

## 6. 上线检查

主副文的内容、图片、格式、自动校验和后台预览统一按 [微信公众号双图文草稿推送检查规范](./wechat-draft-push-checklist.md) 执行。下面项目是接入层的补充检查，不能代替文章验收。

1. `https://<部署域名>/api/health` 返回 `ok: true`。
2. 微信公众号后台能成功保存服务器配置。
3. `npm run wechat:check` 能取得稳定版 `access_token`。
4. 双图文 dry-run 确认两篇顺序、封面和 HTML 限额，实际调用返回一份草稿的 `media_id`。
5. 在公众号后台核对主文大图、副文缩略图、手机正文、配图与图注、代码块、参考资料和“阅读原文”。
6. 不调用发布或群发接口；发布前继续由人工审阅草稿。
