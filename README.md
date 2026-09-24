# Inkroom Promo Video Skill

`inkroom-promo-video` is a review-gated Codex workflow for Inkroom product videos.

It coordinates product-fact review, copy, script, storyboard, first frames, Seedance prompts or authorized generation, per-shot returns, HyperFrames assembly, audio/caption QA, preview approval, and local MP4 delivery.

The repository contains workflow instructions, small deterministic helpers, and a sanitized fixture. It does not contain Inkroom credentials, real recordings, generated media, or private project files.

## Install

Copy the `inkroom-promo-video` directory into `~/.codex/skills/`, or install it through your normal Codex skill workflow. Automatic discovery remains enabled; explicit invocation is also available with `$inkroom-promo-video`.

## Boundaries

- Product UI, catalogs, prices, API fields, and account limits require real evidence.
- Seedance may be manual external generation or an explicitly authorized model mode; neither mode skips user approval.
- The workflow ends at an approved preview, rendered MP4, and a local download. It never publishes automatically.

## Local helpers

```bash
python scripts/init_project.py /path/to/project --project-id demo
python scripts/state.py show /path/to/project/workflow/state.json
python scripts/validate_manifest.py --state /path/to/project/workflow/state.json
python scripts/qa_summary.py /path/to/project --json
```

See `references/` for the state machine, evidence policy, shot contract, Seedance review checklist, HyperFrames rules, and release gate.
