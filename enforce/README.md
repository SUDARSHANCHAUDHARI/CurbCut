# CurbCut Enforcement

The layer an advisory guideline can't ship. Three complementary gates, all driven by the 🟢 AUTO
rules in `CurbCut.md`:

| Gate | Runs | Blocks | File |
| :--- | :--- | :--- | :--- |
| **Hook** | at AI/human write time | the write | [`hooks/curbcut-guard.py`](hooks/curbcut-guard.py) |
| **Lint** | in editor / pre-commit | the commit | [`rules/`](rules/) |
| **CI** | on pull request | the merge | [`ci/curbcut.yml`](ci/curbcut.yml) |

## Hook

A PreToolUse hook for Claude Code (works standalone too — it's just stdin JSON → exit code).

```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Write|Edit|MultiEdit",
        "hooks": [{ "type": "command",
          "command": "python3 /ABS/PATH/CurbCut/enforce/hooks/curbcut-guard.py" }] }
    ]
  }
}
```

**Modes** (env `CURBCUT_MODE` > repo `.curbcut.json` > default `warn`):
- `off` — do nothing.
- `warn` — print findings to stderr, allow the write. **Default; never surprise-blocks.**
- `block` — deny writes containing CRITICAL/HIGH AUTO findings (exit 2). Opt in per repo.

**Escape hatches** (record the reason in `EXCEPTIONS.md`):
```
// curbcut-disable-next-line WEB_CLICKABLE_DIV
// curbcut-disable COMPOSE_TEXT_SIZE_DP
```
or per-repo in `.curbcut.json`: `"disable": ["RULE_ID"]`.

## Rule catalogue (v1)

| ID | Sev | Platform | Blocks in `block` mode |
| :--- | :--- | :--- | :---: |
| `WEB_CLICKABLE_DIV` | 🔴 | web | ✅ |
| `WEB_IMG_NO_ALT` | 🟠 | web | ✅ |
| `WEB_OUTLINE_NONE` | 🟠 | web | ✅ |
| `WEB_POSITIVE_TABINDEX` | 🟠 | web | ✅ |
| `WEB_REDUNDANT_ROLE` | 🟡 | web | warn only |
| `COMPOSE_CLICKABLE_NO_ROLE` | 🔴 | compose | ✅ |
| `COMPOSE_TEXT_SIZE_DP` | 🟠 | compose | ✅ |
| `COMPOSE_ICON_NULL_DESC` | 🟡 | compose | warn only |
| `SWIFTUI_TAP_ON_TEXT` | 🟠 | swiftui | ✅ |
| `SWIFTUI_FIXED_FONT` | 🟡 | swiftui | warn only |

Only CRITICAL/HIGH ever block; MEDIUM always warns (grep can't disambiguate them safely).

## Tests
`python3 tests/test_guard.py` exercises every rule against a bad and a clean sample.
