"""Adversarial evidence/lifecycle tests; no host or artifact substitution."""
import hashlib
from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from connectors.lighttpd.harness import run_stock_sidecar_qualification as qualification
from connectors.lighttpd.tests.test_stock_sidecar_contract import _strict_stock_event


class EvidenceTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR"))
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.receipt, self.events, self.backend = [self.root / name for name in ("receipt", "events", "backend")]
        self.binding = "a" * 64
        self.token = "qualification-transaction-1"
        self.ledger = qualification.Evidence(self.receipt, self.events, self.backend, self.binding)

    def write(self, path, data):
        path.write_bytes(data)
        path.chmod(0o600)

    def snapshot(self, case, token=None):
        result = {"schema_version": 1, "connector": "lighttpd", "connector_profile": "lighttpd-stock-sidecar",
                  "integration_mode": "traffic-owning-sidecar", "transport_version": "HTTP/1.1",
                  "phase_observation": "runtime_snapshot_after_cleanup",
                  "observed_phase_sequence": list(case.expected_phase_sequence),
                  "transaction_id_sha256": hashlib.sha256((token or self.token).encode()).hexdigest(),
                  "receipt_binding_sha256": hashlib.sha256(self.binding.encode()).hexdigest(),
                  "request_body_bytes": qualification.base.expected_snapshot_request_bytes(case),
                  "response_body_bytes": len(case.expected_body), "engine_decision": case.expected_engine_decision,
                  "actual_host_action": "allow", "visible_http_status": case.expected_status,
                  "original_http_status": case.expected_status, "response_committed": case.expected_response_committed,
                  "cleanup_status": "complete", "cleanup_complete": True,
                  "payloads_persisted": False, "opaque_handles_persisted": False}
        if case.expected_engine_decision != "allow":
            result.update(schema_version=2, receipt_kind="non_allow", contract_action=case.expected_contract_action,
                          error_class=case.expected_error_class, mode=case.phase4_mode,
                          request_body_truncated=False, response_body_truncated=False,
                          last_completed_phase=case.expected_phase_sequence[-1],
                          response_headers_processed=False, response_headers_sent=False, response_body_finished=False,
                          created_at_ms=1, completed_at_ms=2, cleanup_at_ms=3)
            del result["actual_host_action"]
            del result["visible_http_status"]
        return result

    def publish(self, case, *, token=None, mutate=None):
        value = self.snapshot(case, token)
        if mutate:
            value.update(mutate)
        self.write(self.receipt, json.dumps(value).encode())
        if case.expected_backend_requests:
            self.write(self.backend, (token or self.token).encode() + b"\n")

    def pair(self, case, token=None):
        phase = qualification.base._EVENT_CONTRACT_PHASE_NAMES[case.expected_phase_sequence[-1]]
        engine = _strict_stock_event(qualification.base, message_id=case.expected_engine_event,
                                     transaction_id=token or self.token, sequence=1, previous_hash=0,
                                     phase=phase, actual_action="deny", requested_action="deny", event_name="rule_block")
        host = _strict_stock_event(qualification.base, message_id=case.expected_host_action_event,
                                   transaction_id=token or self.token, sequence=2, previous_hash=engine["event_hash"],
                                   phase=phase, actual_action="deny", requested_action="deny",
                                   transport_result="http_status", visible_http_status=case.expected_status,
                                   rule_id=case.expected_rule_id)
        engine["rule_id"] = case.expected_rule_id
        engine["event_hash"] = qualification.base.event_integrity_hash(engine, 0)
        host["previous_event_hash"] = engine["event_hash"]
        host["event_hash"] = qualification.base.event_integrity_hash(host, engine["event_hash"])
        self.write(self.events, b"".join(json.dumps(value).encode() + b"\n" for value in (engine, host)))
        return engine, host

    def test_allow_receipt_consumed_only_after_validation(self):
        case = qualification.CASES["allow_full"]
        self.ledger.ready()
        self.publish(case)
        result = self.ledger.finish(case, self.token)
        self.assertEqual(result["backend_requests"], 1)
        self.assertFalse(self.receipt.exists())

    def test_p1_p2_have_zero_backend_and_exact_engine_host_pair(self):
        for name in ("p1_deny", "p2_deny"):
            with self.subTest(name=name):
                self.ledger = qualification.Evidence(self.receipt, self.events, self.backend, self.binding)
                case = qualification.CASES[name]
                self.publish(case)
                self.pair(case)
                result = self.ledger.finish(case, self.token)
                self.assertEqual(result["events_added"], 2)
                self.assertEqual(result["backend_requests"], 0)

    def test_stale_receipt_prevents_request(self):
        self.publish(qualification.CASES["allow_full"])
        with self.assertRaisesRegex(RuntimeError, "stale"):
            self.ledger.ready()

    def test_missing_receipt_fails_without_consumption(self):
        with mock.patch.object(qualification.time, "monotonic", side_effect=(0, 4)):
            with self.assertRaisesRegex(RuntimeError, "missing"):
                self.ledger.finish(qualification.CASES["allow_full"], self.token)

    def test_duplicate_transaction_receipt_is_retained_and_rejected(self):
        case = qualification.CASES["p1_deny"]
        self.publish(case)
        self.pair(case)
        self.ledger.finish(case, self.token)
        self.publish(case)
        with self.assertRaisesRegex(RuntimeError, "duplicate or stale"):
            self.ledger.finish(case, self.token)
        self.assertTrue(self.receipt.exists())

    def test_wrong_transaction_and_binding_fail(self):
        case = qualification.CASES["allow_full"]
        for mutation, expected in (({"transaction_id_sha256": "0" * 64}, "correlated"),
                                   ({"receipt_binding_sha256": "0" * 64}, "bound"),
                                   ({"cleanup_complete": False}, "cleanup")):
            with self.subTest(mutation=mutation):
                self.publish(case, mutate=mutation)
                with self.assertRaisesRegex(RuntimeError, expected):
                    self.ledger.finish(case, self.token)

    def test_unrecognized_receipt_field_cannot_persist_payload(self):
        case = qualification.CASES["allow_full"]
        self.publish(case, mutate={"secret_payload": "raw bytes"})
        with self.assertRaisesRegex(RuntimeError, "unexpected fields"):
            self.ledger.finish(case, self.token)

    def test_abort_requires_genuine_correlated_cancel_and_host_outcome(self):
        case = replace(qualification.CASES["p1_deny"], name="client_abort",
                       request=qualification.base.http_request("POST", "/health.txt", b"stock-abort-marker"),
                       expected_status=502, expected_engine_decision="client_cancel",
                       expected_contract_action="abort_connection", expected_error_class="client_cancel")
        for mutation in (None, {"cancelled": False}, {"client_disconnected": False}, {"eos_seen": True},
                         {"body_bytes_seen": 0}, {"message_id": "MSCONN_EVENT_CONNECTOR_ERROR"}):
            with self.subTest(mutation=mutation):
                self.ledger = qualification.Evidence(self.receipt, self.events, self.backend, self.binding)
                self.publish(case)
                engine = _strict_stock_event(qualification.base, message_id="MSCONN_EVENT_CLIENT_CANCEL",
                                             transaction_id=self.token, sequence=1, previous_hash=0,
                                             phase="request_body", actual_action="abort_connection",
                                             requested_action="abort_connection")
                engine.update(cancelled=True, client_disconnected=True, eos_seen=False, body_bytes_seen=18)
                if mutation:
                    engine.update(mutation)
                engine["event_hash"] = qualification.base.event_integrity_hash(engine, 0)
                host = _strict_stock_event(qualification.base, message_id="MSCONN_EVENT_CONNECTOR_ERROR",
                                           transaction_id=self.token, sequence=2, previous_hash=engine["event_hash"],
                                           phase="request_body", actual_action="deny", requested_action="error",
                                           transport_result="http_status", visible_http_status=502)
                self.write(self.events, b"".join(json.dumps(record).encode() + b"\n" for record in (engine, host)))
                if mutation:
                    with self.assertRaisesRegex(RuntimeError, "outcome is not exact"):
                        self.ledger.finish(case, self.token, abort=True)
                else:
                    self.assertEqual(self.ledger.finish(case, self.token, abort=True)["backend_requests"], 0)

    def test_log_and_request_bounds_fail(self):
        self.write(self.receipt, b"a" * 101)
        with self.assertRaisesRegex(RuntimeError, "bounded"):
            qualification.bounded_read(self.receipt, 100)
        self.receipt.unlink()
        self.ledger.requests = qualification.MAX_REQUESTS
        with self.assertRaisesRegex(RuntimeError, "request bound"):
            self.ledger.ready()

    def test_missing_and_duplicate_common_events_fail(self):
        case = qualification.CASES["p1_deny"]
        self.publish(case)
        with self.assertRaisesRegex(RuntimeError, "missing or stale"):
            self.ledger.finish(case, self.token)
        pair = self.pair(case)
        data = self.events.read_bytes()
        self.write(self.events, data + json.dumps(pair[1]).encode() + b"\n")
        with self.assertRaisesRegex(RuntimeError, "sequence"):
            self.ledger.finish(case, self.token)

    def test_event_hash_and_wrong_transaction_fail(self):
        case = qualification.CASES["p1_deny"]
        self.publish(case)
        pair = self.pair(case, "other-transaction")
        with self.assertRaisesRegex(RuntimeError, "correlated"):
            self.ledger.finish(case, self.token)
        pair[1]["event_hash"] = 0
        self.write(self.events, b"".join(json.dumps(value).encode() + b"\n" for value in pair))
        with self.assertRaisesRegex(RuntimeError, "hash"):
            self.ledger.finish(case, self.token)

    def test_extra_or_uncorrelated_backend_rejected(self):
        case = qualification.CASES["allow_full"]
        for data in (b"unrelated\n", self.token.encode() + b"\nextra\n"):
            with self.subTest(data=data):
                self.publish(case)
                self.write(self.backend, data)
                with self.assertRaisesRegex(RuntimeError, "uncorrelated"):
                    self.ledger.finish(case, self.token)

    def test_block_with_backend_receipt_fails(self):
        case = qualification.CASES["p1_deny"]
        self.publish(case)
        self.pair(case)
        self.write(self.backend, self.token.encode() + b"\n")
        with self.assertRaisesRegex(RuntimeError, "backend"):
            self.ledger.finish(case, self.token)

    def test_append_only_full_chain_survives_allow_delta(self):
        case = qualification.CASES["p1_deny"]
        self.publish(case)
        self.pair(case)
        self.ledger.finish(case, self.token)
        self.ledger.ready()
        case = qualification.CASES["allow_full"]
        self.publish(case, token="new-transaction")
        self.assertEqual(self.ledger.finish(case, "new-transaction")["events_added"], 0)

    def test_replaced_or_truncated_event_log_fails(self):
        case = qualification.CASES["p1_deny"]
        self.publish(case)
        self.pair(case)
        self.ledger.finish(case, self.token)
        original = self.events.read_bytes()
        self.write(self.events, b"")
        with self.assertRaisesRegex(RuntimeError, "truncated"):
            self.ledger.ready()
        self.events.unlink()
        self.write(self.events, original)
        # Pin drift is explicit; inode reuse cannot invalidate this test.
        self.ledger.event_inode = (0, 0)
        with self.assertRaisesRegex(RuntimeError, "replaced"):
            self.ledger.ready()

    def test_unattributed_backend_before_request_fails(self):
        self.write(self.backend, b"stale\n")
        with self.assertRaisesRegex(RuntimeError, "unattributed"):
            self.ledger.ready()

    def test_duplicate_json_payload_and_unsafe_files_fail(self):
        with self.assertRaises(ValueError):
            qualification.decode(b'{"key":1,"key":2}')
        self.write(self.receipt, b"{}")
        self.receipt.chmod(0o644)
        with self.assertRaisesRegex(RuntimeError, "private"):
            qualification.bounded_read(self.receipt, 100)
        self.receipt.chmod(0o600)
        link = self.root / "link"
        link.symlink_to(self.receipt)
        with self.assertRaises(OSError):
            qualification.bounded_read(link, 100)
        os.link(self.receipt, self.root / "hardlink")
        with self.assertRaisesRegex(RuntimeError, "private"):
            qualification.bounded_read(self.receipt, 100)


