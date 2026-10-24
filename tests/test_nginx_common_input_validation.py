"""Compile actual Common boundary guards; never claim native HTTP evidence."""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CommonInputValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary = tempfile.TemporaryDirectory(prefix="common-input-", dir=os.environ.get("RUNNER_TEMP"))
        cls.addClassCleanup(temporary.cleanup)
        cls.binary = Path(temporary.name) / "probe"
        subprocess.run(["/usr/bin/cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                        "-ffunction-sections", "-Wl,--gc-sections", "-I", str(ROOT / "common/include"),
                        str(ROOT / "tests/fixtures/nginx_common_input_validation.c"),
                        str(ROOT / "common/src/request_helpers.c"),
                        str(ROOT / "common/src/request_mapper_contract.c"), "-o", str(cls.binary)],
                       check=True, capture_output=True, timeout=30)

    def probe(self, mode):
        result = subprocess.run([str(self.binary), mode], check=True, capture_output=True, text=True, timeout=5)
        return result.stdout.splitlines()

    def test_nonzero_body_with_null_data_rejected_at_actual_common_mapper_boundary(self):
        result = self.probe("body")
        self.assertEqual(result[:2], ["0", "0"])
        self.assertEqual(result[2], "missing body data")

    def test_nonzero_headers_with_null_array_rejected_at_actual_common_mapper_boundary(self):
        self.assertEqual(self.probe("headers"), ["0", "0", "missing headers"])

    def test_valid_and_truly_empty_inputs_remain_accepted(self):
        for mode in ("valid", "empty"):
            with self.subTest(mode=mode):
                self.assertEqual(self.probe(mode), ["1", "1", ""])

    def test_unsupported_body_policy_error_precedes_pointer_validation(self):
        self.assertEqual(self.probe("unsupported"), ["0", "0", "body unsupported"])


if __name__ == "__main__":
    unittest.main()
