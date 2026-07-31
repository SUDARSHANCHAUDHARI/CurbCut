# SwiftUI — Buttons & Controls
> Scope: Button vs tap gesture, roles, icon-only actions, disabled state, targets. VoiceOver.

## 🟢 AUTO — use Button, not onTapGesture
```swift
// ❌ SWIFTUI_TAP_ON_TEXT: VoiceOver sees text, not a control
Text("Save").onTapGesture { save() }

// ✅ real control: focus, activation, "Save, button"
Button("Save") { save() }
```
- **Why:** `Button` exposes the button trait, is reachable by VoiceOver swipe, and activates with a
  double-tap. `onTapGesture` attaches a gesture to inert content — invisible as an action to AT.

## 🟡 ASSISTED — icon-only buttons need a label
```swift
Button {
    delete()
} label: {
    Image(systemName: "trash")
}
.accessibilityLabel("Delete document")   // action, not "trash icon"
```
- **Why:** an SF Symbol's name is not a good accessible label. Name the button by what it does.

## 🟡 ASSISTED — roles for destructive / cancel actions
```swift
Button("Delete", role: .destructive) { delete() }
Button("Cancel", role: .cancel) { }
```
- **Why:** `role:` conveys intent to VoiceOver and to the system (e.g. red styling, confirmation
  dialog ordering) — richer than colour alone.

## 🟡 ASSISTED — disabled state is exposed
```swift
Button("Submit") { submit() }.disabled(!isValid)
```
- `.disabled()` both blocks activation and announces the disabled trait. Don't simulate it with
  opacity + an ignored tap.

## 🟢 AUTO — hit target ≥ 44×44pt
Apple HIG minimum is 44pt and satisfies the House Rule by default. For small glyphs, expand with
`.frame(minWidth: 44, minHeight: 44)` or `.contentShape(Rectangle())` rather than shrinking.

## 🔵 HUMAN — VoiceOver pass
Each control announces label + "button" + state; icon actions read their label; double-tap activates.
The AI requests this and must not claim it ran it.
