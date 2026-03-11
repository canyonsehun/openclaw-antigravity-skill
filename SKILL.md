---
name: openclaw
description: Configure and operate OpenClaw — a self-hosted, multi-channel AI agent gateway. Use when installing OpenClaw, managing Gateway operations, setting up channels (WhatsApp, Telegram, Discord, Slack, iMessage, Signal, and 15+ others), creating or updating Telegram bot agents, configuring model providers (including relay), multi-agent routing, security hardening, binding account-to-agent routing, validating relay scheduling/account behavior, and troubleshooting model/channel issues (including warmup, image models, 403/429).
---

# OpenClaw

Use this skill to build and maintain a stable multi-bot OpenClaw setup, especially when users need relay models and predictable `/model` behavior.

## Read references only when needed

| Reference | When to read |
|---|---|
| `references/official.md` | Checking official OpenClaw setup/CLI behavior or release notes |
| `references/bot-onboarding.md` | Creating or modifying Telegram bots |
| `references/relay-models.md` | Changing relay models and `/model` visibility |
| `references/relay-tools.md` | Relay Tools behavior (account rotation, scheduling mode, LAN exposure, auth, warmup, image model support, 403/429 analysis) |
| `references/channels.md` | Per-channel setup: WhatsApp, Telegram, Discord, Slack, Signal, iMessage, plugins |
| `references/gateway_ops.md` | Gateway architecture, service management, remote access, install/update |
| `references/multi_agent.md` | Multi-agent routing, bindings, per-agent config |
| `references/providers.md` | Model provider setup (Anthropic, OpenAI, Ollama, 20+ providers) |
| `references/security.md` | Auth, access control, hardening baseline, secrets, incident response |

## Workflow decision

1. Perform install/bootstrap work when OpenClaw is missing or broken.
2. Perform release-check/update work when user asks for latest version, changelog, or auto-upgrade.
3. Perform bot onboarding when user provides bot name/username/token/default model.
4. Perform relay model sync when user asks to add/remove `/model relay` options.
5. Perform relay capability checks when user asks whether image models, auto account/model behavior, or LAN proxy mode work.
6. Perform verification/troubleshooting when user reports wrong model, no reply, 403/429, or routing confusion.
7. Perform execution-integrity checks when user reports "说了已完成但没做" or multi-step runs stop halfway.

## Install and bootstrap (OpenClaw v2026.2.19+ style)

1. Install Node.js 22+.
2. Install CLI: `npm i -g openclaw`.
3. Run setup/repair: `openclaw setup` or `openclaw doctor --repair`.
4. Start gateway: `openclaw gateway start` (or `openclaw gateway restart`).
5. Validate baseline:
   - `openclaw gateway status`
   - `openclaw channels status`
   - `openclaw agents list --json`

## GitHub Codespaces / github.dev remote deployment notes

Use this when the user follows the “no Mac/Linux, phone drives cloud dev” workflow.

1. Local access prerequisite for a Codespace:
   - `gh auth refresh -h github.com -s codespace`
   - `gh codespace view -c <name>`
   - `gh codespace ssh -c <name>`
2. Fresh remote bootstrap:
   - prefer `openclaw onboard --non-interactive --accept-risk ...`
   - `openclaw setup --non-interactive` is not sufficient on some fresh installs because onboarding now requires explicit risk acknowledgement
3. In ephemeral remote shells, prefer env-file driven startup:
   - write secrets to `~/.secrets/openclaw.env`
   - source it from `~/.bashrc`, `~/.zshrc`, and `~/.zprofile`
   - set `env.shellEnv.enabled = true` in `~/.openclaw/openclaw.json`
   - start gateway with:

```bash
nohup bash -lc '[ -f ~/.secrets/openclaw.env ] && source ~/.secrets/openclaw.env; exec openclaw gateway --port 18789' \
  > ~/.openclaw/logs/gateway.stdout.log \
  2> ~/.openclaw/logs/gateway.stderr.log < /dev/null &
```

4. For remote/Codespaces deployments, validate the upstream model endpoint from that host before blaming OpenClaw:
   - `curl -I <baseUrl>/responses`
   - or the provider-specific health endpoint actually used by the selected API mode
