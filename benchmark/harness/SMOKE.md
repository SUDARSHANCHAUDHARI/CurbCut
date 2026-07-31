# Pipeline Smoke Test — NOT the benchmark result

This validates that the scoring pipeline runs end to end and produces numbers. It is **not** the
pre-registered efficacy result and makes **no efficacy claim**. See [`../METHODOLOGY.md`](../METHODOLOGY.md);
real results require the full protocol (3 models, fresh sessions, axe-core) and appear only in
`RESULTS.md`, which does not yet exist by design.

## What this is
Two **author-written** sample outputs for Task 1 (signup form) — one deliberately naive (`samples/bare/`),
one accessible (`samples/grounded/`) — scored by `score.py`, which reuses the enforcement hook's rule
engine.

## Result (hook-detected AUTO violations only)

| Sample | critical | high | medium | total |
| :--- | :---: | :---: | :---: | :---: |
| `bare/signup.html` | 1 | 5 | 0 | **6** |
| `grounded/signup.html` | 0 | 0 | 0 | **0** |

`bare` findings: `WEB_CLICKABLE_DIV` (submit as a `div`), `WEB_IMG_NO_ALT`, `WEB_OUTLINE_NONE`, and
`WEB_POSITIVE_TABINDEX` ×3.

## Why this is NOT a benchmark number
- **n = 1**, single task, single author — not the pre-registered 81 generations.
- **Samples are hand-written**, not model-generated in fresh sessions; the "bare" case is a
  constructed illustration, so it says nothing about how any model actually behaves.
- **Hook-detectable violations only** — axe-core (the other half of the measurement) was not run here.

## What it does prove
The measurement plumbing works: `score.py` loads the guard engine, walks outputs, and emits per-file
severity counts (and CSV via `--csv`). When real model outputs are dropped into
`outputs/<model>/<task>/<condition>/run-<n>`, the same command produces the study's raw rows.
