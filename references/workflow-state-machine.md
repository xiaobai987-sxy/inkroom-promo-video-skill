# Workflow State Machine

## State file

`workflow/state.json` is the resumable source of truth. Use `scripts/state.py` for mutations so transitions are explicit and append an audit event.

Minimum shape:

```json
{
  "project_id": "example",
  "version": 1,
  "film_subject": "Inkroom product",
  "production_workflow": "behind-the-scenes production",
  "host": "XiaoMo",
  "platform": "bilibili",
  "aspect_ratio": "16:9",
  "generation_mode": "manual_external",
  "stage": "intake",
  "status": "awaiting_user",
  "artifacts": [],
  "approvals": [],
  "shots": [],
  "evidence": [],
  "audio": [],
  "blockers": [],
  "release_status": "not_ready",
  "events": []
}
```

## Transition rules

- `awaiting_user` requires an explicit approval record before the next review stage.
- `blocked` records the reason and the smallest action that can unblock it.
- `per_shot_received` requires a known `shot_code` and `take`; it never implies approval.
- `per_shot_rejected` may return only that shot to frame/prompt/generation review.
- `qa_pass` is necessary but never sufficient for `user_render_approval`.
- `publish_ready` requires all placeholders replaced, all claims evidenced, all active takes approved, and audio licensing resolved. This skill does not publish.

## Approval record

```json
{
  "gate": "copy_review",
  "decision": "approved",
  "approved_by": "user",
  "at": "2026-01-01T00:00:00Z",
  "notes": "Approved wording; keep first-person XiaoMo voice"
}
```

The implementation must reject an approval without `approved_by`, `at`, and `decision`.
