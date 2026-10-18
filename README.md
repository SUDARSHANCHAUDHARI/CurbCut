<div align="center">
  <h1>CurbCut</h1>
  <p><b>Enforced accessibility context for AI-built UIs.</b></p>

  <p>
    <img src="https://img.shields.io/badge/WCAG-2.2_AA-blue.svg" alt="WCAG 2.2 AA" />
    <img src="https://img.shields.io/badge/Compliance-ADA_%7C_EAA-success.svg" alt="ADA / EAA" />
    <img src="https://img.shields.io/badge/Native-Compose_%7C_SwiftUI-orange.svg" alt="Native first" />
    <img src="https://img.shields.io/badge/Enforcement-hook_%7C_lint_%7C_CI-D97757.svg" alt="Enforced" />
  </p>
</div>

> Most "AI + accessibility" projects hand the model a guideline and hope it complies.
> **CurbCut ships the guideline _and_ the gate that blocks the model when it doesn't.**

Point your coding agent at `CurbCut.md` and it generates accessible UI from the first line.
Install the hook and CI pack, and any anti-pattern the model still slips through gets
**blocked before it lands** — the same rules, machine-enforced.

---

## Table of Contents

- [Why "CurbCut"?](#why-curbcut)
- [What makes it different](#what-makes-it-different)
- [Quick start (under 2 minutes)](#quick-start-under-2-minutes)
- [What's in the box](#whats-in-the-box)
- [Enforcement fidelity (stated honestly)](#enforcement-fidelity-stated-honestly)
- [Roadmap](#roadmap)
- [Credits & license](#credits--license)
- [About](#about)

## Why "CurbCut"?

The curb cut — the little ramp where a sidewalk meets the road — was built for wheelchair
users. It turned out to help everyone: strollers, luggage, delivery carts, cyclists. That's
the whole thesis: **accessibility done at the source is baseline quality that lifts every user**,
not a favor to a minority.

---

## What makes it different

CurbCut is built around one idea a plain guideline can't express — **every rule declares who verifies it:**

| Level | Verified by | Example | What happens |
| :--- | :--- | :--- | :--- |
| 🟢 **AUTO** | The hook / lint / CI | clickable `<div>`, missing `alt`, `outline:none` | **Write is blocked** |
| 🟡 **ASSISTED** | The AI, at generation | focus order, live-region correctness | AI must apply + explain |
| 🔵 **HUMAN** | A real screen-reader session | announcement quality, plain language | AI may only *request* it |

That split is the bridge between *AI advice* and *CI gate*. Advisory docs mark everything a
flat "MUST" — so nothing is actually enforced. CurbCut proves what a build can prove and is
honest about what only a person can.

---

## Quick start (under 2 minutes)

**1. Point your agent at the standard.** Add one rule to `CLAUDE.md` / `.cursorrules` / `AGENTS.md`:

> *"When building UI, follow the accessibility rules in CurbCut.md strictly, and identify the
> target platform (web / Compose / SwiftUI) before loading any reference:
> https://github.com/SUDARSHANCHAUDHARI/CurbCut/blob/main/CurbCut.md"*

> **v0.1 scope, stated plainly:** web enforcement (hook + eslint + axe) is reliable today; Compose is
> partial; SwiftUI is experimental (it isn't reliably static-checkable). Component guides cover the
> five core components — **Forms, Buttons, Modals, Images, Live regions** — end-to-end on all three platforms.

**2. Turn on enforcement (optional but it's the point).** Register the hook in `.claude/settings.json`
(see [`enforce/hooks/`](enforce/hooks/curbcut-guard.py)) and drop a `.curbcut.json` in your repo:

```json
{ "mode": "block", "profile": "standard" }
```

`mode`: `off` · `warn` (default, never surprise-blocks) · `block`. Opt a repo into hard-blocking
by setting `"block"`; leave it out and unconfigured repos only ever warn.

**3. Wire CI.** Copy [`enforce/ci/curbcut.yml`](enforce/ci/curbcut.yml) — it runs axe + the lint
packs on every PR.

---

## What's in the box

```
CurbCut.md              ← the normative core; every rule tagged AUTO/ASSISTED/HUMAN
references/
  web/  compose/  swiftui/   ← platform guides (real code, not a translation table)
enforce/
  hooks/curbcut-guard.py     ← PreToolUse hook: blocks AUTO anti-patterns at write time
  rules/{eslint,detekt,swiftlint}/   ← shippable lint configs
  ci/curbcut.yml             ← GitHub Action (axe + lint)
benchmark/               ← pre-registered method + published bare-vs-grounded numbers
templates/               ← EXCEPTIONS · DECISIONS · REPORT (wired into the hook)
```

## Enforcement fidelity (stated honestly)

Depth tiers by what's actually machine-checkable — that's physics, not a shortcut. JSX greps
cleanly; SwiftUI barely does.

| | Guides | Hook block | Lint pack |
| :--- | :---: | :---: | :---: |
| **Web** | deep | ✅ | ✅ eslint |
| **Compose** | deep | ⚠️ core rules | ⚠️ detekt seed |
| **SwiftUI** | deep | 🔬 experimental | 🔬 seed |

Guidance is full-depth on all three; *automatic blocking* is honest about where it's reliable.

---

## Roadmap

- [ ] Complete Compose & SwiftUI lint rule coverage
- [ ] Native benchmark tasks (currently web-only)
- [ ] First-class cognitive / plain-language layer (COGA)
- [ ] Contrast + design-token validator
- [ ] MCP server for on-demand guide loading

---

## Credits & license

Inspired by [**A11Y.md**](https://github.com/fecarrico/A11Y.md) by Felipe A. Carriço — CurbCut
extends its persistent-context idea with an enforcement layer and native-first depth. MIT licensed.
Contributions to the reference guides and lint packs are very welcome.

<div align="center"><sub>Built by <a href="https://github.com/SUDARSHANCHAUDHARI">SudarshanTechLabs</a></sub></div>

---

## About

I'm Sudarshan Chaudhari, a Senior Quality Engineer, Test Automation specialist, and AI systems builder based in Bangkok, Thailand.

I have 13+ years of experience in software quality engineering, working across SaaS, fintech, gaming, web, mobile, cloud, and digital signage platforms. My background combines hands-on test automation with QA leadership, test strategy, CI/CD, release quality, production investigation, and cross-platform validation.

Alongside my professional QA career, I run [SudarshanTechLabs](https://sudarshantechlabs.com/), my independent engineering and product lab where I design, build, test, and ship software across Android, web, AI, cybersecurity, developer tooling, and cross-platform applications.

### What I work on

- ⚙️ **Quality Engineering & Test Automation** — Playwright, Selenium, Cypress, Appium, API testing, automation frameworks, end-to-end testing, CI/CD, release gates, GitHub Actions, risk-based testing, and production validation
- 🤖 **AI Systems & Automation** — AI agents, multi-agent orchestration, MCP servers, AI-assisted QA, prompt tooling, developer workflows, automation systems, and Claude Code plugins
- 📱 **Mobile & Cross-Platform Applications** — Android applications built with Kotlin and Jetpack Compose, Google Play releases, automated build and publishing pipelines, and cross-platform development spanning iOS, web, Windows, and macOS
- 🌐 **Web Applications & Platforms** — Full-stack applications using Next.js, TypeScript, Firebase, Cloudflare, REST APIs, and modern web infrastructure
- 🛠️ **Developer Tooling & CLI Engineering** — Rust, Python, TypeScript, CLI utilities, multi-repository tooling, build automation, release tooling, and engineering productivity systems
- 🛡️ **Cybersecurity & Observability** — Threat detection, log analysis, security auditing, vulnerability assessment, monitoring, and security-focused developer tools
- 📺 **Digital Signage & Device Platforms** — Content validation, playback testing, device compatibility, production investigation, monitoring, and QA across diverse hardware and operating-system environments

My work sits at the intersection of quality engineering, automation, AI, and software development. I approach products with a QA mindset from the beginning: understanding failure modes, designing for testability, automating repetitive work, and building release confidence into the engineering process.

Through SudarshanTechLabs, I also build products and tools from idea to production, covering architecture, development, testing, CI/CD, release automation, monitoring, and ongoing maintenance.

🌐 [sudarshantechlabs.com](https://sudarshantechlabs.com/) · 💼 [LinkedIn](https://linkedin.com/in/sudarshan-chaudhari) · 🐙 [GitHub](https://github.com/SUDARSHANCHAUDHARI) · ✉️ [sunny.sudarshan@gmail.com](mailto:sunny.sudarshan@gmail.com)
