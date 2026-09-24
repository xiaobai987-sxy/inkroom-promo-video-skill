# Seedance Review Checklist

## Prompt gate

- The storyboard unit is approved before the prompt is exported.
- The prompt locks a true 16:9 landscape frame when the project is landscape.
- XiaoMo identity, palette, paper/line style, and reference order are explicit.
- One dominant action and a readable end state are described.
- Generated text, fake UI, prices, logos, API fields, and watermarks are prohibited unless the user explicitly requests a non-product concept.
- Sound effects may be requested, but background music is added later in the controlled audio pass.

## Returned take gate

Inspect the actual clip, not only metadata:

1. Identity, framing, palette, and prop continuity.
2. One clear action with no duplicated gesture or competing motion.
3. No fake UI, illegible text, invented numbers, logos, or watermarks.
4. True landscape output, no pillarbox or black bars.
5. Stable end state that can cut to the next shot.
6. No repeated frames or material freeze; verify with FFmpeg.
7. Audio presence and level are recorded separately from visual approval.

Reject only the affected shot. Preserve the failed take and the review reason for later comparison.
