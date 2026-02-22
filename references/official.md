# Official sources

Use these sources when behavior needs official confirmation:

- Getting started: https://docs.openclaw.ai/start/getting-started
- Latest release: https://github.com/openclaw/openclaw/releases/latest
- Release v2026.2.21: https://github.com/openclaw/openclaw/releases/tag/v2026.2.21
- Release v2026.2.19: https://github.com/openclaw/openclaw/releases/tag/v2026.2.19
- Release v2026.2.17: https://github.com/openclaw/openclaw/releases/tag/v2026.2.17

## Feature highlights (new features only)

### v2026.2.21 (2026-02-21)

- Google Gemini 3.1 model support (`google/gemini-3.1-pro-preview`).
- New providers/models: Volcano Engine (Doubao) + BytePlus, with interactive/non-interactive onboarding auth and `volcengine-api-key` doc alignment.
- Per-account/channel outbound routing fallback via `defaultTo` (lets `openclaw agent --deliver` send without explicit `--reply-to`).
- Per-channel model overrides via `channels.modelByChannel`, surfaced in `/status`.
- Telegram streaming config simplified to `channels.telegram.streaming` (boolean) with legacy auto-mapping.
- Discord streaming preview mode (partial/block + chunking controls).
- Discord/Telegram lifecycle status reactions for queued/thinking/tool/done/error with emoji/timing overrides.
- Discord voice channel join/leave/status via `/vc`, plus auto-join config.
- Discord forum tag updates via channel edit actions; thread-bound subagents with per-thread controls.
- /status and WebUI show model fallback lifecycle context; iOS UI cleanup and watch quick-reply bridging.

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
