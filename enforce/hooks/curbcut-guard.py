#!/usr/bin/env python3
"""
CurbCut Guard — a PreToolUse hook that ENFORCES accessibility at write time.

This is the piece an advisory guideline cannot ship. It inspects the code an AI
(or a human) is about to write and blocks the 🟢 AUTO-level anti-patterns defined
in CurbCut.md before they ever land on disk.

Wire it into Claude Code (.claude/settings.json):

    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Write|Edit|MultiEdit",
            "hooks": [
              { "type": "command",
                "command": "python3 /ABS/PATH/CurbCut/enforce/hooks/curbcut-guard.py" }
            ]
          }
        ]
      }
    }

Protocol: reads the tool-call JSON on stdin, decides, and communicates via exit code:
    exit 0            → allow (silent, or warnings printed to stderr)
    exit 2            → BLOCK the write; stderr is shown to the model as the reason

Mode resolution (first hit wins):
    1. env  CURBCUT_MODE = off | warn | block
    2. .curbcut.json  {"mode": "...", "profile": "...", "disable": ["RULE_ID", ...]}
       searched upward from the target file to the repo root
    3. default: "warn"  (never surprise-blocks across unconfigured repos)

Opt-in to blocking per repo by dropping a .curbcut.json with {"mode": "block"}.

Escape hatches (mirroring eslint):
    // curbcut-disable-next-line RULE_ID        (line above the offending line)
    // curbcut-disable RULE_ID                   (whole-file, anywhere)
An honest disable belongs in EXCEPTIONS.md; the hook only checks syntax, not process.
"""
from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

DEFAULT_MODE = "warn"


# --------------------------------------------------------------------------- #
# Rule model
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str      # CRITICAL | HIGH
    line: int          # 1-indexed
    message: str
    fix: str


@dataclass(frozen=True)
class Rule:
    rule_id: str
    severity: str
    exts: tuple[str, ...]
    check: Callable[[str], list[tuple[int, str]]]  # source -> [(line_idx0, snippet)]
    message: str
    fix: str
    sc: str = ""       # WCAG success criterion, for the report


def _line_matches(pattern: re.Pattern[str]) -> Callable[[str], list[tuple[int, str]]]:
    def run(src: str) -> list[tuple[int, str]]:
        out: list[tuple[int, str]] = []
        for i, line in enumerate(src.splitlines()):
            if pattern.search(line):
                out.append((i, line.strip()))
        return out
    return run


# --------------------------------------------------------------------------- #
# Rules  (🟢 AUTO only — everything ASSISTED/HUMAN lives in CurbCut.md, not here)
# --------------------------------------------------------------------------- #
WEB = (".jsx", ".tsx", ".js", ".ts", ".html", ".htm", ".vue", ".svelte")
COMPOSE = (".kt",)
SWIFTUI = (".swift",)

