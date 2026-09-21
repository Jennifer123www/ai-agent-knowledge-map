# 微信公众号 API 接入与草稿生成

## 文档元数据

| 项目 | 值 |
| --- | --- |
| 版本 | `0.4.0` |
| 阶段 | 草稿 API、文章校验与“工具、技能与协议”7 组分层推文已完成，待部署并绑定公众号凭证 |
| Git 状态 | `9bfc7e6`（`main`；更新时 dirty，含总概览重写和系列完整性校验） |
| 修改时间 | `2026-09-21 00:41 CST` |

## 1. 已实现链路

```text
微信公众号平台
  ├─ GET /api/wechat/callback  -> 验签并原样返回 echostr
  ├─ POST /api/wechat/callback -> 验签并返回 success
  └─ 微信 API
       ├─ stable_token         -> 获取并缓存 access_token
       ├─ material/add_material -> 上传永久封面素材
       ├─ media/uploadimg      -> 上传正文图片
       └─ draft/add            -> 创建草稿，不发布、不群发
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

导入前会强制校验：标题、作者和摘要长度；HTML 少于 20000 个字符且小于 1 MB；正文不含 JavaScript；封面和正文图片均为本地 JPG/PNG；文章包含“参考资料”小节和至少一个 HTTP(S) 文档链接。正文图片在创建草稿时先调用微信图片上传接口，HTML 只使用微信返回的 URL。

默认将以下文章转换为公众号 HTML，上传本地配图并写入草稿箱：

```text
content/wechat/tools-skills-and-protocols/beginner-main.md
```

该主题当前包含 1 组总概览和 6 组子模块，共 14 篇 Markdown。子模块文章位于 `content/wechat/tools-skills-and-protocols/submodules/<child>/`，同样通过 `--file` 指定导入。

项目复盘系列位于 `content/wechat/project-retrospective/`，包含“我是如何引导 AI 生成一份 AI Agent 知识图谱的”主文和一篇独立踩坑指南。两篇同样登记在 `series.json` 并接受完整校验。

执行：

```sh
npm run wechat:draft
```

脚本只调用草稿接口 `draft/add`，不会调用发布接口。成功后输出草稿 `media_id`。也可指定另一篇文章：

```sh
npm run wechat:draft -- --file content/wechat/tools-skills-and-protocols/interview-side.md
```

复盘文章示例：

```sh
npm run wechat:draft -- --file content/wechat/project-retrospective/beginner-main.md
npm run wechat:draft -- --file content/wechat/project-retrospective/interview-side.md
```

微信正文图片按 1 MB 上限预检。本机 macOS 运行时，超限 PNG 会通过系统自带的 `sips` 临时压缩为 JPEG 后上传；临时文件在命令结束时删除，源图片不会改动。其他系统需要预先把正文图片压缩到 1 MB 以下。

可独立检查仓库内全部公众号文章：

```sh
npm run wechat:articles:check
```

## 6. 上线检查

1. `https://<部署域名>/api/health` 返回 `ok: true`。
2. 微信公众号后台能成功保存服务器配置。
3. `npm run wechat:check` 能取得稳定版 `access_token`。
4. `npm run wechat:draft` 返回 `media_id`，且草稿箱出现一篇文章。
5. 不调用发布或群发接口；发布前继续由人工审阅草稿。
