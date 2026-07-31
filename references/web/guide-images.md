# Web — Images & Icons
> Scope: informative vs decorative, complex images, icon fonts/SVG, text in images. NVDA/VoiceOver/JAWS.

## 🟢 AUTO — every `<img>` has an `alt` (informative *or* empty)
```html
<img src="chart.png" alt="Sales up 12% in Q3" />   <!-- informative: describe the meaning -->
<img src="divider.png" alt="" />                     <!-- decorative: empty alt hides it -->
```
- **Why:** a missing `alt` (`WEB_IMG_NO_ALT`) makes screen readers fall back to the file name or skip
  silently. `alt=""` is a deliberate signal "this carries no information" — different from *absent*.

## 🟡 ASSISTED — describe function, not appearance
For actionable images (a logo linking home, an icon button), the alt describes the **destination or
action**, not the picture: `alt="Acme home"`, not `alt="Acme logo"`.

## 🟡 ASSISTED — complex images need a long description
Charts, diagrams, and maps need more than a phrase. Provide the data nearby (a table), or link a text
description, or use `aria-describedby` pointing at a fuller explanation. The short `alt` gives the gist;
the long description gives the detail.

## 🟢 AUTO — decorative SVG/icons are hidden
```html
<button aria-label="Search">
  <svg aria-hidden="true" focusable="false"><!-- magnifier --></svg>
</button>
```
- **Why:** an inline decorative SVG announces its guts unless `aria-hidden="true"`; `focusable="false"`
  keeps it out of the tab order in older browsers. The accessible name comes from the button.

## 🟠 HIGH — avoid text baked into images
Text in an image can't be resized, recoloured, translated, or read (SC 1.4.5). Use real text styled
with CSS; reserve images-of-text for logos.

## 🔵 HUMAN — screen-reader pass
Informative images read their meaning; decorative ones are silent; complex images expose their data.
The AI requests this and must not claim it ran it.
