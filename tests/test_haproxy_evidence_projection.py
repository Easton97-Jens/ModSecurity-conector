"""Security contracts for the bounded HAProxy runtime evidence projection."""

from __future__ import annotations

import contextlib
import grp
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import socket
import stat
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PROJECTOR_PATH = ROOT / "ci" / "runtime" / "lifecycle" / "project-haproxy-runtime-evidence.py"
SPEC = importlib.util.spec_from_file_location("haproxy_evidence_projection", PROJECTOR_PATH)
assert SPEC is not None
assert SPEC.loader is not None
projector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(projector)
SETPRIV = shutil.which("setpriv")
SYSTEM_PYTHON = "/usr/bin/python3"


def _cross_identity_staging_supported() -> bool:
    """Skip only when this local namespace cannot model runner/nobody ownership."""
    if os.geteuid() != 0 or not SETPRIV or not Path(SYSTEM_PYTHON).is_file():
        return False
    switched = subprocess.run(
        [
            str(SETPRIV),
            "--reuid=65534",
            "--regid=65534",
            "--clear-groups",
            "--no-new-privs",
            "--",
            "/usr/bin/true",
        ],
        check=False,
        capture_output=True,
    )
    if switched.returncode != 0:
        return False
    try:
        with tempfile.TemporaryDirectory(prefix="haproxy-evidence-identity-") as directory:
            candidate = Path(directory) / "candidate"
            candidate.mkdir()
            os.chown(candidate, 65534, 65534)
    except OSError:
        return False
    return True


class HaproxyEvidenceRootGuardTests(unittest.TestCase):
    def test_every_runtime_evidence_entrypoint_refuses_root(self) -> None:
        if os.geteuid() != 0:
            self.skipTest("root-entrypoint guard is exercised by the host runner identity")
        trusted = projector.TrustedRuntimeValues(
            parent_sha="a" * 40,
            framework_sha="b" * 40,
            mrts_sha="c" * 40,
        )
        calls = (
            lambda: projector.write_source_receipt(
                source_root=Path("/nonexistent"), trusted=trusted, observed_status=403
            ),
            lambda: projector.export_source_receipt(
                source_root=Path("/nonexistent"), trusted=trusted, runtime_uid=1001
            ),
            lambda: projector.project_document(
                source_document="{}\n",
                runner_temp=Path("/nonexistent"),
                stage_parent=Path("/nonexistent/parent"),
                stage_root=Path("/nonexistent/parent/package"),
                trusted=trusted,
                runtime_uid=1001,
            ),
            lambda: projector.verify_staged_package(
                runner_temp=Path("/nonexistent"),
                stage_parent=Path("/nonexistent/parent"),
                stage_root=Path("/nonexistent/parent/package"),
                trusted=trusted,
                runtime_uid=1001,
            ),
        )
        for call in calls:
            with self.subTest(call=call), self.assertRaisesRegex(
                projector.EvidenceProjectionError, "PRIVILEGED_PROJECTOR_FORBIDDEN"
            ):
                call()


class HaproxyEvidenceDocumentValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.trusted = projector.TrustedRuntimeValues(
            parent_sha="a" * 40,
            framework_sha="b" * 40,
            mrts_sha="c" * 40,
        )

    def test_valid_source_receipt_has_one_canonical_allowlist_encoding(self) -> None:
        source = projector._source_receipt(self.trusted, 403)
        reordered = dict(reversed(list(source.items())))
        canonical = projector.canonical_json_bytes(source)
        self.assertEqual(canonical, projector.canonical_json_bytes(reordered))
        self.assertEqual(
            projector._parse_canonical_object(
                canonical, maximum_bytes=projector.MAX_SOURCE_RECEIPT_BYTES
            ),
            source,
        )
        projector._validate_source_receipt(source, self.trusted)

    def test_source_receipt_rejects_untrusted_semantics_and_payload_keys(self) -> None:
        invalid_values = (
            ("unknown", "forbidden"),
            ("request_body", "forbidden"),
            ("response_headers", "forbidden"),
            ("cookie", "forbidden"),
            ("token", "forbidden"),
            ("credential", "forbidden"),
            ("opaque_handle", "forbidden"),
            ("socket_path", "/tmp/opaque.sock"),
            ("parent_sha", "d" * 40),
            ("connector", "envoy"),
            ("case_id", "phase2_args_block"),
            ("crs_mode", "no-crs"),
            ("mrts_mode", "with-mrts"),
            ("evidence_scope", "full_p1_p4_capability"),
            ("cleanup_result", "incomplete"),
            ("runtime_result", "failure"),
            ("connector_profile", "/tmp/receipt"),
            ("connector_profile", "../receipt"),
            ("connector_profile", "embedded/path"),
            ("expected_status", 403.0),
            ("host_status", 403.0),
            ("rule_id", 942270.0),
            ("schema_version", True),
        )
        for field, value in invalid_values:
            with self.subTest(field=field, value=value):
                candidate = projector._source_receipt(self.trusted, 403)
                candidate[field] = value
                with self.assertRaises(projector.EvidenceProjectionError):
                    projector._validate_source_receipt(candidate, self.trusted)

        nested = projector._source_receipt(self.trusted, 403)
        nested["phase_counts"] = {"P1": 0, "P2": True, "P3": 0, "P4": 0}
        with self.assertRaises(projector.EvidenceProjectionError):
            projector._validate_source_receipt(nested, self.trusted)

    def test_json_parser_rejects_duplicate_noncanonical_and_unsafe_values(self) -> None:
        malformed = (
            b'{"x":1,"x":1}\n',
            b'{"x":NaN}\n',
            b'{"x":"broken"}\x00\n',
            b'{"x":"\\xff"}\n',
            b'{"x":1}\n\n',
        )
        for raw in malformed:
            with self.subTest(raw=raw):
                with self.assertRaises(projector.EvidenceProjectionError):
                    projector._parse_canonical_object(
                        raw, maximum_bytes=projector.MAX_SOURCE_RECEIPT_BYTES
                    )

    def test_standard_input_reader_is_size_bounded_and_rejects_invalid_utf8(self) -> None:
        cases = (
            (
                b"x" * (projector.MAX_SOURCE_RECEIPT_BYTES + 1),
                "SOURCE_RECEIPT_TOO_LARGE",
            ),
            (b"\xff", "UNSAFE_SOURCE_DOCUMENT"),
        )
        for raw, expected_error in cases:
            with self.subTest(expected_error=expected_error):
                standard_input = io.TextIOWrapper(io.BytesIO(raw), encoding="utf-8")
                with mock.patch.object(projector.sys, "stdin", standard_input):
                    with self.assertRaisesRegex(
                        projector.EvidenceProjectionError, expected_error
                    ):
                        projector._read_source_document_from_standard_input()

    def test_standard_input_reader_accepts_exact_limit_without_shell_buffering(self) -> None:
        raw = b"x" * projector.MAX_SOURCE_RECEIPT_BYTES
        standard_input = io.TextIOWrapper(io.BytesIO(raw), encoding="utf-8")
        with mock.patch.object(projector.sys, "stdin", standard_input):
            self.assertEqual(projector._read_source_document_from_standard_input(), raw.decode())

    def test_project_command_requires_explicit_standard_input_mode(self) -> None:
        arguments = (
            "project-document",
            "--runner-temp",
            "/tmp/runner-temp",
            "--stage-parent",
            "/tmp/runner-temp/haproxy-runtime-evidence-parent.A1b2C3d4",
            "--stage-root",
            "/tmp/runner-temp/haproxy-runtime-evidence-parent.A1b2C3d4/package",
            "--runtime-uid",
            "1001",
            "--expected-parent-sha",
            "a" * 40,
            "--expected-framework-sha",
            "b" * 40,
            "--expected-mrts-sha",
            "c" * 40,
        )
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(projector.main(arguments), 2)
        self.assertIn("UNSAFE_SOURCE_DOCUMENT", stderr.getvalue())

    def test_partial_cleanup_reopens_a_sealed_directory_only_to_remove_allowlisted_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-evidence-cleanup-") as directory:
            stage = Path(directory) / "package"
            stage.mkdir(mode=0o700)
            partial = stage / projector.EVIDENCE_FILENAME
            partial.write_text("{}\n", encoding="utf-8")
            partial.chmod(0o444)
            stage.chmod(0o555)
            descriptor = os.open(stage, os.O_RDONLY | os.O_DIRECTORY)
            try:
                projector._discard_staged_files(
                    descriptor,
                    stage_uid=os.geteuid(),
                    stage_gid=os.getegid(),
                )
            finally:
                os.close(descriptor)
            self.assertEqual(list(stage.iterdir()), [])
            self.assertEqual(stat.S_IMODE(stage.stat().st_mode), 0o700)

            unexpected = stage / "foreign"
            unexpected.write_text("x", encoding="utf-8")
            unexpected.chmod(0o444)
            descriptor = os.open(stage, os.O_RDONLY | os.O_DIRECTORY)
            try:
                with self.assertRaises(projector.EvidenceProjectionError):
                    projector._discard_staged_files(
                        descriptor,
                        stage_uid=os.geteuid(),
                        stage_gid=os.getegid(),
                    )
            finally:
                os.close(descriptor)
            self.assertTrue(unexpected.exists())


