#!/usr/bin/env python3
"""Provide the locked security tools in a run-private directory at run time.

Local Make runs call this helper for `$RUNNER_TEMP/security-tools`, the
directory the checksum-verified scanner checks read. It installs exactly:

- the release tools of `ci/tooling/security-tools.lock.yml`, through the
  checksum-verifying `fetch_security_tool.py`;
- the Go tools of `ci/tooling/go-tools.lock.json`, built with the exact Go of
  `.go-version` after the module sum is verified, and checked afterwards
  against the binary's recorded build information.

A per-tool stamp records the lock entry that produced the binary; a missing,
changed or unstamped binary is replaced atomically. Nothing is installed
outside the selected directory. CI workflows fetch their tools explicitly.

Exit status: 0 ready, 1 provisioning failed, 77 a prerequisite is missing.
"""
from __future__ import annotations

import argparse
import datetime
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

BLOCKED = 77
SCHEMA = 1
ROOT = Path(__file__).resolve().parents[2]
RELEASE_LOCK = ROOT / "ci/tooling/security-tools.lock.yml"
GO_LOCK = ROOT / "ci/tooling/go-tools.lock.json"
GO_VERSION_FILE = ROOT / ".go-version"
SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
MODULE_PATH = re.compile(r"^[a-z0-9.-]+(?:/[A-Za-z0-9_.-]+)+$")
GO_RELEASE = re.compile(r"^v\d+\.\d+\.\d+$")
MODULE_SUM = re.compile(r"^h1:[A-Za-z0-9+/]{43}=$")
GO_FIELDS = ("module", "package", "version", "module_sum", "executable", "upstream", "license")


class Blocked(Exception):
    """A prerequisite of one tool is missing."""


def say(message: str) -> None:
    print(f"security-tools: {message}", file=sys.stderr, flush=True)


