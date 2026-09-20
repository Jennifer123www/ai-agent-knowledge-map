# AI Agent Knowledge Map

A Chinese AI Agent knowledge project with a static learning site and a separate WeChat Official Account publishing integration. The site presents one shared topic system through a beginner guide and an interview guide; the server-side tools verify WeChat callbacks and turn repository Markdown into unpublished drafts.

## Structure

```text
site/
  index.html                 # Editorial home page
  learn/
    index.html               # Beginner overview
    concepts.html            # Concept diagrams and "大话" explanations
  interview/
    index.html               # Interview topic map
    questions.html           # Interview question drill-down
  assets/js/
    site-search.js           # Shared cross-site search
scripts/
  check-site.mjs             # Link and syntax validation
  check-wechat-config.mjs    # Validate AppID/AppSecret with stable_token
  create-wechat-draft.mjs    # Upload article assets and create a draft
api/
  wechat/callback.mjs        # Serverless callback endpoint
lib/wechat/                  # Signature, API client, and Markdown conversion
server/wechat-server.mjs     # Local/standalone callback server
test/wechat.test.mjs         # Callback and article conversion tests
```

The `site/` directory is the publish root for GitHub Pages, Netlify, Vercel, or any ordinary static-file host. The paths use stable English lowercase URLs, while the pages and learning material remain in Chinese.

## Local Preview

```sh
npm run serve
```

Open [http://127.0.0.1:4173/](http://127.0.0.1:4173/).

## Validation

```sh
npm run check
npm test
```

The check confirms expected pages, local HTML links, inline script syntax, the shared search script, and every WeChat article's official field, HTML-size, and local-image constraints.

## WeChat Draft Integration

The integration has no third-party runtime dependencies and requires Node.js 20 or newer. Configure a local `.env` from `.env.example`, then run:

```sh
npm run wechat:check
npm run wechat:articles:check
npm run wechat:draft -- --dry-run
npm run wechat:draft
```

The last command creates a draft only. It does not publish or mass-send it. See `docs/wechat-integration.md` for callback and deployment details.

## Project Metadata

- Version: `0.3.2`
- Stage: WeChat callback, draft API, YAML Front Matter, article-limit and reference-link checks implemented; public deployment and account binding pending
- Git status during this update: dirty; based on `main` at `e5afada`
- Updated: `2026-09-20 17:31 CST`
