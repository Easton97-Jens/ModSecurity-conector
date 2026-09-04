"""Mutation coverage for Apache's helper-aware Common-adoption checker."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER_DIRECTORY = ROOT / "ci" / "checks" / "connectors" / "apache"
APACHE_DIRECTORY = ROOT / "connectors" / "apache"
FILTERS_RELATIVE_PATH = Path("connectors/apache/src/msc_filters.c")
sys.path.insert(0, str(CHECKER_DIRECTORY))

import apache_common_adoption_base as checker_base


def replace_once(path: Path, old: str, new: str) -> None:
    """Replace one expected source fragment or fail the test setup loudly."""
    source = path.read_text(encoding="utf-8")
    if source.count(old) != 1:
        raise AssertionError(f"expected one mutable fragment in {path}: {old!r}")
    path.write_text(source.replace(old, new, 1), encoding="utf-8")


class ApacheCommonAdoptionCheckerTests(unittest.TestCase):
    """Exercise the checker against compact, isolated source mutations."""

    def _copy_repository(self, destination: Path) -> Path:
        (destination / "Makefile").write_text(
            "# synthetic checker repository\n", encoding="utf-8"
        )
        checker_destination = destination / "ci" / "checks" / "connectors" / "apache"
        checker_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(CHECKER_DIRECTORY, checker_destination)
        apache_destination = destination / "connectors" / "apache"
        apache_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(APACHE_DIRECTORY, apache_destination)
        for relative_path in (
            Path("docs/connectors/apache.md"),
            Path("reports/audits/architecture-and-evidence.md"),
        ):
            source = ROOT / relative_path
            target = destination / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        return destination / FILTERS_RELATIVE_PATH

    def _run_checker(self, mutate=None) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="apache-common-adoption-") as temporary:
            repository = Path(temporary)
            filters = self._copy_repository(repository)
            if mutate is not None:
                mutate(filters)
            environment = os.environ.copy()
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            return subprocess.run(
                [
                    sys.executable,
                    str(
                        repository
                        / "ci"
                        / "checks"
                        / "connectors"
                        / "apache"
                        / "check-apache-common-adoption.py"
                    ),
                ],
                cwd=repository,
                env=environment,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

    def _assert_rejected(self, mutate, message: str) -> None:
        result = self._run_checker(mutate)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(message, result.stdout + result.stderr)

    def test_current_helper_based_input_filter_is_accepted(self) -> None:
        result = self._run_checker()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "apache-common-adoption: scoped review guards passed",
            result.stdout,
        )

    def test_masking_keeps_code_offsets_while_hiding_decoy_tokens(self) -> None:
        source = (
            "int active = 1; // append decoy\n"
            "/* block\ncomment */ int tail = 2;\n"
            'const char *literal = "// not a comment";\n'
            "const char quote = '\\''; // after literal\n"
            '"unterminated literal\n'
        )

        masked = checker_base._mask_c_comments_and_literals(source)

        self.assertEqual(len(masked), len(source))
        self.assertEqual(masked.count("\n"), source.count("\n"))
        self.assertIn("int active = 1;", masked)
        self.assertIn("int tail = 2;", masked)
        self.assertNotIn("append decoy", masked)
        self.assertNotIn("block", masked)
        self.assertNotIn("not a comment", masked)
        self.assertNotIn("after literal", masked)
        self.assertNotIn("unterminated literal", masked)

    def test_missing_eos_helper_call_is_rejected(self) -> None:
        def mutate(filters: Path) -> None:
            replace_once(
                filters,
                "            return apache_input_filter_handle_eos(msr, r, f, pbbOut, pbktIn);\n",
                "            return APR_EGENERAL;\n",
            )

        self._assert_rejected(
            mutate,
            "Apache input-filter errors enter Apache core through the input-side terminal bridge",
        )

    def test_forwarding_before_validation_is_rejected(self) -> None:
        def mutate(filters: Path) -> None:
            replace_once(
                filters,
                "    if (ret != APR_SUCCESS)\n        return ret;\n",
                "    if (ret != APR_SUCCESS)\n        return ret;\n"
                "    APR_BUCKET_REMOVE(bucket);\n"
                "    APR_BRIGADE_INSERT_TAIL(output, bucket);\n",
            )
            replace_once(
                filters,
                "    APR_BUCKET_REMOVE(bucket);\n"
                "    APR_BRIGADE_INSERT_TAIL(output, bucket);\n"
                "    return APR_SUCCESS;\n",
                "    return APR_SUCCESS;\n",
            )

        self._assert_rejected(
            mutate,
            "Apache Phase2 bounded bucket helper reads, plans, records, appends",
        )

    def test_unreachable_pipeline_decoy_is_rejected(self) -> None:
        def mutate(filters: Path) -> None:
            replace_once(
                filters,
                "    if (msr->contract.active_phase != MSCONNECTOR_PHASE_REQUEST_BODY &&\n"
                "        !msc_apache_contract_begin(msr, MSCONNECTOR_PHASE_REQUEST_BODY)) {\n",
                "    if (0) {\n"
                "    if (msr->contract.active_phase != MSCONNECTOR_PHASE_REQUEST_BODY &&\n"
                "        !msc_apache_contract_begin(msr, MSCONNECTOR_PHASE_REQUEST_BODY)) {\n",
            )
            replace_once(
                filters,
                "    if (plan.truncated)\n"
                "        msr->request_body_truncated = 1;\n"
                "    APR_BUCKET_REMOVE(bucket);\n",
                "    if (plan.truncated)\n"
                "        msr->request_body_truncated = 1;\n"
                "    }\n"
                "    APR_BUCKET_REMOVE(bucket);\n",
            )

        self._assert_rejected(
            mutate,
            "Apache Phase2 direct bucket pipeline cannot satisfy its bounded-forwarding contract",
        )

    def test_removed_eos_finalization_is_rejected(self) -> None:
        def mutate(filters: Path) -> None:
            replace_once(
                filters,
                "        intervention = msc_finalize_request_body(msr, r);\n",
                "        intervention = N_INTERVENTION_STATUS;\n",
            )

        self._assert_rejected(
            mutate,
            "Apache request chunks are borrowed and phase 2 finalizes once at EOS",
        )

    def test_unreachable_eos_finalization_decoy_is_rejected(self) -> None:
        def mutate(filters: Path) -> None:
            replace_once(
                filters,
                "        intervention = msc_finalize_request_body(msr, r);\n",
                "        if (0)\n"
                "        {\n"
                "            intervention = msc_finalize_request_body(msr, r);\n"
                "        }\n"
                "        intervention = N_INTERVENTION_STATUS;\n",
            )

        self._assert_rejected(
            mutate,
            "Apache Phase2 EOS helper has one direct canonical success tail and no dead-code control transfer",
        )

    def test_removed_duplicate_eos_terminal_bridge_is_rejected(self) -> None:
        def mutate(filters: Path) -> None:
            replace_once(
                filters,
                "        ap_remove_input_filter(filter);\n"
                "        return apache_input_filter_terminal_error(msr, r,\n"
                "            HTTP_INTERNAL_SERVER_ERROR);\n",
                "        ap_remove_input_filter(filter);\n"
                "        return APR_EGENERAL;\n",
            )

        self._assert_rejected(
            mutate,
            "Apache input-filter errors enter Apache core through the input-side terminal bridge",
        )

    def test_comment_only_eos_helper_token_is_rejected(self) -> None:
        def mutate(filters: Path) -> None:
            replace_once(
                filters,
                "            return apache_input_filter_handle_eos(msr, r, f, pbbOut, pbktIn);\n",
                "            return APR_EGENERAL;\n",
            )
            with filters.open("a", encoding="utf-8") as source:
                source.write(
                    "\n/* apache_input_filter_handle_eos(msr, r, f, pbbOut, pbktIn); */\n"
                )

        self._assert_rejected(
            mutate,
            "Apache input-filter errors enter Apache core through the input-side terminal bridge",
        )

    def test_foreign_function_eos_helper_token_is_rejected(self) -> None:
        def mutate(filters: Path) -> None:
            replace_once(
                filters,
                "            return apache_input_filter_handle_eos(msr, r, f, pbbOut, pbktIn);\n",
                "            return APR_EGENERAL;\n",
            )
            with filters.open("a", encoding="utf-8") as source:
                source.write(
                    "\nstatic void apache_input_filter_decoy(void)\n"
                    "{\n"
                    "    (void)apache_input_filter_handle_eos(NULL, NULL, NULL, NULL, NULL);\n"
                    "}\n"
                )

        self._assert_rejected(
            mutate,
            "Apache input-filter errors enter Apache core through the input-side terminal bridge",
        )

    def test_unbounded_append_is_rejected(self) -> None:
        def mutate(filters: Path) -> None:
            replace_once(
                filters,
                "            (const unsigned char *)data, plan.append_size) != 1) {\n",
                "            (const unsigned char *)data, len) != 1) {\n",
            )

        self._assert_rejected(
            mutate,
            "Apache Phase2 bounded bucket helper reads, plans, records, appends",
        )


if __name__ == "__main__":
    unittest.main()
