"""Boundary and verdict controls for stock-native supplementary diagnostics."""
import importlib.util
import json
import hashlib
from pathlib import Path
import tempfile
import socket
import shutil
import subprocess
import threading
import unittest


SPEC = importlib.util.spec_from_file_location("lighttpd_i12_diagnostic",
    Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/i12/lighttpd/diagnostic_capture.py")
DIAGNOSTIC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DIAGNOSTIC)
NATIVE_SPEC = importlib.util.spec_from_file_location("lighttpd_i12_diagnostic_native",
    Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/i12/lighttpd/diagnostic_native.py")
NATIVE = importlib.util.module_from_spec(NATIVE_SPEC)
NATIVE_SPEC.loader.exec_module(NATIVE)
PACKETS_SPEC = importlib.util.spec_from_file_location("lighttpd_i12_diagnostic_packets",
    Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/i12/lighttpd/diagnostic_packets.py")
PACKETS = importlib.util.module_from_spec(PACKETS_SPEC)
PACKETS_SPEC.loader.exec_module(PACKETS)


class DiagnosticTests(unittest.TestCase):
    def test_rule_oracle_uses_exact_main_transaction_event_or_audit_token(self):
        def audit_record(boundary, transaction_id, rule_id, extra=""):
            return (f"---{boundary}---A--\n[date] {transaction_id} 127.0.0.1\n"
                    f"---{boundary}---H--\n{extra}[id \"{rule_id}\"]\n"
                    f"---{boundary}---Z--\n")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            expected = {"rule_id": 1100001, "event_fields": []}
            (root / "audit.log").write_text(
                audit_record("main", "tx-main", 1100001)
                + audit_record("neighbor", "tx-neighbor", 1100202))
            matched = PACKETS._matching_oracle_events(root, [], expected, "tx-main")
            self.assertTrue(matched[2])
            expected["rule_id"] = 1100202
            self.assertFalse(PACKETS._matching_oracle_events(root, [], expected, "tx-main")[2])
            (root / "audit.log").write_text("unrelated-neighbor-metadata=1100001\n")
            expected["rule_id"] = 1100001
            self.assertFalse(PACKETS._matching_oracle_events(root, [], expected, "tx-main")[2])
            event = {"transaction_id": "tx-main", "rule_id": "1100001"}
            self.assertTrue(PACKETS._matching_oracle_events(root, [event], expected, "tx-main")[2])

    def test_parser_first_cause_preserves_first_physical_diagnostic_without_case_inference(self):
        self.assertIsNone(DIAGNOSTIC.parser_first_cause("dlopen failed: missing module\nConfiguration of plugins failed."))
        stderr = ("source.c.242: msconnector runtime config check failed: invalid enabled value\n"
                  "source.c.242: msconnector runtime config check failed: later diagnostic\n")
        self.assertEqual(DIAGNOSTIC.parser_first_cause(stderr), "invalid enabled value")

    def test_case_sources_reject_directory_escape_duplicates_and_parent_alias(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cases = root / "cases.json"
            for names in (("../escape",), ("same", "same")):
                cases.write_text(json.dumps({"cases": [{"case_id": name} for name in names]}))
                with self.assertRaisesRegex(ValueError, "unique physical-directory-safe"):
                    NATIVE.declared_cases(cases)
            cases.write_text(json.dumps({"cases": [{"case_id": "NEED-precommit-error"}]}))
            self.assertEqual(len(NATIVE.declared_cases(cases)), 1)
            (root / "alias").symlink_to(root, target_is_directory=True)
            alias = root / "alias/cases.json"
            with self.assertRaisesRegex(ValueError, "physical single-link"):
                NATIVE.declared_cases(alias)

    def test_waited_parser_receipt_preserves_exact_exit_and_real_rules_absence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            host = root / "lighttpd"
            shutil.copyfile("/bin/sh", host)
            host.chmod(0o500)
            directory = root / "parser"
            directory.mkdir()
            argv = ["rtk", "proxy", str(host), "-c", "exit 255"]
            actual = subprocess.run(argv, capture_output=True, timeout=5)
            self.assertEqual(actual.returncode, 255)
            record = {"argv": argv, "cwd": str(Path.cwd()), "exitcode": actual.returncode,
                      "waited_signal": None, "host_config_sha256": hashlib.sha256(b"test config").hexdigest()}
            missing = root / "absent.conf"
            case = ("missing_rules_file", "rules_file", str(missing))
            identity = {"run_id": "independent-receipt-unit", "parent_sha": "fixture-test"}
            DIAGNOSTIC.parser_process_receipt(directory, case, record, actual, host, missing, identity)
            receipt = json.loads((directory / "parser-process.json").read_text())
            absence = json.loads((directory / "rules-absence.json").read_text())
            self.assertEqual(receipt["waited_exit"], 255)
            self.assertIsNone(receipt["rules_sha256"])
            self.assertEqual((absence["measurement"], absence["errno"], absence["exists"]), ("lstat", 2, False))
            self.assertEqual(receipt["rules_path"], str(missing))
            self.assertEqual(receipt["rules_absence_sha256"], hashlib.sha256((directory / "rules-absence.json").read_bytes()).hexdigest())
            record["exitcode"] = 1
            with self.assertRaisesRegex(ValueError, "actually waited"):
                DIAGNOSTIC.parser_process_receipt(directory, case, record, actual, host, missing, identity)

    def test_cli_artifacts_reject_relative_wrong_name_and_symlink_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            physical = root / "lighttpd"
            physical.write_text("fixture")
            self.assertEqual(DIAGNOSTIC.approved_input(physical, "lighttpd"), physical)
            with self.assertRaisesRegex(ValueError, "artifact name"):
                DIAGNOSTIC.approved_input(physical, "mod_msconnector.so")
            (root / "alias").symlink_to(physical)
            with self.assertRaisesRegex(ValueError, "physical absolute"):
                DIAGNOSTIC.approved_input(root / "alias")
            with self.assertRaisesRegex(ValueError, "physical absolute"):
                DIAGNOSTIC.approved_input(Path("lighttpd"))

    def test_real_peer_response_over_bound_is_rejected_and_socket_closes(self):
        with socket.socket() as server:
            server.bind(("127.0.0.1", 0))
            server.listen(1)
            server.settimeout(3)
            def peer():
                with server.accept()[0] as client:
                    client.recv(65536)
                    try:
                        client.sendall(b"HTTP/1.1 200 OK\r\n\r\n" + b"x" * 140000)
                    except (BrokenPipeError, ConnectionResetError):
                        pass
            thread = threading.Thread(target=peer)
            thread.start()
            port = server.getsockname()[1]
            try:
                with self.assertRaisesRegex(ValueError, "128 KiB"):
                    DIAGNOSTIC.request(port)
            finally:
                thread.join(timeout=5)
            self.assertFalse(thread.is_alive())

    def test_negative_parser_acceptance_and_signals_cannot_succeed(self):
        receipt = {"configuration_probes": [{"exitcode": code} for code in [0] + [255] * 7],
                   "clients": [{"status": code} for code in [200, 403, 200]]}
        self.assertTrue(DIAGNOSTIC.controls_match(receipt))
        for code in (0, -9):
            receipt["configuration_probes"][3]["exitcode"] = code
            self.assertFalse(DIAGNOSTIC.controls_match(receipt))
        receipt["configuration_probes"][3]["exitcode"] = 255
        receipt["clients"][2]["status"] = 500
        self.assertFalse(DIAGNOSTIC.controls_match(receipt))

    def test_output_parent_alias_existing_and_private_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "alias").symlink_to(root, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "physical"):
                DIAGNOSTIC.fresh_output(root / "alias/child")
            actual = DIAGNOSTIC.fresh_output(root / "physical")
            self.assertEqual(actual.stat().st_mode & 0o777, 0o700)
            with self.assertRaisesRegex(ValueError, "Fresh"):
                DIAGNOSTIC.fresh_output(actual)

    def test_numeric_loopback_client_keeps_origin_form_contract(self):
        source = (Path(__file__).resolve().parents[1]
                  / "ci/runtime/lifecycle/i12/lighttpd/stock_raw_client.py").read_text()
        generated = NATIVE.numeric_loopback_client(source)
        self.assertNotIn("urlsplit", generated)
        self.assertIn("socket.create_connection(('127.0.0.1',port)", generated)
        self.assertEqual(NATIVE.loopback_target(8080, "/diagnostic?case=p1"),
                         ["--i12-port", "8080", "--i12-path", "/diagnostic?case=p1"])


if __name__ == "__main__":
    unittest.main()
