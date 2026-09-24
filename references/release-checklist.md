# Release Checklist

## Preview gate

- Current facts and claims are reconciled.
- Copy, script, storyboard, frame package, and returned takes have explicit approvals.
- No unresolved rejected take is active.
- All placeholders are listed with their replacement requirement.
- Caption text, weight, font loading, and caption-zone layout pass.
- Native audio, narration, BGM, and SFX are audible and balanced.
- `validate_manifest.py`, project validators, and narrative validators pass.
- `hyperframes check --strict --snapshots --at-transitions --frame-check` passes.

## Render gate

- User explicitly approves the Studio preview.
- Render uses the pinned HyperFrames version and a named output path.
- Verify the output exists, is non-empty, and has expected duration, resolution, codec, audio, and sample rate.
- Copy the verified MP4 to `Downloads` without overwriting an earlier user file; report the exact path.

## Publish gate

Publishing is outside this Skill. A project may be marked `publish_ready` only after real recordings, product facts, approved takes, and audio licenses are complete. The Skill must not upload, schedule, or release content automatically.
