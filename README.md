# openclaw-antigravity-skill

A practical skill repository for operating OpenClaw with Antigravity reverse-proxy models in real production usage.

This repo keeps one thing stable: **repeatable setup + repeatable troubleshooting** for multi-bot OpenClaw environments.

## What This Skill Is For

- Configure and operate OpenClaw agents/channels safely.
- Onboard/update Telegram bots and bind them to the right agent/model.
- Maintain Antigravity model catalogs and `/model` selector behavior.
- Run reliable cron workflows (collection, aggregation, delivery).
- Troubleshoot real issues fast (wrong model, no reply, 403/429, warmup confusion, delivery failures).

## Repository Layout

- `SKILL.md`: Main operating playbook.
- `references/official.md`: Official OpenClaw behavior and command references.
- `references/antigravity-tools.md`: Antigravity Tools operation notes and troubleshooting.
- `references/antigravity-models.md`: Model list/sync patterns for antigravity provider.
- `references/bot-onboarding.md`: Bot onboarding reference notes.
- `scripts/provision_telegram_bot.py`: One-shot bot provisioning helper.
- `scripts/sync_antigravity_models.py`: Sync antigravity model catalogs across config files.

## When New Content Gets Added

New content is added only when there is a **real operator-facing capability change**:

1. OpenClaw introduces a new usable feature, command, workflow, or config path.
2. Antigravity Tools introduces a new usable feature affecting model/proxy/account operations.
3. Existing steps become outdated due to version changes and need a new correct procedure.

## When Content Is NOT Added

Do not update the skill for changes that are only:

- bug fixes
- performance/stability tuning
- UI text or layout tweaks
- pure security patch notes with no operator workflow change

## Update Policy (OpenClaw + Antigravity)

When a new feature qualifies for inclusion:

1. Record **what changed** and **why operators should care**.
2. Add **how to use it** (commands + config path).
3. Add **how to verify success** (logs/status/output).
4. Place it in the correct section (`SKILL.md` and matching `references/*`).
5. Write a changelog entry.

## Security Rules

- Never commit real tokens, API keys, chat IDs, or credentials.
- Keep placeholders only (e.g. `<bot_token>`, `<api_key>`).
- If examples include secrets, redact before commit.

## Changelog Rules

Use `CHANGELOG.md` for operator-relevant changes only:

- Added new capability usage
- Changed operational process
- Added/updated troubleshooting flow

Skip entries for cosmetic-only edits.
