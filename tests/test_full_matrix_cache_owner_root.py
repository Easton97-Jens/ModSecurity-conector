from __future__ import annotations

import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MATRIX_RUNNER = ROOT / "ci" / "runtime" / "lifecycle" / "run-full-matrix-parallel.sh"
FRAMEWORK_ROOT = ROOT / "modules" / "ModSecurity-test-Framework"


class FullMatrixCacheOwnerRootTest(unittest.TestCase):
    def write_fake_make(self, bin_dir: Path) -> None:
        fake_make = bin_dir / "make"
        fake_make.write_text(
            """#!/bin/sh
set -eu

case "$*" in
    *smoke-apache*)
        connector=apache
        connector_build_root=$APACHE_BUILD_ROOT
        owner_root=$APACHE_BUILD_OWNER_ROOT
        ;;
    *smoke-nginx*)
        connector=nginx
        connector_build_root=$NGINX_BUILD_DIR
        owner_root=$NGINX_BUILD_OWNER_ROOT
        ;;
    *)
        echo "unexpected fake make invocation: $*" >&2
        exit 97
        ;;
esac

printf '%s|%s|%s|%s|%s\\n' \\
    "$connector" "$REFRESH" "$BUILD_ROOT" "$connector_build_root" "$owner_root" \\
    >> "$CAPTURE_FILE"
""",
            encoding="utf-8",
        )
        fake_make.chmod(fake_make.stat().st_mode | stat.S_IXUSR)

    def matrix_environment(
        self,
        root: Path,
        bin_dir: Path,
        capture_file: Path,
        *,
        connectors: str,
        apache_build_root: Path,
        nginx_build_root: Path,
    ) -> tuple[dict[str, str], Path, Path]:
        verified_root = root / "verified"
        component_cache = verified_root / "cache-v2" / "shared"
        owner_root = component_cache / "builds" / "connectors"
        owner_root.mkdir(parents=True)
        apache_build_root.mkdir(parents=True)
        nginx_build_root.mkdir(parents=True)

        environment = os.environ.copy()
        environment.update(
            {
                "PATH": f"{bin_dir}{os.pathsep}{environment['PATH']}",
                "CAPTURE_FILE": str(capture_file),
                "CONNECTOR_ROOT": str(ROOT),
                "FRAMEWORK_ROOT": str(FRAMEWORK_ROOT),
                "VERIFIED_RUN_ROOT": str(verified_root),
                "VERIFIED_BUILD_ROOT": str(verified_root / "build"),
                "BUILD_ROOT": str(verified_root / "build"),
                "TMP_ROOT": str(verified_root / "tmp"),
                "LOG_ROOT": str(verified_root / "logs"),
                "CONNECTOR_COMPONENT_CACHE": str(component_cache),
                "VERIFIED_COMPONENT_CACHE": str(component_cache),
                "MATRIX_ROOT": str(verified_root / "matrix"),
                "MRTS_BUILD_ROOT": str(verified_root / "mrts"),
                "NGINX_HARNESS_PARENT": str(verified_root / "nginx-harness"),
                "FULL_MATRIX_VARIANTS": "no-crs/no-mrts",
                "FULL_MATRIX_CONNECTORS": connectors,
                "FULL_MATRIX_SKIP_REPORTS": "1",
                "FULL_MATRIX_REPORT_DIR": str(verified_root / "reports"),
                "FULL_MATRIX_MANIFEST": str(verified_root / "matrix" / "runs.jsonl"),
                "APACHE_BUILD_ROOT": str(apache_build_root),
                "NGINX_BUILD_DIR": str(nginx_build_root),
                "APACHE_HTTPD": "",
                "APACHE_MODULE": "",
                "APACHE_MRTS_MODSECURITY_LIB_DIR": "",
                "MRTS_NATIVE_NGINX_BIN": "",
                "MRTS_NATIVE_NGINX_MODULE_DIR": "",
                "MRTS_NATIVE_NGINX_MODSECURITY_LIB_DIR": "",
            }
        )
        return environment, owner_root, verified_root

    def test_cache_backed_refreshes_receive_one_narrow_explicit_owner_root(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="full-matrix-owner-root-") as temporary:
            root = Path(temporary)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            self.write_fake_make(bin_dir)
            capture_file = root / "make-capture.txt"
            owner_root = root / "verified" / "cache-v2" / "shared" / "builds" / "connectors"
            apache_build_root = owner_root / "apache" / "cache-key" / "build"
            nginx_build_root = owner_root / "nginx" / "cache-key" / "build"
            environment, expected_owner_root, verified_root = self.matrix_environment(
                root,
                bin_dir,
                capture_file,
                connectors="apache nginx",
                apache_build_root=apache_build_root,
                nginx_build_root=nginx_build_root,
            )

            process = subprocess.run(
                ["sh", str(MATRIX_RUNNER)],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            records = {
                fields[0]: fields
                for fields in (
                    line.split("|") for line in capture_file.read_text(encoding="utf-8").splitlines()
                )
            }
            self.assertEqual(set(records), {"apache", "nginx"})
            for connector, fields in records.items():
                with self.subTest(connector=connector):
                    _, refresh, job_build_root, connector_build_root, owner_root_text = fields
                    self.assertEqual(refresh, "1")
                    self.assertEqual(owner_root_text, str(expected_owner_root))
                    self.assertTrue(Path(connector_build_root).is_relative_to(expected_owner_root))
                    self.assertTrue(Path(job_build_root).is_relative_to(verified_root / "matrix"))
                    self.assertNotEqual(job_build_root, owner_root_text)

    def test_outside_connector_cache_build_is_rejected_before_make(self) -> None:
        with tempfile.TemporaryDirectory(prefix="full-matrix-owner-root-reject-") as temporary:
            root = Path(temporary)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            self.write_fake_make(bin_dir)
            capture_file = root / "make-capture.txt"
            outside_build_root = root / "verified" / "outside" / "apache-build"
            nginx_build_root = (
                root
                / "verified"
                / "cache-v2"
                / "shared"
                / "builds"
                / "connectors"
                / "nginx"
                / "cache-key"
                / "build"
            )
            environment, expected_owner_root, verified_root = self.matrix_environment(
                root,
                bin_dir,
                capture_file,
                connectors="apache",
                apache_build_root=outside_build_root,
                nginx_build_root=nginx_build_root,
            )

            process = subprocess.run(
                ["sh", str(MATRIX_RUNNER)],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
            self.assertFalse(capture_file.exists())
            run_log = verified_root / "matrix" / "no-crs" / "no-mrts" / "apache" / "run.log"
            self.assertIn(
                f"apache matrix build root must stay under {expected_owner_root}",
                run_log.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
