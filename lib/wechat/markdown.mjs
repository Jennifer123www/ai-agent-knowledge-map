import path from "node:path";

const imagePattern = /^!\[([^\]]*)\]\(([^)]+)\)\s*$/;
const WECHAT_TITLE_LIMIT = 32;
const WECHAT_AUTHOR_LIMIT = 16;
const WECHAT_DIGEST_LIMIT = 120;
const WECHAT_CONTENT_CHARACTER_LIMIT = 20_000;
const WECHAT_CONTENT_BYTE_LIMIT = 1024 * 1024;
const THEMES = {
  green: {
    ink: "#25312c",
    heading: "#16211c",
    accent: "#16865b",
    accentDark: "#176b45",
    codeBackground: "#f3f5f4",
    captionText: "#6b7b73",
    quoteBorder: "#8fb9a7",
    quoteBackground: "#f4f8f6",
    quoteText: "#46564f",
  },
  orange: {
    ink: "#20252B",
    heading: "#20252B",
    accent: "#E87522",
    accentDark: "#C85D12",
    codeBackground: "#FFF3E6",
    captionText: "#888888",
    quoteBorder: "#F2C6A0",
    quoteBackground: "#FFF9F2",
    quoteText: "#595959",
  },
};

function characterLength(value) {
  return [...value].length;
}

function parseFrontMatterScalar(rawValue) {
  const value = rawValue.trim();
  if (!value) return "";
  if (value.startsWith('"') && value.endsWith('"')) return JSON.parse(value);
  if (value.startsWith("'") && value.endsWith("'")) {
    return value.slice(1, -1).replaceAll("''", "'");
  }
  if (value === "true") return true;
  if (value === "false") return false;
  if (value === "null") return null;
  if (/^-?\d+(?:\.\d+)?$/.test(value)) return Number(value);
  return value;
}

function extractFrontMatter(lines, markdownPath) {
  if (lines[0]?.trim() !== "---") return { metadata: {}, lines, present: false };
  const closingIndex = lines.findIndex((line, index) => index > 0 && line.trim() === "---");
  if (closingIndex < 0) throw new Error(`Unclosed YAML front matter in ${markdownPath}`);

  const metadata = {};
  for (const line of lines.slice(1, closingIndex)) {
    if (!line.trim() || line.trimStart().startsWith("#")) continue;
    const match = line.match(/^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$/);
    if (!match) throw new Error(`Unsupported YAML front matter line in ${markdownPath}: ${line}`);
    metadata[match[1]] = parseFrontMatterScalar(match[2]);
  }
  return { metadata, lines: lines.slice(closingIndex + 1), present: true };
}

function assertTextLimit(label, value, limit, markdownPath) {
  const length = characterLength(value);
  if (length > limit) {
    throw new Error(`${label} exceeds WeChat limit (${length}/${limit} characters): ${markdownPath}`);
  }
}

