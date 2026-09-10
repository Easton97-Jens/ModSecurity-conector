"""Focused contracts for HAProxy SPOP peer failure and admission handling."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "connectors" / "haproxy" / "src" / "haproxy_spop_diagnostic_runtime.c"
).read_text(encoding="utf-8")


class HAProxySPOPSigpipePeerIsolationContractTests(unittest.TestCase):
    def test_protocol_writes_use_local_sigpipe_suppression(self) -> None:
        self.assertIn("send(fd, p, len, MSG_NOSIGNAL | MSG_DONTWAIT)", SOURCE)
        self.assertNotIn("signal(SIGPIPE, SIG_IGN)", SOURCE)
        self.assertNotIn("sigaction(SIGPIPE", SOURCE)
        self.assertIn("if (rc < 0)", SOURCE)

    def test_peer_worker_closes_and_releases_admission_on_every_exit(self) -> None:
        worker = SOURCE.split("static void *spop_connection_thread", 1)[1].split(
            "static int accept_loop", 1
        )[0]
        self.assertIn("connection_rc = handle_connection", worker)
        self.assertIn("if (connection_rc != 0)", worker)
        self.assertIn("log_peer_failure_rate_limited(task->log)", worker)
        self.assertIn("close(task->fd)", worker)
        self.assertIn("if (task->gate->active > 0U)", worker)
        self.assertIn("task->gate->active--", worker)
        self.assertIn("pthread_cond_broadcast(&task->gate->changed)", worker)
        self.assertIn("free(task)", worker)

    def test_accept_loop_is_bounded_and_does_not_run_protocol_inline(self) -> None:
        accept_loop = SOURCE.split("static int accept_loop", 1)[1].split(
            "static int client_expect_frame", 1
        )[0]
        spawn = SOURCE.split("static int spawn_spop_connection_worker", 1)[1].split(
            "static int accept_loop", 1
        )[0]
        self.assertIn("SPOP_MIN_WORKER_COUNT", SOURCE)
        self.assertIn("if (gate->active >= gate->limit)", spawn)
        self.assertIn(
            '"event=spop-peer-capacity-rejected action=close reason=worker-capacity"',
            spawn,
        )
        self.assertIn("pthread_create(&thread, detached_attributes", spawn)
        self.assertNotIn("handle_connection(fd, state, log", accept_loop)
        self.assertIn("close(fd);", spawn)
        self.assertIn("while (gate.active != 0U)", accept_loop)
        result_handler = SOURCE.split(
            "static spop_accept_iteration_result process_spop_worker_result", 1
        )[1].split("static int accept_loop", 1)[0]
        self.assertIn("SPOP_CONNECTION_WORKER_CAPACITY_REJECTED", result_handler)
        self.assertIn("SPOP_CONNECTION_WORKER_STOPPED", result_handler)
        self.assertIn("worker_result == SPOP_CONNECTION_WORKER_FATAL", result_handler)
        capacity = result_handler.index("SPOP_CONNECTION_WORKER_CAPACITY_REJECTED")
        stopped = result_handler.index("SPOP_CONNECTION_WORKER_STOPPED")
        fatal = result_handler.index("worker_result == SPOP_CONNECTION_WORKER_FATAL")
        capacity_return = result_handler.index(
            "return SPOP_ACCEPT_ITERATION_CONTINUE;", capacity
        )
        iteration_continue = accept_loop.index(
            "iteration_result == SPOP_ACCEPT_ITERATION_CONTINUE"
        )
        iteration_stop = accept_loop.index(
            "iteration_result == SPOP_ACCEPT_ITERATION_STOP"
        )
        handled = accept_loop.index("handled++;")
        self.assertLess(capacity, capacity_return)
        self.assertLess(
            iteration_continue,
            accept_loop.index("continue;", iteration_continue),
        )
        self.assertLess(iteration_continue, handled)
        self.assertLess(iteration_stop, accept_loop.index("break;", iteration_stop))
        self.assertLess(iteration_stop, handled)
        self.assertLess(
            capacity_return,
            result_handler.index("SPOP_ACCEPT_ITERATION_STOP", stopped),
        )
        self.assertLess(fatal, result_handler.index("loop_rc = 1;"))

    def test_peer_failure_event_is_rate_limited_and_preserves_peer_cleanup(self) -> None:
        self.assertIn("static uint64_t last_peer_failure_log_ms = 0U", SOURCE)
        self.assertIn("static void log_peer_failure_rate_limited", SOURCE)
        self.assertIn(
            '"event=spop-peer-session-failed action=close "',
            SOURCE,
        )
        self.assertIn('"reason=protocol-or-write-error"', SOURCE)
        self.assertIn("now - last_peer_failure_log_ms >= 1000U", SOURCE)

    def test_peer_close_and_follow_up_handshake_are_runtime_regressions(self) -> None:
        self.assertIn("run_spop_peer_close_write_self_test", SOURCE)
        self.assertIn("shutdown(sockets[1], SHUT_RD)", SOURCE)
        self.assertIn("client healthcheck handshake PASS", SOURCE)
        self.assertIn("client notify set-var ack disconnect PASS", SOURCE)
        self.assertIn("finish_ms - start_ms > 1000U", SOURCE)


if __name__ == "__main__":
    unittest.main()
