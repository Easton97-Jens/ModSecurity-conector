"""Compiled fixture controls use simulated process IDs, never native evidence."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InputFaultScopeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = tempfile.TemporaryDirectory(prefix="input-fault-scope-", dir=os.environ.get("RUNNER_TEMP"))
        cls.addClassCleanup(temporary.cleanup)
        cls.root = Path(temporary.name)
        cls.binary = cls.root / "probe"
        flags = ["/usr/bin/cc", "-std=c17", "-Wall", "-Wextra", "-Werror", "-I", str(ROOT / "common/include")]
        obj = cls.root / "guard.o"
        subprocess.run(flags + ["-Dmsconnector_request_mapper_validate_output=actual_common_guard", "-c",
                        str(ROOT / "common/src/request_mapper_contract.c"), "-o", str(obj)],
                       check=True, capture_output=True, timeout=30)
        subprocess.run(flags + [str(ROOT / "tests/fixtures/nginx_common_input_fault_scope.c"), str(obj),
                                 "-o", str(cls.binary)], check=True, capture_output=True, timeout=30)

    def probe(self, case, control):
        ledger = self.root / (case + "-" + control + ".jsonl")
        ledger.touch(mode=0o600)
        result = subprocess.run([str(self.binary), case, control, str(ledger)],
                                check=True, capture_output=True, text=True, timeout=5)
        rows = [json.loads(line) for line in ledger.read_text().splitlines() if line]
        return result.stdout.strip(), rows

    def test_exact_target_reaches_real_common_guard_once(self):
        for case in ("body_size_nonzero_with_null_data", "header_count_nonzero_with_null_headers"):
            with self.subTest(case=case):
                result, rows = self.probe(case, "exact")
                self.assertEqual(result, "0 1")
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["validator_return"], 0)
                self.assertIs(rows[0]["diagnostic_match"], True)

    def test_wrong_transaction_uid_parent_uri_or_method_never_inject(self):
        for control in ("transaction", "uid", "parent", "uri", "method", "foreign-after-match"):
            with self.subTest(control=control):
                result, rows = self.probe("body_size_nonzero_with_null_data", control)
                self.assertEqual(result, "1 1")
                self.assertEqual(rows, [])
