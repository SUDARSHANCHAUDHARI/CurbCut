# CurbCut — Enforced Accessibility Context for AI-Built UIs
> **Version:** 0.1.0 | **Target Standard:** WCAG 2.2 AA · ISO 9241-171 · ADA · EAA | **Last Updated:** 2026-07-31

CurbCut is a persistent context contract that any coding agent (Claude, Cursor, Copilot, Gemini)
**MUST** obey when generating or reviewing user-interface code. Unlike an advisory guideline, every
rule here carries an **enforcement level** that says *who* verifies it — a machine, the AI, or a human —
so the same document drives both the AI's behavior and the CI gate that blocks it.

> **The curb-cut principle:** the ramp cut into a sidewalk was built for wheelchair users and ends up
> serving everyone — strollers, luggage, delivery carts. Accessibility, done at the source, is not a
> cost centre for a minority; it is baseline quality that lifts every user.

---

## 0. Principle Zero — Accessibility is a Pre-condition
- Accessibility is **not** a feature, a polish pass, or an incremental improvement. It is a **pre-condition for use**.
- If a user cannot complete a task because of an accessibility barrier, the feature is **technically broken** — treat it as a functional bug, not a nice-to-have.
- **Task completion** is the primary quality metric, above visual fidelity.

---

## 1. The Enforcement Model — CurbCut's Core Distinction

Every rule in this document is tagged with exactly one enforcement level. This is the mechanism that
turns *advice* into a *gate*. The AI MUST respect the level: it dictates what the AI may claim.

| Level | Meaning | Verified by | The AI's duty |
| :--- | :--- | :--- | :--- |
| 🟢 **AUTO** | Deterministically machine-checkable from source | The CurbCut hook / lint pack / CI (`enforce/`) | Never emit it. If it slips through, the hook **blocks the write**. The AI must not disable the rule to get past it. |
| 🟡 **ASSISTED** | Requires reasoning over intent; not reliably greppable | The AI, at generation time | Apply proactively and **explain** how the rule was satisfied. May not claim more certainty than it has. |
| 🔵 **HUMAN** | Requires a real assistive-technology session | A person with a screen reader | **MUST NOT** claim the test was run, nor fabricate its result. May only prepare and request it. |

> Why this matters: A11Y-style guideline docs mark everything as one undifferentiated "MUST," which
> means nothing is actually enforced — compliance rests entirely on the model choosing to comply.
> CurbCut separates the rules a build can *prove* from the ones only a human can, and ships the tooling
> that proves the first kind.

---

## 2. Severity & Impact Model
Classify every finding by user impact — independent of enforcement level:
- 🔴 **CRITICAL** — Operation failure. Blocks task completion (broken keyboard nav, click on `div`/`span`, modal without focus management). **MUST FIX.**
- 🟠 **HIGH** — Perception/readability failure. Raises error or abandonment rate (insufficient contrast, sub-12px critical text, un-announced dynamic feedback). **MUST FIX.**
- 🟡 **MEDIUM** — Reduces efficiency/satisfaction (missing optional shortcuts, no redundant labels). **SHOULD FIX.**
- 🔵 **LOW** — Cosmetic/polish (micro-interaction labels, refining an already-visible focus ring). **MAY FIX.**

---

## 3. Compliance Profiles
CurbCut defaults to **Standard (AA)**. If the profile is unspecified, the AI MUST ask which to apply.

| Profile | Target | Contrast (text / UI) | Min font† | Min target | Use case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🛡️ **Shield (AAA)** | WCAG AAA | 7:1 / 3:1 (SC 1.4.6, 1.4.11) | 14px† | 44×44 (SC 2.5.5) · 48×48† | Regulated: health, gov, finance |
| ⚖️ **Standard (AA)** | WCAG AA | 4.5:1 / 3:1 (SC 1.4.3, 1.4.11) | 12px† | 24×24 (SC 2.5.8) · 44×44† | **Default.** Production apps, public web |
| 🚀 **Launchpad (A)** | WCAG A | 3:1† house floor | 10px† | 24×24† | MVPs, internal tools, prototypes |

