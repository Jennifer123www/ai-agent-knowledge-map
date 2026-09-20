function value(name) {
  return process.env[name]?.trim() || "";
}

export function getWechatConfig({ requireCredentials = false } = {}) {
  const config = {
    appId: value("WECHAT_APP_ID"),
    appSecret: value("WECHAT_APP_SECRET"),
    token: value("WECHAT_TOKEN"),
    callbackMode: value("WECHAT_CALLBACK_MODE") || "plain",
    encodingAesKey: value("WECHAT_ENCODING_AES_KEY"),
    author: value("WECHAT_AUTHOR"),
    contentSourceUrl: value("WECHAT_CONTENT_SOURCE_URL"),
  };

  const missing = [];
  if (!config.token) missing.push("WECHAT_TOKEN");
  if (requireCredentials && !config.appId) missing.push("WECHAT_APP_ID");
  if (requireCredentials && !config.appSecret) missing.push("WECHAT_APP_SECRET");

  if (config.callbackMode !== "plain") {
    throw new Error(
      "WECHAT_CALLBACK_MODE currently supports only 'plain'. Complete plaintext verification before enabling secure mode.",
    );
  }

  if (missing.length > 0) {
    throw new Error(`Missing required environment variables: ${missing.join(", ")}`);
  }

  return config;
}