5. Important diagnostic pattern:
   - `openclaw gateway status` can be healthy
   - `memory-lancedb-pro` can register successfully
   - Jina embedding probe can return HTTP 200
   - but agent inference can still fail if the model upstream blocks the Codespaces egress IP
6. Cloudflare / WAF failure signature to recognize immediately:
   - `HTTP 403`
   - header like `cf-mitigated: challenge`
   - HTML body containing “Just a moment...” or a managed challenge page
   - This means the issue is upstream network policy, not OpenClaw routing/plugin startup
7. When channels are not configured yet, use a channel-free smoke test:
   - `openclaw agent --local --agent main --message "reply only: ok" --json`
   - if using gateway mode instead of `--local`, pass `--agent`, `--session-id`, or `--to`; otherwise the call fails before inference
8. Safety rule for cloud rehearsals:
   - do not attach the same Telegram / WhatsApp production credentials to both local and cloud gateways unless the migration is intentional
   - otherwise the two gateways can compete for the same bot/session and create confusing false negatives

## Claude Code fallback on remote hosts / Codespaces

Use this when remote OpenClaw is healthy but the configured coding provider still fails, and the user wants to reuse local Claude Code on the remote machine.

1. Important separation:
   - remote `Claude Code` working does **not** mean OpenClaw has already been switched to use Anthropic / Claude models
   - it only proves the remote host can successfully run `claude` with its own endpoint/auth
2. Practical diagnosis from real-world runs:
   - `codex` / custom OpenAI-compatible upstream can fail with Cloudflare `403` from a Codespaces egress IP
   - at the same time, `Claude Code` can still succeed against a separate Anthropic-compatible endpoint
   - therefore do not conclude “remote machine/network is broken” just because one provider is blocked
3. Local Claude Code auth shape to inspect first:
   - binary/version: `claude --version`
   - settings file: `~/.claude/settings.json`
   - common keys observed in the field:
     - `env.ANTHROPIC_BASE_URL`
     - `env.ANTHROPIC_AUTH_TOKEN`
     - `model`
4. Remote sync workflow that worked reliably:
   - install the same Claude Code version on the remote host
   - write the remote `~/.claude/settings.json` as valid JSON
   - also mirror the same auth vars into `~/.secrets/openclaw.env` so shell-launched tools can read them
   - source `~/.secrets/openclaw.env` from shell startup files as part of the normal remote bootstrap
5. Critical pitfall:
   - if `~/.claude/settings.json` is malformed JSON, Claude Code fails before any network test
   - fix the JSON first before debugging auth/base URL
6. Minimal remote smoke test:

```bash
claude -p --output-format json 'reply only: ok'
```

Pass criteria:
   - `"is_error": false`
   - `"result": "ok"`
   - `modelUsage` is populated
7. Operator takeaway:
   - if remote Claude Code smoke test passes while remote OpenClaw `codex` still fails, the next action is provider switching/reconfiguration, not gateway repair
   - if the user wants OpenClaw to actually use Claude on that remote machine, update OpenClaw model/provider config explicitly after the Claude Code smoke test succeeds

## Release check and auto-update workflow (v2026.2.19+)

Run this flow when the user asks for "latest version", "what changed", or requests automatic upgrades.

1. Read current version:
   - `openclaw --version`
2. Read latest official release (GitHub):
   - `gh release view -R openclaw/openclaw --json tagName,publishedAt,url,body`
3. If latest tag is newer than current, upgrade immediately:
   - `npm install -g openclaw@latest`
   - Verify with `openclaw --version`
4. Report in user-facing plain language:
   - Current vs latest version
   - Whether update was performed
   - New features only (exclude pure bug-fix/security-fix items unless user explicitly asks)
5. For v2026.2.19 feature highlights, explain usage when relevant:
   - Apple Watch companion MVP: watch inbox + watch command entry points (requires iOS/Watch app side setup).
   - iOS wake/reconnect improvements via APNs: reduces invoke failures while iOS app is backgrounded.
   - Paired-device hygiene commands:
     - `openclaw devices list`
     - `openclaw devices remove <id>`
     - `openclaw devices clear --yes [--pending]`
   - APNs registration/signing options: set `apns.{bundle_id,team_id,key_id}` in OpenClaw config when iOS push is needed.
   - APNs push-test pipeline: use to validate iOS push before relying on wake/reconnect.

