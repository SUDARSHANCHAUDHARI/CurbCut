#!/usr/bin/env python3
"""
Benchmark aggregator — turns raw per-generation rows into the outcomes defined in
../METHODOLOGY.md. Runs the analysis; it does NOT invent data.

Input CSV columns (produced by score.py, plus axe columns you merge in):
    model,task,condition,run,file,critical,high,medium,total,rules[,axe_critical,axe_serious]

Usage:
    python3 aggregate.py results.csv

Outcomes reported:
  - Primary: median (hook critical+high) per condition, per model.
             If axe columns are present, also median (axe critical+serious).
  - Secondary: share of generations with ZERO critical (hook), per condition.
  - Deltas: A->B (context effect) and B->C (enforcement effect) on the primary median.

Conditions expected: A (bare), B (grounded), C (enforced). Missing cells are skipped,
so a partial run (e.g. one model, some conditions) still aggregates what exists.
"""
from __future__ import annotations

import csv
import statistics
import sys
from collections import defaultdict


def _num(row: dict, key: str) -> int:
    try:
        return int(row.get(key) or 0)
    except (TypeError, ValueError):
        return 0


def load(path: str) -> list[dict]:
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def median(xs: list[int]) -> float:
    return round(statistics.median(xs), 2) if xs else float("nan")


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    rows = load(argv[0])
    if not rows:
        print("empty CSV")
        return 1

    has_axe = any(r.get("axe_critical") for r in rows)

    # key: (model, condition) -> list of severities
    hook_cs: dict[tuple[str, str], list[int]] = defaultdict(list)
    axe_cs: dict[tuple[str, str], list[int]] = defaultdict(list)
    zero_crit: dict[tuple[str, str], list[int]] = defaultdict(list)

    for r in rows:
        k = (r.get("model", ""), r.get("condition", ""))
        hook_cs[k].append(_num(r, "critical") + _num(r, "high"))
        zero_crit[k].append(1 if _num(r, "critical") == 0 else 0)
        if has_axe:
            axe_cs[k].append(_num(r, "axe_critical") + _num(r, "axe_serious"))

    models = sorted({m for m, _ in hook_cs})
    conditions = [c for c in ("A", "B", "C") if any(c == cc for _, cc in hook_cs)]
    conditions += sorted({cc for _, cc in hook_cs} - set(conditions))

    print("Primary — median (hook critical+high) per condition:\n")
    header = f"{'model':<12}" + "".join(f"{c:>8}" for c in conditions)
    print(header)
    print("-" * len(header))
    for m in models:
        cells = "".join(f"{median(hook_cs[(m, c)]):>8}" for c in conditions)
        print(f"{m:<12}{cells}")

    if has_axe:
        print("\nPrimary — median (axe critical+serious) per condition:\n")
        print(header)
        print("-" * len(header))
        for m in models:
            cells = "".join(f"{median(axe_cs[(m, c)]):>8}" for c in conditions)
            print(f"{m:<12}{cells}")

    print("\nSecondary — share of generations with ZERO critical (hook):\n")
    print(header)
    print("-" * len(header))
    for m in models:
        cells = ""
        for c in conditions:
            xs = zero_crit[(m, c)]
            cells += f"{(round(100*sum(xs)/len(xs)) if xs else 0):>7}%"
        print(f"{m:<12}{cells}")

    print("\nDeltas on primary median (lower = better):")
    for m in models:
        a, b, cc = (median(hook_cs[(m, x)]) for x in ("A", "B", "C"))
        def d(x, y):
            return "n/a" if (x != x or y != y) else f"{y - x:+.2f}"
        print(f"  {m}: A->B (context) {d(a, b)}   B->C (enforcement) {d(b, cc)}")

    print("\nNote: this is analysis of whatever rows exist. A published RESULTS.md requires the full")
    print("pre-registered protocol in ../METHODOLOGY.md (3 models, fresh sessions, axe-core).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
