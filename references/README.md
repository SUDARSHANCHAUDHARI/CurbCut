# CurbCut Reference Library

Lazy-loaded, platform-split guides. The AI **MUST NOT** preload these — it consults a guide only
when the task involves that component, and **only for the target platform**.

## Enforcement-level legend
Each pattern in a guide is tagged the same way as the core (`CurbCut.md` §1):

- 🟢 **AUTO** — the hook / lint pack blocks it (`enforce/`).
- 🟡 **ASSISTED** — the AI verifies it and explains how.
- 🔵 **HUMAN** — a real screen-reader session must confirm it.

## Platforms

| Platform | Folder | Idioms | Screen reader |
| :--- | :--- | :--- | :--- |
| Web | [`web/`](web/) | HTML, ARIA, CSS px | NVDA, VoiceOver, JAWS |
| Jetpack Compose | [`compose/`](compose/) | `semantics {}`, `sp`/`dp`, `Role` | TalkBack |
| SwiftUI | [`swiftui/`](swiftui/) | `.accessibility*`, Dynamic Type | VoiceOver |

> **Never translate literally across platforms.** ARIA and CSS pixels do not exist in Compose or
> SwiftUI. Read a web guide as *semantic intent*, then emit the native equivalent. Inventing hybrids
> (e.g. `aria-live` in SwiftUI) is 🔴 CRITICAL.

## Component index

All five core components below are available on every platform. Further components (tables, tabs,
carousels, drag-and-drop, autocomplete, tooltips) are the next contribution target — until a
component-specific guide exists, the platform-agnostic core rules in `CurbCut.md` still apply.
**Contributions welcome** — a new guide is a single Markdown file following the Forms guide's shape.

| Component | web | compose | swiftui |
| :--- | :---: | :---: | :---: |
| **Forms & validation** | [available](web/guide-forms.md) | [available](compose/guide-forms.md) | [available](swiftui/guide-forms.md) |
| **Buttons & controls** | [available](web/guide-buttons.md) | [available](compose/guide-buttons.md) | [available](swiftui/guide-buttons.md) |
| **Modals & dialogs** | [available](web/guide-modals.md) | [available](compose/guide-modals.md) | [available](swiftui/guide-modals.md) |
| **Images & icons** | [available](web/guide-images.md) | [available](compose/guide-images.md) | [available](swiftui/guide-images.md) |
| **Live regions / announcements** | [available](web/guide-live-regions.md) | [available](compose/guide-live-regions.md) | [available](swiftui/guide-live-regions.md) |
