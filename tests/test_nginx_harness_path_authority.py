"""Regression coverage for root NGINX harness output-path authority."""

from __future__ import annotations

import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "ci" / "runtime" / "common" / "validate-nginx-harness-paths.py"
PROJECTOR = ROOT / "ci" / "runtime" / "common" / "prepare-nginx-docroot-projection.py"
HARNESS = ROOT / "connectors" / "nginx" / "harness" / "run_nginx_smoke.sh"


class NginxHarnessPathAuthorityTests(unittest.TestCase):
    maxDiff = None

    def run_validator(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), *arguments],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )

    def run_projector(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(PROJECTOR), *arguments],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )

    @staticmethod
    def directory_identity_and_mode(path: Path) -> tuple[int, int, int]:
        metadata = path.lstat()
        return metadata.st_uid, metadata.st_gid, stat.S_IMODE(metadata.st_mode)

    @staticmethod
    def worker_traversable_temporary_directory() -> tempfile.TemporaryDirectory[str]:
        candidates = (Path(tempfile.gettempdir()), Path("/tmp"), Path("/dev/shm"))
        attempted: set[Path] = set()
        failures: list[str] = []

        for candidate in candidates:
            if candidate in attempted:
                continue
            attempted.add(candidate)
            current = Path("/")
            for component in candidate.parts[1:]:
                current /= component
                try:
                    metadata = current.lstat()
                except OSError as exc:
                    failures.append(f"{candidate}: {exc}")
                    break
                if not stat.S_ISDIR(metadata.st_mode) or not metadata.st_mode & stat.S_IXOTH:
                    failures.append(f"{candidate}: non-traversable ancestor")
                    break
            else:
                try:
                    return tempfile.TemporaryDirectory(
                        prefix="nginx-path-authority-", dir=candidate
                    )
                except OSError as exc:
                    failures.append(f"{candidate}: {exc}")

        raise RuntimeError(
            "no worker-traversable temporary directory available: " + "; ".join(failures)
        )

    def run_parent_harness_with_output_override(
        self,
        verified_root: Path,
        variable: str,
        outside_path: Path,
    ) -> subprocess.CompletedProcess[str]:
        build_root = verified_root / "build"
        environment = os.environ.copy()
        for inherited in (
            "NGINX_HARNESS_WORK_ROOT",
            "RUNTIME_ROOT",
            "PERMISSIONS_LOG",
            "NGINX_WORKER_PREFLIGHT_FILE",
        ):
            environment.pop(inherited, None)
        environment.update(
            {
                "PYTHON": sys.executable,
                "PYTHONDONTWRITEBYTECODE": "1",
                "VERIFIED_RUN_ROOT": str(verified_root),
                "VERIFIED_BUILD_ROOT": str(build_root),
                "BUILD_ROOT": str(build_root),
                "NGINX_HARNESS_PARENT": str(build_root / "nginx-harness"),
                "RUNTIME_BASE": str(build_root / "runtime"),
                "RESULTS_DIR": str(build_root / "results"),
                "RUN_ONE_CASE": "0",
                "MSCONNECTOR_SMOKE_STAGE": "config_load",
                variable: str(outside_path),
            }
        )
        return subprocess.run(
            ["sh", str(HARNESS)],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
            env=environment,
        )

    def test_system_root_is_rejected_before_any_output_is_authorized(self) -> None:
        result = self.run_validator(
            "--verified-run-root",
            "/etc",
            "--directory",
            "LOG_DIR",
            "/etc/codex-nginx-harness-regression",
            "--quiet",
        )

        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("runtime root is unsafe for writes: /etc", result.stderr)

    def test_sibling_and_symlink_escape_are_rejected_without_creating_targets(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-path-authority-") as temporary:
            base = Path(temporary)
            verified_root = base / "ModSecurity-conector-verified"
            sibling = base / "outside"
            escaped = verified_root / "escape"
            verified_root.mkdir()
            escaped.symlink_to(sibling, target_is_directory=True)

            sibling_result = self.run_validator(
                "--verified-run-root",
                str(verified_root),
                "--directory",
                "LOG_DIR",
                str(sibling / "logs"),
                "--quiet",
            )
            self.assertEqual(sibling_result.returncode, 2, sibling_result.stderr)
            self.assertFalse(sibling.exists())

            escape_result = self.run_validator(
                "--verified-run-root",
                str(verified_root),
                "--directory",
                "LOG_DIR",
                str(escaped / "logs"),
                "--quiet",
            )
            self.assertEqual(escape_result.returncode, 2, escape_result.stderr)
            self.assertFalse(sibling.exists())

    def test_verified_runtime_descendants_and_direct_log_child_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-path-authority-") as temporary:
            verified_root = Path(temporary) / "ModSecurity-conector-verified"
            build_root = verified_root / "build"
            log_dir = build_root / "logs"
            config_file = build_root / "runtime" / "nginx.conf"
            permissions_log = log_dir / "permissions.log"

            result = self.run_validator(
                "--verified-run-root",
                str(verified_root),
                "--directory",
                "BUILD_ROOT",
                str(build_root),
                "--directory",
                "LOG_DIR",
                str(log_dir),
                "--path",
                "CONFIG_FILE",
                str(config_file),
                "--direct-child",
                "PERMISSIONS_LOG",
                str(permissions_log),
                str(log_dir),
                "--quiet",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(verified_root.is_dir())
            self.assertTrue(build_root.is_dir())
            self.assertTrue(log_dir.is_dir())
            self.assertTrue(config_file.parent.is_dir())
            self.assertFalse(config_file.exists())
            self.assertFalse(permissions_log.exists())

    def test_explicit_external_projection_parent_is_narrowly_authorized(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-path-authority-") as temporary:
            base = Path(temporary)
            verified_root = base / "verified"
            projection_parent = base / "worker-visible-projection"
            projection_root = projection_parent / "nginx-docroot"
            projection_parent.mkdir(mode=0o711)
            projection_parent.chmod(0o711)

            result = self.run_validator(
                "--verified-run-root",
                str(verified_root),
                "--existing-private-directory",
                "NGINX_DOCROOT_PROJECTION_PARENT",
                str(projection_parent),
                "--existing-direct-child",
                "NGINX_DOCROOT_PROJECTION_ROOT",
                str(projection_root),
                str(projection_parent),
                "--quiet",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(projection_parent.is_dir())
            self.assertFalse(projection_root.exists())

    def test_validator_and_projector_keep_external_projection_narrow(self) -> None:
        """Exercise the real CLI boundary without starting a privileged NGINX runtime."""

        with self.worker_traversable_temporary_directory() as temporary:
            base = Path(temporary)
            # The helper checks every ancestor for worker traversal.  Keep the
            # test-owned outer directory non-enumerable but traversable.
            base.chmod(0o711)
            verified_root = base / "verified"
            generic_output_directory = verified_root / "generic-output"
            generic_output = generic_output_directory / "status.txt"
            private_root = verified_root / "build"
            source_docroot = private_root / "runtime" / "htdocs"
            projection_parent = base / "worker-visible-projection"
            projection_root = projection_parent / "explicit-docroot"
            projection_parent.mkdir(mode=0o711)
            projection_parent.chmod(0o711)
            parent_before = self.directory_identity_and_mode(projection_parent)

            validation = self.run_validator(
                "--verified-run-root",
                str(verified_root),
                "--directory",
                "GENERIC_OUTPUT_DIRECTORY",
                str(generic_output_directory),
                "--path",
                "GENERIC_OUTPUT",
                str(generic_output),
                "--existing-private-directory",
                "NGINX_DOCROOT_PROJECTION_PARENT",
                str(projection_parent),
                "--existing-direct-child",
                "NGINX_DOCROOT_PROJECTION_ROOT",
                str(projection_root),
                str(projection_parent),
                "--quiet",
            )

            self.assertEqual(validation.returncode, 0, validation.stderr)
            self.assertTrue(generic_output_directory.is_dir())
            self.assertEqual(
                generic_output.relative_to(verified_root),
                Path("generic-output") / "status.txt",
            )
            self.assertFalse(generic_output.exists())
            self.assertFalse(projection_root.exists())
            self.assertEqual(self.directory_identity_and_mode(projection_parent), parent_before)

            generic_output.write_text("verified generic output\n", encoding="utf-8")
            source_docroot.mkdir(parents=True, mode=0o700)
            (source_docroot / "index.html").write_text("projected index\n", encoding="utf-8")
            (source_docroot / "__modsec_smoke_ready").write_text("ready\n", encoding="utf-8")
            (source_docroot / "not-projected.txt").write_text("private\n", encoding="utf-8")

            projection = self.run_projector(
                "--source-docroot",
                str(source_docroot),
                "--private-root",
                str(private_root),
                "--projection-parent",
                str(projection_parent),
                "--projection-root",
                str(projection_root),
                "--avoid-root",
                str(verified_root),
            )

            self.assertEqual(projection.returncode, 0, projection.stderr)
            self.assertEqual(projection.stdout.strip(), str(projection_root))
            self.assertEqual(projection_root.parent, projection_parent)
            self.assertEqual(
                {entry.name for entry in projection_parent.iterdir()},
                {projection_root.name},
            )
            self.assertEqual(
                {entry.name for entry in projection_root.iterdir()},
                {"index.html", "__modsec_smoke_ready"},
            )
            self.assertEqual(
                (projection_root / "index.html").read_text(encoding="utf-8"),
                "projected index\n",
            )
            self.assertEqual(
                (projection_root / "__modsec_smoke_ready").read_text(encoding="utf-8"),
                "ready\n",
            )
            self.assertFalse((projection_root / "not-projected.txt").exists())
            self.assertEqual(stat.S_IMODE(projection_root.lstat().st_mode), 0o711)
            self.assertTrue(generic_output.is_file())
            self.assertEqual(
                generic_output.relative_to(verified_root),
                Path("generic-output") / "status.txt",
            )
            self.assertFalse((projection_parent / generic_output.name).exists())
            self.assertEqual(self.directory_identity_and_mode(projection_parent), parent_before)

    def test_stale_external_projection_child_is_rejected_before_projection(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-path-authority-") as temporary:
            base = Path(temporary)
            base.chmod(0o711)
            verified_root = base / "verified"
            projection_parent = base / "worker-visible-projection"
            projection_root = projection_parent / "explicit-docroot"
            projection_parent.mkdir(mode=0o711)
            projection_parent.chmod(0o711)
            projection_root.mkdir(mode=0o700)
            marker = projection_root / "existing-marker"
            marker.write_text("keep\n", encoding="utf-8")
            parent_before = self.directory_identity_and_mode(projection_parent)

            result = self.run_validator(
                "--verified-run-root",
                str(verified_root),
                "--existing-private-directory",
                "NGINX_DOCROOT_PROJECTION_PARENT",
                str(projection_parent),
                "--existing-direct-child",
                "NGINX_DOCROOT_PROJECTION_ROOT",
                str(projection_root),
                str(projection_parent),
                "--quiet",
            )

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("must be a fresh non-symlink child", result.stderr)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep\n")
            self.assertEqual(
                {entry.name for entry in projection_parent.iterdir()},
                {projection_root.name},
            )
            self.assertEqual(self.directory_identity_and_mode(projection_parent), parent_before)

    def test_system_projection_parent_is_rejected_without_creating_a_child(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-path-authority-") as temporary:
            result = self.run_validator(
                "--verified-run-root",
                str(Path(temporary) / "verified"),
                "--existing-private-directory",
                "NGINX_DOCROOT_PROJECTION_PARENT",
                "/etc",
                "--existing-direct-child",
                "NGINX_DOCROOT_PROJECTION_ROOT",
                "/etc/codex-nginx-harness-regression",
                "/etc",
                "--quiet",
            )

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("unsafe for runtime writes: /etc", result.stderr)

    def test_parent_multi_case_outputs_are_rejected_before_their_first_write(self) -> None:
        with tempfile.TemporaryDirectory(prefix="nginx-path-authority-") as temporary:
            base = Path(temporary)
            for variable, suffix in (
                ("LOG_DIR", "logs"),
                ("RESULTS_DIR", "results"),
            ):
                with self.subTest(variable=variable):
                    verified_root = base / f"verified-{suffix}"
                    outside_path = base / f"outside-{suffix}" / suffix
                    result = self.run_parent_harness_with_output_override(
                        verified_root,
                        variable,
                        outside_path,
                    )

                    self.assertEqual(result.returncode, 77, result.stderr)
                    self.assertIn("outside verified runtime storage", result.stdout)
                    self.assertFalse(outside_path.parent.exists())

    def test_harness_validates_authority_before_root_mutation_sinks(self) -> None:
        harness = HARNESS.read_text(encoding="utf-8")

        for fragment in (
            "validate-nginx-harness-paths.py",
            "validate_nginx_harness_bootstrap_paths",
            "validate_nginx_harness_outer_paths",
            "validate_nginx_generated_path_authority",
            "validate_nginx_external_projection_authority",
            "--verified-run-root \"$VERIFIED_RUN_ROOT\"",
            "--directory RESULTS_DIR \"$RESULTS_DIR\"",
            "--direct-child PERMISSIONS_LOG \"$PERMISSIONS_LOG\" \"$LOG_DIR\"",
            "--direct-child NGINX_WORKER_PREFLIGHT_FILE \"$NGINX_WORKER_PREFLIGHT_FILE\" \"$LOG_DIR\"",
            "--existing-private-directory NGINX_DOCROOT_PROJECTION_PARENT \"$NGINX_DOCROOT_PROJECTION_PARENT\"",
            "--existing-direct-child NGINX_DOCROOT_PROJECTION_ROOT \"$NGINX_DOCROOT_PROJECTION_ROOT\" \"$NGINX_DOCROOT_PROJECTION_PARENT\"",
            "validate_nginx_request_output_path SEND_CASE_RESPONSE_BODY \"$response_output\"",
            "validate_nginx_request_output_path SEND_CASE_CURL_ERROR_LOG \"$curl_error_output\"",
            "NGINX_PATHS_VALIDATED=1",
            "write_harness_status",
        ):
            self.assertIn(fragment, harness)

        authority_call = harness.rindex("validate_nginx_generated_path_authority")
        projection_authority_call = harness.rindex("validate_nginx_external_projection_authority")
        first_root_mutation = harness.index('ensure_dir_755 "$NGINX_HARNESS_WORK_ROOT"')
        self.assertLess(authority_call, first_root_mutation)
        self.assertLess(projection_authority_call, first_root_mutation)
        outer_authority_call = harness.rindex("validate_nginx_harness_outer_paths")
        all_case_root_mutation = harness.index('mkdir -p "$LOG_DIR" "$RESULTS_DIR"')
        self.assertLess(outer_authority_call, all_case_root_mutation)
        blocked_definition = harness[
            harness.index("blocked() {") : harness.index("fail() {")
        ]
        self.assertNotIn("mkdir", blocked_definition)


if __name__ == "__main__":
    unittest.main()
