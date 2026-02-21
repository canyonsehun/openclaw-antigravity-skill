#!/usr/bin/env python3
"""Synchronize antigravity provider models across OpenClaw config files.

Usage:
  python3 sync_antigravity_models.py \
    --openclaw-json ~/.openclaw/openclaw.json \
    --api-key <key> \
    --base-url http://127.0.0.1:8045/v1

Optional:
  --model <id> (repeatable)
  --agent-models <path> (repeatable)
  --dry-run
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

DEFAULT_MODELS = [
    "gemini-3-pro-high",
    "gemini-3-pro-low",
    "gemini-3-flash",
    "gemini-2.5-flash-thinking",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "claude-sonnet-4-6",
    "claude-opus-4-6-thinking",
]


def model_entry(model_id: str) -> Dict:
    image_capable = model_id.startswith("claude-")
    context_window = 200000 if image_capable else 1048576
    return {
        "id": model_id,
        "name": model_id,
        "api": "openai-completions",
        "reasoning": True,
        "input": ["text", "image"] if image_capable else ["text"],
        "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0,
        },
        "contextWindow": context_window,
        "maxTokens": 8192,
    }


def upsert_provider_block(providers: Dict, base_url: str, api_key: str, models: List[str]) -> None:
    providers["antigravity"] = {
        "baseUrl": base_url,
        "apiKey": api_key,
        "api": "openai-completions",
        "models": [model_entry(m) for m in models],
    }


def update_openclaw_json(path: Path, base_url: str, api_key: str, models: List[str], dry_run: bool) -> bool:
    data = json.loads(path.read_text())
    providers = data.setdefault("models", {}).setdefault("providers", {})
    before = json.dumps(providers.get("antigravity", {}), sort_keys=True)
    upsert_provider_block(providers, base_url, api_key, models)
    after = json.dumps(providers.get("antigravity", {}), sort_keys=True)
    changed = before != after
    if changed and not dry_run:
        path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n")
    return changed


def update_agent_models(path: Path, base_url: str, api_key: str, models: List[str], dry_run: bool) -> bool:
    data = json.loads(path.read_text())
    providers = data.setdefault("providers", {})
    before = json.dumps(providers.get("antigravity", {}), sort_keys=True)
    upsert_provider_block(providers, base_url, api_key, models)
    after = json.dumps(providers.get("antigravity", {}), sort_keys=True)
    changed = before != after
    if changed and not dry_run:
        path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n")
    return changed


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Sync antigravity model provider across OpenClaw config files")
    p.add_argument("--openclaw-json", required=True)
    p.add_argument("--api-key", required=True)
    p.add_argument("--base-url", default="http://127.0.0.1:8045/v1")
    p.add_argument("--model", action="append", dest="models")
    p.add_argument("--agent-models", action="append", default=[])
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    models = args.models or DEFAULT_MODELS

    openclaw_json = Path(args.openclaw_json).expanduser().resolve()
    if not openclaw_json.exists():
        raise SystemExit(f"openclaw.json not found: {openclaw_json}")

    changed_files: List[str] = []
    if update_openclaw_json(openclaw_json, args.base_url, args.api_key, models, args.dry_run):
        changed_files.append(str(openclaw_json))

    agent_files: List[Path] = []
    if args.agent_models:
        agent_files = [Path(p).expanduser().resolve() for p in args.agent_models]
    else:
        root = openclaw_json.parent / "agents"
        agent_files = list(root.glob("*/agent/models.json"))

    for f in agent_files:
        if not f.exists():
            continue
        if update_agent_models(f, args.base_url, args.api_key, models, args.dry_run):
            changed_files.append(str(f))

    action = "Would update" if args.dry_run else "Updated"
    if changed_files:
        print(f"{action} {len(changed_files)} file(s):")
        for path in changed_files:
            print(path)
    else:
        print("No changes needed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
