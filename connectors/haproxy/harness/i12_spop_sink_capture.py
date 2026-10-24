#!/usr/bin/env python3
"""Retain argv, exits and physical artifacts from native SPOP sink controls.

Runs the existing production-source sink tests, including their unsafe
mutations, with compiler/process commands proxied through RTK. This is native
C and physical stdio evidence, independent of private HAProxy host evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import unittest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    output = arguments.output
    authorized = Path("/var/tmp/codex/ModSecurity-conector")
    if (not output.is_absolute() or output != output.resolve()
            or not output.is_relative_to(authorized) or output.exists()):
        parser.error("output must be a fresh absolute directory below the external project root")
    output.mkdir(parents=True)
    root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(root))
    os.environ["RUNNER_TEMP"] = str(output)
    from tests.test_haproxy_spop_event_sink_failures import HaproxySpopEventSinkFailureTests

    receipts = []
    original = subprocess.run

    def observed(argv, **kwargs):
        actual = ["rtk", "proxy", *argv]
        started = time.time_ns()
        result = original(actual, **kwargs)
        index = len(receipts)
        for name in ("stdout", "stderr"):
            data = getattr(result, name)
            if data is not None:
                (output / f"command-{index:03d}.{name}").write_bytes(data.encode() if isinstance(data, str) else data)
        receipts.append({"argv": actual, "cwd": str(kwargs.get("cwd", Path.cwd())),
                         "exit": result.returncode, "started_ns": started, "finished_ns": time.time_ns()})
        (output / "commands.json").write_text(json.dumps(receipts, indent=2) + "\n")
        return result

    subprocess.run = observed
    try:
        HaproxySpopEventSinkFailureTests.setUpClass()
        # Preserve generated C, compiled current/unsafe binaries and every
        # resulting physical sink after assertions, before normal cleanup.
        stream = io.StringIO()
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(HaproxySpopEventSinkFailureTests)
        # setUpClass already ran under observation; prevent a second build.
        HaproxySpopEventSinkFailureTests.setUpClass = classmethod(lambda cls: None)
        retained = output / "native-artifacts"
        unittest_result = None
        original_cleanup = HaproxySpopEventSinkFailureTests.doClassCleanups

        def retain_and_clean(cls):
            shutil.copytree(cls.directory, retained)
            original_cleanup()

        HaproxySpopEventSinkFailureTests.doClassCleanups = classmethod(retain_and_clean)
        unittest_result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        (output / "tests.log").write_text(stream.getvalue())
        files = {str(path.relative_to(output)): hashlib.sha256(path.read_bytes()).hexdigest()
                 for path in output.rglob("*") if path.is_file()}
        (output / "receipt.json").write_text(json.dumps({"evidence_class": "native-C-physical-stdio",
            "full_lifecycle_pass": False, "tests_run": unittest_result.testsRun,
            "failures": len(unittest_result.failures), "errors": len(unittest_result.errors),
            "files": files}, indent=2) + "\n")
        return 0 if unittest_result.wasSuccessful() else 1
    finally:
        subprocess.run = original


if __name__ == "__main__":
    raise SystemExit(main())
