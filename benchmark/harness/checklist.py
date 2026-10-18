#!/usr/bin/env python3
"""
Deterministic per-task DOM checklist — the second measurement in ../METHODOLOGY.md
("Deterministic checklist vs the rendered DOM"). Complements score.py (hook rules)
and the axe-core run (serve_and_axe.sh).

Usage:
    python3 checklist.py <file-or-dir> [...]                  # human table
    python3 checklist.py --csv checklist.csv outputs/         # append CSV rows
    python3 checklist.py --selftest                           # assert on bundled samples

Path convention: outputs/<model>/<task>/<condition>/run-<n>.html
Task also inferred from the filename when the path is not in that layout, so the
SMOKE.md samples score too.

Check families (from METHODOLOGY.md), applied per task:
    native_controls  label_assoc  modal_focus  live_region  target_size  aria_soup

A family can return PASS, FAIL or UNKNOWN. UNKNOWN is excluded from the pass count
rather than counted as a failure — a static parser cannot see computed styles, and
scoring an unknowable check as a failure would manufacture a number. `target_size`
is UNKNOWN unless an explicit px size is declared; axe-core's `target-size` rule
(run by serve_and_axe.sh) is the authority for that criterion.

Stdlib only, Python 3.9+. No rendering: these are static-DOM checks, which is a
documented deviation from "rendered DOM" in METHODOLOGY.md — see RESULTS.md.
"""
from __future__ import annotations

import csv
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PASS, FAIL, UNKNOWN = "PASS", "FAIL", "UNKNOWN"

# Which check families apply to which task. A family not listed is n/a for the task.
TASK_CHECKS = {
    "form": ["native_controls", "label_assoc", "live_region", "target_size", "aria_soup"],
    "modal": ["native_controls", "modal_focus", "target_size", "aria_soup"],
    "table": ["native_controls", "live_region", "target_size", "aria_soup"],
}

# Roles that are already implied by the native element — declaring them is ARIA soup.
REDUNDANT_ROLE = {
    "button": "button", "a": "link", "nav": "navigation", "main": "main",
    "header": "banner", "footer": "contentinfo", "table": "table",
    "ul": "list", "ol": "list", "li": "listitem", "form": "form",
    "h1": "heading", "h2": "heading", "h3": "heading",
    "input": "textbox", "select": "combobox", "textarea": "textbox",
    "dialog": "dialog", "img": "img",
}

LABELLABLE = {"input", "select", "textarea"}
UNLABELLED_INPUT_TYPES = {"hidden", "submit", "button", "reset", "image"}
LIVE_ROLES = {"status", "alert", "log", "progressbar"}
FOCUSABLE_TAGS = {"a", "button", "input", "select", "textarea", "summary"}


