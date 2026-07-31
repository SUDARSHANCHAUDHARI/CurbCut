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

Written and linked below = available now. Everything else is **planned for v0.2** and not yet
written — until a cell is a link, the core rules in `CurbCut.md` (which are platform-agnostic) still
apply; there just isn't a component-specific guide yet. **Contributions welcome** — a new guide is a
single Markdown file following the Forms guide's shape.

| Component | web | compose | swiftui |
| :--- | :---: | :---: | :---: |
| **Forms & validation** | [available](web/guide-forms.md) | [available](compose/guide-forms.md) | [available](swiftui/guide-forms.md) |
| **Buttons & controls** | [available](web/guide-buttons.md) | [available](compose/guide-buttons.md) | [available](swiftui/guide-buttons.md) |
| **Modals & dialogs** | [available](web/guide-modals.md) | [available](compose/guide-modals.md) | [available](swiftui/guide-modals.md) |
| Images & icons | planned | planned | planned |
| Live regions / announcements | planned | planned | planned |
