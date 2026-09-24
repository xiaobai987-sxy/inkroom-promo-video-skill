#!/usr/bin/env python3
"""Validate shot/state contracts without claiming media approval."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SHOT_STATUSES = {"planned", "prompt_ready", "received", "approved", "rejected", "placeholder", "blocked"}
SHOT_KINDS = {"seedance", "recording", "placeholder", "closing_card"}


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_shots(shots: list[dict], check_files: bool, root: Path) -> list[str]:
    errors: list[str] = []
    seen: set[tuple[str, str]] = set()
    for index, shot in enumerate(shots):
        prefix = f"shots[{index}]"
        for key in ("shot_code", "kind", "status"):
            if not shot.get(key):
                errors.append(f"{prefix} missing {key}")
        if shot.get("kind") not in SHOT_KINDS:
            errors.append(f"{prefix} invalid kind {shot.get('kind')}")
        if shot.get("status") not in SHOT_STATUSES:
            errors.append(f"{prefix} invalid status {shot.get('status')}")
        key = (str(shot.get("shot_code")), str(shot.get("take", "")))
        if key in seen:
            errors.append(f"{prefix} duplicate shot/take {key[0]}/{key[1]}")
        seen.add(key)
        if shot.get("status") == "approved":
            if shot.get("kind") == "placeholder":
                errors.append(f"{prefix} placeholder cannot be approved")
            for key_name in ("return_file", "approved_source", "sha256"):
                if not shot.get(key_name):
                    errors.append(f"{prefix} approved shot missing {key_name}")
        if shot.get("status") == "received" and shot.get("approved_source"):
            errors.append(f"{prefix} received shot cannot already claim approved_source")
        if check_files:
            for key_name in ("return_file", "approved_source", "first_frame"):
                value = shot.get(key_name)
                if value and not (root / value).is_file():
                    errors.append(f"{prefix} missing file {value}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--check-files", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    state = load(args.state)
    root = args.state.parent.parent
    manifest = load(args.manifest) if args.manifest else state
    shots = manifest.get("shots", []) if isinstance(manifest, dict) else manifest
    errors = []
    if not isinstance(shots, list):
        errors.append("shots must be a list")
    else:
        errors.extend(validate_shots(shots, args.check_files, root))
    if isinstance(state, dict) and state.get("stage") == "publish_ready":
        if state.get("blockers"):
            errors.append("publish_ready state still has blockers")
        if any(shot.get("status") == "placeholder" for shot in state.get("shots", [])):
            errors.append("publish_ready cannot contain placeholders")
    result = {"ok": not errors, "shot_count": len(shots) if isinstance(shots, list) else 0, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
