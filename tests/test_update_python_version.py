from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update-python-version.py"


def load_module():
    spec = importlib.util.spec_from_file_location("update_python_version", SCRIPT)
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


def release(name: str, *, published: bool = True, prerelease: bool = False) -> dict[str, object]:
    return {
        "name": name,
        "is_published": published,
        "pre_release": prerelease,
    }


class UpdatePythonVersionTests(unittest.TestCase):
    def _root_with_version(self, root: Path, version: str = "3.13.14") -> Path:
        root.mkdir(parents=True, exist_ok=True)
        (root / ".python-version").write_text(f"{version}\n", encoding="utf-8")
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

    def test_selects_highest_stable_patch_while_ignoring_prerelease_and_wrong_minor(self):
        metadata = [
            release("Python 3.13.0"),
            release("Python 3.13.14"),
            release("Python 3.13.99rc1", prerelease=True),
            release("Python 3.12.99"),
            release("Python 3.13.16"),
        ]
        self.assertEqual(str(updater.resolve_latest_stable_version(metadata=metadata)), "3.13.16")

    def test_zero_patch_is_a_valid_canonical_stable_version(self):
        metadata = [release("Python 3.13.0")]
        self.assertEqual(str(updater.resolve_latest_stable_version(metadata=metadata)), "3.13.0")

        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "3.13.0")
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "3.13.0", "--json"],
                metadata=metadata,
            )

        self.assertEqual(result, 0)
        self.assertEqual(record["status"], "current")
        self.assertEqual(record["latest_version"], "3.13.0")
        self.assertIs(record["update_available"], False)
        self.assertIs(record["changed"], False)

    def test_check_reports_update_available_in_stable_json(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "3.13.14")
            result, record = self._run_cli(
                root,
                ["--check", "--json"],
                metadata=[release("Python 3.13.15")],
            )

        self.assertEqual(result, 0)
        self.assertEqual(record["status"], "update_available")
        self.assertEqual(record["current_version"], "3.13.14")
        self.assertEqual(record["latest_version"], "3.13.15")
        self.assertIs(record["update_available"], True)
        self.assertNotIn("changed", record)

    def test_check_reports_current_in_stable_json(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "3.13.15")
            result, record = self._run_cli(
                root,
                ["--check", "--json"],
                metadata=[release("Python 3.13.15")],
            )

        self.assertEqual(result, 0)
        self.assertEqual(record["status"], "current")
        self.assertEqual(record["current_version"], "3.13.15")
        self.assertEqual(record["latest_version"], "3.13.15")
        self.assertIs(record["update_available"], False)

    def test_update_replaces_version_atomically_and_reports_changed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "3.13.14")
            target = root / ".python-version"
            original_mode = target.stat().st_mode & 0o777
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "3.13.15", "--json"],
                metadata=[release("Python 3.13.15")],
            )
            content = target.read_text(encoding="utf-8")
            updated_mode = target.stat().st_mode & 0o777

        self.assertEqual(result, 0)
        self.assertEqual(record["status"], "update_available")
        self.assertIs(record["update_available"], True)
        self.assertIs(record["changed"], True)
        self.assertEqual(content, "3.13.15\n")
        self.assertEqual(updated_mode, original_mode)

    def test_update_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "3.13.15")
            target = root / ".python-version"
            before = target.stat()
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "3.13.15", "--json"],
                metadata=[release("Python 3.13.15")],
            )
            after = target.stat()

        self.assertEqual(result, 0)
        self.assertEqual(record["status"], "current")
        self.assertIs(record["update_available"], False)
        self.assertIs(record["changed"], False)
        self.assertEqual((after.st_ino, after.st_mtime_ns), (before.st_ino, before.st_mtime_ns))

    def test_leading_zero_current_version_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "3.13.00")
            result, record = self._run_cli(
                root,
                ["--check", "--json"],
                metadata=[release("Python 3.13.15")],
            )
            content = (root / ".python-version").read_text(encoding="utf-8")

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "error")
        self.assertEqual(content, "3.13.00\n")

    def test_update_rejects_downgrade(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "3.13.15")
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "3.13.14", "--json"],
                metadata=[release("Python 3.13.14")],
            )
            content = (root / ".python-version").read_text(encoding="utf-8")

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "error")
        self.assertEqual(content, "3.13.15\n")

    def test_expected_version_mismatch_rejects_update_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary), "3.13.14")
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "3.13.16", "--json"],
                metadata=[release("Python 3.13.15")],
            )
            content = (root / ".python-version").read_text(encoding="utf-8")

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "error")
        self.assertEqual(content, "3.13.14\n")

    def test_expected_version_must_be_an_exact_supported_series(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary))
            opener = FakeOpener(FakeResponse(b"[]"))
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "3.14.1", "--json"],
                opener=opener,
            )

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "error")
        self.assertEqual(opener.requests, [])

    def test_expected_version_rejects_a_leading_zero_patch(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary))
            opener = FakeOpener(FakeResponse(b"[]"))
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "3.13.00", "--json"],
                opener=opener,
            )

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "error")
        self.assertEqual(opener.requests, [])

    def test_malformed_json_is_rejected(self):
        self._assert_metadata_failure(FakeResponse(b"{"))

    def test_truncated_metadata_is_rejected(self):
        self._assert_metadata_failure(FakeResponse(b"[]", content_length=3))

    def test_non_json_body_is_rejected(self):
        self._assert_metadata_failure(FakeResponse(b"<html>not-json</html>"))

    def test_bad_content_type_is_rejected(self):
        self._assert_metadata_failure(FakeResponse(b"[]", content_type="text/html"))

    def test_redirect_is_rejected(self):
        self._assert_metadata_failure(FakeResponse(b"[]", url="https://mirror.invalid/releases"))

    def test_network_error_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary))
            result, record = self._run_cli(
                root,
                ["--check", "--json"],
                opener=FakeOpener(error=urllib.error.URLError("offline")),
            )

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "error")

    def test_noncanonical_metadata_url_is_rejected_before_opening(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary))
            opener = FakeOpener(FakeResponse(b"[]"))
            with mock.patch.object(updater, "RELEASE_API_URL", "http://www.python.org/api/v2/downloads/release/?is_published=true"):
                result, record = self._run_cli(root, ["--check", "--json"], opener=opener)

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "error")
        self.assertEqual(opener.requests, [])

    def test_schema_with_unpublished_or_malformed_records_is_rejected(self):
        with self.subTest("unpublished"):
            with self.assertRaises(updater.MetadataError):
                updater.resolve_latest_stable_version(metadata=[release("Python 3.13.15", published=False)])
        with self.subTest("non-array"):
            with self.assertRaises(updater.MetadataError):
                updater.resolve_latest_stable_version(metadata={"objects": []})
        with self.subTest("bad-boolean"):
            with self.assertRaises(updater.MetadataError):
                updater.resolve_latest_stable_version(
                    metadata=[{"name": "Python 3.13.15", "is_published": "true", "pre_release": False}]
                )

    def test_symlink_target_is_refused_without_touching_its_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "outside-version"
            destination.write_text("3.13.14\n", encoding="utf-8")
            (root / ".python-version").symlink_to(destination)
            result, record = self._run_cli(
                root,
                ["--update", "--expected-version", "3.13.15", "--json"],
                metadata=[release("Python 3.13.15")],
            )
            destination_content = destination.read_text(encoding="utf-8")

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "error")
        self.assertEqual(destination_content, "3.13.14\n")

    def test_symlinked_root_path_is_refused(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            real_root = self._root_with_version(parent / "real")
            root_link = parent / "root-link"
            root_link.symlink_to(real_root, target_is_directory=True)
            result, record = self._run_cli(
                root_link,
                ["--check", "--json"],
                metadata=[release("Python 3.13.15")],
            )

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "error")

    def _assert_metadata_failure(self, response: FakeResponse) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self._root_with_version(Path(temporary))
            result, record = self._run_cli(root, ["--check", "--json"], opener=FakeOpener(response))

        self.assertEqual(result, 1)
        self.assertEqual(record["status"], "error")


if __name__ == "__main__":
    unittest.main()