## Input contract before creating a Telegram bot

Collect all fields before writing config:

- `display_name`
- `telegram_username` (e.g. `@canyonMain_bot`)
- `bot_token`
- `default_model` (full provider/model, e.g. `relay/gemini-3-pro-low`)
- `agent_id` (optional; derive from name if omitted)
- `is_main_agent` (`yes` or `no`)

If user also wants `/model relay` choices configured, collect model IDs list too.

## Add one bot and bind one agent

Preferred one-command flow for this skill:

```bash
python3 scripts/provision_telegram_bot.py \\
  --name "<display_name>" \\
  --username "@<telegram_username>" \\
  --token "<bot_token>" \\
  --model "<provider/model>"
```

Add `--main` when this bot should become the main agent.

1. Add Telegram account:

```bash
openclaw channels add \\
  --channel telegram \\
  --account <account_id> \\
  --name "<display_name>" \\
  --token "<bot_token>"
```

2. Create agent:

```bash
openclaw agents add "<display_name>" \\
  --non-interactive \\
  --workspace /Users/<user>/.openclaw/workspace-<agent_id> \\
  --agent-dir /Users/<user>/.openclaw/agents/<agent_id>/agent \\
  --model <default_model> \\
  --json
```

3. Ensure provider catalog exists for the new agent:

```bash
mkdir -p /Users/<user>/.openclaw/agents/<agent_id>/agent
cp /Users/<user>/.openclaw/agents/main/agent/models.json \\
  /Users/<user>/.openclaw/agents/<agent_id>/agent/models.json
```

4. Ensure explicit binding in `~/.openclaw/openclaw.json`:

```json
{
  "agentId": "<agent_id>",
  "match": {
    "channel": "telegram",
    "accountId": "<account_id>"
  }
}
```

5. Use open DM policy for fast testing when requested:
   - `dmPolicy: "open"`
   - `allowFrom: ["*"]`

6. Restart and verify:

```bash
openclaw gateway restart
openclaw channels status
openclaw agents list --json
```

## Make a bot the main agent

1. Set `agents.list` entry where `id == "main"`:
   - `name = <display_name>`
   - `model = <default_model>`
2. Set `agents.defaults.model.primary = <default_model>`.
3. Ensure Telegram binding for `main` points to the intended account.
4. Restart gateway and run smoke test.

## Configure relay and `/model` choices

1. Keep relay provider in both places:
   - `~/.openclaw/openclaw.json` at `models.providers.relay`
   - `~/.openclaw/agents/<agent_id>/agent/models.json` at `providers.relay`
2. Use OpenAI-compatible relay settings:
   - `baseUrl`: usually `http://127.0.0.1:8045/v1`
   - `api`: `openai-completions`
   - `apiKey`: relay key from user
3. Maintain model IDs under `relay.models` and sync all target files with `scripts/sync_relay_models.py`.
4. When user asks "can this model be selected in /model":
   - verify it exists in relay `/v1/models`
   - verify it exists in OpenClaw relay provider catalog
5. Control `/model` visibility with `agents.defaults.models`:
   - `{}` means do not restrict to a fixed allowlist.
   - non-empty map means only listed keys are selectable.

## Verification checklist

Run in order:

1. `openclaw gateway restart`
2. `openclaw channels status`
3. Relay probe: `curl -sS http://127.0.0.1:8045/v1/models -H "Authorization: Bearer <key>"`
4. `openclaw channels logs --channel telegram --lines 120`
5. Smoke test:

```bash
openclaw agent --agent <agent_id> --channel telegram --message "reply only: ok" --json
```

6. Confirm `result.meta.agentMeta.provider/model` matches expectation.
7. For image model requests, run one direct proxy probe and report exact upstream error code/message if failed.

## Anti-stall and execution-integrity protocol

Use this protocol when the user reports "it stopped", "you only explained", or "claimed done but not applied".

