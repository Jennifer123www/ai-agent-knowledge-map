import assert from "node:assert/strict";
import test from "node:test";
import path from "node:path";
import { handleWechatCallback } from "../lib/wechat/callback.mjs";
import { createWechatClient } from "../lib/wechat/client.mjs";
import { createWechatSignature } from "../lib/wechat/signature.mjs";
import { parseWechatArticle, renderWechatHtml } from "../lib/wechat/markdown.mjs";

test("creates the official WeChat SHA-1 callback signature", () => {
  assert.equal(
    createWechatSignature("token", "1711111111", "nonce"),
    createWechatSignature("nonce", "token", "1711111111"),
  );
});

test("returns echostr for a valid callback verification request", () => {
  const token = "test-token";
  const timestamp = "1711111111";
  const nonce = "abc123";
  const signature = createWechatSignature(token, timestamp, nonce);
  const result = handleWechatCallback({
    method: "GET",
    requestUrl: `/wechat/callback?timestamp=${timestamp}&nonce=${nonce}&signature=${signature}&echostr=connected`,
    token,
  });
  assert.deepEqual(result, {
    status: 200,
    headers: {
      "content-type": "text/plain; charset=utf-8",
      "cache-control": "no-store",
    },
    body: "connected",
  });
});

test("rejects an invalid callback signature", () => {
  const result = handleWechatCallback({
    method: "GET",
    requestUrl: "/wechat/callback?timestamp=1&nonce=2&signature=bad&echostr=nope",
    token: "test-token",
  });
  assert.equal(result.status, 403);
});

test("gets a stable token once and creates an unpublished draft", async () => {
  const requests = [];
  const fetchImpl = async (url, options) => {
    requests.push({ url, options });
    if (url.endsWith("/cgi-bin/stable_token")) {
      return new Response(JSON.stringify({ access_token: "token-value", expires_in: 7200 }));
    }
    if (url.includes("/cgi-bin/draft/add")) {
      return new Response(JSON.stringify({ media_id: "draft-media-id" }));
    }
    throw new Error(`Unexpected request: ${url}`);
  };
  const client = createWechatClient({
    appId: "test-app-for-draft",
    appSecret: "test-secret",
    fetchImpl,
  });

  assert.equal(await client.getAccessToken(), "token-value");
  const result = await client.addDraft({ title: "Demo", content: "<p>Demo</p>" });

  assert.equal(result.media_id, "draft-media-id");
  assert.equal(requests.length, 2);
  assert.match(requests[1].url, /\/cgi-bin\/draft\/add\?access_token=token-value$/);
  assert.deepEqual(JSON.parse(requests[1].options.body), {
    articles: [{ title: "Demo", content: "<p>Demo</p>" }],
  });
});

test("parses and renders a WeChat article", () => {
  const markdownPath = path.resolve("content/wechat/example/article.md");
  const markdown = `# Demo title

## 文档元数据

| 项目 | 值 |
| --- | --- |
| 版本 | 1 |

![cover](./cover.png)

First **paragraph**.

## Section

1. First item
2. Second item

![diagram](./diagram.png)
`;
  const article = parseWechatArticle(markdown, markdownPath);
  const html = renderWechatHtml(article, new Map([["./diagram.png", "https://example.com/diagram.png"]]));

  assert.equal(article.title, "Demo title");
  assert.equal(article.images.length, 2);
  assert.doesNotMatch(html, /文档元数据/);
  assert.match(html, /<strong>paragraph<\/strong>/);
  assert.match(html, /https:\/\/example\.com\/diagram\.png/);
  assert.doesNotMatch(html, /cover\.png/);
});
