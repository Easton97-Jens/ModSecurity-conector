from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
import urllib.parse
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update-go-version.py"


def load_module():
    spec = importlib.util.spec_from_file_location("update_go_version", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


updater = load_module()


class FakeResponse:
    def __init__(
        self,
        body: bytes,
        *,
        content_type: str | None = "application/json; charset=utf-8",
        content_length: int | None = None,
        url: str | None = None,
        status: int = 200,
    ) -> None:
        self.body = body
        self.status = status
        self.url = updater.CANONICAL_RELEASE_API_URL if url is None else url
        self.headers: dict[str, str] = {}
        if content_type is not None:
            self.headers["Content-Type"] = content_type
        if content_length is None:
            content_length = len(body)
        self.headers["Content-Length"] = str(content_length)
        self.closed = False

    def read(self, size: int = -1) -> bytes:
        return self.body if size < 0 else self.body[:size]

    def geturl(self) -> str:
        return self.url

    def getcode(self) -> int:
        return self.status

    def close(self) -> None:
        self.closed = True


class FakeOpener:
    def __init__(self, response: FakeResponse | None = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.requests = []

    def open(self, request, timeout):
        self.requests.append((request, timeout))
        if self.error is not None:
            raise self.error
        if self.response is None:
            raise AssertionError("FakeOpener needs a response or an error")
        return self.response


def release(version: str, *, stable: bool = True) -> dict[str, object]:
    return {"version": version, "stable": stable}


class UpdateGoVersionTests(unittest.TestCase):
    def _root_with_version(self, root: Path, version: str = "1.26.4") -> Path:
        for relative in updater.MODULE_PATHS:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"module example.test/{relative.parent.name}\n\ngo {version}\n", encoding="utf-8")
        workflow = root / updater.CODEQL_WORKFLOW_PATH
        workflow.parent.mkdir(parents=True, exist_ok=True)
        workflow.write_text(
            """name: CodeQL\n\njobs:\n  envoy-go:\n    steps:\n      - uses: actions/setup-go@0123456789abcdef0123456789abcdef01234567 # v7.0.0\n        with:\n          go-version: '"""
            + version
            + """'\n  traefik-go:\n    steps:\n      - uses: actions/setup-go@0123456789abcdef0123456789abcdef01234567 # v7.0.0\n        with:\n          go-version: '"""
            + version
            + """'\n""",
            encoding="utf-8",
        )
        return root

    def _run_cli(
        self,
        root: Path,
        argv: list[str],
        *,
        opener: FakeOpener | None = None,
        metadata=updater._UNSET,
    ) -> tuple[int, dict[str, object]]:
        output = io.StringIO()
        result = updater.main(argv, root=root, opener=opener, metadata=metadata, output=output)
        return result, json.loads(output.getvalue())

    def _contract_text(self, root: Path) -> dict[Path, str]:
        return {relative: (root / relative).read_text(encoding="utf-8") for relative in updater.TARGET_PATHS}

    def test_selects_highest_stable_patch_without_crossing_minor(self):
        metadata = [
            release("go1.26.4"),
            release("go1.26.5"),
            release("go1.26.6rc1", stable=False),
            release("go1.27.0"),
            release("go1.20"),
            release("go1"),
            release("go1.25.99"),
        ]
        self.assertEqual(str(updater.resolve_latest_stable_version(metadata=metadata)), "1.26.5")

    def test_check_reports_patch_update_and_newer_minor_in_stable_json(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "1.26.4")
            result, record = self._run_cli(
                root,
                ["--check", "--json"],
                metadata=[release("go1.26.5"), release("go1.27.0")],
            )

        self.assertEqual(result, 0)
        self.assertEqual(record["status"], "patch_update_available")
        self.assertEqual(record["current_version"], "1.26.4")
        self.assertEqual(record["latest_version"], "1.26.5")
        self.assertIs(record["update_available"], True)
        self.assertIs(record["newer_minor_available"], True)
        self.assertEqual(record["newer_minor_version"], "1.27.0")
        self.assertNotIn("changed", record)

    def test_check_reports_newer_minor_without_selecting_it(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "1.26.5")
            result, record = self._run_cli(
                root,
                ["--check", "--json"],
                metadata=[release("go1.26.5"), release("go1.27.0")],
            )

        self.assertEqual(result, 0)
        self.assertEqual(record["status"], "newer_minor_available")
        self.assertEqual(record["latest_version"], "1.26.5")
        self.assertIs(record["update_available"], False)
        self.assertIs(record["newer_minor_available"], True)
        self.assertEqual(record["newer_minor_version"], "1.27.0")

    def test_no_approved_stable_patch_is_reported_separately(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "1.26.5")
            result, record = self._run_cli(
                root,
                ["--check", "--json"],
                metadata=[release("go1.25.99"), release("go1.27.0", stable=False)],
            )

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "no_stable_release")

    def test_update_replaces_only_all_three_contract_fields(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "1.26.4")
            before_paths = set(path.relative_to(root) for path in root.rglob("*"))
            original_modes = {
                relative: (root / relative).stat().st_mode & 0o777 for relative in updater.TARGET_PATHS
            }
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "1.26.5", "--json"],
                metadata=[release("go1.26.5")],
            )
            contents = self._contract_text(root)
            after_paths = set(path.relative_to(root) for path in root.rglob("*"))
            updated_modes = {
                relative: (root / relative).stat().st_mode & 0o777 for relative in updater.TARGET_PATHS
            }

        self.assertEqual(result, 0)
        self.assertEqual(record["status"], "patch_update_available")
        self.assertIs(record["changed"], True)
        self.assertEqual(before_paths, after_paths)
        for relative in updater.MODULE_PATHS:
            self.assertIn("go 1.26.5\n", contents[relative])
            self.assertNotIn("toolchain ", contents[relative])
        self.assertEqual(contents[updater.CODEQL_WORKFLOW_PATH].count("go-version: '1.26.5'"), 2)
        for relative, mode in original_modes.items():
            self.assertEqual(mode, updated_modes[relative])

    def test_update_is_idempotent_when_current(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "1.26.5")
            before = {relative: (root / relative).stat() for relative in updater.TARGET_PATHS}
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "1.26.5", "--json"],
                metadata=[release("go1.26.5")],
            )
            after = {relative: (root / relative).stat() for relative in updater.TARGET_PATHS}

        self.assertEqual(result, 0)
        self.assertEqual(record["status"], "current")
        self.assertIs(record["changed"], False)
        for relative in updater.TARGET_PATHS:
            self.assertEqual((after[relative].st_ino, after[relative].st_mtime_ns), (before[relative].st_ino, before[relative].st_mtime_ns))

    def test_update_rejects_downgrade_without_touching_contract(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "1.26.5")
            before = self._contract_text(root)
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "1.26.4", "--json"],
                metadata=[release("go1.26.4")],
            )
            after = self._contract_text(root)

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "invalid_current_version")
        self.assertEqual(before, after)

    def test_expected_version_mismatch_fails_before_writing(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "1.26.4")
            before = self._contract_text(root)
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "1.26.6", "--json"],
                metadata=[release("go1.26.5")],
            )
            after = self._contract_text(root)

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "candidate_failed")
        self.assertEqual(before, after)

    def test_inconsistent_contract_is_rejected_without_touching_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "1.26.4")
            (root / updater.MODULE_PATHS[1]).write_text("module example.test/traefik\n\ngo 1.26.3\n", encoding="utf-8")
            before = self._contract_text(root)
            result, record = self._run_cli(root, ["--check", "--json"], metadata=[release("go1.26.5")])
            after = self._contract_text(root)

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "invalid_current_version")
        self.assertEqual(before, after)

    def test_explicit_toolchain_directive_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "1.26.5")
            target = root / updater.MODULE_PATHS[0]
            target.write_text(target.read_text(encoding="utf-8") + "toolchain go1.26.5\n", encoding="utf-8")
            result, record = self._run_cli(root, ["--check", "--json"], metadata=[release("go1.26.5")])

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "invalid_current_version")

    def test_symlink_target_is_rejected_without_touching_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "1.26.4")
            target = root / updater.MODULE_PATHS[0]
            destination = root / "outside-go-mod"
            destination.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
            target.unlink()
            target.symlink_to(destination)
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "1.26.5", "--json"],
                metadata=[release("go1.26.5")],
            )
            destination_content = destination.read_text(encoding="utf-8")

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "invalid_current_version")
        self.assertIn("go 1.26.4", destination_content)

    def test_malformed_or_redirected_metadata_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary))
            malformed_result, malformed_record = self._run_cli(
                root,
                ["--check", "--json"],
                opener=FakeOpener(FakeResponse(b"{")),
            )
            redirected_result, redirected_record = self._run_cli(
                root,
                ["--check", "--json"],
                opener=FakeOpener(FakeResponse(b"[]", url="https://mirror.invalid/dl/")),
            )

        self.assertEqual(malformed_result, 1)
        self.assertEqual(malformed_record["status"], "blocked_metadata")
        self.assertEqual(redirected_result, 1)
        self.assertEqual(redirected_record["status"], "blocked_metadata")

    def test_noncanonical_metadata_url_is_rejected_before_opening(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary))
            opener = FakeOpener(FakeResponse(b"[]"))
            invalid_url = urllib.parse.urlunsplit(
                ("http", "go.dev", "/dl/", "mode=json&include=all", "")
            )
            with mock.patch.object(updater, "RELEASE_API_URL", invalid_url):
                result, record = self._run_cli(root, ["--check", "--json"], opener=opener)

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "blocked_metadata")
        self.assertEqual(opener.requests, [])

    def test_network_error_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary))
            result, record = self._run_cli(
                root,
                ["--check", "--json"],
                opener=FakeOpener(error=urllib.error.URLError("offline")),
            )

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "blocked_network")


if __name__ == "__main__":
    unittest.main()
