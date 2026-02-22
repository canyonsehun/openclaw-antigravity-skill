---
name: openclaw
description: Configure and operate OpenClaw with Telegram bots and antigravity reverse-proxy models (Antigravity Tools). Use when installing OpenClaw, setting up gateway/channels, creating or updating Telegram bot agents, configuring /model choices (especially antigravity), binding account-to-agent routing, validating antigravity scheduling/account behavior, and troubleshooting model/channel issues (including warmup, image models, 403/429).
---

# OpenClaw

Use this skill to build and maintain a stable multi-bot OpenClaw setup, especially when users need antigravity relay models and predictable `/model` behavior.

## Read references only when needed

- Read `references/official.md` when checking official OpenClaw setup/CLI behavior.
- Read `references/bot-onboarding.md` when creating or modifying Telegram bots.
- Read `references/antigravity-models.md` when changing antigravity relay models and `/model` visibility.
- Read `references/antigravity-tools.md` when requests involve Antigravity Tools behavior (account rotation, scheduling mode, LAN exposure, auth, warmup, image model support, 403/429 analysis).

## Workflow decision

1. Perform install/bootstrap work when OpenClaw is missing or broken.
2. Perform release-check/update work when user asks for latest version, changelog, or auto-upgrade.
3. Perform bot onboarding when user provides bot name/username/token/default model.
4. Perform antigravity model sync when user asks to add/remove `/model antigravity` options.
5. Perform antigravity capability checks when user asks whether image models, auto account/model behavior, or LAN proxy mode work.
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
- `default_model` (full provider/model, e.g. `antigravity/gemini-3-pro-low`)
- `agent_id` (optional; derive from name if omitted)
- `is_main_agent` (`yes` or `no`)

If user also wants `/model antigravity` choices configured, collect model IDs list too.

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

## Configure antigravity relay and `/model` choices

1. Keep antigravity provider in both places:
   - `~/.openclaw/openclaw.json` at `models.providers.antigravity`
   - `~/.openclaw/agents/<agent_id>/agent/models.json` at `providers.antigravity`
2. Use OpenAI-compatible relay settings:
   - `baseUrl`: usually `http://127.0.0.1:8045/v1`
   - `api`: `openai-completions`
   - `apiKey`: relay key from user
3. Maintain model IDs under `antigravity.models` and sync all target files with `scripts/sync_antigravity_models.py`.
4. When user asks "can this model be selected in /model":
   - verify it exists in relay `/v1/models`
   - verify it exists in OpenClaw antigravity provider catalog
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

- Diagnose routing first when user says "wrong model".
- Inspect `bindings` before changing model provider config.
- Inspect session overrides in `~/.openclaw/agents/<agent_id>/sessions/sessions.json` when `/status` disagrees with defaults.
- If user says "you said done but it didn't change", run the execution-integrity protocol above before any further explanation.
- Distinguish relay-level failures from OpenClaw failures:
  - 429/503 capacity exhaustion: relay/upstream availability issue.
  - 403 validation required: upstream account verification issue.
  - warmup calls in monitor logs: internal relay warmup traffic, not user prompt traffic.
- If error signature matches Antigravity community-known Google-side issues (HTTP 400 precondition check, 403 ToS/validation, invalid project resource name), load `references/antigravity-tools.md` community section and clearly label the guidance as non-official/community-sourced.
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