def load_fetcher():
    spec = importlib.util.spec_from_file_location(
        "fetch_security_tool", ROOT / "ci/tools/fetch_security_tool.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def release_tool_names() -> list[str]:
    """Return the two-space keys of the top-level `tools:` section."""
    names, inside = [], False
    for line in RELEASE_LOCK.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            inside = line == "tools:"
            continue
        match = re.fullmatch(r" {2}([a-z][a-z\d_]*):", line)
        if inside and match:
            names.append(match.group(1))
    if not names:
        raise ValueError("security tool lock has no tools section")
    return names


def go_records() -> dict[str, dict[str, str]]:
    data = json.loads(GO_LOCK.read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA or not isinstance(data.get("tools"), dict):
        raise ValueError("Go tool lock has an unsupported schema")
    records = {}
    for name, entry in data["tools"].items():
        if not SAFE_NAME.fullmatch(name) or not isinstance(entry, dict):
            raise ValueError("Go tool lock entry is malformed")
        record = {field: entry.get(field) for field in GO_FIELDS}
        if not all(isinstance(value, str) for value in record.values()):
            raise ValueError(f"{name}: incomplete Go tool lock entry")
        valid = (MODULE_PATH.fullmatch(record["module"])
                 and (record["package"] == record["module"]
                      or record["package"].startswith(record["module"] + "/"))
                 and GO_RELEASE.fullmatch(record["version"])
                 and MODULE_SUM.fullmatch(record["module_sum"])
                 and SAFE_NAME.fullmatch(record["executable"]))
        if not valid:
            raise ValueError(f"{name}: Go tool lock entry fails validation")
        records[name] = record
    return records


def go_toolchain() -> tuple[str, str]:
    """Return the go executable and its version; require .go-version exactly."""
    go = shutil.which("go")
    if go is None:
        raise Blocked("go is not on PATH")
    expected = "go" + GO_VERSION_FILE.read_text(encoding="ascii").strip()
    observed = subprocess.run([go, "env", "GOVERSION"], env=go_environment(), check=False,
                              capture_output=True, text=True).stdout.strip()
    if observed != expected:
        raise Blocked(f"go reports {observed or 'nothing'}, .go-version selects {expected}")
    return go, expected


def go_environment(gobin: Path | None = None) -> dict[str, str]:
    child = dict(os.environ)
    child.update(GOTOOLCHAIN="local", CGO_ENABLED="0", GOFLAGS="-trimpath")
    if gobin is not None:
        child["GOBIN"] = str(gobin)
    return child


def stamp_path(destination: Path, executable: str) -> Path:
    return destination / f".{executable}.lock-record.json"


def file_identity(path: Path) -> dict[str, int]:
    observed = path.lstat()
    return {"size": observed.st_size, "mtime_ns": observed.st_mtime_ns}


def is_current(destination: Path, executable: str, expected: dict) -> bool:
    target = destination / executable
    if target.is_symlink() or not target.is_file() or not os.access(target, os.X_OK):
        return False
    try:
        stamp = json.loads(stamp_path(destination, executable).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return stamp.get("source") == expected and stamp.get("file") == file_identity(target)


def build_go_tool(name: str, record: dict[str, str], go: str, go_version: str,
                  staging: Path) -> Path:
    module = f"{record['module']}@{record['version']}"
    downloaded = subprocess.run([go, "mod", "download", "-json", module], env=go_environment(),
                                cwd=staging, check=False, capture_output=True, text=True)
    try:
        observed_sum = json.loads(downloaded.stdout).get("Sum")
    except ValueError:
        observed_sum = None
    if downloaded.returncode or observed_sum != record["module_sum"]:
        raise RuntimeError(f"{name}: module sum of {module} does not match the lock")
    package = f"{record['package']}@{record['version']}"
    if subprocess.run([go, "install", package], env=go_environment(staging), cwd=staging,
                      check=False).returncode:
        raise RuntimeError(f"{name}: go install {package} failed")
    binary = staging / record["executable"]
    info = subprocess.run([go, "version", "-m", str(binary)], env=go_environment(),
                          check=False, capture_output=True, text=True).stdout
    expected_lines = (f": {go_version}", f"\tpath\t{record['package']}",
                      f"\tmod\t{record['module']}\t{record['version']}\t{record['module_sum']}")
    if not all(line in info for line in expected_lines):
        raise RuntimeError(f"{name}: built binary's build information differs from the lock")
    return binary


def install(destination: Path, name: str, executable: str, source: dict, staged: Path) -> None:
    """Move the verified binary into place, then record its producing lock entry.

    The old stamp is removed first, so a failure at any later step leaves an
    unstamped binary that the next run replaces.
    """
    target = destination / executable
    stamp_file = stamp_path(destination, executable)
    try:
        stamp_file.unlink(missing_ok=True)
        os.replace(staged, target)
    except OSError as error:
        raise RuntimeError(f"{name}: cannot install {target}: {error}") from error
    try:
        stamp = {"schema": SCHEMA, "tool": name, "source": source,
                 "file": file_identity(target),
                 "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                 "installed_utc": datetime.datetime.now(datetime.timezone.utc)
                 .strftime("%Y-%m-%dT%H:%M:%SZ")}
        partial = stamp_file.with_suffix(".tmp")
        partial.write_text(json.dumps(stamp, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(partial, stamp_file)
    except OSError as error:
        raise RuntimeError(f"{name}: installed but cannot record its stamp: {error}") from error


class Provisioner:
    def __init__(self, destination: Path, verbose: bool) -> None:
        self.destination = destination
        self.verbose = verbose
        self.fetcher = load_fetcher()
        self.go_records = go_records()
        self._go: tuple[str, str] | None = None

    def known(self) -> list[str]:
        return release_tool_names() + sorted(self.go_records)

    def go(self) -> tuple[str, str]:
        if self._go is None:
            self._go = go_toolchain()
        return self._go

    def source(self, name: str) -> tuple[str, dict]:
        if name in self.go_records:
            record = self.go_records[name]
            return record["executable"], {"kind": "go", "record": record,
                                          "go": self.go()[1]}
        record = self.fetcher.record(name)
        return record["executable"], {"kind": "release", "record": record}

    def ensure(self, name: str) -> None:
        executable, source = self.source(name)
        if is_current(self.destination, executable, source):
            if self.verbose:
                say(f"{name} current: {self.destination / executable}")
            return
        say(f"installing {name} {source['record']['version']} into {self.destination}")
        with tempfile.TemporaryDirectory(prefix=".staging-", dir=self.destination,
                                         ignore_cleanup_errors=True) as temporary:
            staging = Path(temporary)
            if source["kind"] == "go":
                go, go_version = self.go()
                staged = build_go_tool(name, source["record"], go, go_version, staging)
            else:
                staged = self.fetcher.fetch_record(name, source["record"], staging / "bin")
            install(self.destination, name, executable, source, staged)
        say(f"{name} ready: {self.destination / executable}")


def tool_detail(name: str, error: Exception) -> str:
    """Prefix the tool name once; the fetcher's own messages already carry it."""
    detail = str(error)
    return detail if detail.startswith(f"{name}:") else f"{name}: {detail}"


def prepare_destination(destination: Path) -> Path:
    if not destination.is_absolute():
        raise Blocked("the tool directory must be absolute and outside the checkout")
    if destination.is_symlink():
        raise Blocked(f"{destination} must not be a symlink")
    configured = os.environ.get("RUNNER_TEMP", "")
    if not configured or not Path(configured).is_absolute():
        raise Blocked("RUNNER_TEMP must select an absolute run-private directory")
    approved = Path(configured).resolve() / "security-tools"
    if approved.is_relative_to(ROOT):
        raise Blocked("the tool directory must be absolute and outside the checkout")
    if approved.is_symlink():
        raise Blocked(f"{approved} must not be a symlink")
    if destination.resolve() != approved:
        raise Blocked("--destination must match RUNNER_TEMP/security-tools")
    approved.mkdir(mode=0o700, parents=True, exist_ok=True)
    approved.chmod(0o700)
    return approved


def run(destination: Path, selected: list[str], verbose: bool) -> int:
    destination = prepare_destination(destination)
    provisioner = Provisioner(destination, verbose)
    known = provisioner.known()
    unknown = sorted(set(selected) - set(known))
    if unknown:
        raise ValueError("unknown tool: " + ", ".join(unknown))
    canonical = {name: name for name in known}
    names = [canonical[name] for name in selected] if selected else known
    status = 0
    descriptor = os.open(destination, os.O_RDONLY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        for name in names:
            try:
                provisioner.ensure(name)
            except Blocked as error:
                print(f"BLOCKED: security-tools: {tool_detail(name, error)}", file=sys.stderr)
                if status == 0:
                    status = BLOCKED
            except (OSError, RuntimeError, ValueError, tarfile.TarError,
                    subprocess.SubprocessError) as error:
                print(f"FAIL: security-tools: {tool_detail(name, error)}", file=sys.stderr)
                status = 1
    finally:
        os.close(descriptor)
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--destination", type=Path, required=True,
                        help="confirm the RUNNER_TEMP/security-tools directory")
    parser.add_argument("--tool", action="append", default=[], help="limit to this tool")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    try:
        return run(args.destination, args.tool, args.verbose)
    except Blocked as error:
        print(f"BLOCKED: security-tools: {error}", file=sys.stderr)
        return BLOCKED
    except (OSError, ValueError) as error:
        print(f"FAIL: security-tools: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