RULES: list[Rule] = [
    # ---- Web ----------------------------------------------------------------
    Rule(
        "WEB_CLICKABLE_DIV", "CRITICAL", WEB,
        _line_matches(re.compile(r"<(div|span|li|p)\b[^>]*\bonClick\b", re.I)),
        "Click handler on a non-interactive element — keyboard users cannot reach it.",
        "Use a native <button> (or <a> for navigation). If truly unavoidable, add "
        'role="button" tabindex="0" and Enter/Space key handlers.',
        "SC 4.1.2 / 2.1.1",
    ),
    Rule(
        "WEB_IMG_NO_ALT", "HIGH", WEB,
        _line_matches(re.compile(r"<img\b(?![^>]*\balt=)[^>]*>", re.I)),
        "<img> without an alt attribute — screen readers announce the file name or nothing.",
        'Add alt="description" for informative images, or alt="" for decorative ones.',
        "SC 1.1.1",
    ),
    Rule(
        "WEB_OUTLINE_NONE", "HIGH", WEB,
        _line_matches(re.compile(r"outline\s*:\s*(none|0)\b", re.I)),
        "Focus outline removed — keyboard users lose all sense of position.",
        "Remove it, or pair it with a visible :focus-visible fallback (≥2px, 3:1 contrast).",
        "SC 2.4.7",
    ),
    Rule(
        "WEB_REDUNDANT_ROLE", "MEDIUM", WEB,
        _line_matches(re.compile(r"<button\b[^>]*\brole=[\"']button[\"']", re.I)),
        'Redundant role="button" on a native <button> — ARIA soup.',
        'Delete role="button"; the element already has button semantics.',
        "SC 4.1.2",
    ),
    Rule(
        "WEB_POSITIVE_TABINDEX", "HIGH", WEB,
        _line_matches(re.compile(r"tabindex\s*=\s*[\"']?\s*[1-9]", re.I)),
        "Positive tabindex hijacks the natural tab order — a frequent keyboard trap.",
        "Use tabindex=\"0\" (in flow) or \"-1\" (programmatic focus); reorder the DOM instead.",
        "SC 2.4.3",
    ),
    Rule(
        "WEB_ANCHOR_NO_HREF", "HIGH", WEB,
        _line_matches(re.compile(r"<a\b(?![^>]*href=)[^>]*\bonClick\b", re.I)),
        "Anchor with a click handler but no href — not keyboard-focusable, wrong role.",
        "Use a <button> for actions; give <a> a real href only for navigation.",
        "SC 2.1.1 / 4.1.2",
    ),
    Rule(
        "WEB_AUTOFOCUS", "MEDIUM", WEB,
        _line_matches(re.compile(r"\bauto[Ff]ocus\b", re.I)),
        "autofocus can disorient screen-reader and magnifier users by moving focus unexpectedly.",
        "Set focus deliberately in response to a user action instead of on load.",
        "SC 2.4.3",
    ),
    # ---- Jetpack Compose ----------------------------------------------------
    Rule(
        "COMPOSE_CLICKABLE_NO_ROLE", "CRITICAL", COMPOSE,
        # matches both .clickable( … ) and .clickable { … }; skips lines that already
        # declare a Role or a semantics block (the common inline fix).
        _line_matches(re.compile(r"\.clickable\s*[({](?![^\n]*(?:Role\.|semantics))", re.I)),
        "Modifier.clickable without a semantics Role — TalkBack cannot announce it as a control.",
        "Prefer a Button. If clickable is required, add "
        "Modifier.semantics { role = Role.Button } and a contentDescription.",
        "SC 4.1.2",
    ),
    Rule(
        "COMPOSE_TEXT_SIZE_DP", "HIGH", COMPOSE,
        _line_matches(re.compile(r"fontSize\s*=\s*\d+\.dp", re.I)),
        "Font size in dp does not scale with the user's system font setting.",
        "Use sp for text: fontSize = 16.sp.",
        "SC 1.4.4",
    ),
    Rule(
        # MEDIUM (warn-only): grep can't tell a decorative icon (null is correct)
        # from an interactive one (null is a bug), so this informs rather than blocks.
        "COMPOSE_ICON_NULL_DESC", "MEDIUM", COMPOSE,
        _line_matches(re.compile(r"contentDescription\s*=\s*null", re.I)),
        "contentDescription = null is silent to TalkBack — correct only for decorative icons.",
        "If this icon is interactive or informative, describe its ACTION "
        "(e.g. \"Delete item\"). Keep null only when a labelled sibling conveys the meaning.",
        "SC 1.1.1",
    ),
    Rule(
        "COMPOSE_EMPTY_DESC", "MEDIUM", COMPOSE,
        _line_matches(re.compile(r"contentDescription\s*=\s*[\"']\s*[\"']")),
        'contentDescription = "" announces nothing but is not marked decorative — likely a bug.',
        "Use null for genuine decoration, or a real action/meaning description otherwise.",
        "SC 1.1.1",
    ),
    # ---- SwiftUI (experimental — greppable subset only) ---------------------
    Rule(
        "SWIFTUI_TAP_ON_TEXT", "HIGH", SWIFTUI,
        _line_matches(re.compile(r"\bText\([^)]*\)\s*\n?\s*\.onTapGesture", re.I)),
        "onTapGesture on Text is invisible to VoiceOver as a control.",
        "Use a Button { } with a Text label instead.",
        "SC 4.1.2",
    ),
    Rule(
        "SWIFTUI_FIXED_FONT", "MEDIUM", SWIFTUI,
        _line_matches(re.compile(r"\.font\(\.system\(size:\s*\d+", re.I)),
        "Fixed system font size opts out of Dynamic Type.",
        "Use a semantic style (.font(.body)) or add .dynamicTypeSize support.",
        "SC 1.4.4",
    ),
]


