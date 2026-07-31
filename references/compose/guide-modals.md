# Compose — Modals & Dialogs
> Scope: Dialog/AlertDialog, focus scoping, labelling, dismissal, destructive confirmation. TalkBack.

## 🟢 AUTO — use Dialog / AlertDialog, which scope focus for you
```kotlin
if (showConfirm) {
    AlertDialog(
        onDismissRequest = { showConfirm = false },     // back gesture / scrim tap dismisses
        title = { Text("Delete this document?") },
        text = { Text("This cannot be undone.") },
        confirmButton = { TextButton(onClick = ::delete) { Text("Delete") } },
        dismissButton = { TextButton(onClick = { showConfirm = false }) { Text("Cancel") } },
    )
}
```
- **Why:** `Dialog`/`AlertDialog` create a new window that scopes TalkBack focus to the dialog content
  and returns it on dismiss — the platform equivalent of a focus trap + restore. Don't rebuild a modal
  as a full-screen `Box` overlay; that leaves the background reachable.

## 🟡 ASSISTED — label and describe
`title` + `text` become the dialog's accessible name and description automatically. For a custom
`Dialog {}`, add a heading (`Modifier.semantics { heading() }`) and ensure the first meaningful element
is what TalkBack lands on.

## 🟡 ASSISTED — destructive confirmation
Use `AlertDialog` for irreversible actions and order the buttons so the safe choice (Cancel) is
reachable first. Record the pattern once in `DECISIONS.md` and reuse it.

## 🟢 AUTO — don't fake a modal with a Box
A `Box` overlay with a scrim does **not** scope focus — TalkBack can still swipe into the content
behind it. Use a real `Dialog`, or apply focus/semantics containment explicitly.

## 🔵 HUMAN — TalkBack pass
Opening moves focus into the dialog and announces its title; swiping stays inside; back dismisses and
focus returns to the trigger. The AI requests this and must not claim it ran it.
