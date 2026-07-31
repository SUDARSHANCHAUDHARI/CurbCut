# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/); this project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
