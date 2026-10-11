"""Executable Common runtime policy evidence using genuine libModSecurity."""
from dataclasses import dataclass
from pathlib import Path
import os
import re
import shlex
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def engine_fixture_arguments(directory, limit, action, mode, length, chunk, marker):
    if limit is None or action is None:
        raise ValueError("response fixture requires explicit SecResponseBodyLimit and SecResponseBodyLimitAction")
    if limit <= 0 or action not in ("Reject", "ProcessPartial"):
        raise ValueError("invalid explicit engine response policy")
    return [str(directory), str(limit), action, mode, str(length), str(chunk), str(marker)]


@dataclass(frozen=True)
class NativeRequestPolicy:
    limit: int
    no_files_limit: int
    action: str
    engine_mode: str


@dataclass(frozen=True)
class RequestPayload:
    body_mode: str
    length: int
    chunk: int
    marker: int
    input_kind: str


def request_fixture_arguments(directory, policy, payload):
    if policy.limit is None or policy.no_files_limit is None or policy.action is None:
        raise ValueError("request fixture requires explicit SecRequestBodyLimit, SecRequestBodyNoFilesLimit and SecRequestBodyLimitAction")
    if policy.limit <= 0 or policy.no_files_limit <= 0 or policy.action not in ("Reject", "ProcessPartial"):
        raise ValueError("invalid explicit engine request policy")
    return ["--request", str(directory), str(policy.limit), str(policy.no_files_limit), policy.action,
            policy.engine_mode, payload.body_mode, str(payload.length), str(payload.chunk),
            str(payload.marker), payload.input_kind]