function binaryFlag(value, fallback, label, markdownPath) {
  const result = value ?? fallback;
  if (result !== 0 && result !== 1) {
    throw new Error(`${label} must be 0 or 1 in ${markdownPath}`);
  }
  return result;
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function safeUrl(rawUrl) {
  const url = rawUrl.trim();
  return /^(https?:\/\/|#)/i.test(url) ? url : "#";
}

function inlineMarkdown(value, theme) {
  let html = escapeHtml(value.trim());
  const codeSnippets = [];
  html = html.replace(/`([^`]+)`/g, (_match, code) => {
    const marker = `\uE000${codeSnippets.length}\uE001`;
    codeSnippets.push(`<code style="padding:2px 5px;background:${theme.codeBackground};border-radius:3px;color:${theme.accentDark};">${code}</code>`);
    return marker;
  });
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_match, label, url) => {
    return `<a href="${escapeHtml(safeUrl(url))}" style="color:${theme.accent};text-decoration:underline;">${label}</a>`;
  });
  return html.replace(/\uE000(\d+)\uE001/g, (_match, index) => codeSnippets[Number(index)]);
}

function stripDocumentMetadata(lines) {
  const output = [];
  let skipping = false;
  for (const line of lines) {
    if (line.trim() === "## 文档元数据") {
      skipping = true;
      continue;
    }
    if (skipping) {
      const value = line.trim();
      if (!value || /^\|.*\|$/.test(value)) continue;
      skipping = false;
    }
    if (!skipping) output.push(line);
  }
  return output;
}

export function parseWechatArticle(markdown, markdownPath) {
  const originalLines = markdown.replaceAll("\r\n", "\n").split("\n");
  const frontMatter = extractFrontMatter(originalLines, markdownPath);
  if (frontMatter.present) {
    for (const field of ["title", "author", "digest", "cover"]) {
      if (!String(frontMatter.metadata[field] ?? "").trim()) {
        throw new Error(`Missing required YAML front matter field '${field}' in ${markdownPath}`);
      }
    }
  }
  const titleLine = frontMatter.lines.find((line) => /^#\s+/.test(line));
  const headingTitle = titleLine?.replace(/^#\s+/, "").trim() || "";
  const title = String(frontMatter.metadata.title || headingTitle).trim();
  if (!title) throw new Error(`No title found in YAML front matter or H1 in ${markdownPath}`);
  if (frontMatter.metadata.title && headingTitle && title !== headingTitle) {
    throw new Error(`YAML title and H1 title must match in ${markdownPath}`);
  }

  const lines = stripDocumentMetadata(frontMatter.lines).filter((line) => line !== titleLine);
  const bodyImages = [];
  let imageScanFence = null;
  for (const line of lines) {
    const trimmed = line.trim();
    if (imageScanFence) {
      const closingFence = trimmed.match(/^(`{3,}|~{3,})\s*$/);
      if (closingFence && closingFence[1][0] === imageScanFence[0] && closingFence[1].length >= imageScanFence.length) {
        imageScanFence = null;
      }
      continue;
    }
    const openingFence = trimmed.match(/^(`{3,}|~{3,})(?:\s*[A-Za-z0-9_-]+)?\s*$/);
    if (openingFence) {
      imageScanFence = openingFence[1];
      continue;
    }
    const match = line.match(imagePattern);
    if (!match) continue;
    const source = match[2].trim();
    if (/^(?:https?:\/\/|data:)/i.test(source)) {
      throw new Error(`WeChat article images must be local so they can be uploaded first: ${source}`);
    }
    bodyImages.push({
      alt: match[1].trim(),
      source,
      absolutePath: path.resolve(path.dirname(markdownPath), source),
    });
  }

  const coverSource = String(frontMatter.metadata.cover || bodyImages[0]?.source || "").trim();
  if (!coverSource) {
    throw new Error(`At least one local image is required for the WeChat cover: ${markdownPath}`);
  }
  if (/^(?:https?:\/\/|data:)/i.test(coverSource)) {
    throw new Error(`WeChat cover must be a local image: ${coverSource}`);
  }
  const cover = bodyImages.find((image) => image.source === coverSource) || {
    alt: title,
    source: coverSource,
    absolutePath: path.resolve(path.dirname(markdownPath), coverSource),
  };
  const images = [cover, ...bodyImages.filter((image) => image.source !== cover.source)];

  const firstParagraph = lines.find((line) => {
    const value = line.trim();
    return value && !value.startsWith("#") && !value.startsWith("|") && !imagePattern.test(value);
  });
  const generatedDigest = (firstParagraph || title)
    .replace(/\*\*|`|\[|\]|\([^)]*\)/g, "");
  const digest = String(frontMatter.metadata.digest || generatedDigest).trim();
  const author = String(frontMatter.metadata.author || "").trim();
  const configuredSourceUrl = String(frontMatter.metadata.content_source_url || "").trim();
  const footerSourceUrls = [...lines.join("\n").matchAll(/\[阅读原文\]\((https?:\/\/[^\s)]+)\)/g)]
    .map((match) => match[1]);
  if (new Set(footerSourceUrls).size > 1) {
    throw new Error(`Conflicting 阅读原文 links in ${markdownPath}`);
  }
  const footerSourceUrl = footerSourceUrls[0] || "";
  if (configuredSourceUrl && footerSourceUrl && configuredSourceUrl !== footerSourceUrl) {
    throw new Error(`content_source_url and 阅读原文 link must match in ${markdownPath}`);
  }
  const contentSourceUrl = configuredSourceUrl || footerSourceUrl;
  const articleType = String(frontMatter.metadata.article_type || "news").trim();

  assertTextLimit("Title", title, WECHAT_TITLE_LIMIT, markdownPath);
  assertTextLimit("Author", author, WECHAT_AUTHOR_LIMIT, markdownPath);
  assertTextLimit("Digest", digest, WECHAT_DIGEST_LIMIT, markdownPath);
  if (articleType !== "news") {
    throw new Error(`Markdown articles currently support article_type=news only: ${markdownPath}`);
  }
  if (contentSourceUrl && !/^https?:\/\//i.test(contentSourceUrl)) {
    throw new Error(`content_source_url must be empty or an HTTP(S) URL: ${markdownPath}`);
  }

  return {
    title,
    author,
    digest,
    contentSourceUrl,
    articleType,
    needOpenComment: binaryFlag(frontMatter.metadata.need_open_comment, 0, "need_open_comment", markdownPath),
    onlyFansCanComment: binaryFlag(frontMatter.metadata.only_fans_can_comment, 0, "only_fans_can_comment", markdownPath),
    order: Number(frontMatter.metadata.order || 0),
    metadata: frontMatter.metadata,
    lines,
    images,
    cover,
  };
}

