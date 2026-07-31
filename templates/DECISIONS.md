# CurbCut Decisions Log (Template)

Records choices between **equally-conformant** accessibility options so the AI (and the team) reuse
them instead of re-deriving — or worse, flip-flopping — across turns. Indexed **by pattern**, never
by screen. Copy into your project root as `DECISIONS.md`.

> The AI MUST consult this log before generating a mapped pattern, and append a new entry when it
> resolves a fresh one.

| Pattern | Decision | Rationale | Date |
| :--- | :--- | :--- | :--- |
| Destructive confirmation | `role="alertdialog"` (web) / `AlertDialog` (Compose) / `.alert` (SwiftUI) | interrupts and demands acknowledgement; plain dialog is too passive for data loss | 2026-07-31 |
| Async submit result | polite live region (`role="status"`) | non-interrupting; `role="alert"` reserved for true errors | 2026-07-31 |
| Icon-only actions | visible tooltip **and** accessible name, target 44px | tooltip alone fails touch + SR; name alone fails sighted-motor users | 2026-07-31 |

*Append below. One row per pattern; if a decision changes, update the row and note why in the PR.*