class Doc(HTMLParser):
    """Collects the element facts the checks need, plus inline <script>/<style> text."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.elements: list[tuple[str, dict]] = []   # (tag, attrs)
        self.label_wrapped: set[int] = set()         # indices of elements inside a <label>
        self.label_for: set[str] = set()             # ids referenced by <label for=>
        self.script = ""
        self.style = ""
        self._label_depth = 0
        self._capture = None

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if self._label_depth:
            self.label_wrapped.add(len(self.elements))
        self.elements.append((tag, a))
        if tag == "label":
            self._label_depth += 1
            if a.get("for"):
                self.label_for.add(a["for"])
        elif tag in ("script", "style"):
            self._capture = tag

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == "label":
            self._label_depth -= 1
        self._capture = None

    def handle_endtag(self, tag):
        if tag == "label" and self._label_depth:
            self._label_depth -= 1
        if tag == self._capture:
            self._capture = None

    def handle_data(self, data):
        if self._capture == "script":
            self.script += data
        elif self._capture == "style":
            self.style += data

    def find(self, tag):
        return [(i, a) for i, (t, a) in enumerate(self.elements) if t == tag]


def _has(doc: Doc, pred) -> bool:
    return any(pred(t, a) for t, a in doc.elements)


def check_native_controls(doc: Doc, src: str) -> tuple[str, str]:
    """Interactive affordances must be real controls, not divs with handlers."""
    bad = [
        t for t, a in doc.elements
        if t in ("div", "span", "li", "p")
        and ("onclick" in a or a.get("role") == "button" or "tabindex" in a)
    ]
    if bad:
        return FAIL, f"{len(bad)} non-semantic clickable element(s): {sorted(set(bad))}"
    natives = [
        t for t, a in doc.elements
        if t == "button" or (t == "input" and a.get("type", "text") in ("submit", "button"))
        or (t == "a" and a.get("href"))
    ]
    if not natives and re.search(r"addEventListener\(\s*['\"]click", doc.script):
        return FAIL, "click handlers present but no native button/link in the document"
    if not natives:
        return UNKNOWN, "no interactive control found to judge"
    return PASS, f"{len(natives)} native control(s), no div-as-button"


def check_label_assoc(doc: Doc, src: str) -> tuple[str, str]:
    """Every user-visible field needs a programmatic name."""
    missing = []
    checked = 0
    for i, a in [(i, a) for i, (t, a) in enumerate(doc.elements) if t in LABELLABLE]:
        tag = doc.elements[i][0]
        if tag == "input" and a.get("type", "text").lower() in UNLABELLED_INPUT_TYPES:
            continue
        checked += 1
        named = (
            (a.get("id") and a["id"] in doc.label_for)
            or a.get("aria-label")
            or a.get("aria-labelledby")
            or i in doc.label_wrapped
        )
        if not named:
            missing.append(a.get("name") or a.get("id") or f"{tag}#{i}")
    if not checked:
        return UNKNOWN, "no labellable field in the document"
    if missing:
        return FAIL, f"{len(missing)}/{checked} field(s) with no accessible name: {missing}"
    return PASS, f"{checked}/{checked} field(s) labelled"


def check_modal_focus(doc: Doc, src: str) -> tuple[str, str]:
    """focus in + trap + return + Esc. Native <dialog>.showModal() supplies trap and Esc."""
    js = doc.script
    native_dialog = bool(doc.find("dialog")) and "showModal" in js
    sub = {
        "focus-in": native_dialog or ".focus()" in js,
        "trap": native_dialog
        or bool(re.search(r"['\"]Tab['\"]|keyCode\s*===?\s*9", js))
        or _has(doc, lambda t, a: a.get("inert") is not None),
        "return": "activeElement" in js,
        "esc": native_dialog
        or bool(re.search(r"['\"]Esc(ape)?['\"]|keyCode\s*===?\s*27", js)),
    }
    dialogish = native_dialog or _has(
        doc, lambda t, a: a.get("role") == "dialog" or a.get("aria-modal") or t == "dialog"
    )
    if not dialogish:
        return FAIL, "no <dialog>, role=dialog or aria-modal element — confirmation is not a dialog"
    failed = [k for k, v in sub.items() if not v]
    if failed:
        return FAIL, f"dialog present but missing: {', '.join(failed)}"
    return PASS, "dialog with focus-in, trap, return and Esc" + (" (native)" if native_dialog else "")


def check_live_region(doc: Doc, src: str) -> tuple[str, str]:
    """Status and error feedback must be announced, not only painted."""
    hits = [
        a.get("role") or f"aria-live={a.get('aria-live')}"
        for t, a in doc.elements
        if a.get("aria-live") or a.get("role") in LIVE_ROLES
    ]
    if hits:
        return PASS, f"{len(hits)} live region(s): {sorted(set(hits))}"
    return FAIL, "no aria-live or role=status/alert region for dynamic feedback"


def check_target_size(doc: Doc, src: str) -> tuple[str, str]:
    """Static screen only — axe-core's target-size rule is the authority."""
    css = doc.style
    small = []
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if not re.search(r"\b(button|input|a|\[role=[\"']?button)", sel, re.I):
            continue
        for prop, val in re.findall(
            r"\b(min-height|min-width|height|width)\s*:\s*([\d.]+)px", body, re.I
        ):
            if float(val) < 24:
                small.append(f"{sel.strip()} {{{prop}:{val}px}}")
    if small:
        return FAIL, f"declared interactive size below 24px: {small}"
    return UNKNOWN, "no sub-24px size declared; computed size needs axe-core target-size"


def check_aria_soup(doc: Doc, src: str) -> tuple[str, str]:
    """Redundant roles and aria-hidden on focusable content."""
    problems = []
    for t, a in doc.elements:
        role = a.get("role")
        if role and REDUNDANT_ROLE.get(t) == role:
            problems.append(f'<{t} role="{role}">')
        if a.get("aria-hidden") == "true" and (t in FOCUSABLE_TAGS or "tabindex" in a):
            problems.append(f'<{t} aria-hidden="true"> on focusable')
    if problems:
        return FAIL, f"{len(problems)} redundant/conflicting ARIA: {problems[:4]}"
    return PASS, "no redundant role or aria-hidden on focusable content"


