import { readFile } from "node:fs/promises";
import path from "node:path";

const API_ROOT = "https://api.weixin.qq.com";
const tokenCache = new Map();

export class WechatApiError extends Error {
  constructor(message, response) {
    super(message);
    this.name = "WechatApiError";
    this.code = response?.errcode;
    this.response = response;
  }
}

function assertWechatResponse(data, operation) {
  if (data && Number(data.errcode || 0) !== 0) {
    const suffix = data.errmsg ? `: ${data.errmsg}` : "";
    throw new WechatApiError(
      `${operation} failed with WeChat error ${data.errcode}${suffix}`,
      data,
    );
  }
  return data;
}

async function parseJsonResponse(response, operation) {
  const text = await response.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error(`${operation} returned non-JSON HTTP ${response.status}: ${text.slice(0, 300)}`);
  }

  if (!response.ok) {
    throw new WechatApiError(`${operation} returned HTTP ${response.status}`, data);
  }
  return assertWechatResponse(data, operation);
}

function mimeType(filePath) {
  switch (path.extname(filePath).toLowerCase()) {
    case ".png":
      return "image/png";
    case ".gif":
      return "image/gif";
    case ".webp":
      return "image/webp";
    case ".jpg":
    case ".jpeg":
      return "image/jpeg";
    default:
      return "application/octet-stream";
  }
}

export function createWechatClient({ appId, appSecret, fetchImpl = fetch }) {
  if (!appId || !appSecret) {
    throw new Error("appId and appSecret are required");
  }

  async function getAccessToken({ forceRefresh = false } = {}) {
    const cached = tokenCache.get(appId);
    if (!forceRefresh && cached && cached.expiresAt > Date.now()) {
      return cached.value;
    }

    const response = await fetchImpl(`${API_ROOT}/cgi-bin/stable_token`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        grant_type: "client_credential",
        appid: appId,
        secret: appSecret,
        force_refresh: forceRefresh,
      }),
    });
    const data = await parseJsonResponse(response, "Get stable access token");
    if (!data.access_token) {
      throw new WechatApiError("WeChat did not return access_token", data);
    }

    const expiresInMs = Math.max(60, Number(data.expires_in || 7200)) * 1000;
    const safetyWindowMs = Math.min(5 * 60 * 1000, expiresInMs / 2);
    tokenCache.set(appId, {
      value: data.access_token,
      expiresAt: Date.now() + expiresInMs - safetyWindowMs,
    });
    return data.access_token;
  }

  async function uploadImage(filePath, { permanent = false } = {}) {
    const accessToken = await getAccessToken();
    const bytes = await readFile(filePath);
    const form = new FormData();
    form.append(
      "media",
      new Blob([bytes], { type: mimeType(filePath) }),
      path.basename(filePath),
    );

    const endpoint = permanent
      ? `/cgi-bin/material/add_material?access_token=${encodeURIComponent(accessToken)}&type=image`
      : `/cgi-bin/media/uploadimg?access_token=${encodeURIComponent(accessToken)}`;
    const operation = permanent ? "Upload permanent cover image" : "Upload article image";
    const response = await fetchImpl(`${API_ROOT}${endpoint}`, { method: "POST", body: form });
    const data = await parseJsonResponse(response, operation);

    if (permanent && !data.media_id) {
      throw new WechatApiError(`${operation} did not return media_id`, data);
    }
    if (!permanent && !data.url) {
      throw new WechatApiError(`${operation} did not return url`, data);
    }
    return data;
  }

  async function addDraft(articleOrArticles) {
    const articles = Array.isArray(articleOrArticles) ? articleOrArticles : [articleOrArticles];
    if (articles.length === 0) throw new Error("At least one article is required for a draft");
    const accessToken = await getAccessToken();
    const response = await fetchImpl(
      `${API_ROOT}/cgi-bin/draft/add?access_token=${encodeURIComponent(accessToken)}`,
      {
        method: "POST",
        headers: { "content-type": "application/json; charset=utf-8" },
        body: JSON.stringify({ articles }),
      },
    );
    const data = await parseJsonResponse(response, "Create draft");
    if (!data.media_id) {
      throw new WechatApiError("Create draft did not return media_id", data);
    }
    return data;
  }

  async function getDraft(mediaId) {
    if (!mediaId) throw new Error("mediaId is required to read a draft");
    const accessToken = await getAccessToken();
    const response = await fetchImpl(
      `${API_ROOT}/cgi-bin/draft/get?access_token=${encodeURIComponent(accessToken)}`,
      {
        method: "POST",
        headers: { "content-type": "application/json; charset=utf-8" },
        body: JSON.stringify({ media_id: mediaId }),
      },
    );
    return parseJsonResponse(response, "Read draft");
  }

  return { getAccessToken, uploadImage, addDraft, getDraft };
}
