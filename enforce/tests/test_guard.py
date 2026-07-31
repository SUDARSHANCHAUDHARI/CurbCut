#!/usr/bin/env python3
"""Self-contained tests for curbcut-guard. Run: python3 enforce/tests/test_guard.py"""
import importlib.util
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "hooks" / "curbcut-guard.py"
spec = importlib.util.spec_from_file_location("guard", GUARD)
guard = importlib.util.module_from_spec(spec)
sys.modules["guard"] = guard  # required before exec so dataclass annotations resolve (py3.9)
spec.loader.exec_module(guard)

BAD = {
    "a.jsx": '<div onClick={go}>Save</div>\n<img src="x.png">\ninput:focus{outline:none}\n'
             '<a onClick={go}>x</a>\n<input autoFocus />',
    "a.kt": 'Box(Modifier.clickable { go() })\nText(fontSize = 12.dp)\n'
            'Icon(x, contentDescription = "")',
    "a.swift": 'Text("Tap").onTapGesture { go() }\n.font(.system(size: 13))',
}
CLEAN = {
    "a.jsx": '<button onClick={go}>Save</button>\n<img src="x.png" alt="logo">',
    "a.kt": 'Button(onClick = ::go) { Text("Save", fontSize = 16.sp) }',
    "a.swift": 'Button { go() } label: { Text("Tap") }.font(.body)',
}

failures = 0

def check(name, cond):
    global failures
    status = "ok  " if cond else "FAIL"
    if not cond:
        failures += 1
    print(f"  [{status}] {name}")

print("BAD samples should produce findings:")
for path, src in BAD.items():
    findings = guard.analyze(path, src, {})
    check(f"{path}: {len(findings)} finding(s)", len(findings) >= 1)

print("CLEAN samples should be silent:")
for path, src in CLEAN.items():
    findings = guard.analyze(path, src, {})
    check(f"{path}: {len(findings)} finding(s)", len(findings) == 0)

print("disable-next-line suppresses:")
suppressed = guard.analyze(
    "a.jsx", "// curbcut-disable-next-line WEB_CLICKABLE_DIV\n<div onClick={go}>x</div>", {})
check("suppressed clickable div", len(suppressed) == 0)

print("config disable list suppresses:")
cfg_off = guard.analyze("a.kt", "Box(Modifier.clickable { go() })",
                        {"disable": ["COMPOSE_CLICKABLE_NO_ROLE"]})
check("config-disabled rule", len(cfg_off) == 0)

print(f"\n{'PASSED' if failures == 0 else str(failures) + ' FAILED'}")
sys.exit(1 if failures else 0)
