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
