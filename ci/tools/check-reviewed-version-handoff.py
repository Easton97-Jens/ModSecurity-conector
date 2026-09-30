#!/usr/bin/env python3
"""Check reviewed NGINX/ModSecurity handoff data without executing candidate code.

This is an early consistency check, not approval of a new upstream release.
The existing candidate verifier and all native/runtime gates remain required.
Only fixed repository paths are read. No network, shell, writes or imports from
candidate common.sh or the documentation generator are performed.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

MAX_BYTES = 2 * 1024 * 1024
COMMON = "modules/ModSecurity-test-Framework/ci/lib/common.sh"
VERIFIER = "ci/tools/verify-framework-candidate-contract.py"
WRITER = "ci/runtime/lifecycle/write-nginx-functional-a-evidence.py"
WORKFLOW = ".github/workflows/test-nginx-exact-head.yml"
GUIDE_SOURCES = ("scripts/generate_compiler_guides.py", "tests/test_compiler_guides.py")
GUIDES = ("docs/build/compilers/libmodsecurity.md", "docs/build/compilers/libmodsecurity.de.md")
MODSECURITY_KEYS = (
    "MODSECURITY_V3_APPROVED_REPO_URL",
    "MODSECURITY_V3_RELEASE_TAG",
    "MODSECURITY_V3_APPROVED_COMMIT",
)
OFFICIAL_REPOSITORY = "https://github.com/owasp-modsecurity/ModSecurity.git"


class HandoffError(ValueError):
    """A checked-in projection disagrees with reviewed source data."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise HandoffError(message)


def read_text(root: Path, relative: str) -> str:
    path = root / relative
    require(path.is_absolute(), "repository root must be absolute")
    require(path.resolve(strict=True) == path, f"symlink in checked path: {relative}")
    details = path.lstat()
    require(stat.S_ISREG(details.st_mode), f"not a regular file: {relative}")
    require(details.st_size <= MAX_BYTES, f"file exceeds bound: {relative}")
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        opened = os.fstat(stream.fileno())
        require((opened.st_dev, opened.st_ino) == (details.st_dev, details.st_ino),
                f"file changed while opening: {relative}")
        payload = stream.read(MAX_BYTES + 1)
    require(len(payload) <= MAX_BYTES, f"file exceeds bound: {relative}")
    return payload.decode("utf-8")


def python_constant(text: str, name: str):
    values = [node.value for node in ast.parse(text).body
              if isinstance(node, ast.Assign)
              and any(isinstance(target, ast.Name) and target.id == name for target in node.targets)]
    require(len(values) == 1, f"expected exactly one Python assignment: {name}")
    try:
        return ast.literal_eval(values[0])
    except (ValueError, TypeError, SyntaxError) as error:
        raise HandoffError(f"expected literal Python data: {name}") from error


def reviewed_common(text: str, verifier_text: str) -> None:
    fields = python_constant(verifier_text, "MUTABLE_SOURCE_FIELDS")
    expected = python_constant(verifier_text, "APPROVED_FRAMEWORK_COMMON_STRUCTURE_SHA256")
    require(isinstance(fields, tuple) and bool(fields), "invalid mutable-field registry")
    require(all(isinstance(field, str) for field in fields), "invalid mutable-field name")
    require(len(fields) == len(set(fields)), "duplicate mutable-field name")
    require(not any(field.startswith(("MODSECURITY_", "NGINX_")) for field in fields),
            "NGINX and ModSecurity must remain structurally reviewed")
    require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
            "invalid production review digest")
    normalized = []
    seen = set()
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        name, separator, _value = content.partition("=")
        if separator and name in fields:
            require(name not in seen, f"duplicate mutable source field: {name}")
            seen.add(name)
            normalized.append(name + "=<PARENT_REVIEWED_SOURCE_DATA>" + line[len(content):])
        else:
            normalized.append(line)
    require(seen == set(fields), "incomplete mutable source field registry")
    digest = hashlib.sha256("".join(normalized).encode("utf-8")).hexdigest()
    require(digest == expected,
            "Framework structure is not approved; review the complete change, not just the hash")


def literal_pin(text: str, name: str) -> str:
    prefix = name + "="
    lines = [line for line in text.splitlines() if line.startswith(prefix)]
    require(len(lines) == 1, f"expected one literal source assignment: {name}")
    value = lines[0][len(prefix):]
    require(len(value) >= 3 and value[0] == '"' and value[-1] == '"', f"invalid literal: {name}")
    value = value[1:-1]
    require(value.isascii() and not any(char in value for char in '$`\\\"\';&|<> \t\r\n'),
            f"nonliteral or unsafe value: {name}")
    return value


def command_pins(text: str, label: str, *, python: bool) -> dict[str, str]:
    if python:
        candidates = [node.value for node in ast.walk(ast.parse(text))
                      if isinstance(node, ast.Constant) and isinstance(node.value, str)]
    else:
        candidates = text.splitlines()
    result = {}
    for name in ("MODSECURITY_REF", "MODSECURITY_COMMIT"):
        lines = [value for value in candidates if value.startswith(name + "=")]
        require(bool(lines), f"missing documented assignment: {label}:{name}")
        observed = {literal_pin(value, name) for value in lines}
        require(len(observed) == 1, f"conflicting documented assignments: {label}:{name}")
        result[name] = observed.pop()
    return result


def inspect_handoff(root: Path) -> dict[str, str]:
    root = Path(os.path.abspath(root))
    common = read_text(root, COMMON)
    reviewed_common(common, read_text(root, VERIFIER))
    nginx_tag = literal_pin(common, "NGINX_RELEASE_TAG")
    require(re.fullmatch(r"release-[1-9][0-9]*\.[0-9]+\.[0-9]+", nginx_tag) is not None,
            "invalid reviewed NGINX release tag")
    version = nginx_tag.removeprefix("release-")
    writer_version = python_constant(read_text(root, WRITER), "EXPECTED_NGINX_VERSION")
    require(writer_version == version, "NGINX evidence writer version differs from reviewed Framework")
    workflow_tags = re.findall(r"(?m)^ +NGINX_RELEASE_TAG: ([^\r\n ]+) *$", read_text(root, WORKFLOW))
    require(workflow_tags == [nginx_tag], "NGINX workflow release differs from reviewed Framework")
    repository, release, commit = (literal_pin(common, name) for name in MODSECURITY_KEYS)
    require(repository == OFFICIAL_REPOSITORY, "unexpected ModSecurity repository")
    require(re.fullmatch(r"v3\.[0-9]+\.[0-9]+", release) is not None, "not a stable ModSecurity v3 tag")
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None, "ModSecurity requires an exact commit")
    expected = {"MODSECURITY_REF": release, "MODSECURITY_COMMIT": commit}
    for path in (*GUIDE_SOURCES, *GUIDES):
        observed = command_pins(read_text(root, path), path, python=path.endswith(".py"))
        require(observed == expected,
                f"ModSecurity tag/commit drift in {path}; update generator, tests and EN/DE output together")
    return {"status": "consistent", "nginx_release": nginx_tag,
            "modsecurity_release": release, "modsecurity_commit": commit,
            "scope": "reviewed source and projection consistency; not runtime compatibility"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args(argv)
    try:
        result = inspect_handoff(args.repo_root)
    except (HandoffError, OSError, UnicodeError, SyntaxError) as error:
        print(f"reviewed-version-handoff: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