class LifecycleTest(unittest.TestCase):
    def starts(self):
        return [{"identity": {"pid": number, "start_ticks": number}, "controlled_stop_reaped": True,
                 "backend_identity": {"pid": number + 10, "start_ticks": number + 10},
                 "backend_port": 10000 + number, "sidecar_port": 20000 + number,
                 "backend_controlled_stop_reaped": True, "backend_final_log_verified": True,
                 "elapsed_seconds": 2, "probes": [{"case": name} for name in ("allow_full", "p1_deny", "p2_deny")],
                 "resources_before": {"fd_count": 4, "rss_kib": 100},
                 "resources_after": {"fd_count": 4, "rss_kib": 100, "accepted_peer_ports": []},
                 "overlap_verified": True, "keepalive_verified": True, "abort_recovery_verified": True}
                for number in range(1, 4)]

    def test_three_distinct_starts_and_lifecycle_evidence_required(self):
        qualification.validate_starts(self.starts())
        for mutate in (lambda items: items.pop(),
                       lambda items: items[1].update(identity=items[0]["identity"]),
                       lambda items: items[1].update(backend_identity=items[0]["backend_identity"]),
                       lambda items: items[1].update(backend_port=items[0]["backend_port"]),
                       lambda items: items[1].update(backend_controlled_stop_reaped=False),
                       lambda items: items[1].update(backend_final_log_verified=False),
                       lambda items: items[0].update(overlap_verified=False),
                       lambda items: items[0].update(abort_recovery_verified=False),
                       lambda items: items[0].update(keepalive_verified=False),
                       lambda items: items[2].update(probes=[]),
                       lambda items: items[2].update(controlled_stop_reaped=False),
                       lambda items: items[2].update(elapsed_seconds=61),
                       lambda items: items[2]["resources_after"].update(fd_count=5),
                       lambda items: items[2]["resources_after"].update(rss_kib=10000),
                       lambda items: items[2]["resources_after"].update(accepted_peer_ports=[123])):
            items = self.starts()
            mutate(items)
            with self.assertRaises(RuntimeError):
                qualification.validate_starts(items)

    def test_final_backend_log_must_match_consumed_prefix_and_identity(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as temporary:
            path = Path(temporary) / "backend.log"
            path.write_bytes(b"request-one\n")
            path.chmod(0o600)
            data, inode = qualification.bounded_read(path, 100)
            evidence = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                        "device": inode[0], "inode": inode[1]}
            qualification.verify_final_backend_log(path, evidence)
            path.write_bytes(data + b"late-dispatch\n")
            with self.assertRaisesRegex(RuntimeError, "final backend log"):
                qualification.verify_final_backend_log(path, evidence)
            path.write_bytes(data)
            evidence["inode"] = -1
            with self.assertRaisesRegex(RuntimeError, "final backend log"):
                qualification.verify_final_backend_log(path, evidence)

    def test_overlap_requires_four_matching_process_owned_sockets(self):
        clients = [mock.Mock() for _ in range(4)]
        for number, client in enumerate(clients):
            client.getsockname.return_value = ("127.0.0.1", 100 + number)
        qualification.verify_overlap({"accepted_peer_ports": list(range(100, 104))}, clients)
        with self.assertRaisesRegex(RuntimeError, "overlap"):
            qualification.verify_overlap({"accepted_peer_ports": list(range(100, 103))}, clients)
        with self.assertRaisesRegex(RuntimeError, "overlap"):
            qualification.verify_overlap({"accepted_peer_ports": list(range(100, 104))}, clients[:3])

    def test_process_identity_drift_fails_before_resource_read(self):
        pin = qualification.Identity(100, 200, "a" * 64)
        with mock.patch.object(qualification, "identity", return_value=qualification.Identity(100, 201, "a" * 64)):
            with self.assertRaisesRegex(RuntimeError, "identity drifted"):
                qualification.resources(pin, 12345)

    def test_controlled_stop_cannot_pass_hard_kill_or_live_listener(self):
        process = mock.Mock(pid=999999999)
        process.poll.return_value = None
        process.wait.side_effect = [subprocess.TimeoutExpired("sidecar", 5), -9]
        with self.assertRaisesRegex(RuntimeError, "hard kill"):
            qualification.controlled_stop(process, 12345)
        process.kill.assert_called_once()
        process.wait.side_effect = None
        process.wait.return_value = -15
        with mock.patch.object(qualification.socket, "socket") as sock:
            sock.return_value.__enter__.return_value.connect_ex.return_value = 0
            with self.assertRaisesRegex(RuntimeError, "listener survived"):
                qualification.controlled_stop(process, 12345)


