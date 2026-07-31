# Compose — Forms & Validation
> Scope: labels, error announcement, focus, and touch targets in Jetpack Compose. TalkBack is the reference screen reader.

## 🟢 AUTO — labels are programmatic, never placeholder-only
`placeholder` in Compose is the empty-state hint; it disappears on input and is **not** a label.

```kotlin
// ❌ hint used as the only label — vanishes while typing, weak TalkBack name
TextField(value = email, onValueChange = ::onEmail,
    placeholder = { Text("Email") })

// ✅ visible label + the field's accessible name
Column {
    Text("Email", style = MaterialTheme.typography.labelLarge)
    TextField(
        value = email,
        onValueChange = ::onEmail,
        placeholder = { Text("name@example.com") },   // format hint, not the label
        modifier = Modifier.semantics { contentDescription = "Email" },
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
    )
}
```
- **Why:** the visible `Text` is the human label; `contentDescription` (or a `Label` slot on M3
  `OutlinedTextField`) is the TalkBack name. The format lives in the placeholder, where its loss on
  focus is harmless.

## 🟡 ASSISTED — validation errors must be announced, not just coloured
A red border is invisible to TalkBack and to colour-blind users. Bind the error to the field **and**
push it to a live region.

```kotlin
OutlinedTextField(
    value = email,
    onValueChange = ::onEmail,
    isError = emailError != null,
    supportingText = { emailError?.let { Text(it) } },   // read as part of the field
    modifier = Modifier.semantics {
        if (emailError != null) error(emailError)         // TalkBack: "invalid entry"
    },
)

// For a form-level result (submit failed), announce it:
val announce = LocalView.current
LaunchedEffect(submitState) {
    if (submitState is Submit.Failed) {
        announce.announceForAccessibility(submitState.message)  // deprecated API 36+ → prefer liveRegion
    }
}
```
- **Why:** `Modifier.semantics { error(...) }` is the Compose equivalent of `aria-invalid` +
  `aria-describedby`. Icon + text + colour together satisfy "colour is never the only signal."
- **Note (SC 1.4.4):** never set `fontSize` in `dp` — use `sp` so error text scales. *(🟢 AUTO: `COMPOSE_TEXT_SIZE_DP`.)*

## 🟡 ASSISTED — focus the first invalid field on submit
```kotlin
val emailFocus = remember { FocusRequester() }
LaunchedEffect(submitState) {
    if (submitState is Submit.Failed && emailError != null) emailFocus.requestFocus()
}
// …Modifier.focusRequester(emailFocus) on the email field
```

## 🟢 AUTO — touch targets ≥ 24×24dp (design to 48×48dp)
```kotlin
IconButton(onClick = ::clear, modifier = Modifier.size(48.dp)) {   // House†: 48dp
    Icon(Icons.Default.Clear, contentDescription = "Clear email")  // action, not "clear icon"
}
```

## 🔵 HUMAN — TalkBack pass
Swipe through the form with TalkBack on: every field announces its label, type, and error; the submit
result is spoken without touching the screen. The AI MUST request this — it may not claim it ran it.
