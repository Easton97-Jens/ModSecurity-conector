#!/usr/bin/env python3
"""Generate source-backed connector configuration references and inventory."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
sys.path.insert(0, str(ROOT / "ci" / "checks" / "documentation"))

from connector_config_reference import generated_file_paths, rendered_files, write_rendered_files  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when generated outputs are stale")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    try:
        outputs = rendered_files(root)
    except (OSError, ValueError) as error:
        print(f"connector configuration generation: FAIL: {error}", file=sys.stderr)
        return 2
    if args.check:
        stale = [path.relative_to(root).as_posix() for path, content in outputs.items() if not path.is_file() or path.read_text(encoding="utf-8") != content]
        if stale:
            print("connector configuration generation: FAIL (stale generated files)", file=sys.stderr)
            print("\n".join(sorted(stale)), file=sys.stderr)
            return 1
        print(f"connector configuration generation: PASS ({len(generated_file_paths(root))} generated files current)")
        return 0
    changed = write_rendered_files(root)
    for path in changed:
        print(path.relative_to(root).as_posix())
    print(f"connector configuration generation: wrote {len(changed)} changed files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
