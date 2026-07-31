# Compose — Buttons & Controls
> Scope: Button vs clickable, roles, icon-only actions, disabled state, targets. TalkBack.

## 🟢 AUTO — prefer Button; clickable needs a Role
```kotlin
// ❌ COMPOSE_CLICKABLE_NO_ROLE: TalkBack reads content but not "button"
Box(Modifier.clickable { save() }) { Text("Save") }

// ✅ semantics + focus + activation for free
Button(onClick = ::save) { Text("Save") }

// ✅ if a custom surface is truly needed, declare the role
Surface(
    modifier = Modifier
        .clickable(onClickLabel = "Save") { save() }
        .semantics { role = Role.Button },
) { Text("Save") }
```
- **Why:** `Button` ships the `Role.Button` semantics, focusability, and D-pad/keyboard activation.
  Raw `clickable` announces the label but not that it *is* a control. `onClickLabel` gives TalkBack a
  verb ("double-tap to Save").

## 🟡 ASSISTED — icon-only buttons carry an action description
```kotlin
IconButton(onClick = ::delete) {
    Icon(Icons.Default.Delete, contentDescription = "Delete document")  // action, not "trash"
}
```
- **Why:** an `Icon` with `contentDescription = null` is silent; on an interactive control that is a
  bug (`COMPOSE_ICON_NULL_DESC` warns). Describe what it does.

## 🟡 ASSISTED — disabled state is exposed automatically
```kotlin
Button(onClick = ::submit, enabled = isValid) { Text("Submit") }
```
- `enabled = false` disables activation **and** exposes the disabled state to TalkBack. Don't fake it
  with alpha + an ignored click — that lies to assistive tech.

## 🟢 AUTO — touch targets ≥ 24dp (design 48dp)
`IconButton` defaults to 48dp. For custom controls under 48dp, expand with
`Modifier.minimumInteractiveComponentSize()` or padding — never shrink below the 24dp floor.

## 🔵 HUMAN — TalkBack pass
Each control announces label + "button" + state; icon actions read their description; double-tap
activates. The AI requests this and must not claim it ran it.
