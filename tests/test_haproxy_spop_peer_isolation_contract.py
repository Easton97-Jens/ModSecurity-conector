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
        self.assertIn("peer_workers_start(&workers, listen_fd, fd, state, log,", SOURCE)
        self.assertIn("peer worker deadline reached; force-stopping", SOURCE)

    def test_parent_admission_rejection_cannot_parse_a_peer_loop(self) -> None:
        accept_loop = SOURCE.split("static int accept_loop", 1)[1].split(
            "static int client_expect_frame", 1
        )[0]
        self.assertNotIn("handle_admission_failure_connection(fd, state, log)", accept_loop)
        self.assertIn("closing peer without protocol processing", accept_loop)
        self.assertIn("shutdown(fd, SHUT_RDWR)", accept_loop)

    def test_runtime_self_test_covers_reset_slow_peer_and_follow_up_hello(self) -> None:
        self.assertIn("client incomplete peer recovery PASS", SOURCE)
        self.assertIn("client parallel healthcheck handshake PASS", SOURCE)
        self.assertIn("client slow HELLO deadline recovery PASS", SOURCE)
        self.assertIn("client notify set-var ack disconnect PASS", SOURCE)
        self.assertIn("client worker admission close isolation PASS", SOURCE)

    def test_safe_example_does_not_reintroduce_a_single_peer_bottleneck(self) -> None:
        self.assertIn("worker-count=8", EXAMPLE)

    def test_closed_defaults_do_not_allow_continue_on_error(self) -> None:
        self.assertNotIn("option continue-on-error", EXAMPLE)
        self.assertNotIn('echo "    option continue-on-error"', HARNESS)
        self.assertIn("fail-mode=closed", EXAMPLE)
        self.assertIn("status 503", HARNESS)


if __name__ == "__main__":
    unittest.main()
