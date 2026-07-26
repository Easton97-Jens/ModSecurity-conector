"""Static safety contract for the Parent Apache Valgrind soak."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "ci/runtime/apache/run-apache-valgrind-soak.py"


class ApacheValgrindSoakTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = RUNNER.read_text(encoding="utf-8")

    def test_modes_limits_traffic_and_graceful_restarts_are_bounded(self) -> None:
        self.assertIn('choices=("memcheck", "helgrind")', self.source)
        self.assertIn("1 <= args.parallelism <= 16", self.source)
        self.assertIn("SIGUSR1", self.source)
        self.assertIn("process.wait(timeout=20)", self.source)
        self.assertIn("os.killpg(process.pid, signal.SIGKILL)", self.source)

    def test_memcheck_categories_and_failures_are_explicit(self) -> None:
        for category in ("definitely_lost", "indirectly_lost", "possibly_lost", "still_reachable", "invalid_access", "use_after_free", "double_free"):
            self.assertIn(category, self.source)
        self.assertIn('"still_reachable_is_not_leak_free": True', self.source)

    def test_missing_native_environment_is_blocked_not_passed(self) -> None:
        self.assertIn("EXIT_BLOCKED = 77", self.source)
        self.assertIn("BLOCKED: Valgrind", self.source)

    def test_no_suppressions_or_worktree_artifacts(self) -> None:
        self.assertNotIn("--suppressions", self.source)
        self.assertIn("evidence root must be outside the Git worktree", self.source)


if __name__ == "__main__":
    unittest.main()