*† = **House Rule** (non-normative CurbCut ergonomics where WCAG requires less). WCAG sets no minimum
font size at any level; Level A defines no contrast or target-size criteria; 44–48px targets come from
Apple HIG / Material. Skipping a **WCAG SC** at your target level → log in `EXCEPTIONS.md`. Relaxing a
**House Rule** → record in `DECISIONS.md`.*

> ⚠️ **Launchpad never relaxes CRITICAL (🟢 AUTO) rules.** Keyboard operability, focus management, and
> semantic structure are Level A — mandatory at every profile.

---

## 4. AI Behavior Contract
Any AI generating or reviewing UI in a CurbCut project **MUST**:

- 🟡 **No Inference** — never assert accessibility without direct evidence in the code or spec.
- 🟢 **Respect the hook** — if `enforce/` blocks a write, **fix the code**, never suppress the rule or route the write through a shell to bypass the hook. A suppression without an `EXCEPTIONS.md` entry is itself a violation.
- 🟡 **Platform first** — identify the target platform **before** loading any reference. The normative layer (§0–§4) is platform-agnostic; the guides in `references/` are split by platform. Never emit web idioms (ARIA, CSS px) into Compose or SwiftUI — that is 🔴 CRITICAL. *See `references/{web,compose,swiftui}/`.*
- 🟡 **Lazy loading** — do **not** preload `references/`. Consult a guide only when the task involves that component. If the folder isn't local, resolve links against upstream: `https://github.com/SUDARSHANCHAUDHARI/CurbCut/tree/main/`.
- 🟢 **Component interrogation** — before adding a click handler (`onClick`, `Modifier.clickable`, `.onTapGesture`) to a non-semantic element, propose the native control instead. This is the single most common AI anti-pattern and is AUTO-enforced.
- 🟡 **Component reuse** — check for an existing implementation in the project/design system and extend it. A parallel re-implementation of an existing pattern is a violation.
- 🟡 **Decision memory** — record choices between equally-conformant options (e.g. `alertdialog` vs `dialog`) in `DECISIONS.md`, indexed by pattern, and reuse them. *See `templates/DECISIONS.md`.*
- 🟡 **Explain trade-offs** — when suggesting a change, state its impact on Accessibility vs UX vs Business.
- 🔵 **Never fake a human test** — for any 🔵 HUMAN rule, prepare the expected behavior and *request* validation. Claiming a screen-reader pass you did not run is a hard breach of this contract.
- 🟡 **Mode awareness** — generating new code: apply all rules proactively. Reviewing existing code: classify by §2 severity and propose targeted fixes, not full rewrites unless damage is CRITICAL. Honor `EXCEPTIONS.md`; flag any entry past its expiry as 🟠 HIGH debt.

---

## 5. Technical Standards (POUR) — with enforcement levels

### Perceivable
- 🟢 **Alt text (SC 1.1.1)** — informative images MUST carry a functional description (`alt`, `contentDescription`, `.accessibilityLabel`). Decorative images MUST be explicitly empty/hidden. *Guides: web/compose/swiftui `guide-images.md`.*
- 🟢 **Color is never the only signal** — state MUST use **icon + text + color**, not color alone.
- 🟡 **Contrast (SC 1.4.3, 1.4.11)** — text ≥ 4.5:1, UI/meaningful graphics ≥ 3:1. Prefer real luminance difference over hue. *ASSISTED because contrast depends on rendered values the source may not expose; the `contrast` check in `enforce/` covers literal color pairs only.*

### Operable
- 🟢 **Semantic controls (SC 4.1.2)** — use the native control (`<button>`, Compose `Button`, SwiftUI `Button`). Click handlers on `div`/`span`/`Box`/`VStack` without a button role are AUTO-blocked.
- 🟢 **Focus not suppressed (SC 2.4.7)** — `outline: none` / `outline: 0` without an equivalent visible fallback is AUTO-blocked on web.
- 🟡 **Keyboard (SC 2.1.1)** — 100% of function operable without a pointer; pair pointer listeners with keyboard equivalents.
- 🟡 **Focus management (SC 2.4.11)** — focus visible, never obscured by sticky content; after SPA route changes, reset focus (to H1 or top); modals move focus in, trap it, and restore it on close.
- 🟢 **Target size (SC 2.5.8)** — interactive targets ≥ 24×24 CSS px (House†: design to 44×44). Literal undersized sizes are flagged.
- 🟡 **Reduced motion (SC 2.3.3†)** — respect `prefers-reduced-motion` / `accessibilityReduceMotion` / system animator scale.

