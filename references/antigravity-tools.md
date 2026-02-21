# Antigravity Tools integration reference (for OpenClaw)

Use this reference when OpenClaw bots rely on Antigravity Tools as a reverse proxy.

## Official sources

- Main docs: https://opencodedocs.com/lbjlaq/Antigravity-Manager/
- Proxy setup and first client: https://opencodedocs.com/zh/lbjlaq/Antigravity-Manager/start/proxy-and-first-client/
- Config deep dive: https://opencodedocs.com/lbjlaq/Antigravity-Manager/advanced/config/
- Security: https://opencodedocs.com/zh/lbjlaq/Antigravity-Manager/advanced/security/
- 429 rotation FAQ: https://opencodedocs.com/zh/lbjlaq/Antigravity-Manager/faq/429-rotation/
- Endpoints appendix: https://opencodedocs.com/lbjlaq/Antigravity-Manager/appendix/endpoints/
- Image support (Imagen mapping): https://opencodedocs.com/lbjlaq/Antigravity-Manager/platforms/imagen/
- GitHub repo: https://github.com/lbjlaq/Antigravity-Manager

## Scheduling and account behavior

- Default scheduling mode is `Balance`.
- `Balance` keeps session stickiness and a short reuse window, then rotates when limits/errors occur.
- `PerformanceFirst` is for high concurrency/stateless workloads and rotates more aggressively.
- `CacheFirst` favors conversation continuity and cache reuse.
- Model id is still chosen by client request; account can rotate automatically according to scheduler rules.

## What to tell users about "same account for 3 messages?"

- In default `Balance`, consecutive messages in one active chat usually hit the same account until a limit/error/cooldown triggers rotation.
- It is not guaranteed to stay on one account forever.
- Check monitor `Account` column or response headers (for example `X-Account-Email`) for actual routing.

## Image model support and limits

- Antigravity supports image generation flows.
- Two common ways:
  1. `POST /v1/images/generations` with `model: gemini-3-pro-image`
  2. `POST /v1/chat/completions` with image-capable model and optional `size`
- Do not guarantee availability from docs alone. Live capacity/verification gates can still fail at runtime.

## Frequent upstream failures (and meaning)

- `429` with `MODEL_CAPACITY_EXHAUSTED`: all candidate accounts had no capacity for that model.
- `403` with `VALIDATION_REQUIRED`: account must complete upstream verification.
- `warmup` monitor traffic: relay internal warmup calls, not user prompt calls.

## LAN exposure and auth guidance

- `allow_lan_access=false`: localhost only (`127.0.0.1`).
- `allow_lan_access=true`: listen on `0.0.0.0` for LAN clients.
- Use auth mode with API keys for any LAN exposure (`auto`/`strict` per policy).
- Never expose an unauthenticated LAN relay.

## OpenClaw integration checklist

1. Relay responds on `/v1/models` and includes required model IDs.
2. `~/.openclaw/openclaw.json` and each agent `models.json` contain same `antigravity` provider model catalog.
3. Telegram account -> binding -> agent mapping is explicit and unique.
4. Gateway restart done after config update.
5. Smoke test each bot and confirm provider/model in runtime metadata.
6. If image model fails, report exact upstream error and next action instead of masking the failure.


## Community troubleshooting notes (non-official)

Use this section only when users report matching errors and explicitly label it as community guidance (not OpenClaw official docs).

- HTTP 400 (`Bad Request`, `Precondition check failed`)
  - Possible auth/session drift between local CLI credentials and upstream Google endpoints.
  - Common community actions: refresh Google/Gemini CLI auth, clear stale auth files, re-login.
  - If still failing, check whether upstream project/API is restricted and avoid aggressive retries.

- HTTP 403 (`Terms of Service violation`, `VALIDATION_REQUIRED`)
  - Indicates upstream account is blocked or requires verification.
  - Common community action: open provided Google verification link and complete required checks (for example phone verification), then retry.

- `Invalid project resource name projects/`
  - Usually means project id is empty/malformed in upstream-related config.
  - Re-check project id fields and environment variables, then retry.

- Safety note
  - If user suspects risk controls triggered, prefer cooldown and controlled retries instead of continuous high-frequency retries.
