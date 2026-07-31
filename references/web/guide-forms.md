# Web — Forms & Validation
> Scope: labels, inline errors, focus, and live regions in HTML/JS. NVDA, VoiceOver, and JAWS are the reference screen readers.

## 🟢 AUTO — every input has a programmatic label
```html
<!-- ❌ placeholder is not a label (WEB_* flags this) -->
<input type="email" placeholder="Email" />

<!-- ✅ explicit association -->
<label for="email">Email</label>
<input id="email" type="email" autocomplete="email"
       aria-describedby="email-hint email-err" />
<p id="email-hint">Format: name@example.com</p>
```
- **Why:** `<label for>` (or wrapping the input) gives the field a name every AT reads. Instructions
  go in visible text referenced by `aria-describedby`, never in the placeholder — placeholders vanish
  on input and often fail contrast.

## 🟡 ASSISTED — errors are associated and announced
```html
<input id="email" type="email" aria-invalid="true"
       aria-describedby="email-err" />
<p id="email-err" class="error">
  <svg aria-hidden="true">…</svg> Enter a valid email address.   <!-- icon + text + colour -->
</p>

<!-- one live region per form for the submit-level result -->
<div id="form-status" role="status" aria-live="polite"></div>
```
```js
// on failed submit:
form.querySelector('#form-status').textContent =
  '3 fields need attention.';           // announced by role="status"
firstInvalid.focus();                    // move focus to the first error
```
- **Why:** `aria-invalid` + `aria-describedby` binds the message to the field; `role="status"`
  (polite) announces the summary without stealing focus. Use `role="alert"` only for urgent,
  interrupting messages.

## 🟢 AUTO — don't kill the focus ring
```css
/* ❌ WEB_OUTLINE_NONE */
input:focus { outline: none; }

/* ✅ visible, high-contrast focus */
input:focus-visible { outline: 2px solid; outline-offset: 2px; }  /* ≥2px, 3:1 */
```

## 🟡 ASSISTED — native validation, then enhance
Prefer built-in constraints (`required`, `type="email"`, `pattern`) so the browser's own accessible
messaging works, then layer custom inline errors on top. Never disable the submit button as the only
error signal — it strands keyboard users with no explanation.

## 🔵 HUMAN — screen-reader pass
Tab through with NVDA/VoiceOver: each field speaks label, type, hint, and (when invalid) its error;
the submit summary is announced. The AI MUST request this and may not fabricate the result.
