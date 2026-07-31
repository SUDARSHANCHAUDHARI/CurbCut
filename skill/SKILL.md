---
name: curbcut
description: Enforced accessibility (WCAG 2.2 AA) for AI-generated UI — Compose, SwiftUI, and web. Use when building or reviewing any user interface. Triggers on Compose UI, SwiftUI views, HTML/JSX/TSX, "accessibility", "a11y", "TalkBack", "VoiceOver", "screen reader", "aria", "contentDescription", "focus", "contrast", "WCAG". NOT FOR non-UI logic.
---

# CurbCut — Accessibility Enforcement

Apply the CurbCut standard when generating or reviewing UI. The normative core is
[`CurbCut.md`](../CurbCut.md); the rules there are authoritative. This skill is the short operating
procedure.

## 1. Identify the platform FIRST
Before loading any reference, determine the target: **web** / **Compose** / **SwiftUI**. The core
rules (POUR, profiles, severity, the AI contract) are platform-agnostic; the component guides are
platform-specific. Never emit web idioms (ARIA, CSS px) into Compose or SwiftUI — that is 🔴 CRITICAL.

## 2. Respect the enforcement levels
Every rule is tagged:
- 🟢 **AUTO** — machine-checkable; the CurbCut hook blocks it at write time. Never emit it. Do not
  suppress the rule to get past the hook — fix the code.
- 🟡 **ASSISTED** — apply proactively and explain how it's satisfied.
- 🔵 **HUMAN** — requires a real screen-reader session. Prepare and *request* it; never claim you ran it.

## 3. Lazy-load the right guide
Consult only the guide for the component + platform you're building. All five core components exist
for each platform:

| Component | Guides |
| :--- | :--- |
| Forms & validation | `references/{web,compose,swiftui}/guide-forms.md` |
| Buttons & controls | `references/{web,compose,swiftui}/guide-buttons.md` |
| Modals & dialogs | `references/{web,compose,swiftui}/guide-modals.md` |
| Images & icons | `references/{web,compose,swiftui}/guide-images.md` |
| Live regions | `references/{web,compose,swiftui}/guide-live-regions.md` |

## 4. The reflexes that catch most violations
- Never a clickable `div` / `Box` / `Text` — use the native control.
- Every input has a programmatic label (not placeholder-only).
- Every informative image has a description; decorative ones are explicitly hidden.
- Focus is visible, managed, and restored (modals, SPA routes).
- Dynamic results are announced via a live region — not colour alone.
- No redundant/stale ARIA (no ARIA where native semantics already exist).

## 5. Record decisions
Log choices between equally-conformant options in `templates/DECISIONS.md` (indexed by pattern) and
reuse them. Log accepted deviations in `templates/EXCEPTIONS.md` with owner, approver, issue, expiry.

> Local hook: `enforce/hooks/curbcut-guard.py` (installed at `~/.claude/hooks/curbcut-guard.py`).
> Set `.curbcut.json` `{"mode":"block"}` in a repo to make AUTO violations hard-fail.
