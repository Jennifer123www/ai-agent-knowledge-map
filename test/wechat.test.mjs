import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import test from "node:test";
import path from "node:path";
import { handleWechatCallback } from "../lib/wechat/callback.mjs";
import { createWechatClient } from "../lib/wechat/client.mjs";
import { createWechatSignature } from "../lib/wechat/signature.mjs";
import { parseWechatArticle, renderWechatHtml, validateWechatHtml } from "../lib/wechat/markdown.mjs";

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

test("creates one draft with the main article followed by its side article", async () => {
  const requests = [];
  const fetchImpl = async (url, options) => {
    requests.push({ url, options });
    if (url.endsWith("/cgi-bin/stable_token")) {
      return new Response(JSON.stringify({ access_token: "token-value", expires_in: 7200 }));
    }
    if (url.includes("/cgi-bin/draft/add")) {
      return new Response(JSON.stringify({ media_id: "paired-draft-id" }));
    }
    throw new Error(`Unexpected request: ${url}`);
  };
  const client = createWechatClient({
    appId: "test-app-for-paired-draft",
    appSecret: "test-secret",
    fetchImpl,
  });
  const main = { title: "Main", content: "<p>Main</p>", thumb_media_id: "main-cover" };
  const side = { title: "Side", content: "<p>Side</p>", thumb_media_id: "side-cover" };

  const result = await client.addDraft([main, side]);
  assert.equal(result.media_id, "paired-draft-id");
  assert.deepEqual(JSON.parse(requests[1].options.body), { articles: [main, side] });
});

