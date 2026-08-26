import unittest
from pathlib import Path


CONFIG = (
    Path(__file__).resolve().parents[1]
    / "config"
    / "traefik-forwardauth-composite-dynamic.yaml"
)


class CompositeConfigTests(unittest.TestCase):
    def test_private_lease_is_not_copied_from_forwardauth_response(self):
        text = CONFIG.read_text(encoding="utf-8")
        self.assertNotIn("authResponseHeaders", text)
        self.assertIn("authRequestHeaders:", text)
        self.assertIn("- X-Msconnector-Composite-Lease", text)
        self.assertNotIn("- X-Msconnector-Composite-Request-Context", text)

    def test_lease_is_stripped_after_forwardauth_before_upstream(self):
        text = CONFIG.read_text(encoding="utf-8")
        chain = [
            "- modsecurity-composite",
            "- modsecurity-composite-forwardauth",
            "- modsecurity-composite-strip-internal-lease",
        ]
        offsets = [text.index(item) for item in chain]
        self.assertEqual(offsets, sorted(offsets))
        strip_start = text.index("modsecurity-composite-strip-internal-lease:")
        self.assertIn("X-Msconnector-Composite-Lease: \"\"", text[strip_start:])
        self.assertIn("X-Msconnector-Composite-Request-Context: \"\"", text[strip_start:])

    def test_upstream_uses_verifying_loopback_tls_transport(self):
        text = CONFIG.read_text(encoding="utf-8")
        self.assertIn("- url: https://__UPSTREAM_ADDRESS__", text)
        self.assertIn("serversTransport: composite-upstream-transport", text)
        self.assertIn("serverName: composite-upstream.local", text)
        self.assertIn("rootCAs:", text)
        self.assertIn("__UPSTREAM_CERTIFICATE__", text)
        self.assertNotIn("insecureSkipVerify", text)


if __name__ == "__main__":
    unittest.main()
