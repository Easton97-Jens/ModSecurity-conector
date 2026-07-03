#!/usr/bin/env python3
"""Check Makefile and script wiring for Apache C-standard smoke checks."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = ROOT / "Makefile"
SCRIPT = ROOT / "ci/check-apache-c-standards.sh"

ok = True

def fail(message: str) -> None:
    global ok
    print(f"FAIL: {message}")
    ok = False

def pass_(message: str) -> None:
    print(f"PASS: {message}")

if not SCRIPT.exists():
    fail("ci/check-apache-c-standards.sh exists")
    script_text = ""
else:
    pass_("ci/check-apache-c-standards.sh exists")
    script_text = SCRIPT.read_text(encoding="utf-8")

make_text = MAKEFILE.read_text(encoding="utf-8")
for target in (
    "check-apache-c17",
    "check-apache-c23",
    "check-apache-future-c",
    "check-apache-c-standards",
    "check-apache-c20",
    "check-apache-c26",
):
    if f"{target}:" in make_text:
        pass_(f"Makefile contains {target}")
    else:
        fail(f"Makefile contains {target}")

lint_block = make_text.split("lint:", 1)[1].split("\n\n", 1)[0] if "lint:" in make_text else ""
if "$(MAKE) check-apache-c17" in lint_block:
    pass_("lint invokes check-apache-c17")
else:
    fail("lint invokes check-apache-c17")

if "-Wno-error" in script_text:
    fail("Apache C standards check must not use -Wno-error")
else:
    pass_("Apache C standards check does not use -Wno-error")

required_script_terms = {
    "mandatory C17 flags": "-std=c17 -Wall -Wextra -Werror",
    "optional c23 profile": "--profile \"$profile\"",
    "exit 77 blocked path": "exit 77",
    "optional skip wording": "SKIPPED: optional Apache C23 check",
    "future-C skip wording": "SKIPPED: optional Apache future-C check",
}
for label, term in required_script_terms.items():
    if term in script_text:
        pass_(label)
    else:
        fail(label)

if not ok:
    sys.exit(1)
print("apache-c-standard-wiring: pass")
