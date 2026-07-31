# CurbCut Accessibility Report (Template)

One per release or major feature. The AUTO section is filled by tooling; ASSISTED by the AI with
evidence; HUMAN only by a person who ran the session.

- **Feature / release:**
- **Profile:** ⚖️ Standard (AA)
- **Platforms:** web · compose · swiftui
- **Date / reviewer:**

## 🟢 AUTO — tooling (attach output)
- [ ] CurbCut hook scan: **0** CRITICAL/HIGH
- [ ] eslint-jsx-a11y / detekt / SwiftLint: pass
- [ ] axe-core: **__** critical, **__** serious

## 🟡 ASSISTED — AI-verified (describe how)
- [ ] Keyboard/focus order validated end-to-end
- [ ] Dynamic feedback announced via live regions (error + success)
- [ ] Zoom to 200% / reflow at 320px with no loss
- [ ] Colour never the sole signal

## 🔵 HUMAN — screen-reader session (who / when / device)
- [ ] VoiceOver / TalkBack / NVDA task-completion pass
- [ ] Announcement quality and plain language confirmed

## Exceptions
- Open `EXCEPTIONS.md` entries: **__** · expired: **__**

## Verdict
- [ ] Ship  [ ] Ship with logged exceptions  [ ] Blocked
