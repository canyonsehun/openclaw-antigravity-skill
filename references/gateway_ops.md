# OpenClaw Gateway Operations Reference

## Architecture

- Single long-lived daemon owns all messaging surfaces
- One multiplexed port for WebSocket RPC, HTTP APIs, Control UI, and hooks
- One Gateway per host controls a single WhatsApp/Baileys session
- Canvas served at `/__openclaw__/canvas/` and `/__openclaw__/a2ui/` on same port
- Default bind: `127.0.0.1:18789` (loopback)

Components:
- **Gateway daemon**: provider connections, typed WS API, JSON Schema validation
- **Clients** (macOS app / CLI / web admin): one WS connection each
- **Nodes** (macOS / iOS / Android / headless): WS with `role: node`, expose device commands
- **WebChat**: static UI using Gateway WS API

## Starting the Gateway

```bash
# Foreground (dev/debug)
openclaw gateway --port 18789
openclaw gateway --port 18789 --verbose     # Debug/trace to stdout
openclaw gateway --force                    # Kill existing listener first

# With auth
openclaw gateway --token <token>
openclaw gateway --password <password>

# With Tailscale
openclaw gateway --tailscale serve          # Tailscale Serve
openclaw gateway --tailscale funnel         # Tailscale Funnel (public)

# Dev profile (separate port 19001)
openclaw --dev gateway --allow-unconfigured
```

## Service Management

### macOS (launchd)

```bash
openclaw gateway install    # Install launch agent (ai.openclaw.gateway)
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway status     # Probe RPC
openclaw gateway uninstall
```

### Linux (systemd user)

```bash
openclaw gateway install
systemctl --user enable --now openclaw-gateway.service
openclaw gateway status
```

### Linux (system service)

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now openclaw-gateway.service
sudo loginctl enable-linger <username>   # Keep user service running
```

### Service Install Options

```bash
openclaw gateway install --port <port> --runtime <runtime> --token <token> --force
```

Note: Node runtime recommended; Bun has WhatsApp/Telegram bugs.

## Port and Bind Configuration

Precedence (highest to lowest):
1. `--port` CLI flag
2. `OPENCLAW_GATEWAY_PORT` env var
3. `gateway.port` in config
4. Default: `18789`

Bind modes:
- `loopback` (default) — localhost only
- `tailnet` — Tailscale network only
- `lan` — local network
- `auto` — auto-detect
- `custom` — manual bind address

## Hot Reload

Config setting: `gateway.reload.mode`

| Mode | Behavior |
|---|---|
| `off` | No automatic reload |
| `hot` | Hot-apply supported changes without restart |
| `restart` | Full restart on config change |
| `hybrid` | Hot-apply what it can, restart for the rest |

What hot-applies: system prompt changes, model selection, tool config.
What needs restart: port/bind changes, channel add/remove, auth changes.

## Remote Access

### SSH Tunnel (simple)

```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

Then connect clients to `ws://127.0.0.1:18789` with same token/password.

### Tailscale

```bash
openclaw gateway --tailscale serve    # Private (tailnet only)
openclaw gateway --tailscale funnel   # Public (internet-accessible)
```

### VPN

Any VPN that provides network-level access. Gateway auth still required.

## Multiple Gateways

Requirements per instance:
- Unique `gateway.port`
- Unique `OPENCLAW_CONFIG_PATH`
- Unique `OPENCLAW_STATE_DIR`
- Unique `agents.defaults.workspace`

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json OPENCLAW_STATE_DIR=~/.openclaw-a openclaw gateway --port 19001
OPENCLAW_CONFIG_PATH=~/.openclaw/b.json OPENCLAW_STATE_DIR=~/.openclaw-b openclaw gateway --port 19002
```

## Health Checks

```bash
openclaw gateway status             # Runtime: running, RPC probe: ok
openclaw gateway status --deep      # System-level scan
openclaw gateway status --json      # JSON output for scripting
openclaw channels status --probe    # Connected/ready channels
openclaw health                     # Overall health check
openclaw doctor                     # Full diagnostics
openclaw doctor --fix               # Auto-repair
```

## Operator Commands

```bash
openclaw gateway status [--deep] [--json]
openclaw gateway install
openclaw gateway restart
openclaw gateway stop
openclaw secrets reload
openclaw logs --follow
openclaw logs --limit 200
openclaw logs --json
openclaw doctor
```

## Gateway Protocol

- Transport: WebSocket, text frames, JSON payloads
- First frame must be `connect`
- After handshake: `hello-ok` snapshot (presence, health, stateVersion, uptimeMs)
- Requests: `{type:"req", id, method, params}` → `{type:"res", id, ok, payload|error}`
- Events: `{type:"event", event, payload, seq?, stateVersion?}`
- Auth token via `connect.params.auth.token` or `OPENCLAW_GATEWAY_TOKEN`
- Idempotency keys required for `send`, `agent` methods
- Nodes declare `role: "node"` with capabilities in `connect`

Common events: `connect.challenge`, `agent`, `chat`, `presence`, `tick`, `health`, `heartbeat`, `shutdown`.

## Install / Update / Uninstall

### Install Methods

```bash
# Installer script (macOS / Linux)
curl -fsSL https://openclaw.ai/install.sh | bash

# npm
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

System requirements: Node 22+, macOS/Linux/Windows.

### Update

```bash
npm install -g openclaw@latest
openclaw doctor   # Apply any migrations
```

### Uninstall

```bash
openclaw uninstall
```

## Common Failure Signatures

| Error | Cause | Fix |
|---|---|---|
| `refusing to bind gateway ... without auth` | Non-loopback bind without token | Set `gateway.auth.token` or `gateway.auth.password` |
| `another gateway instance is already listening` / `EADDRINUSE` | Port conflict | `openclaw gateway --force` or change port |
| `Gateway start blocked: set gateway.mode=local` | Local mode not enabled | Set `gateway.mode="local"` |
| `unauthorized` / reconnect loop | Token/password mismatch | Check `OPENCLAW_GATEWAY_TOKEN` or config auth |
| `device identity required` | Missing device auth | Ensure client completes connect.challenge flow |
| No replies from bot | Pairing/allowlist/mention gating | Check `openclaw pairing list`, DM policy, mention patterns |

## Environment Variables

| Variable | Purpose |
|---|---|
| `OPENCLAW_GATEWAY_TOKEN` | Gateway auth token |
| `OPENCLAW_GATEWAY_PASSWORD` | Gateway auth password |
| `OPENCLAW_GATEWAY_PORT` | Override gateway port |
| `OPENCLAW_CONFIG_PATH` | Override config file path |
| `OPENCLAW_STATE_DIR` | Override state directory |
| `OPENCLAW_HOME` | Override home directory |
| `OPENCLAW_LOAD_SHELL_ENV` | Import shell env (set to `1`) |
