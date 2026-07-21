from __future__ import annotations

import importlib.util
import sys
import tarfile
import tempfile
import unittest
import urllib.request
from email.message import Message
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ci" / "tools" / "fetch_security_tool.py"


def load_module():
    spec = importlib.util.spec_from_file_location("fetch_security_tool", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


fetcher = load_module()


class FakeDownloadResponse:
    def __init__(self, final_url: str, body: bytes) -> None:
        self.status = 200
        self.headers = {"Content-Length": str(len(body))}
        self._final_url = final_url
        self._body = body
        self._offset = 0

    def geturl(self) -> str:
        return self._final_url

    def read(self, size: int) -> bytes:
        chunk = self._body[self._offset : self._offset + size]
        self._offset += len(chunk)
        return chunk

    def close(self) -> None:
        return None


class FakeOpener:
    def __init__(self, response: FakeDownloadResponse) -> None:
        self.response = response

    def open(self, request, timeout: int):  # type: ignore[no-untyped-def]
        return self.response


class FetchSecurityToolTest(unittest.TestCase):
    def test_checked_in_records_enforce_exact_release_provenance(self) -> None:
        for tool in ("actionlint", "zizmor", "gitleaks"):
            record = fetcher.record(tool)
            self.assertRegex(record["version"], fetcher.VERSION)
            self.assertRegex(record["release_commit"], fetcher.SHA1)
            self.assertRegex(record["sha256"], fetcher.SHA256)
            self.assertEqual(
                record["url"],
                f"{record['upstream']}/releases/download/{record['version']}/{record['asset']}",
            )

    def test_record_rejects_an_asset_url_outside_its_fixed_release(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            lock = Path(temporary) / "security-tools.lock.yml"
            lock.write_text(
                """schema_version: 1
checked_at: \"2026-07-21\"
pinned_actions:
  actions/checkout:
    version: v7.0.1
    commit_sha: 3d3c42e5aac5ba805825da76410c181273ba90b1
    upstream: https://github.com/actions/checkout
tools:
  actionlint:
    version: v1.7.12
    release_commit: 914e7df21a07ef503a81201c76d2b11c789d3fca
    asset: actionlint_1.7.12_linux_amd64.tar.gz
    url: https://example.invalid/actionlint.tar.gz
    sha256: 8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8
    executable: actionlint
    upstream: https://github.com/rhysd/actionlint
dispositions:
  sample: test
""",
                encoding="utf-8",
            )
            with mock.patch.object(fetcher, "LOCK", lock):
                with self.assertRaisesRegex(ValueError, "exact recorded upstream"):
                    fetcher.record("actionlint")

    def test_record_rejects_a_non_immutable_release_commit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            lock = Path(temporary) / "security-tools.lock.yml"
            lock.write_text(
                (ROOT / "ci" / "tooling" / "security-tools.lock.yml")
                .read_text(encoding="utf-8")
                .replace("release_commit: 914e7df21a07ef503a81201c76d2b11c789d3fca", "release_commit: main"),
                encoding="utf-8",
            )
            with mock.patch.object(fetcher, "LOCK", lock):
                with self.assertRaisesRegex(ValueError, "malformed release commit SHA"):
                    fetcher.record("actionlint")

    def test_safe_member_rejects_links_and_path_traversal(self) -> None:
        regular = tarfile.TarInfo("bin/actionlint")
        regular.type = tarfile.REGTYPE
        regular.size = 1
        traversal = tarfile.TarInfo("../actionlint")
        traversal.type = tarfile.REGTYPE
        traversal.size = 1
        link = tarfile.TarInfo("actionlint")
        link.type = tarfile.SYMTYPE
        self.assertTrue(fetcher.safe_member(regular))
        self.assertFalse(fetcher.safe_member(traversal))
        self.assertFalse(fetcher.safe_member(link))

    def test_trusted_release_redirect_handler_allows_only_bounded_https_asset_hosts(self) -> None:
        initial = "https://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_linux_amd64.tar.gz"
        allowed = "https://release-assets.githubusercontent.com/github-production-release-asset/test?sig=example"
        legacy = "https://github-releases.githubusercontent.com/github-production-release-asset/test?sig=example"
        handler = fetcher.TrustedReleaseRedirectHandler(initial)
        request = urllib.request.Request(initial)
        first = handler.redirect_request(request, None, 302, "Found", Message(), allowed)
        self.assertIsNotNone(first)
        second = handler.redirect_request(first, None, 302, "Found", Message(), legacy)
        self.assertIsNotNone(second)
        with self.assertRaisesRegex(ValueError, "redirect limit"):
            handler.redirect_request(second, None, 302, "Found", Message(), allowed)

    def test_trusted_release_redirect_handler_rejects_foreign_or_insecure_hosts(self) -> None:
        initial = "https://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_linux_amd64.tar.gz"
        for target in (
            "https://example.invalid/actionlint.tar.gz",
            "https://github.com/rhysd/actionlint/releases/download/v1.7.12/other.tar.gz",
            "http://release-assets.githubusercontent.com/actionlint.tar.gz",
            "https://release-assets.githubusercontent.com.evil.invalid/actionlint.tar.gz",
        ):
            with self.subTest(target=target):
                handler = fetcher.TrustedReleaseRedirectHandler(initial)
                with self.assertRaisesRegex(ValueError, "allowed GitHub release-asset host|direct HTTPS URL"):
                    handler.redirect_request(urllib.request.Request(initial), None, 302, "Found", Message(), target)

    def test_trusted_release_redirect_handler_requires_the_exact_https_github_origin(self) -> None:
        for initial in (
            "http://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_linux_amd64.tar.gz",
            "https://example.invalid/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_linux_amd64.tar.gz",
            "https://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_linux_amd64.tar.gz?redirect=1",
        ):
            with self.subTest(initial=initial):
                with self.assertRaisesRegex(ValueError, "direct HTTPS URL|exact GitHub release origin"):
                    fetcher.TrustedReleaseRedirectHandler(initial)

    def test_download_accepts_an_allowed_final_asset_url_and_rejects_foreign_final_url(self) -> None:
        initial = "https://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_linux_amd64.tar.gz"
        allowed = "https://release-assets.githubusercontent.com/github-production-release-asset/test?sig=example"
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "asset.tar.gz"
            with mock.patch.object(
                fetcher.urllib.request,
                "build_opener",
                return_value=FakeOpener(FakeDownloadResponse(allowed, b"asset")),
            ):
                fetcher._download(initial, archive)
            self.assertEqual(b"asset", archive.read_bytes())

            foreign_archive = Path(temporary) / "foreign.tar.gz"
            with mock.patch.object(
                fetcher.urllib.request,
                "build_opener",
                return_value=FakeOpener(FakeDownloadResponse("https://example.invalid/asset", b"asset")),
            ):
                with self.assertRaisesRegex(ValueError, "allowed GitHub release-asset host"):
                    fetcher._download(initial, foreign_archive)

    def test_security_tool_docs_describe_the_redirect_boundary(self) -> None:
        english = (ROOT / "docs" / "security" / "ci-security-tooling.md").read_text(encoding="utf-8")
        german = (ROOT / "docs" / "security" / "ci-security-tooling.de.md").read_text(encoding="utf-8")
        for text in (english, german):
            self.assertIn("release-assets.githubusercontent.com", text)
            self.assertIn("github-releases.githubusercontent.com", text)
            self.assertIn("SHA-256", text)
            self.assertIn("python-ci-requirements.lock", text)
            self.assertIn("PyPI", text)


if __name__ == "__main__":
    unittest.main()
