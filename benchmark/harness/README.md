# Benchmark Harness

Reproducibility scaffold for the pre-registered methodology. Populated as runs happen.

```
harness/
  outputs/        # raw generations: <model>/<task>/<condition>/run-<n>.html
  axe/            # pinned axe-core runner + per-output JSON results
  checklist/      # deterministic DOM checks (one script per task)
  results.csv     # tidy long-format: model,task,condition,run,axe_critical,axe_serious,checklist_pass
  RESULTS.md      # the write-up, added only after data collection
```

**Status:** empty — no data collected yet. `RESULTS.md` appears only once runs exist, reported
strictly against `../METHODOLOGY.md`. Until then, any efficacy figure quoted anywhere is a
**claim, not a result.**

To run: mount each generation unmodified in a static page, execute the pinned axe-core version and the
per-task checklist, and append one row per generation to `results.csv`. Condition C additionally logs
the number of hook fix-rounds and any residual findings.

## Pipeline (turnkey)
1. **Score** each output through the hook engine:
   `python3 score.py --csv results.csv outputs/`
2. **axe** the rendered outputs and merge `axe_critical`/`axe_serious` columns into `results.csv`
   (see [`run_axe.md`](run_axe.md)).
3. **Aggregate** into the methodology's outcomes:
   `python3 aggregate.py results.csv`
   → medians per condition, zero-critical share, and A→B (context) / B→C (enforcement) deltas.

`score.py`, `aggregate.py`, and `run_axe.md` are the runner. `RESULTS.md` is written only after a full
pre-registered run; [`SMOKE.md`](SMOKE.md) validates the plumbing (not a result).
