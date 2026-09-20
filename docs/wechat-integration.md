# 微信公众号 API 接入与草稿生成

## 文档元数据

| 项目 | 值 |
| --- | --- |
| 版本 | `0.1.0` |
| 阶段 | 服务端回调与草稿 API 实现完成，待部署并绑定公众号凭证 |
| Git 基线 | `0cc5805`（`main`；开始修改前工作区 clean） |
| 修改时间 | `2026-09-20 13:03 CST` |

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

默认将以下文章转换为公众号 HTML，上传本地配图并写入草稿箱：

```text
content/wechat/tools-skills-and-protocols/beginner-main.md
```

执行：

```sh
npm run wechat:draft
```

脚本只调用草稿接口 `draft/add`，不会调用发布接口。成功后输出草稿 `media_id`。也可指定另一篇文章：

```sh
npm run wechat:draft -- --file content/wechat/tools-skills-and-protocols/interview-side.md
```

微信正文图片按 1 MB 上限预检。本机 macOS 运行时，超限 PNG 会通过系统自带的 `sips` 临时压缩为 JPEG 后上传；临时文件在命令结束时删除，源图片不会改动。其他系统需要预先把正文图片压缩到 1 MB 以下。

## 6. 上线检查

1. `https://<部署域名>/api/health` 返回 `ok: true`。
2. 微信公众号后台能成功保存服务器配置。
3. `npm run wechat:check` 能取得稳定版 `access_token`。
4. `npm run wechat:draft` 返回 `media_id`，且草稿箱出现一篇文章。
5. 不调用发布或群发接口；发布前继续由人工审阅草稿。
