"""Focused contract tests for the closed no-CRS/with-MRTS Parent route."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TARGET = load("mrts_target", "ci/runtime/lifecycle/run-no-crs-with-mrts-target.py")
EXECUTOR = load("mrts_executor", "ci/runtime/lifecycle/execute-no-crs-mrts-cases.py")


class NoCrsWithMrtsTargetContractTests(unittest.TestCase):
    def test_profile_is_closed_to_three_connectors(self):
        self.assertEqual(TARGET.CONNECTORS, {"envoy", "traefik", "lighttpd"})
        self.assertEqual(TARGET.PROFILE, "no-crs/with-mrts")

    def test_runtime_route_requires_explicit_checkout_roots_and_stage(self):
        source = (ROOT / "ci" / "runtime" / "lifecycle" / "run-no-crs-with-mrts-target.py").read_text(encoding="utf-8")
        self.assertIn('parser.add_argument("--parent-root", required=True)', source)
        self.assertIn('parser.add_argument("--framework-root", required=True)', source)
        self.assertIn('stop("--execute-stage is mandatory', source)
        self.assertIn('"no_crs_with_mrts"', source)

    def test_executor_binds_localhost_and_provenance(self):
        source = (ROOT / "ci" / "runtime" / "lifecycle" / "execute-no-crs-mrts-cases.py").read_text(encoding="utf-8")
        self.assertIn('if args.host != "127.0.0.1":', source)
        self.assertIn('item.get("transaction_id") != correlation_id', source)
        self.assertIn('item.get("connector") != connector', source)
        self.assertIn('item.get("uri") != uri', source)
        self.assertIn("executor digest mismatch", source)
        self.assertIn("MRTS case digest mismatch", source)
        self.assertIn('parser.add_argument("--load-file", required=True)', source)

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaises(SystemExit):
            EXECUTOR.reject_duplicates([("a", 1), ("a", 2)])

    def test_generated_plan_has_control_detection_and_bypass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "case.yaml"
            source.write_text(
                """name: mrts_case\nmetadata:\n  upstream_file: tools/MRTS/generated/tests/regression/tests/MRTS_002_ARGS_A-GET.yaml\n  phase: 1\nportable: true\nrequest:\n  method: GET\n  path: /?foo=attack\nexpect:\n  rule_id: 100000\n""",
                encoding="utf-8",
            )
            # The framework parser is intentionally used by the runner; this
            # test only verifies the executor's required case contract.
            plan = {"profile": "no-crs/with-mrts", "connector": "envoy", "cases": [
                {"id": "control", "kind": "control", "uri": "/?control=1", "expect_ids": []},
                {"id": "detect", "kind": "detection", "uri": "/?foo=attack", "expect_ids": ["100000"]},
                {"id": "bypass", "kind": "bypass", "uri": "/?foo=benign", "expect_ids": []},
            ]}
            self.assertEqual({case["kind"] for case in plan["cases"]}, {"control", "detection", "bypass"})
            json.loads(json.dumps(plan), object_pairs_hook=EXECUTOR.reject_duplicates)

    def test_mrts_load_permits_generated_rules_under_a_private_no_crs_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "mrts-no-crs"
            rules = runtime / "build" / "mrts" / "upstream-config-tests" / "rules"
            rules.mkdir(parents=True)
            generated = rules / "MRTS_002_ARGS_A-GET.conf"
            generated.write_text('SecRule ARGS:foo "@streq attack" "id:100000,phase:1,pass"\n', encoding="utf-8")
            load = runtime / "mrts.load"
            load.write_text(f'Include "{generated}"\n', encoding="utf-8")
            baseline = root / "baseline.conf"
            baseline.write_text("SecRuleEngine DetectionOnly\n", encoding="utf-8")
            canonical = root / "pinned-mrts" / "generated" / "rules"
            canonical.mkdir(parents=True)
            (canonical / generated.name).write_bytes(generated.read_bytes())
            self.assertEqual(
                TARGET.validate_mrts_load_file(load, rules, baseline, canonical.parents[1], runtime),
                {generated.name: TARGET.hashlib.sha256(generated.read_bytes()).hexdigest()},
            )

    def test_mrts_load_rejects_a_crs_named_or_outside_include(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "runtime"
            rules = runtime / "build" / "mrts" / "upstream-config-tests" / "rules"
            rules.mkdir(parents=True)
            foreign = rules / "MRTS_002_ARGS_A-GET.conf"
            foreign.write_text('SecRule ARGS:foo "@streq attack" "id:949110,phase:1,pass"\n', encoding="utf-8")
            load = runtime / "mrts.load"
            load.write_text(f'Include "{foreign}"\n', encoding="utf-8")
            baseline = root / "baseline.conf"
            baseline.write_text("SecRuleEngine DetectionOnly\n", encoding="utf-8")
            canonical = root / "pinned-mrts" / "generated" / "rules"
            canonical.mkdir(parents=True)
            (canonical / foreign.name).write_text('SecRule ARGS:foo "@streq attack" "id:100000,phase:1,pass"\n', encoding="utf-8")
            with self.assertRaises(SystemExit):
                TARGET.validate_mrts_load_file(load, rules, baseline, canonical.parents[1], runtime)

    def test_mrts_load_rejects_a_symlinked_private_rules_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "runtime"
            external = root / "external-rules"
            external.mkdir(parents=True)
            generated = external / "MRTS_002_ARGS_A-GET.conf"
            generated.write_text('SecRule ARGS:foo "@streq attack" "id:100000,phase:1,pass"\n', encoding="utf-8")
            rules = runtime / "build" / "mrts" / "upstream-config-tests" / "rules"
            rules.parent.mkdir(parents=True)
            rules.symlink_to(external, target_is_directory=True)
            load = runtime / "mrts.load"
            load.write_text(f'Include "{rules / generated.name}"\n', encoding="utf-8")
            baseline = root / "baseline.conf"
            baseline.write_text("SecRuleEngine DetectionOnly\n", encoding="utf-8")
            canonical = root / "pinned-mrts" / "generated" / "rules"
            canonical.mkdir(parents=True)
            (canonical / generated.name).write_bytes(generated.read_bytes())
            with self.assertRaises(SystemExit):
                TARGET.validate_mrts_load_file(load, rules, baseline, canonical.parents[1], runtime)


if __name__ == "__main__":
    unittest.main()
