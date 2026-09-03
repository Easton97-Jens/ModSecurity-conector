"""Regression contracts for lossless and reject-before-transaction SPOP targets."""

from pathlib import Path
import subprocess


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c"
).read_text(encoding="utf-8")
HARNESS = (
    Path(__file__).resolve().parents[1]
    / "tests/haproxy_spop_request_target_test.c"
).read_text(encoding="utf-8")


def test_targets_use_canonical_storage_and_target_specific_validation() -> None:
    assert "char path[MSCONNECTOR_MAX_PATH_LENGTH + 1U];" in SOURCE
    assert "char uri[MSCONNECTOR_MAX_PATH_LENGTH + 1U];" in SOURCE

    start = SOURCE.index("static int read_typed_target_to_buffer(")
    end = SOURCE.index("/* Correlation identifiers", start)
    helper = SOURCE[start:end]
    assert "value_len > MSCONNECTOR_MAX_PATH_LENGTH" in helper
    assert "memchr(value, '\\0', value_len)" in helper
    assert "memcpy(out, value, value_len)" in helper
    assert "out[value_len] = '\\0';" in helper


def test_path_and_uri_route_through_target_parser_without_changing_generic_copy() -> None:
    parser_start = SOURCE.index("static int parse_notify_string_argument(")
    parser_end = SOURCE.index("static int parse_notify_uint_argument(", parser_start)
    parser = SOURCE[parser_start:parser_end]
    assert "if (index == 4U || index == 5U)" in parser
    assert "read_typed_target_to_buffer" in parser
    assert "read_typed_string_to_buffer" in parser

    generic_start = SOURCE.index("static void copy_spop_string(")
    generic_end = SOURCE.index("static void copy_cstring(", generic_start)
    generic = SOURCE[generic_start:generic_end]
    assert "if (copy_len >= out_len)" in generic
    assert "copy_len = out_len - 1U;" in generic


def test_executable_harness_covers_1023_and_post_1023_mapper_marker() -> None:
    assert 'assert_lossless("path", 1023)' in HARNESS
    assert 'assert_lossless("uri", 1023)' in HARNESS
    assert 'assert_marker_reaches_mapper("path")' in HARNESS
    assert 'assert_marker_reaches_mapper("uri")' in HARNESS
    assert "value[1023U] = 'Z';" in HARNESS
    assert "build_modsecurity_request_from_notify" in HARNESS
    assert "mapped.uri[1023U] != 'Z'" in HARNESS
    assert "memchr(value, '\\0', value_len)" in SOURCE


def test_production_parser_harness_executes_lossless_and_reject_paths(tmp_path: Path) -> None:
    binary = tmp_path / "haproxy-spop-request-target-test"
    subprocess.run(
        [
            "cc",
            "-std=c17",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-ffunction-sections",
            "-fdata-sections",
            "-Wl,--gc-sections",
            "-Icommon/include",
            "-Iconnectors/haproxy/include",
            "tests/haproxy_spop_request_target_test.c",
            "common/src/transaction_state.c",
            "-o",
            str(binary),
            "-pthread",
        ],
        check=True,
    )
    subprocess.run([str(binary)], check=True)


def test_parse_failure_precedes_both_notify_transaction_sinks() -> None:
    parse_start = SOURCE.index("static int handle_notify_frame(")
    parse_end = SOURCE.index("static int handle_connection(", parse_start)
    handler = SOURCE[parse_start:parse_end]
    assert handler.index("parse_notify_payload") < handler.index("process_production_notify")
    assert handler.index("parse_notify_payload") < handler.index("process_legacy_notify")
