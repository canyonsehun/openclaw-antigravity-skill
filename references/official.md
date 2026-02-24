# Official sources

Use these sources when behavior needs official confirmation:

- Getting started: https://docs.openclaw.ai/start/getting-started
- Latest release: https://github.com/openclaw/openclaw/releases/latest
- Release v2026.2.22: https://github.com/openclaw/openclaw/releases/tag/v2026.2.22
- Release v2026.2.21: https://github.com/openclaw/openclaw/releases/tag/v2026.2.21

## Feature highlights (new features only)

### v2026.2.22 (2026-02-23)

- Provider/Mistral: 新增 Mistral 供应商支持，包括内存嵌入和语音支持。
- Update/Core: 新增可选的内置自动更新功能（默认关闭）。
- CLI/Update: 新增 `openclaw update --dry-run` 以预览更新操作而不实际执行。
- Channels/Synology Chat: 新增原生 Synology Chat 频道插件支持。
- Memory/FTS: 新增西班牙语、葡萄牙语、日语、韩语和阿拉伯语的停用词过滤和查询扩展，提升搜索召回率。
- Gateway/Auth: 统一了凭据来源优先级处理，重构了 WebSocket 握手路径以支持显式的 `auth.deviceToken`。

### v2026.2.21 (2026-02-21)

- Models/Google: 新增 Gemini 3.1 系列支持（如 `google/gemini-3.1-pro-preview`）。
- Providers: 新增火山引擎（豆包）和 BytePlus 供应方及模型支持。
- Channels: Telegram/Discord 新增流式回复预览、生命周期状态 emoji 反馈（排队/思考/执行中等）。
- Discord: 新增 `/vc` 语音频道管理、论坛标签管理、线程绑定子代代理（Thread-bound subagents）。
- iOS: 优化聊天 UI 噪音、增强 Watch 快速回复、稳定后台连接。
- Security: 强化 exec allowlist 检查（防止 heredoc/shell 注入）、增强浏览器文件访问限制、加固多项认证安全。

### v2026.2.19 (2026-02-19)

- Apple Watch companion MVP (watch inbox + watch command surfaces).
- iOS/Gateway APNs wake + auto-reconnect improvements for disconnected iOS nodes.
- Paired-device hygiene flows (`openclaw devices remove`, `openclaw devices clear --yes [--pending]`).
- APNs registration/signing options (`apns.bundle_id`, `apns.team_id`, `apns.key_id`).
- APNs push-test pipeline in gateway flows.

### v2026.2.17 (2026-02-18)

- Anthropic models can use 1M context in supported flows.
- `/subagents spawn` chat command support.
- iOS share-extension support.

## Notes captured for this skill

- Install path is Node.js + npm global install (`npm i -g openclaw`).
- First-run flow uses `openclaw setup` / `openclaw doctor` style workflows.
- `openclaw channels` command family manages Telegram account creation and status checks.
- `openclaw agents` command family manages isolated agents and routing-related state.
- Configuration file remains `~/.openclaw/openclaw.json`.

Re-check these links when CLI output differs from expected behavior.
