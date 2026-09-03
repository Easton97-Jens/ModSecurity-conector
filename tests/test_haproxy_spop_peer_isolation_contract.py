"""Regression contracts for the bounded HAProxy SPOP peer runtime."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "connectors" / "haproxy" / "src" / "haproxy_spop_diagnostic_runtime.c"
).read_text(encoding="utf-8")
EXAMPLE = (
    ROOT / "examples" / "haproxy" / "compatibility-spoe" / "modsecurity-agent.conf"
).read_text(encoding="utf-8")
HARNESS = (ROOT / "connectors" / "haproxy" / "harness" / "run_haproxy_smoke.sh").read_text(
    encoding="utf-8"
)


class HAProxySPOPPeerIsolationContractTests(unittest.TestCase):
    def test_peer_writes_are_bounded_and_not_globally_sigpipe_ignored(self) -> None:
        self.assertIn("send(fd, p, len, MSG_NOSIGNAL)", SOURCE)
        self.assertIn("write_full_until(fd, &net_len, sizeof(net_len), deadline)", SOURCE)
        self.assertIn("write_full_until(fd, frame.data, frame.len, deadline)", SOURCE)
        self.assertNotIn("SIG_IGN", SOURCE)
        self.assertNotIn("sigaction(SIGPIPE", SOURCE)

    def test_peer_isolation_has_bounded_deadlines_and_admission(self) -> None:
        self.assertIn("SPOP_OWNER_CALLER_WAIT_MS 1000U", SOURCE)
        self.assertIn("SPOP_OWNER_QUEUE_CAPACITY 128U", SOURCE)
        self.assertIn("send_frame_timeout(fd,", SOURCE)
        self.assertIn("recv_frame(fd, &frame, timeout_ms)", SOURCE)
        self.assertIn("read_full_until", SOURCE)

    def test_accept_loop_closes_each_peer_after_protocol_processing(self) -> None:
        accept_loop = SOURCE.split("static int accept_loop", 1)[1].split(
            "static int client_expect_frame", 1
        )[0]
        worker = SOURCE.split("static void *spop_connection_thread", 1)[1].split(
            "static int accept_loop", 1
        )[0]
        self.assertIn("handle_connection(task->fd, task->state, task->log", worker)
        self.assertIn("if (connection_rc != 0)", worker)
        self.assertIn("log_peer_failure_rate_limited(task->log)", worker)
        self.assertIn("close(task->fd)", worker)
        self.assertIn("task->gate->active--", worker)
        self.assertIn("pthread_cond_broadcast(&task->gate->changed)", worker)
        self.assertIn("pthread_attr_setdetachstate", accept_loop)
        self.assertIn("PTHREAD_CREATE_DETACHED", accept_loop)
        self.assertIn("if (gate.active >= gate.limit)", accept_loop)
        self.assertIn(
            '"event=spop-peer-capacity-rejected action=close reason=worker-capacity"',
            accept_loop,
        )
        self.assertIn("last_capacity_rejection_log_ms", accept_loop)
        self.assertIn("pthread_create(&thread", accept_loop)
        self.assertIn("close(fd)", accept_loop)

    def test_peer_admission_has_a_safe_minimum_and_bounded_pool(self) -> None:
        self.assertIn("#define SPOP_MIN_WORKER_COUNT 2U", SOURCE)
        self.assertIn("#define SPOP_MAX_WORKER_COUNT 64U", SOURCE)
        self.assertIn("config->worker_count = 8U", SOURCE)
        self.assertIn("config->worker_count < SPOP_MIN_WORKER_COUNT", SOURCE)
        self.assertIn("SPOP_MAX_TRANSACTION_SLOTS_TOTAL / config->worker_count", SOURCE)

    def test_peer_close_write_self_test_requires_normal_process_survival(self) -> None:
        self.assertIn("run_spop_peer_close_write_self_test", SOURCE)
        self.assertIn("shutdown(sockets[1], SHUT_RD)", SOURCE)
        self.assertIn("WIFEXITED(status)", SOURCE)
        self.assertIn("finish_ms - start_ms > 1000U", SOURCE)

    def test_runtime_self_test_covers_reset_slow_peer_and_follow_up_hello(self) -> None:
        self.assertIn("client healthcheck handshake PASS", SOURCE)
        self.assertIn("client notify set-var ack disconnect PASS", SOURCE)
        self.assertIn("read_full_until", SOURCE)

    def test_safe_example_does_not_reintroduce_a_single_peer_bottleneck(self) -> None:
        self.assertIn("worker-count=8", EXAMPLE)

    def test_closed_defaults_preserve_explicit_error_status_mapping(self) -> None:
        self.assertNotIn("option continue-on-error", EXAMPLE)
        self.assertIn("fail-mode=closed", EXAMPLE)
        self.assertIn("deny status 503", HARNESS)


if __name__ == "__main__":
    unittest.main()
