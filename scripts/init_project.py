#!/usr/bin/env python3
"""Initialize a review-gated Inkroom promo project without inventing approvals."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("--project-id", default=None)
    parser.add_argument("--subject", default="Inkroom product")
    parser.add_argument("--production-workflow", default="behind-the-scenes production")
    parser.add_argument("--host", default="XiaoMo")
    parser.add_argument("--platform", default="bilibili")
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument(
        "--generation-mode",
        choices=("manual_external", "authorized_model"),
        default="manual_external",
    )
    parser.add_argument("--force", action="store_true", help="allow creation in a non-empty directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project_dir.resolve()
    if root.exists() and any(root.iterdir()) and not args.force:
        raise SystemExit(f"refusing non-empty project directory: {root} (use --force only after review)")

    project_id = args.project_id or root.name
    for relative in (
        "workflow",
        "seedance/first-frames",
        "seedance/prompts",
        "seedance/returns",
        "seedance/qa",
        "assets",
        "audio",
    ):
        (root / relative).mkdir(parents=True, exist_ok=True)

    state = {
        "project_id": project_id,
        "version": 1,
        "film_subject": args.subject,
        "production_workflow": args.production_workflow,
        "host": args.host,
        "platform": args.platform,
        "aspect_ratio": args.aspect_ratio,
        "generation_mode": args.generation_mode,
        "stage": "intake",
        "status": "awaiting_user",
        "artifacts": [],
        "approvals": [],
        "shots": [],
        "evidence": [],
        "audio": [],
        "blockers": ["product facts are not locked"],
        "release_status": "not_ready",
        "events": [{"event": "initialized", "at": now(), "by": "skill"}],
    }
    facts = {
        "status": "pending",
        "source_checked_at": None,
        "confirmed": [],
        "user_decisions": [],
        "inferences": [],
        "pending": ["current Inkroom product facts and evidence scope"],
        "forbidden_claims": [
            "generated visuals are real Inkroom UI",
            "Seedance or HyperFrames are Inkroom product features",
            "unverified prices, model availability, limits, or API fields",
        ],
    }
    (root / "BRIEF.md").write_text(
        "---\n"
        f"project_id: {project_id}\n"
        f"film_subject: {args.subject}\n"
        f"production_workflow: {args.production_workflow}\n"
        f"host: {args.host}\n"
        f"platform: {args.platform}\n"
        f"aspect_ratio: {args.aspect_ratio}\n"
        f"generation_mode: {args.generation_mode}\n"
        "flow: companion\n"
        "---\n\n"
        "This project is awaiting product-fact review. No copy, generation, or release approval is implied.\n",
        encoding="utf-8",
    )
    write_json(root / "workflow/state.json", state)
    write_json(root / "workflow/PRODUCT_FACTS.json", facts)
    print(json.dumps({"ok": True, "project": str(root), "stage": "intake", "status": "awaiting_user"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
