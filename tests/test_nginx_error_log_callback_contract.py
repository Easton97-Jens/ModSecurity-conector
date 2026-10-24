"""Source contract for the native NGINX ModSecurity log callback."""

from pathlib import Path
import unittest

from tests.c_source_contract import function_definition


ROOT = Path(__file__).resolve().parents[1]
LOG_SOURCE = ROOT / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_log.c"


class NginxErrorLogCallbackContractTest(unittest.TestCase):
    def setUp(self) -> None:
        source = LOG_SOURCE.read_text(encoding="utf-8")
        self.callback = function_definition(source, "ngx_http_modsecurity_log")

    def test_callback_guards_null_inputs_and_context(self) -> None:
        self.assertIn("if (log == NULL || data == NULL)", self.callback)
        self.assertIn(
            "if (r == NULL || r->connection == NULL || r->connection->log == NULL)",
            self.callback,
        )
        self.assertIn(
            "if (mcf == NULL)",
            self.callback,
        )

    def test_jsonl_rule_match_precedes_effective_error_log_guard(self) -> None:
        emission = self.callback.index("ngx_http_modsecurity_log_rule_match_event")
        guard = self.callback.index(
            "if (mcf->common_config.use_error_log != MSCONNECTOR_BOOL_ON)"
        )
        host_log = self.callback.index("ngx_log_error(NGX_LOG_INFO")
        self.assertLess(emission, guard)
        self.assertLess(guard, host_log)
        self.assertIn("mcf->common_config.use_error_log", self.callback)

    def test_error_log_setting_does_not_change_waf_callback_processing(self) -> None:
        self.assertIn("ctx->native_event_phase_active", self.callback)
        self.assertIn("msconnector_rule_id_extract_from_message", self.callback)
        self.assertIn("ngx_http_modsecurity_log_rule_match_event(r,", self.callback)


if __name__ == "__main__":
    unittest.main()
