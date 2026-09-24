#!/usr/bin/env python3
"""Manage explicit, auditable project-state transitions."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


STAGES = (
    "intake",
    "facts_locked",
    "outline_review",
    "copy_review",
    "script_review",
    "storyboard_review",
    "frames_review",
    "seedance_package_ready",
    "awaiting_external_returns",
    "per_shot_received",
    "per_shot_approved",
    "per_shot_rejected",
    "assembly_preview",
    "audio_review",
    "qa_pass",
    "user_render_approval",
    "rendered_downloaded",
    "publish_ready",
)

NEXT = {
    "intake": {"facts_locked", "blocked"},
    "facts_locked": {"outline_review", "blocked"},
    "outline_review": {"copy_review", "blocked"},
    "copy_review": {"script_review", "blocked"},
    "script_review": {"storyboard_review", "blocked"},
    "storyboard_review": {"frames_review", "blocked"},
    "frames_review": {"seedance_package_ready", "blocked"},
    "seedance_package_ready": {"awaiting_external_returns", "per_shot_received", "blocked"},
    "awaiting_external_returns": {"per_shot_received", "blocked"},
    "per_shot_received": {"per_shot_approved", "per_shot_rejected", "blocked"},
    "per_shot_approved": {"assembly_preview", "blocked"},
    "per_shot_rejected": {"frames_review", "seedance_package_ready", "blocked"},
    "assembly_preview": {"audio_review", "blocked"},
    "audio_review": {"qa_pass", "blocked"},
    "qa_pass": {"user_render_approval", "blocked"},
    "user_render_approval": {"rendered_downloaded", "blocked"},
    "rendered_downloaded": {"publish_ready", "blocked"},
    "publish_ready": set(),
    "blocked": set(STAGES) - {"blocked"},
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("state must be a JSON object")
    return value


def save(path: Path, value: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def event(state: dict, name: str, **details: object) -> None:
    state.setdefault("events", []).append({"event": name, "at": timestamp(), **details})


def transition(path: Path, target: str, approved_by: str | None, note: str | None) -> dict:
    if target not in STAGES and target != "blocked":
        raise ValueError(f"unknown stage: {target}")
    state = load(path)
    current = state.get("stage")
    if target not in NEXT.get(current, set()):
        raise ValueError(f"invalid transition {current} -> {target}")
    review_gate = target.endswith("_review") or target in {"user_render_approval", "publish_ready"}
    if review_gate and not approved_by:
        raise ValueError(f"{target} requires --approved-by")
    state["stage"] = target
    state["status"] = "blocked" if target == "blocked" else ("approved" if approved_by else "awaiting_user")
    if target != "blocked":
        state["blockers"] = []
    if target == "blocked" and note:
        state["blockers"] = sorted(set(state.get("blockers", [])) | {note})
    event(state, "transition", from_stage=current, to_stage=target, approved_by=approved_by, note=note)
    if approved_by:
        state.setdefault("approvals", []).append({"gate": target, "decision": "approved", "approved_by": approved_by, "at": timestamp(), "notes": note or ""})
    save(path, state)
    return state


def add_artifact(path: Path, artifact_type: str, artifact_path: str, status: str) -> dict:
    state = load(path)
    project_root = path.parent.parent
    resolved = (project_root / artifact_path).resolve()
    if not resolved.is_file():
        raise ValueError(f"artifact is not a file: {artifact_path}")
    digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
    entry = {"type": artifact_type, "path": artifact_path, "sha256": digest, "status": status, "recorded_at": timestamp()}
    state.setdefault("artifacts", []).append(entry)
    event(state, "artifact_registered", artifact=entry)
    save(path, state)
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("show",):
        p = sub.add_parser(name); p.add_argument("state", type=Path)
    p = sub.add_parser("transition"); p.add_argument("state", type=Path); p.add_argument("--stage", required=True); p.add_argument("--approved-by"); p.add_argument("--note")
    p = sub.add_parser("block"); p.add_argument("state", type=Path); p.add_argument("--reason", required=True)
    p = sub.add_parser("artifact"); p.add_argument("state", type=Path); p.add_argument("--type", required=True); p.add_argument("--path", required=True); p.add_argument("--status", default="draft")
    args = parser.parse_args()
    if args.command == "show":
        result = load(args.state)
    elif args.command == "transition":
        result = transition(args.state, args.stage, args.approved_by, args.note)
    elif args.command == "block":
        result = transition(args.state, "blocked", None, args.reason)
    else:
        result = add_artifact(args.state, args.type, args.path, args.status)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