class EngineResponseLimits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(os.environ.get("CODEX_RUN_ROOT", "/var/tmp/codex/ModSecurity-conector/runs"))
        root.mkdir(parents=True, exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(prefix="engine-response-limits-", dir=root)
        cls.addClassCleanup(cls.temp.cleanup)
        cls.directory = Path(cls.temp.name)
        cls.binary = cls.directory / "engine-limit"
        command = shlex.split(os.environ.get("CC", "cc")) + [
            "-std=c17", "-Wall", "-Wextra", "-Werror", "-I.", "-Icommon/include",
            "tests/engine_response_limit_test.c", "common/runtime/msconnector_runtime.c",
        ] + [str(p.relative_to(ROOT)) for p in sorted((ROOT / "common/src").glob("*.c"))] + [
            "connectors/profile_registry.c", "-lmodsecurity", "-pthread", "-o", str(cls.binary)]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=90)
        if result.returncode:
            raise AssertionError("real libModSecurity test compilation failed:\n" + result.stdout + result.stderr)

    def run_case(self, limit, action, mode, length, chunk, marker):
        with tempfile.TemporaryDirectory(dir=self.directory) as directory:
            args = engine_fixture_arguments(directory, limit, action, mode, length, chunk, marker)
            result = subprocess.run([str(self.binary)] + args, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            print(result.stdout.strip())

    def test_boundaries_actions_chunking_and_modes(self):
        for limit in (128, 1024):
            for action in ("Reject", "ProcessPartial"):
                for mode in ("off", "safe", "strict"):
                    for delta in (-1, 0, 1):
                        for chunk in (17, 65536):
                            with self.subTest(limit=limit, action=action, mode=mode, delta=delta, chunk=chunk):
                                self.run_case(limit, action, mode, limit + delta, chunk, 0)

    def test_engine_partial_prefix_excludes_marker_after_limit(self):
        for mode in ("off", "safe", "strict"):
            self.run_case(128, "ProcessPartial", mode, 256, 17, 160)

    def test_marker_after_old_one_megabyte_connector_default(self):
        for mode in ("off", "safe", "strict"):
            self.run_case(3 * 1024 * 1024, "Reject", mode, 2 * 1024 * 1024, 65536, 1536 * 1024)
            self.run_case(1536 * 1024, "ProcessPartial", mode, 2 * 1024 * 1024, 65536, 1200 * 1024)

    def run_request_case(self, policy, payload):
        with tempfile.TemporaryDirectory(dir=self.directory) as directory:
            arguments = request_fixture_arguments(directory, policy, payload)
            result = subprocess.run([str(self.binary)] + arguments,
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            print(result.stdout.strip())
            return result.stdout

    def test_detection_only_native_actions_have_different_observed_prefixes(self):
        payload = RequestPayload("streaming", 256, 17, 160, "memory")
        observed = {}
        for action in ("Reject", "ProcessPartial"):
            output = self.run_request_case(NativeRequestPolicy(128, 128, action, "DetectionOnly"), payload)
            match = re.search(r"native_prefix=(\d+)", output)
            self.assertIsNotNone(match)
            observed[action] = int(match.group(1))
        self.assertEqual(observed, {"Reject": 120, "ProcessPartial": 128})

    def test_request_boundaries_actions_modes_and_chunking(self):
        for limit in (128, 1024):
            for action in ("Reject", "ProcessPartial"):
                for engine_mode in ("On", "DetectionOnly"):
                    for body_mode in ("buffered", "streaming"):
                        for delta in (-1, 0, 1):
                            for chunk in (17, 65536):
                                with self.subTest(limit=limit, action=action, engine=engine_mode,
                                                  mode=body_mode, delta=delta, chunk=chunk):
                                    self.run_request_case(NativeRequestPolicy(limit, limit, action, engine_mode), RequestPayload(body_mode, limit + delta, chunk, 0, "memory"))

    def test_genuine_http_service_large_request_before_companion_handoff(self):
        binary = self.directory / "http-stream"
        command = shlex.split(os.environ.get("CC", "cc")) + [
            "-std=c17", "-Wall", "-Wextra", "-Werror", "-I.", "-Icommon/include",
            "tests/engine_http_request_stream_test.c", "common/runtime/msconnector_runtime.c",
        ] + [str(p.relative_to(ROOT)) for p in sorted((ROOT / "common/src").glob("*.c"))] + [
            "connectors/profile_registry.c", "-lmodsecurity", "-pthread", "-o", str(binary)]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=90)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for limit, action, marker, expected_status in (
            (3 * 1024 * 1024, "Reject", 1536 * 1024, 451),
            (1024 * 1024, "ProcessPartial", 1536 * 1024, 200),
            (3 * 1024 * 1024, "Reject", 0, 200),
            (1024 * 1024, "Reject", 0, 403),
        ):
            with tempfile.TemporaryDirectory(dir=self.directory) as directory:
                result = subprocess.run([str(binary), directory, str(limit), str(limit), action,
                    str(2 * 1024 * 1024), str(marker), str(expected_status)],
                    capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_native_multipart_no_files_limit_eos(self):
        for engine_mode in ("On", "DetectionOnly"):
            for action in ("Reject", "ProcessPartial"):
                self.run_request_case(NativeRequestPolicy(1024, 128, action, engine_mode),
                    RequestPayload("streaming", 256, 17, 160, "multipart"))

    def test_request_no_files_limit_differs_from_total_limit(self):
        for engine_mode in ("On", "DetectionOnly"):
            for action in ("Reject", "ProcessPartial"):
                self.run_request_case(NativeRequestPolicy(1024, 128, action, engine_mode), RequestPayload("streaming", 256, 17, 160, "urlencoded"))

    def test_request_file_input_and_two_engine_limits_for_same_payload(self):
        for engine_mode in ("On", "DetectionOnly"):
            for action in ("Reject", "ProcessPartial"):
                for limit in (128, 1024):
                    self.run_request_case(NativeRequestPolicy(limit, limit, action, engine_mode), RequestPayload("buffered", 256, 17, 160, "file"))

    def test_request_markers_after_old_connector_limit(self):
        for input_kind in ("memory", "file"):
            for engine_mode in ("On", "DetectionOnly"):
                for limit in (1536 * 1024, 3 * 1024 * 1024):
                    self.run_request_case(NativeRequestPolicy(limit, limit, "ProcessPartial", engine_mode), RequestPayload("streaming", 2 * 1024 * 1024, 65536, 1700 * 1024, input_kind))

    def test_request_helpers_require_each_native_policy_parameter(self):
        for limit, no_files_limit, action in ((None, 128, "Reject"), (128, None, "Reject"), (128, 128, None)):
            policy = NativeRequestPolicy(limit, no_files_limit, action, "On")
            payload = RequestPayload("buffered", 128, 17, 0, "memory")
            with self.assertRaisesRegex(ValueError, "requires explicit"):
                request_fixture_arguments(self.directory, policy, payload)
        result = subprocess.run([str(self.binary), "--request"], capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertIn("request required:", result.stderr)

    def test_product_configuration_allows_omitted_engine_directives_without_inspection(self):
        result = subprocess.run([str(self.binary), "--config-only", str(self.directory)],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("no response inspection", result.stdout)

    def test_missing_policy_parameters_fail_readably(self):
        for limit, action in ((None, "Reject"), (128, None)):
            with self.assertRaisesRegex(ValueError, "requires explicit"):
                engine_fixture_arguments(self.directory, limit, action, "safe", 128, 17, 0)
        result = subprocess.run([str(self.binary)], capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertIn("required:", result.stderr)

if __name__ == "__main__":
    unittest.main()
