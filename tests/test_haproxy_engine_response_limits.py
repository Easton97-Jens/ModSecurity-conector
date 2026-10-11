"""Real libModSecurity limit effects through the HAProxy binding, not host proof."""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = r"""
#include "haproxy_modsecurity_binding.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
    haproxy_modsecurity_engine_config config = {0};
    haproxy_modsecurity_engine *engine = NULL;
    haproxy_modsecurity_transaction *transaction = NULL;
    haproxy_modsecurity_decision decision;
    haproxy_modsecurity_header header = {"Content-Type", "text/plain"};
    haproxy_modsecurity_header request_header = {"Host", "localhost"};
    haproxy_modsecurity_request request = {0};
    haproxy_modsecurity_response response = {0};
    unsigned char chunk[32768];
    size_t length, marker, sent = 0U;
    int reject, match, rc;
    FILE *file = NULL;
    if (argc != 9) return 2;
    length = strtoul(argv[2], NULL, 10);
    marker = strtoul(argv[8], NULL, 10);
    reject = atoi(argv[3]); match = atoi(argv[4]);
    msconnector_config_init(&config.common_config);
    msconnector_config_apply_defaults(&config.common_config);
    config.common_config.phase4_mode = strtoul(argv[5], NULL, 10);
    config.rules_file = argv[1];
    request.request_id = "real-limit-binding";
    request.client_ip = "192.0.2.10"; request.client_port = 12345;
    request.server_ip = "198.51.100.20"; request.server_port = 8080;
    request.method = "GET"; request.uri = "/engine-limit";
    request.headers = &request_header; request.header_count = 1U;
    response.status = 200; response.protocol = "HTTP/1.1";
    response.headers = &header; response.header_count = 1U;
    if (haproxy_modsecurity_engine_create(&config, &engine, &decision) ||
        haproxy_modsecurity_transaction_begin_request_with_profile(engine, &request,
            "haproxy-htx", &decision, &transaction) ||
        haproxy_modsecurity_transaction_finish_request_body(transaction, &decision) ||
        haproxy_modsecurity_transaction_process_response_headers(transaction, &response, &decision)) {
        fprintf(stderr, "prelude phase=%d status=%d log=%s\n", decision.phase, decision.status, decision.log_message); return 3;
    }
    memset(chunk, 'a', sizeof(chunk));
    if (strcmp(argv[6], "file") == 0) {
        file = fopen(argv[7], "rb");
        if (!file) return 4;
    }
    while (sent < length) {
        size_t amount = length - sent < sizeof(chunk) ? length - sent : sizeof(chunk);
        if (file && fread(chunk, 1U, amount, file) != amount) return 5;
        if (!file && marker >= sent && marker < sent + amount) chunk[marker - sent] = 'Z';
        rc = haproxy_modsecurity_transaction_append_response_body_chunk(transaction,
            chunk, (unsigned int)amount, &decision);
        if (rc) { fprintf(stderr, "append: %d %s\n", rc, decision.log_message); return 6; }
        sent += amount;
    }
    if (file) fclose(file);
    rc = haproxy_modsecurity_transaction_finish_response_body(transaction, &decision);
    if (rc || decision.phase != 4 || decision.disruptive != (reject || match) ||
        (reject && (!decision.body_limit || decision.status != 403 || decision.rule_id)) ||
        (!reject && decision.rule_id != (match ? 1250801 : 0))) {
        fprintf(stderr, "finish rc=%d phase=%d disruptive=%d body_limit=%d status=%d rule=%d log=%s\n",
            rc, decision.phase, decision.disruptive, decision.body_limit,
            decision.status, decision.rule_id, decision.log_message);
        return 7;
    }
    haproxy_modsecurity_transaction_abort(transaction);
    haproxy_modsecurity_engine_destroy(engine);
    return 0;
}
"""


class HaproxyRealEngineResponseLimitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="haproxy-real-limits-", dir=os.environ.get("TMPDIR"))
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.runroot = Path(cls.temporary.name)
        cls.build = cls.runroot / "build"
        include_dir = os.environ.get("MODSECURITY_INCLUDE_DIR", "/usr/include")
        lib_dir = os.environ.get("MODSECURITY_LIB_DIR", "/usr/lib/x86_64-linux-gnu")
        built = subprocess.run(["rtk", "proxy", "make", "-C", str(ROOT / "connectors/haproxy"),
            "build-modsecurity-binding", f"BUILD_ROOT={cls.build}",
            f"MODSECURITY_INCLUDE_DIR={include_dir}", f"MODSECURITY_LIB_DIR={lib_dir}"],
            capture_output=True, text=True, timeout=180)
        if built.returncode:
            raise AssertionError(built.stdout + built.stderr)
        source = cls.runroot / "limits.c"
        source.write_text(PROGRAM)
        cls.binary = cls.runroot / "limits"
        objroot = cls.build / "haproxy-modsecurity-binding"
        resolution = dict(line.split("=", 1) for line in (objroot / "paths.env").read_text().splitlines() if "=" in line)
        # Reuse native build objects and selected real engine; exclude probe/main().
        objects = [str(p) for p in objroot.glob("*.o") if p.name != "haproxy_modsecurity_binding_self_test.o" and not p.name.startswith("verify_")]
        compiled = subprocess.run(["cc", "-std=c17", "-Wall", "-Wextra", "-Werror",
            "-I", str(ROOT / "connectors/haproxy/src"), "-I", str(ROOT / "common/include"),
            str(source), *objects, resolution["MODSECURITY_LIBRARY"],
            f'-Wl,-rpath,{resolution["MODSECURITY_LIB_DIR"]}', "-lstdc++", "-o", str(cls.binary)],
            capture_output=True, text=True, timeout=60)
        if compiled.returncode:
            raise AssertionError(compiled.stdout + compiled.stderr)

    def run_case(self, *, limit, action, length, reject, match, mode, representation, marker_offset=None, phase4_pass=False):
        # Required arguments are deliberately explicit at every test invocation.
        if limit <= 0 or action not in {"Reject", "ProcessPartial"}:
            raise ValueError("explicit positive SecResponseBodyLimit and valid SecResponseBodyLimitAction required")
        rules = self.runroot / "case.conf"
        rules.write_text(f"SecRuleEngine On\nSecRequestBodyAccess Off\nSecResponseBodyAccess On\n"
            f"SecResponseBodyMimeType text/plain\nSecResponseBodyLimit {limit}\n"
            f"SecResponseBodyLimitAction {action}\nSecAuditEngine Off\n"
            'SecRule RESPONSE_BODY "@contains Z" "id:1250801,phase:4,deny,status:403,log"\n')
        marker = length - 1 if marker_offset is None else marker_offset
        if phase4_pass:
            with rules.open("a") as output:
                output.write('SecAction "id:1250802,phase:4,pass,nolog"\n')
        payload = self.runroot / "response.bin"
        if representation == "file":
            with payload.open("wb") as output:
                left = length - 1
                while left:
                    amount = min(left, 32768)
                    output.write(b"a" * amount)
                    left -= amount
                output.write(b"Z")
        result = subprocess.run([str(self.binary), str(rules), str(length), str(int(reject)),
            str(int(match)), str(mode), representation, str(payload), str(marker)],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_explicit_engine_boundaries_and_actions(self):
        for action in ("Reject", "ProcessPartial"):
            for length in (7, 8, 9):
                with self.subTest(action=action, length=length):
                    self.run_case(limit=8, action=action, length=length,
                        reject=action == "Reject" and length > 8,
                        match=length <= 8, mode=1, representation="memory")

    def test_same_engine_configuration_across_modes_and_chunks(self):
        for mode in (0, 1, 2):
            self.run_case(limit=70000, action="Reject", length=65537,
                reject=False, match=True, mode=mode, representation="memory")
            self.run_case(limit=65536, action="ProcessPartial", length=65537,
                reject=False, match=False, mode=mode, representation="file")

    def test_large_file_has_no_hidden_one_mib_connector_limit(self):
        self.run_case(limit=2097152, action="Reject", length=1048577,
            reject=False, match=True, mode=1, representation="file")
        self.run_case(limit=1048576, action="Reject", length=1048577,
            reject=True, match=False, mode=1, representation="file")

    def test_process_partial_still_evaluates_rules_in_engine_retained_prefix(self):
        self.run_case(limit=8, action="ProcessPartial", length=9,
            reject=False, match=True, mode=1, representation="memory", marker_offset=3)

    def test_reject_retains_native_intervention_across_later_chunks(self):
        self.run_case(limit=65536, action="Reject", length=120000,
            reject=True, match=False, mode=1, representation="memory", phase4_pass=True)

    def test_missing_fixture_limit_or_action_fails_at_creation(self):
        with self.assertRaisesRegex(TypeError, "limit"):
            self.run_case(action="Reject", length=7, reject=False, match=True, mode=1, representation="memory")
        with self.assertRaisesRegex(TypeError, "action"):
            self.run_case(limit=8, length=7, reject=False, match=True, mode=1, representation="memory")


if __name__ == "__main__":
    unittest.main()
