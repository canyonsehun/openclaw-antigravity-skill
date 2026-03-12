<div align="center">

# 🦞 openclaw-graduate · OpenClaw Operations Skill Repository

**A production-oriented OpenClaw setup, deployment, troubleshooting, and operations playbook**

*This repository turns our real-world local macOS + remote Codespaces experience into an execution-ready OpenClaw skill and reference set.*

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/canyonsehun/openclaw-graduate)
[![Operations](https://img.shields.io/badge/Focus-Operations%20%26%20Troubleshooting-6f42c1)](https://github.com/canyonsehun/openclaw-graduate)
[![Codespaces](https://img.shields.io/badge/Remote-Codespaces-24292f)](https://github.com/features/codespaces)
[![Telegram](https://img.shields.io/badge/Channel-Telegram-26A5E4)](https://telegram.org/)
[![Claude Code](https://img.shields.io/badge/Tool-Claude%20Code-D97706)](https://www.anthropic.com/claude-code)
[![Codex](https://img.shields.io/badge/Tool-Codex-0F766E)](https://openai.com/)

[中文](./README.md) | **English (current)**

</div>

---

## ✨ Why this repository exists

The official OpenClaw docs are useful, but often generic. This repository is the **battle-tested operator layer**: it captures what we actually ran, fixed, verified, and kept using in local and remote environments.

| Scenario | What this repository gives you |
|---|---|
| 🛠️ **Install / repair** | `openclaw setup`, `doctor --repair`, gateway startup, and health checks |
| 🤖 **Multi-bot / multi-agent routing** | Telegram onboarding, agent binding, default models, and `/model` catalog control |
| 🧠 **Provider switching** | working setups for `codex`, `anthropic / Claude`, relay, and OpenAI-compatible providers |
| ☁️ **Remote deployment** | GitHub Codespaces / github.dev bootstrap patterns and env-file driven startup |
| 🔍 **Troubleshooting** | 403 / 429, Cloudflare challenge, wrong-model routing, no-reply, malformed JSON, session locks |
| 🧩 **Memory plugin integration** | `memory-lancedb-pro` setup, update-check task, and runtime diagnostics |

---

## 🚀 What this repository covers

- **Install and repair**: `openclaw setup`, `openclaw doctor --repair`, `gateway start/restart/status`, `channels status`, and `agents list`
- **Provider and model switching**: working setups for `codex`, `anthropic / Claude`, and OpenAI-compatible relay providers, including defaults, fallbacks, and smoke tests
- **Bot and channel onboarding**: Telegram bot onboarding, agent binding, default model assignment, multi-bot routing, and `/model` catalog maintenance
- **Remote deployment**: GitHub Codespaces / github.dev bootstrap patterns and `~/.secrets/openclaw.env` conventions
- **Plugin and memory diagnostics**: `memory-lancedb-pro`, Jina embedding checks, plugin registration failures, and session lock issues
- **Claude Code integration**: practical fallback flows when Claude Code works remotely and OpenClaw needs a usable execution path
- **Troubleshooting and verification**: concrete paths for 403 / 429, Cloudflare challenge pages, wrong-model routing, no-reply cases, malformed JSON, and provider config mistakes

---

## 🧭 Quick Navigation

| Path | Purpose |
|---|---|
| `SKILL.md` | main skill instructions |
| `references/official.md` | official OpenClaw behavior, release notes, CLI references |
| `references/providers.md` | provider setup for `codex`, Claude, and others |
| `references/channels.md` | Telegram / WhatsApp / Slack and channel setup |
| `references/multi_agent.md` | multi-agent routing and binding notes |
| `references/memory-lancedb-pro.md` | memory plugin setup, tools, cron update flow, and diagnostics |
| `references/experience-distill-bot.md` | experience distill / skill distill bot workflow for turning stable `main` chat conclusions into skill/reference drafts |
| `scripts/provision_telegram_bot.py` | Telegram bot provisioning helper |
| `scripts/sync_relay_models.py` | relay model catalog sync helper |

---

## 🧠 memory-lancedb-pro source and author

This repository documents how to use `memory-lancedb-pro` with OpenClaw, but the plugin code itself lives upstream.

- **Current source repository**: [`CortexReach/memory-lancedb-pro`](https://github.com/CortexReach/memory-lancedb-pro)
- **Historical public path**: [`win4r/memory-lancedb-pro`](https://github.com/win4r/memory-lancedb-pro)
- **Current GitHub author / maintainer**: `CortexReach`
- **What we maintain here**: OpenClaw-side setup, integration, update checks, and troubleshooting notes

---

## 🌟 Highlights

- **Built from real operations**: derived from actual local macOS and remote Codespaces runs
- **Execution-ready guidance**: focused on commands, file paths, verification steps, and failure signals
- **Clear local vs remote split**: separates what works locally, what fails remotely, and when Claude fallback is the right move
- **Ops-first focus**: optimized for “why it broke”, “what to change”, and “how to confirm it is fixed”
- **Reusable helper scripts**: includes Telegram bot provisioning and relay model sync helpers

---

## 📦 Repository Layout

| Path | Role |
|---|---|
| `SKILL.md` | main skill instructions |
| `references/` | topic-specific operating references |
| `scripts/` | helper scripts |
| `CHANGELOG.md` | repository change history |

---

## ⚡ Quick Start

```bash
openclaw --version
openclaw gateway status
openclaw channels status
openclaw agents list --json
openclaw agent --local --agent main --message "reply only: ok" --json
```

## Scope

- OpenClaw install, upgrades, and gateway ops
- Channel setup for Telegram / WhatsApp / Slack and more
- Provider/model configuration and switching
- Remote deployment on Codespaces / github.dev
- Troubleshooting 403 / 429, wrong-model routing, no-reply, session locks, and plugin issues

## Sync Policy

- Mirror only the current local `~/.codex/skills/openclaw` content
- Keep only operator-relevant procedures, commands, config, and troubleshooting conclusions
- Never commit real keys, tokens, or chat identifiers
