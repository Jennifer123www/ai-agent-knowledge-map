import { verifyWechatSignature } from "./signature.mjs";

const textHeaders = {
  "content-type": "text/plain; charset=utf-8",
  "cache-control": "no-store",
};

export function handleWechatCallback({ method, requestUrl, token }) {
  const url = new URL(requestUrl, "http://localhost");
  const verified = verifyWechatSignature({
    token,
    timestamp: url.searchParams.get("timestamp"),
    nonce: url.searchParams.get("nonce"),
    signature: url.searchParams.get("signature"),
  });

  if (!verified) {
    return { status: 403, headers: textHeaders, body: "invalid signature" };
  }

  if (method === "GET") {
    const echo = url.searchParams.get("echostr");
    if (!echo) {
      return { status: 400, headers: textHeaders, body: "missing echostr" };
    }
    return { status: 200, headers: textHeaders, body: echo };
  }

  if (method === "POST") {
    return { status: 200, headers: textHeaders, body: "success" };
  }

  return {
    status: 405,
    headers: { ...textHeaders, allow: "GET, POST" },
    body: "method not allowed",
  };
}
