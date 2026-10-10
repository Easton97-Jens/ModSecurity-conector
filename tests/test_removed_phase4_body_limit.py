"""Removal contract; genuine host configuration rejection is tested separately."""

from pathlib import Path
import os
import shlex
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RemovedPhase4BodyLimitTests(unittest.TestCase):
    def test_common_public_api_has_no_removed_setting(self):
        for name in ("config.h", "directives.h", "options.h"):
            text = (ROOT / "common/include/msconnector" / name).read_text()
            self.assertNotIn("phase4_body_limit", text)
            self.assertNotIn("PHASE4_BODY_LIMIT", text)

    def test_native_hosts_do_not_register_removed_directive(self):
        for name in ("connectors/nginx/src/ngx_http_modsecurity_module.c",
                     "connectors/apache/src/msc_config.c"):
            text = (ROOT / name).read_text()
            self.assertNotIn("phase4_body_limit", text)
            self.assertNotIn("PHASE4_BODY_LIMIT", text)

    def test_storage_defaults_remain_independent_and_bounded(self):
        text = (ROOT / "common/include/msconnector/options.h").read_text()
        self.assertIn("#define MSCONNECTOR_DEFAULT_REQUEST_BODY_LIMIT 1048576", text)
        self.assertIn("#define MSCONNECTOR_DEFAULT_RESPONSE_BODY_LIMIT 1048576", text)

    def test_compiled_common_registry_rejects_removed_api(self):
        compiler = shlex.split(os.environ.get("CC", "cc"))
        if not compiler or shutil.which(compiler[0]) is None:
            self.skipTest("C compiler unavailable")
        source = r'''
#include <assert.h>
#include "msconnector/directive_spec.h"
#include "msconnector/directive_adapter.h"
int main(void) {
    assert(msconnector_directive_spec_find("modsecurity_phase4_body_limit") == 0);
    assert(msconnector_directive_adapter_find("modsecurity_phase4_body_limit") == 0);
    assert(msconnector_directive_spec_find("modsecurity_phase4_mode") != 0);
    assert(msconnector_directive_adapter_find("modsecurity_phase4_mode") != 0);
    assert(msconnector_directive_spec_find("modsecurity_response_body_limit") != 0);
    assert(msconnector_directive_adapter_find("modsecurity_request_body_limit") != 0);
    assert(msconnector_directive_adapter_validate_all(0, 0));
    return 0;
}
'''
        with tempfile.TemporaryDirectory(prefix="removed-phase4-api-") as directory:
            binary = Path(directory) / "registry-test"
            command = compiler + ["-std=c17", "-Wall", "-Wextra", "-Werror",
                                  "-I", str(ROOT / "common/include"),
                                  "-x", "c", "-",
                                  str(ROOT / "common/src/directive_spec.c"),
                                  str(ROOT / "common/src/directive_adapter.c"),
                                  "-o", str(binary)]
            compiled = subprocess.run(command, input=source, text=True,
                                      capture_output=True, timeout=30)
            self.assertEqual(compiled.returncode, 0, compiled.stdout + compiled.stderr)
            result = subprocess.run([str(binary)], text=True, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
