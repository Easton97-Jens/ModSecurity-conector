#!/usr/bin/env python3
"""Run the isolated, hash-bound preparation source with reviewed corrections.

Both files are temporary validation infrastructure and absent from the repair
commit. Only our own pinned helper is loaded; candidate common.sh stays data.
"""
from pathlib import Path
import ast
import hashlib
import runpy
import os

source = Path(__file__).with_name("task-pr393-apply-source.py")
payload = source.read_bytes()
identity = hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload,
                       usedforsecurity=False).hexdigest()
if identity != "88df2e4f92e42ad17a88058e6bf06b10efa18ab4":
    raise ValueError("Reviewed preparation helper changed")
text = payload.decode("utf-8")
before = '"differs from approved reviewed structure" in baseline.stderr'
after = '"differs from approved reviewed structure" in (baseline.stdout + baseline.stderr)'
if text.count(before) != 1:
    raise ValueError("Expected baseline diagnostic predicate is not unique")
text = text.replace(before, after, 1)
before_write = '    for path, text in desired.items():\n'
after_write = before_write + '        if not text.endswith("\\n"):\n            text += "\\n"\n'
if text.count(before_write) != 1:
    raise ValueError("Expected final source-writing loop is not unique")
text = text.replace(before_write, after_write, 1)
ast.parse(text, filename=str(source))
target = Path(os.environ["RUNNER_TEMP"]) / "reviewed-pr393-prepare.py"
with target.open("x", encoding="utf-8", newline="") as stream:
    stream.write(text)
runpy.run_path(str(target), run_name="__main__")
