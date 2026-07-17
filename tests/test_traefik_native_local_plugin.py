from __future__ import annotations

import concurrent.futures
import importlib.util
import json
import os
import re
import socket
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "connectors" / "traefik" / "native_middleware"
RUNNER_PATH = ROOT / "connectors" / "traefik" / "scripts" / "runtime_native_smoke.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("traefik_native_runner", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the Traefik native runtime runner")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


runner = load_runner()


def engine_socket_parent(path: Path) -> object:
    return runner.EngineSocketParent(
        path=path,
        identity=runner.private_directory_identity(path, "test parent"),
        generated=False,
    )


def short_socket_temporary_directory() -> tempfile.TemporaryDirectory:
    """Allocate test state under a writable, short existing temp boundary."""

    default_root = Path(tempfile.gettempdir())
    for candidate in (default_root.parent, default_root):
        if candidate == Path(candidate.anchor) or not candidate.is_dir():
            continue
        if not os.access(candidate, os.W_OK | os.X_OK):
            continue
        longest_socket = (
            candidate
            / ("q" + "f" * 8)
            / (
                runner.ENGINE_SOCKET_DIRECTORY_PREFIX
                + "f" * runner.ENGINE_SOCKET_DIRECTORY_RANDOM_HEX_LENGTH
            )
            / "engine.sock"
        )
        if len(os.fsencode(str(longest_socket))) <= 100:
            return tempfile.TemporaryDirectory(prefix="q", dir=candidate)
    raise RuntimeError("no writable short temporary directory is available for AF_UNIX tests")


