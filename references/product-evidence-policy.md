# Product Evidence Policy

## Subject boundary

Every project declares two separate fields:

- `film_subject`: the product or brand the audience is learning about. For this skill, normally `Inkroom product`.
- `production_workflow`: the internal process used to make the video. This may mention Seedance, HyperFrames, GitHub projects, or a local workbench, but it is not product functionality.

Never move facts from `production_workflow` into product copy. Historical files such as `inkroom-formal-agent-task.json`, old MVP handoffs, and old README versions are recovery references only.

## Evidence classes

| Class | Meaning | Allowed in product copy |
| --- | --- | --- |
| `confirmed` | Current official product fact or verified recording | Yes, with the stated scope |
| `user_decision` | Direction explicitly chosen by the user | Yes as creative direction, not as independent proof |
| `inference` | Reasoned interpretation or positioning | Label internally; do not present as a measured fact |
| `pending` | Needs a current recording, catalog check, or approval | No; use a placeholder or neutral wording |

Claims about UI, model availability, prices, points, API fields, account limits, or successful workflows require current evidence. A generated animation may explain the relationship, but cannot stand in for the evidence.

## Stale document handling

At intake, compare the active composition, active handoff, product facts, manifest, and QA report. Mark older README, timing, task, and audio files as stale when their duration, copy, shot IDs, or provider metadata disagree. Preserve them for history; do not silently delete them or use them as active inputs.
