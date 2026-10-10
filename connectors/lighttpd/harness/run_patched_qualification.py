#!/usr/bin/env python3
"""Fail-closed composition contract for patched-native lighttpd qualification.

The existing namespace/lifecycle and P2 runners are reused by an injected
trusted executor. They do not yet produce the campaign extensions required
below. Consequently the CLI deliberately exits 77; fixture results alone
cannot qualify this profile. Injection is a Python integration seam, not a
CLI option for importing arbitrary evidence or bypassing the namespace.
An independent verifier must correlate every receipt with raw host, client,
upstream, namespace and process observations before it is accepted.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import re
import secrets
import stat
import sys
from typing import Callable, Mapping, Protocol

HARNESS = Path(__file__).resolve().parent
if str(HARNESS) not in sys.path:
    sys.path.insert(0, str(HARNESS))
from safe_runtime_output import create_private_runtime_directory  # noqa: E402

PROFILE = "lighttpd-patched-native"
ROLES = frozenset({"host", "module", "library", "rules", "build_manifest"})
CASES = {
    "allow": (200, "allow", 1),
    "p1": (403, "deny", 0),
    "p2": (403, "deny", 0),
    "p2-delayed": (403, "deny", 0),
    "request-boundary": (200, "allow", 1),
    "request-overlimit": (413, "deny", 0),
    "p3": (403, "deny", 1),
    "p4-safe": (200, "log_only", 1),
}
EXTENSIONS = frozenset({"client_abort", "dependency_failure", "keepalive", "overlap", "resources", "restart"})


class Blocked(RuntimeError):
    """The independent runtime boundary or producer is unavailable."""


class Failure(ValueError):
    """Observed evidence contradicts the qualification contract."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Failure(message)


def positive(value: object) -> bool:
    return type(value) is int and value > 0


def serialize_receipt(receipt: Mapping[str, object]) -> str:
    """Return one bounded canonical snapshot of an untrusted receipt."""
    try:
        serialized = json.dumps(receipt, sort_keys=True, allow_nan=False) + "\n"
    except (TypeError, ValueError) as error:
        raise Failure("start receipt is not finite JSON evidence") from error
    require(len(serialized.encode("utf-8")) <= 1048576, "start receipt exceeds bounded size")
    return serialized


@dataclass(frozen=True)
class Pin:
    path: Path
    sha256: str

    def observe(self) -> tuple[int, int, int, str]:
        require(self.path.is_absolute(), "input path must be absolute")
        require(re.fullmatch(r"[0-9a-f]{64}", self.sha256) is not None, "invalid SHA256 pin")
        require(self.path.resolve() == self.path, "input path contains a symlink")
        descriptor = os.open(self.path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            before = os.fstat(descriptor)
            require(stat.S_ISREG(before.st_mode), "input must be a regular file")
            require(not before.st_mode & 0o022, "input is group/world writable")
            digest = hashlib.sha256()
            while chunk := os.read(descriptor, 65536):
                digest.update(chunk)
            after = os.fstat(descriptor)
            require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns)
                    == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns),
                    "input changed during hashing")
            require(digest.hexdigest() == self.sha256, "input hash mismatch")
            return before.st_dev, before.st_ino, before.st_size, digest.hexdigest()
        finally:
            os.close(descriptor)


@dataclass(frozen=True)
class StartPlan:
    run_id: str
    index: int
    root: Path
    root_identity: str
    source_sha256: str
    pins: Mapping[str, Pin]
    namespace_launcher: Path = HARNESS / "run_no_crs_fixture_trusted_namespace.py"
    lifecycle_runner: Path = HARNESS / "run_patched_full_lifecycle.sh"
    phase2_runner: Path = HARNESS / "run_phase2_pre_upstream_gate.py"

    @property
    def lifecycle_command(self) -> tuple[str, ...]:
        """The canonical CLI invocation; environment stays executor-owned."""
        return ("/usr/bin/python3", str(self.namespace_launcher), "--timeout-seconds", "900",
                "--", "/bin/sh", str(self.lifecycle_runner))


class Executor(Protocol):
    def preflight(self, pins: Mapping[str, Pin], source_sha256: str) -> None:
        """Prove independent build provenance and canonical nonroot namespace.

        Must raise Blocked before starts if the enforced unshare/private
        noexec tmpfs/bwrap capability-drop boundary cannot be used. P2 must
        run in the same canonical boundary; the production namespace CLI
        currently only admits the lifecycle shell runner.
        """

    def run_start(self, plan: StartPlan) -> Mapping[str, object]:
        """Compose native runners and extensions, with bounded finally cleanup."""

    def verify(self, plan: StartPlan, receipt: Mapping[str, object]) -> bool:
        """Independently revalidate raw, run-local artifacts, never just booleans.

        Must reject stale/sibling/Stock/fixture-only artifacts; correlate
        pinned executable/mapped library/module/rules/source and namespace
        identities; verify actual process/socket stop and all resource samples.
        """


