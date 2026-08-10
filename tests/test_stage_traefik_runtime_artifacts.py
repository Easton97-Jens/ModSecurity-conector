"""Contracts for the fixed Traefik build-root to raw-run staging bridge."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import stat
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CI_LIB = ROOT / "ci" / "lib"
if str(CI_LIB) not in sys.path:
    sys.path.insert(0, str(CI_LIB))

SPECIFICATION = importlib.util.spec_from_file_location(
    "stage_traefik_runtime_artifacts_contract",
    ROOT / "ci" / "runtime" / "lifecycle" / "stage-traefik-runtime-artifacts.py",
)
assert SPECIFICATION is not None
assert SPECIFICATION.loader is not None
STAGER = importlib.util.module_from_spec(SPECIFICATION)
sys.modules[SPECIFICATION.name] = STAGER
SPECIFICATION.loader.exec_module(STAGER)


class StageTraefikRuntimeArtifactsTest(unittest.TestCase):
    def test_moves_only_fixed_regular_outputs_into_raw_run(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage-traefik-runtime-") as temporary:
            parent = Path(temporary)
            build_root = parent / "build"
            runtime_root = build_root / "traefik-runtime"
            events = runtime_root / "logs" / "events.jsonl"
            events.parent.mkdir(parents=True)
            result = runtime_root / "result.json"
            result.write_text('{"connector":"traefik"}\n', encoding="utf-8")
            events.write_text('{"event":"blocked"}\n', encoding="utf-8")
            raw_root = parent / "raw"

            staged = STAGER.stage_traefik_runtime_artifacts(build_root, raw_root)

            expected_result = raw_root / "traefik-source" / "result.json"
            expected_events = raw_root / "traefik-source" / "events.jsonl"
            self.assertEqual(staged, (expected_result, expected_events))
            self.assertFalse(result.exists())
            self.assertFalse(events.exists())
            self.assertEqual(expected_result.read_text(encoding="utf-8"), '{"connector":"traefik"}\n')
            self.assertEqual(expected_events.read_text(encoding="utf-8"), '{"event":"blocked"}\n')
            self.assertEqual(stat.S_IMODE(expected_result.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(expected_events.stat().st_mode), 0o600)

    def test_event_failure_after_result_move_fails_closed_before_collection(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage-traefik-runtime-failure-") as temporary:
            parent = Path(temporary)
            build_root = parent / "build"
            runtime_root = build_root / "traefik-runtime"
            runtime_root.mkdir(parents=True)
            result = runtime_root / "result.json"
            result.write_text('{"connector":"traefik"}\n', encoding="utf-8")
            logs = runtime_root / "logs"
            logs.mkdir()
            event_directory = logs / "events.jsonl"
            event_directory.mkdir()
            raw_root = parent / "raw"

            with self.assertRaisesRegex(ValueError, "existing regular file"):
                STAGER.stage_traefik_runtime_artifacts(build_root, raw_root)

            self.assertFalse(result.exists())
            self.assertTrue((raw_root / "traefik-source" / "result.json").is_file())
            self.assertTrue(event_directory.is_dir())

    def test_absence_stays_absence_and_symlink_sources_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage-traefik-runtime-absence-") as temporary:
            parent = Path(temporary)
            build_root = parent / "build"
            raw_root = parent / "raw"
            build_root.mkdir()
            self.assertEqual(STAGER.stage_traefik_runtime_artifacts(build_root, raw_root), ())
            with self.assertRaisesRegex(ValueError, "must remain separate"):
                STAGER.stage_traefik_runtime_artifacts(build_root, build_root)

            runtime_root = build_root / "traefik-runtime"
            runtime_root.mkdir()
            target = parent / "outside.json"
            target.write_text("outside\n", encoding="utf-8")
            (runtime_root / "result.json").symlink_to(target)
            with self.assertRaisesRegex(
                ValueError, "symbolic link|must not use symbolic links|below the runtime root"
            ):
                STAGER.stage_traefik_runtime_artifacts(build_root, raw_root)


if __name__ == "__main__":
    unittest.main()
