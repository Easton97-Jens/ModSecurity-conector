"""Regression coverage for the root-safe NGINX case environment reader."""

from __future__ import annotations

import importlib.util
import shlex
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "connectors/nginx/harness/read_case_env.py"


def load_reader_module():
    spec = importlib.util.spec_from_file_location("nginx_case_env_reader", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load NGINX case environment reader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


READER = load_reader_module()


def valid_environment(**overrides: str) -> str:
    values = {
        "CASE_NAME": "phase4_deny_after_commit_log_only",
        "REQUEST_METHOD": "GET",
        "REQUEST_PATH": "/no-crs/response-body",
        "REQUEST_HAS_BODY": "0",
        "REQUEST_HEADERS_FILE": "/runtime/request-headers.txt",
        "REQUEST_BODY_FILE": "/runtime/request-body.bin",
        "AUDIT_LOG_FILE": "/runtime/audit.log",
        "AUDIT_LOG_DIR": "/runtime/audit",
        "EXPECT_STATUS": "200",
        "EXPECT_INTERVENTION": "",
        "EXPECT_RULE_ID": "1100301",
        "EXPECT_RESPONSE_CONTAINS": "no-crs-response-body-marker",
        "EXPECT_TRANSPORT": "http_status",
        "EXPECT_AUDIT_LOG_REQUIRED": "0",
        "NGINX_PHASE4_MODE": "safe",
    }
    values.update(overrides)
    return "".join(
        ["# Generated from common test case. Do not edit.\n"]
        + [f"{key}={shlex.quote(value)}\n" for key, value in values.items()]
    )


class NginxCaseEnvironmentReaderTest(unittest.TestCase):
    def read(self, content: str) -> dict[str, str]:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "case.env"
            path.write_text(content, encoding="utf-8")
            return READER.read_case_environment(path)

    def test_reads_the_framework_data_fragment_without_shell_evaluation(self) -> None:
        values = self.read(valid_environment(REQUEST_PATH="/a path?query=literal;$(not-run)"))
        self.assertEqual(values["REQUEST_PATH"], "/a path?query=literal;$(not-run)")
        self.assertEqual(values["EXPECT_RULE_ID"], "1100301")
        self.assertEqual(set(values), READER._ALLOWED_KEYS)

    def test_rejects_unknown_assignment_and_shell_command_suffix(self) -> None:
        content = valid_environment().replace(
            "REQUEST_PATH=/no-crs/response-body\n",
            "REQUEST_PATH=/no-crs/response-body; /usr/bin/id\n",
        )
        with self.assertRaisesRegex(READER.CaseEnvironmentError, "exactly one quoted value"):
            self.read(content)

        with self.assertRaisesRegex(READER.CaseEnvironmentError, "unexpected key"):
            self.read(valid_environment() + "UNSAFE=1\n")

    def test_rejects_duplicate_missing_and_control_character_values(self) -> None:
        duplicate = valid_environment() + "CASE_NAME=second\n"
        with self.assertRaisesRegex(READER.CaseEnvironmentError, "duplicate key"):
            self.read(duplicate)

        missing = valid_environment().replace("NGINX_PHASE4_MODE=safe\n", "")
        with self.assertRaisesRegex(READER.CaseEnvironmentError, "missing required keys"):
            self.read(missing)

        with self.assertRaisesRegex(READER.CaseEnvironmentError, "forbidden control character"):
            self.read(valid_environment(REQUEST_PATH="/ok\x00not-ok"))

    def test_harness_uses_reader_only_for_the_root_functional_path(self) -> None:
        harness = (
            ROOT / "connectors/nginx/harness/run_nginx_smoke.sh"
        ).read_text(encoding="utf-8")
        self.assertIn('NGINX_HOSTED_FUNCTIONAL_A="${NGINX_HOSTED_FUNCTIONAL_A:-0}"', harness)
        self.assertIn("load_functional_case_environment", harness)
        self.assertIn('if [ "$NGINX_HOSTED_FUNCTIONAL_A" = "1" ]; then\n    load_functional_case_environment', harness)
        self.assertIn('else\n    . "$CASE_ENV_FILE"', harness)
        functional_section = harness.split("load_functional_case_environment()", 1)[1].split(
            "write_harness_status()", 1
        )[0]
        self.assertNotIn("eval", functional_section)
        self.assertNotIn('. "$CASE_ENV_FILE"', functional_section)


if __name__ == "__main__":
    unittest.main()
