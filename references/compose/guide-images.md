# Compose — Images & Icons
> Scope: contentDescription, decorative vs informative, complex images. TalkBack.

## 🟢 AUTO — contentDescription describes meaning, or is null only when decorative
```kotlin
// informative
Image(painter = chart, contentDescription = "Sales up 12% in Q3")

// decorative — null is correct ONLY when the image adds no information
Image(painter = divider, contentDescription = null)

// interactive icon — describe the ACTION
Icon(Icons.Default.Search, contentDescription = "Search")
```
- **Why:** `contentDescription = null` removes the node from TalkBack. That's right for a pure
  decoration, wrong for anything informative or interactive (`COMPOSE_ICON_NULL_DESC` warns because
  grep can't tell which case you meant).

## 🟡 ASSISTED — function over appearance
For an actionable image, describe the destination/action ("Acme home"), not the picture ("Acme logo").

## 🟡 ASSISTED — complex images
Charts/diagrams need the data available another way — an adjacent text summary, an expandable details
section, or a data table. A one-line `contentDescription` can't carry a chart.

## 🟡 ASSISTED — merge label + icon into one node
```kotlin
Row(Modifier.semantics(mergeDescendants = true) {}) {
    Icon(Icons.Default.Star, contentDescription = null)   // decorative; label comes from the Text
    Text("Favourited")
}
```
- **Why:** merging avoids TalkBack reading a meaningless icon then the label as two stops.

## 🔵 HUMAN — TalkBack pass
Informative images speak their meaning; decorative ones are skipped; icon actions read their action.
The AI requests this and must not claim it ran it.
