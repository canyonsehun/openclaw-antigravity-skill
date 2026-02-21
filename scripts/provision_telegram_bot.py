#!/usr/bin/env python3
"""Provision one Telegram bot + OpenClaw agent + binding, then restart and verify."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "bot"


def derive_account_id(username: str, fallback_name: str) -> str:
    raw = username.strip().lstrip("@")
    raw = raw.replace("_", "-")
    if raw.endswith("-bot"):
        raw = raw[: -len("-bot")]
    elif raw.endswith("bot"):
        raw = raw[: -len("bot")]
    raw = slugify(raw)
    if raw:
        return raw
    return slugify(fallback_name)


def run(cmd: list[str], dry_run: bool = False) -> str:
    print("+", " ".join(shlex.quote(c) for c in cmd))
    if dry_run:
        return ""
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        if proc.stdout:
            print(proc.stdout, file=sys.stderr)
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
        raise RuntimeError("Command failed (%s): %s" % (proc.returncode, " ".join(cmd)))
    if proc.stdout.strip():
        print(proc.stdout.strip())
    return proc.stdout


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())


def save_json(path: Path, data: Dict[str, Any], dry_run: bool = False) -> None:
    if dry_run:
        return
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n")


def find_agent(agents: list[Dict[str, Any]], agent_id: str) -> Optional[Dict[str, Any]]:
    for item in agents:
        if str(item.get("id", "")) == agent_id:
            return item
    return None


def ensure_agent_model_catalog(openclaw_home: Path, agent_id: str, dry_run: bool = False) -> None:
    src = openclaw_home / "agents" / "main" / "agent" / "models.json"
    dst = openclaw_home / "agents" / agent_id / "agent" / "models.json"
    if src.resolve() == dst.resolve():
        return
    if not src.exists():
        return
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Provision Telegram bot + OpenClaw agent")
    parser.add_argument("--name", required=True, help="Display name")
    parser.add_argument("--username", required=True, help="Telegram username, e.g. @canyonMain_bot")
    parser.add_argument("--token", required=True, help="Telegram Bot API token")
    parser.add_argument("--model", required=True, help="Default model, e.g. antigravity/gemini-3-pro-low")
    parser.add_argument("--main", action="store_true", help="Use/update main agent")
    parser.add_argument("--agent-id", help="Override agent id")
    parser.add_argument("--account-id", help="Override telegram account id")
    parser.add_argument("--openclaw-home", default="~/.openclaw", help="OpenClaw home path")
    parser.add_argument("--dm-policy", default="open", choices=["open", "pairing"], help="Telegram DM policy")
    parser.add_argument("--skip-restart", action="store_true", help="Skip gateway restart")
    parser.add_argument("--skip-verify", action="store_true", help="Skip smoke verify message")
    parser.add_argument("--verify-message", default="reply only: ok", help="Smoke verify message")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    openclaw_home = Path(args.openclaw_home).expanduser().resolve()
    openclaw_json = openclaw_home / "openclaw.json"
    if not openclaw_json.exists():
        raise SystemExit("openclaw.json not found: %s" % openclaw_json)

    account_id = args.account_id or derive_account_id(args.username, args.name)
    agent_id = "main" if args.main else (args.agent_id or slugify(args.name))

    data = load_json(openclaw_json)
    agents_cfg = data.setdefault("agents", {})
    agents_list = agents_cfg.setdefault("list", [])
    existing_agent = find_agent(agents_list, agent_id)

    run(
        [
            "openclaw",
            "channels",
            "add",
            "--channel",
            "telegram",
            "--account",
            account_id,
            "--name",
            args.name,
            "--token",
            args.token,
        ],
        dry_run=args.dry_run,
    )

    workspace = str(openclaw_home / ("workspace" if agent_id == "main" else "workspace-" + agent_id))
    agent_dir = str(openclaw_home / "agents" / agent_id / "agent")

    if (not args.main) and (existing_agent is None):
        run(
            [
                "openclaw",
                "agents",
                "add",
                args.name,
                "--non-interactive",
                "--workspace",
                workspace,
                "--agent-dir",
                agent_dir,
                "--model",
                args.model,
                "--json",
            ],
            dry_run=args.dry_run,
        )
        if not args.dry_run:
            data = load_json(openclaw_json)
            agents_cfg = data.setdefault("agents", {})
            agents_list = agents_cfg.setdefault("list", [])
            existing_agent = find_agent(agents_list, agent_id)

    if existing_agent is None:
        existing_agent = {
            "id": agent_id,
            "name": args.name,
            "workspace": workspace,
            "agentDir": agent_dir,
            "model": args.model,
        }
        agents_list.append(existing_agent)

    existing_agent["name"] = args.name
    existing_agent["model"] = args.model
    existing_agent.setdefault("workspace", workspace)
    existing_agent.setdefault("agentDir", agent_dir)

    if args.main:
        defaults = agents_cfg.setdefault("defaults", {})
        model_defaults = defaults.setdefault("model", {})
        model_defaults["primary"] = args.model

    telegram = data.setdefault("channels", {}).setdefault("telegram", {})
    accounts = telegram.setdefault("accounts", {})
    acc = accounts.setdefault(account_id, {})
    acc["name"] = args.name
    acc["enabled"] = True
    acc["botToken"] = args.token
    acc["dmPolicy"] = args.dm_policy
    acc["groupPolicy"] = acc.get("groupPolicy", "allowlist")
    acc["streamMode"] = acc.get("streamMode", "partial")
    if args.dm_policy == "open":
        acc["allowFrom"] = ["*"]

    bindings = data.setdefault("bindings", [])
    cleaned = []
    for b in bindings:
        match = b.get("match", {})
        if match.get("channel") != "telegram":
            cleaned.append(b)
            continue
        if args.main and b.get("agentId") == "main":
            continue
        if match.get("accountId") == account_id:
            continue
        if b.get("agentId") == agent_id:
            continue
        cleaned.append(b)
    cleaned.append({"agentId": agent_id, "match": {"channel": "telegram", "accountId": account_id}})
    data["bindings"] = cleaned

    save_json(openclaw_json, data, dry_run=args.dry_run)
    ensure_agent_model_catalog(openclaw_home, agent_id, dry_run=args.dry_run)

    if not args.skip_restart:
        run(["openclaw", "gateway", "restart"], dry_run=args.dry_run)
        run(["openclaw", "channels", "status"], dry_run=args.dry_run)

    verify_provider = None
    verify_model = None
    if not args.skip_verify:
        out = run(
            [
                "openclaw",
                "agent",
                "--agent",
                agent_id,
                "--channel",
                "telegram",
                "--message",
                args.verify_message,
                "--json",
            ],
            dry_run=args.dry_run,
        )
        if out.strip() and (not args.dry_run):
            payload = json.loads(out)
            meta = payload.get("result", {}).get("meta", {}).get("agentMeta", {})
            verify_provider = meta.get("provider")
            verify_model = meta.get("model")

    summary = {
        "display_name": args.name,
        "telegram_username": args.username,
        "account_id": account_id,
        "agent_id": agent_id,
        "is_main_agent": args.main,
        "expected_model": args.model,
        "verified_provider": verify_provider,
        "verified_model": verify_model,
        "config": str(openclaw_json),
    }
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
