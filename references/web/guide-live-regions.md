# Web — Live Regions & Announcements
> Scope: aria-live, role=status/alert, toasts, async results, politeness. NVDA/VoiceOver/JAWS.

## 🟡 ASSISTED — announce dynamic changes that aren't focus moves
When content updates without the user's focus moving (a toast, a search-result count, an async save),
screen readers don't notice unless a live region tells them.

```html
<!-- present in the DOM BEFORE the update; then change its text -->
<div id="status" role="status" aria-live="polite"></div>
```
```js
document.getElementById('status').textContent = 'Saved.';   // announced politely
```
- **Why:** the live region must exist in the DOM *before* you write to it — injecting the region and
  its text together often isn't announced. `role="status"` implies `aria-live="polite"`.

## 🟡 ASSISTED — polite vs assertive
- `role="status"` / `aria-live="polite"` — waits for a pause. Default for confirmations, counts, saves.
- `role="alert"` / `aria-live="assertive"` — interrupts immediately. Reserve for **errors and urgent**
  messages; overuse makes the UI feel like it's shouting.

## 🟢 AUTO — form errors ride a live region (not colour)
A red border alone is silent and invisible to colour-blind users. Bind the message to the field
(`aria-describedby` + `aria-invalid`) and surface a summary through a `role="status"`/`alert` region.
*(See `guide-forms.md`.)*

## 🟡 ASSISTED — toasts
A toast MUST be in a live region, MUST stay long enough to read (or be dismissible), and MUST NOT be the
only place a critical result appears — auto-dismiss can beat a screen-reader user to it.

## 🔵 HUMAN — screen-reader pass
Each async result is spoken once, at the right urgency, without the user hunting for it.
The AI requests this and must not claim it ran it.
