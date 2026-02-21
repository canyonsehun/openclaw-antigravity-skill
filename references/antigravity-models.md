# Antigravity relay model rules

## Provider shape

Use provider key `antigravity` with OpenAI-compatible API mode:

- `baseUrl`: relay endpoint (common local relay: `http://127.0.0.1:8045/v1`)
- `apiKey`: relay key
- `api`: `openai-completions`
- `models`: explicit model catalog entries

## Current model set used in this environment

- gemini-3-pro-high
- gemini-3-pro-low
- gemini-3-flash
- gemini-2.5-flash-thinking
- gemini-2.5-flash
- gemini-2.5-flash-lite
- claude-sonnet-4-6
- claude-opus-4-6-thinking

Optional model (supported upstream but can be capacity-limited):

- gemini-3-pro-image

Removed from current set:

- claude-sonnet-4-5
- claude-sonnet-4-5-thinking

## `/model` visibility behavior

- `agents.defaults.models = {}`: do not restrict to fixed allowlist keys.
- Non-empty `agents.defaults.models`: restrict selectable models to listed keys.

## Sync target files

- `~/.openclaw/openclaw.json`
- `~/.openclaw/agents/main/agent/models.json`
- `~/.openclaw/agents/<bot-agent>/agent/models.json` for each active bot agent

## Validation rule before promising model availability

If user asks "can this model be used now", always run a live probe first:

1. Check `GET /v1/models` includes the model id.
2. Send one real completion/image request through relay.
3. If failure occurs, report exact upstream code and reason (for example: `MODEL_CAPACITY_EXHAUSTED`, `VALIDATION_REQUIRED`).
