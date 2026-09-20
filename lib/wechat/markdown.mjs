import path from "node:path";

const imagePattern = /^!\[([^\]]*)\]\(([^)]+)\)\s*$/;

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

function inlineMarkdown(value) {
  let html = escapeHtml(value.trim());
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/`([^`]+)`/g, '<code style="padding:2px 5px;background:#f3f5f4;border-radius:3px;color:#176b45;">$1</code>');
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_match, label, url) => {
    return `<a href="${escapeHtml(safeUrl(url))}" style="color:#16865b;text-decoration:underline;">${label}</a>`;
  });
  return html;
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
  const titleLine = originalLines.find((line) => /^#\s+/.test(line));
  if (!titleLine) throw new Error(`No H1 title found in ${markdownPath}`);

  const lines = stripDocumentMetadata(originalLines).filter((line) => line !== titleLine);
  const images = [];
  for (const line of lines) {
    const match = line.match(imagePattern);
    if (!match) continue;
    const source = match[2].trim();
    if (/^https?:\/\//i.test(source)) continue;
    images.push({
      alt: match[1].trim(),
      source,
      absolutePath: path.resolve(path.dirname(markdownPath), source),
    });
  }

  if (images.length === 0) {
    throw new Error(`At least one local image is required for the WeChat cover: ${markdownPath}`);
  }

  const firstParagraph = lines.find((line) => {
    const value = line.trim();
    return value && !value.startsWith("#") && !value.startsWith("|") && !imagePattern.test(value);
  });
  const digest = (firstParagraph || titleLine.replace(/^#\s+/, ""))
    .replace(/\*\*|`|\[|\]|\([^)]*\)/g, "")
    .slice(0, 120);

  return {
    title: titleLine.replace(/^#\s+/, "").trim(),
    digest,
    lines,
    images,
    cover: images[0],
  };
}

export function renderWechatHtml(article, uploadedImageUrls) {
  const output = [];
  let paragraph = [];
  let listType = null;
  let listItems = [];
  let skippedCover = false;

  function flushParagraph() {
    if (paragraph.length === 0) return;
    output.push(
      `<p style="margin:16px 0;line-height:1.85;font-size:16px;color:#25312c;">${inlineMarkdown(paragraph.join(" "))}</p>`,
    );
    paragraph = [];
  }

  function flushList() {
    if (!listType || listItems.length === 0) return;
    const items = listItems.map((item) => `<li style="margin:8px 0;">${inlineMarkdown(item)}</li>`).join("");
    output.push(`<${listType} style="margin:16px 0;padding-left:24px;line-height:1.75;font-size:16px;color:#25312c;">${items}</${listType}>`);
    listType = null;
    listItems = [];
  }

  for (const rawLine of article.lines) {
    const line = rawLine.trim();
    const image = line.match(imagePattern);
    if (image) {
      flushParagraph();
      flushList();
      if (!skippedCover && image[2].trim() === article.cover.source) {
        skippedCover = true;
        continue;
      }
      const url = uploadedImageUrls.get(image[2].trim());
      if (!url) throw new Error(`No uploaded URL for image ${image[2]}`);
      output.push(
        `<p style="margin:24px 0;text-align:center;"><img src="${escapeHtml(url)}" alt="${escapeHtml(image[1])}" style="display:block;width:100%;max-width:100%;height:auto;" /></p>`,
      );
      continue;
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
      output.push(`<h2 style="margin:32px 0 14px;padding-left:10px;border-left:4px solid #16865b;font-size:22px;line-height:1.45;color:#16211c;">${inlineMarkdown(line.replace(/^##\s+/, ""))}</h2>`);
    } else if (/^###\s+/.test(line)) {
      flushParagraph();
      output.push(`<h3 style="margin:24px 0 12px;font-size:18px;line-height:1.5;color:#176b45;">${inlineMarkdown(line.replace(/^###\s+/, ""))}</h3>`);
    } else if (/^>\s+/.test(line)) {
      flushParagraph();
      output.push(`<blockquote style="margin:18px 0;padding:12px 16px;border-left:3px solid #8fb9a7;background:#f4f8f6;color:#46564f;line-height:1.75;">${inlineMarkdown(line.replace(/^>\s+/, ""))}</blockquote>`);
    } else if (!/^\|.*\|$/.test(line) && !/^\s*---+\s*$/.test(line)) {
      paragraph.push(line);
    }
  }

  flushParagraph();
  flushList();
  return `<section style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;letter-spacing:0;">${output.join("")}</section>`;
}
