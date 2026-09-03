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
    def test_writes_are_peer_scoped_and_not_globally_sigpipe_ignored(self) -> None:
        self.assertIn("send(fd, p, len, MSG_NOSIGNAL)", SOURCE)
        self.assertIn("SO_NOSIGPIPE", SOURCE)
        self.assertNotIn("SIG_IGN", SOURCE)
        self.assertNotIn("sigaction(SIGPIPE", SOURCE)

    def test_peer_isolation_has_bounded_deadlines_and_admission(self) -> None:
        self.assertIn("SPOP_DEFAULT_TIMEOUT_MS 2000U", SOURCE)
        self.assertIn("SPOP_DEFAULT_WORKER_COUNT 8U", SOURCE)
        self.assertIn("SPOP_MAX_WORKER_COUNT 64U", SOURCE)
        self.assertIn("set_peer_socket_timeouts(fd, peer_timeout_ms(state))", SOURCE)
        self.assertIn("peer_workers_start(workers, listen_fd, fd, state, log,", SOURCE)
        self.assertIn("peer worker deadline reached; force-stopping", SOURCE)
        self.assertIn("active_fds[SPOP_MAX_WORKER_COUNT]", SOURCE)
        self.assertIn("pthread_cond_timedwait(&workers->drained", SOURCE)
        self.assertIn("shutdown(workers->active_fds[i], SHUT_RDWR)", SOURCE)
        self.assertNotIn("pthread_cancel", SOURCE)

    def test_parent_admission_rejection_cannot_parse_a_peer_loop(self) -> None:
        accept_loop = SOURCE.split("static int accept_loop", 1)[1].split(
            "static int client_expect_frame", 1
        )[0]
        accepted_peer = SOURCE.split("static void process_accepted_peer", 1)[1].split(
            "static int accept_loop", 1
        )[0]
        self.assertNotIn("handle_admission_failure_connection(fd, state, log)", accept_loop)
        self.assertIn("closing peer without protocol processing", accepted_peer)
        self.assertIn("shutdown(fd, SHUT_RDWR)", accepted_peer)

    def test_runtime_self_test_covers_reset_slow_peer_and_follow_up_hello(self) -> None:
        self.assertIn("client incomplete peer recovery PASS", SOURCE)
        self.assertIn("client parallel healthcheck handshake PASS", SOURCE)
        self.assertIn("server enforced slow HELLO deadline recovery PASS", SOURCE)
        slow_hello = SOURCE.split("static int run_client_slow_peer_test", 1)[1].split(
            "static int run_client_self_test", 1
        )[0]
        self.assertIn(
            "received = recv(slow_fd, &byte, sizeof(byte), MSG_DONTWAIT)",
            slow_hello,
        )
        self.assertIn("if (received != 0", slow_hello)
        self.assertIn("client notify set-var ack disconnect PASS", SOURCE)
        self.assertIn("client worker admission close isolation PASS", SOURCE)

    def test_deadline_keeps_worker_state_quarantined_until_drain(self) -> None:
        self.assertIn("destroying it here would be a UAF", SOURCE)
        self.assertIn("if (workers->initialized)", SOURCE)
        self.assertIn("#define SPOP_ACCEPT_QUARANTINED 2", SOURCE)
        self.assertIn("return SPOP_ACCEPT_QUARANTINED;", SOURCE)
        self.assertIn("if (accept_result == SPOP_ACCEPT_QUARANTINED)", SOURCE)
        self.assertIn("if (rc == SPOP_ACCEPT_QUARANTINED)", SOURCE)
        self.assertIn("_Exit(SPOP_ACCEPT_QUARANTINED);", SOURCE)

    def test_read_accepts_payload_with_terminal_poll_hup(self) -> None:
        self.assertIn("(descriptor.revents & POLLHUP) != 0", SOURCE)
        self.assertIn("(descriptor.revents & POLLIN) == 0", SOURCE)

    def test_accept_error_also_enters_worker_quarantine_path(self) -> None:
        accept_loop = SOURCE.split("static int accept_loop", 1)[1].split(
            "static int client_expect_frame", 1
        )[0]
        self.assertIn("result = 1;", accept_loop)
        self.assertIn("result == 0", accept_loop)
        self.assertIn("const int wait_result = peer_workers_wait", accept_loop)
        self.assertIn("if (workers->initialized)", accept_loop)

    def test_safe_example_does_not_reintroduce_a_single_peer_bottleneck(self) -> None:
        self.assertIn("worker-count=8", EXAMPLE)

    def test_closed_defaults_do_not_allow_continue_on_error(self) -> None:
        self.assertNotIn("option continue-on-error", EXAMPLE)
        self.assertNotIn('echo "    option continue-on-error"', HARNESS)
        self.assertIn("fail-mode=closed", EXAMPLE)
        self.assertIn("status 503", HARNESS)


if __name__ == "__main__":
    unittest.main()