class TraefikNativeLocalPluginTest(unittest.TestCase):
    def test_local_plugin_package_matches_module_suffix(self) -> None:
        module = re.search(
            r"(?m)^module\s+([^\s]+)\s*$",
            (PLUGIN / "go.mod").read_text(encoding="utf-8"),
        )
        package = re.search(
            r"(?m)^package\s+([A-Za-z_][A-Za-z0-9_]*)\s*$",
            (PLUGIN / "middleware.go").read_text(encoding="utf-8"),
        )
        self.assertIsNotNone(module)
        self.assertIsNotNone(package)
        assert module is not None
        assert package is not None
        self.assertEqual(module.group(1).rsplit("/", 1)[-1], package.group(1))

    def test_native_host_runner_stages_plugin_and_refuses_promotion(self) -> None:
        source = (
            ROOT / "connectors" / "traefik" / "scripts" / "runtime_native_smoke.py"
        ).read_text(encoding="utf-8")
        self.assertIn('"plugins-local/src"', source)
        self.assertIn('"rule_evaluation": "host_runtime_observed_not_promoted"', source)
        self.assertNotIn('"rule_evaluation": "not_wired"', source)
        self.assertIn('"capability_promotion": "not_permitted"', source)
        self.assertIn('"integration_mode": "native-traefik-middleware"', source)
        self.assertIn('rule: "PathPrefix(`/`)"', source)

    def test_native_host_runner_uses_a_short_private_uds_root(self) -> None:
        source = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertIn("tempfile.mkdtemp", source)
        self.assertIn("TRAEFIK_ENGINE_SOCKET_PARENT", source)
        self.assertIn("resolve_engine_socket_parent", source)
        self.assertNotIn('dir="/var/tmp"', source)
        self.assertIn("ENGINE_SOCKET_PATH_MAX_BYTES", source)
        self.assertIn("engine_socket_dir = create_private_engine_socket_dir(engine_socket_parent)", source)
        self.assertIn('"host_runtime_cleanup_incomplete"', source)
        self.assertIn("DirectoryIdentity", source)

    def test_engine_socket_parent_resolution_prefers_explicit_then_tmpdir_then_generated_fallback(self) -> None:
        with tempfile.TemporaryDirectory(prefix="msconnector-traefik-test-") as temporary:
            root = Path(temporary)
            explicit = root / "explicit"
            tmpdir = root / "tmpdir"
            explicit.mkdir(mode=0o700)
            tmpdir.mkdir(mode=0o700)
            with mock.patch.dict(
                os.environ,
                {
                    runner.ENGINE_SOCKET_PARENT_ENV: str(explicit),
                    "TMPDIR": str(tmpdir),
                },
                clear=False,
            ):
                selected = runner.resolve_engine_socket_parent()
                self.assertEqual(selected.path, explicit)
                self.assertFalse(selected.generated)
            with mock.patch.dict(
                os.environ,
                {runner.ENGINE_SOCKET_PARENT_ENV: "", "TMPDIR": str(tmpdir)},
                clear=False,
            ):
                selected = runner.resolve_engine_socket_parent()
                self.assertEqual(selected.path, tmpdir)
                self.assertFalse(selected.generated)
            with mock.patch.dict(
                os.environ,
                {runner.ENGINE_SOCKET_PARENT_ENV: "", "TMPDIR": ""},
                clear=False,
            ), mock.patch.object(
                runner, "ENGINE_SOCKET_FALLBACK_ALLOCATION_ROOT", root
            ), mock.patch.object(runner, "ENGINE_SOCKET_PATH_MAX_BYTES", 1000):
                fallback = runner.resolve_engine_socket_parent()
                try:
                    self.assertEqual(fallback.path.parent, root)
                    self.assertTrue(
                        fallback.path.name.startswith(runner.ENGINE_SOCKET_FALLBACK_PARENT_PREFIX)
                    )
                    self.assertTrue(fallback.generated)
                    self.assertEqual(fallback.path.stat().st_mode & 0o777, 0o700)
                finally:
                    self.assertTrue(runner.remove_private_engine_socket_fallback_parent(fallback))

    def test_engine_socket_parent_rejects_unsafe_explicit_values(self) -> None:
        with tempfile.TemporaryDirectory(prefix="msconnector-traefik-test-") as temporary:
            root = Path(temporary)
            private = root / "private"
            private.mkdir(mode=0o700)
            nonprivate = root / "nonprivate"
            nonprivate.mkdir(mode=0o755)
            os.chmod(nonprivate, 0o755)
            symlink = root / "symlink"
            symlink.symlink_to(private, target_is_directory=True)
            regular = root / "regular"
            regular.write_text("not a directory", encoding="utf-8")
            for candidate, reason in (
                (Path("relative"), "absolute"),
                (Path("/tmp"), "too broad"),
                (ROOT, "outside checkout"),
                (nonprivate, "private"),
                (symlink, "symlink"),
                (regular, "directory"),
            ):
                with self.subTest(candidate=candidate):
                    with self.assertRaisesRegex(runner.MissingDependency, reason):
                        runner.assert_private_engine_socket_parent(candidate, "test parent")

    def test_engine_socket_parent_rejects_control_characters_and_yaml_quotes_paths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="msconnector-traefik-test-") as temporary:
            root = Path(temporary)
            control_parent = root / "private\ninjection"
            control_parent.mkdir(mode=0o700)
            with mock.patch.dict(
                os.environ,
                {runner.ENGINE_SOCKET_PARENT_ENV: str(control_parent), "TMPDIR": ""},
                clear=False,
            ):
                with self.assertRaisesRegex(runner.MissingDependency, "control characters"):
                    runner.resolve_engine_socket_parent()

            dynamic_config = root / "dynamic.yaml"
            unusual_socket = root / "socket: # value" / "engine.sock"
            runner.write_dynamic_config(dynamic_config, 18080, unusual_socket)
            self.assertIn(
                f"engineSocketPath: {json.dumps(str(unusual_socket))}",
                dynamic_config.read_text(encoding="utf-8"),
            )

    @mock.patch.object(runner, "ENGINE_SOCKET_PATH_MAX_BYTES", 1000)
    def test_engine_socket_child_is_private_short_and_cleanup_keeps_parent(self) -> None:
        with tempfile.TemporaryDirectory(prefix="msconnector-traefik-test-") as temporary:
            parent = Path(temporary)
            selected_parent = engine_socket_parent(parent)
            child = runner.create_private_engine_socket_dir(selected_parent)
            self.assertEqual(child.path.parent, parent)
            self.assertTrue(child.path.name.startswith(runner.ENGINE_SOCKET_DIRECTORY_PREFIX))
            self.assertEqual(child.path.stat().st_mode & 0o777, 0o700)
            self.assertLessEqual(
                len(os.fsencode(str(child.path / "engine.sock"))), runner.ENGINE_SOCKET_PATH_MAX_BYTES
            )
            self.assertTrue(runner.remove_private_engine_socket_dir(child, selected_parent))
            self.assertFalse(child.path.exists())
            self.assertTrue(parent.is_dir())

    @mock.patch.object(runner, "ENGINE_SOCKET_PATH_MAX_BYTES", 1000)
    def test_engine_socket_children_allocate_without_collision_for_parallel_runs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="msconnector-traefik-test-") as temporary:
            parent = Path(temporary)
            selected_parent = engine_socket_parent(parent)
            barrier = threading.Barrier(2)

            def allocate_child() -> object:
                barrier.wait(timeout=5)
                return runner.create_private_engine_socket_dir(selected_parent)

            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                first_future = executor.submit(allocate_child)
                second_future = executor.submit(allocate_child)
                first = first_future.result(timeout=5)
                second = second_future.result(timeout=5)
            try:
                self.assertNotEqual(first.path, second.path)
                self.assertTrue(first.path.is_dir())
                self.assertTrue(second.path.is_dir())
                self.assertEqual(first.path.parent, parent)
                self.assertEqual(second.path.parent, parent)
            finally:
                self.assertTrue(runner.remove_private_engine_socket_dir(first, selected_parent))
                self.assertTrue(runner.remove_private_engine_socket_dir(second, selected_parent))

    @mock.patch.object(runner, "ENGINE_SOCKET_PATH_MAX_BYTES", 1000)
    def test_engine_socket_child_preserves_an_existing_foreign_socket(self) -> None:
        with short_socket_temporary_directory() as temporary:
            parent = Path(temporary)
            selected_parent = engine_socket_parent(parent)
            foreign_child = runner.create_private_engine_socket_dir(selected_parent)
            foreign_socket = foreign_child.path / "engine.sock"
            server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                server.bind(os.fspath(foreign_socket))
                next_child = runner.create_private_engine_socket_dir(selected_parent)
                try:
                    self.assertNotEqual(next_child, foreign_child)
                    self.assertTrue(foreign_socket.exists())
                    self.assertFalse((next_child.path / "engine.sock").exists())
                finally:
                    self.assertTrue(
                        runner.remove_private_engine_socket_dir(
                            next_child, selected_parent
                        )
                    )
            finally:
                server.close()
                self.assertFalse(
                    runner.remove_private_engine_socket_dir(foreign_child, selected_parent)
                )
                self.assertTrue(foreign_socket.exists())
                foreign_socket.unlink()
                self.assertTrue(
                    runner.remove_private_engine_socket_dir(foreign_child, selected_parent)
                )

    @mock.patch.object(runner, "ENGINE_SOCKET_PATH_MAX_BYTES", 1000)
    def test_engine_socket_cleanup_refuses_replaced_child_or_fallback_parent(self) -> None:
        with tempfile.TemporaryDirectory(prefix="msconnector-traefik-test-") as temporary:
            root = Path(temporary)
            selected_parent = engine_socket_parent(root)
            child = runner.create_private_engine_socket_dir(selected_parent)
            child.path.rmdir()
            child.path.mkdir(mode=0o700)
            self.assertFalse(runner.remove_private_engine_socket_dir(child, selected_parent))
            self.assertTrue(child.path.exists())
            child.path.rmdir()

            with mock.patch.object(runner, "ENGINE_SOCKET_FALLBACK_ALLOCATION_ROOT", root), mock.patch.object(
                runner, "ENGINE_SOCKET_PATH_MAX_BYTES", 1000
            ):
                fallback = runner.create_private_engine_socket_fallback_parent()
                fallback.path.rmdir()
                fallback.path.mkdir(mode=0o700)
                self.assertFalse(runner.remove_private_engine_socket_fallback_parent(fallback))
                self.assertTrue(fallback.path.exists())
                fallback.path.rmdir()

    def test_engine_socket_setup_failure_removes_the_allocated_child(self) -> None:
        with tempfile.TemporaryDirectory(prefix="msconnector-traefik-test-") as temporary:
            root = Path(temporary)
            runtime_root = root / "runtime"
            parent_path = root / "socket-parent"
            parent_path.mkdir(mode=0o700)
            selected_parent = engine_socket_parent(parent_path)
            with mock.patch.dict(
                os.environ,
                {"TRAEFIK_NATIVE_RUNTIME_ROOT": str(runtime_root), "TRAEFIK_BIN": "/bin/true"},
                clear=False,
            ), mock.patch.object(runner, "assert_runtime_root", return_value=runtime_root), mock.patch.object(
                runner, "require_local_executable", return_value=Path("/bin/true")
            ), mock.patch.object(
                runner, "require_modsecurity_environment", return_value=(root, root)
            ), mock.patch.object(
                runner, "select_engine_rules", return_value=(root / "rules", {}, "test")
            ), mock.patch.object(
                runner, "require_engine_inputs"
            ), mock.patch.object(
                runner, "read_plugin_module", return_value="test-plugin"
            ), mock.patch.object(
                runner, "resolve_engine_socket_parent", return_value=selected_parent
            ), mock.patch.object(
                runner, "free_port", side_effect=RuntimeError("injected setup failure")
            ), mock.patch.object(
                runner, "ENGINE_SOCKET_PATH_MAX_BYTES", 1000
            ):
                with self.assertRaisesRegex(RuntimeError, "injected setup failure"):
                    runner.run()
            self.assertEqual(list(parent_path.iterdir()), [])

    def test_engine_socket_parent_length_is_checked_before_child_allocation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="msconnector-traefik-test-") as temporary:
            parent = Path(temporary) / ("x" * 90)
            parent.mkdir(mode=0o700)
            with self.assertRaisesRegex(runner.MissingDependency, "too long"):
                runner.assert_engine_socket_path_length(parent)

    def test_engine_service_runtime_test_uses_a_short_private_uds_root(self) -> None:
        source = (
            ROOT / "connectors" / "traefik" / "build" / "test-engine-service-runtime.sh"
        ).read_text(encoding="utf-8")
        self.assertIn('SOCKET_PARENT="${TRAEFIK_ENGINE_SOCKET_TEST_PARENT:-/var/tmp}"', source)
        self.assertIn('mktemp -d "$SOCKET_PARENT"/msconnector-traefik-engine-test.XXXXXX', source)
        self.assertIn('SOCKET_PATH="$SOCKET_DIR/engine.sock"', source)
        self.assertIn('[ "${#SOCKET_PATH}" -le 100 ]', source)
        self.assertIn('rmdir "$SOCKET_DIR"', source)
        self.assertIn("replacement-sentinel", source)
        self.assertNotIn('rm -f "$SOCKET_PATH"', source)

    def test_engine_service_binds_cleanup_to_the_created_socket_identity(self) -> None:
        source = (
            ROOT / "connectors" / "traefik" / "src" / "traefik_engine_service.c"
        ).read_text(encoding="utf-8")
        self.assertIn("traefik_engine_socket_identity", source)
        self.assertIn("traefik_engine_capture_bound_socket_identity", source)
        self.assertIn("traefik_engine_remove_owned_socket", source)
        self.assertIn("traefik_engine_listener_accepts_self_probe", source)
        self.assertIn("SO_PEERCRED", source)
        self.assertIn("traefik_engine_listener_post_bind_hook", source)
        self.assertIn("traefik_engine_listener_post_probe_hook", source)
        self.assertIn("fchmod(socket_fd, S_IRUSR | S_IWUSR)", source)
        listener_source = source[
            source.index("static int traefik_engine_create_listener") : source.index(
                "static void traefik_engine_wait_for_workers"
            )
        ]
        serve_source = source[
            source.index("static int traefik_engine_serve") : source.index(
                "static int traefik_engine_self_test_append_u16"
            )
        ]
        self.assertNotIn("(void)unlink(socket_path);", listener_source)
        self.assertNotIn("(void)unlink(socket_path);", serve_source)


if __name__ == "__main__":
    unittest.main()