@unittest.skipUnless(
    _cross_identity_staging_supported(),
    "cross-identity staging fixture requires root, mapped identities, and setpriv",
)
class HaproxyEvidenceProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="haproxy-evidence-projection-")
        self.root = Path(self.temporary.name)
        self.root.chmod(0o755)
        self.runtime_uid = 1001
        self.runtime_gid = 1001
        self.evidence_uid = 65534
        self.evidence_gid = grp.getgrnam("nogroup").gr_gid
        self.assertNotEqual(self.runtime_uid, self.evidence_uid)
        self.runner_temp = self.root / "runner-temp"
        self.source_root = self.root / "runtime-source"
        self.stage_parent = self.runner_temp / "haproxy-runtime-evidence-parent.A1b2C3d4"
        self.stage_root = self.stage_parent / projector.STAGE_DIRECTORY_NAME
        self.runner_temp.mkdir(mode=0o755)
        self.trusted = projector.TrustedRuntimeValues(
            parent_sha="a" * 40,
            framework_sha="b" * 40,
            mrts_sha="c" * 40,
        )
        self._fresh_source()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @property
    def receipt_path(self) -> Path:
        return self.source_root / projector.SOURCE_RECEIPT_FILENAME

    def _fresh_source(self) -> None:
        if self.source_root.exists() or self.source_root.is_symlink():
            if self.source_root.is_dir() and not self.source_root.is_symlink():
                shutil.rmtree(self.source_root)
            else:
                self.source_root.unlink()
        self.source_root.mkdir(mode=0o700)
        os.chown(self.source_root, self.runtime_uid, self.runtime_gid)
        self.source_root.chmod(0o700)
        result = self._run_as(
            self.runtime_uid,
            self.runtime_gid,
            [
                "write-source-receipt",
                "--source-root",
                os.fspath(self.source_root),
                "--observed-status",
                "403",
                *self._trusted_arguments(),
            ],
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))

    def _fresh_stage(self) -> None:
        if self.stage_parent.exists():
            shutil.rmtree(self.stage_parent)
        self.stage_parent.mkdir(mode=0o755)
        os.chown(self.stage_parent, 0, 0)
        self.stage_parent.chmod(0o755)
        self.stage_root.mkdir(mode=0o700)
        os.chown(self.stage_root, self.evidence_uid, self.evidence_gid)
        self.stage_root.chmod(0o700)

    def _run_as(
        self,
        uid: int,
        gid: int,
        arguments: list[str],
        standard_input: bytes | None = None,
    ) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            [
                str(SETPRIV),
                f"--reuid={uid}",
                f"--regid={gid}",
                "--clear-groups",
                "--no-new-privs",
                "--",
                "/usr/bin/env",
                "-i",
                "PATH=/usr/bin:/bin",
                "HOME=/nonexistent",
                "PYTHONDONTWRITEBYTECODE=1",
                SYSTEM_PYTHON,
                "-I",
                str(PROJECTOR_PATH),
                *arguments,
            ],
            check=False,
            capture_output=True,
            input=standard_input,
        )

    def _trusted_arguments(self) -> list[str]:
        return [
            "--expected-parent-sha",
            self.trusted.parent_sha,
            "--expected-framework-sha",
            self.trusted.framework_sha,
            "--expected-mrts-sha",
            self.trusted.mrts_sha,
        ]

    def _export(self, source_root: Path | None = None) -> subprocess.CompletedProcess[bytes]:
        return self._run_as(
            self.runtime_uid,
            self.runtime_gid,
            [
                "export-source-receipt",
                "--source-root",
                os.fspath(source_root or self.source_root),
                "--runtime-uid",
                str(self.runtime_uid),
                *self._trusted_arguments(),
            ],
        )

    def _project(self, source_document: bytes) -> subprocess.CompletedProcess[bytes]:
        self._fresh_stage()
        return self._run_as(
            self.evidence_uid,
            self.evidence_gid,
            [
                "project-document",
                "--source-document-stdin",
                "--runner-temp",
                os.fspath(self.runner_temp),
                "--stage-parent",
                os.fspath(self.stage_parent),
                "--stage-root",
                os.fspath(self.stage_root),
                "--runtime-uid",
                str(self.runtime_uid),
                *self._trusted_arguments(),
            ],
            standard_input=source_document,
        )

    def _verify(self) -> subprocess.CompletedProcess[bytes]:
        return self._run_as(
            self.evidence_uid,
            self.evidence_gid,
            [
                "verify",
                "--runner-temp",
                os.fspath(self.runner_temp),
                "--stage-parent",
                os.fspath(self.stage_parent),
                "--stage-root",
                os.fspath(self.stage_root),
                "--runtime-uid",
                str(self.runtime_uid),
                *self._trusted_arguments(),
            ],
        )

    def _valid_document(self) -> bytes:
        result = self._export()
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))
        return result.stdout

    def _project_valid_document(self) -> bytes:
        document = self._valid_document()
        result = self._project(document)
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))
        return document

    def _receipt(self) -> dict[str, object]:
        return json.loads(self.receipt_path.read_text(encoding="utf-8"))

    def _replace_receipt(self, value: dict[str, object]) -> None:
        self.receipt_path.write_bytes(projector.canonical_json_bytes(value))
        os.chown(self.receipt_path, self.runtime_uid, self.runtime_gid)
        self.receipt_path.chmod(0o600)

    def _assert_export_rejected(self, source_root: Path | None = None) -> None:
        result = self._export(source_root)
        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stderr.startswith(b"FAIL: "))

    def test_valid_receipt_is_canonically_reserialized_and_verified(self) -> None:
        document = self._project_valid_document()
        self.assertEqual(document, projector.canonical_json_bytes(projector._source_receipt(self.trusted, 403)))
        self.assertEqual(
            sorted(path.name for path in self.stage_root.iterdir()),
            [projector.EVIDENCE_FILENAME, projector.MANIFEST_FILENAME],
        )
        stage_details = self.stage_root.stat()
        self.assertEqual((stage_details.st_uid, stage_details.st_gid), (self.evidence_uid, self.evidence_gid))
        self.assertEqual(stat.S_IMODE(stage_details.st_mode), 0o555)
        self.assertNotEqual(stage_details.st_uid, self.runtime_uid)
        self.assertEqual(self._verify().returncode, 0)

        evidence = self.stage_root / projector.EVIDENCE_FILENAME
        manifest = self.stage_root / projector.MANIFEST_FILENAME
        for candidate in (evidence, manifest):
            details = candidate.stat()
            self.assertTrue(stat.S_ISREG(details.st_mode))
            self.assertFalse(candidate.is_symlink())
            self.assertEqual((details.st_uid, details.st_gid), (self.evidence_uid, self.evidence_gid))
            self.assertEqual(stat.S_IMODE(details.st_mode), 0o444)
            self.assertLessEqual(details.st_size, projector.MAX_FILE_BYTES)
            raw = candidate.read_bytes()
            self.assertNotIn(b"\x00", raw)
            self.assertTrue(raw.endswith(b"\n"))
            self.assertEqual(raw, projector.canonical_json_bytes(json.loads(raw)))

        serialized = evidence.read_text(encoding="utf-8").lower()
        for forbidden in ("body", "header", "cookie", "token", "password", "handle", "/tmp"):
            self.assertNotIn(forbidden, serialized)
        self.assertEqual(projector.MAX_FILE_BYTES * 2, 128 * 1024)
        self.assertGreaterEqual(projector.MAX_TOTAL_BYTES, projector.MAX_FILE_BYTES * 2)

    def test_runtime_identity_cannot_mutate_the_sealed_package(self) -> None:
        self._project_valid_document()
        mutation = self.stage_root / "runtime-mutation"
        result = subprocess.run(
            [
                str(SETPRIV),
                f"--reuid={self.runtime_uid}",
                f"--regid={self.runtime_gid}",
                "--clear-groups",
                "--no-new-privs",
                "--",
                "/usr/bin/touch",
                os.fspath(mutation),
            ],
            check=False,
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(mutation.exists())
        self.assertEqual(self._verify().returncode, 0)

    def test_projector_contains_no_privileged_helper_path(self) -> None:
        source = PROJECTOR_PATH.read_text(encoding="utf-8")
        self.assertNotIn("seal-helper", source)
        self.assertNotIn("seal_projector_helper", source)
        self.assertNotIn("PRIVILEGED_PROJECTOR_REQUIRED", source)

    def test_source_path_types_and_unknown_contents_are_rejected(self) -> None:
        safe = self.root / "safe.json"
        safe.write_text("{}\n", encoding="utf-8")
        self.receipt_path.unlink()
        self.receipt_path.symlink_to(safe)
        self._assert_export_rejected()
        self._fresh_source()

        linked_root = self.root / "linked-source"
        linked_root.symlink_to(self.source_root, target_is_directory=True)
        self._assert_export_rejected(linked_root)

        (self.source_root / "unexpected.json").write_text("{}\n", encoding="utf-8")
        os.chown(self.source_root / "unexpected.json", self.runtime_uid, self.runtime_gid)
        (self.source_root / "unexpected.json").chmod(0o600)
        self._assert_export_rejected()

    def test_fifo_socket_device_and_oversized_source_are_rejected(self) -> None:
        self.receipt_path.unlink()
        os.mkfifo(self.receipt_path, 0o600)
        os.chown(self.receipt_path, self.runtime_uid, self.runtime_gid)
        self._assert_export_rejected()
        self._fresh_source()

        with tempfile.TemporaryDirectory(prefix="hep-", dir=tempfile.gettempdir()) as directory:
            socket_root = Path(directory)
            socket_root.chmod(0o755)
            source_root = socket_root / "source"
            source_root.mkdir(mode=0o700)
            os.chown(source_root, self.runtime_uid, self.runtime_gid)
            result = self._run_as(
                self.runtime_uid,
                self.runtime_gid,
                [
                    "write-source-receipt",
                    "--source-root",
                    os.fspath(source_root),
                    "--observed-status",
                    "403",
                    *self._trusted_arguments(),
                ],
            )
            self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))
            socket_receipt = source_root / projector.SOURCE_RECEIPT_FILENAME
            socket_receipt.unlink()
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
                server.bind(os.fspath(socket_receipt))
                self._assert_export_rejected(source_root)

        self._fresh_source()
        self.receipt_path.write_bytes(b"x" * (projector.MAX_SOURCE_RECEIPT_BYTES + 1))
        os.chown(self.receipt_path, self.runtime_uid, self.runtime_gid)
        self.receipt_path.chmod(0o600)
        self._assert_export_rejected()

        self._fresh_source()
        self.receipt_path.unlink()
        try:
            os.mknod(self.receipt_path, stat.S_IFCHR | 0o600, os.makedev(1, 3))
        except PermissionError:
            self.skipTest("the current root namespace cannot create device fixtures")
        try:
            os.chown(self.receipt_path, self.runtime_uid, self.runtime_gid)
            self._assert_export_rejected()
        finally:
            self.receipt_path.unlink(missing_ok=True)

    def test_json_schema_numeric_and_prohibited_values_are_rejected(self) -> None:
        for field, value in (
            ("unknown", "forbidden"),
            ("request_body", "forbidden"),
            ("response_headers", "forbidden"),
            ("cookie", "forbidden"),
            ("token", "forbidden"),
            ("credential", "forbidden"),
            ("opaque_handle", "forbidden"),
            ("socket_path", "forbidden"),
            ("parent_sha", "d" * 40),
            ("connector", "envoy"),
            ("case_id", "phase2_args_block"),
            ("crs_mode", "no-crs"),
            ("mrts_mode", "with-mrts"),
            ("evidence_scope", "full_p1_p4_capability"),
            ("cleanup_result", "incomplete"),
            ("runtime_result", "failure"),
            ("connector_profile", "/tmp/receipt"),
            ("connector_profile", "../receipt"),
            ("connector_profile", "embedded/path"),
            ("expected_status", 403.0),
            ("host_status", 403.0),
            ("rule_id", 942270.0),
            ("schema_version", True),
        ):
            with self.subTest(field=field, value=value):
                candidate = self._receipt()
                candidate[field] = value
                self._replace_receipt(candidate)
                self._assert_export_rejected()
                self._fresh_source()

        candidate = self._receipt()
        candidate["phase_counts"]["P2"] = True
        self._replace_receipt(candidate)
        self._assert_export_rejected()

    def test_malformed_canonical_and_duplicate_json_are_rejected(self) -> None:
        malformed = (
            b'{"x":1,"x":1}\n',
            b'{"x":NaN}\n',
            b'{"x":"broken"}\x00\n',
            b'{"x":"\xff"}\n',
            b'{"x":' + b"1" * 15000 + b"}\n",
            b'{"x":' + b"[" * 4000 + b"0" + b"]" * 4000 + b"}\n",
        )
        for raw in malformed:
            with self.subTest(size=len(raw)):
                self.receipt_path.write_bytes(raw)
                os.chown(self.receipt_path, self.runtime_uid, self.runtime_gid)
                self.receipt_path.chmod(0o600)
                self._assert_export_rejected()
                self._fresh_source()

    def test_stage_path_identity_extra_file_and_digest_mutation_are_rejected(self) -> None:
        self._project_valid_document()
        self.stage_root.chmod(0o755)
        extra = self.stage_root / "unexpected.json"
        extra.write_text("{}\n", encoding="utf-8")
        os.chown(extra, self.evidence_uid, self.evidence_gid)
        extra.chmod(0o444)
        self.stage_root.chmod(0o555)
        self.assertEqual(self._verify().returncode, 2)

        self.stage_root.chmod(0o755)
        extra.unlink()
        manifest = self.stage_root / projector.MANIFEST_FILENAME
        manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
        manifest_data["files"][0]["sha256"] = "0" * 64
        manifest.write_bytes(projector.canonical_json_bytes(manifest_data))
        os.chown(manifest, self.evidence_uid, self.evidence_gid)
        manifest.chmod(0o444)
        self.stage_root.chmod(0o555)
        self.assertEqual(self._verify().returncode, 2)

        linked_runner = self.root / "linked-runner"
        linked_runner.symlink_to(self.runner_temp, target_is_directory=True)
        result = self._run_as(
            self.evidence_uid,
            self.evidence_gid,
            [
                "verify",
                "--runner-temp",
                os.fspath(linked_runner),
                "--stage-parent",
                os.fspath(linked_runner / self.stage_parent.name),
                "--stage-root",
                os.fspath(linked_runner / self.stage_parent.name / projector.STAGE_DIRECTORY_NAME),
                "--runtime-uid",
                str(self.runtime_uid),
                *self._trusted_arguments(),
            ],
        )
        self.assertEqual(result.returncode, 2)

    def test_partial_stage_cleanup_is_allowlist_only_and_nonrecursive(self) -> None:
        self._fresh_stage()
        partial = self.stage_root / projector.EVIDENCE_FILENAME
        partial.write_text("{}\n", encoding="utf-8")
        os.chown(partial, self.evidence_uid, self.evidence_gid)
        partial.chmod(0o444)
        self.stage_root.chmod(0o555)
        descriptor = os.open(self.stage_root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            projector._discard_staged_files(
                descriptor,
                stage_uid=self.evidence_uid,
                stage_gid=self.evidence_gid,
            )
        finally:
            os.close(descriptor)
        self.assertEqual(list(self.stage_root.iterdir()), [])

        forbidden = self.stage_root / "foreign"
        forbidden.write_text("x", encoding="utf-8")
        os.chown(forbidden, self.evidence_uid, self.evidence_gid)
        forbidden.chmod(0o444)
        descriptor = os.open(self.stage_root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            with self.assertRaises(projector.EvidenceProjectionError):
                projector._discard_staged_files(
                    descriptor,
                    stage_uid=self.evidence_uid,
                    stage_gid=self.evidence_gid,
                )
        finally:
            os.close(descriptor)
        self.assertTrue(forbidden.exists())


if __name__ == "__main__":
    unittest.main()
