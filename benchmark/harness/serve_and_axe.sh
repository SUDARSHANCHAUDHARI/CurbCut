#!/usr/bin/env bash
# axe-core half of the measurement (see run_axe.md, ../METHODOLOGY.md).
#
# Serves this harness directory over HTTP, runs the pinned @axe-core/cli against every
# generated output in a real browser, saves the raw JSON per file, and emits a tidy CSV
# of critical/serious counts ready to merge into results.csv.
#
# Usage:
#   bash serve_and_axe.sh                 # all of outputs/
#   bash serve_and_axe.sh outputs/claude  # a subtree
#   PORT=8123 bash serve_and_axe.sh       # pick the port
#
# Output:
#   axe/<model>-<task>-<condition>-<run>.json   raw axe results
#   axe/axe_counts.csv                          model,task,condition,run,file,axe_*
set -euo pipefail

HARNESS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HARNESS/../.." && pwd)"
TARGET="${1:-outputs}"
PORT="${PORT:-8731}"
AXE_DIR="$HARNESS/axe"
COUNTS="$AXE_DIR/axe_counts.csv"

cd "$HARNESS"

if [ ! -d "$TARGET" ]; then
  echo "error: '$TARGET' not found under $HARNESS" >&2
  exit 1
fi

# The pinned CLI must come from the repo lockfile, not an ad-hoc npx download.
AXE_BIN="$REPO/node_modules/.bin/axe"
if [ ! -x "$AXE_BIN" ]; then
  echo "error: @axe-core/cli not installed. Run 'npm ci' in $REPO" >&2
  exit 1
fi
AXE_VERSION="$(node -p "require('$REPO/node_modules/@axe-core/cli/package.json').version")"
CORE_VERSION="$(node -p "require('$REPO/node_modules/axe-core/package.json').version")"

# The CLI bundles its own chromedriver, which goes stale the moment Chrome auto-updates.
# Use the pinned chromedriver dependency instead and fail loudly on a version mismatch.
DRIVER="$REPO/node_modules/chromedriver/lib/chromedriver/chromedriver"
if [ ! -x "$DRIVER" ]; then
  echo "error: pinned chromedriver missing. Run 'npm ci' in $REPO" >&2
  exit 1
fi
DRIVER_VERSION="$("$DRIVER" --version | awk '{print $2}')"
CHROME_APP="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROME_VERSION="unknown"
if [ -x "$CHROME_APP" ]; then
  CHROME_VERSION="$("$CHROME_APP" --version | awk '{print $NF}')"
  if [ "${CHROME_VERSION%%.*}" != "${DRIVER_VERSION%%.*}" ]; then
    echo "error: chromedriver $DRIVER_VERSION cannot drive Chrome $CHROME_VERSION." >&2
    echo "       Install the matching driver: npm i -D chromedriver@${CHROME_VERSION%%.*}" >&2
    echo "       (then re-pin the exact version in package.json)" >&2
    exit 1
  fi
fi

# while-read, not mapfile: macOS ships bash 3.2.
FILES=()
while IFS= read -r line; do
  FILES+=("$line")
done < <(find "$TARGET" -type f \( -name '*.html' -o -name '*.htm' \) | sort)
if [ "${#FILES[@]}" -eq 0 ]; then
  echo "error: no .html outputs under $HARNESS/$TARGET — run Block 1 first (../RUNBOOK.md)" >&2
  exit 1
fi

mkdir -p "$AXE_DIR"
python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SERVER_PID=$!
# Always reap the server, including on error or Ctrl-C.
trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT INT TERM

for _ in $(seq 1 40); do
  curl -sf "http://127.0.0.1:$PORT/" >/dev/null 2>&1 && break
  sleep 0.25
done
if ! curl -sf "http://127.0.0.1:$PORT/" >/dev/null 2>&1; then
  echo "error: static server did not come up on port $PORT" >&2
  exit 1
fi

echo "@axe-core/cli $AXE_VERSION (axe-core $CORE_VERSION) · chromedriver $DRIVER_VERSION · Chrome $CHROME_VERSION"
echo "${#FILES[@]} file(s) · port $PORT"
echo "model,task,condition,run,file,axe_critical,axe_serious,axe_moderate,axe_minor,axe_status" > "$COUNTS"

fail=0
for f in "${FILES[@]}"; do
  rel="${f#./}"
  # outputs/<model>/<task>/<condition>/run-<n>.html — metadata only for that layout,
  # so a plumbing run over samples/ still works with blank attribution.
  model=""; task=""; condition=""
  case "$rel" in
    outputs/*/*/*/*) IFS='/' read -r _ model task condition _ <<< "$rel" ;;
  esac
  run="$(basename "${rel%.*}")"
  if [ -n "$model" ]; then
    slug="$model-$task-$condition-$run"
  else
    # Outside the outputs/ layout, keep the whole relative path so slugs stay unique.
    slug="${rel%.*}"
  fi
  slug="$(printf '%s' "$slug" | tr -c 'A-Za-z0-9._-' '-')"
  # --save is resolved relative to the cwd, so it must not be an absolute path.
  json_rel="axe/$slug.json"
  json="$AXE_DIR/$slug.json"

  # axe exits non-zero when it finds violations; that is data, not an error.
  set +e
  "$AXE_BIN" "http://127.0.0.1:$PORT/$rel" \
    --chromedriver-path "$DRIVER" --save "$json_rel" --exit >"$AXE_DIR/$slug.log" 2>&1
  code=$?
  set -e

  if [ ! -s "$json" ]; then
    echo "  ERROR  $rel (axe exit $code, no JSON — see $AXE_DIR/$slug.log)"
    echo "${model},${task},${condition},${run},${rel},,,,,error" >> "$COUNTS"
    fail=$((fail + 1))
    continue
  fi

  read -r c s m n < <(python3 - "$json" <<'PY'
import json, sys
from collections import Counter
# One count per violated rule, per run_axe.md ("count violations by impact").
data = json.load(open(sys.argv[1]))
pages = data if isinstance(data, list) else [data]
c = Counter()
for page in pages:
    for v in page.get("violations", []):
        c[v.get("impact") or "unknown"] += 1
print(c["critical"], c["serious"], c["moderate"], c["minor"])
PY
)
  echo "  ok     $rel  critical=$c serious=$s moderate=$m minor=$n"
  echo "${model},${task},${condition},${run},${rel},${c},${s},${m},${n},ok" >> "$COUNTS"
done

echo
echo "wrote $COUNTS"
echo "raw JSON in $AXE_DIR"
[ "$fail" -gt 0 ] && echo "WARNING: $fail file(s) failed to run — listed as axe_status=error in the CSV"
exit 0