class ResponseGrammarTest(unittest.TestCase):
    def parse(self, headers, *, keepalive=False, status=b"HTTP/1.1 200 OK"):
        body = qualification.CASES["allow_full"].expected_body
        wire = status + b"\r\n" + headers + b"\r\n" + body
        client = mock.Mock()
        client.recv.side_effect = [bytes([byte]) for byte in wire[:wire.index(b"\r\n\r\n") + 4]] + [body, b""]
        qualification.response(client, qualification.CASES["allow_full"], keepalive)

    def test_canonical_framing_passes(self):
        self.parse(b"Content-Length: 20\r\nConnection: close\r\n")
        self.parse(b"Content-Length: 20\r\nConnection: keep-alive\r\n", keepalive=True)

    def test_ambiguous_and_malformed_header_lines_fail(self):
        canonical = b"Content-Length: 20\r\nConnection: close\r\n"
        for extra in (b"Connection: keep-alive\r\n", b"Connection: close\r\n",
                      b"Transfer-Encoding: chunked\r\n", b"Transfer-Encoding : chunked\r\n",
                      b" Transfer-Encoding: chunked\r\n", b"\tContent-Length: 20\r\n",
                      b"X-Test : value\r\n", b"X Test: value\r\n", b"X-\x00Test: value\r\n",
                      b"X-Test:\tvalue\r\n", b"X-Test: value\r\n folded\r\n",
                      b"Content-Length: 020\r\n", b"Content-Length: +20\r\n",
                      b"Content-Length: 20, 20\r\n", b"X-Test: value\x7f\r\n"):
            with self.subTest(extra=extra):
                with self.assertRaises(RuntimeError):
                    self.parse(canonical + extra)
        for replacement in (b"Content-Length : 20", b"Content-Length: 020", b"Content-Length: +20",
                            b"Content-Length:  20", b"Content-Length: 20 "):
            with self.subTest(replacement=replacement):
                with self.assertRaises(RuntimeError):
                    self.parse(replacement + b"\r\nConnection: close\r\n")


