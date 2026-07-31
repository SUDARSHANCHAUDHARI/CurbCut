# SwiftUI — Forms & Validation
> Scope: labels, error announcement, focus, and Dynamic Type in SwiftUI. VoiceOver is the reference screen reader.

## 🟢 AUTO — a field's accessible name is explicit, not the placeholder
`TextField`'s title/prompt is not a reliable VoiceOver label once text is entered.

```swift
// ❌ prompt as the only label
TextField("Email", text: $email)

// ✅ visible label + explicit accessibility label
VStack(alignment: .leading, spacing: 4) {
    Text("Email").font(.subheadline).bold()
    TextField("name@example.com", text: $email)      // format hint
        .textContentType(.emailAddress)
        .keyboardType(.emailAddress)
        .accessibilityLabel("Email")
}
```
- **Why:** the `Text` is the human label; `.accessibilityLabel` fixes the VoiceOver name regardless
  of field contents. Never fold instructions into the prompt alone — they vanish on input.

## 🟡 ASSISTED — announce validation, don't just tint the border
```swift
TextField("name@example.com", text: $email)
    .accessibilityLabel("Email")
    .accessibilityValue(emailError ?? "")            // VoiceOver reads the error with the field
    .overlay(alignment: .bottomLeading) {
        if let emailError {
            Label(emailError, systemImage: "exclamationmark.circle")   // icon + text + colour
                .font(.footnote).foregroundStyle(.red)
                .accessibilityHidden(true)           // avoid double-read; value already carries it
        }
    }

// Form-level result (submit failed):
.onChange(of: submitState) { _, state in
    if case .failed(let message) = state {
        AccessibilityNotification.Announcement(message).post()   // iOS 17+; the aria-live equivalent
    }
}
```
- **Why:** `.accessibilityValue` is VoiceOver's analogue of `aria-describedby` for the error;
  `AccessibilityNotification.Announcement` is the analogue of `aria-live`. The `Label` gives a
  redundant visual (icon + text + colour).

## 🟡 ASSISTED — move VoiceOver focus to the first invalid field
```swift
@AccessibilityFocusState private var focusedField: Field?

.accessibilityFocused($focusedField, equals: .email)
.onChange(of: submitState) { _, state in
    if case .failed = state, emailError != nil { focusedField = .email }
}
```

## 🟢 AUTO — respect Dynamic Type
```swift
Text("Email").font(.subheadline)      // ✅ semantic style scales
// ❌ .font(.system(size: 13))         → COMPOSE/SWIFTUI_FIXED_FONT: opts out of Dynamic Type
```

## 🔵 HUMAN — VoiceOver pass
Rotor to each field: label, value/error, and type are spoken; the submit result is announced without
touch. The AI MUST request this session — it may not claim to have performed it.
