"""Static contracts for NGINX-native request boundary hardening."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ACCESS = (ROOT / "connectors/nginx/src/ngx_http_modsecurity_access.c").read_text(
    encoding="utf-8"
)
MAPPER = (ROOT / "connectors/nginx/src/ngx_http_modsecurity_mapper.c").read_text(
    encoding="utf-8"
)
MODULE = (ROOT / "connectors/nginx/src/ngx_http_modsecurity_module.c").read_text(
    encoding="utf-8"
)
COMMON = (ROOT / "connectors/nginx/src/ngx_http_modsecurity_common.h").read_text(
    encoding="utf-8"
)


class NginxNativeSecurityContractTest(unittest.TestCase):
    def test_hostname_requires_received_host_and_has_no_server_name_fallback(self) -> None:
        hostname = ACCESS.split(
            "ngx_http_modsecurity_set_request_hostname", 1
        )[1].split("static ngx_int_t", 1)[0]
        self.assertIn("r->headers_in.host != NULL", hostname)
        self.assertIn("NGX_HTTP_BAD_REQUEST", hostname)
        self.assertNotIn("server_name", hostname)
        self.assertNotIn("headers_in.server", hostname)
        self.assertNotIn("server_name", MAPPER)
        self.assertNotIn("headers_in.server", MAPPER)

    def test_request_body_has_content_length_chunk_and_file_caps(self) -> None:
        self.assertIn("common_config.request_body_limit", ACCESS)
        self.assertIn("request_body_bytes_seen > limit", ACCESS)
        self.assertIn("chunk_size > limit - ctx->request_body_bytes_seen", ACCESS)
        self.assertIn("ngx_file_info(", ACCESS)
        self.assertIn("ngx_file_size(&file_info)", ACCESS)
        self.assertIn("NGX_HTTP_REQUEST_ENTITY_TOO_LARGE", ACCESS)

    def test_native_ingestion_failures_remain_fail_closed(self) -> None:
        self.assertIn("ret = msc_append_request_body", ACCESS)
        self.assertIn("ret = msc_request_body_from_file", ACCESS)
        self.assertIn("if (ret != 1)", ACCESS)

    def test_mapper_failure_stops_initialization_before_header_sink(self) -> None:
        mapper = ACCESS.split(
            "ngx_http_modsecurity_validate_common_request_mapper", 1
        )[1].split("static ngx_int_t", 1)[0]
        initialize = ACCESS.split(
            "ngx_http_modsecurity_initialize_request", 1
        )[1].split("static ngx_int_t", 1)[0]

        self.assertIn("validation failed", mapper)
        self.assertIn("return NGX_HTTP_BAD_REQUEST", mapper)
        self.assertNotIn("validation skipped", mapper)
        self.assertIn(
            "rc = ngx_http_modsecurity_validate_common_request_mapper(r);",
            initialize,
        )
        self.assertIn(
            "if (rc != NGX_OK) {\n        ctx->intervention_triggered = 1;\n        return rc;\n    }",
            initialize,
        )
        self.assertLess(
            initialize.index("ngx_http_modsecurity_validate_common_request_mapper"),
            initialize.index("ngx_http_modsecurity_set_request_hostname"),
        )
        self.assertLess(
            initialize.index("return rc;"),
            initialize.index("ngx_http_modsecurity_process_request_headers"),
        )
        self.assertIn("ngx_http_modsecurity_add_n_request_header", ACCESS)
        request_header_sink = COMMON.split(
            "ngx_http_modsecurity_add_n_request_header", 1
        )[1].split("ngx_http_modsecurity_add_n_response_header", 1)[0]
        self.assertIn("msc_add_n_request_header", request_header_sink)
        self.assertLess(
            request_header_sink.index("ngx_http_modsecurity_validate_header"),
            request_header_sink.index("msc_add_n_request_header"),
        )

    def test_native_event_file_configuration_is_disabled_before_open(self) -> None:
        setter = MODULE.split("static char *\nngx_conf_set_phase4_log", 1)[1].split(
            "static ngx_int_t", 1
        )[0]
        self.assertIn("native NGINX phase4 event-file logging is disabled", setter)
        self.assertNotIn("ngx_conf_open_file(", setter)
        self.assertNotIn("ngx_write_fd", setter)

    def test_content_type_file_is_descriptor_pinned_regular_and_bounded(self) -> None:
        loader = MODULE.split(
            "static char *\nngx_http_modsecurity_phase4_load_content_types_file", 1
        )[1].split("\n\nstatic char *\nngx_conf_set_common_flag_slot", 1)[0]

        self.assertIn(
            "#define MSCONNECTOR_NGINX_PHASE4_CONTENT_TYPES_FILE_MAX_BYTES (64U * 1024U)",
            MODULE,
        )
        self.assertIn("ngx_fd_info(file.fd, &fi)", loader)
        self.assertIn("!ngx_is_file(&fi)", loader)
        self.assertIn("NGX_FILE_RDONLY|NGX_FILE_NONBLOCK", loader)
        self.assertIn("#if (NGX_WIN32)", loader)
        self.assertIn("unavailable on Win32 by security policy", loader)
        self.assertIn(
            "MSCONNECTOR_NGINX_PHASE4_CONTENT_TYPES_FILE_MAX_BYTES", loader
        )
        self.assertIn("n != (ssize_t) file_size", loader)
        self.assertLess(loader.index("ngx_open_file("), loader.index("ngx_fd_info("))
        self.assertLess(loader.index("ngx_fd_info("), loader.index("ngx_pnalloc("))

    def test_rejected_native_event_and_remote_paths_have_no_active_examples(self) -> None:
        safe = (ROOT / "examples/nginx/safe/nginx.conf").read_text(
            encoding="utf-8"
        )
        strict = (ROOT / "examples/nginx/strict/nginx.conf").read_text(
            encoding="utf-8"
        )
        smoke = (ROOT / "connectors/nginx/harness/nginx_smoke.conf").read_text(
            encoding="utf-8"
        )
        reference = (ROOT / "examples/nginx/configuration-reference.md").read_text(
            encoding="utf-8"
        )
        reference_de = (
            ROOT / "examples/nginx/configuration-reference.de.md"
        ).read_text(encoding="utf-8")

        for configuration in (safe, strict, smoke):
            self.assertNotIn("modsecurity_phase4_log ", configuration)
        self.assertIn("registered but always rejected path", reference)
        self.assertIn("registrierter, aber immer abgelehnter Pfad", reference_de)
        self.assertIn("Policy A rejects remote-rule configuration", reference)
        self.assertIn("Policy A weist Remote-Rule-Konfiguration ab", reference_de)
        self.assertNotIn("Passes the key/URL pair to libmodsecurity", reference)
        self.assertNotIn(
            "Übergibt das Schlüssel-/URL-Paar an den Remote-Regel-Loader",
            reference_de,
        )


if __name__ == "__main__":
    unittest.main()
