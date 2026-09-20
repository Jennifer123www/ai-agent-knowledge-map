import { createHash, timingSafeEqual } from "node:crypto";

export function createWechatSignature(token, timestamp, nonce) {
  return createHash("sha1")
    .update([token, timestamp, nonce].sort().join(""), "utf8")
    .digest("hex");
}

export function verifyWechatSignature({ token, timestamp, nonce, signature }) {
  if (![token, timestamp, nonce, signature].every(Boolean)) {
    return false;
  }

  const expected = Buffer.from(createWechatSignature(token, timestamp, nonce));
  const received = Buffer.from(String(signature));
  return expected.length === received.length && timingSafeEqual(expected, received);
}
