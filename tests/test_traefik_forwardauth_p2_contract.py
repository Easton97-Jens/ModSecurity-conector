from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "traefik_runtime_smoke",
    ROOT / "connectors/traefik/scripts/runtime_smoke.py",
)
assert SPEC is not None
assert SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class TraefikForwardAuthP2ContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dynamic = RUNNER.dynamic_config(
            18081, 18082, Path("/run/modsecurity/traefik-forwardauth-companion.sock")
        )
        self.service = (
            ROOT / "connectors/traefik/config/traefik-forwardauth.conf"
        ).read_text(encoding="utf-8")

    def test_checked_in_pair_enables_bounded_buffered_p2(self) -> None:
        RUNNER.validate_forwardauth_p2_contract(self.dynamic, self.service)
        self.assertRegex(self.dynamic, r"(?m)^        forwardBody: true$")
        self.assertRegex(self.dynamic, r"(?m)^        maxBodySize: 4096$")
        self.assertRegex(self.service, r"(?m)^request_body_mode=buffered$")
        self.assertRegex(self.service, r"(?m)^request_body_limit=4096$")

    def test_post_body_fixture_and_oversize_case_are_explicitly_modelled(self) -> None:
        """Source-contract coverage; a Traefik binary is required for host evidence."""

        post_body = b"traefik-forwardauth-p2-body-marker"
        oversized_body = b"x" * (RUNNER.FORWARDAUTH_P2_BODY_LIMIT + 1)
        self.assertLessEqual(len(post_body), RUNNER.FORWARDAUTH_P2_BODY_LIMIT)
        self.assertGreater(len(oversized_body), RUNNER.FORWARDAUTH_P2_BODY_LIMIT)
        self.assertIn("forwardBody: true", self.dynamic)
        self.assertIn("maxBodySize: 4096", self.dynamic)
        self.assertIn("request_body_limit=4096", self.service)

    def test_missing_forward_body_is_rejected(self) -> None:
        missing_forward_body = self.dynamic.replace("        forwardBody: true\n", "")
        with self.assertRaisesRegex(RuntimeError, "forwardBody"):
            RUNNER.validate_forwardauth_p2_contract(missing_forward_body, self.service)

    def test_oversized_host_limit_is_rejected(self) -> None:
        oversized = self.dynamic.replace("        maxBodySize: 4096", "        maxBodySize: 4097")
        with self.assertRaisesRegex(RuntimeError, "maxBodySize must equal 4096"):
            RUNNER.validate_forwardauth_p2_contract(oversized, self.service)

    def test_mismatched_common_limit_is_rejected(self) -> None:
        mismatched = self.service.replace("request_body_limit=4096", "request_body_limit=4097")
        with self.assertRaisesRegex(RuntimeError, "request_body_limit must equal 4096"):
            RUNNER.validate_forwardauth_p2_contract(self.dynamic, mismatched)

    def test_body_headers_are_auth_request_only_and_not_response_or_upstream_headers(self) -> None:
        auth_request, auth_response = self.dynamic.split("        authResponseHeaders:", 1)
        self.assertIn("- Content-Type", auth_request)
        self.assertIn("- Content-Length", auth_request)
        self.assertNotIn("- Content-Type", auth_response)
        self.assertNotIn("- Content-Length", auth_response)
        self.assertNotIn("request_body", auth_response)
        self.assertNotIn("body_marker", auth_response)

    def test_start_smoke_has_fail_closed_p2_guards(self) -> None:
        script = (ROOT / "connectors/traefik/scripts/start-smoke.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("forwardAuth P2 requires forwardBody=true and maxBodySize=4096", script)
        self.assertIn("request_body_mode=buffered", script)
        self.assertIn("request_body_limit=4096", script)
        self.assertIn("exit 77", script)


if __name__ == "__main__":
    unittest.main()
