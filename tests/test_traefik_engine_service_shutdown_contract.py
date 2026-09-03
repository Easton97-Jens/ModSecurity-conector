"""Static lifecycle contracts for the native Traefik UDS engine service."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "connectors" / "traefik" / "src" / "traefik_engine_service.c"
).read_text(encoding="utf-8")


class TraefikEngineServiceShutdownContractTests(unittest.TestCase):
    def test_peer_writes_and_worker_admission_are_bounded(self) -> None:
        self.assertIn("TRAEFIK_ENGINE_MAX_WORKERS 64U", SOURCE)
        self.assertIn("TRAEFIK_ENGINE_SEND_TIMEOUT_MILLISECONDS", SOURCE)
        self.assertIn("clock_gettime(CLOCK_MONOTONIC, &deadline)", SOURCE)
        self.assertIn("poll(&descriptor, 1U, remaining_ms)", SOURCE)
        self.assertIn("send(socket_fd, data + offset, size - offset,\n            MSG_NOSIGNAL | MSG_DONTWAIT)", SOURCE)
        self.assertIn("errno == EAGAIN ||", SOURCE)
        self.assertNotIn("SIGPIPE", SOURCE)
        self.assertIn("if (worker_status == 0)", SOURCE)
        self.assertIn("(void)close(client);\n                continue;", SOURCE)

    def test_worker_cleanup_uses_stable_admission_slot(self) -> None:
        self.assertIn("size_t slot;", SOURCE)
        self.assertIn("worker->slot = slot;", SOURCE)
        self.assertIn("slot = worker->slot;", SOURCE)
        self.assertIn(
            "if (slot < TRAEFIK_ENGINE_MAX_WORKERS &&\n"
            "            service->worker_sockets[slot] == socket_fd)",
            SOURCE,
        )
        self.assertNotIn(
            "for (size_t index = 0U; index < TRAEFIK_ENGINE_MAX_WORKERS; ++index) {\n"
            "            if (service->worker_sockets[index] == socket_fd)",
            SOURCE,
        )

    def test_shutdown_cancels_workers_and_never_waits_forever(self) -> None:
        self.assertIn("shutdown(service->worker_sockets[index], SHUT_RDWR)", SOURCE)
        self.assertIn("pthread_cond_timedwait", SOURCE)
        self.assertIn("TRAEFIK_ENGINE_WORKER_SHUTDOWN_TIMEOUT_SECONDS 30", SOURCE)
        self.assertIn("failure_stage=worker_shutdown_timeout; ", SOURCE)
        self.assertIn("_exit(1);", SOURCE)


if __name__ == "__main__":
    unittest.main()
