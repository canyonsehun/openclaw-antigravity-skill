# Official sources

Use these sources when behavior needs official confirmation:

- Getting started: https://docs.openclaw.ai/start/getting-started
- Latest release: https://github.com/openclaw/openclaw/releases/latest
- Release v2026.3.11: https://github.com/openclaw/openclaw/releases/tag/v2026.3.11
- Release v2026.2.26: https://github.com/openclaw/openclaw/releases/tag/v2026.2.26
- Release v2026.2.25: https://github.com/openclaw/openclaw/releases/tag/v2026.2.25
- Release v2026.2.19: https://github.com/openclaw/openclaw/releases/tag/v2026.2.19

## Feature highlights (new features only)

### v2026.3.11 (2026-03-12)

- **Security / Gateway**: Browser-originated WebSocket connections now enforce origin validation even in `trusted-proxy` mode. This matters for any exposed gateway.
- **Cron / doctor migration**: Isolated cron delivery is tightened and legacy cron storage now needs `openclaw doctor --fix` migration. This is a real operator-facing breaking change for existing `~/.openclaw/cron/jobs.json` installs.
- **ACP session resume**: `sessions_spawn` for `runtime: "acp"` now supports `resumeSessionId`, so ACP / ACPX / Codex child sessions can continue an existing conversation instead of always starting fresh.
- **Memory / Gemini embeddings**: `memorySearch` adds `gemini-embedding-2-preview` support, configurable output dimensions, automatic reindexing on dimension change, and opt-in multimodal image/audio indexing for `memorySearch.extraPaths`.
- **Ollama onboarding**: OpenClaw now has first-class Ollama onboarding with Local and Cloud + Local modes, cloud sign-in, curated model suggestions, and smarter local-pull behavior.

### v2026.2.26 (2026-02-27)

- **External Secrets Management**: Full `openclaw secrets` workflow (`audit`, `configure`, `apply`, `reload`) for managing secrets with runtime snapshot activation.
- **ACP/Thread-bound agents**: ACP agents are now first-class runtimes for thread sessions with full spawn/send integration.
- **Agents/Routing CLI**: New `openclaw agents bindings` commands for account-scoped route management and binding upgrades.
- **Android/Nodes**: Added Android device capabilities and notification listing (`nodes notifications_list`).

### v2026.2.25 (2026-02-26)

- **Android/Chat**: Improved streaming delivery and markdown rendering quality in the native Android UI.
- **Startup performance**: Optimized Android startup and added macrobenchmark tracking.
- **UI/Chat compose**: Added mobile stacked layout for compose actions on small screens.

### v2026.2.19 (2026-02-19)

- Apple Watch companion MVP (watch inbox + watch command surfaces).
- iOS/Gateway APNs wake + auto-reconnect improvements for disconnected iOS nodes.
- Paired-device hygiene flows (`openclaw devices remove`, `openclaw devices clear --yes [--pending]`).
- APNs registration/signing options (`apns.bundle_id`, `apns.team_id`, `apns.key_id`).
- APNs push-test pipeline in gateway flows.
