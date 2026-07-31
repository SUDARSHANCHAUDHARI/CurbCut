# SwiftUI — Modals & Dialogs
> Scope: sheet/alert/confirmationDialog, focus scoping, labelling, destructive roles. VoiceOver.

## 🟢 AUTO — use the platform presentations, which scope focus
```swift
// Destructive confirmation — confirmationDialog / alert scope VoiceOver automatically:
.confirmationDialog("Delete this document?",
                    isPresented: $showConfirm, titleVisibility: .visible) {
    Button("Delete", role: .destructive) { delete() }
    Button("Cancel", role: .cancel) { }
} message: {
    Text("This cannot be undone.")
}

// General modal content:
.sheet(isPresented: $showEditor) { EditorView() }   // routes focus into the sheet, returns on dismiss
```
- **Why:** `.sheet`, `.alert`, and `.confirmationDialog` present as system surfaces that move VoiceOver
  focus into the modal and restore it on dismiss — the native equivalent of a focus trap + restore.
  Don't simulate a modal with a `ZStack` overlay; that leaves the background swipeable.

## 🟡 ASSISTED — label and describe
Provide a visible title (`titleVisibility: .visible`) and a `message` for consequences. For custom
sheet content, mark the heading with `.accessibilityAddTraits(.isHeader)` and ensure VoiceOver lands
on it first (`.accessibilityFocused`).

## 🟡 ASSISTED — roles carry intent
`role: .destructive` / `role: .cancel` tell VoiceOver and the system how to treat each action
(styling, placement, escape behavior) — clearer than colour alone. Record the chosen pattern in
`DECISIONS.md`.

## 🟢 AUTO — don't fake a modal with a ZStack overlay
A manual overlay does not scope focus; VoiceOver can reach the content behind it. Use `.sheet` /
`.fullScreenCover` / `.alert`, or contain focus and mark the background inert explicitly.

## 🔵 HUMAN — VoiceOver pass
Presenting moves focus into the modal and announces its title; swiping stays inside; dismiss returns
focus to the trigger. The AI requests this and must not claim it ran it.