### Understandable
- 🟢 **Labels (SC 1.3.1, 3.3.2)** — every input MUST have a programmatically-associated label (`<label for>`, wrapping, `contentDescription`, `.accessibilityLabel`). Placeholder-as-only-label is AUTO-flagged.
- 🟡 **Dynamic feedback (SC 4.1.3)** — toasts, async results, and validation MUST be announced via a live region (`aria-live` / `role=status|alert`, Compose `liveRegion`, SwiftUI announcement API).
- 🔵 **Plain language & announcement quality** — label text and announcements MUST be understandable to a screen-reader user in context. HUMAN-verified.

### Robust
- 🟢 **No ARIA soup** — no ARIA where native HTML already provides the semantics; no redundant roles (`role="button"` on `<button>`); no static never-updated ARIA state (hardcoded `aria-expanded`). AUTO-flagged. *(Field data: WebAIM Million 2026 — pages average 133+ ARIA attributes, 6× the 2019 figure, more ARIA correlating with more errors.)*
- 🟡 **Interoperability (ISO 9241-171)** — compatible with current assistive technologies.

---

## 6. Anti-patterns (never generate)
- 🟢 **Clickable non-controls** — `<div onClick>`, `Modifier.clickable` on a `Box`, `.onTapGesture` on a `Text`, used as buttons. Use the native control; if truly unavoidable, replicate full button semantics (role, focusability, Enter/Space).
- 🟡 **Leaked focus traps** — modals that don't move focus in, contain it, and restore it on close.
- 🟢 **Placeholder-only labels** — `placeholder` (or a hint with no label) as the sole field label.
- 🟢 **ARIA soup** — decorative/redundant/stale ARIA (see §5 Robust).
- 🟡 **Reinventing the complex wheel** — hand-rolled comboboxes/datepickers/treeviews instead of a vetted accessible primitive (Headless UI, Compose/SwiftUI platform components).

---

## 7. Verification Workflow (Definition of Done)
- [ ] 🟢 **AUTO gate green** — CurbCut hook + lint pack + axe pass with no CRITICAL/HIGH (`enforce/`).
- [ ] 🟡 **Tab order** — keyboard path validated end to end; no dead-ends.
- [ ] 🟡 **Dynamic flows** — error and success states announced via live regions, mouse-free.
- [ ] 🟡 **Zoom & reflow** — text resizes to 200% (SC 1.4.4); reflows at 320 CSS px / 400% (SC 1.4.10) with no 2-D scroll.
- [ ] 🔵 **Screen-reader pass** — VoiceOver / TalkBack / NVDA session requested and logged (human).
- [ ] 🟡 **Exceptions audit** — every active `EXCEPTIONS.md` entry has an owner, approver, issue, and unexpired review date.

---

### 📚 Reference & Templates
**Guides by platform:** [`references/web/`](references/web/) · [`references/compose/`](references/compose/) · [`references/swiftui/`](references/swiftui/) — see [`references/README.md`](references/README.md) for the full index and enforcement-level legend.
**Enforcement:** [`enforce/`](enforce/) — hook, lint packs, CI. **Proof:** [`benchmark/`](benchmark/).
**Templates:** [Exceptions](templates/EXCEPTIONS.md) · [Decisions](templates/DECISIONS.md) · [Report](templates/REPORT.md).
**External standards:** [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/) · [WCAG 2.2](https://www.w3.org/TR/WCAG22/) · [WCAG2ICT](https://www.w3.org/TR/wcag2ict-22/) · [Deque axe-core](https://github.com/dequelabs/axe-core).

*Inspired by the [A11Y.md](https://github.com/fecarrico/A11Y.md) project by Felipe A. Carriço. CurbCut extends the persistent-context idea with an enforcement layer and native-first depth.*