test("reads a saved WeChat draft for post-upload verification", async () => {
  const requests = [];
  const fetchImpl = async (url, options) => {
    requests.push({ url, options });
    if (url.endsWith("/cgi-bin/stable_token")) {
      return new Response(JSON.stringify({ access_token: "token-value", expires_in: 7200 }));
    }
    if (url.includes("/cgi-bin/draft/get")) {
      return new Response(JSON.stringify({ news_item: [{ title: "Saved sample" }] }));
    }
    throw new Error(`Unexpected request: ${url}`);
  };
  const client = createWechatClient({ appId: "test-app-for-readback", appSecret: "test-secret", fetchImpl });

  const draft = await client.getDraft("saved-media-id");
  assert.equal(draft.news_item[0].title, "Saved sample");
  assert.deepEqual(JSON.parse(requests[1].options.body), { media_id: "saved-media-id" });
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

test("renders an orange WeChat theme without changing the green default", () => {
  const markdownPath = path.resolve("content/wechat/example/article.md");
  const article = parseWechatArticle(`# Demo title

![cover](./cover.png)

Read **this** \`code\` and [source](https://example.com).

## Main heading

### Detail heading

> A useful note.

- One item
`, markdownPath);
  const images = new Map();
  const green = renderWechatHtml(article, images);
  const orange = renderWechatHtml(article, images, { theme: "orange" });

  assert.match(green, /border-left:4px solid #16865b/);
  assert.match(green, /color:#25312c/);
  assert.match(orange, /border-left:4px solid #E87522/);
  assert.match(orange, /color:#C85D12/);
  assert.match(orange, /background:#FFF3E6/);
  assert.match(orange, /background:#FFF9F2/);
  assert.match(orange, /color:#20252B/);
  assert.doesNotMatch(orange, /#16865b|#176b45/);
  assert.throws(() => renderWechatHtml(article, images, { theme: "purple" }), /Unsupported WeChat theme/);
});

test("renders three distinct comparison themes within the long interview article limit", async () => {
  const articlePath = path.resolve("content/wechat/foundation-models-and-inference/submodules/llm/interview-side.md");
  const article = parseWechatArticle(await readFile(articlePath, "utf8"), articlePath);
  const placeholderUrl = `https://mmbiz.qpic.cn/${"x".repeat(180)}`;
  const images = new Map(article.images.slice(1).map((image) => [image.source, placeholderUrl]));
  const themes = ["warm-paper", "simple-elegant", "tech-blue"];
  const html = themes.map((theme) => renderWechatHtml(article, images, { theme }));

  assert.match(html[0], /background:#FFFCF8/);
  assert.match(html[1], /border-bottom:2px solid #39735C/);
  assert.match(html[2], /background:#EAF3F9/);
  assert.equal(new Set(html).size, themes.length);
  for (const content of html) assert.ok(validateWechatHtml(content).characters < 20_000);
});

test("sample draft dry-run prepares three labeled main-and-side pairs", () => {
  const output = execFileSync(process.execPath, [
    "scripts/create-wechat-draft.mjs",
    "--dry-run",
    "--sample-themes",
    "--file", "content/wechat/foundation-models-and-inference/submodules/llm/beginner-main.md",
    "--side-file", "content/wechat/foundation-models-and-inference/submodules/llm/interview-side.md",
  ], { cwd: path.resolve("."), encoding: "utf8" });
  const result = JSON.parse(output);

  assert.equal(result.sampleCount, 3);
  assert.deepEqual(result.drafts.map((draft) => draft.theme), ["warm-paper", "simple-elegant", "tech-blue"]);
  for (const draft of result.drafts) {
    assert.equal(draft.articleCount, 2);
    assert.equal(draft.articles.length, 2);
    assert.match(draft.articles[0].title, /^【[ABC] /);
    assert.match(draft.articles[1].title, /^【[ABC] /);
    assert.ok(draft.articles.every((article) => article.titleCharacters <= 32));
  }
});

test("renders image captions and fenced code blocks as distinct elements", () => {
  const markdownPath = path.resolve("content/wechat/example/article.md");
  const markdown = [
    "# Demo title",
    "",
    "![cover](./cover.png)",
    "",
    "A paragraph with *emphasis* and `a*b`.",
    "",
    "![diagram](./diagram.png)",
    "",
    "*Caption with `token`.*",
    "",
    "```json",
    "{",
    '  "key": "<safe>"',
    "}",
    "```",
  ].join("\n");
  const article = parseWechatArticle(markdown, markdownPath);
  const html = renderWechatHtml(article, new Map([["./diagram.png", "https://mmbiz.qpic.cn/diagram.png"]]), { theme: "orange" });

  assert.match(html, /<em>emphasis<\/em>/);
  assert.match(html, /<code[^>]*>a\*b<\/code>/);
  assert.match(html, /text-align:center;font-size:13px;line-height:1\.6;color:#888888;">Caption with <code/);
  assert.match(html, /background:#FFF3E6;">/);
  assert.match(html, /<p[^>]*>\{<\/p><p[^>]*>&nbsp;&nbsp;&quot;key&quot;:&nbsp;&quot;&lt;safe&gt;&quot;<\/p>/);
  assert.doesNotMatch(html, /\*Caption|```json|<script/);
});

test("rejects an unclosed fenced code block", () => {
  const markdownPath = path.resolve("content/wechat/example/article.md");
  const article = parseWechatArticle([
    "# Demo title",
    "",
    "![cover](./cover.png)",
    "",
    "```json",
    "{}",
  ].join("\n"), markdownPath);
  assert.throws(() => renderWechatHtml(article, new Map()), /Unclosed Markdown code fence/);
});

test("does not upload image syntax shown inside a code block", () => {
  const markdownPath = path.resolve("content/wechat/example/article.md");
  const article = parseWechatArticle([
    "# Demo title",
    "",
    "![cover](./cover.png)",
    "",
    "```markdown",
    "![example](./not-a-real-image.png)",
    "```",
  ].join("\n"), markdownPath);
  assert.equal(article.images.length, 1);
  assert.match(renderWechatHtml(article, new Map()), /!\[example\]\(\.\/not-a-real-image\.png\)/);
});

test("uses YAML front matter for WeChat draft metadata", () => {
  const markdownPath = path.resolve("content/wechat/example/article.md");
  const markdown = `---
title: "Demo title"
author: "Demo author"
digest: "A short digest"
cover: "./cover.png"
content_source_url: "https://example.com/source"
article_type: "news"
need_open_comment: 1
only_fans_can_comment: 0
order: 2
---

# Demo title

![cover](./cover.png)

First paragraph.

![diagram](./diagram.png)
`;
  const article = parseWechatArticle(markdown, markdownPath);
  const html = renderWechatHtml(article, new Map([["./diagram.png", "https://mmbiz.qpic.cn/diagram.png"]]));

  assert.equal(article.title, "Demo title");
  assert.equal(article.author, "Demo author");
  assert.equal(article.digest, "A short digest");
  assert.equal(article.contentSourceUrl, "https://example.com/source");
  assert.equal(article.needOpenComment, 1);
  assert.equal(article.onlyFansCanComment, 0);
  assert.equal(article.order, 2);
  assert.equal(article.cover.source, "./cover.png");
  assert.doesNotMatch(html, /title:|digest:|content_source_url:/);
});

test("uses the 阅读原文 link when no source URL is configured", () => {
  const markdownPath = path.resolve("content/wechat/example/article.md");
  const markdown = [
    "# Demo title",
    "",
    "![cover](./cover.png)",
    "",
    "Read the article.",
    "",
    "[阅读原文](https://example.com/project)",
  ].join("\n");
  const article = parseWechatArticle(markdown, markdownPath);
  assert.equal(article.contentSourceUrl, "https://example.com/project");
});

test("rejects mismatched source URLs in metadata and the article footer", () => {
  const markdownPath = path.resolve("content/wechat/example/article.md");
  const markdown = [
    "---",
    'title: "Demo title"',
    'author: "Demo author"',
    'digest: "A short digest"',
    'cover: "./cover.png"',
    'content_source_url: "https://example.com/one"',
    "---",
    "",
    "# Demo title",
    "",
    "![cover](./cover.png)",
    "",
    "[阅读原文](https://example.com/two)",
  ].join("\n");
  assert.throws(() => parseWechatArticle(markdown, markdownPath), /content_source_url and 阅读原文 link must match/);
});

test("enforces WeChat article metadata and HTML limits", () => {
  const markdownPath = path.resolve("content/wechat/example/article.md");
  const longTitle = "标".repeat(33);
  assert.throws(
    () => parseWechatArticle(`---\ntitle: "${longTitle}"\nauthor: "Author"\ndigest: "Digest"\ncover: "./cover.png"\n---\n\n# ${longTitle}\n\n![cover](./cover.png)`, markdownPath),
    /Title exceeds WeChat limit/,
  );
  assert.throws(
    () => validateWechatHtml(`<section>${"文".repeat(20_000)}</section>`),
    /under 20,000 characters/,
  );
  assert.throws(
    () => validateWechatHtml('<section><script>alert("x")</script></section>'),
    /must not contain JavaScript/,
  );
});

test("requires local WeChat images before upload", () => {
  const markdownPath = path.resolve("content/wechat/example/article.md");
  assert.throws(
    () => parseWechatArticle(`---
title: "Demo"
author: "Author"
digest: "Digest"
cover: "./cover.png"
---

# Demo

![cover](./cover.png)

![remote](https://example.com/remote.png)
`, markdownPath),
    /images must be local/,
  );
});

test("requires core fields when YAML front matter is present", () => {
  const markdownPath = path.resolve("content/wechat/example/article.md");
  assert.throws(
    () => parseWechatArticle(`---
title: "Demo"
cover: "./cover.png"
---

# Demo

![cover](./cover.png)
`, markdownPath),
    /Missing required YAML front matter field 'author'/,
  );
});
