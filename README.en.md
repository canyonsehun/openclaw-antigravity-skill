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

Add content only when there is an **operator-facing capability change**:

1. OpenClaw introduces a new usable command/config/workflow.
2. Antigravity Tools introduces a new usable capability affecting model/proxy/account operations.
3. Existing procedures become outdated due to version changes.

## When Content Is Not Added

Do not update the skill for:

- bug-fix-only changes
- performance/stability-only improvements
- UI copy/layout tweaks
- security patch notes that do not change operator workflows

## Update Policy (OpenClaw + Antigravity)

For each qualifying update, include:

1. What changed and why it matters for operators.
2. How to use it (commands + config paths).
3. How to verify success (logs/status/output).
4. Where to place docs (`SKILL.md` + matching `references/*`).
5. A changelog entry in `CHANGELOG.md`.

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