# --------------------------------------------------------------------------- #
# Config + disable-comment handling
# --------------------------------------------------------------------------- #
def load_config(target: Path) -> dict:
    for folder in [target.parent, *target.parents]:
        cfg = folder / ".curbcut.json"
        if cfg.is_file():
            try:
                return json.loads(cfg.read_text())
            except (json.JSONDecodeError, OSError):
                return {}
        if (folder / ".git").exists():
            break
    return {}


def resolve_mode(cfg: dict) -> str:
    env = os.environ.get("CURBCUT_MODE", "").strip().lower()
    if env in {"off", "warn", "block"}:
        return env
    mode = str(cfg.get("mode", DEFAULT_MODE)).strip().lower()
    return mode if mode in {"off", "warn", "block"} else DEFAULT_MODE


def disabled_ids(src: str, cfg: dict) -> set[str]:
    ids: set[str] = set(cfg.get("disable", []) or [])
    for m in re.finditer(r"curbcut-disable(?:-next-line)?\s+([A-Z0-9_,\s]+)", src):
        ids.update(t.strip() for t in m.group(1).split(",") if t.strip())
    return ids


def suppressed_lines(src: str) -> set[int]:
    """Line numbers (1-indexed) protected by a curbcut-disable-next-line above them."""
    out: set[int] = set()
    for i, line in enumerate(src.splitlines()):
        if "curbcut-disable-next-line" in line:
            out.add(i + 2)  # the line *after* the comment
    return out


# --------------------------------------------------------------------------- #
# Engine
# --------------------------------------------------------------------------- #
def analyze(path: str, src: str, cfg: dict) -> list[Finding]:
    ext = Path(path).suffix.lower()
    off_ids = disabled_ids(src, cfg)
    off_lines = suppressed_lines(src)
    findings: list[Finding] = []
    for rule in RULES:
        if ext not in rule.exts or rule.rule_id in off_ids:
            continue
        for line_idx0, _snippet in rule.check(src):
            if (line_idx0 + 1) in off_lines:
                continue
            findings.append(Finding(
                rule.rule_id, rule.severity, line_idx0 + 1,
                f"{rule.message} ({rule.sc})" if rule.sc else rule.message,
                rule.fix,
            ))
    return findings


def extract_writes(tool_name: str, tool_input: dict) -> list[tuple[str, str]]:
    """Return [(path, content_being_written)] for the supported write tools."""
    path = tool_input.get("file_path") or tool_input.get("path") or ""
    if not path:
        return []
    if tool_name == "Write":
        return [(path, tool_input.get("content", ""))]
    if tool_name == "Edit":
        return [(path, tool_input.get("new_string", ""))]
    if tool_name == "MultiEdit":
        return [(path, "\n".join(e.get("new_string", "")
                                 for e in tool_input.get("edits", [])))]
    return []


def render(findings: list[Finding], path: str, mode: str) -> str:
    verb = "BLOCKED" if mode == "block" else "warning"
    head = f"CurbCut {verb}: {len(findings)} accessibility issue(s) in {Path(path).name}"
    lines = [head, ""]
    for f in sorted(findings, key=lambda x: x.line):
        icon = "🔴" if f.severity == "CRITICAL" else "🟠"
        lines.append(f"  {icon} L{f.line} [{f.rule_id}] {f.message}")
        lines.append(f"      fix: {f.fix}")
    lines.append("")
    if mode == "block":
        lines.append("Fix these before writing. To accept a specific line deliberately, add")
        lines.append("`// curbcut-disable-next-line RULE_ID` and record it in EXCEPTIONS.md.")
    return "\n".join(lines)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # never break the toolchain on malformed input

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}

    all_findings: list[Finding] = []
    mode = DEFAULT_MODE
    target = ""
    for path, content in extract_writes(tool_name, tool_input):
        cfg = load_config(Path(path).resolve())
        mode = resolve_mode(cfg)
        if mode == "off":
            return 0
        found = analyze(path, content, cfg)
        # Blocking only ever triggers on CRITICAL/HIGH; MEDIUM is warn-only.
        if found:
            all_findings.extend(found)
            target = path

    if not all_findings:
        return 0

    blockable = [f for f in all_findings if f.severity in {"CRITICAL", "HIGH"}]
    print(render(all_findings, target, mode), file=sys.stderr)

    if mode == "block" and blockable:
        return 2  # deny the write; stderr becomes the reason shown to the model
    return 0      # warn mode, or only MEDIUM findings: allow


if __name__ == "__main__":
    sys.exit(main())
