"""Compiled resource-bound regressions for the HAProxy SPOP agent."""

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


class HAProxySPOPResourceLimitsContractTests(unittest.TestCase):
    """Reject header and transaction-cache growth before allocation expands."""

    def test_header_and_transaction_cache_bounds_are_enforced(self) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("requires a C compiler")

        harness_source = r'''
#define main haproxy_spop_diagnostic_runtime_program_main
#include "__RUNTIME_SOURCE__"
#undef main

#include <assert.h>
#include <stdio.h>

int main(void) {
    notify_request request;
    unsigned char value[SPOP_MAX_HEADER_VALUE_BYTES + 1U];
    unsigned char name[SPOP_MAX_HEADER_NAME_BYTES + 1U];
    agent_config config;
    agent_state state;
    char too_large[32];
    unsigned char typed_string[2048U + 3U];
    size_t typed_pos;
    char typed_output[2048U];
    int typed_present;

    memset(value, 'v', sizeof(value));
    memset(&request, 0, sizeof(request));
    assert(add_request_header(&request, (const unsigned char *)"x", 1U,
        value, SPOP_MAX_HEADER_VALUE_BYTES) == 0);
    assert(add_request_header(&request, (const unsigned char *)"x", 1U,
        value, SPOP_MAX_HEADER_VALUE_BYTES - 2U) == 0);
    assert(request.header_bytes == SPOP_MAX_TOTAL_HEADER_BYTES);
    assert(add_request_header(&request, (const unsigned char *)"x", 1U,
        value, 1U) != 0);
    free_notify_request(&request);

    memset(&request, 0, sizeof(request));
    memset(name, 'n', sizeof(name));
    assert(add_request_header(&request, name, SPOP_MAX_HEADER_NAME_BYTES,
        (const unsigned char *)"v", 1U) == 0);
    free_notify_request(&request);
    memset(&request, 0, sizeof(request));
    assert(add_request_header(&request, name, SPOP_MAX_HEADER_NAME_BYTES + 1U,
        (const unsigned char *)"v", 1U) != 0);
    assert(add_request_header(&request, (const unsigned char *)"x", 1U,
        value, SPOP_MAX_HEADER_VALUE_BYTES + 1U) != 0);
    free_notify_request(&request);

    memset(&request, 0, sizeof(request));
    for (unsigned int index = 0U; index < SPOP_MAX_HEADER_COUNT; ++index) {
        assert(add_request_header(&request, (const unsigned char *)"x", 1U,
            (const unsigned char *)"v", 1U) == 0);
    }
    assert(add_request_header(&request, (const unsigned char *)"x", 1U,
        (const unsigned char *)"v", 1U) != 0);
    free_notify_request(&request);

    config_init(&config);
    assert(config_set(&config, "max-transactions", "1") == 0);
    assert(config.max_transactions == 1U);
    assert(config_set(&config, "max-transactions", "0") != 0);
    snprintf(too_large, sizeof(too_large), "%u", SPOP_MAX_TRANSACTIONS + 1U);
    assert(config_set(&config, "max-transactions", too_large) != 0);

    config_init(&config);
    config.port = 1U;
    config.worker_count = SPOP_MAX_WORKER_COUNT;
    config.max_transactions =
        SPOP_MAX_TRANSACTION_SLOTS_TOTAL / SPOP_MAX_WORKER_COUNT;
    assert(production_config_has_safe_peer_limits(&config) == 1);
    config.max_transactions++;
    assert(production_config_has_safe_peer_limits(&config) == 0);
    memset(&state, 0, sizeof(state));
    state.config = config;
    assert(transaction_cache_init(&state) != 0);

    memset(typed_string, 's', sizeof(typed_string));
    typed_string[0] = SPOP_DATA_STR;
    /* SPOP's varint encoding uses the 240 escape for values >= 240. */
    typed_string[1] = 0xffU;
    typed_string[2] = 0x70U;
    typed_pos = 0U;
    typed_present = 0;
    assert(read_typed_string_to_buffer(typed_string, 2050U,
        &typed_pos, typed_output, sizeof(typed_output), &typed_present) == 0);
    assert(typed_present == 1);
    assert(typed_pos == 2050U);

    typed_string[1] = 0xf0U;
    typed_string[2] = 0x71U;
    typed_pos = 0U;
    typed_present = 0;
    assert(read_typed_string_to_buffer(typed_string, sizeof(typed_string),
        &typed_pos, typed_output, sizeof(typed_output), &typed_present) != 0);
    assert(typed_present == 0);

    config_init(&config);
    assert(config_set(&config, "spoe-timeout", "1") == 0);
    assert(config.spoe_timeout_ms == 1U);
    assert(config_set(&config, "spoe-timeout", "60000") == 0);
    assert(config.spoe_timeout_ms == 60000U);
    assert(config_set(&config, "spoe-timeout", "0") != 0);
    assert(config_set(&config, "spoe-timeout", "-1") != 0);
    assert(config_set(&config, "spoe-timeout", "+1") != 0);
    assert(config_set(&config, "spoe-timeout", " 1") != 0);
    assert(config_set(&config, "spoe-timeout", "60001") != 0);
    assert(config_set(&config, "spoe-timeout", "18446744073709551616") != 0);
    assert(config_set(&config, "spoe-timeout", "2000ms") != 0);

    assert(config_set(&config, "worker-count", "1") == 0);
    assert(config.worker_count == 1U);
    assert(config_set(&config, "worker-count", "64") == 0);
    assert(config.worker_count == SPOP_MAX_WORKER_COUNT);
    assert(config_set(&config, "worker-count", "0") != 0);
    assert(config_set(&config, "worker-count", "-1") != 0);
    assert(config_set(&config, "worker-count", "+1") != 0);
    assert(config_set(&config, "worker-count", " 1") != 0);
    assert(config_set(&config, "worker-count", "65") != 0);
    assert(config_set(&config, "worker-count", "18446744073709551616") != 0);
    assert(config_set(&config, "worker-count", "8workers") != 0);
    return 0;
}
'''.replace("__RUNTIME_SOURCE__", RUNTIME_SOURCE.as_posix())

        with tempfile.TemporaryDirectory(
            prefix="haproxy-spop-resource-limits-",
            dir=os.environ.get("TMPDIR"),
        ) as temporary_directory:
            temporary_root = Path(temporary_directory)
            harness = temporary_root / "resource_limits_contract.c"
            binary = temporary_root / "resource_limits_contract"
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
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(run_result.returncode, 0, run_result.stderr)


if __name__ == "__main__":
    unittest.main()
