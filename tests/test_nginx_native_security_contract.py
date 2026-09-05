"""Static contracts for NGINX-native request boundary hardening."""

from pathlib import Path
import unittest

from tests.c_source_contract import function_definition


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
BODY_FILTER = (
    ROOT / "connectors/nginx/src/ngx_http_modsecurity_body_filter.c"
).read_text(encoding="utf-8")
COMMON = (ROOT / "connectors/nginx/src/ngx_http_modsecurity_common.h").read_text(
    encoding="utf-8"
)
HARNESS = (ROOT / "connectors/nginx/harness/run_nginx_smoke.sh").read_text(
    encoding="utf-8"
)
EXACT_GATE = (ROOT / "connectors/nginx/harness/run_exact_head_use_error_log.sh").read_text(
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

    def test_native_event_file_configuration_uses_common_private_descriptor(self) -> None:
        setter = MODULE.split("static char *\nngx_conf_set_phase4_log", 1)[1].split(
            "static ngx_int_t", 1
        )[0]

        self.assertIn('return "is duplicate";', setter)
        self.assertIn("ngx_strlchr", setter)
        self.assertIn("msconnector_open_private_event_file(path, &fd)", setter)
        self.assertNotIn("ngx_conf_open_file(", setter)
        self.assertNotIn("ngx_list_push(", setter)
        self.assertIn("generic reopen routine", setter)
        self.assertIn("event_file->fd = NGX_INVALID_FILE", setter)
        self.assertIn("ngx_pool_cleanup_add(cf->pool, 0)", setter)
        self.assertIn(
            "cleanup->handler = ngx_http_modsecurity_cleanup_phase4_log", setter
        )
        self.assertIn("cleanup->handler = NULL", setter)
        self.assertIn("cleanup->data = NULL", setter)
        self.assertIn("ngx_conf_log_error(NGX_LOG_EMERG", setter)
        self.assertIn("event_file->fd = (ngx_fd_t)fd", setter)
        self.assertIn("event_file->name = value[1]", setter)
        self.assertIn("mcf->phase4_log_path = value[1]", setter)
        self.assertIn("mcf->common_config.phase4_log_path = path", setter)
        self.assertLess(
            setter.index("ngx_pool_cleanup_add(cf->pool, 0)"),
            setter.index("msconnector_open_private_event_file(path, &fd)"),
        )
        self.assertLess(
            setter.index("msconnector_open_private_event_file(path, &fd)"),
            setter.index("event_file->fd = (ngx_fd_t)fd"),
        )

    def test_native_event_file_cleanup_invalidates_before_close(self) -> None:
        cleanup = MODULE.split(
            "static void\nngx_http_modsecurity_cleanup_phase4_log", 1
        )[1].split("\n\n\n/* vi:set", 1)[0]

        self.assertIn("event_file->fd == NGX_INVALID_FILE", cleanup)
        self.assertIn("fd = event_file->fd", cleanup)
        self.assertIn("event_file->fd = NGX_INVALID_FILE", cleanup)
        self.assertIn("(void)ngx_close_file(fd)", cleanup)
        self.assertLess(
            cleanup.index("event_file->fd = NGX_INVALID_FILE"),
            cleanup.index("(void)ngx_close_file(fd)"),
        )

    def test_native_event_file_inheritance_borrows_without_new_cleanup(self) -> None:
        merge = MODULE.split("static char *\nngx_http_modsecurity_merge_conf", 1)[1].split(
            "\n\nstatic void\nngx_http_modsecurity_cleanup_instance", 1
        )[0]

        self.assertIn("if (c->phase4_log_file == NGX_CONF_UNSET_PTR)", merge)
        self.assertIn("c->phase4_log_file = p->phase4_log_file", merge)
        self.assertIn("c->phase4_log_path = p->phase4_log_path", merge)
        self.assertIn("c->phase4_log_file = NULL", merge)
        self.assertNotIn("ngx_conf_merge_ptr_value(c->phase4_log_file", merge)

    def test_phase4_event_uses_the_safe_request_metadata_helper(self) -> None:
        phase4_event = function_definition(
            BODY_FILTER, "ngx_http_modsecurity_phase4_log_event"
        )

        self.assertIn(
            "ngx_http_modsecurity_event_request_metadata_t request_metadata;",
            phase4_event,
        )
        self.assertIn(
            "request_metadata = ngx_http_modsecurity_event_request_metadata(r);",
            phase4_event,
        )
        self.assertIn("event.request.method = request_metadata.method;", phase4_event)
        self.assertIn("event.request.uri = request_metadata.uri;", phase4_event)
        self.assertLess(
            phase4_event.index(
                "request_metadata = ngx_http_modsecurity_event_request_metadata(r);"
            ),
            phase4_event.index("event.request.uri = request_metadata.uri;"),
        )

    def test_hosted_phase4_lifecycle_keeps_generic_reopen_outside_the_sink(self) -> None:
        for target_mode in (
            "unsafe_symlink",
            "unsafe_fifo",
            "unsafe_directory",
            "unsafe_writable_parent",
            "unsafe_wrong_owner",
        ):
            self.assertIn(target_mode, HARNESS)
        self.assertIn('"$NGINX_BINARY" -t -p "$RUNTIME_ROOT" -c "$CONFIG_FILE"', HARNESS)
        self.assertIn("nginx-reload-unsafe-phase4-configtest.log", HARNESS)
        self.assertIn('/bin/kill -USR1 "$NGINX_PID"', HARNESS)
        self.assertIn("phase4_fd_count_for_target()", HARNESS)
        self.assertIn("assert_phase4_fd_absent", HARNESS)
        self.assertIn("start_phase4_reload_overlap_client", HARNESS)
        self.assertIn("phase=phase4_reload_overlap", HARNESS)
        self.assertIn("phase=phase4_fd_shutdown result=closed_after_master_exit", HARNESS)
        self.assertIn("phase4_reload_unsafe result=failed_old_cycle_preserved", EXACT_GATE)
        self.assertIn("phase4_reload_secure result=new_validated_fd", EXACT_GATE)
        self.assertIn("phase=phase4_reload_overlap", EXACT_GATE)
        self.assertIn("phase=phase4_fd_shutdown result=closed_after_master_exit", EXACT_GATE)

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

    def test_native_event_file_examples_remain_bounded_and_remote_rules_stay_disabled(self) -> None:
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

        for configuration in (safe, strict):
            self.assertNotIn("modsecurity_phase4_log ", configuration)
        # The pinned Framework fixture supplies the directive through the one
        # location include.  The Parent template must not add a second copy:
        # duplicate directives would open a second owned descriptor.
        self.assertIn('include "@@NGINX_LOCATION_DIRECTIVES@@";', smoke)
        self.assertNotIn("modsecurity_phase4_log", smoke)
        self.assertNotIn("registered but always rejected path", reference)
        self.assertNotIn("registrierter, aber immer abgelehnter Pfad", reference_de)
        self.assertIn("Policy A rejects remote-rule configuration", reference)
        self.assertIn("Policy A weist Remote-Rule-Konfiguration ab", reference_de)
        self.assertNotIn("Passes the key/URL pair to libmodsecurity", reference)
        self.assertNotIn(
            "Übergibt das Schlüssel-/URL-Paar an den Remote-Regel-Loader",
            reference_de,
        )


if __name__ == "__main__":
    unittest.main()
