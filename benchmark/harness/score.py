#!/usr/bin/env python3
"""
Benchmark scorer — counts CurbCut hook findings across generated output files and
emits a tidy CSV row per file. This is the deterministic half of the measurement
(the `axe-core` half runs separately; see run_axe.md).

Usage:
    python3 score.py <file-or-dir> [<file-or-dir> ...]           # human table
    python3 score.py --csv results.csv outputs/                  # append CSV rows

Path convention (for CSV attribution): outputs/<model>/<task>/<condition>/run-<n>.html
Anything not matching that layout is scored with blank metadata.

Reuses the exact rule engine that enforces at write time, so "what the hook blocks"
and "what the benchmark measures" can never drift apart.
"""
from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

# Load the single source of truth: the guard rule engine.
GUARD = Path(__file__).resolve().parents[2] / "enforce" / "hooks" / "curbcut-guard.py"
_spec = importlib.util.spec_from_file_location("guard", GUARD)
guard = importlib.util.module_from_spec(_spec)
sys.modules["guard"] = guard
_spec.loader.exec_module(guard)

EXTS = {".html", ".htm", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".kt", ".swift"}


def meta_from_path(p: Path) -> tuple[str, str, str, str]:
    """Best-effort (model, task, condition, run) from outputs/<m>/<t>/<c>/run-<n>."""
    parts = p.parts
    try:
        i = parts.index("outputs")
        model, task, condition = parts[i + 1], parts[i + 2], parts[i + 3]
    except (ValueError, IndexError):
        model = task = condition = ""
    return model, task, condition, p.stem


def score_file(p: Path) -> dict:
    src = p.read_text(encoding="utf-8", errors="replace")
    findings = guard.analyze(str(p), src, {})
    crit = sum(1 for f in findings if f.severity == "CRITICAL")
    high = sum(1 for f in findings if f.severity == "HIGH")
    med = sum(1 for f in findings if f.severity == "MEDIUM")
    model, task, condition, run = meta_from_path(p)
    return {
        "model": model, "task": task, "condition": condition, "run": run,
        "file": str(p), "critical": crit, "high": high, "medium": med,
        "total": len(findings),
        "rules": ";".join(sorted({f.rule_id for f in findings})),
    }


def gather(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            out += [f for f in sorted(p.rglob("*")) if f.suffix.lower() in EXTS]
        elif p.suffix.lower() in EXTS:
            out.append(p)
    return out


def main(argv: list[str]) -> int:
    csv_path = None
    if argv and argv[0] == "--csv":
        csv_path, argv = argv[1], argv[2:]
    if not argv:
        print(__doc__)
        return 1

    rows = [score_file(p) for p in gather(argv)]
    if not rows:
        print("No scorable files found.")
        return 1

    if csv_path:
        fields = ["model", "task", "condition", "run", "file",
                  "critical", "high", "medium", "total", "rules"]
        exists = Path(csv_path).exists()
        with open(csv_path, "a", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            if not exists:
                w.writeheader()
            w.writerows(rows)
        print(f"Wrote {len(rows)} row(s) to {csv_path}")
    else:
        print(f"{'file':<44} {'CRIT':>4} {'HIGH':>4} {'MED':>4} {'TOT':>4}")
        print("-" * 66)
        for r in rows:
            print(f"{Path(r['file']).name:<44} {r['critical']:>4} "
                  f"{r['high']:>4} {r['medium']:>4} {r['total']:>4}")
        tot = sum(r["total"] for r in rows)
        print("-" * 66)
        print(f"{len(rows)} file(s), {tot} finding(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
