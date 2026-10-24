"""Adversarial contract tests; synthetic receipts are never runtime evidence."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "connectors/lighttpd/harness/run_patched_qualification.py"
SPEC = importlib.util.spec_from_file_location("patched_qualification", PATH)
qualification = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = qualification
SPEC.loader.exec_module(qualification)


def receipt(plan):
    identity = [100 + plan.index, 1000 + plan.index]
    cases = {}
    for number, (name, expected) in enumerate(qualification.CASES.items(), 1):
        cases[name] = dict(zip(("status", "action", "backend_receipts"), expected))
        cases[name].update(host_transaction_id=f"lighttpd-{identity[0]}-{number}", upstream_connections=0,
                           upstream_headers=0, predecision_upstream_connections=0)
    cases["p4-safe"].update(eos_count=1, first_byte_before_eos=True)
    sample = {"host_identity": identity, "rss_kib": 1024, "fds": 4, "sockets": 2}
    recovery = {"observed": True, "bounded": True, "recovery_status": 200, "recovery_host_identity": identity}
    return {
        "run_id": plan.run_id, "index": plan.index, "profile": qualification.PROFILE,
        "evidence_origin": "real_host", "source_sha256": plan.source_sha256,
        "pins": {name: pin.sha256 for name, pin in plan.pins.items()}, "root_identity": plan.root_identity,
        "namespace": {"launcher": str(plan.namespace_launcher), "host_uid": 33, "host_euid": 33,
                      **{key: True for key in ("user", "mount", "pid", "private_propagation", "tmpfs_noexec",
                                              "tmpfs_nosuid", "tmpfs_nodev", "no_new_privs", "capabilities_zero",
                                              "further_userns_disabled")}},
        "engine_mode": "On", "host_identity": identity, "cases": cases,
        "limitations": ["HTTP/1.1 identity mod_proxy entities", "P4 Safe log_only after commit"],
        "extensions": {"client_abort": copy.deepcopy(recovery), "dependency_failure": copy.deepcopy(recovery),
                       "keepalive": {"statuses": [200, 403, 200, 403, 200], "connection_count": 1, "distinct_transactions": 5},
                       "overlap": {"clients": 4, "peak_active": 4, "intervals": [[1, 5], [2, 5], [3, 5], [4, 5]]},
                       "resources": {name: copy.deepcopy(sample) for name in ("before", "peak", "after")},
                       "restart": {"controlled_stop": True, "old_process_absent": True,
                                   "new_allow_status": 200, "new_host_identity": [10000 + plan.index, 20000 + plan.index]}},
        "cleanup": {"owned_processes_absent": True, "owned_listeners_absent": True,
                    "namespace_reaped": True, "unexpected_artifacts": []},
    }


class SyntheticExecutor:
    """Unit-test injection only, never a trusted runtime implementation."""
    def __init__(self, mutation=None, verification=True):
        self.plans = []
        self.mutation = mutation
        self.verification = verification

    def preflight(self, pins, source_sha256):
        pass

    def run_start(self, plan):
        self.plans.append(plan)
        value = receipt(plan)
        if self.mutation:
            self.mutation(plan, value)
        return value

    def verify(self, plan, value):
        return self.verification


class QualificationTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="patched-contract-", dir="/var/tmp/codex/ModSecurity-conector")
        self.addCleanup(self.temporary.cleanup)
        self.parent = Path(self.temporary.name)
        self.pins = {}
        for role in qualification.ROLES:
            path = self.parent / role
            path.write_bytes(role.encode())
            path.chmod(0o600)
            self.pins[role] = qualification.Pin(path, hashlib.sha256(role.encode()).hexdigest())
        self.source = "a" * 64

    def run_campaign(self, executor=None, caller=lambda: (33, 33)):
        return qualification.qualify(self.parent, self.pins, self.source, executor, caller=caller)

    def test_three_fresh_starts_are_diagnostic_only(self):
        executor = SyntheticExecutor()
        value = self.run_campaign(executor)
        self.assertEqual(len(executor.plans), 3)
        self.assertEqual(len({x.root_identity for x in executor.plans}), 3)
        self.assertFalse(value["readiness_awarded"])
        self.assertFalse(value["catalog_promotion"])
        self.assertEqual(value["result"], "diagnostic_pass")
        for plan in executor.plans:
            self.assertEqual(plan.root.stat().st_mode & 0o777, 0o700)
            self.assertEqual((plan.root / "qualification.json").stat().st_mode & 0o777, 0o600)
            self.assertEqual(plan.phase2_runner.name, "run_phase2_pre_upstream_gate.py")
            self.assertEqual(plan.lifecycle_runner.name, "run_patched_full_lifecycle.sh")

    def test_missing_executor_blocks_without_outputs(self):
        before = set(self.parent.iterdir())
        with self.assertRaises(qualification.Blocked):
            self.run_campaign()
        self.assertEqual(set(self.parent.iterdir()), before)

    def test_root_and_setid_are_blocked_before_preflight(self):
        for identity in ((0, 0), (33, 0), (33, 34)):
            executor = SyntheticExecutor()
            with self.assertRaises(qualification.Blocked):
                self.run_campaign(executor, caller=lambda: identity)
            self.assertFalse(executor.plans)

    def test_namespace_preflight_block_never_starts(self):
        class Unavailable(SyntheticExecutor):
            def preflight(self, pins, source):
                raise qualification.Blocked("unshare EPERM")
        executor = Unavailable()
        with self.assertRaises(qualification.Blocked):
            self.run_campaign(executor)
        self.assertFalse(executor.plans)

    def test_independent_verification_rejection_is_a_failure(self):
        for result in (False, None, 1, "PASS"):
            with self.subTest(result=result), self.assertRaises(qualification.Failure):
                self.run_campaign(SyntheticExecutor(verification=result))

    def test_independent_verifier_cannot_mutate_the_published_snapshot(self):
        class MutatingVerifier(SyntheticExecutor):
            def verify(self, plan, value):
                value["cases"]["p1"]["status"] = 200
                return True

        with self.assertRaisesRegex(qualification.Failure, "mutated the start receipt"):
            self.run_campaign(MutatingVerifier())

    def assert_rejected(self, mutate):
        with self.assertRaises(qualification.Failure):
            self.run_campaign(SyntheticExecutor(mutate))

    def test_every_namespace_enforcement_flag_is_required(self):
        flags = receipt(qualification.StartPlan("x", 1, self.parent, "1:2", self.source, self.pins))["namespace"]
        for flag in set(flags) - {"launcher", "host_uid", "host_euid"}:
            with self.subTest(flag=flag):
                self.assert_rejected(lambda plan, value: value["namespace"].update({flag: False}))

    def test_bwrap_only_or_root_namespace_receipt_rejected(self):
        self.assert_rejected(lambda p, v: v["namespace"].update(launcher="/usr/bin/bwrap"))
        self.assert_rejected(lambda p, v: v["namespace"].update(host_uid=0, host_euid=0))

    def test_identity_drift_stale_stock_and_sibling_rejected(self):
        mutations = [lambda p, v: v.update(source_sha256="b" * 64),
                     lambda p, v: v["pins"].update(module="b" * 64),
                     lambda p, v: v.update(root_identity="1:999"),
                     lambda p, v: v.update(run_id="stale"), lambda p, v: v.update(index=99),
                     lambda p, v: v.update(profile="lighttpd-stock"),
                     lambda p, v: v.update(evidence_origin="fixture"),
                     lambda p, v: v.update(engine_mode="DetectionOnly")]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                self.assert_rejected(mutate)

    def test_fixture_only_success_rejected(self):
        self.assert_rejected(lambda p, v: v.update(extensions={}))
        self.assert_rejected(lambda p, v: v["cases"].pop("p2-delayed"))

    def test_predecision_leak_rejected(self):
        self.assert_rejected(lambda p, v: v["cases"]["p2-delayed"].update(upstream_connections=1))
        self.assert_rejected(lambda p, v: v["cases"]["request-boundary"].update(predecision_upstream_connections=1))

    def test_four_clients_without_real_overlap_rejected(self):
        self.assert_rejected(lambda p, v: v["extensions"]["overlap"].update(peak_active=3))
        self.assert_rejected(lambda p, v: v["extensions"]["overlap"].update(intervals=[[1, 2], [2, 3], [3, 4], [4, 5]]))
        self.assert_rejected(lambda p, v: v["extensions"]["overlap"].update(intervals=[[1, float("nan")]] * 4))

    def test_same_host_recovery_keepalive_restart_resource_requirements(self):
        self.assert_rejected(lambda p, v: v["extensions"]["client_abort"].update(recovery_host_identity=[999, 999]))
        self.assert_rejected(lambda p, v: v["extensions"]["dependency_failure"].update(bounded=False))
        self.assert_rejected(lambda p, v: v["extensions"]["keepalive"].update(connection_count=5))
        self.assert_rejected(lambda p, v: v["extensions"]["resources"]["after"].update(fds=0))
        self.assert_rejected(lambda p, v: v["extensions"]["restart"].update(old_process_absent=False))

    def test_cleanup_missing_or_unexpected_artifacts_rejected(self):
        for key in ("owned_processes_absent", "owned_listeners_absent", "namespace_reaped"):
            self.assert_rejected(lambda p, v: v["cleanup"].update({key: False}))
        self.assert_rejected(lambda p, v: v["cleanup"].update(unexpected_artifacts=["other-run.json"]))

    def test_same_start_identity_reused_rejected(self):
        self.assert_rejected(lambda p, v: v.update(host_identity=[101, 1001]) if p.index > 1 else None)

    def test_hash_drift_replacement_and_symlink_inputs_rejected(self):
        original = self.pins["module"]
        original.path.write_bytes(b"wrong")
        with self.assertRaises(qualification.Failure):
            self.run_campaign(SyntheticExecutor())
        original.path.unlink()
        original.path.symlink_to(self.pins["host"].path)
        with self.assertRaises(qualification.Failure):
            self.run_campaign(SyntheticExecutor())

    def test_input_changes_during_start_rejected(self):
        def replace(plan, value):
            path = self.pins["module"].path
            path.unlink()
            path.write_bytes(b"module")
            path.chmod(0o600)
        with self.assertRaises(qualification.Failure):
            self.run_campaign(SyntheticExecutor(replace))

    def test_output_replacement_and_stale_qualification_artifact_rejected(self):
        def stale(plan, value):
            (plan.root / "qualification.json").write_text("stale")
        with self.assertRaises((qualification.Failure, ValueError)):
            self.run_campaign(SyntheticExecutor(stale))


if __name__ == "__main__":
    unittest.main()
