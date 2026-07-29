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
    def test_traefik_result_payload_uses_fail_closed_bounded_copies(self) -> None:
        source = (
            ROOT / "connectors" / "traefik" / "src" / "traefik_engine_service.c"
        ).read_text(encoding="utf-8")
        send_result = source[source.index("static int traefik_engine_send_result") :]

        helper_start = source.index("static int traefik_engine_copy_bounded_text")
        helper_end = source.index("\n}\n\nstatic uint16_t", helper_start)
        helper = source[helper_start:helper_end]

        self.assertNotIn("traefik_engine_empty_text", source)
        self.assertIn("if (size == 0U)", helper)
        self.assertIn("if (destination == NULL || source == NULL)", helper)
        self.assertIn("for (size_t offset = 0U; offset < size; ++offset)", helper)
        self.assertIn("destination[offset] = (unsigned char)source[offset];", helper)
        for field in ("transaction_id", "rule_id", "redirect"):
            self.assertIn(f"const char *{field} = NULL;", send_result)
            self.assertIn(f"{field}_size", send_result)

        self.assertEqual(send_result.count("traefik_engine_copy_bounded_text("), 3)
        self.assertNotIn("memcpy(payload + offset", send_result)

        self.assertIn("const char *const runtime_transaction_id", send_result)
        self.assertIn("const char *const decision_rule_id", send_result)
        self.assertIn("const char *const decision_redirect", send_result)

    def test_traefik_result_payload_wire_contract_for_optional_text(self) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("requires a C compiler")

        engine_source = (
            ROOT / "connectors" / "traefik" / "src" / "traefik_engine_service.c"
        )
        harness_source = r'''
#define main traefik_engine_service_program_main
#include "__ENGINE_SOURCE__"
#undef main

#include <assert.h>

static const char *test_runtime_transaction_id = NULL;

const char *msconnector_runtime_transaction_id(
    const msconnector_runtime_transaction *transaction)
{
    (void)transaction;
    return test_runtime_transaction_id;
}

static void read_exact(int fd, unsigned char *out, size_t size)
{
    size_t offset = 0U;

    while (offset < size) {
        ssize_t received = recv(fd, out + offset, size - offset, 0);

        assert(received > 0);
        offset += (size_t)received;
    }
}

static void assert_result_frame(int fd, uint8_t command, uint8_t result_code,
    uint8_t action, uint8_t phase, uint16_t status, uint16_t flags,
    const char *transaction_id, const char *rule_id, const char *redirect)
{
    unsigned char header[TRAEFIK_ENGINE_PROTOCOL_HEADER_SIZE];
    unsigned char payload[4096U];
    size_t transaction_id_size = strlen(transaction_id);
    size_t rule_id_size = strlen(rule_id);
    size_t redirect_size = strlen(redirect);
    size_t expected_size = 14U + transaction_id_size + rule_id_size + redirect_size;
    size_t offset = 14U;

    assert(expected_size <= sizeof(payload));
    read_exact(fd, header, sizeof(header));
    assert(memcmp(header, "MSE1", 4U) == 0);
    assert(header[4] == TRAEFIK_ENGINE_PROTOCOL_VERSION);
    assert(header[5] == TRAEFIK_ENGINE_PROTOCOL_RESULT);
    assert(header[6] == 0U && header[7] == 0U);
    assert(traefik_engine_read_u32(header + 8U) == expected_size);
    read_exact(fd, payload, expected_size);
    assert(payload[0] == command);
    assert(payload[1] == result_code);
    assert(payload[2] == action);
    assert(payload[3] == phase);
    assert(traefik_engine_read_u16(payload + 4U) == status);
    assert(traefik_engine_read_u16(payload + 6U) == flags);
    assert(traefik_engine_read_u16(payload + 8U) == transaction_id_size);
    assert(traefik_engine_read_u16(payload + 10U) == rule_id_size);
    assert(traefik_engine_read_u16(payload + 12U) == redirect_size);
    assert(memcmp(payload + offset, transaction_id, transaction_id_size) == 0);
    offset += transaction_id_size;
    assert(memcmp(payload + offset, rule_id, rule_id_size) == 0);
    offset += rule_id_size;
    assert(memcmp(payload + offset, redirect, redirect_size) == 0);
}

int main(void)
{
    int sockets[2];
    traefik_engine_session session;
    msconnector_decision decision;
    unsigned char copy_probe[2U] = {0xa5U, 0x5aU};
    char maximum_transaction_id[TRAEFIK_ENGINE_PROTOCOL_MAX_TRANSACTION_ID + 1U];
    char maximum_rule_id[TRAEFIK_ENGINE_PROTOCOL_MAX_RULE_ID + 1U];
    char maximum_redirect[TRAEFIK_ENGINE_PROTOCOL_MAX_REDIRECT + 1U];

    assert(socketpair(AF_UNIX, SOCK_STREAM, 0, sockets) == 0);
    assert(traefik_engine_copy_bounded_text(copy_probe, NULL, 0U) == 1);
    assert(traefik_engine_copy_bounded_text(copy_probe, NULL, 1U) == 0);
    assert(copy_probe[0] == 0xa5U && copy_probe[1] == 0x5aU);
    memset(&session, 0, sizeof(session));
    session.transaction = (msconnector_runtime_transaction *)(uintptr_t)1U;
    memset(&decision, 0, sizeof(decision));
    test_runtime_transaction_id = NULL;
    assert(traefik_engine_send_result(sockets[0],
        TRAEFIK_ENGINE_PROTOCOL_BEGIN, TRAEFIK_ENGINE_PROTOCOL_RESULT_OK,
        &session, &decision) == 1);
    assert_result_frame(sockets[1], TRAEFIK_ENGINE_PROTOCOL_BEGIN,
        TRAEFIK_ENGINE_PROTOCOL_RESULT_OK, MSCONNECTOR_DECISION_KIND_ALLOW,
        MSCONNECTOR_PHASE_CONNECTION, 0U, 0U, "", "", "");

    test_runtime_transaction_id = "transaction-7";
    memset(&decision, 0, sizeof(decision));
    decision.kind = MSCONNECTOR_DECISION_KIND_REDIRECT;
    decision.phase = MSCONNECTOR_PHASE_RESPONSE_HEADERS;
    decision.http_status = 307;
    decision.rule_id = "942100";
    decision.redirect_url = "https://example.test/blocked";
    decision.disruptive = 1;
    decision.late_intervention = 1;
    assert(traefik_engine_send_result(sockets[0],
        TRAEFIK_ENGINE_PROTOCOL_RESPONSE_HEADERS,
        TRAEFIK_ENGINE_PROTOCOL_RESULT_RUNTIME, &session, &decision) == 1);
    assert_result_frame(sockets[1], TRAEFIK_ENGINE_PROTOCOL_RESPONSE_HEADERS,
        TRAEFIK_ENGINE_PROTOCOL_RESULT_RUNTIME,
        MSCONNECTOR_DECISION_KIND_REDIRECT,
        MSCONNECTOR_PHASE_RESPONSE_HEADERS, 307U,
        TRAEFIK_ENGINE_PROTOCOL_RESULT_DISRUPTIVE |
            TRAEFIK_ENGINE_PROTOCOL_RESULT_LATE,
        "transaction-7", "942100", "https://example.test/blocked");

    memset(maximum_transaction_id, 't',
        TRAEFIK_ENGINE_PROTOCOL_MAX_TRANSACTION_ID);
    maximum_transaction_id[TRAEFIK_ENGINE_PROTOCOL_MAX_TRANSACTION_ID] = '\0';
    memset(maximum_rule_id, 'r', TRAEFIK_ENGINE_PROTOCOL_MAX_RULE_ID);
    maximum_rule_id[TRAEFIK_ENGINE_PROTOCOL_MAX_RULE_ID] = '\0';
    memset(maximum_redirect, 'u', TRAEFIK_ENGINE_PROTOCOL_MAX_REDIRECT);
    maximum_redirect[TRAEFIK_ENGINE_PROTOCOL_MAX_REDIRECT] = '\0';
    test_runtime_transaction_id = maximum_transaction_id;
    decision.rule_id = maximum_rule_id;
    decision.redirect_url = maximum_redirect;
    assert(traefik_engine_send_result(sockets[0],
        TRAEFIK_ENGINE_PROTOCOL_RESPONSE_HEADERS,
        TRAEFIK_ENGINE_PROTOCOL_RESULT_RUNTIME, &session, &decision) == 1);
    assert_result_frame(sockets[1], TRAEFIK_ENGINE_PROTOCOL_RESPONSE_HEADERS,
        TRAEFIK_ENGINE_PROTOCOL_RESULT_RUNTIME,
        MSCONNECTOR_DECISION_KIND_REDIRECT,
        MSCONNECTOR_PHASE_RESPONSE_HEADERS, 307U,
        TRAEFIK_ENGINE_PROTOCOL_RESULT_DISRUPTIVE |
            TRAEFIK_ENGINE_PROTOCOL_RESULT_LATE,
        maximum_transaction_id, maximum_rule_id, maximum_redirect);

    assert(close(sockets[0]) == 0);
    assert(close(sockets[1]) == 0);
    return 0;
}
'''.replace("__ENGINE_SOURCE__", engine_source.as_posix())
        temporary_parent = os.environ.get("TMPDIR")
        with tempfile.TemporaryDirectory(
            prefix="traefik-result-optional-text-", dir=temporary_parent
        ) as temporary_directory:
            temporary_root = Path(temporary_directory)
            harness = temporary_root / "traefik_result_optional_text.c"
            binary = temporary_root / "traefik_result_optional_text"
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
                    str(ROOT),
                    "-I",
                    str(ROOT / "common" / "include"),
                    "-I",
                    str(ROOT / "common" / "runtime"),
                    "-I",
                    str(ROOT / "connectors" / "traefik"),
                    "-I",
                    str(ROOT / "connectors" / "traefik" / "src"),
                    str(harness),
                    "-Wl,--gc-sections",
                    "-pthread",
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

    def test_common_error_descriptions_are_private_and_keyed(self) -> None:
        source = (ROOT / "common" / "src" / "error.c").read_text(encoding="utf-8")
        descriptions = source[
            source.index("const char *msconnector_error_code_name") : source.index(
                "enum msconnector_status msconnector_error_status"
            )
        ]

        self.assertIn("typedef struct msconnector_error_description", source)
        self.assertIn(
            "static const msconnector_error_description msconnector_error_descriptions[]",
            source,
        )
        self.assertIn(
            "msconnector_error_descriptions[index].code == code",
            source,
        )
        self.assertIn("return &msconnector_error_descriptions[index];", source)
        self.assertNotIn("msconnector_error_descriptions[code]", source)
        self.assertNotIn("switch (code)", descriptions)
        self.assertIn("msconnector_error_description_for_code(code)", descriptions)
        self.assertIn("return description->name;", descriptions)
        self.assertIn("return description->default_message;", descriptions)
        self.assertIn('return "internal";', descriptions)
        self.assertIn('return "Internal connector error";', descriptions)

    def test_haproxy_accept_loop_retries_only_interrupted_accepts(self) -> None:
        source = (
            ROOT
            / "connectors"
            / "haproxy"
            / "src"
            / "haproxy_spop_diagnostic_runtime.c"
        ).read_text(encoding="utf-8")
        accept_loop_start = source.index("static int accept_loop(")
        accept_loop_end = source.index(
            "\n}\n\nstatic int client_expect_frame", accept_loop_start
        )
        accept_loop = source[accept_loop_start:accept_loop_end]
        failed_accept_start = accept_loop.index("if (fd < 0) {")
        success_start = accept_loop.index("handle_connection(", failed_accept_start)
        failed_accept = accept_loop[failed_accept_start:success_start]
        terminal_error_start = failed_accept.index("if (errno != EINTR) {")
        interrupted_stop_start = failed_accept.index("if (stop_requested) {")
        terminal_error = failed_accept[
            terminal_error_start:interrupted_stop_start
        ]
        interrupted_accept = failed_accept[interrupted_stop_start:]

        self.assertNotIn("if (errno == EINTR)", failed_accept)
        self.assertIn(
            'log_line(log, "accept failed errno=%d", errno);', terminal_error
        )
        self.assertIn("return 1;", terminal_error)
        self.assertLess(
            terminal_error.index('log_line(log, "accept failed errno=%d", errno);'),
            terminal_error.index("return 1;"),
        )
        self.assertNotIn("if (stop_requested)", terminal_error)
        self.assertIn("break;", interrupted_accept)
        self.assertIn("continue;", interrupted_accept)
        self.assertLess(
            interrupted_accept.index("break;"), interrupted_accept.index("continue;")
        )
        self.assertNotIn("return 1;", interrupted_accept)
        self.assertNotIn("handle_connection(", failed_accept)
        self.assertNotIn("close(fd);", failed_accept)
        self.assertNotIn("handled++;", failed_accept)

        success_path = accept_loop[success_start:]
        self.assertLess(
            success_path.index("handle_connection("), success_path.index("close(fd);")
        )
        self.assertLess(
            success_path.index("close(fd);"), success_path.index("handled++;"),
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

static void test_notify_header_argument(
        const char *argument_name,
        unsigned int type,
        const spop_buffer *headers,
        int expected_response,
        int expected_binary,
        int expected_text,
        unsigned int expected_header_count) {
    spop_buffer argument;
    notify_request request;
    size_t pos = 0U;

    memset(&argument, 0, sizeof(argument));
    memset(&request, 0, sizeof(request));
    assert(append_byte(&argument, type) == 0);
    assert(append_bytes(&argument, headers->data, sizeof(headers->data), headers->len) == 0);
    assert(parse_notify_header_argument(&request,
        (const unsigned char *)argument_name, strlen(argument_name),
        argument.data, argument.len, &pos) == 0);
    assert(pos == argument.len);
    assert(request.header_count == expected_header_count);
    assert(strcmp(request.headers[0].value, "one") == 0);
    if (expected_header_count > 1U) {
        assert(strcmp(request.headers[1].value, "two") == 0);
    }
    assert(request.is_response == expected_response);
    assert(request.has_headers_bin == expected_binary);
    assert(request.has_headers_text == expected_text);
    free_notify_request(&request);
}

static void test_notify_header_arguments_preserve_type_and_response_role(void) {
    spop_buffer header_pairs;
    spop_buffer binary_headers;
    spop_buffer text_headers;

    memset(&header_pairs, 0, sizeof(header_pairs));
    assert(append_string(&header_pairs, "X-One") == 0);
    assert(append_string(&header_pairs, "one") == 0);
    assert(append_string(&header_pairs, "X-Two") == 0);
    assert(append_string(&header_pairs, "two") == 0);
    memset(&binary_headers, 0, sizeof(binary_headers));
    assert(append_varint(&binary_headers, header_pairs.len) == 0);
    assert(append_bytes(
        &binary_headers, header_pairs.data, sizeof(header_pairs.data), header_pairs.len) == 0);

    memset(&text_headers, 0, sizeof(text_headers));
    assert(append_string(&text_headers, "X-One: one\r\nX-Two: two\r\n") == 0);

    test_notify_header_argument(
        "headers_bin", SPOP_DATA_BIN, &binary_headers, 0, 1, 0, 2U);
    test_notify_header_argument(
        "response_headers_bin", SPOP_DATA_BIN, &binary_headers, 1, 1, 0, 2U);
    test_notify_header_argument(
        "headers", SPOP_DATA_STR, &text_headers, 0, 0, 1, 1U);
    test_notify_header_argument(
        "response_headers", SPOP_DATA_STR, &text_headers, 1, 0, 1, 1U);
}

static void test_response_header_key_marks_response_for_nonbytes(void) {
    spop_buffer argument;
    notify_request request;
    size_t pos = 0U;

    memset(&argument, 0, sizeof(argument));
    memset(&request, 0, sizeof(request));
    assert(append_typed_bool(&argument, 1) == 0);
    assert(parse_notify_header_argument(&request,
        (const unsigned char *)"response_headers", sizeof("response_headers") - 1U,
        argument.data, argument.len, &pos) == 0);
    assert(pos == argument.len);
    assert(request.header_count == 0U);
    assert(request.is_response == 1);
    free_notify_request(&request);
}

static void test_notify_body_key_argument(
        const char *argument_name,
        unsigned int type,
        int expected_body,
        int expected_response,
        int expected_response_body) {
    spop_buffer argument;
    notify_request request;
    size_t pos = 0U;

    memset(&argument, 0, sizeof(argument));
    memset(&request, 0, sizeof(request));
    if (type == SPOP_DATA_BIN) {
        assert(append_byte(&argument, SPOP_DATA_BIN) == 0);
        assert(append_varint(&argument, 4U) == 0);
        assert(append_bytes(&argument, "body", 4U, 4U) == 0);
    } else if (type == SPOP_DATA_STR) {
        assert(append_typed_string(&argument, "body") == 0);
    } else {
        assert(append_typed_bool(&argument, 1) == 0);
    }
    assert(parse_notify_body_key_argument(&request,
        (const unsigned char *)argument_name, strlen(argument_name),
        argument.data, argument.len, &pos) == 0);
    assert(pos == argument.len);
    assert(request.has_body == expected_body);
    assert(request.is_response == expected_response);
    assert(request.is_response_body == expected_response_body);
    if (expected_body) {
        assert(request.body_len == 4U);
        assert(memcmp(request.body, "body", 4U) == 0);
    }
    free_notify_request(&request);
}

static void test_notify_body_arguments_preserve_type_and_response_role(void) {
    test_notify_body_key_argument("body", SPOP_DATA_STR, 1, 0, 0);
    test_notify_body_key_argument("body", SPOP_DATA_BIN, 1, 0, 0);
    test_notify_body_key_argument("response_body", SPOP_DATA_STR, 1, 1, 1);
    test_notify_body_key_argument("response_body", SPOP_DATA_BIN, 1, 1, 1);
    test_notify_body_key_argument("response_body", SPOP_DATA_BOOL, 0, 0, 0);
}

static void test_unknown_body_key_does_not_consume_or_mutate(void) {
    spop_buffer argument;
    notify_request request;
    size_t pos = 0U;

    memset(&argument, 0, sizeof(argument));
    memset(&request, 0, sizeof(request));
    assert(append_typed_string(&argument, "body") == 0);
    assert(parse_notify_body_key_argument(&request,
        (const unsigned char *)"unknown_body", sizeof("unknown_body") - 1U,
        argument.data, argument.len, &pos) == 1);
    assert(pos == 0U);
    assert(request.has_body == 0);
    assert(request.is_response == 0);
    assert(request.is_response_body == 0);
    free_notify_request(&request);
}

int main(void) {
    test_varint_length_contract();
    test_varint_boundaries();
    test_exact_fit_and_overflow_are_atomic();
    test_unterminated_input_does_not_mutate();
    test_notify_header_arguments_preserve_type_and_response_role();
    test_response_header_key_marks_response_for_nonbytes();
    test_notify_body_arguments_preserve_type_and_response_role();
    test_unknown_body_key_does_not_consume_or_mutate();
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
