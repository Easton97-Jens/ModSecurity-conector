from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "ci" / "tools" / "print-framework-apr-util-env.sh"
FRAMEWORK_ROOT = ROOT / "modules" / "ModSecurity-test-Framework"
sys.path.insert(0, str(ROOT / "ci" / "provisioning" / "components"))
SPEC = importlib.util.spec_from_file_location(
    "framework_apr_util_provenance_components",
    ROOT / "ci" / "provisioning" / "components" / "prepare-runtime-components.py",
)
assert SPEC is not None
assert SPEC.loader is not None
components = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = components
SPEC.loader.exec_module(components)


class FrameworkAprUtilProvenanceTest(unittest.TestCase):
    @staticmethod
    def fixture_tuple(version: str, digest: str) -> dict[str, str]:
        source_url = f"https://downloads.apache.org/apr/apr-util-{version}.tar.bz2"
        return {
            "APR_UTIL_VERSION": version,
            "APR_UTIL_SOURCE_URL": source_url,
            "APR_UTIL_SHA256": digest,
            "APR_UTIL_SHA256_URL": f"{source_url}.sha256",
        }

    def bridge(self, environment: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["/bin/sh", str(BRIDGE), str(FRAMEWORK_ROOT), str(ROOT)],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_absent_parent_tuple_uses_dynamic_framework_guarded_values(self) -> None:
        environment = os.environ.copy()
        for key in components.FRAMEWORK_APR_UTIL_ENV_KEYS:
            environment.pop(key, None)
        result = self.bridge(environment)
        self.assertEqual(result.returncode, 0, result.stderr)
        values = {}
        for line in result.stdout.splitlines():
            match = components.SHELL_QUOTED_ENV_RE.fullmatch(line)
            self.assertIsNotNone(match)
            assert match is not None
            values[match.group(1)] = match.group(2)
        self.assertEqual(set(values), set(components.FRAMEWORK_APR_UTIL_ENV_KEYS))
        self.assertEqual(values, components.require_apr_util_pinned_provenance(values))
        self.assertEqual(
            values["APR_UTIL_SOURCE_URL"],
            f"https://downloads.apache.org/apr/apr-util-{values['APR_UTIL_VERSION']}.tar.bz2",
        )
        self.assertEqual(values["APR_UTIL_SHA256_URL"], f"{values['APR_UTIL_SOURCE_URL']}.sha256")
        loaded, status = components.load_framework_environment(ROOT, FRAMEWORK_ROOT, environment)
        self.assertEqual(status, "loaded")
        self.assertEqual(
            {key: loaded[key] for key in components.FRAMEWORK_APR_UTIL_ENV_KEYS},
            values,
        )

    def test_single_and_coherent_parent_overrides_are_rejected(self) -> None:
        base = os.environ.copy()
        for key in components.FRAMEWORK_APR_UTIL_ENV_KEYS:
            base.pop(key, None)
        alternate = self.fixture_tuple("9.9.9", "a" * 64)
        for key, value in alternate.items():
            with self.subTest(override=key):
                environment = dict(base)
                environment[key] = value
                result = self.bridge(environment)
                self.assertEqual(result.returncode, 77)
                self.assertIn(key, result.stderr)

        coherent = dict(base)
        coherent.update(alternate)
        result = self.bridge(coherent)
        self.assertEqual(result.returncode, 77)
        self.assertIn("APR_UTIL_VERSION", result.stderr)

    def test_python_loader_rejects_parent_overrides_without_running_the_bridge(self) -> None:
        env = {"APR_UTIL_VERSION": "9.9.9"}
        with tempfile.TemporaryDirectory(prefix="framework-apr-util-override-") as temporary:
            framework_root = Path(temporary) / "framework"
            common_sh = framework_root / "ci" / "lib" / "common.sh"
            common_sh.parent.mkdir(parents=True)
            common_sh.write_text("#!/bin/sh\n", encoding="utf-8")
            with mock.patch.object(components, "_run_framework_guard") as run_guard:
                loaded, status = components.load_framework_environment(ROOT, framework_root, env)
        self.assertEqual(loaded, env)
        self.assertEqual(status, "failed:inherited_parent_apr_util_override:APR_UTIL_VERSION")
        run_guard.assert_not_called()

    def test_framework_guard_runtime_error_keeps_the_fail_closed_status(self) -> None:
        with mock.patch.object(components.subprocess, "run", side_effect=RuntimeError("guard failure")):
            output, status = components._run_framework_guard(["/bin/sh"], ROOT, {})
        self.assertIsNone(output)
        self.assertEqual(status, "failed:guard failure")

    def test_python_loader_uses_fixed_guard_environment_and_parses_both_outputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="framework-apr-util-loader-") as temporary:
            framework_root = Path(temporary) / "framework"
            common_sh = framework_root / "ci" / "lib" / "common.sh"
            common_sh.parent.mkdir(parents=True)
            tuple_values = self.fixture_tuple("7.8.9", "a" * 64)
            common_sh.write_text(
                "\n".join(
                    [
                        "#!/bin/sh",
                        *(f'{key}="{value}"' for key, value in tuple_values.items()),
                        "COMMON_CONTROL=passed",
                        "ci_require_apr_util_pinned_provenance() { :; }",
                        "ci_validate_https_runtime_url_config() { :; }",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            for key in (*components.FRAMEWORK_APR_UTIL_ENV_KEYS, "ENV", "BASH_ENV", "SHELLOPTS"):
                environment.pop(key, None)
            environment.update({"ENV": "untrusted-hook", "BASH_ENV": "untrusted-hook", "SHELLOPTS": "nounset"})
            loaded, status = components.load_framework_environment(ROOT, framework_root, environment)

        self.assertEqual(status, "loaded")
        self.assertEqual({key: loaded[key] for key in tuple_values}, tuple_values)
        self.assertEqual(loaded["COMMON_CONTROL"], "passed")
        self.assertNotIn("ENV", loaded)
        self.assertNotIn("BASH_ENV", loaded)
        self.assertNotIn("SHELLOPTS", loaded)

    def test_framework_child_sourcing_preserves_the_canonical_tuple(self) -> None:
        environment = os.environ.copy()
        for key in components.FRAMEWORK_APR_UTIL_ENV_KEYS:
            environment.pop(key, None)
        script = (
            '. "$1/ci/lib/common.sh"; ci_require_apr_util_pinned_provenance; '
            'first="$APR_UTIL_VERSION:$APR_UTIL_SOURCE_URL:$APR_UTIL_SHA256:$APR_UTIL_SHA256_URL"; '
            '. "$1/ci/lib/common.sh"; ci_require_apr_util_pinned_provenance; '
            'second="$APR_UTIL_VERSION:$APR_UTIL_SOURCE_URL:$APR_UTIL_SHA256:$APR_UTIL_SHA256_URL"; '
            'test "$first" = "$second"'
        )
        result = subprocess.run(
            ["/bin/sh", "-eu", "-c", script, "framework-child-source", str(FRAMEWORK_ROOT)],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_malformed_apr_util_tuples_fail_closed(self) -> None:
        valid = self.fixture_tuple("7.8.9", "a" * 64)
        self.assertEqual(components.require_apr_util_pinned_provenance(valid), valid)
        for label, key, value in (
            (
                "foreign host",
                "APR_UTIL_SOURCE_URL",
                f"https://mirror.invalid/apr-util-{valid['APR_UTIL_VERSION']}.tar.bz2",
            ),
            ("wrong archive path", "APR_UTIL_SOURCE_URL", "https://downloads.apache.org/apr/apr-util-7.8.9.tar.gz"),
            ("foreign checksum path", "APR_UTIL_SHA256_URL", "https://downloads.apache.org/apr/foreign.sha256"),
            ("malformed SHA", "APR_UTIL_SHA256", "not-a-sha256"),
        ):
            with self.subTest(malformed=label):
                candidate = dict(valid)
                candidate[key] = value
                with self.assertRaises(RuntimeError):
                    components.require_apr_util_pinned_provenance(candidate)

    def test_apr_util_version_rejects_unicode_digits(self) -> None:
        unicode_version = "١.٢.٣"
        candidate = self.fixture_tuple(unicode_version, "a" * 64)
        self.assertIsNone(components.APR_UTIL_VERSION_RE.fullmatch(unicode_version))
        with self.assertRaises(RuntimeError):
            components.require_apr_util_pinned_provenance(candidate)

    def test_apr_util_cache_identity_changes_for_version_and_sha(self) -> None:
        first = self.fixture_tuple("7.8.9", "a" * 64)
        second = self.fixture_tuple("7.8.10", "a" * 64)
        changed_sha = {**first, "APR_UTIL_SHA256": "b" * 64}
        first_identity = components.apr_util_archive_cache_identity(first)
        self.assertNotEqual(first_identity["cache_key"], components.apr_util_archive_cache_identity(second)["cache_key"])
        self.assertNotEqual(first_identity["cache_key"], components.apr_util_archive_cache_identity(changed_sha)["cache_key"])
        self.assertEqual(first_identity["archive_name"], f"apr-util-{first['APR_UTIL_VERSION']}.tar.bz2")


if __name__ == "__main__":
    unittest.main()