def validate_start(plan: StartPlan, value: Mapping[str, object]) -> tuple[int, int]:
    require(value.get("run_id") == plan.run_id and value.get("index") == plan.index,
            "stale or sibling start")
    require(value.get("profile") == PROFILE and value.get("evidence_origin") == "real_host",
            "wrong profile or fixture-only evidence")
    require(value.get("source_sha256") == plan.source_sha256, "source identity drift")
    require(value.get("pins") == {role: pin.sha256 for role, pin in plan.pins.items()}, "runtime identity drift")
    require(value.get("root_identity") == plan.root_identity, "output root identity drift")
    ns = value.get("namespace")
    require(isinstance(ns, dict), "missing namespace evidence")
    require(ns.get("launcher") == str(plan.namespace_launcher), "noncanonical namespace launcher")
    require(positive(ns.get("host_uid")) and ns.get("host_uid") == ns.get("host_euid"), "root or set-id caller")
    for flag in ("user", "mount", "pid", "private_propagation", "tmpfs_noexec", "tmpfs_nosuid", "tmpfs_nodev", "no_new_privs", "capabilities_zero", "further_userns_disabled"):
        require(ns.get(flag) is True, f"missing namespace enforcement: {flag}")
    require(value.get("engine_mode") == "On", "engine is not enforcing")
    identity = value.get("host_identity")
    require(isinstance(identity, list) and len(identity) == 2 and all(positive(x) for x in identity), "missing process identity")
    cases = value.get("cases")
    require(isinstance(cases, dict) and set(cases) == set(CASES), "incomplete phase/boundary probes")
    transaction_ids = []
    for name, expected in CASES.items():
        case = cases[name]
        require(isinstance(case, dict), "invalid case")
        require(type(case.get("status")) is int and type(case.get("backend_receipts")) is int,
                "status/receipt counts must be integers")
        require((case.get("status"), case.get("action"), case.get("backend_receipts")) == expected, f"case failed: {name}")
        token = case.get("host_transaction_id")
        require(isinstance(token, str) and re.fullmatch(r"lighttpd-[1-9][0-9]*-[1-9][0-9]*", token) is not None, "missing host transaction correlation")
        transaction_ids.append(token)
        require(token.startswith(f"lighttpd-{identity[0]}-"), "transaction belongs to a different host")
        if name in {"p1", "p2", "p2-delayed", "request-overlimit"}:
            require(case.get("upstream_connections") == 0 and case.get("upstream_headers") == 0, "blocked request leaked upstream")
        if name.startswith("p2") or name.startswith("request-"):
            require(case.get("predecision_upstream_connections") == 0, "P2 released upstream before its decision")
    require(len(set(transaction_ids)) == len(transaction_ids), "reused host transaction id")
    require(cases["p4-safe"].get("eos_count") == 1 and cases["p4-safe"].get("first_byte_before_eos") is True,
            "P4 Safe lifecycle unproved")
    require(value.get("limitations") == ["HTTP/1.1 identity mod_proxy entities", "P4 Safe log_only after commit"], "phase limitations not declared")
    ext = value.get("extensions")
    require(isinstance(ext, dict) and set(ext) == EXTENSIONS, "fixture-only success lacks campaign extensions")
    for name in ("client_abort", "dependency_failure"):
        probe = ext[name]
        require(isinstance(probe, dict) and probe.get("observed") is True and probe.get("bounded") is True,
                f"missing bounded failure: {name}")
        require(probe.get("recovery_status") == 200 and probe.get("recovery_host_identity") == identity,
                "recovery did not use the same host")
    keepalive = ext["keepalive"]
    require(isinstance(keepalive, dict) and keepalive.get("statuses") == [200, 403, 200, 403, 200]
            and keepalive.get("connection_count") == 1 and keepalive.get("distinct_transactions") == 5,
            "keepalive alternation unproved")
    overlap = ext["overlap"]
    require(isinstance(overlap, dict) and overlap.get("clients") == 4 and overlap.get("peak_active") == 4,
            "four-client overlap unproved")
    intervals = overlap.get("intervals")
    require(isinstance(intervals, list) and len(intervals) == 4, "missing overlap intervals")
    require(all(isinstance(x, list) and len(x) == 2 and all(type(t) in (int, float) and math.isfinite(t) for t in x)
                and x[0] < x[1] for x in intervals), "invalid overlap timestamps")
    require(max(x[0] for x in intervals) < min(x[1] for x in intervals), "clients never overlapped")
    resources = ext["resources"]
    require(isinstance(resources, dict) and set(resources) == {"before", "peak", "after"}, "missing resource samples")
    for sample in resources.values():
        require(isinstance(sample, dict) and sample.get("host_identity") == identity
                and all(positive(sample.get(key)) for key in ("rss_kib", "fds", "sockets")), "invalid resource sample")
    restart = ext["restart"]
    require(isinstance(restart, dict) and restart.get("controlled_stop") is True
            and restart.get("old_process_absent") is True and restart.get("new_allow_status") == 200
            and restart.get("new_host_identity") != identity
            and isinstance(restart.get("new_host_identity"), list)
            and len(restart["new_host_identity"]) == 2
            and all(positive(x) for x in restart["new_host_identity"]), "controlled restart unproved")
    cleanup = value.get("cleanup")
    require(cleanup == {"owned_processes_absent": True, "owned_listeners_absent": True,
                        "namespace_reaped": True, "unexpected_artifacts": []}, "cleanup failed or incomplete")
    require(all(cleanup[key] is True for key in ("owned_processes_absent", "owned_listeners_absent", "namespace_reaped")),
            "cleanup claims must be exact booleans")
    return tuple(identity)


