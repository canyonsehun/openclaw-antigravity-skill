# OpenClaw Model Providers Reference

## Quick Start

1. Authenticate with provider (usually via `openclaw onboard` or `openclaw models auth add`)
2. Set default model in config or CLI:

```bash
openclaw models set anthropic/claude-sonnet-4-5
```

## Supported Providers

### Cloud Providers

| Provider | Model Format | Auth Method |
|---|---|---|
| Anthropic | `anthropic/claude-*` | API key or OAuth |
| OpenAI | `openai/gpt-*` | API key or Codex OAuth |
| Venice AI | `venice/llama-*`, `venice/claude-*` | API key |
| OpenRouter | `openrouter/*` | API key |
| Google (Gemini) | `google/*` | API key |
| Together AI | `together/*` | API key |
| Mistral | `mistral/*` | API key |
| Moonshot AI (Kimi) | `moonshot/*` | API key |
| Amazon Bedrock | `bedrock/*` | AWS credentials |
| Qwen | `qwen/*` | OAuth |
| Hugging Face | `huggingface/*` | API key |
| NVIDIA | `nvidia/*` | API key |
| Cloudflare AI Gateway | via gateway config | API key |
| Vercel AI Gateway | via gateway config | API key |
| LiteLLM | via unified gateway | API key |
| Z.AI | `zai/*` | API key |
| Xiaomi | `xiaomi/*` | API key |
| GLM | `glm/*` | API key |
| MiniMax | `minimax/*` | API key |
| Qianfan | `qianfan/*` | API key |
| OpenCode Zen | `opencode/*` | API key |

### Local Providers

| Provider | Notes |
|---|---|
| Ollama | `ollama/*` — local models |
| vLLM | `vllm/*` — local models |

### Antigravity Relay (custom)

OpenAI-compatible relay at `http://127.0.0.1:8045/v1`. See `references/antigravity-models.md` for full setup.

```json5
{
  models: {
    providers: {
      antigravity: {
        api: "openai-completions",
        baseUrl: "http://127.0.0.1:8045/v1",
        apiKey: "<relay-key>",
      },
    },
  },
}
```

## CLI Commands

```bash
# Model management
openclaw models                         # Overview
openclaw models list --all              # All available models
openclaw models list --local            # Local models only
openclaw models list --provider <name>  # Filter by provider
openclaw models status                  # Auth/token status
openclaw models status --probe          # Live probe auth profiles
openclaw models set <provider/model>    # Set default primary
openclaw models set-image <model>       # Set default image model
openclaw models scan                    # Scan for available models

# Fallbacks
openclaw models fallbacks list
openclaw models fallbacks add <model>
openclaw models fallbacks remove <model>
openclaw models fallbacks clear

# Auth
openclaw models auth add                # Interactive auth
openclaw models auth setup-token        # Token setup
openclaw models auth paste-token        # Paste existing token
openclaw models auth order get|set|clear
```

## Configuration

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-5.2"],
      },
      imageModel: {
        primary: "openai/dall-e-3",
      },
      models: {
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "openai/gpt-5.2": { alias: "GPT" },
      },
      imageMaxDimensionPx: 1200,  // Default 1200; reduces vision-token usage
    },
  },
}
```

- `agents.defaults.models` defines the model catalog and allowlist for `/model` command
- `{}` means do not restrict to a fixed allowlist
- Non-empty map: only listed keys are selectable

## Model Fallbacks

When primary model fails, Gateway tries fallbacks in order:

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["anthropic/claude-sonnet-4-5", "openai/gpt-5.2"],
      },
    },
  },
}
```

## Auth Profiles

Stored at: `~/.openclaw/agents/<id>/agent/auth-profiles.json`

```bash
openclaw models status --check          # Exit 1=expired/missing, 2=expiring
openclaw models status --probe          # Live probe
openclaw models status --probe-provider anthropic
```

## Local Models

### Ollama

```bash
# Install Ollama, then:
openclaw models set ollama/llama3
```

### vLLM

```bash
openclaw models set vllm/my-model
```

See provider-specific docs at https://docs.openclaw.ai/providers/.
