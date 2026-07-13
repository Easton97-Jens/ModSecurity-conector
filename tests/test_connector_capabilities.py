from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci" / "evidence" / "collectors"))
SPEC = importlib.util.spec_from_file_location(
    "connector_capabilities", ROOT / "ci/evidence/collectors/connector_capabilities.py"
)
assert SPEC is not None and SPEC.loader is not None
connector_capabilities = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(connector_capabilities)


class ConnectorCapabilitiesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifests, errors = connector_capabilities.load_manifests()
        assert not errors, errors

    def _results(self, run_id: str) -> dict[str, dict[str, object]]:
        results: dict[str, dict[str, object]] = {}
        for connector in connector_capabilities.CONNECTORS:
            states = {
                name: self.manifests[connector]["capabilities"][name]["state"]
                for name in connector_capabilities.CAPABILITY_NAMES
            }
            results[connector] = {
                "result": {
                    "status": "PASS",
                    "source_failure": False,
                    "cases_failed": 0,
                    "cases_blocked": 0,
                    "capabilities_verified": ["request_headers"],
                    "capability_states": states,
                },
                "path": f"{connector}/{run_id}/result.json",
                "sha256": "a" * 64,
            }
        return results

    def test_static_payload_remains_source_contract_only(self) -> None:
        payload = connector_capabilities.aggregate_payload(self.manifests)
        self.assertFalse(payload["runtime_promotion"])
        self.assertNotIn("runtime_evidence", payload)

    def test_runtime_merge_is_report_only_and_promotes_checked_capabilities(self) -> None:
        run_id = "ci-123"
        source_snapshot = copy.deepcopy(self.manifests)
        results = self._results(run_id)
        results["nginx"]["result"]["status"] = "FAIL"  # type: ignore[index]

        merged, evidence = connector_capabilities.merge_runtime_results(
            self.manifests, results, run_id
        )

        self.assertEqual(
            "implemented_not_asserted",
            self.manifests["apache"]["capabilities"]["request_headers"]["state"],
        )
        self.assertEqual(source_snapshot, self.manifests)
        self.assertEqual(
            "verified",
            merged["apache"]["capabilities"]["request_headers"]["state"],
        )
        self.assertEqual(
            "implemented_not_asserted",
            merged["apache"]["capabilities"]["request_headers"]["declared_state"],
        )
        self.assertEqual(
            "supported_and_verified",
            merged["apache"]["evidence_stages"]["no_crs_baseline"]["status"],
        )
        self.assertEqual(
            "failed",
            merged["nginx"]["evidence_stages"]["no_crs_baseline"]["status"],
        )
        self.assertEqual(
            "implemented_not_asserted",
            merged["nginx"]["capabilities"]["request_headers"]["state"],
        )
        self.assertFalse(evidence["connectors"]["nginx"]["promotion_eligible"])
        self.assertEqual(
            "apache/ci-123/result.json",
            evidence["connectors"]["apache"]["result"],
        )

    def test_result_shape_rejects_a_negative_source_capability_promotion(self) -> None:
        manifest = self.manifests["traefik"]
        states = {
            name: manifest["capabilities"][name]["state"]
            for name in connector_capabilities.CAPABILITY_NAMES
        }
        result = {
            "connector": "traefik",
            "run_id": "ci-123",
            "evidence_stage": "no_crs_baseline",
            "ruleset": "no-crs-baseline",
            "status": "PASS",
            "source_failure": False,
            "cases_failed": 0,
            "cases_blocked": 0,
            "capabilities_verified": ["response_headers"],
            "capability_states": states,
        }

        errors = connector_capabilities._validated_result_shape_errors(
            "traefik", "ci-123", result, manifest
        )

        self.assertTrue(any("declares unsupported_by_host_model" in error for error in errors))

    def test_failed_or_tainted_results_never_promote_partial_cases(self) -> None:
        for update in (
            {"status": "FAIL"},
            {"status": "BLOCKED"},
            {"source_failure": True},
            {"cases_failed": 1},
            {"cases_blocked": 1},
        ):
            with self.subTest(update=update):
                results = self._results("ci-123")
                results["apache"]["result"].update(update)  # type: ignore[index]
                merged, evidence = connector_capabilities.merge_runtime_results(
                    self.manifests, results, "ci-123"
                )
                self.assertEqual(
                    "implemented_not_asserted",
                    merged["apache"]["capabilities"]["request_headers"]["state"],
                )
                self.assertFalse(evidence["connectors"]["apache"]["promotion_eligible"])

    def test_missing_evidence_is_all_or_nothing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="capability-evidence-") as temporary:
            results, errors = connector_capabilities.load_validated_runtime_results(
                self.manifests, Path(temporary), "ci-123"
            )
        self.assertEqual({}, results)
        self.assertEqual(len(connector_capabilities.CONNECTORS), len(errors))
        self.assertTrue(all("run directory is missing" in error for error in errors))

    def test_cli_renders_a_complete_validated_overlay_view(self) -> None:
        run_id = "ci-123"
        with tempfile.TemporaryDirectory(prefix="capability-evidence-") as temporary:
            root = Path(temporary)
            evidence_root = root / "evidence"
            results = self._results(run_id)
            for connector, record in results.items():
                result = record["result"]  # type: ignore[assignment]
                result.update({  # type: ignore[union-attr]
                    "connector": connector,
                    "run_id": run_id,
                    "evidence_stage": "no_crs_baseline",
                    "ruleset": "no-crs-baseline",
                })
                run_dir = evidence_root / connector / run_id
                run_dir.mkdir(parents=True)
                (run_dir / "result.json").write_text(
                    json.dumps(result), encoding="utf-8"
                )
            output = root / "report"
            with mock.patch.object(
                connector_capabilities, "_validate_evidence_run", return_value=[]
            ):
                rc = connector_capabilities.main(
                    [
                        "generate",
                        "--evidence-root",
                        str(evidence_root),
                        "--run-id",
                        run_id,
                        "--output-dir",
                        str(output),
                    ]
                )
            self.assertEqual(0, rc)
            payload = json.loads(
                (output / "connector-capabilities.generated.json").read_text(
                    encoding="utf-8"
                )
            )
        self.assertTrue(payload["runtime_promotion"])
        self.assertEqual(run_id, payload["runtime_evidence"]["run_id"])
        self.assertEqual(run_id, payload["metadata"]["verified_run_id"])
        self.assertEqual(
            "verified",
            payload["connectors"]["apache"]["capabilities"]["request_headers"]["state"],
        )

    def test_framework_validator_is_required_for_each_runtime_result(self) -> None:
        run_dir = ROOT / "evidence" / "apache" / "ci-123"
        manifest_path = ROOT / "connectors/apache/capabilities.json"
        completed = subprocess.CompletedProcess([], 0, stdout="ok", stderr="")
        with mock.patch.object(
            connector_capabilities.subprocess, "run", return_value=completed
        ) as run:
            errors = connector_capabilities._validate_evidence_run(
                "apache", run_dir, manifest_path
            )

        self.assertEqual([], errors)
        command = run.call_args.args[0]
        self.assertIn("validate", command)
        self.assertIn("--check", command)
        self.assertEqual("all", command[command.index("--check") + 1])
        self.assertIn("--connector-root", command)
        self.assertEqual(str(ROOT), command[command.index("--connector-root") + 1])

    def test_cli_requires_evidence_root_and_run_id_together(self) -> None:
        with tempfile.TemporaryDirectory(prefix="capability-output-") as temporary:
            rc = connector_capabilities.main(
                [
                    "generate",
                    "--evidence-root",
                    temporary,
                    "--output-dir",
                    temporary,
                ]
            )
        self.assertEqual(2, rc)


if __name__ == "__main__":
    unittest.main()
