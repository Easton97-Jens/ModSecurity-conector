from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


RUNNER_PATH = Path(__file__).resolve().parents[1] / "scripts" / "runtime_native_smoke.py"


def load_runner() -> object:
    specification = importlib.util.spec_from_file_location("traefik_mrts_runner", RUNNER_PATH)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class TraefikMRTSRuntimeInputsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = load_runner()

    def mrts_inputs(self, root: Path, plan_file: Path) -> object:
        return self.runner.NativeRuntimeInputs(
            runtime_root=root,
            verified_run_root=root.parent,
            engine_socket_parent=None,
            run_id=None,
            first_byte_output=None,
            binary=Path("/dev/null"),
            include_dir=Path("/dev/null"),
            library_dir=Path("/dev/null"),
            rules_file=plan_file,
            rule_ids={},
            rules_profile="mrts-load",
            module_name=self.runner.read_plugin_module(self.runner.PLUGIN_SOURCE),
            mrts_runtime=True,
            mrts_executor=plan_file,
            mrts_load_file=plan_file,
            mrts_plan=plan_file,
            mrts_plan_sha256="0" * 64,
            mrts_result=root / "mrts-runtime-result.json",
        )

    def test_load_file_rejects_crs_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            load_file = Path(temporary) / "mrts.load"
            load_file.write_text('Include "/private/owasp-crs/rules.conf"\n', encoding="utf-8")
            with self.assertRaisesRegex(self.runner.MissingDependency, "CRS material"):
                self.runner.require_no_crs_mrts_load_file(load_file)

    def test_load_file_rejects_bare_crs_path_component(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            load_file = Path(temporary) / "mrts.load"
            load_file.write_text('Include "/private/crs/rules.conf"\n', encoding="utf-8")
            with self.assertRaisesRegex(self.runner.MissingDependency, "CRS material"):
                self.runner.require_no_crs_mrts_load_file(load_file)

    def test_load_file_allows_a_private_no_crs_parent_segment(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "mrts-no-crs-master"
            root.mkdir()
            load_file = root / "mrts.load"
            load_file.write_text(
                f'Include "{root}/MRTS_002_ARGS_A-GET.conf"\n', encoding="utf-8"
            )
            self.assertEqual(self.runner.require_no_crs_mrts_load_file(load_file), load_file)

    def test_load_file_rejects_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "target.load"
            target.write_text('Include "/private/mrts/rules.conf"\n', encoding="utf-8")
            alias = root / "alias.load"
            alias.symlink_to(target)
            with self.assertRaisesRegex(self.runner.MissingDependency, "symlink"):
                self.runner.require_no_crs_mrts_load_file(alias)

    def test_executor_receives_the_validated_load_file(self) -> None:
        source = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertIn('"--load-file"', source)
        self.assertIn("MSCONNECTOR_RULES_FILE must resolve exactly to MRTS_LOAD_FILE", source)
        self.assertIn("require_no_crs_mrts_load_file", source)
        self.assertIn('"--plan-sha256"', source)
        self.assertIn('MRTS_RUNTIME_PLAN_SHA256', source)

    def test_plan_digest_requires_lowercase_sha256(self) -> None:
        self.assertEqual(self.runner.require_plan_sha256("a" * 64), "a" * 64)
        for value in ("A" * 64, "g" * 64, "0" * 63, "0" * 65):
            with self.assertRaisesRegex(self.runner.MissingDependency, "PLAN_SHA256"):
                self.runner.require_plan_sha256(value)

    def test_engine_config_uses_sealed_mrts_correlation_only_in_mrts_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rules = root / "rules.conf"
            events = root / "events.jsonl"
            normal = root / "normal.conf"
            mrts = root / "mrts.conf"
            self.runner.write_engine_config(normal, rules, events)
            self.runner.write_engine_config(mrts, rules, events, True)
            normal_text = normal.read_text(encoding="utf-8")
            mrts_text = mrts.read_text(encoding="utf-8")
            self.assertIn("transaction_id_header=x-request-id\n", normal_text)
            self.assertIn("emit_rule_match_evidence=off\n", normal_text)
            self.assertIn("transaction_id_header=x-mrts-transaction-id\n", mrts_text)
            self.assertIn("emit_rule_match_evidence=on\n", mrts_text)
            self.assertNotIn("transaction_id_header=x-request-id\n", mrts_text)

    def test_mrts_executor_uses_top_level_verified_run_root(self) -> None:
        source = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertIn("verified_run_root: Path", source)
        self.assertIn("assert_private_verified_run_root", source)
        self.assertIn('os.environ.get("VERIFIED_RUN_ROOT", "")', source)
        self.assertIn('"--runtime-root",\n        str(inputs.verified_run_root)', source)
        self.assertNotIn('"--runtime-root",\n        str(inputs.runtime_root)', source)

    def test_stage_root_must_be_below_distinct_verified_run_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            verified = root / "verified"
            stage = verified / "build" / "stages" / "traefik" / "no_crs_with_mrts" / "runtime"
            verified.mkdir(mode=0o700)
            stage.mkdir(mode=0o700, parents=True)
            self.assertEqual(
                self.runner.assert_stage_runtime_root(stage, verified), stage
            )
            with self.assertRaisesRegex(self.runner.MissingDependency, "canonical Traefik MRTS stage root"):
                self.runner.assert_stage_runtime_root(root / "foreign-stage", verified)
            with self.assertRaisesRegex(self.runner.MissingDependency, "canonical Traefik MRTS stage root"):
                self.runner.assert_stage_runtime_root(verified, verified)
            with self.assertRaisesRegex(self.runner.MissingDependency, "canonical Traefik MRTS stage root"):
                self.runner.assert_stage_runtime_root(stage / "nested", verified)

    def test_crs_host_root_must_be_private_and_below_verified_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            verified = root / "verified"
            host = verified / "runs" / "traefik" / "crs-runtime" / "host"
            verified.mkdir(mode=0o700)
            host.parent.mkdir(mode=0o700, parents=True)
            host.mkdir(mode=0o700)
            self.assertEqual(
                self.runner.assert_private_host_runtime_root(host, verified), host
            )
            outside = root / "outside-host"
            outside.mkdir(mode=0o700)
            with self.assertRaisesRegex(self.runner.MissingDependency, "below VERIFIED_RUN_ROOT"):
                self.runner.assert_private_host_runtime_root(outside, verified)

    def test_crs_host_root_rejects_non_private_existing_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            verified = root / "verified"
            host = verified / "host"
            verified.mkdir(mode=0o700)
            host.mkdir(mode=0o755, parents=True)
            host.chmod(0o755)
            with self.assertRaisesRegex(self.runner.MissingDependency, "exact-0700"):
                self.runner.assert_private_host_runtime_root(host, verified)

    def test_missing_or_symlinked_verified_run_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            verified = root / "verified"
            verified.mkdir(mode=0o700)
            alias = root / "verified-alias"
            alias.symlink_to(verified, target_is_directory=True)
            with self.assertRaisesRegex(self.runner.MissingDependency, "symlink"):
                self.runner.assert_private_verified_run_root(alias)

    def test_verified_run_root_requires_exact_private_mode_and_owner_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            verified = root / "verified"
            verified.mkdir(mode=0o755)
            verified.chmod(0o755)
            with self.assertRaisesRegex(self.runner.MissingDependency, "exact-0700"):
                self.runner.assert_private_verified_run_root(verified)
            with self.assertRaisesRegex(self.runner.MissingDependency, "outside checkout"):
                self.runner.assert_private_verified_run_root(self.runner.REPO_ROOT)

    def test_staging_allows_only_the_prevalidated_plan_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "runtime"
            root.mkdir()
            plan_file = root / "mrts-runtime-plan.json"
            plan_file.write_text("{}\n", encoding="utf-8")
            artifacts = self.runner.stage_native_runtime(self.mrts_inputs(root, plan_file))
            self.assertTrue(plan_file.is_file())
            self.assertTrue(artifacts.logs_dir.is_dir())

    def test_staging_rejects_any_content_beside_the_prevalidated_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "runtime"
            root.mkdir()
            plan_file = root / "mrts-runtime-plan.json"
            plan_file.write_text("{}\n", encoding="utf-8")
            (root / "foreign.txt").write_text("unexpected\n", encoding="utf-8")
            inputs = self.mrts_inputs(root, plan_file)
            with self.assertRaisesRegex(self.runner.MissingDependency, "only its sealed plan"):
                self.runner.stage_native_runtime(inputs)

    def test_mrts_mode_starts_the_host_before_running_the_executor(self) -> None:
        inputs = object()
        artifacts = object()
        setup = object()
        processes = object()
        observation = object()
        calls: list[str] = []

        with (
            mock.patch.object(
                self.runner,
                "run_native_requests",
                side_effect=lambda *_args: calls.append("start") or None,
            ),
            mock.patch.object(
                self.runner,
                "run_mrts_runtime_executor",
                side_effect=lambda *_args: calls.append("executor"),
            ),
            mock.patch.object(
                self.runner,
                "observe_live_mrts_host",
                side_effect=lambda *_args: calls.append("observe") or observation,
            ),
            mock.patch.object(
                self.runner,
                "stop_native_processes",
                side_effect=lambda *_args: calls.append("stop") or (True, True),
            ),
            mock.patch.object(
                self.runner,
                "write_mrts_host_summary",
                side_effect=lambda *_args: calls.append("summary"),
            ),
        ):
            self.runner.execute_mrts_mode(inputs, artifacts, setup, processes)

        self.assertEqual(calls, ["start", "executor", "observe", "stop", "summary"])

    def test_mrts_mode_rejects_unexpected_native_request_results(self) -> None:
        with (
            mock.patch.object(self.runner, "run_native_requests", return_value=object()),
            mock.patch.object(self.runner, "run_mrts_runtime_executor") as executor,
            self.assertRaisesRegex(RuntimeError, "unexpectedly produced native request results"),
        ):
            self.runner.execute_mrts_mode(object(), object(), object(), object())
        executor.assert_not_called()


if __name__ == "__main__":
    unittest.main()
