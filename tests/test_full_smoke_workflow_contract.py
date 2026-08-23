"""Static contracts for retained heavy-smoke runtime evidence."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "test-full-smoke-sequential.yml"


class FullSmokeWorkflowContractTest(unittest.TestCase):
    def test_runtime_component_reports_are_private_and_retained(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        initialize_start = workflow.index("      - name: Initialize paths\n")
        initialize_end = workflow.index("\n      - name: Lint and py-compile\n", initialize_start)
        initialize_paths = workflow[initialize_start:initialize_end]
        upload_start = workflow.index("      - name: Upload smoke artifacts\n")
        upload = workflow[upload_start:]

        self.assertIn(
            'echo "RUNTIME_REPORT_OUTPUT_ROOT=$build_root/runtime-component-reports"',
            initialize_paths,
        )
        self.assertIn(
            "${{ steps.paths.outputs.build_root }}/runtime-component-reports",
            upload,
        )
        self.assertNotIn("$GITHUB_WORKSPACE", initialize_paths)


if __name__ == "__main__":
    unittest.main()
