# 微信公众号 API 接入与草稿生成

## 文档元数据

| 项目 | 值 |
| --- | --- |
| 版本 | `0.5.2` |
| 阶段 | 支持三套双图文排版样稿和草稿回读；公网回调仍待部署 |
| Git 状态 | 基于 `14cbaab`（`main`；本文及排版实现待提交，另有用户的 Word 临时锁文件未跟踪） |
| 修改时间 | `2026-09-29 19:22 CST` |

## 1. 已实现链路

```text
微信公众号平台
  ├─ GET /api/wechat/callback  -> 验签并原样返回 echostr
  ├─ POST /api/wechat/callback -> 验签并返回 success
  └─ 微信 API
       ├─ stable_token         -> 获取并缓存 access_token
       ├─ material/add_material -> 上传永久封面素材
       ├─ media/uploadimg      -> 上传正文图片
       ├─ draft/add            -> 创建草稿，不发布、不群发
       └─ draft/get            -> 回读草稿，核对文章顺序与样式
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
npm run wechat:draft -- --dry-run
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

## 5. 创建 Demo 草稿

文章使用 UTF-8 Markdown 作为唯一内容源，文件开头使用 YAML Front Matter 描述草稿字段：

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

默认将以下文章转换为公众号 HTML，上传本地配图并写入草稿箱：

```text
content/wechat/tools-skills-and-protocols/beginner-main.md
```

该主题当前包含 1 组总概览和 6 组子模块，共 14 篇 Markdown。子模块文章位于 `content/wechat/tools-skills-and-protocols/submodules/<child>/`，同样通过 `--file` 指定导入。

项目复盘系列位于 `content/wechat/project-retrospective/`，包含“我是如何引导 AI 生成一份 AI Agent 知识图谱的”主文和一篇独立踩坑指南。两篇同样登记在 `series.json` 并接受完整校验。

基础模型系列位于 `content/wechat/foundation-models-and-inference/`，包含 1 组总概览和大语言模型、多模态模型、向量嵌入、重排序、模型适配 5 组子模块，共 12 篇 Markdown 与 30 张本地配图。各组文章路径、题目边界、提纲和配图以该目录的 `series.json` 为准。

执行：

```sh
npm run wechat:draft
```

脚本只调用草稿接口 `draft/add`，不会调用发布接口。成功后输出草稿 `media_id`。也可指定另一篇文章：

```sh
npm run wechat:draft -- --file content/wechat/tools-skills-and-protocols/interview-side.md
```

要把主文和面试副文放进同一份双图文草稿，先 dry-run，再创建；`--file` 的文章排在第一篇，`--side-file` 排在第二篇，两篇各用自己的封面：

```sh
npm run wechat:draft -- --dry-run --theme orange --file content/wechat/foundation-models-and-inference/submodules/llm/beginner-main.md --side-file content/wechat/foundation-models-and-inference/submodules/llm/interview-side.md
npm run wechat:draft -- --theme orange --file content/wechat/foundation-models-and-inference/submodules/llm/beginner-main.md --side-file content/wechat/foundation-models-and-inference/submodules/llm/interview-side.md
```

双图文仍只创建一份草稿、返回一个 `media_id`；脚本复用两篇文章共有的正文图片上传结果，原有单篇草稿不会被覆盖。

复盘文章示例：

```sh
npm run wechat:draft -- --file content/wechat/project-retrospective/beginner-main.md
npm run wechat:draft -- --file content/wechat/project-retrospective/interview-side.md
```

基础模型系列示例：

```sh
npm run wechat:draft -- --file content/wechat/foundation-models-and-inference/beginner-main.md
npm run wechat:draft -- --file content/wechat/foundation-models-and-inference/submodules/llm/interview-side.md
```

微信正文图片按 1 MB 上限预检。本机 macOS 运行时，超限 PNG 会通过系统自带的 `sips` 临时压缩为 JPEG 后上传；临时文件在命令结束时删除，源图片不会改动。其他系统需要预先把正文图片压缩到 1 MB 以下。

可独立检查仓库内全部公众号文章：

```sh
npm run wechat:articles:check
```

## 6. 排版主题对照样稿

`--sample-themes` 会用同一组主文和面试副文，一次创建三份双图文草稿。图片只上传一次，三份草稿分别带有 A/B/C 标题前缀和“排版样稿，请勿发布”摘要；原 Markdown 与既有草稿不变。创建后调用 `draft/get` 回读，核对文章顺序及关键样式是否保留。

| 样稿 | 本项目主题参数 | 参考方向 | 主要区别 |
| --- | --- | --- | --- |
| A 暖陶米白 | `warm-paper` | [MarkNice 的暖陶米白](https://github.com/willmove/marknice) | 暖纸底色、棕色标题、细分隔线 |
| B 简洁优雅 | `simple-elegant` | [doocs/md 的简洁／优雅主题](https://github.com/doocs/md/discussions/426) | 白底、墨绿标题、清晰的章节下划线 |
| C 技术蓝 | `tech-blue` | [Markdown Nice 的技术文章主题库](https://github.com/mdnice/markdown-nice) | 浅蓝标题块、蓝色代码与提示框 |

这是按三种排版方向制作的**独立样稿**，不是复制第三方模板的 HTML、CSS 或素材。三套样式使用公众号 API 可接受的内联样式，兼顾较长的面试副文；最终效果仍须在手机端预览。

```sh
npm run wechat:draft -- --dry-run --sample-themes --file content/wechat/foundation-models-and-inference/submodules/llm/beginner-main.md --side-file content/wechat/foundation-models-and-inference/submodules/llm/interview-side.md
npm run wechat:draft -- --sample-themes --file content/wechat/foundation-models-and-inference/submodules/llm/beginner-main.md --side-file content/wechat/foundation-models-and-inference/submodules/llm/interview-side.md
```

选定一种样式后，日常草稿仍只创建一份，例如 `--theme warm-paper`；原有 `green`、`orange` 主题继续可用。

## 7. 上线检查

1. `https://<部署域名>/api/health` 返回 `ok: true`。
2. 微信公众号后台能成功保存服务器配置。
3. `npm run wechat:check` 能取得稳定版 `access_token`。
4. `npm run wechat:draft` 返回 `media_id`，且草稿箱出现单篇或双图文草稿。
5. 不调用发布或群发接口；发布前继续由人工审阅草稿。
