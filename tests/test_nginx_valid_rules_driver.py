"""Driver unit controls are not substitutes for actual native runtime evidence."""

import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


class ValidRulesDriverTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location(
            "valid_rules_driver", ROOT / "ci/runtime/lifecycle/run-nginx-valid-rules.py")
        cls.driver = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.driver)

    def test_projection_name_is_bounded_safe_and_run_specific(self):
        first = self.driver.projection_name("a" * 128)
        self.assertLessEqual(len(first), 128)
        self.assertRegex(first, r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
        self.assertEqual(first, self.driver.projection_name("a" * 128))
        self.assertNotEqual(first, self.driver.projection_name("b" * 128))

    def test_native_event_requires_exact_native_transaction_rule_and_request(self):
        event = {"connector": "nginx", "integration_mode": "native-nginx-http-module",
                 "transaction_id": "native-123", "phase": 1, "rule_id": "1100001",
                 "method": "GET", "uri": "/no-crs/deny", "event": "engine_decision",
                 "message_id": "MSCONN_EVENT_ENGINE_DECISION", "status": "blocked",
                 "http_status": 403, "requested_action": "deny", "actual_action": "",
                 "visible_http_status": 0, "transport_result": "not_observable"}
        self.assertEqual(self.driver.match_native_event([event], "unit"), "native-123")
        for field, value in (("connector", "apache"), ("phase", 0), ("rule_id", "1100002"),
                             ("method", "POST"), ("uri", "/other"),
                             ("transaction_id", ""), ("run_id", "foreign")):
            with self.subTest(field=field):
                bad = dict(event, **{field: value})
                with self.assertRaises(ValueError):
                    self.driver.match_native_event([bad], "unit")
        for field in ("event", "message_id", "status", "http_status", "requested_action",
                      "actual_action", "visible_http_status", "transport_result"):
            for missing in (True, False):
                bad = dict(event)
                if missing:
                    bad.pop(field)
                else:
                    bad[field] = "wrong"
                with self.assertRaises(ValueError):
                    self.driver.match_native_event([bad], "unit")

    def test_native_evidence_with_multiple_transactions_is_ambiguous(self):
        event = {"connector": "nginx", "integration_mode": "native-nginx-http-module",
                 "transaction_id": "first", "phase": 1, "rule_id": "1100001",
                 "method": "GET", "uri": "/no-crs/deny", "event": "engine_decision",
                 "message_id": "MSCONN_EVENT_ENGINE_DECISION", "status": "blocked",
                 "http_status": 403, "requested_action": "deny", "actual_action": "",
                 "visible_http_status": 0, "transport_result": "not_observable"}
        with self.assertRaises(ValueError):
            self.driver.match_native_event([event, dict(event, transaction_id="second")], "unit")

    def test_roles_require_root_master_and_actual_nobody_child(self):
        good = {"run_id": "unit", "master_pid": 123, "worker_pid": 124,
                "master_uid": 0, "worker_uid": 65534}
        self.assertTrue(self.driver.valid_roles(good))
        for field, value in (("master_uid", 65534), ("worker_uid", 0),
                             ("worker_pid", 123), ("master_pid", 0)):
            self.assertFalse(self.driver.valid_roles(dict(good, **{field: value})))

    def test_configuration_retains_exact_rules_module_and_external_docroot(self):
        text = self.driver.config_template(Path("/var/tmp/codex/unit"), 32123,
                                           "/var/tmp/codex/projection/child")
        self.assertIn('load_module "/var/tmp/codex/unit/nginx-module.so";', text)
        self.assertIn('modsecurity_rules_file "/var/tmp/codex/unit/no-crs-baseline.conf";', text)
        self.assertIn('user nobody nogroup;', text)
        self.assertIn('daemon off;', text)
        self.assertIn('access_log off;', text,
                      'never inherit a compiled staging-prefix access-log path')
        self.assertIn('listen 127.0.0.1:32123;', text)
        self.assertIn('root "/var/tmp/codex/projection/child";', text)

    def test_bounded_capture_rejects_symlink_special_and_oversized(self):
        with tempfile.TemporaryDirectory(prefix="valid-rules-capture-") as temporary:
            root = Path(temporary)
            regular = root / "regular"
            regular.write_bytes(b"actual retained bytes")
            self.assertEqual(self.driver.bounded_capture(regular), b"actual retained bytes")
            link = root / "link"
            link.symlink_to(regular)
            with self.assertRaises(OSError):
                self.driver.bounded_capture(link)
            fifo = root / "fifo"
            os.mkfifo(fifo)
            with self.assertRaises(ValueError):
                self.driver.bounded_capture(fifo)
            regular.write_bytes(b"a" * (self.driver.BASE.CAPTURE_LIMIT + 1))
            with self.assertRaises(ValueError):
                self.driver.bounded_capture(regular)

    def test_cleanup_checks_actual_processes_and_listener(self):
        process = mock.Mock()
        process.poll.return_value = None
        roles = {"master_pid": 123, "worker_pid": 124, "master_uid": 0, "worker_uid": 65534}
        with mock.patch.object(self.driver, "process_info", return_value=None), \
                mock.patch.object(self.driver, "listener_open", return_value=False):
            cleanup = self.driver.stop_owned_master(process, roles, 32123, "unit")
        process.send_signal.assert_called_once_with(self.driver.signal.SIGQUIT)
        process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(cleanup, {"run_id": "unit", "master_pid": 123, "worker_pid": 124,
                                   "master_running": False, "worker_running": False,
                                   "listener_open": False, "verified": True})
        with mock.patch.object(self.driver, "process_info", return_value=(65534, 123, "S", "1")), \
                mock.patch.object(self.driver, "listener_open", return_value=True):
            cleanup = self.driver.stop_owned_master(None, roles, 32123, "unit")
        self.assertFalse(cleanup["verified"])

    def test_forced_cleanup_is_not_successful_cleanup_evidence(self):
        process = mock.Mock()
        process.poll.return_value = None
        process.wait.side_effect = [self.driver.subprocess.TimeoutExpired("owned-nginx", 5), 0]
        with mock.patch.object(self.driver, "process_info", return_value=None), \
                mock.patch.object(self.driver, "listener_open", return_value=False):
            cleanup = self.driver.stop_owned_master(process, {"master_pid": 123, "worker_pid": 124}, 32123, "unit")
        process.kill.assert_called_once_with()
        self.assertFalse(cleanup["verified"])

    def test_forced_cleanup_signals_only_bound_child_handle(self):
        process = mock.Mock(pid=123)
        process.poll.return_value = None
        process.wait.side_effect = [self.driver.subprocess.TimeoutExpired("owned-nginx", 5), 0]
        child = (65534, 123, "S", "bound-starttime")
        with mock.patch.object(Path, "read_text", return_value="124"), \
                mock.patch.object(self.driver, "process_info", side_effect=[child, child, None, None]), \
                mock.patch.object(self.driver.os, "pidfd_open", return_value=987) as opened, \
                mock.patch.object(self.driver, "pidfd_running", side_effect=[True, False, False]), \
                mock.patch.object(self.driver.os, "close") as closed, \
                mock.patch.object(self.driver.signal, "pidfd_send_signal") as signalled, \
                mock.patch.object(self.driver, "listener_open", return_value=False):
            cleanup = self.driver.stop_owned_master(process, {"master_pid": 123, "worker_pid": 124}, 32123, "unit")
        opened.assert_called_once_with(124)
        signalled.assert_called_once_with(987, self.driver.signal.SIGKILL)
        closed.assert_called_once_with(987)
        self.assertFalse(cleanup["verified"])

    def test_exited_master_still_retires_previously_bound_surviving_worker(self):
        process = mock.Mock(pid=123)
        process.poll.return_value = 0
        roles = {"master_pid": 123, "worker_pid": 124, "master_uid": 0, "worker_uid": 65534}
        handles = {124: 987}
        with mock.patch.object(self.driver, "pidfd_running", side_effect=[True, False, False]), \
                mock.patch.object(self.driver, "process_info", return_value=None), \
                mock.patch.object(self.driver.os, "close") as closed, \
                mock.patch.object(self.driver.signal, "pidfd_send_signal") as signalled, \
                mock.patch.object(self.driver, "listener_open", return_value=False):
            cleanup = self.driver.stop_owned_master(process, roles, 32123, "unit", handles)
        signalled.assert_called_once_with(987, self.driver.signal.SIGKILL)
        closed.assert_called_once_with(987)
        self.assertFalse(cleanup["verified"])

    def test_unknown_roles_never_produce_verified_cleanup(self):
        with mock.patch.object(self.driver, "process_info", return_value=None), \
                mock.patch.object(self.driver, "listener_open", return_value=False):
            cleanup = self.driver.stop_owned_master(None, {}, 32123, "unit")
        self.assertFalse(cleanup["verified"])

    def test_startup_failure_binds_children_before_role_observation(self):
        process = mock.Mock(pid=123)
        process.poll.return_value = 1
        handles = {}
        def bind(actual_process, registry):
            self.assertIs(actual_process, process)
            registry[124] = 987
        with mock.patch.object(self.driver, "bind_owned_children", side_effect=bind):
            with self.assertRaisesRegex(ValueError, "NGINX exited"):
                self.driver.observe_roles(process, "unit", 32123, Path("/unused"), handles)
        self.assertEqual(handles, {124: 987})
        with mock.patch.object(self.driver, "pidfd_running", side_effect=[True, False, False]), \
                mock.patch.object(self.driver, "process_info", return_value=None), \
                mock.patch.object(self.driver.os, "close"), \
                mock.patch.object(self.driver.signal, "pidfd_send_signal") as signalled, \
                mock.patch.object(self.driver, "listener_open", return_value=False):
            cleanup = self.driver.stop_owned_master(process, {}, 32123, "unit", handles)
        signalled.assert_called_once_with(987, self.driver.signal.SIGKILL)
        self.assertFalse(cleanup["verified"])


if __name__ == "__main__":
    unittest.main()
