# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/); this project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-08-01

### Added
- **Complete core reference library:** Buttons, Modals, Images, and Live-regions guides added for all three platforms — the reference set now covers five core components (Forms, Buttons, Modals, Images, Live regions) ×3 (web / Compose / SwiftUI).
- **Three new hook rules:** `WEB_ANCHOR_NO_HREF` (blocks), `WEB_AUTOFOCUS` (warn), `COMPOSE_EMPTY_DESC` (warn). 13 rules total; test suite extended.
- **`curbcut` skill (`skill/SKILL.md`):** auto-invoking operating procedure for accessibility work; installable to `~/.claude/skills/`.
- **Benchmark runner:** `harness/aggregate.py` computes the methodology's outcomes (medians per condition, zero-critical share, A→B / B→C deltas) from `results.csv`. The pipeline (score → axe → aggregate) is now turnkey; `RESULTS.md` still reserved for a full pre-registered run.

### Fixed
- `WEB_AUTOFOCUS` regex corrected to match `autoFocus`/`autofocus` (was missing the `o`).

## [0.1.0] - 2026-07-31

### Added
- **Normative core (`CurbCut.md`):** Principle Zero, POUR, severity model, three compliance profiles, and an 8-point AI Behavior Contract — every rule tagged with an **enforcement level** (🟢 AUTO / 🟡 ASSISTED / 🔵 HUMAN), the project's defining distinction from advisory guidelines.
- **Enforcement hook (`enforce/hooks/curbcut-guard.py`):** a PreToolUse hook that blocks AUTO anti-patterns at write time. Configurable modes (`off`/`warn`/`block`), per-repo `.curbcut.json`, `curbcut-disable` inline escape hatches, and `EXCEPTIONS.md` awareness. 10 rules across web/Compose/SwiftUI. Test suite in `enforce/tests/`.
- **Lint packs (`enforce/rules/`):** eslint-plugin-jsx-a11y config (web, deep), detekt seed (Compose), SwiftLint custom rules (SwiftUI, experimental).
- **CI (`enforce/ci/curbcut.yml`):** GitHub Action running the hook scan + eslint + axe on pull requests.
- **Platform guides (`references/{web,compose,swiftui}/`):** deep Forms & Validation guide per platform with real, idiomatic code; component index with seeded long-tail guides marked help-wanted.
- **Benchmark (`benchmark/`):** pre-registered methodology adapted from A11Y.md, extended with **Condition C (enforced)** to isolate the hook's effect. Prompts fixed verbatim; no data collected yet.
- **Templates (`templates/`):** EXCEPTIONS, DECISIONS, REPORT — wired to the enforcement layer.

### Credits
- Inspired by [A11Y.md](https://github.com/fecarrico/A11Y.md) by Felipe A. Carriço (MIT). CurbCut adds the enforcement layer and native-first depth.

[0.1.0]: https://github.com/SUDARSHANCHAUDHARI/CurbCut/releases/tag/v0.1.0