1. Keep queue mode stable:
   - Prefer `collect`.
   - Keep debounce at `1000ms` unless user explicitly asks to change.
2. For any state-changing task (cron/channel/agent/config edits):
   - Execute commands first.
   - Report completion only with real tool output evidence.
   - Include key proof fields (`id`, `updatedAtMs`, `delivery.to`, etc.).
3. If interrupted by new user messages mid-task:
   - Re-check real state before continuing.
   - Never assume previous edits succeeded.
4. If "assistant said done but no change":
   - Inspect session jsonl for actual `toolCall` commands (not only text claims).
   - Compare against current live state (`openclaw cron list --json`, config readback).
   - Apply missing edits and run a final readback verification.
5. Use explicit failure labels when needed:
   - `FAILED` when command ran and failed.
   - `NOT_EXECUTED` when no state-changing command was actually run.
6. For high-risk mixed prompts (explain + execute in one turn), prefer:
   - two-phase handling ("execute" then "explain"), or
   - strict response contract requiring command evidence lines only.


## 403 account verification re-test protocol

Use this when user says they finished Google verification and asks to re-test one/all accounts.

1. Re-test a specific account with direct warmup calls on active production models:
   - gemini-3-flash
   - gemini-3-pro-high
   - gemini-3-pro-image (only when this model is enabled in the user setup)
2. Pass criteria:
   - all tested models return HTTP 200 for that account.
3. Evidence you must provide:
   - latest request_logs rows for that email (status/url/model/time)
   - matching app.log Warmup-API SUCCESS lines with timestamps
4. If still 403:
   - return the latest validation_url for that specific account
   - require user to verify in an incognito window with that exact Google account signed in
   - keep account disabled/deprioritized until it passes re-test
5. Security rule:
   - never store or copy passwords, tokens, recovery emails, or 2FA secrets into skill files, repo files, or logs.

## Troubleshooting rules

- Telegram reaction (👀 ack) is a channel/runtime concern, not a memory-plugin concern.
- Do not patch memory plugins (for example `memory-lancedb-pro`) to force Telegram reactions; plugin edits will be overwritten by upgrades and create maintenance risk.
- When reaction feedback is requested, use config + runtime verification first:
  1. Check `channels.telegram.reactionLevel` (`ack`/`minimal`/`extensive` as needed).
  2. Check `channels.telegram.ackReaction` (for example `👀`).
  3. Keep `messages.ackReactionScope` aligned with desired scope (`all` when user wants broad coverage).
  4. Restart gateway and verify hot-reload/restart logs.
  5. Validate Telegram API capability directly (`setMessageReaction`) before blaming OpenClaw logic.
  6. Test on a fresh incoming message (avoid judging by old history items).
- If manual Telegram API reaction succeeds but OpenClaw ack is inconsistent, classify as OpenClaw channel path issue (not LanceDB), collect logs, and prefer OpenClaw config/version fix over plugin code hacks.
- Diagnose routing first when user says "wrong model".
- Inspect `bindings` before changing model provider config.
- Inspect session overrides in `~/.openclaw/agents/<agent_id>/sessions/sessions.json` when `/status` disagrees with defaults.
- If user says "you said done but it didn't change", run the execution-integrity protocol above before any further explanation.
- Distinguish relay-level failures from OpenClaw failures:
  - 429/503 capacity exhaustion: relay/upstream availability issue.
  - 403 validation required: upstream account verification issue.
  - warmup calls in monitor logs: internal relay warmup traffic, not user prompt traffic.
- If error signature matches Relay community-known Google-side issues (HTTP 400 precondition check, 403 ToS/validation, invalid project resource name), load `references/relay-tools.md` community section and clearly label the guidance as non-official/community-sourced.
- Prefer disable over delete for channel accounts unless user explicitly asks delete.
- Never delete workspace or agent dirs unless user explicitly asks.

## Response template for "create a new bot"

Ask exactly this checklist:

- 名称:
- @username:
- token:
- 默认模型(provider/model):
- 是否主智能体(是/否):

After completion, report:

- account_id
- agent_id
- default model
- binding target
- verification result (provider/model)
