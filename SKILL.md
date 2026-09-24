---
name: inkroom-promo-video
description: "Run a review-gated Inkroom product-video workflow from product facts and copy through Seedance generation or handoff, per-shot approval, HyperFrames assembly, QA, preview, and MP4 download. Use for Inkroom or XiaoMo promo videos; do not use for generic video editing or automatic publishing."
---

# Inkroom Promo Video

Build a reusable Inkroom product video as a companion workflow. The default recipe is XiaoMo first-person, 16:9 landscape, Seedance-first picture, real recordings for product evidence, and HyperFrames for deterministic assembly. The recipe is configurable; never copy a prior project's duration, shot count, wording, or approval state without reconciling current artifacts.

## Operating contract

- Separate `film_subject=Inkroom product` from `production_workflow=behind-the-scenes production`. Historical meta-video tasks must not become product copy.
- Treat product claims as `confirmed`, `user_decision`, `inference`, or `pending`. Read current product facts and the active handoff before historical README or old task files.
- Generated imagery may explain a concept, but it must not impersonate Inkroom UI, catalogs, API documentation, prices, files, data, logos, or real evidence. Use real recordings for those claims.
- `received` is not `approved`; a placeholder is never an approved take; an approved source is never silently overwritten.
- Every direction-changing gate waits for explicit user confirmation. File existence never advances a gate.
- The default delivery ends at user-approved preview, rendered MP4, and a local download. Never publish automatically.

## Start and resume

1. Locate the project root and read `BRIEF.md`, the active handoff, `workflow/state.json`, the active composition, and the latest QA report. Warn about stale documents instead of treating them as truth.
2. If no state exists, initialize it with `scripts/init_project.py`; do not infer approvals.
3. Resume from the recorded stage. Do not repeat approved work or offer an accepted capability as new.
4. Keep one canonical handoff plus machine-readable state, manifest, asset ledger, and QA report.

## State machine and gates

Use these stages exactly:

`intake -> facts_locked -> outline_review -> copy_review -> script_review -> storyboard_review -> frames_review -> seedance_package_ready -> awaiting_external_returns -> per_shot_received -> per_shot_approved|per_shot_rejected -> assembly_preview -> audio_review -> qa_pass -> user_render_approval -> rendered_downloaded -> publish_ready`

The project may branch back from a rejected shot to its own frame/prompt/generation review. Read [references/workflow-state-machine.md](references/workflow-state-machine.md) before changing state and use `scripts/state.py` for transitions.

## Stage routing

- **Facts and outline:** refresh product facts; use `marketing-skills` as a candidate research aid only. Lock the audience problem and evidence gaps before copy.
- **Copy, script, storyboard:** use the confirmed copy and the complete-action-per-shot rule. `screenwriting-skills` may inform structure, but never import Ottermind-specific content. Read [references/product-evidence-policy.md](references/product-evidence-policy.md).
- **Frames:** use `imagegen` or `image-2` when available, with the approved character sheet and style anchor. Keep frames text-free and landscape.
- **Seedance:** use `seedance1` to turn approved storyboard units into independent prompts and a handoff package. If an authorized video model is available, direct generation is allowed only after user approval; otherwise wait for manual external returns. Read [references/seedance-review-checklist.md](references/seedance-review-checklist.md).
- **Returns:** match by `shot_code` and `take`; inspect each clip independently; approve or reject per shot. Do not repair a failed generation with frozen frames or hidden trimming.
- **Assembly:** use `hyperframes`, `hyperframes-core`, `general-video`, and `hyperframes-cli`. Play each approved Seedance source once from source time zero; overlay captions/fact labels and replace placeholders with real recordings only. Read [references/hyperframes-assembly-rules.md](references/hyperframes-assembly-rules.md).
- **Media:** use `media-use` for voice, BGM, SFX, captions, and provenance. Preview TTS/music must carry a license status.
- **QA and delivery:** run the project validators, `hyperframes check --strict`, snapshots, and FFmpeg/ffprobe checks. Render only after the user approves the preview. Read [references/release-checklist.md](references/release-checklist.md).

## Standard outputs

Each project should produce, as applicable: `BRIEF.md`, `workflow/state.json`, `workflow/PRODUCT_FACTS.json`, `OUTLINE.md`, `COPY.md`, `SCRIPT.md`, `STORYBOARD.md`, `INKROOM_VIDEO_COMPLETE_HANDOFF.md`, `seedance/*manifest.json`, a Seedance ZIP, `ASSET_LEDGER.md`, `QA-REPORT.md`, a Studio preview URL, and the approved MP4 path.

Record each stage's tool, status (`used`, `candidate`, or `blocked`), license, and boundary. Use `scripts/validate_manifest.py` before accepting a package or a returned take.
