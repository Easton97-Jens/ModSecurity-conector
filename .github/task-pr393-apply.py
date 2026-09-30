#!/usr/bin/env python3
"""Run isolated hash-bound preparation; helpers are excluded from the repair."""
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
needle = '    (temp/"repair-paths.json").write_text(json.dumps(sorted(desired)))\n'
addition = '''    # Generate projections only after the reviewed Framework checkout is active.
    # The trusted Parent generator is unchanged; candidate shell is not executed.
    import runpy
    guide_generator = root / "scripts/generate_compiler_guides.py"
    require(guide_generator.read_bytes() == git(root, "show", HEAD + ":scripts/generate_compiler_guides.py"),
            "Compiler guide generator changed")
    rendered = runpy.run_path(str(guide_generator))["rendered_files"]()
    generated_paths = []
    for name, content in rendered.items():
        require(Path(name).name == name, "Unsafe generated guide filename")
        path = "docs/build/compilers/" + name
        if name not in ("nginx.md", "nginx.de.md"):
            require((root / path).read_text(encoding="utf-8") == content,
                    "Unexpected unrelated generated-guide drift: " + name)
            continue
        require("1.31.6" in content, "Generated NGINX guide lacks reviewed version")
        (root / path).write_text(content, encoding="utf-8", newline="")
        desired[path] = content
        generated_paths.append(path)
    require(len(generated_paths) == 2, "Expected both generated NGINX language companions")
    git(root, "add", "--", *generated_paths)
'''
if text.count(needle) != 1:
    raise ValueError("Expected pre-validation tree capture is not unique")
text = text.replace(needle, addition + needle, 1)
ast.parse(text, filename=str(source))
target = Path(os.environ["RUNNER_TEMP"]) / "reviewed-pr393-prepare.py"
with target.open("x", encoding="utf-8", newline="") as stream:
    stream.write(text)
runpy.run_path(str(target), run_name="__main__")