CHECKS = {
    "native_controls": check_native_controls,
    "label_assoc": check_label_assoc,
    "modal_focus": check_modal_focus,
    "live_region": check_live_region,
    "target_size": check_target_size,
    "aria_soup": check_aria_soup,
}

# Filename hints used only when the path is not outputs/<model>/<task>/<condition>/.
NAME_HINTS = [("signup", "form"), ("form", "form"), ("modal", "modal"),
              ("dialog", "modal"), ("table", "table")]


def meta_from_path(p: Path) -> tuple[str, str, str, str]:
    parts = p.parts
    try:
        i = parts.index("outputs")
        return parts[i + 1], parts[i + 2], parts[i + 3], p.stem
    except (ValueError, IndexError):
        pass
    low = str(p).lower()
    task = next((t for hint, t in NAME_HINTS if hint in low), "")
    return "", task, "", p.stem


def score_file(p: Path) -> dict:
    src = p.read_text(encoding="utf-8", errors="replace")
    doc = Doc()
    doc.feed(src)
    model, task, condition, run = meta_from_path(p)
    names = TASK_CHECKS.get(task) or sorted(CHECKS)
    results = {n: CHECKS[n](doc, src) for n in names}
    passed = [n for n, (v, _) in results.items() if v == PASS]
    failed = [n for n, (v, _) in results.items() if v == FAIL]
    unknown = [n for n, (v, _) in results.items() if v == UNKNOWN]
    return {
        "model": model, "task": task or "?", "condition": condition, "run": run,
        "file": str(p),
        "checklist_pass": 0 if failed else 1,
        "checks_passed": len(passed),
        "checks_applicable": len(passed) + len(failed),
        "checks_unknown": len(unknown),
        "failed": ";".join(sorted(failed)),
        "_detail": results,
    }


EXTS = {".html", ".htm"}


def gather(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            out += [f for f in sorted(p.rglob("*")) if f.suffix.lower() in EXTS]
        elif p.suffix.lower() in EXTS:
            out.append(p)
    return out


def selftest() -> int:
    """Assert the checks separate the two bundled SMOKE.md samples."""
    base = Path(__file__).resolve().parent / "samples"
    bare, grounded = base / "bare" / "signup.html", base / "grounded" / "signup.html"
    for f in (bare, grounded):
        if not f.exists():
            print(f"selftest: missing sample {f}")
            return 1
    b, g = score_file(bare), score_file(grounded)
    assert b["task"] == g["task"] == "form", (b["task"], g["task"])
    assert b["checklist_pass"] == 0, f"bare sample should fail: {b['failed']!r}"
    assert g["checks_applicable"] > 0, "grounded sample scored no applicable checks"
    assert g["checks_passed"] > b["checks_passed"], (
        f"grounded ({g['checks_passed']}) must pass more than bare ({b['checks_passed']})"
    )
    print(f"selftest OK — bare: {b['checks_passed']}/{b['checks_applicable']} passed, "
          f"failed [{b['failed']}]; grounded: {g['checks_passed']}/{g['checks_applicable']} "
          f"passed, failed [{g['failed'] or '-'}]")
    return 0


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--selftest":
        return selftest()
    csv_path = None
    if argv and argv[0] == "--csv":
        if len(argv) < 2:
            print("--csv needs a path")
            return 1
        csv_path, argv = argv[1], argv[2:]
    if not argv:
        print(__doc__)
        return 1

    files = gather(argv)
    if not files:
        print("No .html files found. Generate Block 1 outputs first (see ../RUNBOOK.md).")
        return 1
    rows = [score_file(p) for p in files]

    if csv_path:
        fields = ["model", "task", "condition", "run", "file", "checklist_pass",
                  "checks_passed", "checks_applicable", "checks_unknown", "failed"]
        exists = Path(csv_path).exists()
        with open(csv_path, "a", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
            if not exists:
                w.writeheader()
            w.writerows(rows)
        print(f"Wrote {len(rows)} row(s) to {csv_path}")
        return 0

    for r in rows:
        unknown_note = f" ({r['checks_unknown']} unknown)" if r["checks_unknown"] else ""
        print(f"\n{r['file']}  [task={r['task']}]  "
              f"{r['checks_passed']}/{r['checks_applicable']} passed{unknown_note}")
        for name, (verdict, why) in r["_detail"].items():
            print(f"  {verdict:<7} {name:<16} {why}")
    npass = sum(r["checklist_pass"] for r in rows)
    print(f"\n{npass}/{len(rows)} file(s) passed every applicable check")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
