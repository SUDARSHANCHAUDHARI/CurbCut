# Benchmark Harness

Reproducibility scaffold for the pre-registered methodology. Populated as runs happen.

```
harness/
  outputs/            # raw generations: <model>/<task>/<condition>/run-<n>.html
  axe/                # per-output axe JSON + logs, and axe_counts.csv
  score.py            # hook-rule half (reuses enforce/hooks/curbcut-guard.py)
  checklist.py        # deterministic per-task DOM checks
  serve_and_axe.sh    # serves outputs/ and runs the pinned axe-core CLI
  hook_check.sh       # condition C helper: guard in block mode against one file
  aggregate.py        # medians, zero-critical share, A->B and B->C deltas
  results.csv         # tidy long-format: model,task,condition,run,...,axe_*,checklist_pass
  RESULTS.md          # the write-up, added only after data collection
```

**Status:** `outputs/` is an empty skeleton — no generations collected yet. The scripts are built
and smoke-checked (see [`SMOKE.md`](SMOKE.md)); Block 1 of [`../RUNBOOK.md`](../RUNBOOK.md) is
manual and has not been run. `RESULTS.md` appears only once runs exist, reported
strictly against `../METHODOLOGY.md`. Until then, any efficacy figure quoted anywhere is a
**claim, not a result.**

To run: mount each generation unmodified in a static page, execute the pinned axe-core version and the
per-task checklist, and append one row per generation to `results.csv`. Condition C additionally logs
the number of hook fix-rounds and any residual findings.

## Pipeline (turnkey)
Run from this directory, after `npm ci` in the repo root (pins `@axe-core/cli` and `chromedriver`).

1. **Score** each output through the hook engine:
   `python3 score.py --csv results.csv outputs/`
2. **axe** the rendered outputs in headless Chrome:
   `bash serve_and_axe.sh` → `axe/axe_counts.csv` (see [`run_axe.md`](run_axe.md)), then merge its
   `axe_critical`/`axe_serious` columns into `results.csv`.
3. **Checklist** the DOM:
   `python3 checklist.py --csv checklist.csv outputs/` → merge `checklist_pass` into `results.csv`.
4. **Aggregate** into the methodology's outcomes:
   `python3 aggregate.py results.csv`
   → medians per condition, zero-critical share, and A→B (context) / B→C (enforcement) deltas.

`score.py`, `checklist.py`, `serve_and_axe.sh` and `aggregate.py` are the runner. `RESULTS.md` is
written only after a full pre-registered run; [`SMOKE.md`](SMOKE.md) validates the plumbing
(not a result).
