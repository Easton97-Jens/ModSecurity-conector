import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "common" / "runtime" / "http_authorization_service.c"
COMPANION_FIXTURE = ROOT / "tests" / "http_authorization_service_response_companion_lifecycle_smoke.c"


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

    def test_response_companion_failure_quarantines_service_and_returns_failure(self) -> None:
        failure = self.source.split(
            "if (!authorization_shutdown_response_companion(profile)) {", 1
        )[1].split("authorization_service_release(service);", 1)[0]
        self.assertIn("refusing runtime destruction", failure)
        self.assertIn("return service_status != 0 ? service_status : 1;", failure)
        self.assertNotIn("authorization_service_destroy(service);", failure)
        self.assertNotIn("authorization_service_release(service);", failure)

    def test_deferred_cleanup_waits_for_companion_quiescence(self) -> None:
        self.assertIn("int response_companion_quiesced;", self.source)
        self.assertIn("int release_claimed;", self.source)
        self.assertIn(
            "service->deferred_cleanup &&\n                service->response_companion_quiesced",
            self.source,
        )
        self.assertIn(
            "authorization_mark_response_companion_quiesced(service)",
            self.source,
        )
        self.assertIn("&& !service->release_claimed", self.source)
        self.assertIn("service->release_claimed = 1;", self.source)
        self.assertIn(
            "service->deferred_cleanup = 1;",
            self.source,
        )

    def test_deferred_cleanup_releases_only_profiles_without_a_companion(self) -> None:
        deferred_path = self.source.split(
            "static int authorization_defer_uninterruptible_worker(", 1
        )[1].split("static authorization_listener_iteration", 1)[0]
        self.assertIn("authorization_defer_cleanup(service) == 0", deferred_path)
        self.assertIn("profile->shutdown_response_companion == NULL", deferred_path)
        self.assertIn(
            "authorization_mark_response_companion_quiesced(service)", deferred_path
        )
        self.assertIn("return 1;", deferred_path)

    def test_companion_failure_keeps_runtime_quarantined(self) -> None:
        failure = self.source.split(
            "if (!authorization_shutdown_response_companion(profile)) {", 1
        )[1].split("return service_status != 0 ? service_status : 1;", 1)[0]
        self.assertIn("refusing runtime destruction", failure)
        self.assertIn("Keep the service and runtime quarantined", failure)

    def test_release_claim_is_made_under_worker_lock(self) -> None:
        release_path = self.source.split(
            "static int authorization_mark_response_companion_quiesced(", 1
        )[1].split("static int authorization_shutdown_response_companion(", 1)[0]
        self.assertIn("pthread_mutex_lock(&service->worker_lock)", release_path)
        self.assertIn("service->release_claimed = 1;", release_path)
        self.assertIn("pthread_mutex_unlock(&service->worker_lock)", release_path)

    def test_existing_sigpipe_control_remains_active(self) -> None:
        self.assertIn("signal(SIGPIPE, SIG_IGN)", self.source)

    def test_response_companion_fixture_exercises_live_handoff_and_quarantine(self) -> None:
        fixture = COMPANION_FIXTURE.read_text(encoding="utf-8")
        self.assertIn("msconnector_http_authorization_service_main", fixture)
        self.assertIn("companion_handoff", fixture)
        self.assertIn("companion_shutdown", fixture)
        self.assertIn("companion_has_retained_transaction", fixture)
        self.assertIn("test_failed_companion_quarantines_service", fixture)
        self.assertIn("test_concurrent_owner_worker_release", fixture)
        self.assertIn("test_no_companion_deferred_release", fixture)


if __name__ == "__main__":
    unittest.main()
