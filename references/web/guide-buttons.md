# Web — Buttons & Controls
> Scope: native controls, buttons vs links, icon-only actions, disabled state. NVDA/VoiceOver/JAWS.

## 🟢 AUTO — use the native control, never a clickable box
```html
<!-- ❌ WEB_CLICKABLE_DIV: not focusable, no Enter/Space, no role -->
<div class="btn" onclick="save()">Save</div>

<!-- ✅ free keyboard + focus + semantics -->
<button type="button" onclick="save()">Save</button>
```
- **Why:** `<button>` is focusable, fires on Enter **and** Space, and announces as "Save, button."
  A `div` reproduces none of that. If a design system forces a box, you must add `role="button"`,
  `tabindex="0"`, and key handlers — strictly more code than using the native element.

## 🟢 AUTO — button vs link is semantic, not visual
```html
<button type="button" onclick="openMenu()">Menu</button>   <!-- does something on THIS page -->
<a href="/settings">Settings</a>                            <!-- navigates somewhere -->
```
- **Why:** screen-reader users navigate by role. A link that runs JS and goes nowhere (`href="#"`)
  or a button that navigates both mislead. Match the element to the action.

## 🟡 ASSISTED — icon-only buttons need an accessible name
```html
<button type="button" aria-label="Delete document" onclick="del()">
  <svg aria-hidden="true" focusable="false"><!-- trash icon --></svg>
</button>
```
- **Why:** the icon is hidden from AT (`aria-hidden`), so the button needs `aria-label` (or visually
  hidden text). Name it by the **action** ("Delete document"), not the icon ("trash").

## 🟡 ASSISTED — disabled vs "not yet valid"
Prefer keeping the button enabled and reporting *why* on activation, over `disabled`, which removes the
element from the tab order and gives no explanation. If you must disable, ensure the reason is visible
and programmatically available elsewhere.

## 🟢 AUTO — target size
Interactive controls ≥ 24×24 CSS px (SC 2.5.8); design to 44×44 (House†). For dense inline controls,
expand the **hit area** with padding rather than shrinking the visual.

## 🔵 HUMAN — screen-reader pass
Each control announces role + name + state; icon-only actions read their action; Enter and Space both
activate. The AI requests this — it does not claim to have run it.
