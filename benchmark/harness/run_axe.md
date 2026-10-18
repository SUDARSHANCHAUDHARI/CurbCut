# axe-core runner (the other half of the measurement)

`score.py` covers the deterministic hook-rule half. Real barriers also need `axe-core`, run against
each output **rendered in a browser** (axe evaluates the live DOM + computed styles, which static
grep cannot).

## Pinned setup
Both dependencies are pinned to exact versions in the repo root `package.json`:

```bash
npm ci   # @axe-core/cli 4.14.0 (axe-core 4.14.0) + chromedriver 155.0.2
```

The CLI bundles its own chromedriver, which breaks as soon as Chrome auto-updates
(`session not created: This version of ChromeDriver only supports Chrome version N`). The pinned
`chromedriver` dependency is used instead, via `--chromedriver-path`. When Chrome moves to a new
major version, `serve_and_axe.sh` stops with the mismatch and the command to fix it:

```bash
npm i -D chromedriver@<chrome-major>   # then re-pin the exact version in package.json
```

## Running it
`serve_and_axe.sh` does the whole loop — serves this directory on 127.0.0.1, runs the pinned CLI
against every `.html` under `outputs/`, saves raw JSON per file, and writes `axe/axe_counts.csv`.

```bash
bash serve_and_axe.sh                 # all of outputs/
bash serve_and_axe.sh outputs/claude  # one subtree
PORT=8123 bash serve_and_axe.sh       # pick the port (default 8731)
```

Violations are counted per violated rule, by `impact` (critical / serious / moderate / minor). A
file axe cannot evaluate is written to the CSV as `axe_status=error`, never silently dropped; its
stdout is kept in `axe/<slug>.log`.

## Combine
Merge the axe critical+serious counts with `score.py`'s per-file rows into `results.csv`, then compute
the medians per condition described in `../METHODOLOGY.md`. Only then does `RESULTS.md` get written.
