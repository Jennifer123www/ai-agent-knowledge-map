import { createServer } from "node:http";
import { getWechatConfig } from "../lib/wechat/config.mjs";
import { handleWechatCallback } from "../lib/wechat/callback.mjs";

const config = getWechatConfig();
const port = Number(process.env.PORT || 3000);

const server = createServer((request, response) => {
  if (request.url === "/health") {
    response.writeHead(200, { "content-type": "application/json; charset=utf-8" });
    response.end(JSON.stringify({ ok: true, service: "wechat-official-account" }));
    return;
  }

  const pathname = new URL(request.url || "/", "http://localhost").pathname;
  if (pathname !== "/wechat/callback" && pathname !== "/api/wechat/callback") {
    response.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    response.end("not found");
    return;
  }

  const result = handleWechatCallback({
    method: request.method,
    requestUrl: request.url,
    token: config.token,
  });
  response.writeHead(result.status, result.headers);
  response.end(result.body);
});

server.listen(port, () => {
  console.log(`WeChat callback server listening on http://127.0.0.1:${port}`);
});
