# SwiftUI — Live Regions & Announcements
> Scope: AccessibilityNotification, announcements, toasts, async results. VoiceOver.

## 🟡 ASSISTED — announce dynamic changes
SwiftUI has no persistent `aria-live` element; you post announcements imperatively when state changes.
```swift
.onChange(of: status) { _, newValue in
    AccessibilityNotification.Announcement(newValue).post()   // iOS 17+
    // pre-iOS 17: UIAccessibility.post(notification: .announcement, argument: newValue)
}
```
- **Why:** the announcement speaks the change without moving VoiceOver focus — the native equivalent
  of a polite live region.

## 🟡 ASSISTED — urgency
Plain announcements are polite. For something that must interrupt, keep it rare (errors); flooding
announcements makes VoiceOver unusable.

## 🟡 ASSISTED — screen-changed vs layout-changed
```swift
UIAccessibility.post(notification: .screenChanged, argument: firstElement)   // major view swap
UIAccessibility.post(notification: .layoutChanged, argument: nil)            // smaller update
```
Use these when a whole region appears (e.g. a results list) so focus lands sensibly.

## 🟡 ASSISTED — toasts
A custom toast overlay is NOT announced automatically — post an announcement when it appears, give it
readable duration, and keep critical results reachable elsewhere.

## 🔵 HUMAN — VoiceOver pass
Async results are announced once, at the right urgency, focus undisturbed.
The AI requests this and must not claim it ran it.
