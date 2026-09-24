# Handoff and Shot Schema

## Shot record

Each shot has a stable `shot_code` and independent history:

```json
{
  "shot_code": "S05-A",
  "kind": "seedance",
  "status": "received",
  "take": "take01",
  "voiceover": "需要更深接入……",
  "duration_target_s": 5.0,
  "first_frame": "seedance/first-frames/S05-A_first.png",
  "prompt": "seedance/prompts/S05-A.md",
  "return_file": "seedance/returns/S05-A_take01.mp4",
  "approved_source": null,
  "sha256": null,
  "review_findings": []
}
```

`placeholder` is a separate kind and cannot satisfy a `seedance` approval. A new take is additive until explicitly approved; never overwrite the previous approved source silently.

## Package contract

The Seedance package must contain, per generated shot:

- copy and exact time range;
- visual thesis and start/end state;
- prompt and negative constraints;
- first-frame and reference asset names;
- upload order and continuity constraints;
- return filename convention;
- acceptance checklist.

Do not include real product screenshots as generated references unless the user has cleared them for that shot. Do not claim a generation artifact until a real file or authorized model response exists.
