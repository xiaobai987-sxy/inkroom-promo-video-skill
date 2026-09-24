#!/usr/bin/env python3
"""Produce a compact, read-only status summary for a project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.project.resolve()
    state_path = root / "workflow/state.json"
    if not state_path.is_file():
        raise SystemExit(f"state file not found: {state_path}")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    manifest_path = root / "workflow/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    shots = state.get("shots", [])
    if not shots and isinstance(manifest, dict):
        shots = manifest.get("shots", [])
    counts: dict[str, int] = {}
    for shot in shots:
        status = str(shot.get("status", "unknown"))
        counts[status] = counts.get(status, 0) + 1
    received_missing_files = []
    for shot in shots:
        if shot.get("status") not in {"received", "approved"}:
            continue
        return_file = shot.get("return_file")
        if not return_file or not (root / str(return_file)).is_file():
            received_missing_files.append(str(shot.get("shot_code", "unknown")))
    stale = []
    for name in ("workflow/mvp-handoff.json", "workflow/inkroom-formal-agent-task.json"):
        if (root / name).exists():
            stale.append(name)
    readme = root / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8", errors="replace")
        if "52.7" in text or "v2" in text.lower():
            stale.append("README.md")
    result = {
        "project_id": state.get("project_id"),
        "stage": state.get("stage"),
        "status": state.get("status"),
        "generation_mode": state.get("generation_mode"),
        "shot_counts": counts,
        "manifest_source": "workflow/manifest.json" if manifest_path.is_file() else None,
        "received_missing_files": received_missing_files,
        "artifact_count": len(state.get("artifacts", [])),
        "blockers": state.get("blockers", []),
        "stale_candidates": stale,
        "release_status": state.get("release_status"),
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['project_id']}: {result['stage']} / {result['status']}")
        print(f"shots={result['shot_counts']} artifacts={result['artifact_count']}")
        if result["blockers"]:
            print("blockers:", "; ".join(result["blockers"]))
        if stale:
            print("stale candidates:", ", ".join(stale))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
