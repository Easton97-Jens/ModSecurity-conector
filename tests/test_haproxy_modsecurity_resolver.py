"""Focused precedence and rejection tests for the native HAProxy resolver."""

from __future__ import annotations

import os
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
RESOLVER = ROOT / "connectors" / "haproxy" / "htx-overlay" / "resolve-modsecurity.sh"
CONTRACT = ROOT / "connectors" / "haproxy" / "htx-overlay" / "version-contract.json"
CONTRACT_MODULE_PATH = ROOT / "connectors" / "haproxy" / "htx-overlay" / "version_contract.py"
CONTRACT_SPEC = importlib.util.spec_from_file_location("haproxy_version_contract", CONTRACT_MODULE_PATH)
if CONTRACT_SPEC is None or CONTRACT_SPEC.loader is None:
    raise RuntimeError("cannot load HAProxy version-contract module")
CONTRACT_MODULE = importlib.util.module_from_spec(CONTRACT_SPEC)
CONTRACT_SPEC.loader.exec_module(CONTRACT_MODULE)


class HAProxyModSecurityResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cc = shutil.which("cc")
        self.assertIsNotNone(self.cc, "cc is required for resolver tests")

    def make_installation(self, root: Path) -> tuple[Path, Path]:
        include_dir = root / "include"
        header_dir = include_dir / "modsecurity"
        lib_dir = root / "lib"
        header_dir.mkdir(parents=True)
        lib_dir.mkdir()
        for name in ("modsecurity.h", "rules_set.h", "transaction.h"):
            (header_dir / name).write_text("#pragma once\n", encoding="utf-8")
        source = root / "modsecurity.c"
        source.write_text("int modsecurity_resolver_probe(void) { return 0; }\n", encoding="utf-8")
        subprocess.run(
            [str(self.cc), "-shared", "-fPIC", str(source), "-o", str(lib_dir / "libmodsecurity.so")],
            check=True,
            capture_output=True,
            text=True,
        )
        return include_dir, lib_dir

    def run_resolver(self, output: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["sh", str(RESOLVER), str(output)],
            cwd=ROOT,
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_explicit_paths_take_precedence(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-resolver-explicit-") as temporary:
            root = Path(temporary)
            include_dir, lib_dir = self.make_installation(root / "explicit")
            output = root / "resolution.env"
            env = os.environ.copy()
            env["MODSECURITY_INCLUDE_DIR"] = str(include_dir)
            env["MODSECURITY_LIB_DIR"] = str(lib_dir)
            result = self.run_resolver(output, env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            values = {
                key: value.strip("'")
                for key, value in (line.split("=", 1) for line in output.read_text().splitlines())
            }
            self.assertEqual(values["MODSECURITY_INCLUDE_DIR"], str(include_dir))
            self.assertEqual(values["MODSECURITY_LIB_DIR"], str(lib_dir))
            self.assertEqual(values["MODSECURITY_RESOLUTION"], "explicit")

    def test_pkg_config_is_used_when_paths_are_not_explicit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-resolver-pkgconfig-") as temporary:
            root = Path(temporary)
            include_dir, lib_dir = self.make_installation(root / "installation")
            pkg_dir = root / "pkgconfig"
            pkg_dir.mkdir()
            (pkg_dir / "libmodsecurity.pc").write_text(
                f"prefix={root / 'installation'}\nincludedir={include_dir}\nlibdir={lib_dir}\nName: libmodsecurity\nDescription: test libModSecurity\nVersion: 3.0.14\nLibs: -L{lib_dir} -lmodsecurity\nCflags: -I{include_dir}\n",
                encoding="utf-8",
            )
            output = root / "resolution.env"
            env = os.environ.copy()
            env.pop("MODSECURITY_INCLUDE_DIR", None)
            env.pop("MODSECURITY_LIB_DIR", None)
            env["PKG_CONFIG_LIBDIR"] = str(pkg_dir)
            result = self.run_resolver(output, env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            values = {
                key: value.strip("'")
                for key, value in (line.split("=", 1) for line in output.read_text().splitlines())
            }
            self.assertEqual(values["MODSECURITY_RESOLUTION"], "pkg-config")

    def test_header_library_pairing_mismatch_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-resolver-mismatch-") as temporary:
            root = Path(temporary)
            include_dir = root / "include"
            (include_dir / "modsecurity").mkdir(parents=True)
            (include_dir / "modsecurity/modsecurity.h").write_text("#pragma once\n", encoding="utf-8")
            (include_dir / "modsecurity/rules_set.h").write_text("#pragma once\n", encoding="utf-8")
            (include_dir / "modsecurity/transaction.h").write_text("#pragma once\n", encoding="utf-8")
            lib_dir = root / "lib"
            lib_dir.mkdir()
            (lib_dir / "libmodsecurity.so").write_text("not an ELF library\n", encoding="utf-8")
            env = os.environ.copy()
            env["MODSECURITY_INCLUDE_DIR"] = str(include_dir)
            env["MODSECURITY_LIB_DIR"] = str(lib_dir)
            result = self.run_resolver(root / "resolution.env", env)
            self.assertEqual(result.returncode, 77)
            self.assertIn("architecture", result.stderr)

    def test_shared_library_symlink_is_resolved_for_validation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-resolver-symlink-") as temporary:
            root = Path(temporary)
            include_dir, lib_dir = self.make_installation(root / "installation")
            target = lib_dir / "libmodsecurity.so.3.0.14"
            (lib_dir / "libmodsecurity.so").rename(target)
            (lib_dir / "libmodsecurity.so").symlink_to(target.name)
            output = root / "resolution.env"
            env = os.environ.copy()
            env["MODSECURITY_INCLUDE_DIR"] = str(include_dir)
            env["MODSECURITY_LIB_DIR"] = str(lib_dir)
            result = self.run_resolver(output, env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            values = {
                key: value.strip("'")
                for key, value in (line.split("=", 1) for line in output.read_text().splitlines())
            }
            self.assertEqual(values["MODSECURITY_LIBRARY"], str(lib_dir / "libmodsecurity.so"))

    def test_malicious_versioned_library_name_is_blocked_without_execution(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-resolver-library-name-") as temporary:
            root = Path(temporary)
            include_dir, lib_dir = self.make_installation(root / "installation")
            valid_library = lib_dir / "libmodsecurity.so"
            malicious_name = "libmodsecurity.so.3'$(touch-marker)'"
            malicious_library = lib_dir / malicious_name
            valid_library.rename(malicious_library)
            marker = root / "touch-marker"
            output = root / "resolution.env"
            env = os.environ.copy()
            env["MODSECURITY_INCLUDE_DIR"] = str(include_dir)
            env["MODSECURITY_LIB_DIR"] = str(lib_dir)
            result = self.run_resolver(output, env)
            self.assertEqual(result.returncode, 77)
            self.assertIn("libmodsecurity is missing", result.stderr)
            self.assertFalse(marker.exists())
            self.assertFalse(output.exists())

    def test_path_metacharacters_are_blocked_before_env_file_write(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-resolver-injection-") as temporary:
            root = Path(temporary)
            marker = root / "marker"
            output = root / "resolution.env"
            env = os.environ.copy()
            env["MODSECURITY_INCLUDE_DIR"] = f"{root}/include;touch {marker}"
            env["MODSECURITY_LIB_DIR"] = f"{root}/lib"
            result = self.run_resolver(output, env)
            self.assertEqual(result.returncode, 77)
            self.assertFalse(marker.exists())
            self.assertFalse(output.exists())

    def test_output_path_metacharacters_are_blocked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-resolver-output-") as temporary:
            root = Path(temporary)
            marker = root / "marker"
            output = f"{root}/resolution.env;touch {marker}"
            env = os.environ.copy()
            result = subprocess.run(
                ["sh", str(RESOLVER), output],
                cwd=ROOT,
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 77)
            self.assertFalse(marker.exists())

    def test_contract_mentions_distro_paths_and_htx_provenance(self) -> None:
        makefile = (ROOT / "connectors/haproxy/Makefile").read_text(encoding="utf-8")
        overlay = (ROOT / "connectors/haproxy/htx-overlay/build-overlay.sh").read_text(encoding="utf-8")
        resolver = RESOLVER.read_text(encoding="utf-8")
        self.assertIn("resolve-modsecurity.sh", makefile)
        self.assertIn("/usr/include", resolver)
        self.assertIn("/usr/lib/x86_64-linux-gnu", resolver)
        self.assertIn("version-contract.json", overlay)
        self.assertIn("HAPROXY_VERSION=$(contract_field version)", overlay)

    def test_version_contract_accepts_the_repository_contract(self) -> None:
        contract = CONTRACT_MODULE.load_contract(CONTRACT)
        version_parts = contract["version"].split(".")
        self.assertEqual(version_parts[:2], ["3", "2"])
        self.assertTrue(version_parts[2].isdigit())
        self.assertTrue(contract["makefile_patch"].endswith(".patch"))

    def test_version_contract_rejects_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-contract-symlink-") as temporary:
            root = Path(temporary)
            outside = root / "outside.json"
            outside.write_text(CONTRACT.read_text(encoding="utf-8"), encoding="utf-8")
            allowed = root / "allowed"
            allowed.mkdir()
            escaped = allowed / "version-contract.json"
            escaped.symlink_to(outside)
            with mock.patch.object(CONTRACT_MODULE, "CONTRACT_ROOT", allowed.resolve()):
                with self.assertRaisesRegex(ValueError, "symlink"):
                    CONTRACT_MODULE.load_contract(escaped)

    def test_version_contract_rejects_unsafe_patch_and_digest_values(self) -> None:
        with tempfile.TemporaryDirectory(prefix="haproxy-contract-values-") as temporary:
            root = Path(temporary)
            payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
            valid_patch = payload["makefile_patch"]
            payload["makefile_patch"] = "../escape.patch"
            candidate = root / "invalid-patch.json"
            candidate.write_text(json.dumps(payload), encoding="utf-8")
            with mock.patch.object(CONTRACT_MODULE, "CONTRACT_ROOT", root.resolve()):
                with self.assertRaisesRegex(ValueError, "makefile_patch"):
                    CONTRACT_MODULE.load_contract(candidate)
            payload["makefile_patch"] = valid_patch
            payload["sha256"] = "A" * 64
            candidate.write_text(json.dumps(payload), encoding="utf-8")
            with mock.patch.object(CONTRACT_MODULE, "CONTRACT_ROOT", root.resolve()):
                with self.assertRaisesRegex(ValueError, "SHA-256"):
                    CONTRACT_MODULE.load_contract(candidate)


if __name__ == "__main__":
    unittest.main()
