# Web — Modals & Dialogs
> Scope: focus movement/trap/restore, labelling, Esc, background inertness. NVDA/VoiceOver/JAWS.

## 🟢 AUTO — prefer the native `<dialog>`
```html
<dialog id="confirm" aria-labelledby="confirm-title">
  <h2 id="confirm-title">Delete this document?</h2>
  <p>This cannot be undone.</p>
  <button value="cancel" formmethod="dialog">Cancel</button>
  <button id="confirm-delete" value="delete">Delete</button>
</dialog>
```
```js
document.getElementById('confirm').showModal();   // moves focus in, makes backdrop inert, Esc closes
```
- **Why:** `showModal()` gives you focus containment, background inertness, and Esc-to-close for free —
  the four modal requirements without hand-rolled JS. `aria-labelledby` names the dialog.

## 🟡 ASSISTED — the four focus rules (if you can't use `<dialog>`)
When a custom `role="dialog" aria-modal="true"` opens:
1. **Save** the element that had focus.
2. **Move** focus into the dialog (title or first control).
3. **Trap** Tab/Shift+Tab within the dialog.
4. **Restore** focus to the saved element on close.
Background content MUST be non-interactive (`inert` attribute) while open.

## 🟢 AUTO — Esc closes; destructive uses alertdialog
- `Escape` MUST close the dialog (native `<dialog>` does this).
- For irreversible confirmations use `role="alertdialog"` with `aria-describedby` pointing at the
  consequence text — it interrupts more assertively than a plain dialog. *(See `DECISIONS.md`.)*

## 🟡 ASSISTED — don't let focus leak
A modal whose trigger keeps focus, or that dumps focus to `<body>` on close, strands keyboard and
screen-reader users. Restoration to the trigger is what keeps their place in the page.

## 🔵 HUMAN — screen-reader pass
Opening announces the dialog name; Tab cycles only inside; Esc closes; focus returns to the trigger.
The AI requests this and must not claim it ran it.
