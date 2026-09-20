import { getWechatConfig } from "../lib/wechat/config.mjs";
import { createWechatClient, WechatApiError } from "../lib/wechat/client.mjs";

try {
  const config = getWechatConfig({ requireCredentials: true });
  const client = createWechatClient(config);
  await client.getAccessToken();
  console.log(`WeChat API credentials are valid for AppID ${config.appId}.`);
} catch (error) {
  if (error instanceof WechatApiError && error.code === 40164) {
    console.error(`${error.message}\nAdd this server's public egress IP to the WeChat API IP allowlist.`);
  } else {
    console.error(error.message);
  }
  process.exitCode = 1;
}
