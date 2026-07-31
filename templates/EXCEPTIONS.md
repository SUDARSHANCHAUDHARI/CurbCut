# CurbCut Exceptions Log (Template)

Documented, temporary, auditable deviations from a WCAG success criterion. Copy this file into your
project root as `EXCEPTIONS.md`. The hook reads rule IDs disabled here as legitimate — **an inline
`curbcut-disable` without a matching entry here is itself a violation.**

> **Rules**
> 1. An exception is **temporary** and never changes the requirement.
> 2. Every entry has a **risk owner**, an **approver**, a **tracking issue**, and an **expiry date**.
> 3. Scope is the **narrowest practical** — one component/selector, never a whole rule.
> 4. At expiry it is fixed and removed, or consciously renewed. **Never silently suppressed.**
> 5. **AI duty (review mode):** flag any entry past its expiry as 🟠 HIGH technical debt.
> 6. **Never** add this file to `.gitignore` — a risk record hidden from version control protects no one.

---

### EXT-2026-001  <!-- example -->
- **Component / file:** `LegacyChart.tsx` (third-party canvas widget)
- **Rule / SC affected:** `WEB_*` keyboard access · SC 2.1.1 Keyboard (A)
- **Severity (user impact):** 🟠 HIGH
- **Risk owner:** [a person, not a team]
- **Approved by:** [lead / PO / QA]
- **Tracking issue:** [link]
- **What's broken:** the vendor chart is mouse-only; keyboard users cannot read data points.
- **Workaround:** a screen-reader-navigable data table renders the same series below the chart.
- **Expiry (review-by):** 2026-10-01
- **Resolution criterion:** vendor ships keyboard support, or we replace the widget.

---

*Blank copy:*

### EXT-____-___
- **Component / file:**
- **Rule / SC affected:**
- **Severity:**
- **Risk owner:**
- **Approved by:**
- **Tracking issue:**
- **What's broken:**
- **Workaround:**
- **Expiry (review-by):**
- **Resolution criterion:**
