# HyperFrames Assembly Rules

- The root composition owns duration, timing, and one paused deterministic timeline.
- An approved source video appears once, starts at source time zero, and plays continuously. Do not split a complete action merely to follow subtitle changes.
- Captions are an independent overlay track. Caption timing follows measured audio/SRT boundaries, not guessed scene boundaries.
- Real MCP, catalog, and API recordings are explicit placeholders until supplied. Generated footage must never impersonate those screens.
- Exact fact labels may be deterministic HTML overlays when their wording is approved; keep them separate from generated pixels.
- Keep narration, native source audio, BGM, and SFX on separate tracks. Record preview-only voice/music licensing status.
- Use `hyperframes preview` for review, `check --strict` for the gate, and render only after `user_render_approval`.
- Use FFmpeg/ffprobe for source duration, codec, frame rate, freeze, silence, loudness, and final-container checks.

The current project uses HyperFrames. Editly is not a fallback runtime for this workflow; if another renderer is proposed, it must pass a separate compatibility review.
