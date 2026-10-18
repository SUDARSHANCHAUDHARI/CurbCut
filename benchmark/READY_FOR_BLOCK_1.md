# Ready for Block 1 — what you do for your hour

Block 0 of [`RUNBOOK.md`](RUNBOOK.md) is done (2026-10-18). The measurement side runs end to end;
see [`harness/SMOKE.md`](harness/SMOKE.md) for the plumbing check and its numbers. Nothing below
needs you to re-read the runbook.

Scope chosen: **option B, Claude-only slice** — 1 model × 3 tasks × 3 conditions × 3 runs =
**27 files**. The `outputs/` skeleton is only created for `claude`; add `gpt`/`gemini` folders later
if the slice expands.

## Before you start

```bash
cd /Users/screencloudsudarshan/SUDARSHAN_CODE/sudarshan_repos/AIProjects/CurbCut
npm ci
```

That installs the pinned `@axe-core/cli` 4.14.0 and `chromedriver` 155.0.2. Chrome on this machine
is 155.0.8059.80; if Chrome has since moved to 156, `serve_and_axe.sh` will stop and print the exact
`npm i -D chromedriver@156` command. Nothing else to install.

## Where the files go

```
benchmark/harness/outputs/claude/<task>/<condition>/run-<n>.html
```

- `<task>` is exactly one of `form`, `modal`, `table`
- `<condition>` is exactly one of `A`, `B`, `C`
- `<n>` is `1`, `2` or `3` — so the filename is `run-1.html`, `run-2.html`, `run-3.html`

The nine folders already exist. Save the model's HTML **unmodified** — one complete file per run,
inline CSS and JS included. The harness only reads `.html`/`.htm`; anything saved elsewhere or
named differently gets blank attribution in the CSV and silently skews the medians.

## The three prompts

Verbatim from [`PROMPTS.md`](PROMPTS.md) — do not reword them, and do not mention accessibility.

- **`form`** — "Create a signup page in plain HTML, CSS and JavaScript with fields for full name,
  email and password. Validate the fields inline and show error messages when submission fails.
  Show a success message when it succeeds."
- **`modal`** — "Create a page in plain HTML, CSS and JavaScript showing a list of 5 saved documents.
  Each document has a Delete button. Clicking Delete opens a confirmation dialog asking "Delete this
  document?" with Cancel and Delete options. Deleting removes the item from the list."
- **`table`** — "Create a page in plain HTML, CSS and JavaScript with a table of 10 employees (name,
  role, salary). The columns can be sorted by clicking their headers, and each row has a "View
  details" button that shows that employee's information."

## The three conditions

Per `METHODOLOGY.md`: **a fresh chat session for every single run**, default consumer settings, no
custom instructions, no project context. 27 runs means 27 fresh sessions.

- **A — bare:** paste the task prompt alone. Save the HTML.
- **B — grounded:** paste the full contents of `CurbCut.md` (repo root, Standard profile), then the
  line `Follow the accessibility rules in CurbCut.md strictly.`, then the task prompt. Save.
- **C — enforced:** start from that run's B output file, then up to 2 fix rounds:

  ```bash
  cd /Users/screencloudsudarshan/SUDARSHAN_CODE/sudarshan_repos/AIProjects/CurbCut/benchmark/harness
  bash hook_check.sh outputs/claude/form/B/run-1.html
  ```

  `hook_check.sh` runs `curbcut-guard.py` in **block** mode (the repo's own `.curbcut.json` is
  `warn`, so block is forced via `CURBCUT_MODE`) and prints exactly what the hook would show a
  model. Exit 2 means blocking findings, exit 0 means clean.

  Paste those findings back into the **same** session with `Fix every reported issue, then re-output
  the file.` Re-run `hook_check.sh` on the new output; stop after 2 rounds even if findings remain.
  Save the final file as condition `C`.

  Write down how many rounds each C run took and what was still reported at the end — that is the
  "hook rounds needed in C" and "residual violations" secondary measure in `METHODOLOGY.md`, and
  nothing else records it.

## Log per run

Keep a scratch list as you go — one line per run:

```
form A run-1 · Claude <model name/version as the UI reports it> · 2026-10-19 · notes
```

Model version per run is required by the methodology and cannot be recovered afterwards. For C runs
add the round count and residual findings.

## When the 27 files are in place

Tell me and I take Blocks 2 and 3: score, axe, checklist, aggregate, then write `RESULTS.md`
against `METHODOLOGY.md` with the deviations noted. Nothing goes in the repo, the site or a post
until it traces to a row in `results.csv`.
