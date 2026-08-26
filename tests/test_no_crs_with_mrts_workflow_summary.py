"""Behavioral contracts for the no-CRS/with-MRTS GitHub job summary."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "ci" / "runtime" / "lifecycle" / "summarize-no-crs-with-mrts-workflow.py"


def load_summary() -> object:
    specification = importlib.util.spec_from_file_location(
        "no_crs_with_mrts_workflow_summary", SUMMARY_PATH
    )
    if specification is None or specification.loader is None:
        raise AssertionError(f"cannot load {SUMMARY_PATH}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


SUMMARY = load_summary()


def assert_summary_path_safety(
    test_case: unittest.TestCase,
    summary: object,
    environment: dict[str, str],
    *,
    check_nonblock: bool = False,
) -> None:
    with tempfile.TemporaryDirectory(prefix="workflow-summary-runner-") as temporary:
        root = Path(temporary)
        runner_temp = root / "runner-temp"
        summary_directory = runner_temp / "_runner_file_commands"
        summary_directory.mkdir(parents=True)
        target = summary_directory / "step_summary_abc123"
        target.touch()
        target.chmod(0o600)
        configured_environment = {
            **environment,
            "RUNNER_TEMP": str(runner_temp),
            "GITHUB_STEP_SUMMARY": str(target),
        }
        summary.append_github_step_summary(configured_environment, "first\n")
        test_case.assertEqual(target.read_text(encoding="utf-8"), "first\n")
        with mock.patch.dict(summary.os.environ, configured_environment, clear=True):
            test_case.assertEqual(summary.main(["--connector", "apache"]), 0)
        test_case.assertIn("### apache", target.read_text(encoding="utf-8"))

        outside = root / "outside.md"
        outside.touch()
        outside.chmod(0o600)
        with test_case.assertRaisesRegex(ValueError, "path is unsafe"):
            summary.append_github_step_summary(
                {**configured_environment, "GITHUB_STEP_SUMMARY": str(outside)},
                "must-not-write\n",
            )
        with test_case.assertRaisesRegex(ValueError, "path is unsafe"):
            summary.append_github_step_summary(
                {
                    **configured_environment,
                    "GITHUB_STEP_SUMMARY": str(
                        summary_directory / ".." / "step_summary_abc123"
                    ),
                },
                "must-not-write\n",
            )
        target.unlink()
        target.symlink_to(outside)
        with test_case.assertRaisesRegex(ValueError, "path is unsafe"):
            summary.append_github_step_summary(configured_environment, "must-not-follow\n")
        with mock.patch.object(summary.os, "O_NOFOLLOW", None):
            with test_case.assertRaisesRegex(ValueError, "safe-open capability"):
                summary.append_github_step_summary(configured_environment, "must-not-write\n")
        if check_nonblock:
            with mock.patch.object(summary.os, "O_NONBLOCK", None):
                with test_case.assertRaisesRegex(ValueError, "safe-open capability"):
                    summary.append_github_step_summary(
                        configured_environment, "must-not-write\n"
                    )


class NoCrsWithMrtsWorkflowSummaryTest(unittest.TestCase):
    def outcomes(self, **overrides: str) -> dict[str, str]:
        values = {stage: "success" for stage, _label, _environment_name in SUMMARY.STAGES}
        values.update(overrides)
        return values

    def test_summary_reports_actual_connector_local_outcomes(self) -> None:
        summary = SUMMARY.render_summary(
            "traefik", self.outcomes(prepare_runtime="failure", runtime="skipped")
        )
        self.assertIn("### traefik — no-CRS/with-MRTS runtime overview", summary)
        self.assertIn("| Stages passed | `8` |", summary)
        self.assertIn("| Stages failed | `1` |", summary)
        self.assertIn("| Stages skipped | `1` |", summary)
        self.assertIn(
            "| First non-passing stage | `Connector-isolated runtime preparation` |", summary
        )
        self.assertIn("| Real connector MRTS host runtime | `skipped` |", summary)
        self.assertIn("`MISSING — runtime target did not run`", summary)
        self.assertNotIn("PASS — real target", summary)

    def test_summary_marks_all_go_stages_not_applicable_for_apache_and_haproxy(self) -> None:
        summary = SUMMARY.render_summary(
            "apache",
            self.outcomes(
                setup_go="skipped", verify_go="skipped", snapshot_go="skipped"
            ),
        )
        self.assertIn("| Stages passed | `7` |", summary)
        self.assertIn("| Stages skipped | `0` |", summary)
        self.assertIn("| First non-passing stage | `none` |", summary)
        self.assertIn("| Locked Go toolchain | `not_applicable` |", summary)
        self.assertIn("| Go interpreter contract | `not_applicable` |", summary)
        self.assertIn("| Verified setup-Go binary provenance | `not_applicable` |", summary)

    def test_summary_reports_cancelled_runtime_as_not_completed(self) -> None:
        summary = SUMMARY.render_summary("envoy", self.outcomes(runtime="cancelled"))
        self.assertIn("| Stages cancelled | `1` |", summary)
        self.assertIn("`CANCELLED — runtime target did not complete`", summary)

    def test_summary_rejects_unclosed_connector_and_missing_outcome(self) -> None:
        outcomes = self.outcomes()
        with self.assertRaisesRegex(ValueError, "fixed no-CRS/with-MRTS"):
            SUMMARY.render_summary("nginx", outcomes)
        environment = {
            environment_name: "success" for _stage, _label, environment_name in SUMMARY.STAGES
        }
        environment.pop("RUNTIME_OUTCOME")
        with self.assertRaisesRegex(ValueError, "RUNTIME_OUTCOME"):
            SUMMARY.outcomes_from_environment(environment)

    def test_summary_requires_a_runner_owned_nonsymlink_file(self) -> None:
        environment = {
            environment_name: "success"
            for _stage, _label, environment_name in SUMMARY.STAGES
        }
        assert_summary_path_safety(self, SUMMARY, environment)


if __name__ == "__main__":
    unittest.main()
