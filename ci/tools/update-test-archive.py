#!/usr/bin/env python3
"""Describe retained specialist definitions; this artifact never selects tests."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
DESTINATION = ROOT / "reports/testing/test-selection-archive.generated.json"


def archive() -> dict:
    inventory_bytes = (ROOT / "config/testing/active-cases.json").read_bytes()
    inventory = json.loads(inventory_bytes)
    python_targets = {item["selector"]["target"] for item in inventory["executions"]
                      if item["selector"]["kind"] == "python"}
    go_targets = {(item["selector"]["module"], item["selector"]["package"], item["selector"]["test"].split("/")[0])
                  for item in inventory["executions"] if item["selector"]["kind"] == "go"}
    raw = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT)
    files = sorted(set(raw.decode("utf-8").rstrip("\0").split("\0")))
    retained = []
    for name in files:
        path = ROOT / name
        if name.startswith("modules/") or path.is_symlink() or not path.is_file():
            continue
        definitions = []
        selected = []
        if path.suffix == ".py" and (path.name.startswith("test_") or path.name.endswith("_test.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            module = name[:-3].replace("/", ".")
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    for method in node.body:
                        if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)) and method.name.startswith("test_"):
                            target = f"{module}.{node.name}.{method.name}"
                            (selected if target in python_targets else definitions).append(target)
        elif name.endswith("_test.go"):
            module = next((parent.as_posix() for parent in path.relative_to(ROOT).parents
                           if (ROOT / parent / "go.mod").is_file()), None)
            if module:
                relative = path.relative_to(ROOT / module).parent.as_posix()
                package = "." if relative == "." else "./" + relative
                for method in re.findall(r"^func (Test\w+|Fuzz\w+)\(", path.read_text(encoding="utf-8"), re.MULTILINE):
                    (selected if (module, package, method) in go_targets else definitions).append(method)
        if definitions or selected:
            retained.append({"source": name, "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                             "on_demand_definitions": definitions, "contains_selected_definitions": selected})
    return {"schema_version": 1, "generator": "ci/tools/update-test-archive.py",
            "purpose": "Non-executable archive disposition; only config/testing/active-cases.json selects active cases.",
            "inventory_sha256": hashlib.sha256(inventory_bytes).hexdigest(),
            "counting": "Definitions are not expanded behavioral cases. Unselected parameters of partially selected definitions remain on demand.",
            "disposition": "Retained source; no automatic execution and no new PASS. Original historical evidence retains its original revision.",
            "on_demand_definition_count": sum(len(item["on_demand_definitions"]) for item in retained),
            "sources": retained}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    expected = json.dumps(archive(), indent=2, sort_keys=True) + "\n"
    if arguments.check:
        if not DESTINATION.is_file() or DESTINATION.read_text(encoding="utf-8") != expected:
            raise SystemExit("Specialist archive differs from its inventory/source generator inputs")
        print("Specialist archive matches current inventory and retained source definitions")
    else:
        DESTINATION.write_text(expected, encoding="utf-8")
        print(DESTINATION.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
