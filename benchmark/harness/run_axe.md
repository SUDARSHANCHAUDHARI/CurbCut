# axe-core runner (the other half of the measurement)

`score.py` covers the deterministic hook-rule half. Real barriers also need `axe-core`, run against
each output **rendered in a browser** (axe evaluates the live DOM + computed styles, which static
grep cannot).

## Pinned setup
```bash
npm i -D @axe-core/cli   # pin the version in package-lock and record it per run
```

## Per output
```bash
# serve the file, then:
npx @axe-core/cli "http://localhost:PORT/outputs/<model>/<task>/<condition>/run-<n>.html" \
  --exit --save axe/<model>-<task>-<condition>-<n>.json
```
`--exit` returns non-zero on violations (useful for CI); `--save` keeps the raw JSON for the tidy
results table. Count violations by `impact` (critical / serious / moderate / minor).

## Combine
Merge the axe critical+serious counts with `score.py`'s per-file rows into `results.csv`, then compute
the medians per condition described in `../METHODOLOGY.md`. Only then does `RESULTS.md` get written.
