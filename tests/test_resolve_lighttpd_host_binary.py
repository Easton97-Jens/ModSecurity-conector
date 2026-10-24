from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "resolve_lighttpd_host_binary",
    ROOT / "ci/runtime/lifecycle/resolve-lighttpd-host-binary.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load Lighttpd host-binary resolver")
resolver = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(resolver)


class ResolveLighttpdHostBinaryTest(unittest.TestCase):
    def test_legacy_minimal_runtime_explicitly_allows_private_lighttpd_provisioning(self) -> None:
        workflow = yaml.safe_load(
            (ROOT / ".github/workflows/open-connectors-smoke.yml").read_text(
                encoding="utf-8"
            )
        )
        job = workflow["jobs"]["open-connectors-smoke"]
        self.assertNotIn("ALLOW_RUNTIME_BUILDS", job["env"])
        steps = {step["name"]: step for step in job["steps"] if "name" in step}
        with tempfile.TemporaryDirectory() as name:
            directory = Path(name)
            capture = directory / "make-env.txt"
            fake_make = directory / "make"
            fake_make.write_text(
                "#!/bin/sh\n"
                'printf "%s|%s|%s\\n" "${ALLOW_RUNTIME_DOWNLOADS:-0}" '
                '"${ALLOW_RUNTIME_BUILDS:-0}" "$*" > "$MAKE_ENV_CAPTURE"\n',
                encoding="utf-8",
            )
            fake_make.chmod(0o700)
            environment = dict(os.environ)
            environment.pop("ALLOW_RUNTIME_BUILDS", None)
            environment.update(job["env"])
            environment["PATH"] = str(directory) + os.pathsep + os.defpath
            environment["MAKE_ENV_CAPTURE"] = str(capture)
            for step_name, expected in (
                ("Native connector build diagnostics", "1|0|build-remaining-connectors"),
                ("Native request-free host start diagnostics", "1|0|start-smoke-remaining-connectors"),
                ("Native minimal runtime diagnostics", "1|1|runtime-smoke-remaining-connectors"),
            ):
                with self.subTest(step=step_name):
                    subprocess.run(
                        ["/bin/sh", "-c", steps[step_name]["run"]],
                        env=environment,
                        check=True,
                        capture_output=True,
                        timeout=10,
                    )
                    self.assertEqual(capture.read_text().strip(), expected)

    def executable(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def test_accepts_regular_executable_below_current_build_root(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            build_root = Path(name) / "build"
            binary = self.executable(build_root / "lighttpd-connector/bin/lighttpd")
            self.assertEqual(
                resolver.resolve_lighttpd_host_binary(build_root), binary
            )

    def test_rejects_missing_staged_binary_or_relative_build_root(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            build_root = Path(name) / "build"
            build_root.mkdir()
            with self.assertRaises(ValueError):
                resolver.resolve_lighttpd_host_binary(build_root)
            with self.assertRaises(ValueError):
                resolver.resolve_lighttpd_host_binary(Path("relative-build-root"))

    def test_does_not_accept_an_arbitrary_in_tree_executable(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            build_root = Path(name) / "build"
            self.executable(build_root / "other-tool")
            with self.assertRaises(ValueError):
                resolver.resolve_lighttpd_host_binary(build_root)

    def test_rejects_symlink_directory_and_non_executable_staged_path(self) -> None:
        for kind in ("symlink", "directory", "non_executable"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as name:
                build_root = Path(name) / "build"
                expected = build_root / "lighttpd-connector/bin/lighttpd"
                expected.parent.mkdir(parents=True)
                if kind == "symlink":
                    expected.symlink_to(self.executable(build_root / "real-lighttpd"))
                elif kind == "directory":
                    expected.mkdir()
                else:
                    expected.write_text("data\n", encoding="utf-8")
                with self.assertRaises(ValueError):
                    resolver.resolve_lighttpd_host_binary(build_root)

    def test_runner_uses_only_the_fixed_staged_path_for_generic_lighttpd(self) -> None:
        runner = (ROOT / "ci/runtime/lifecycle/run-no-crs-baseline.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "\n".join(
                (
                    'host_binary=$("$PYTHON" "$LIGHTTPD_HOST_BINARY_RESOLVER" \\',
                    '                --build-root "$CONNECTOR_BUILD_ROOT")',
                )
            ),
            runner,
        )
        self.assertIn("inherited LIGHTTPD_BIN values", runner)
        self.assertNotIn("--candidate \"$LIGHTTPD_BIN\"", runner)
        self.assertNotIn(
            "host_binary=$CONNECTOR_COMPONENT_CACHE/lighttpd/bin/lighttpd", runner
        )
        self.assertIn(
            "host_binary=$HOST_RUNTIME_ROOT/lighttpd-patched/stage/bin/lighttpd", runner
        )


if __name__ == "__main__":
    unittest.main()