export function validateWechatHtml(html) {
  const characters = characterLength(html);
  const bytes = Buffer.byteLength(html, "utf8");
  if (characters >= WECHAT_CONTENT_CHARACTER_LIMIT) {
    throw new Error(`WeChat HTML content must be under 20,000 characters (${characters})`);
  }
  if (bytes >= WECHAT_CONTENT_BYTE_LIMIT) {
    throw new Error(`WeChat HTML content must be under 1 MB (${bytes} bytes)`);
  }
  if (/<script\b|\son\w+\s*=|javascript:/i.test(html)) {
    throw new Error("WeChat HTML content must not contain JavaScript");
  }
  return { characters, bytes };
}

export function renderWechatHtml(article, uploadedImageUrls, { theme = "green" } = {}) {
  const palette = THEMES[theme];
  if (!palette) throw new Error(`Unsupported WeChat theme: ${theme}`);
  const output = [];
  let paragraph = [];
  let listType = null;
  let listItems = [];
  let skippedCover = false;
  let awaitingImageCaption = false;
  let codeFence = null;
  let codeLines = [];

  function flushParagraph() {
    if (paragraph.length === 0) return;
    output.push(
      `<p style="margin:16px 0;">${inlineMarkdown(paragraph.join(" "), palette)}</p>`,
    );
    paragraph = [];
  }

  function flushList() {
    if (!listType || listItems.length === 0) return;
    const items = listItems.map((item) => `<li style="margin:8px 0;">${inlineMarkdown(item, palette)}</li>`).join("");
    output.push(`<${listType} style="margin:16px 0;padding-left:24px;line-height:1.75;font-size:16px;color:${palette.ink};">${items}</${listType}>`);
    listType = null;
    listItems = [];
  }

  function flushCodeBlock() {
    const lines = codeLines.map((codeLine) => {
      const code = escapeHtml(codeLine.replaceAll("\t", "    ")).replaceAll(" ", "&nbsp;") || "&nbsp;";
      return `<p style="margin:0;line-height:1.55;font-family:Menlo,Consolas,monospace;font-size:13px;color:${palette.ink};">${code}</p>`;
    });
    output.push(`<section style="margin:18px 0;padding:12px 14px;border-left:3px solid ${palette.accent};background:${palette.codeBackground};">${lines.join("")}</section>`);
    codeLines = [];
  }

  for (const rawLine of article.lines) {
    const line = rawLine.trim();
    if (codeFence) {
      const closingFence = line.match(/^(`{3,}|~{3,})\s*$/);
      if (closingFence && closingFence[1][0] === codeFence[0] && closingFence[1].length >= codeFence.length) {
        flushCodeBlock();
        codeFence = null;
      } else {
        codeLines.push(rawLine);
      }
      continue;
    }

    const openingFence = line.match(/^(`{3,}|~{3,})(?:\s*[A-Za-z0-9_-]+)?\s*$/);
    if (openingFence) {
      flushParagraph();
      flushList();
      awaitingImageCaption = false;
      codeFence = openingFence[1];
      continue;
    }

    const image = line.match(imagePattern);
    if (image) {
      flushParagraph();
      flushList();
      if (!skippedCover && image[2].trim() === article.cover.source) {
        skippedCover = true;
        awaitingImageCaption = false;
        continue;
      }
      const url = uploadedImageUrls.get(image[2].trim());
      if (!url) throw new Error(`No uploaded URL for image ${image[2]}`);
      output.push(
        `<p style="margin:24px 0;text-align:center;"><img src="${escapeHtml(url)}" alt="${escapeHtml(image[1])}" style="display:block;width:100%;max-width:100%;height:auto;" /></p>`,
      );
      awaitingImageCaption = true;
      continue;
    }

    if (awaitingImageCaption && line) {
      const caption = line.match(/^\*([^*]+)\*$/);
      awaitingImageCaption = false;
      if (caption) {
        output.push(`<p style="margin:4px 0 18px;text-align:center;font-size:13px;line-height:1.6;color:${palette.captionText};">${inlineMarkdown(caption[1], palette)}</p>`);
        continue;
      }
    }

    const ordered = line.match(/^\d+\.\s+(.+)/);
    const unordered = line.match(/^[-*]\s+(.+)/);
    if (ordered || unordered) {
      flushParagraph();
      const nextType = ordered ? "ol" : "ul";
      if (listType && listType !== nextType) flushList();
      listType = nextType;
      listItems.push((ordered || unordered)[1]);
      continue;
    }

    flushList();
    if (!line) {
      flushParagraph();
    } else if (/^##\s+/.test(line)) {
      flushParagraph();
      output.push(`<h2 style="margin:32px 0 14px;padding-left:10px;border-left:4px solid ${palette.accent};font-size:22px;line-height:1.45;color:${palette.heading};">${inlineMarkdown(line.replace(/^##\s+/, ""), palette)}</h2>`);
    } else if (/^###\s+/.test(line)) {
      flushParagraph();
      output.push(`<h3 style="margin:24px 0 12px;font-size:18px;line-height:1.5;color:${palette.accentDark};">${inlineMarkdown(line.replace(/^###\s+/, ""), palette)}</h3>`);
    } else if (/^>\s+/.test(line)) {
      flushParagraph();
      output.push(`<blockquote style="margin:18px 0;padding:12px 16px;border-left:3px solid ${palette.quoteBorder};background:${palette.quoteBackground};color:${palette.quoteText};line-height:1.75;">${inlineMarkdown(line.replace(/^>\s+/, ""), palette)}</blockquote>`);
    } else if (!/^\|.*\|$/.test(line) && !/^\s*---+\s*$/.test(line)) {
      paragraph.push(line);
    }
  }

  if (codeFence) throw new Error(`Unclosed Markdown code fence: ${codeFence}`);
  flushParagraph();
  flushList();
  const html = `<section style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;letter-spacing:0;line-height:1.85;font-size:16px;color:${palette.ink};">${output.join("")}</section>`;
  validateWechatHtml(html);
  return html;
}
