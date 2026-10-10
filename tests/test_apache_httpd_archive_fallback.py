"""Pinned HTTPD download/archive fallback without changing source identity."""

from __future__ import annotations

import hashlib
import io
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest import mock
import urllib.error

from tests.test_prepare_runtime_components import components


SOURCE = "https://downloads.apache.org/httpd/httpd-2.4.68.tar.bz2"
ARCHIVE = "https://archive.apache.org/dist/httpd/httpd-2.4.68.tar.bz2"


class ApacheHttpdArchiveFallbackTest(unittest.TestCase):
    def setUp(self) -> None:
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w:bz2") as archive:
            entry = tarfile.TarInfo("httpd-2.4.68/README")
            contents = b"synthetic pinned source\n"
            entry.size = len(contents)
            archive.addfile(entry, io.BytesIO(contents))
        self.payload = buffer.getvalue()
        self.digest = hashlib.sha256(self.payload).hexdigest()

    def _failure(self, status: int) -> urllib.error.HTTPError:
        error = urllib.error.HTTPError(SOURCE, status, "synthetic", {}, None)
        self.addCleanup(error.close)
        return error

    def _prepare(self, outcomes, *, url=SOURCE, digest=None, name="httpd", repeat=False, managed=False):
        with tempfile.TemporaryDirectory(prefix="apache-httpd-archive-") as temporary:
            root = Path(temporary)
            cache_root = root / "cache-v2" if managed else None
            destination = cache_root / "archives" if cache_root else root
            if name != "httpd":
                with mock.patch.object(components, "urlopen_bytes", side_effect=outcomes) as network:
                    record = components.prepare_archive(
                        name, url, self.digest if digest is None else digest, "", destination, cache_root,
                        required_literal_sha256=True, verify_digest_before_archive_list=True,
                    )
                return record, [call.args[0] for call in network.call_args_list]

            selected = iter(outcomes)
            requested = []

            def transport(request):
                requested.append(request.full_url)
                outcome = next(selected)
                if isinstance(outcome, BaseException):
                    raise outcome
                response = components.urllib.response.addinfourl(
                    io.BytesIO(outcome), {}, request.full_url, 200,
                )
                response.msg = "synthetic"
                return response

            with mock.patch.object(
                components.urllib.request.HTTPSHandler,
                "https_open",
                side_effect=transport,
            ):
                record = components.prepare_archive(
                    name, url, self.digest if digest is None else digest, "", destination, cache_root,
                    required_literal_sha256=True, verify_digest_before_archive_list=True,
                    allow_httpd_source_recovery=True,
                )
                if repeat:
                    record = components.prepare_archive(
                        name, url, self.digest if digest is None else digest, "", destination, cache_root,
                        required_literal_sha256=True, verify_digest_before_archive_list=True,
                        allow_httpd_source_recovery=True,
                    )
                return record, requested

    def test_primary_404_uses_same_archive_with_verified_digest(self) -> None:
        record, urls = self._prepare([self._failure(404), self.payload])
        self.assertEqual(record["status"], "present", record)
        self.assertEqual(record["checksum_status"], "PASS")
        self.assertEqual(record["expected_sha256"], self.digest)
        self.assertEqual(record["url"], SOURCE)
        self.assertEqual(record["download_url"], ARCHIVE)
        self.assertEqual(urls, [SOURCE, ARCHIVE])

    def test_successful_primary_does_not_contact_archive(self) -> None:
        record, urls = self._prepare([self.payload])
        self.assertEqual(record["status"], "present", record)
        self.assertEqual(record["download_url"], SOURCE)
        self.assertEqual(urls, [SOURCE])

    def test_wrong_archive_digest_fails_before_tar_inspection(self) -> None:
        with mock.patch.object(components, "archive_can_list") as inspect:
            record, urls = self._prepare([self._failure(404), b"wrong source bytes"])
        self.assertEqual(record["status"], "corrupt", record)
        self.assertEqual(record["blocker_reason"], "sha256_mismatch")
        self.assertEqual(urls, [SOURCE, ARCHIVE])
        inspect.assert_not_called()

    def test_other_http_errors_and_timeout_do_not_fall_back(self) -> None:
        for failure in (self._failure(403), self._failure(500), RuntimeError(TimeoutError())):
            with self.subTest(failure=failure):
                record, urls = self._prepare([failure])
                self.assertEqual(record["status"], "blocked", record)
                self.assertEqual(urls, [SOURCE])

    def test_only_exact_official_httpd_url_is_eligible(self) -> None:
        for url in (
            SOURCE.replace("downloads.apache.org", "example.invalid"),
            SOURCE + "?override=1",
            SOURCE + "#fragment",
            SOURCE.replace(".tar.bz2", ".tar.gz"),
            SOURCE.replace("2.4.68", "２.４.６８"),
            SOURCE.replace("2.4.68", "٢.٤.٦٨"),
        ):
            with self.subTest(url=url):
                record, urls = self._prepare([self._failure(404)], url=url)
                self.assertEqual(record["status"], "blocked", record)
                self.assertEqual(urls, [])

    def test_non_httpd_component_does_not_use_httpd_fallback(self) -> None:
        record, urls = self._prepare([self._failure(404)], name="apr")
        self.assertEqual(record["status"], "blocked", record)
        self.assertEqual(urls, [SOURCE])

    def test_missing_or_malformed_digest_cannot_start_download(self) -> None:
        for digest in ("", "not-a-sha256"):
            with self.subTest(digest=digest):
                record, urls = self._prepare([], digest=digest)
                self.assertEqual(record["status"], "blocked", record)
                self.assertEqual(urls, [])

    def test_verified_cache_hit_neither_downloads_nor_invents_fetch_provenance(self) -> None:
        record, urls = self._prepare([self._failure(404), self.payload], repeat=True)
        self.assertEqual(record["status"], "present", record)
        self.assertEqual(record["url"], SOURCE)
        self.assertEqual(record["download_url"], "")
        self.assertEqual(record["download_status"], "cached")
        self.assertEqual(urls, [SOURCE, ARCHIVE])

    def test_managed_cache_keeps_canonical_source_identity_across_fallback_and_reuse(self) -> None:
        with mock.patch.object(
            components, "archive_cache_identity", wraps=components.archive_cache_identity,
        ) as identity:
            record, urls = self._prepare([self._failure(404), self.payload], repeat=True, managed=True)
        self.assertEqual(record["status"], "present", record)
        self.assertEqual(record["download_status"], "cached")
        self.assertEqual(urls, [SOURCE, ARCHIVE])
        self.assertEqual(identity.call_count, 2)
        for call in identity.call_args_list:
            self.assertEqual(call.args, ("httpd", SOURCE, self.digest, ""))

    def test_apache_archive_caller_requires_literal_digest_before_inspection(self) -> None:
        environment = {"HTTPD_SOURCE_URL": SOURCE, "HTTPD_SHA256": self.digest}
        with (
            mock.patch.object(components, "apr_util_archive_cache_identity", return_value={}),
            mock.patch.object(components, "prepare_archive") as prepare,
        ):
            components.apache_archive_records(environment, Path("/synthetic/archives"), Path("/synthetic/cache"))
        httpd_call = prepare.call_args_list[0]
        self.assertEqual(httpd_call.args[:3], ("httpd", SOURCE, self.digest))
        self.assertTrue(httpd_call.kwargs["required_literal_sha256"])
        self.assertTrue(httpd_call.kwargs["verify_digest_before_archive_list"])
        self.assertTrue(httpd_call.kwargs["allow_httpd_source_recovery"])


if __name__ == "__main__":
    unittest.main()
