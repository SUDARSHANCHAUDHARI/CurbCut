# Benchmark Runbook — execution plan

Step-by-step to produce the first real `RESULTS.md` against the pre-registered
[`METHODOLOGY.md`](METHODOLOGY.md). Follow top to bottom.

## Goal
Measure whether `CurbCut.md` (condition B) and the enforcement hook (condition C) reduce
automatically-detectable accessibility violations in AI-generated UI, vs a bare prompt (condition A).

## Decision at the start — pick scope
| Option | Generations | Your time | Credibility |
| :--- | :---: | :---: | :--- |
| **A. Full** (3 models × 3 tasks × 3 conditions × 3 runs) | 81 | ~2–3h | pre-registered result |
| **B. Claude-only slice** (1 model × 3 × 3 × 3) | 27 | ~1h | legit first data point, labeled partial |

Recommendation: **start with B** (Claude-only) tomorrow — get the pipeline validated on real data and
a publishable slice in ~1h; expand to GPT/Gemini later. Same scripts, same output layout.

## Roles
- **You:** generate outputs (paste prompts into fresh chat sessions, save HTML). Only you can drive
  GPT/Gemini; the generation must be manual per the methodology (fresh session each run).
- **Me (Claude Code):** finish the axe runner + checklist scripts, score, aggregate, write `RESULTS.md`,
  commit. Everything after generation is mine.

---

## Timeline (Claude-only slice ≈ 2h total)

### Block 0 — Prep (me, ~45 min, BEFORE you start generating)
- [ ] Build `harness/checklist.py` — deterministic per-task DOM checks (native control, label assoc,
      modal focus, live region, target size, ARIA soup).
- [ ] Build `harness/serve_and_axe.sh` — serve `outputs/` and run pinned `@axe-core/cli` per file.
- [ ] Pin versions: `npm i -D @axe-core/cli` and record the version.
- [ ] Create the `outputs/` tree skeleton.

### Block 1 — Generate (you, ~1h for the slice)
Output path convention (score.py reads this): `outputs/<model>/<task>/<condition>/run-<n>.html`
- Models: `claude` (slice) → add `gpt`, `gemini` for full.
- Tasks: `form`, `modal`, `table` (prompts verbatim in [`PROMPTS.md`](PROMPTS.md)).
- Conditions per run:
  - **A (bare):** paste the task prompt alone. Save the HTML.
  - **B (grounded):** paste full `CurbCut.md` + "Follow the accessibility rules in CurbCut.md strictly." + the task prompt. Save.
  - **C (enforced):** take the B output, run it through the hook (I'll give you a one-liner), paste the
    findings back with "Fix every reported issue, then re-output the file." Up to 2 rounds. Save final.
- 3 runs each → 27 files. **Fresh session per run** (new chat), default settings, log model version.

### Block 2 — Measure (me, ~20 min, automated)
- [ ] `python3 harness/score.py --csv harness/results.csv outputs/`
- [ ] `bash harness/serve_and_axe.sh` → merge axe columns into `results.csv`
- [ ] `python3 harness/checklist.py outputs/ >> results` (checklist pass/fail)
- [ ] `python3 harness/aggregate.py harness/results.csv`

### Block 3 — Report (me, ~30 min)
- [ ] Write `harness/RESULTS.md`: medians per condition, zero-critical share, A→B (context) and
      B→C (enforcement) deltas, honest limitations. Label "Claude-only slice" if scope B.
- [ ] Commit on a branch → PR → merge. Update the README "Benchmark" line with a one-sentence result.
- [ ] (Optional) update the live site with the headline number.

---

## Definition of done
- `results.csv` has one row per generation with hook + axe + checklist columns.
- `aggregate.py` prints medians and deltas.
- `RESULTS.md` committed, honestly scoped, linked from README.
- If any efficacy number is quoted, it traces to a row in `results.csv`.

## Prereqs to have ready tomorrow
- Node (have it: v22) · `npm i -D @axe-core/cli` (Block 0).
- Access to the model chat UIs you're testing (Claude at minimum).
- ~1h uninterrupted for generation (the only manual part).

## Guardrail
No efficacy figure goes into the repo, site, or a post until it traces to `results.csv`.
Pre-registration integrity: report against `METHODOLOGY.md` exactly; note any deviation.
