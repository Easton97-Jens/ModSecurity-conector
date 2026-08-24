import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "common" / "runtime" / "http_authorization_service.c"


class HttpAuthorizationServiceSecurityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE.read_text(encoding="utf-8")

    def test_listener_policy_is_loopback_only(self) -> None:
        listen_parser = self.source.split("static int parse_listen_spec(", 1)[1].split(
            "static void parsed_request_destroy", 1
        )[0]
        self.assertIn('strcmp(host, "127.0.0.1") != 0', listen_parser)
        self.assertNotIn('strcmp(host, "0.0.0.0")', listen_parser)

    def test_security_header_duplicates_are_rejected_before_mapping(self) -> None:
        duplicate_check = self.source.split(
            "static int security_header_duplicates_are_rejected(", 1
        )[1].split("static int request_hostname", 1)[0]
        request_path = self.source.split(
            "static int handle_authorization_request(", 1
        )[1].split("static int create_listener", 1)[0]
        self.assertIn('"host"', duplicate_check)
        self.assertIn("profile->original_uri_headers", duplicate_check)
        self.assertIn("msconnector_headers_count_name", duplicate_check)
        self.assertIn("security_header_duplicates_are_rejected", request_path)
        self.assertLess(
            request_path.index("security_header_duplicates_are_rejected"),
            request_path.index("source.method = parsed.method"),
        )

    def test_missing_or_oversized_host_fails_closed_before_mapping(self) -> None:
        hostname_check = self.source.split("static int request_hostname", 1)[1].split(
            "static int send_all", 1
        )[0]
        request_path = self.source.split(
            "static int handle_authorization_request(", 1
        )[1].split("static int create_listener", 1)[0]
        self.assertIn("msconnector_headers_find_first(", hostname_check)
        self.assertIn('"missing or invalid Host header"', hostname_check)
        self.assertNotIn("return request->server_address", hostname_check)
        self.assertIn("request_hostname(&parsed, error, sizeof(error))", request_path)
        self.assertIn("source.hostname = parsed.hostname", request_path)
        self.assertLess(
            request_path.index("request_hostname(&parsed, error, sizeof(error))"),
            request_path.index("source.method = parsed.method"),
        )

    def test_existing_content_length_and_transfer_encoding_controls_remain(self) -> None:
        self.assertIn("transfer_encoding_supported", self.source)
        self.assertIn("msconnector_headers_parse_content_length", self.source)
        self.assertIn("chunked request bodies are unsupported", self.source)

    def test_common_content_length_parser_rejects_any_duplicate_value(self) -> None:
        headers = (ROOT / "common" / "src" / "headers.c").read_text(encoding="utf-8")
        parser = headers.split("int msconnector_headers_parse_content_length(", 1)[1].split(
            "size_t msconnector_header_sanitize_value_for_log", 1
        )[0]
        self.assertIn("Reject every duplicate", parser)
        self.assertIn("if (seen) { return -1; }", parser)


if __name__ == "__main__":
    unittest.main()
