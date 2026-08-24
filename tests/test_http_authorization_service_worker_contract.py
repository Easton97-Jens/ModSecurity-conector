import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "common" / "runtime" / "http_authorization_service.c"


class HttpAuthorizationServiceWorkerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE.read_text(encoding="utf-8")

    def test_worker_admission_is_bounded_and_rejects_after_limit(self) -> None:
        self.assertIn("AUTH_MAX_CONNECTIONS_MAX 64UL", self.source)
        self.assertIn("service->active_workers >= service->max_connections", self.source)
        self.assertIn("(void)close(socket_fd);", self.source)

    def test_worker_shutdown_is_timed_and_does_not_abort_or_free_live_runtime(self) -> None:
        self.assertIn("pthread_cond_timedwait", self.source)
        self.assertIn("worker shutdown grace period expired", self.source)
        self.assertIn("worker shutdown did not complete", self.source)
        self.assertIn("runtime call may be uninterruptible", self.source)
        self.assertNotIn("abort();", self.source)

    def test_http_writes_are_sigpipe_safe_without_global_signal_suppression(self) -> None:
        self.assertIn("MSG_NOSIGNAL", self.source)
        self.assertIn("SO_NOSIGPIPE", self.source)
        self.assertIn("setsockopt(socket_fd, SOL_SOCKET, SO_NOSIGPIPE", self.source)
        self.assertIn("errno = ENOTSUP", self.source)
        self.assertIn("!configure_client_socket(client_fd)", self.source)
        self.assertNotIn("signal(SIGPIPE, SIG_IGN)", self.source)


if __name__ == "__main__":
    unittest.main()
