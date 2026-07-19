#!/usr/bin/env python3
"""Test the Parent-owned Apache Phase-4 synchronized-upstream wrapper."""

import argparse
from importlib.util import module_from_spec, spec_from_file_location
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest


ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "Makefile").is_file()
)
TARGET = ROOT / "ci/runtime/lifecycle/apache_phase4_content_type_synchronized_upstream.py"
FRAMEWORK_HELPER_MODULE = "phase4_framework_synchronized_upstream"


class ApachePhase4ContentTypeSynchronizedUpstreamTest(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory()
        temporary_root = Path(self._temporary_directory.name)
        framework_root = temporary_root / "framework"
        helper = framework_root / "tests/runners/synchronized_upstream.py"
        helper.parent.mkdir(parents=True)
        helper.write_text(
            "class StreamingProbeError(RuntimeError):\n"
            "    pass\n\n"
            "class SynchronizedStreamingUpstream:\n"
            "    pass\n",
            encoding="utf-8",
        )
        self._control_root = temporary_root / "controls"
        self._control_root.mkdir()
        self._previous_framework_root = os.environ.get("FRAMEWORK_ROOT")
        self._previous_framework_helper = sys.modules.pop(
            FRAMEWORK_HELPER_MODULE, None
        )
        self._module_name = (
            f"apache_phase4_content_type_synchronized_upstream_{id(self)}"
        )
        os.environ["FRAMEWORK_ROOT"] = str(framework_root)
        spec = spec_from_file_location(self._module_name, TARGET)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = module_from_spec(spec)
        sys.modules[self._module_name] = module
        spec.loader.exec_module(module)
        self._module = module

    def tearDown(self) -> None:
        sys.modules.pop(self._module_name, None)
        sys.modules.pop(FRAMEWORK_HELPER_MODULE, None)
        if self._previous_framework_helper is not None:
            sys.modules[FRAMEWORK_HELPER_MODULE] = self._previous_framework_helper
        if self._previous_framework_root is None:
            os.environ.pop("FRAMEWORK_ROOT", None)
        else:
            os.environ["FRAMEWORK_ROOT"] = self._previous_framework_root
        self._temporary_directory.cleanup()

    def control_args(self, **overrides: object) -> argparse.Namespace:
        values: dict[str, object] = {
            "control_root": str(self._control_root),
            "ready_file": str(self._control_root / "ready.json"),
            "release_file": str(self._control_root / "release.json"),
            "paused_file": str(self._control_root / "paused.json"),
            "server_evidence_file": str(self._control_root / "evidence.json"),
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def test_control_paths_accept_distinct_files_beneath_existing_root(self) -> None:
        control_root, ready, release, paused, evidence = self._module.resolve_control_paths(
            self.control_args()
        )

        self.assertEqual(control_root, self._control_root.resolve())
        self.assertEqual(ready, self._control_root / "ready.json")
        self.assertEqual(release, self._control_root / "release.json")
        self.assertEqual(paused, self._control_root / "paused.json")
        self.assertEqual(evidence, self._control_root / "evidence.json")

    def test_control_paths_reject_a_file_outside_the_control_root(self) -> None:
        outside = Path(self._temporary_directory.name) / "outside-release.json"
        args = self.control_args(release_file=str(outside))

        with self.assertRaisesRegex(
            ValueError, "release file must resolve beneath control root"
        ):
            self._module.resolve_control_paths(args)

    def test_control_writer_rejects_an_outside_root_path_before_creation(self) -> None:
        outside = Path(self._temporary_directory.name) / "outside" / "control.json"

        with self.assertRaisesRegex(
            ValueError, "control file must resolve beneath control root"
        ):
            self._module.write_control_json(
                outside, {"schema_version": 1}, control_root=self._control_root
            )

        self.assertFalse(outside.parent.exists())

    def test_control_paths_reject_an_existing_symlink_escape(self) -> None:
        outside = Path(self._temporary_directory.name) / "outside"
        outside.mkdir()
        escape = self._control_root / "escape"
        escape.symlink_to(outside, target_is_directory=True)
        args = self.control_args(ready_file=str(escape / "ready.json"))

        with self.assertRaisesRegex(
            ValueError, "ready file must resolve beneath control root"
        ):
            self._module.resolve_control_paths(args)

    def test_missing_listener_is_recorded_as_a_server_failure(self) -> None:
        upstream = object.__new__(
            self._module.ContentTypedSynchronizedStreamingUpstream
        )
        upstream._listener = None
        upstream._connection = None
        upstream._closed = threading.Event()
        upstream._error = None

        upstream._serve_once()

        self.assertIsInstance(upstream._error, RuntimeError)
        self.assertTrue(upstream._closed.is_set())

    def test_interrupt_propagates_after_listener_cleanup(self) -> None:
        class InterruptingListener:
            def __init__(self) -> None:
                self.closed = False

            def accept(self) -> None:
                raise KeyboardInterrupt

            def close(self) -> None:
                self.closed = True

        listener = InterruptingListener()
        upstream = object.__new__(
            self._module.ContentTypedSynchronizedStreamingUpstream
        )
        upstream._listener = listener
        upstream._connection = None
        upstream._closed = threading.Event()
        upstream._error = None

        with self.assertRaises(KeyboardInterrupt):
            upstream._serve_once()

        self.assertIsNone(upstream._error)
        self.assertTrue(listener.closed)
        self.assertTrue(upstream._closed.is_set())


if __name__ == "__main__":
    unittest.main()
