"""Contracts for the separately built native NGINX response-buffer fixture.

These checks protect fixture wiring only. The native runner is the behavioral
proof because it builds a dedicated test binary and traverses the real NGINX
filter chain.
"""

from __future__ import annotations

import ast
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "nginx_body_buffer_fixture"
MODULE = FIXTURE / "ngx_http_body_buffer_fixture_module.c"
RUNNER = ROOT / "tests" / "run_nginx_body_buffer_fixture.py"


def load_runner():
    specification = importlib.util.spec_from_file_location("nginx_body_fixture_runner", RUNNER)
    if specification is None or specification.loader is None:
        raise RuntimeError("unable to load native fixture runner")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


RUNNER_MODULE = load_runner()


class NginxBodyBufferFixtureContractTest(unittest.TestCase):
    def test_fixture_configuration_keeps_the_test_module_separate(self) -> None:
        config = (FIXTURE / "config").read_text(encoding="utf-8")
        self.assertIn("ngx_http_body_buffer_fixture_module", config)
        self.assertIn("ngx_http_body_buffer_fixture_module.c", config)
        self.assertIn("ngx_module_type=HTTP_FILTER", config)
        self.assertIn("HTTP_FILTER_MODULES", config)
        self.assertIn("ngx_http_modsecurity_module", config)
        self.assertNotIn("connectors/nginx/src", config)

    def test_native_module_emits_each_required_real_buffer_state(self) -> None:
        source = MODULE.read_text(encoding="utf-8")
        for mode in (
            "memory-within",
            "memory-over-limit",
            "file-within",
            "file-over-limit",
            "mixed-within",
            "mixed-over-limit",
            "invalid-metadata",
            "missing-source",
            "read-error",
            "short-read",
            "allocation-failure",
        ):
            self.assertIn(f'"{mode}"', source)
        self.assertIn("buffer->memory = 1", source)
        self.assertIn("buffer->in_file = 1", source)
        self.assertIn("buffer->last_buf = 1", source)
        self.assertIn("buffer->last_in_chain = 1", source)
        self.assertIn("ngx_http_output_filter(r, &output)", source)
        self.assertIn("ngx_http_body_buffer_fixture_body_filter", source)
        self.assertIn("ngx_http_body_buffer_fixture_next_body_filter", source)
        self.assertIn("ngx_http_body_buffer_fixture_init", source)
        self.assertIn("body-buffer-fixture mode=%V", source)
        self.assertIn("body_buffer_fixture_short_file", source)
        self.assertIn("body_buffer_fixture_mixed_file", source)
        self.assertIn("file_length = (off_t) FIXTURE_BODY_LENGTH", source)

    def test_runner_rebuilds_exact_head_modules_and_checks_forwarding(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        ast.parse(source, filename=str(RUNNER))
        self.assertIn("assert_exact_checkout", source)
        self.assertIn("fixture requires a clean exact checkout", source)
        self.assertIn("pwd.getpwuid(os.geteuid())", source)
        self.assertIn('f"user {nginx_user} {nginx_group};"', source)
        self.assertIn("--add-module=", source)
        self.assertNotIn("--add-dynamic-module=", source)
        self.assertIn("--with-ld-opt=-Wl,--wrap=ngx_pnalloc", source)
        self.assertIn("connectors' / 'nginx", source)
        self.assertIn("nginx_body_buffer_fixture", source)
        self.assertNotIn("ngx_http_modsecurity_module.so", source)
        self.assertIn('elif body != b""', source)
        self.assertIn("short_body_file", source)
        self.assertIn("mixed_body_file", source)
        self.assertIn("positive_phase4_event_accounting", source)
        self.assertIn('row.get("rule_id") != "1250001"', source)
        self.assertIn('row.get("body_bytes_seen")', source)
        self.assertIn('row.get("eos_seen") is not True', source)
        self.assertIn("phase4_event_log_sha256", source)
        self.assertIn("require_static_fixture_filter_order", source)
        self.assertIn("connector_then_fixture_then_postpone", source)
        self.assertIn("not_representable_on_this_64_bit_off_t_size_t_runtime", source)

    def test_allocation_fault_is_static_fixture_only(self) -> None:
        source = MODULE.read_text(encoding="utf-8")
        self.assertIn("ngx_http_body_buffer_fixture_fail_allocation", source)
        self.assertIn("ngx_http_body_buffer_fixture_allocation_wrapper_hits", source)
        self.assertIn("volatile sig_atomic_t", source)
        self.assertIn("size == 32768U", source)
        self.assertIn("__wrap_ngx_pnalloc", source)
        self.assertIn("__real_ngx_pnalloc", source)
        self.assertNotIn("setenv(", source)
        self.assertNotIn("getenv(", source)
        runner = RUNNER.read_text(encoding="utf-8")
        self.assertNotIn("LD_PRELOAD", runner)
        self.assertIn(
            "test_only_static_ngx_pnalloc_wrap_32768_byte_scratch",
            runner,
        )
        self.assertIn("allocation-wrapper-hits=1", runner)
        product = (ROOT / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_body_filter.c").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("MSCONNECTOR_NGINX_BODY_FIXTURE_FAIL_ALLOC", product)

    def test_positive_event_accounting_is_retained_with_the_rule_binding(self) -> None:
        events = [
            {
                "uri": path,
                "rule_id": "1250001",
                "body_bytes_seen": RUNNER_MODULE.FIXTURE_LIMIT,
                "body_bytes_inspected": RUNNER_MODULE.FIXTURE_LIMIT,
                "body_truncated": False,
                "truncated": False,
                "eos_seen": True,
            }
            for path in ("/memory-within", "/file-within", "/mixed-within")
        ]
        retained = RUNNER_MODULE.validate_positive_events(events)
        self.assertEqual(set(retained), {"/memory-within", "/file-within", "/mixed-within"})
        self.assertEqual(retained["/mixed-within"]["rule_id"], "1250001")
        self.assertEqual(retained["/file-within"]["body_bytes_seen"], RUNNER_MODULE.FIXTURE_LIMIT)

    def test_positive_event_accounting_rejects_a_mixed_file_backing_match_gap(self) -> None:
        events = [
            {
                "uri": path,
                "rule_id": "1250001" if path != "/mixed-within" else "",
                "body_bytes_seen": RUNNER_MODULE.FIXTURE_LIMIT,
                "body_bytes_inspected": RUNNER_MODULE.FIXTURE_LIMIT,
                "body_truncated": False,
                "truncated": False,
                "eos_seen": True,
            }
            for path in ("/memory-within", "/file-within", "/mixed-within")
        ]
        with self.assertRaises(RUNNER_MODULE.FixtureFailure):
            RUNNER_MODULE.validate_positive_events(events)


if __name__ == "__main__":
    unittest.main()
