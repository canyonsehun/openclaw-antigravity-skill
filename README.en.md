# openclaw-antigravity-skill

> 🌐 Language: [中文](./README.md) | **English (current)**

This is a production-oriented OpenClaw + Antigravity Tools skill repository focused on repeatable setup, operations, and troubleshooting for multi-bot environments.

## What This Skill Is For

- Configure and operate OpenClaw agents/channels safely.
- Onboard or update Telegram bots and bind them to the correct agent/model.
- Maintain Antigravity model catalogs and `/model` selection behavior.
- Run reliable cron workflows (collect, aggregate, deliver).
- Troubleshoot quickly: wrong model routing, no reply, 403/429, warmup confusion, delivery failures.

## Repository Layout

- `SKILL.md`: Main playbook and operating rules.
- `references/official.md`: Official OpenClaw behavior and command references.
- `references/antigravity-tools.md`: Antigravity Tools operations and troubleshooting notes.
- `references/antigravity-models.md`: Antigravity model/sync rules.
- `references/bot-onboarding.md`: Bot onboarding reference notes.
- `scripts/provision_telegram_bot.py`: One-shot bot provisioning helper.
- `scripts/sync_antigravity_models.py`: Model catalog sync helper.

## When New Content Is Added

This repository is **continuously maintained** and checked along OpenClaw + Antigravity Tools releases.  
However, updates are added only when there is an **operator-facing capability change**, with a focus on "how to use the new capability."

1. OpenClaw introduces a new usable command/config entry/workflow, and we document usage, config steps, and verification.
2. Antigravity Tools introduces a new capability affecting model selection, proxy calls, account scheduling, or routing/warmup behavior.
3. Existing procedures become outdated due to version changes, requiring replacement and migration guidance.

## When Content Is Not Added

Do not update the skill for the following unless operator behavior changes:

- bug-fix-only changes
- performance/stability-only improvements
- UI copy/layout tweaks
- security patch notes that do not change operator workflows

## Update Policy (OpenClaw + Antigravity)

For each qualifying update, keep it execution-ready:

1. What changed, who is affected, and where it impacts operations.
2. How to use it (commands + config paths + required params/prerequisites).
3. How to verify success (logs/status/output + failure signals).
4. Where docs must be updated (`SKILL.md` + matching `references/*`) and add a `CHANGELOG.md` entry.
5. Content rule: prioritize "how to use new capability", avoid noise-only updates.

## Security Rules

- Never commit real tokens, API keys, chat IDs, or credentials.
- Use placeholders only (e.g. `<bot_token>`, `<api_key>`).
- Redact any sensitive values before commit.

## Changelog Rules

`CHANGELOG.md` should include only operator-relevant changes:

- new capability usage
- process changes
- troubleshooting additions/fixes

Skip cosmetic-only edits.
