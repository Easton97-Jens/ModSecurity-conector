from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[3]
CONNECTOR = REPO_ROOT / "connectors" / "lighttpd"
PATCH = CONNECTOR / "patches" / "0001-lighttpd-1.4.84-msconnector-stream-hooks.patch"


class PatchedHostContractTest(unittest.TestCase):
    def test_patch_uses_a_file_scope_compile_time_size_check(self) -> None:
        patch = PATCH.read_text(encoding="utf-8")
        self.assertNotIn("ck_static_assert", patch)
        self.assertIn("plugin_fn_request_body_data_must_match_plugin_fn_data", patch)
        self.assertIn("plugin_fn_response_body_data_must_match_plugin_fn_data", patch)

    def test_patched_core_and_host_targets_are_separate_from_no_crs(self) -> None:
        makefile = (CONNECTOR / "Makefile").read_text(encoding="utf-8")
        self.assertIn("build-lighttpd-patched-core", makefile)
        self.assertIn("build-lighttpd-patched-host", makefile)
        self.assertIn("check-lighttpd-patched-host", makefile)
        self.assertIn("runtime-smoke-lighttpd-patched", makefile)

        patched_target = makefile.split("runtime-smoke-lighttpd-patched:", 1)[1].split(
            "\n\n", 1
        )[0]
        self.assertNotIn("MSCONNECTOR_NO_CRS_BASELINE", patched_target)

    def test_patched_build_contract_stages_a_verified_core_and_module(self) -> None:
        core = (CONNECTOR / "build" / "build_patched_core.sh").read_text(encoding="utf-8")
        host = (CONNECTOR / "build" / "build_patched_host.sh").read_text(encoding="utf-8")
        check = (CONNECTOR / "harness" / "check_patched_lifecycle_host.sh").read_text(
            encoding="utf-8"
        )

        for required in (
            "AC_INIT([lighttpd],[1.4.84]",
            "configure",
            '"$MAKE_BIN" -C "$CORE_BUILD_DIR" -j "$MAKE_JOBS"',
            '"$MAKE_BIN" -C "$CORE_BUILD_DIR" install',
            "plugins_call_handle_request_body",
            "plugins_call_handle_response_body",
            "patched-core-build-info.txt",
        ):
            self.assertIn(required, core)
        self.assertIn("LIGHTTPD_MSCONNECTOR_CORE_MODE=patched", host)
        self.assertIn("LIGHTTPD_MODULE_DIR=\"$MODULE_DIR\"", host)
        self.assertIn("patched-host-build-info.txt", host)
        self.assertIn("module_sha256", check)
        self.assertIn("core_binary_sha256", check)

    def test_patched_config_refuses_wire_bytes_as_response_body_input(self) -> None:
        preparer = CONNECTOR / "harness" / "prepare_patched_lifecycle_smoke.sh"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "lighttpd-core-patched" / "lighttpd-1.4.84" / "src"
            source.mkdir(parents=True)
            (source / "plugin.h").write_text(
                "#define LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION 1\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment.update(
                {
                    "BUILD_ROOT": str(root),
                    "LIGHTTPD_PATCHED_ROOT": str(root / "lighttpd-core-patched"),
                    "LIGHTTPD_PATCHED_RESPONSE_BODY_MODE": "streaming",
                }
            )
            result = subprocess.run(
                ["sh", str(preparer)],
                cwd=REPO_ROOT,
                env=environment,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        self.assertEqual(77, result.returncode)
        self.assertIn("wire bytes, not decoded entities", result.stderr)

    def test_response_callback_is_an_explicit_noop_not_phase4_processing(self) -> None:
        module = (CONNECTOR / "module" / "mod_msconnector.c").read_text(encoding="utf-8")
        callback = module.rsplit("static plugin_body_hook_result mod_msconnector_handle_response_body", 1)[1].split(
            "#endif", 1
        )[0]
        self.assertIn("HTTP/1.x socket-write stage", callback)
        self.assertIn("never turn wire ranges or EOS into Phase", callback)
        self.assertNotIn("msconnector_runtime_transaction_append_response_body_chunk", callback)
        self.assertNotIn("msconnector_runtime_transaction_finish_response_body", callback)
        self.assertIn("mod_msconnector_finish_uninspected_response_body", module)
        self.assertIn("response_body_mode=none", module)
        self.assertIn("never calls libmodsecurity's", module)

    def test_unobserved_response_lifecycle_closes_only_at_host_reset(self) -> None:
        module = (CONNECTOR / "module" / "mod_msconnector.c").read_text(
            encoding="utf-8"
        )
        response_start = module.split(
            "REQUEST_FUNC(mod_msconnector_handle_response_start)", 1
        )[1].split("REQUEST_FUNC(mod_msconnector_handle_request_reset)", 1)[0]
        request_reset = module.split(
            "REQUEST_FUNC(mod_msconnector_handle_request_reset)", 1
        )[1]
        self.assertNotIn("mod_msconnector_finish_uninspected_response_body", response_start)
        self.assertIn(
            "mod_msconnector_finish_uninspected_response_body(r, ctx)", request_reset
        )
        self.assertIn(
            "msconnector_runtime_transaction_finish_unobserved_response_body",
            module,
        )
        self.assertNotIn(
            "msconnector_runtime_transaction_finish_response_body", module
        )

    def test_request_body_mapper_uses_an_unsigned_size_bound(self) -> None:
        mapper = (CONNECTOR / "src" / "lighttpd_modsecurity_mapper.c").read_text(
            encoding="utf-8"
        )
        self.assertIn("(uintmax_t)take > (uintmax_t)SIZE_MAX", mapper)
        self.assertNotIn("take > (off_t)SIZE_MAX", mapper)

    def test_disruptive_host_action_is_recorded_after_status_selection(self) -> None:
        module = (CONNECTOR / "module" / "mod_msconnector.c").read_text(
            encoding="utf-8"
        )
        action = module.split("static handler_t mod_msconnector_apply_decision", 1)[1].split(
            "#ifdef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION", 1
        )[0]
        self.assertIn("result = http_status_set_err(r, status);", action)
        self.assertIn("msconnector_runtime_transaction_record_host_action", action)
        self.assertLess(
            action.index("result = http_status_set_err(r, status);"),
            action.index("msconnector_runtime_transaction_record_host_action"),
        )
        self.assertIn("MSCONNECTOR_DECISION_ACTION_DENY", action)
        self.assertIn('"http_status"', action)

    def test_patched_runtime_labels_raw_events_with_its_selected_host_path(self) -> None:
        module = (CONNECTOR / "module" / "mod_msconnector.c").read_text(
            encoding="utf-8"
        )
        self.assertIn("msconnector_runtime_set_event_integration_mode", module)
        self.assertIn('"patched-native-lighttpd"', module)

    def test_host_transaction_identifier_uses_a_process_local_serial(self) -> None:
        module = (CONNECTOR / "module" / "mod_msconnector.c").read_text(
            encoding="utf-8"
        )
        self.assertIn("unsigned long host_transaction_counter;", module)
        factory = module.split("static handler_ctx *handler_ctx_create", 1)[1].split(
            "static void handler_ctx_destroy", 1
        )[0]
        self.assertIn("++p->host_transaction_counter;", factory)
        self.assertIn('"lighttpd-%ld-%lu"', factory)
        self.assertNotIn('"lighttpd-%ld-%d-%u-%u"', factory)


if __name__ == "__main__":
    unittest.main()
