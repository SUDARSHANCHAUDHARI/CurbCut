# CurbCut — Design Spec
> 2026-07-31 · v0.1.0 · status: implemented (v1 skeleton)

## Problem
AI coding agents generate inaccessible UI by default (clickable divs, missing labels, broken focus).
The leading "AI + accessibility context" project, [A11Y.md](https://github.com/fecarrico/A11Y.md), is
**advisory only** — it injects a guideline and trusts the model to comply, ships nothing that enforces,
is web-first with a thin native appendix, and its efficacy benchmark has no published data.

## Goal
A persistent-context standard that is **enforced, native-first, and measured** — filling exactly the
gaps A11Y.md structurally cannot.

## Non-goals (v1)
- Full parity of long-tail component guides (seeded, community-driven).
- Deep static SwiftUI enforcement (not reliably machine-checkable — experimental only).
- Published benchmark numbers (methodology pre-registered; runs are follow-up work).

## Core thesis — the enforcement-level taxonomy
Every rule declares who verifies it: 🟢 **AUTO** (machine → blocks), 🟡 **ASSISTED** (AI → applies +
explains), 🔵 **HUMAN** (person with screen reader → AI may only request). This is the bridge between
AI advice and a CI gate, and the primary differentiator.

## Architecture
1. `CurbCut.md` — platform-agnostic normative core, every rule tagged.
2. `references/{web,compose,swiftui}/` — platform-split guides, real native code.
3. `enforce/` — hook (`curbcut-guard.py`, configurable warn/block), lint packs (eslint/detekt/swiftlint), CI action, tests.
4. `benchmark/` — pre-registered method + Condition C (enforced) to isolate the hook effect.
5. `templates/` — EXCEPTIONS / DECISIONS / REPORT, wired to the hook.

## Key decisions
- **Name:** CurbCut (metaphor: the ramp that helps everyone; no "a11y" in the name, no tool collision).
- **Scope:** all three platforms present; **enforcement fidelity tiers** by what's greppable (web deep, Compose medium, SwiftUI experimental) — stated honestly, not hidden.
- **Hook default `warn`**, `block` opt-in per repo via `.curbcut.json` — never surprise-blocks across unconfigured repos.
- **Only CRITICAL/HIGH block; MEDIUM warns** — grep can't safely disambiguate MEDIUM cases (e.g. decorative vs interactive icon).
- **Attribution:** MIT, credits A11Y.md as inspiration — extension, not clone.

## Verification (done)
- Hook: 4 manual mode tests + `enforce/tests/test_guard.py` (10-rule bad/clean/suppression suite) all pass on Python 3.9.

## Roadmap
Compose/SwiftUI lint depth · native benchmark tasks · run the benchmark · COGA layer · contrast/token
validator · MCP server · `curbcut` skill packaging for the SudarshanTechLabs portfolio.
