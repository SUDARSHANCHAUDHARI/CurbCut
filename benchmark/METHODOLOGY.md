# CurbCut Efficacy Benchmark — Pre-registered Methodology

> **Status:** Pre-registered — published **before** data collection. Results are reported against this
> exactly; any deviation is documented, not hidden.
> **Version:** 1.0 · 2026-07-31
>
> Method adapted, with credit, from the [A11Y.md benchmark](https://github.com/fecarrico/A11Y.md/tree/main/benchmark)
> by Felipe A. Carriço. CurbCut's addition is a **third condition** that measures the enforcement layer,
> not just the context.

## Claim under test
> Injecting `CurbCut.md` as context reduces **automatically detectable** accessibility violations in
> AI-generated UI — and the **enforcement hook** removes a further share the context alone misses.

No claim is made about full accessibility or real assistive-technology usability. Automated tooling
detects an estimated ~30–57% of real barriers; human validation is Phase 2, separately pre-registered.

## Design
- **Models (3):** Claude, Gemini, GPT — default consumer settings, fresh session per run, version logged.
- **Tasks (3):** signup form (inline validation) · destructive-confirmation modal · sortable table with per-row action. Prompts fixed verbatim in [`PROMPTS.md`](PROMPTS.md); they never mention accessibility.
- **Conditions (3):**
  - **A — bare:** task prompt alone.
  - **B — grounded:** identical prompt preceded by full `CurbCut.md` (Standard profile).
  - **C — enforced:** condition B, then every generated file passed through `curbcut-guard.py` in `block` mode; the model is returned the hook's findings and asked to fix, up to 2 rounds. *(This is the condition A11Y.md structurally cannot run.)*
- **Repetitions:** 3 per cell → 3 × 3 × 3 × 3 = **81 generations**.

## Measurement
1. **axe-core (pinned)** over each output in a static harness — violations by impact.
2. **Deterministic checklist** vs the rendered DOM: native control vs clickable div; label association; modal focus in/trap/return + Esc; live-region feedback; ≥24×24px targets; no redundant ARIA.
3. **Secondary:** token footprint per condition; hook rounds needed in C; residual violations after C.

## Analysis
- **Primary:** critical+serious axe violations per generation — median per condition per model.
- **Secondary:** checklist pass-rate; share of generations with **zero** critical violations; **A→B** delta (context effect) vs **B→C** delta (enforcement effect).
- All raw outputs, harness, and scripts published in [`harness/`](harness/). Anyone can re-run it.

## Known limitations (stated up front)
- Automated detection covers only a fraction of barriers — **no conformance claim**.
- Consumer interfaces drift; versions/dates logged per run.
- Author-run; prompts and rubric are public precisely so results can be challenged and reproduced.

## Phase 2 — human validation (planned, not started)
Screen-reader task-completion sessions over the generated outputs, community-recruited, pre-registered here before starting.
