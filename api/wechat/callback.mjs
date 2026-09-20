import { getWechatConfig } from "../../lib/wechat/config.mjs";
import { handleWechatCallback } from "../../lib/wechat/callback.mjs";

export default function handler(request, response) {
  let config;
  try {
    config = getWechatConfig();
  } catch (error) {
    response.status(500).send(error.message);
    return;
  }

  const result = handleWechatCallback({
    method: request.method,
    requestUrl: request.url,
    token: config.token,
  });
  for (const [name, value] of Object.entries(result.headers)) {
    response.setHeader(name, value);
  }
  response.status(result.status).send(result.body);
}
