#!/usr/bin/env bash
# Condition C helper — runs curbcut-guard.py in block mode against an existing file and
# prints exactly the findings the hook would show a model, for pasting back into the session.
#
#   bash hook_check.sh outputs/claude/form/B/run-1.html
#
# The guard is a Claude Code hook: it reads tool-call JSON on stdin, not a file path, so the
# payload is synthesised here. CURBCUT_MODE=block overrides the repo's warn-mode .curbcut.json,
# as METHODOLOGY.md condition C requires.
# Exit code: 2 = findings that would block (CRITICAL/HIGH), 0 = clean or MEDIUM only.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GUARD="$REPO/enforce/hooks/curbcut-guard.py"

if [ $# -ne 1 ]; then
  echo "usage: bash hook_check.sh <file>" >&2
  exit 1
fi
if [ ! -f "$1" ]; then
  echo "error: no such file: $1" >&2
  exit 1
fi
if [ ! -f "$GUARD" ]; then
  echo "error: guard not found at $GUARD" >&2
  exit 1
fi

set +e
python3 -c 'import json,sys; p=sys.argv[1]; print(json.dumps({"tool_name":"Write","tool_input":{"file_path":p,"content":open(p,encoding="utf-8",errors="replace").read()}}))' "$1" \
  | CURBCUT_MODE=block python3 "$GUARD"
code=$?
set -e

[ "$code" -eq 0 ] && echo "CurbCut: no blocking findings in $1"
exit "$code"
