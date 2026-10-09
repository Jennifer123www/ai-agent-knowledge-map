export function assertReplacementDraft(draft, { titles, authors, contentSourceUrls }) {
  const articles = draft?.news_item;
  if (!Array.isArray(articles) || articles.length !== titles.length) {
    throw new Error("Target draft article count changed; refusing to overwrite it");
  }
  for (let index = 0; index < articles.length; index += 1) {
    const article = articles[index];
    if (article.title !== titles[index] || article.author !== authors[index] ||
        (contentSourceUrls[index] && article.content_source_url !== contentSourceUrls[index])) {
      throw new Error(`Target draft article ${index + 1} identity changed; refusing to overwrite it`);
    }
  }
}
