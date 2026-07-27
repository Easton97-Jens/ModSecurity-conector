#!/usr/bin/env python3
"""Focused source contracts for current Sonar reliability repairs."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SonarReliabilityContractTests(unittest.TestCase):
    def test_traefik_result_payload_never_copies_a_null_optional_field(self) -> None:
        source = (
            ROOT / "connectors" / "traefik" / "src" / "traefik_engine_service.c"
        ).read_text(encoding="utf-8")
        self.assertIn("transaction_id != NULL && transaction_id_size > 0U", source)
        self.assertIn("rule_id != NULL && rule_id_size > 0U", source)
        self.assertIn("redirect != NULL && redirect_size > 0U", source)

    def test_authorization_listener_initializes_peer_and_local_socket_state(self) -> None:
        source = (
            ROOT / "common" / "runtime" / "http_authorization_service.c"
        ).read_text(encoding="utf-8")
        self.assertIn("struct sockaddr_in local = {0};", source)
        self.assertIn("struct sockaddr_in peer = {0};", source)

    def test_traefik_runtime_lock_pairs_keep_stable_service_references(self) -> None:
        source = (
            ROOT / "connectors" / "traefik" / "src" / "traefik_engine_service.c"
        ).read_text(encoding="utf-8")
        destroy_start = source.index("static void traefik_engine_session_destroy")
        destroy_end = source.index(
            "\n}\n\nstatic int traefik_engine_handle_begin", destroy_start
        )
        destroy = source[destroy_start:destroy_end]
        begin_start = destroy_end
        begin_end = source.index(
            "\n}\n\nstatic int traefik_engine_handle_request_chunk", begin_start
        )
        begin = source[begin_start:begin_end]

        self.assertNotIn("traefik_engine_lock_runtime", source)
        self.assertNotIn("traefik_engine_unlock_runtime", source)
        self.assertIn("traefik_engine_service *service;", destroy)
        self.assertIn("service = session->service;", destroy)
        self.assertIn("pthread_mutex_lock(&service->runtime_lock)", destroy)
        self.assertIn("pthread_mutex_unlock(&service->runtime_lock)", destroy)
        self.assertNotIn("session->service->runtime_lock", destroy)
        self.assertEqual(destroy.count("session->service"), 1)
        self.assertIn("traefik_engine_service *service;", begin)
        self.assertIn("service = session->service;", begin)
        self.assertIn("pthread_mutex_lock(&service->runtime_lock)", begin)
        self.assertIn("pthread_mutex_unlock(&service->runtime_lock)", begin)
        self.assertIn(
            "msconnector_runtime_transaction_begin(service->runtime,", begin
        )
        self.assertNotIn("session->service->runtime_lock", begin)
        self.assertEqual(begin.count("session->service"), 1)

    def test_oracle_handles_a_missing_optional_json_string_without_dereference(self) -> None:
        source = (ROOT / "ci" / "tools" / "native_modsecurity_oracle.c").read_text(
            encoding="utf-8"
        )
        self.assertIn("if (value == NULL)", source)
        self.assertIn('fputs("\\\"\\\"", out);', source)
        self.assertIn("cursor = (const unsigned char *)value;", source)
        self.assertIn("json_string(out, whoami);", source)
        self.assertNotIn('json_string(out, whoami ? whoami : "");', source)

    def test_haproxy_startup_diagnostics_guard_the_standard_error_stream(self) -> None:
        source = (
            ROOT
            / "connectors"
            / "haproxy"
            / "src"
            / "haproxy_spop_diagnostic_runtime.c"
        ).read_text(encoding="utf-8")
        self.assertGreaterEqual(source.count("if (stderr != NULL)"), 2)

    def test_haproxy_append_bytes_checks_the_source_extent_before_copying(self) -> None:
        source = (
            ROOT
            / "connectors"
            / "haproxy"
            / "src"
            / "haproxy_spop_diagnostic_runtime.c"
        ).read_text(encoding="utf-8")
        append_bytes = source[
            source.index("static int append_bytes")
            : source.index("static int append_uint32")
        ]
        self.assertIn(
            "const void *data, size_t data_len, size_t len",
            append_bytes,
        )
        self.assertIn("if (len > data_len ||", append_bytes)
        self.assertLess(append_bytes.index("len > data_len"), append_bytes.index("memcpy("))
        self.assertIn(
            "append_bytes(buf, &net, sizeof(net), sizeof(net))",
            source,
        )
        self.assertNotIn("append_bytes(buf, value, len, len)", source)
        self.assertIn(
            "append_bytes(frame, payload->data, sizeof(payload->data), payload->len)",
            source,
        )

    def test_haproxy_append_string_preflights_payload_before_mutating_the_frame(self) -> None:
        source = (
            ROOT
            / "connectors"
            / "haproxy"
            / "src"
            / "haproxy_spop_diagnostic_runtime.c"
        ).read_text(encoding="utf-8")
        varint_encoded_length = source[
            source.index("static size_t varint_encoded_length")
            : source.index("static int append_varint")
        ]
        append_string = source[
            source.index("static int append_string")
            : source.index("static int append_typed_string")
        ]

        self.assertIn("if (value >= 240U)", varint_encoded_length)
        self.assertIn("value = (value - 240U) >> 4;", varint_encoded_length)
        self.assertIn("while (value >= 128U)", varint_encoded_length)
        self.assertIn("value = (value - 128U) >> 7;", varint_encoded_length)

        self.assertIn(
            "buf == 0 || bounded_cstring_length(value, SPOP_FRAME_MAX, &len) != 0",
            append_string,
        )
        self.assertIn("encoded_len = varint_encoded_length(len);", append_string)
        self.assertIn("remaining = sizeof(buf->data) - buf->len;", append_string)
        capacity_check = "if (encoded_len > remaining || len > remaining - encoded_len)"
        self.assertIn(capacity_check, append_string)
        self.assertLess(
            append_string.index(capacity_check),
            append_string.index("if (append_varint(buf, len) != 0)"),
        )
        self.assertIn("for (size_t index = 0; index < len; ++index)", append_string)
        self.assertIn(
            "append_byte(buf, (unsigned int)(unsigned char)value[index])",
            append_string,
        )
        self.assertNotIn("append_bytes(buf, value, len, len)", append_string)

    def test_haproxy_append_string_runtime_boundaries(self) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("requires a C compiler")

        runtime_source = (
            ROOT
            / "connectors"
            / "haproxy"
            / "src"
            / "haproxy_spop_diagnostic_runtime.c"
        )
        harness_source = r'''
#define main haproxy_spop_diagnostic_runtime_program_main
#include "__RUNTIME_SOURCE__"
#undef main

#include <assert.h>

static void fill_string(char *value, size_t len, char byte) {
    memset(value, byte, len);
    value[len] = '\0';
}

static void test_varint_length_contract(void) {
    spop_buffer buffer;

    for (uint64_t value = 0; value <= SPOP_FRAME_MAX; ++value) {
        buffer.len = 0U;
        assert(append_varint(&buffer, value) == 0);
        assert(buffer.len == varint_encoded_length(value));
    }
}

static void test_varint_boundaries(void) {
    char value_239[240];
    char value_240[241];
    spop_buffer buffer;

    fill_string(value_239, 239U, 'a');
    fill_string(value_240, 240U, 'b');
    memset(&buffer, 0, sizeof(buffer));

    assert(append_string(&buffer, value_239) == 0);
    assert(buffer.len == 240U);
    assert(buffer.data[0] == 239U);
    assert(memcmp(buffer.data + 1U, value_239, 239U) == 0);

    memset(&buffer, 0, sizeof(buffer));
    assert(append_string(&buffer, value_240) == 0);
    assert(buffer.len == 242U);
    assert(buffer.data[0] == 240U);
    assert(buffer.data[1] == 0U);
    assert(memcmp(buffer.data + 2U, value_240, 240U) == 0);
}

static void test_exact_fit_and_overflow_are_atomic(void) {
    char value[240];
    spop_buffer buffer;
    spop_buffer before;
    const size_t exact_offset = SPOP_FRAME_MAX - 240U;

    fill_string(value, 239U, 'c');
    memset(&buffer, 0x5a, sizeof(buffer));
    buffer.len = exact_offset;
    assert(append_string(&buffer, value) == 0);
    assert(buffer.len == SPOP_FRAME_MAX);
    assert(buffer.data[exact_offset] == 239U);
    assert(memcmp(buffer.data + exact_offset + 1U, value, 239U) == 0);

    memset(&buffer, 0x7b, sizeof(buffer));
    buffer.len = SPOP_FRAME_MAX - 239U;
    before = buffer;
    assert(append_string(&buffer, value) == -1);
    assert(memcmp(&buffer, &before, sizeof(buffer)) == 0);
}

static void test_unterminated_input_does_not_mutate(void) {
    char unterminated[SPOP_FRAME_MAX];
    spop_buffer buffer;
    spop_buffer before;

    memset(unterminated, 'u', sizeof(unterminated));
    memset(&buffer, 0x3d, sizeof(buffer));
    buffer.len = 17U;
    before = buffer;
    assert(append_string(&buffer, unterminated) == -1);
    assert(memcmp(&buffer, &before, sizeof(buffer)) == 0);
    assert(append_string(0, "valid") == -1);
}

int main(void) {
    test_varint_length_contract();
    test_varint_boundaries();
    test_exact_fit_and_overflow_are_atomic();
    test_unterminated_input_does_not_mutate();
    return 0;
}
'''.replace("__RUNTIME_SOURCE__", runtime_source.as_posix())
        temporary_parent = os.environ.get("TMPDIR")
        with tempfile.TemporaryDirectory(
            prefix="haproxy-append-string-boundary-", dir=temporary_parent
        ) as temporary_directory:
            temporary_root = Path(temporary_directory)
            harness = temporary_root / "haproxy_append_string_boundaries.c"
            binary = temporary_root / "haproxy_append_string_boundaries"
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


if __name__ == "__main__":
    unittest.main()
