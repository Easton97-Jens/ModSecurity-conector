"""Compiled regression for the unsupported SPOP response-body timeout."""

from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SOURCE = (
    ROOT / "connectors" / "haproxy" / "src" / "haproxy_spop_diagnostic_runtime.c"
)


class HAProxySPOPResponseTimeoutContractTests(unittest.TestCase):
    """Reject an unenforceable timeout while preserving the zero default."""

    def test_config_and_cli_nonzero_timeout_are_rejected(self) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("requires a C compiler")

        harness_source = r'''
#define main haproxy_spop_diagnostic_runtime_program_main
#include "__RUNTIME_SOURCE__"
#undef main

#include <assert.h>

int main(void) {
    agent_config config;
    char *cli_rejected[] = {"runtime", "--response-body-timeout", "25"};
    char *cli_zero[] = {"runtime", "--response-body-timeout", "0"};
    char *cli_invalid[] = {"runtime", "--response-body-timeout", "not-a-number"};

    config_init(&config);
    assert(config_set(&config, "response-body-timeout", "0") == 0);
    assert(config.response_body_timeout_ms == 0U);

    config_init(&config);
    assert(config_set(&config, "response-body-timeout", "25") != 0);

    config_init(&config);
    assert(config_set(&config, "response-body-timeout", "not-a-number") != 0);

    config_init(&config);
    assert(config_set(&config, "response-body-timeout", "-1") != 0);

    config_init(&config);
    assert(parse_production_options(&config, 3, cli_rejected) != 0);

    config_init(&config);
    assert(parse_production_options(&config, 3, cli_zero) == 0);
    assert(config.response_body_timeout_ms == 0U);

    config_init(&config);
    assert(parse_production_options(&config, 3, cli_invalid) != 0);

    {
        FILE *config_file = fopen("__CONFIG_FILE__", "w");
        assert(config_file != NULL);
        assert(fputs("response-body-timeout=25\n", config_file) >= 0);
        assert(fclose(config_file) == 0);
    }
    config_init(&config);
    assert(load_config_file(&config, "__CONFIG_FILE__") != 0);

    config_init(&config);
    assert(config_set(&config, "response-body-limit", "1") == 0);
    assert(config.response_phases_enabled == 1);
    assert(production_config_has_supported_response_phases(&config) == 0);

    config_init(&config);
    assert(config_set(&config, "enable-response-headers", "true") == 0);
    assert(config.response_phases_enabled == 1);
    assert(production_config_has_supported_response_phases(&config) == 0);

    config_init(&config);
    assert(config_set(&config, "response-phases", "on") == 0);
    assert(config.response_phases_enabled == 1);
    assert(production_config_has_supported_response_phases(&config) == 0);

    {
        char *cli_response_limit[] = {"runtime", "--response-body-limit", "1"};
        char *cli_response_headers[] = {"runtime", "--enable-response-headers"};
        char *cli_response_phases[] = {"runtime", "--response-phases", "true"};

        config_init(&config);
        assert(parse_production_options(&config, 3, cli_response_limit) == 0);
        assert(production_config_has_supported_response_phases(&config) == 0);

        config_init(&config);
        assert(parse_production_options(&config, 2, cli_response_headers) == 0);
        assert(production_config_has_supported_response_phases(&config) == 0);

        config_init(&config);
        assert(parse_production_options(&config, 3, cli_response_phases) == 0);
        assert(production_config_has_supported_response_phases(&config) == 0);
    }

    config_init(&config);
    assert(config.response_body_limit == 0U);
    assert(config.response_phases_enabled == 0);
    assert(production_config_has_safe_peer_limits(&config) == 0);
    config.port = 1U;
    assert(production_config_has_safe_peer_limits(&config) == 1);
    assert(production_config_has_supported_response_phases(&config) == 1);

    {
        FILE *config_file = fopen("CONFIG_FILE_PLACEHOLDER", "w");
        assert(config_file != NULL);
        assert(fputs("response-body-limit=1\n", config_file) >= 0);
        assert(fclose(config_file) == 0);
    }
    config_init(&config);
    assert(load_config_file(&config, "CONFIG_FILE_PLACEHOLDER") == 0);
    assert(production_config_has_supported_response_phases(&config) == 0);
    return 0;
}
'''.replace("__RUNTIME_SOURCE__", RUNTIME_SOURCE.as_posix()).replace(
            "__CONFIG_FILE__", "CONFIG_FILE_PLACEHOLDER"
        )

        with tempfile.TemporaryDirectory(
            prefix="haproxy-spop-response-timeout-",
            dir=os.environ.get("TMPDIR"),
        ) as temporary_directory:
            temporary_root = Path(temporary_directory)
            harness = temporary_root / "response_timeout_contract.c"
            binary = temporary_root / "response_timeout_contract"
            harness.write_text(
                harness_source.replace("CONFIG_FILE_PLACEHOLDER", str(temporary_root / "invalid.conf")),
                encoding="utf-8",
            )
            compile_result = subprocess.run(
                [
                    compiler,
                    "-std=c17",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    "-ffunction-sections",
                    "-fdata-sections",
                    "-I",
                    str(ROOT / "common" / "include"),
                    "-I",
                    str(ROOT / "connectors" / "haproxy" / "src"),
                    str(harness),
                    "-Wl,--gc-sections",
                    "-Wl,--unresolved-symbols=ignore-all",
                    "-o",
                    str(binary),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(compile_result.returncode, 0, compile_result.stderr)

            run_result = subprocess.run(
                [str(binary)],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr)
            self.assertGreaterEqual(
            run_result.stderr.count("response-body-timeout=25 is unsupported"),
            2,
        )
            self.assertIn("response-body-timeout=not-a-number is invalid", run_result.stderr)

    def test_production_entry_point_rejects_response_phases_before_server_start(self) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("requires a C compiler")

        harness_source = r'''
#define main haproxy_spop_diagnostic_runtime_program_main
#include "__RUNTIME_SOURCE__"
#undef main

#include <assert.h>

int main(void) {
    char *response_limit[] = {
        "runtime", "--port", "1", "--rules-file", "/dev/null",
        "--response-body-limit", "1"
    };
    char *response_headers[] = {
        "runtime", "--port", "1", "--rules-file", "/dev/null",
        "--enable-response-headers"
    };
    char *response_phases[] = {
        "runtime", "--port", "1", "--rules-file", "/dev/null",
        "--response-phases", "true"
    };
    char *config_file[] = {
        "runtime", "--config", "CONFIG_FILE_PLACEHOLDER",
        "--port", "1", "--rules-file", "/dev/null"
    };

    /* Every response-phase form must fail before run_agent_server(). */
    assert(run_production_agent_command(
        (int)(sizeof(response_limit) / sizeof(response_limit[0])), response_limit) == 2);
    assert(run_production_agent_command(
        (int)(sizeof(response_headers) / sizeof(response_headers[0])), response_headers) == 2);
    assert(run_production_agent_command(
        (int)(sizeof(response_phases) / sizeof(response_phases[0])), response_phases) == 2);
    assert(run_production_agent_command(
        (int)(sizeof(config_file) / sizeof(config_file[0])), config_file) == 2);
    return 0;
}
'''.replace("__RUNTIME_SOURCE__", RUNTIME_SOURCE.as_posix()).replace(
            "CONFIG_FILE_PLACEHOLDER", "CONFIG_FILE_PLACEHOLDER"
        )

        with tempfile.TemporaryDirectory(
            prefix="haproxy-spop-production-gate-",
            dir=os.environ.get("TMPDIR"),
        ) as temporary_directory:
            temporary_root = Path(temporary_directory)
            config_path = temporary_root / "response-limit.conf"
            config_path.write_text("response-body-limit=1\n", encoding="utf-8")
            harness = temporary_root / "production_gate_contract.c"
            binary = temporary_root / "production_gate_contract"
            harness.write_text(
                harness_source.replace("CONFIG_FILE_PLACEHOLDER", config_path.as_posix()),
                encoding="utf-8",
            )
            compile_result = subprocess.run(
                [
                    compiler,
                    "-std=c17",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    "-ffunction-sections",
                    "-fdata-sections",
                    "-I",
                    str(ROOT / "common" / "include"),
                    "-I",
                    str(ROOT / "connectors" / "haproxy" / "src"),
                    str(harness),
                    "-Wl,--gc-sections",
                    "-Wl,--unresolved-symbols=ignore-all",
                    "-o",
                    str(binary),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(compile_result.returncode, 0, compile_result.stderr)

            run_result = subprocess.run(
                [str(binary)],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr)
            self.assertGreaterEqual(
                run_result.stderr.count("startup rejected fail-closed"), 4
            )

    def test_disabled_response_notify_is_rejected_before_transaction_processing(self) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("requires a C compiler")

        harness_source = r'''
#define main haproxy_spop_diagnostic_runtime_program_main
#include "__RUNTIME_SOURCE__"
#undef main

#include <assert.h>
#include <sys/socket.h>
#include <unistd.h>

int main(void) {
    agent_state state;
    notify_request request;
    spop_frame frame;
    spop_frame ack;
    spop_buffer ack_payload;
    FILE *log = fopen("guard.log", "w+");
    int sockets[2];
    char log_text[2048];
    size_t log_len;

    assert(log != NULL);
    assert(socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) == 0);
    memset(&state, 0, sizeof(state));
    config_init(&state.config);
    state.config.response_phases_enabled = 0;
    state.engine = (haproxy_modsecurity_engine *)0x1;
    state.log = log;
    memset(&request, 0, sizeof(request));
    strcpy(request.message_name, "check-response");
    strcpy(request.request_id, "peer-response");
    request.has_request_id = 1;
    request.is_response = 1;
    memset(&frame, 0, sizeof(frame));
    frame.stream_id = 7;
    frame.frame_id = 9;

    /* A response-typed peer frame must be rejected before the fake engine is
     * touched, while the peer still receives a protocol ACK. */
    assert(process_production_notify(sockets[0], &frame, &state, log,
        &request) == 0);
    assert(recv_frame(sockets[1], &ack) == 0);
    assert(ack.type == SPOP_FRM_ACK);
    ack_payload.len = ack.payload_len;
    memcpy(ack_payload.data, ack.payload, ack.payload_len);
    assert(payload_has_set_var_blocked_true(&ack_payload));
    assert(state.transactions == NULL);

    assert(fseek(log, 0, SEEK_SET) == 0);
    log_len = fread(log_text, 1, sizeof(log_text) - 1U, log);
    log_text[log_len] = '\0';
    assert(strstr(log_text, "event=response-phase-disabled") != NULL);
    assert(strstr(log_text, "outcome=fail-closed") != NULL);
    assert(strstr(log_text, "transaction=not-consumed") != NULL);

    fclose(log);
    close(sockets[0]);
    close(sockets[1]);
    return 0;
}
'''.replace("__RUNTIME_SOURCE__", RUNTIME_SOURCE.as_posix())

        with tempfile.TemporaryDirectory(
            prefix="haproxy-spop-response-phase-guard-",
            dir=os.environ.get("TMPDIR"),
        ) as temporary_directory:
            temporary_root = Path(temporary_directory)
            harness = temporary_root / "response_phase_guard_contract.c"
            binary = temporary_root / "response_phase_guard_contract"
            harness.write_text(harness_source, encoding="utf-8")
            compile_result = subprocess.run(
                [
                    compiler,
                    "-std=c17",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    "-ffunction-sections",
                    "-fdata-sections",
                    "-I",
                    str(ROOT / "common" / "include"),
                    "-I",
                    str(ROOT / "connectors" / "haproxy" / "src"),
                    str(harness),
                    "-Wl,--gc-sections",
                    "-Wl,--unresolved-symbols=ignore-all",
                    "-o",
                    str(binary),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(compile_result.returncode, 0, compile_result.stderr)
            run_result = subprocess.run(
                [str(binary)],
                cwd=temporary_root,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr)

    def test_mixed_response_then_request_notify_remains_response_typed(self) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("requires a C compiler")

        harness_source = r'''
#define main haproxy_spop_diagnostic_runtime_program_main
#include "__RUNTIME_SOURCE__"
#undef main

#include <assert.h>
#include <sys/socket.h>
#include <unistd.h>

int main(void) {
    agent_state state;
    notify_request request;
    spop_frame frame;
    spop_frame ack;
    spop_buffer payload;
    spop_buffer ack_payload;
    FILE *log = fopen("mixed.log", "w+");
    int sockets[2];

    assert(log != NULL);
    assert(socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) == 0);
    memset(&state, 0, sizeof(state));
    config_init(&state.config);
    state.config.response_phases_enabled = 0;
    state.engine = (haproxy_modsecurity_engine *)0x1;
    state.log = log;

    /* A response message followed by a request message is one payload. */
    payload.len = 0;
    assert(append_string(&payload, "check-response") == 0);
    assert(append_byte(&payload, 0U) == 0);
    assert(append_string(&payload, "check-request") == 0);
    assert(append_byte(&payload, 0U) == 0);
    memset(&frame, 0, sizeof(frame));
    frame.stream_id = 11;
    frame.frame_id = 13;
    frame.payload_len = payload.len;
    memcpy(frame.payload, payload.data, payload.len);

    assert(parse_notify_payload(frame.payload, frame.payload_len, &request) == 0);
    assert(request.is_response == 1);
    assert(request.is_response_body == 0);
    assert(process_production_notify(sockets[0], &frame, &state, log,
        &request) == 0);
    assert(recv_frame(sockets[1], &ack) == 0);
    assert(ack.type == SPOP_FRM_ACK);
    ack_payload.len = ack.payload_len;
    memcpy(ack_payload.data, ack.payload, ack.payload_len);
    assert(payload_has_set_var_blocked_true(&ack_payload));
    assert(state.transactions == NULL);
    free_notify_request(&request);

    /* A normal request-only payload still reaches the ordinary request path. */
    payload.len = 0;
    assert(append_string(&payload, "check-request") == 0);
    assert(append_byte(&payload, 0U) == 0);
    frame.payload_len = payload.len;
    memcpy(frame.payload, payload.data, payload.len);
    memset(&request, 0, sizeof(request));
    assert(parse_notify_payload(frame.payload, frame.payload_len, &request) == 0);
    assert(request.is_response == 0);
    /* The ordinary request classification remains unchanged.  The engine
     * path itself is covered by the existing request/decision contracts; this
     * focused control avoids substituting an invalid fake engine pointer. */
    free_notify_request(&request);

    fclose(log);
    close(sockets[0]);
    close(sockets[1]);
    return 0;
}
'''.replace("__RUNTIME_SOURCE__", RUNTIME_SOURCE.as_posix())

        with tempfile.TemporaryDirectory(
            prefix="haproxy-spop-mixed-notify-",
            dir=os.environ.get("TMPDIR"),
        ) as temporary_directory:
            temporary_root = Path(temporary_directory)
            harness = temporary_root / "mixed_notify_contract.c"
            binary = temporary_root / "mixed_notify_contract"
            harness.write_text(harness_source, encoding="utf-8")
            compile_result = subprocess.run(
                [
                    compiler,
                    "-std=c17",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    "-ffunction-sections",
                    "-fdata-sections",
                    "-I",
                    str(ROOT / "common" / "include"),
                    "-I",
                    str(ROOT / "connectors" / "haproxy" / "src"),
                    str(harness),
                    "-Wl,--gc-sections",
                    "-Wl,--unresolved-symbols=ignore-all",
                    "-o",
                    str(binary),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(compile_result.returncode, 0, compile_result.stderr)
            run_result = subprocess.run(
                [str(binary)],
                cwd=temporary_root,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr)

    def test_empty_notify_payload_is_rejected_before_default_request_processing(self) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("requires a C compiler")

        harness_source = r'''
#define main haproxy_spop_diagnostic_runtime_program_main
#include "__RUNTIME_SOURCE__"
#undef main

#include <assert.h>

int main(void) {
    notify_request request;
    unsigned char malformed[] = {SPOP_DATA_STR};
    unsigned char normal[] = {13, 'c', 'h', 'e', 'c', 'k', '-', 'r', 'e', 'q', 'u', 'e', 's', 't', 0};

    memset(&request, 0xA5, sizeof(request));
    assert(parse_notify_payload(NULL, 0U, &request) != 0);
    assert(request.has_notify == 0);
    assert(request.is_response == 0);
    assert(request.message_name[0] == '\0');

    /* A nonempty malformed payload remains malformed. */
    memset(&request, 0xA5, sizeof(request));
    assert(parse_notify_payload(malformed, sizeof(malformed), &request) != 0);
    assert(request.has_notify == 0);

    /* A normal request message remains a valid request classification. */
    memset(&request, 0, sizeof(request));
    assert(parse_notify_payload(normal, sizeof(normal), &request) == 0);
    assert(request.has_notify == 1);
    assert(request.is_response == 0);
    assert(strcmp(request.message_name, "check-request") == 0);
    free_notify_request(&request);
    return 0;
}
'''.replace("__RUNTIME_SOURCE__", RUNTIME_SOURCE.as_posix())

        with tempfile.TemporaryDirectory(
            prefix="haproxy-spop-empty-notify-",
            dir=os.environ.get("TMPDIR"),
        ) as temporary_directory:
            temporary_root = Path(temporary_directory)
            harness = temporary_root / "empty_notify_contract.c"
            binary = temporary_root / "empty_notify_contract"
            harness.write_text(harness_source, encoding="utf-8")
            compile_result = subprocess.run(
                [
                    compiler,
                    "-std=c17",
                    "-Wall",
                    "-Wextra",
                    "-Werror",
                    "-ffunction-sections",
                    "-fdata-sections",
                    "-I",
                    str(ROOT / "common" / "include"),
                    "-I",
                    str(ROOT / "connectors" / "haproxy" / "src"),
                    str(harness),
                    "-Wl,--gc-sections",
                    "-Wl,--unresolved-symbols=ignore-all",
                    "-o",
                    str(binary),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(compile_result.returncode, 0, compile_result.stderr)
            run_result = subprocess.run(
                [str(binary)],
                cwd=temporary_root,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr)


if __name__ == "__main__":
    unittest.main()
