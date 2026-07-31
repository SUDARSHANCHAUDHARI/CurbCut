# SwiftUI — Images & Icons
> Scope: accessibilityLabel, decorative vs informative, SF Symbols, complex images. VoiceOver.

## 🟢 AUTO — label informative images; hide decorative ones
```swift
// informative
Image("chart").accessibilityLabel("Sales up 12% in Q3")

// decorative — remove from the accessibility tree
Image("divider").accessibilityHidden(true)

// SF Symbol used decoratively next to a label
Label("Favourited", systemImage: "star.fill")   // Label pairs text + symbol correctly
```
- **Why:** a bare `Image` may expose its asset name to VoiceOver. Give informative images a label;
  mark decoration `.accessibilityHidden(true)` so it isn't announced.

## 🟡 ASSISTED — describe function, not appearance
For an actionable image, label the action/destination ("Acme home"), not the artwork ("Acme logo").

## 🟡 ASSISTED — decorative SF Symbols inside a labelled control
```swift
Button { save() } label: {
    Image(systemName: "square.and.arrow.down")
}
.accessibilityLabel("Save")   // the symbol itself needs no separate label
```

## 🟡 ASSISTED — complex images
Charts/diagrams need their data another way — an adjacent summary, a details disclosure, or use
`.accessibilityChartDescriptor` (Swift Charts) to expose values to VoiceOver's audio graph.

## 🔵 HUMAN — VoiceOver pass
Informative images speak their meaning; decorative ones are skipped; icon actions read their action.
The AI requests this and must not claim it ran it.
