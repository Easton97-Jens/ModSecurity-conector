"""Contract coverage for Apache Framework case-output containment."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "connectors" / "apache" / "harness" / "run_apache_smoke.sh"
LIFECYCLE = ROOT / "ci" / "runtime" / "lifecycle" / "run-no-crs-baseline.sh"


class ApacheSmokeCaseOutputRootTest(unittest.TestCase):
    def test_harness_passes_one_explicit_output_root_to_each_framework_case_writer(self) -> None:
        source = HARNESS.read_text(encoding="utf-8")
        self.assertIn('APACHE_CASE_OUTPUT_ROOT="${APACHE_CASE_OUTPUT_ROOT:-$BUILD_ROOT}"', source)
        self.assertIn(
            'require_absolute_generated_path "$APACHE_CASE_OUTPUT_ROOT" "APACHE_CASE_OUTPUT_ROOT"',
            source,
        )
        self.assertEqual(source.count('--output-root "$APACHE_CASE_OUTPUT_ROOT"'), 3)

    def test_no_crs_lifecycle_keeps_apache_case_outputs_inside_host_runtime(self) -> None:
        source = LIFECYCLE.read_text(encoding="utf-8")
        self.assertIn(
            'APACHE_RUNTIME_LOG_DIR="$HOST_RUNTIME_ROOT/apache-runtime"',
            source,
        )
        self.assertIn('APACHE_CASE_OUTPUT_ROOT="$HOST_RUNTIME_ROOT"', source)


if __name__ == "__main__":
    unittest.main()
