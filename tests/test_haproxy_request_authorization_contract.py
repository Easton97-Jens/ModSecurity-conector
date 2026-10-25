"""Finite authorization scope uses the real shared FSM; no native/host claim."""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
class RequestAuthorizationContract(unittest.TestCase):
    def run_contract(self, *, sanitizer=False, mutation=None):
        root = Path(os.environ.get("TMPDIR", "/var/tmp/codex/ModSecurity-conector/tmp"))
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="haproxy-auth-contract-", dir=root) as directory:
            out = Path(directory)
            makefile = (ROOT / "connectors/haproxy/Makefile").read_text()
            names = next(line.split(":=", 1)[1].split() for line in makefile.splitlines()
                         if line.startswith("COMMON_SDK_SRCS :="))
            sources = [ROOT / "common/src" / name.rsplit("/", 1)[1] for name in names]
            if mutation:
                state = ROOT / "common/src/transaction_state.c"
                text = state.read_text()
                old, new = mutation
                self.assertIn(old, text)
                changed = out / "transaction_state.c"
                changed.write_text(text.replace(old, new, 1))
                sources = [changed if source == state else source for source in sources]
            command = ["cc", "-std=c17", "-Wall", "-Wextra", "-Werror", "-pthread",
                       "-I", str(ROOT), "-I", str(ROOT / "common/include"),
                       str(ROOT / "tests/haproxy_request_authorization_contract_test.c"),
                       str(ROOT / "connectors/profile_registry.c"), *map(str, sources),
                       "-o", str(out / "contract")]
            if sanitizer:
                command[1:1] = ["-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return subprocess.run([str(out / "contract")], capture_output=True, text=True, timeout=30)
    def test_request_scope_and_full_scope_remain_distinct(self):
        result = self.run_contract()
        self.assertEqual(result.returncode, 0, result.stderr)
    def test_request_scope_under_asan_ubsan(self):
        result = self.run_contract(sanitizer=True)
        self.assertEqual(result.returncode, 0, result.stderr)
    def test_scope_and_cleanup_mutations_are_detected(self):
        mutations = [
            ("if (!contract_has_request_authorization_scope(contract) ||", "if (0 ||"),
            ("contract->status == MSCONNECTOR_TRANSACTION_STATUS_COMPLETED &&\n          contract->completed_phase_mask", "1 &&\n          contract->completed_phase_mask"),
            ("contract->completed_phase_mask != MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL) {", "contract->completed_phase_mask == 0U) {"),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation[0]):
                result = self.run_contract(mutation=mutation)
                self.assertNotEqual(result.returncode, 0, "scope mutation survived")

# Parent default discovery uses the one admitted active-case inventory.
if __import__("os").environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)
