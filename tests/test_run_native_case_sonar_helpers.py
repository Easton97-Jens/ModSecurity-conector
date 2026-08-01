from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "ci" / "runtime" / "lifecycle" / "run-native-case-comparison.py"
sys.path.insert(0, str(ROOT / "ci" / "lib"))
from runtime_path_utils import ensure_safe_runtime_directory


SPEC = importlib.util.spec_from_file_location("native_case_sonar_helpers", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
native_case = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = native_case
SPEC.loader.exec_module(native_case)


class NativeCaseSonarHelpersTest(unittest.TestCase):
    def test_missing_native_prerequisite_keeps_the_full_report_contract(self) -> None:
        with tempfile.TemporaryDirectory(prefix="native-case-sonar-") as temporary:
            root = Path(temporary)
            verified_run_root = ensure_safe_runtime_directory(root / "verified-run")
            case_path = root / "case.yaml"
            case_path.write_text("case fixture\n", encoding="utf-8")
            case_data = {
                "request": {"method": "POST", "path": "/native", "body": "body"},
                "expect": {"status": 403},
                "rules": "",
            }

            with (
                mock.patch.object(native_case, "find_case_path", return_value=case_path),
                mock.patch.object(native_case, "load_case", return_value=case_data),
            ):
                result = native_case.run_native_case(
                    "blocked-native-case",
                    ROOT,
                    root / "framework",
                    verified_run_root,
                    {},
                )

            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["return_code"], 77)
            self.assertEqual(result["expected_status"], 403)
            self.assertEqual(result["native_actual"], None)
            self.assertFalse(result["native_match"])
            self.assertEqual(result["compile"]["reason"], "MODSECURITY_INCLUDE_DIR missing")
            run_dir = Path(result["run_dir"])
            self.assertTrue((run_dir / "native-case-run.md").is_file())
            self.assertEqual(
                json.loads((run_dir / native_case.NATIVE_CASE_RUN_FILENAME).read_text(encoding="utf-8")),
                result,
            )

    def test_missing_case_keeps_the_blocked_report_contract(self) -> None:
        with tempfile.TemporaryDirectory(prefix="native-case-sonar-") as temporary:
            root = Path(temporary)
            verified_run_root = ensure_safe_runtime_directory(root / "verified-run")

            result = native_case.run_native_case(
                "missing-case",
                ROOT,
                root / "missing-framework",
                verified_run_root,
                {},
            )

            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["native_actual"], None)
            self.assertEqual(result["reason"], "case YAML not found")
            report_path = Path(result["run_dir"]) / native_case.NATIVE_CASE_RUN_FILENAME
            self.assertEqual(json.loads(report_path.read_text(encoding="utf-8")), result)

    def test_native_json_writer_rejects_a_symlink_destination(self) -> None:
        with tempfile.TemporaryDirectory(prefix="native-case-sonar-") as temporary:
            root = Path(temporary)
            run_root = ensure_safe_runtime_directory(root / "verified-run")
            victim = root / "outside.json"
            victim.write_text('{"preserve": true}\n', encoding="utf-8")
            target = run_root / "native-result.json"
            target.symlink_to(victim)

            with self.assertRaises(ValueError):
                native_case.write_json(
                    run_root,
                    target,
                    {"status": "blocked"},
                    "native result",
                )

            self.assertEqual(victim.read_text(encoding="utf-8"), '{"preserve": true}\n')


if __name__ == "__main__":
    unittest.main()
