from __future__ import annotations

import importlib.util
import io
import json
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
        self.headers["Content-Length"] = str(len(body) if content_length is None else content_length)
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
    def root_with_version(self, root: Path, version: str = "1.26.5") -> Path:
        root.mkdir(parents=True, exist_ok=True)
        (root / ".go-version").write_text(f"{version}\n", encoding="utf-8")
        return root

    def run_cli(
        self,
        root: Path,
        argv: list[str],
        *,
        opener: FakeOpener | None = None,
        metadata=updater._UNSET,
    ) -> tuple[int, dict[str, object]]:
        output = io.StringIO()
        status = updater.main(argv, root=root, opener=opener, metadata=metadata, output=output)
        return status, json.loads(output.getvalue())

    def test_selects_highest_stable_current_minor_patch(self) -> None:
        metadata = [
            release("go1.26.0"),
            release("go1.26.5"),
            release("go1.27rc1", stable=False),
            release("go1.27.1"),
            release("go1.26.8"),
        ]
        self.assertEqual("1.26.8", str(updater.resolve_latest_stable_version(metadata=metadata)))

    def test_check_and_update_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.root_with_version(Path(temporary))
            status, decision = self.run_cli(root, ["--check", "--json"], metadata=[release("go1.26.6")])
            update_status, update = self.run_cli(
                root,
                ["--update", "--expected-version", "1.26.6", "--json"],
                metadata=[release("go1.26.6")],
            )
            content = (root / ".go-version").read_text(encoding="utf-8")
            current_status, current = self.run_cli(
                root,
                ["--update", "--expected-version", "1.26.6", "--json"],
                metadata=[release("go1.26.6")],
            )
        self.assertEqual(0, status)
        self.assertEqual("update_available", decision["status"])
        self.assertIs(decision["update_available"], True)
        self.assertEqual(0, update_status)
        self.assertIs(update["changed"], True)
        self.assertEqual("1.26.6\n", content)
        self.assertEqual(0, current_status)
        self.assertEqual("current", current["status"])
        self.assertIs(current["changed"], False)

    def test_update_rejects_downgrade_or_wrong_expected_version_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.root_with_version(Path(temporary), "1.26.6")
            downgrade_status, downgrade = self.run_cli(
                root,
                ["--update", "--expected-version", "1.26.5", "--json"],
                metadata=[release("go1.26.5")],
            )
            mismatch_status, mismatch = self.run_cli(
                root,
                ["--update", "--expected-version", "1.26.7", "--json"],
                metadata=[release("go1.26.6")],
            )
            content = (root / ".go-version").read_text(encoding="utf-8")
        self.assertEqual((1, "error"), (downgrade_status, downgrade["status"]))
        self.assertEqual((1, "error"), (mismatch_status, mismatch["status"]))
        self.assertEqual("1.26.6\n", content)

    def test_rejects_noncurrent_minor_prerelease_and_leading_zero_forms(self) -> None:
        for value in ("1.27.1", "go1.26.6", "1.26.06", "1.26.6rc1", "1.26.١"):
            with self.subTest(value=value), self.assertRaises(updater.VersionError):
                updater.parse_stable_version(value)
        with self.assertRaises(updater.MetadataError):
            updater.resolve_latest_stable_version(metadata=[release("go1.26.6rc1")])
        with self.assertRaises(updater.MetadataError):
            updater.resolve_latest_stable_version(metadata=[{"version": "go1.26.6", "stable": "true"}])

    def test_metadata_transport_and_schema_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.root_with_version(Path(temporary))
            cases = (
                FakeOpener(FakeResponse(b"{")),
                FakeOpener(FakeResponse(b"[]", content_type="text/html")),
                FakeOpener(FakeResponse(b"[]", content_length=3)),
                FakeOpener(FakeResponse(b"[]", url="https://mirror.invalid/dl/?mode=json")),
                FakeOpener(error=urllib.error.URLError("offline")),
            )
            for opener in cases:
                with self.subTest(opener=opener):
                    status, record = self.run_cli(root, ["--check", "--json"], opener=opener)
                    self.assertEqual((1, "error"), (status, record["status"]))
        with self.assertRaises(updater.MetadataError):
            updater._decode_metadata(b'[{"version":"go1.26.6","version":"go1.26.7","stable":true}]')

    def test_noncanonical_endpoint_is_rejected_before_opening(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.root_with_version(Path(temporary))
            opener = FakeOpener(FakeResponse(b"[]"))
            invalid = urllib.parse.urlunsplit(("https", "go.dev", "/dl/", "mode=json&include=all", ""))
            with mock.patch.object(updater, "RELEASE_API_URL", invalid):
                status, record = self.run_cli(root, ["--check", "--json"], opener=opener)
        self.assertEqual((1, "error"), (status, record["status"]))
        self.assertEqual([], opener.requests)

    def test_symlink_target_is_refused_without_touching_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            outside = root / "outside-version"
            outside.write_text("1.26.5\n", encoding="utf-8")
            (root / ".go-version").symlink_to(outside)
            status, record = self.run_cli(
                root,
                ["--update", "--expected-version", "1.26.6", "--json"],
                metadata=[release("go1.26.6")],
            )
            content = outside.read_text(encoding="utf-8")
        self.assertEqual((1, "error"), (status, record["status"]))
        self.assertEqual("1.26.5\n", content)


if __name__ == "__main__":
    unittest.main()
