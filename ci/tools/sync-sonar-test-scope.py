#!/usr/bin/env python3
"""Synchronize only sonar.test.inclusions from the reviewed source-role contract."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ci.lib.sonar_source_roles import SourceRoleError, load_roles, read_source

PROPERTIES = (".sonarcloud.properties", "sonar-project.properties")
INCLUSIONS_PROPERTY = "sonar.test.inclusions="


def expected_text(name: str, inclusions: str) -> tuple[bytes, bytes]:
    old = read_source(ROOT, name)
    lines = old.decode("utf-8").splitlines(keepends=True)
    matches = [index for index, line in enumerate(lines)
               if re.match(r"^\s*sonar\.test\.inclusions\s*[:=]", line)]
    if len(matches) != 1 or not lines[matches[0]].startswith(INCLUSIONS_PROPERTY):
        raise SourceRoleError(f"{name} must contain one canonical sonar.test.inclusions line")
    index = matches[0]
    newline = "\r\n" if lines[index].endswith("\r\n") else "\n"
    lines[index] = INCLUSIONS_PROPERTY + inclusions + newline
    return old, "".join(lines).encode("utf-8")


def replace_line(name: str, old: bytes, new: bytes) -> None:
    destination = ROOT / name
    metadata = destination.lstat()
    descriptor, temporary_name = tempfile.mkstemp(prefix=".sonar-test-scope-", dir=ROOT)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(new)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, metadata.st_mode & 0o777)
        if read_source(ROOT, name) != old:
            raise SourceRoleError(f"{name} changed while source-role scope was prepared")
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    arguments = parser.parse_args()
    try:
        roles = load_roles(ROOT)
        updates = [(name, *expected_text(name, roles.test_inclusions())) for name in PROPERTIES]
        drifted = [name for name, old, new in updates if old != new]
        if arguments.check and drifted:
            raise SourceRoleError("Sonar test scope drift: " + ", ".join(drifted))
        if arguments.write:
            for name, old, new in updates:
                if old != new:
                    replace_line(name, old, new)
        print(f"SONAR_SOURCE_ROLES_OK: {len(roles.reviewed)} reviewed exact fixtures; "
              f"{len(roles.exact_tests)} exact Python/Go analysis tests; "
              f"contract_sha256={roles.sha256}")
        return 0
    except (SourceRoleError, OSError, UnicodeError) as exc:
        print(f"SONAR_SOURCE_ROLES_REJECTED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
