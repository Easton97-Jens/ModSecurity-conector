"""Verify fixed product maintenance bytes independently of test inventories.

Publishers reconstruct language/component primaries from trusted Git objects.
This module neither imports the Test Framework nor reads or mutates its tests,
selection inventory or archive.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PROJECT_LOCK = "ci/tooling/project-versions.lock.json"
LANGUAGE_PATHS = {
    "python": frozenset((".python-version", PROJECT_LOCK)),
    "go": frozenset((".go-version", PROJECT_LOCK,
                     "connectors/envoy/ext_proc/go.mod", "connectors/envoy/ext_proc/go.sum")),
}
MAX_BYTES = 16 * 1024 * 1024

class MaintenanceChangeError(ValueError):
    """A product maintenance change violates its fixed primary policy."""

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise MaintenanceChangeError("duplicate maintenance JSON key")
        result[key] = value
    return result

def _json(raw: bytes):
    if len(raw) > MAX_BYTES:
        raise MaintenanceChangeError("maintenance input exceeds its size limit")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_object)

def _same(first, second) -> bool:
    # Python considers True == 1. Inventory/control JSON must not do so.
    return json.dumps(first, sort_keys=True, ensure_ascii=False) == json.dumps(second, sort_keys=True, ensure_ascii=False)

def read_regular(root: Path, relative: str) -> bytes:
    parts = relative.split("/")
    if not parts or any(part in {"", ".", ".."} for part in parts) or relative.startswith("/"):
        raise MaintenanceChangeError("maintenance paths must be canonical relative paths")
    descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        child = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=descriptor)
        with os.fdopen(child, "rb") as source:
            metadata = os.fstat(source.fileno())
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1 or metadata.st_size > MAX_BYTES:
                raise MaintenanceChangeError("maintenance input must be a bounded single-link regular file")
            return source.read(MAX_BYTES + 1)
    finally:
        os.close(descriptor)

def _git(root: Path, *arguments: str) -> bytes:
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(root), *arguments], timeout=30)

def trusted_blob(root: Path, revision: str, relative: str) -> bytes:
    if (re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_./-]{0,199}", revision) is None or ".." in revision
            or relative.startswith("/") or any(part in {"", ".", ".."} for part in relative.split("/"))):
        raise MaintenanceChangeError("unsafe maintenance Git object reference")
    row = _git(root, "ls-tree", "-z", revision, "--", relative).split(b"\0")
    if len(row) != 2 or not row[0].startswith(b"100644 blob ") or row[0].split(b"\t", 1)[-1].decode() != relative:
        raise MaintenanceChangeError("maintenance baseline must contain a fixed regular source blob")
    return _git(root, "show", "--no-textconv", "--format=", "--end-of-options", revision + ":" + relative)

def index_blob(root: Path, relative: str) -> bytes:
    if relative not in LANGUAGE_PATHS["python"] | LANGUAGE_PATHS["go"]:
        raise MaintenanceChangeError("index path escapes fixed maintenance policy")
    rows = _git(root, "ls-files", "--stage", "-z", "--", relative).split(b"\0")
    if len(rows) != 2 or not rows[0].startswith(b"100644 ") or b" 0\t" not in rows[0]:
        raise MaintenanceChangeError("staged maintenance input must be one regular stage-zero blob")
    return _git(root, "show", "--no-textconv", ":" + relative)

def _language_policy(kind: str, before: dict[str, bytes], after: dict[str, bytes]) -> None:
    old, new = _json(before[PROJECT_LOCK]), _json(after[PROJECT_LOCK])
    field = kind + "_version"
    if set(old) != set(new) or any(not _same(old[key], new[key]) for key in old if key != field):
        raise MaintenanceChangeError("maintenance changed another central version-lock field")
    for values, bodies in ((old, before), (new, after)):
        if bodies["." + kind + "-version"] != (str(values[field]) + "\n").encode():
            raise MaintenanceChangeError("maintenance version view differs from its central lock")
    if kind == "python":
        pattern = r"3\.15\.(0|[1-9]\d*)"
        first, second = re.fullmatch(pattern, str(old[field]), re.ASCII), re.fullmatch(pattern, str(new[field]), re.ASCII)
        if not first or not second or int(second[1]) < int(first[1]):
            raise MaintenanceChangeError("maintenance Python version is noncanonical or nonmonotonic")
    elif _go_triplet(new[field]) < _go_triplet(old[field]):
        raise MaintenanceChangeError("maintenance Go version is nonmonotonic")
    if kind == "go":
        _go_component_policy(before, after)

def _cli_root(value: str | Path) -> Path:
    """Confine CLI operations to this source tree; library roots stay explicit."""
    text = os.fspath(value)
    if text != str(ROOT) or Path(text).resolve(strict=True) != ROOT:
        raise MaintenanceChangeError("maintenance CLI root must be exactly its canonical source repository")
    return ROOT

def _go_triplet(value: object) -> tuple[int, int, int]:
    # Same exact stable numeric grammar as the product Go release resolver.
    if type(value) is not str or re.fullmatch(r"[1-9]\d*\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", value, re.ASCII) is None:
        raise MaintenanceChangeError("maintenance Go version is not canonical stable numeric semver")
    return tuple(int(part) for part in value.split("."))


def _go_component_policy(before: dict[str, bytes], after: dict[str, bytes]) -> None:
    mod, sums = "connectors/envoy/ext_proc/go.mod", "connectors/envoy/ext_proc/go.sum"
    if before[mod] == after[mod] and before[sums] == after[sums]:
        return
    temporary_parent = os.environ.get("RUNNER_TEMP") or os.environ.get("TMP_ROOT")
    if not temporary_parent or not Path(temporary_parent).is_absolute() or not Path(temporary_parent).is_dir():
        raise MaintenanceChangeError("Go component verification requires an existing external RUNNER_TEMP or TMP_ROOT")
    parent = Path(temporary_parent).resolve(strict=True)
    if parent == ROOT or ROOT in parent.parents:
        raise MaintenanceChangeError("Go component verification output must stay outside the product source")
    with tempfile.TemporaryDirectory(prefix="maintenance-components-", dir=parent) as temporary:
        candidate = Path(temporary)
        for name in (mod, sums):
            path = candidate / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(after[name])
        baseline = before[mod] + b"\0" + before[sums]
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/update-go-components.py"),
             "--validate-candidate", "--repository-root", str(candidate), "--json"],
            input=baseline, capture_output=True, check=False, timeout=30,
        )
        if completed.returncode:
            raise MaintenanceChangeError("Go component bytes violate the existing candidate policy")


def verify_language_changes(root: Path, base: str, kind: str, head: str | None = None,
                            *, staged: bool = False) -> dict[str, bytes]:
    """Prove fixed primary policy and reject every non-product companion path."""
    if kind not in LANGUAGE_PATHS:
        raise MaintenanceChangeError("unknown fixed language maintenance policy")
    if head and staged:
        raise MaintenanceChangeError("staged verification cannot select a branch head")
    for revision in (base, head):
        if revision is not None and (re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_./-]{0,199}", revision) is None or ".." in revision):
            raise MaintenanceChangeError("unsafe maintenance Git object reference")
    approved = LANGUAGE_PATHS[kind]
    arguments = ["diff", "--name-only", "-z", "--no-renames"]
    if staged:
        arguments.append("--cached")
    arguments += [base]
    if head:
        arguments.append(head)
    arguments.append("--")
    changed = {os.fsdecode(name) for name in _git(root, *arguments).split(b"\0") if name}
    if not changed <= approved:
        raise MaintenanceChangeError("maintenance changed a path outside its fixed product-primary allowlist")
    before = {name: trusted_blob(root, base, name) for name in approved}
    after = {name: (trusted_blob(root, head, name) if head else
                    index_blob(root, name) if staged else read_regular(root, name)) for name in approved}
    _language_policy(kind, before, after)
    return after


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("command", choices=("verify",))
    parser.add_argument("--kind", required=True, choices=tuple(LANGUAGE_PATHS))
    parser.add_argument("--base", required=True)
    parser.add_argument("--head")
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args(argv)
    try:
        root = _cli_root(args.root)
        verify_language_changes(root, args.base, args.kind, args.head, staged=args.staged)
        print("MAINTENANCE_PRIMARY_VERIFIED")
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print("MAINTENANCE_PRIMARY_REJECTED: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