def qualify(parent: Path, pins: Mapping[str, Pin], source_sha256: str,
            executor: Executor | None = None, *, caller: Callable[[], tuple[int, int]] = lambda: (os.getuid(), os.geteuid())) -> dict[str, object]:
    """Run three fresh isolated starts; return bounded diagnostic evidence only."""
    uid, euid = caller()
    if uid <= 0 or uid != euid:
        raise Blocked("canonical launcher requires a nonroot, non-set-id caller")
    require(set(pins) == ROLES, "all exact build inputs must be pinned")
    require(re.fullmatch(r"[0-9a-f]{64}", source_sha256) is not None, "source digest must be pinned")
    observed = {role: pin.observe() for role, pin in pins.items()}
    if executor is None:
        raise Blocked("independent campaign executor/provenance verifier unavailable; fixture-only runners cannot qualify")
    executor.preflight(pins, source_sha256)
    run_id = "lighttpd-patched-" + secrets.token_hex(16)
    receipts = []
    identities = set()
    for index in range(1, 4):
        with create_private_runtime_directory(parent, prefix=f".{run_id}-start-{index}-") as directory:
            root = parent / directory.name
            plan = StartPlan(run_id, index, root, directory.identity, source_sha256, pins)
            receipt = executor.run_start(plan)
            require(isinstance(receipt, dict), "missing start receipt")
            serialized = serialize_receipt(receipt)
            directory.write_text_atomic("attempt.json", serialized, "attempted start receipt")
            # Verify raw artifacts even when normalized evidence later fails.
            if executor.verify(plan, receipt) is not True:
                raise Failure("independent artifact/provenance verification rejected the start")
            require(serialize_receipt(receipt) == serialized,
                    "independent verifier mutated the start receipt")
            identity = validate_start(plan, receipt)
            require(identity not in identities, "starts reused a process identity")
            identities.add(identity)
            require({role: pin.observe() for role, pin in pins.items()} == observed, "input changed during campaign")
            directory.write_text_atomic("qualification.json", serialized, "start qualification receipt")
            receipts.append({"root": str(root), "identity": directory.identity, "host_identity": list(identity)})
    return {"profile": PROFILE, "result": "diagnostic_pass", "readiness_awarded": False,
            "catalog_promotion": False, "run_id": run_id, "source_sha256": source_sha256, "starts": receipts}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--source-sha256", required=True)
    parser.add_argument("--pin", nargs=3, action="append", required=True, metavar=("ROLE", "PATH", "SHA256"))
    args = parser.parse_args(argv)
    try:
        pins = {role: Pin(Path(path), digest) for role, path, digest in args.pin}
        require(len(pins) == len(args.pin), "duplicate input role")
        qualify(args.parent, pins, args.source_sha256)
    except Blocked as error:
        print(f"lighttpd patched qualification: BLOCKED: {error}", file=sys.stderr)
        return 77
    except (Failure, OSError, ValueError) as error:
        print(f"lighttpd patched qualification: FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
