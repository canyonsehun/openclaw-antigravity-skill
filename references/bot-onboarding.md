# Telegram bot onboarding playbook

## Required user input

- display name
- telegram username
- bot token
- default model (provider/model)
- is main agent or not

## Standard account and agent naming

- account_id: use a stable slug, e.g. `canyon-main`, `canyon-gemini-3-pro`
- agent_id: use lowercase kebab-case, e.g. `main`, `gemini-3-pro`, `claude-code`

## Command flow

Preferred automation:

```bash
python3 scripts/provision_telegram_bot.py \
  --name "<display_name>" \
  --username "@<telegram_username>" \
  --token "<bot_token>" \
  --model "<provider/model>"
```

Use `--main` for the main agent route.

```bash
openclaw channels add --channel telegram --account <account_id> --name "<display_name>" --token "<token>"
openclaw agents add "<display_name>" --non-interactive --workspace /Users/<user>/.openclaw/workspace-<agent_id> --agent-dir /Users/<user>/.openclaw/agents/<agent_id>/agent --model <default_model> --json
mkdir -p /Users/<user>/.openclaw/agents/<agent_id>/agent
cp /Users/<user>/.openclaw/agents/main/agent/models.json /Users/<user>/.openclaw/agents/<agent_id>/agent/models.json
openclaw gateway restart
openclaw channels status
```

## Required config checks

- Ensure one explicit binding per Telegram account.
- Ensure `match.channel` is `telegram`.
- Ensure `match.accountId` equals added Telegram account id.

## Final smoke test

```bash
openclaw agent --agent <agent_id> --channel telegram --message "reply only: ok" --json
```

Expect JSON result with expected `provider` and `model`.
