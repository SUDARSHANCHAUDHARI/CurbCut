# Compose — Live Regions & Announcements
> Scope: liveRegion semantics, announcements, toasts/snackbars, async results. TalkBack.

## 🟡 ASSISTED — mark changing content as a live region
```kotlin
Text(
    text = statusMessage,
    modifier = Modifier.semantics { liveRegion = LiveRegionMode.Polite },
)
```
- **Why:** `liveRegion` tells TalkBack to announce the node when its text changes, without moving focus
  — the native equivalent of `aria-live`. `Polite` waits for a pause; `Assertive` interrupts (reserve
  for errors).

## 🟡 ASSISTED — one-shot announcements
For a transient event with no on-screen anchor (e.g. "Copied"), prefer a live region on a visible
element. Where you must fire imperatively:
```kotlin
val view = LocalView.current
view.announceForAccessibility("Copied")   // deprecated in API 36 — prefer liveRegion where possible
```

## 🟡 ASSISTED — Snackbar / toast
`SnackbarHost` content is announced by TalkBack, but auto-dismiss can outrun a screen-reader user —
keep critical results reachable elsewhere too, and give enough duration.

## 🟢 AUTO — validation errors use semantics, not just colour
```kotlin
Modifier.semantics { if (error != null) error(error) }
```
Icon + text + colour together; never colour alone. *(See `guide-forms.md`.)*

## 🔵 HUMAN — TalkBack pass
Async results are announced once, at the right urgency, focus undisturbed.
The AI requests this and must not claim it ran it.