class ClassificationTest(unittest.TestCase):
    def test_cli_preflight_runtime_and_cleanup_exit_statuses(self):
        with mock.patch.object(qualification, "preflight") as preflight, \
                mock.patch.object(qualification, "run_campaign") as campaign, \
                mock.patch("sys.stderr"):
            self.assertEqual(qualification.main(["unexpected"]), 2)
            preflight.assert_not_called()
            preflight.side_effect = RuntimeError("operator attestation missing")
            self.assertEqual(qualification.main([]), 77)
            campaign.assert_not_called()
            preflight.side_effect = TypeError("preflight implementation error")
            self.assertEqual(qualification.main([]), 1)
            campaign.assert_not_called()
            preflight.side_effect = None
            for error in (RuntimeError("product failed"), OSError("evidence failed"),
                          ExceptionGroup("primary and cleanup", [RuntimeError("primary"), RuntimeError("cleanup")])):
                campaign.side_effect = error
                self.assertEqual(qualification.main([]), 1)
            campaign.side_effect = None
            self.assertEqual(qualification.main([]), 0)

    def test_three_complete_generations_launch_three_independent_backends(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as temporary:
            inputs = {"root": Path(temporary), "host": Path("/host"), "modules": Path("/modules"),
                      "binary": Path("/sidecar"), "host_digest": "a" * 64, "digest": "b" * 64,
                      "contract": {}, "attestation": Path("/attestation"), "attestation_digest": "c" * 64}
            generated = []

            def sidecar(root, _binary, _digest, backend_port, access, backend_pin, used_ports):
                number = int(root.name.rsplit("-", 1)[1])
                root.mkdir(mode=0o700)
                root.joinpath("sidecar.log").write_bytes(b"")
                root.joinpath("sidecar.log").chmod(0o600)
                data, inode = qualification.bounded_read(access, 100)
                result = LifecycleTest().starts()[number - 1]
                result["sidecar_port"] = qualification.unused_port(used_ports)
                result["backend_log_evidence"] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                                                  "device": inode[0], "inode": inode[1]}
                generated.append((backend_port, access, backend_pin))
                return result

            processes = [mock.Mock(pid=number) for number in (11, 12, 13)]
            with mock.patch.object(qualification.subprocess, "Popen", side_effect=processes) as launch, \
                    mock.patch.object(qualification.base, "free_port", side_effect=range(10001, 10007)), \
                    mock.patch.object(qualification.base, "verify_stock_launch_artifacts"), \
                    mock.patch.object(qualification.base, "verify_artifact_digest"), \
                    mock.patch.object(qualification.base, "wait_ready"), \
                    mock.patch.object(qualification, "identity", side_effect=lambda pid, digest: qualification.Identity(pid, pid, digest)), \
                    mock.patch.object(qualification, "resources", return_value={"fd_count": 4, "rss_kib": 100, "accepted_peer_ports": []}), \
                    mock.patch.object(qualification, "run_start", side_effect=sidecar) as starts, \
                    mock.patch.object(qualification, "controlled_stop") as stop, \
                    mock.patch.object(qualification.base, "publish_verified_receipt") as publish, \
                    mock.patch("sys.stdout"):
                qualification.run_campaign(inputs)
                self.assertEqual(launch.call_count, 3)
                self.assertEqual(starts.call_count, 3)
                self.assertEqual(stop.call_count, 3)
                self.assertEqual(len({entry[0] for entry in generated}), 3)
                self.assertEqual(len({entry[1] for entry in generated}), 3)
                self.assertEqual(len({entry[2] for entry in generated}), 3)
                self.assertEqual(publish.call_args.args[1]["prerequisites"]["G2"], "passed")

    def test_primary_and_cleanup_errors_survive_and_prevent_publication(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as temporary:
            inputs = {"root": Path(temporary), "host": Path("/host"), "modules": Path("/modules"),
                      "binary": Path("/sidecar"), "host_digest": "a" * 64, "digest": "b" * 64,
                      "contract": {}, "attestation": Path("/attestation"), "attestation_digest": "c" * 64}
            process = mock.Mock(pid=11)
            primary, cleanup = RuntimeError("primary evidence failure"), RuntimeError("cleanup failure")
            with mock.patch.object(qualification.subprocess, "Popen", return_value=process), \
                    mock.patch.object(qualification.base, "free_port", return_value=12345), \
                    mock.patch.object(qualification.base, "verify_stock_launch_artifacts"), \
                    mock.patch.object(qualification.base, "verify_artifact_digest"), \
                    mock.patch.object(qualification.base, "wait_ready"), \
                    mock.patch.object(qualification, "identity", return_value=qualification.Identity(11, 11, "a" * 64)), \
                    mock.patch.object(qualification, "resources", return_value={}), \
                    mock.patch.object(qualification, "run_start", side_effect=primary), \
                    mock.patch.object(qualification, "controlled_stop", side_effect=cleanup), \
                    mock.patch.object(qualification.base, "publish_verified_receipt") as publish:
                with self.assertRaises(ExceptionGroup) as caught:
                    qualification.run_campaign(inputs)
                self.assertEqual(caught.exception.exceptions, (primary, cleanup))
                publish.assert_not_called()
                self.assertFalse(inputs["root"].joinpath("qualification", "qualification.json").exists())


if __name__ == "__main__":
    unittest.main()
