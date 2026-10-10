"""Compile real Common decision/event code; these are not live-host tests."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest

from tests.c_source_contract import function_definition

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = r'''
#include "msconnector/decision_action.h"
#include "msconnector/event.h"
#include <stdio.h>

static const char *text(const char *value) { return value == NULL ? "" : value; }

static void emit(const char *group, int number, const msconnector_decision *decision) {
    msconnector_event event;
    const msconnector_decision_action action = msconnector_decision_action_from_decision(decision);
    int available;
    msconnector_event_init(&event);
    available = msconnector_decision_to_event(decision, &event, "common", "decision-test");
    printf("{\"group\":\"%s\",\"number\":%d,\"action\":\"%s\","
           "\"is_allow\":%d,\"disruptive\":%d,\"event\":%d,"
           "\"status\":\"%s\",\"requested\":\"%s\",\"actual\":\"%s\","
           "\"rule_id\":\"%s\",\"message_id\":\"%s\",\"http_status\":%d}\n",
           group, number, msconnector_decision_action_name(action),
           msconnector_decision_is_allow(decision), msconnector_decision_is_disruptive(decision),
           available, msconnector_event_status_name(&event),
           text(event.decision.requested_action), text(event.decision.actual_action),
           text(event.decision.rule_id), text(event.meta.message_id), event.http.http_status);
}

int main(void) {
    msconnector_decision decision;
    emit("null", 0, NULL);
    for (int kind = 0; kind <= 7; ++kind) {
        msconnector_decision_init(&decision);
        decision.kind = (msconnector_decision_kind)kind;
        decision.phase = MSCONNECTOR_PHASE_REQUEST_BODY;
        decision.http_status = 403;
        decision.rule_id = "123";
        emit("valid", kind, &decision);
        decision.status = MSCONNECTOR_STATUS_ERROR;
        decision.disruptive = 0;
        emit("error_status", kind, &decision);
    }
    const int invalid[] = {-1, 8, 99};
    for (size_t i = 0U; i < sizeof(invalid) / sizeof(invalid[0]); ++i) {
        msconnector_decision_init(&decision);
        decision.kind = (msconnector_decision_kind)invalid[i];
        decision.rule_id = "stale";
        emit("invalid", invalid[i], &decision);
    }
    msconnector_decision_set_deny(&decision, 429, "123", "rate-limit");
    emit("rate_limit", 0, &decision);
    msconnector_decision_set_body_limit(&decision, "request_body_limit_exceeded");
    emit("body_limit", 0, &decision);
    msconnector_decision_set_error(&decision, 503, "connector_error");
    emit("set_error", 0, &decision);
    return 0;
}
'''


class DecisionSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        compiler = shlex.split(os.environ.get("CC", "cc"))
        if not compiler or shutil.which(compiler[0]) is None:
            raise RuntimeError("a C compiler is required for decision regressions")
        temporary = tempfile.TemporaryDirectory(
            prefix="pr382-decisions-", dir=os.environ.get("RUNNER_TEMP")
        )
        cls.addClassCleanup(temporary.cleanup)
        directory = Path(temporary.name)
        fixture = directory / "fixture.c"
        fixture.write_text(FIXTURE, encoding="utf-8")
        phase_file = directory / "phase.c"
        phase_source = (ROOT / "common/src/transaction_state.c").read_text(encoding="utf-8")
        phase_file.write_text(
            '#include "msconnector/transaction_state.h"\n' +
            function_definition(phase_source, "msconnector_phase_name"),
            encoding="utf-8",
        )
        names = ("decision.c", "decision_action.c", "intervention.c", "block_statuses.c",
                 "event.c", "event_jsonl.c", "http_status.c", "json_escape.c", "status.c")
        binary = directory / "decisions"
        command = compiler + ["-std=c17", "-Wall", "-Wextra", "-Werror",
                              "-I", str(ROOT / "common/include"), str(fixture), str(phase_file)]
        command += [str(ROOT / "common/src" / name) for name in names]
        command += ["-o", str(binary)]
        compiled = subprocess.run(command, capture_output=True, text=True, timeout=90, check=False)
        if compiled.returncode:
            raise AssertionError("decision fixture compilation failed:\n" + compiled.stderr[-6000:])
        result = subprocess.run([str(binary)], capture_output=True, text=True, timeout=10, check=True)
        cls.records = [json.loads(line) for line in result.stdout.splitlines()]
        if len(cls.records) != 23:
            raise AssertionError("the compiled decision fixture did not report every case")

    def group(self, name: str) -> list[dict]:
        return [record for record in self.records if record["group"] == name]

    def test_missing_decision_is_error_not_log_only(self) -> None:
        record = self.group("null")[0]
        self.assertEqual(record["action"], "error")
        self.assertEqual(record["is_allow"], 0)
        self.assertEqual(record["event"], 0)

    def test_known_decision_kinds_keep_their_actions(self) -> None:
        expected = ["allow", "log_only", "deny", "redirect", "drop",
                    "abort_connection", "error", "unsupported"]
        self.assertEqual([record["action"] for record in self.group("valid")], expected)
        self.assertEqual(self.group("rate_limit")[0]["action"], "rate_limit")

    def test_explicit_error_overrides_every_stale_kind(self) -> None:
        for record in self.group("error_status"):
            with self.subTest(kind=record["number"]):
                self.assertEqual(record["action"], "error")
                self.assertEqual(record["is_allow"], 0)
                self.assertEqual(record["disruptive"], 1)
                self.assertEqual(record["event"], 1)
                self.assertEqual(record["status"], "error")
                self.assertEqual(record["message_id"], "MSCONN_EVENT_INTERNAL_ERROR")
                self.assertEqual(record["requested"], "error")
                self.assertEqual(record["rule_id"], "")

    def test_unknown_kinds_are_visible_technical_errors(self) -> None:
        for record in self.group("invalid"):
            with self.subTest(kind=record["number"]):
                self.assertEqual(record["action"], "error")
                self.assertEqual(record["disruptive"], 1)
                self.assertEqual(record["event"], 1)
                self.assertEqual(record["status"], "error")
                self.assertEqual(record["rule_id"], "")

    def test_decision_alone_never_claims_observed_host_action(self) -> None:
        for record in self.records:
            with self.subTest(group=record["group"], kind=record["number"]):
                self.assertEqual(record["actual"], "")

    def test_policy_limit_remains_a_block_not_an_engine_error(self) -> None:
        record = self.group("body_limit")[0]
        self.assertEqual(record["action"], "deny")
        self.assertEqual(record["message_id"], "MSCONN_EVENT_BODY_LIMIT")
        self.assertEqual(record["status"], "blocked")
        self.assertEqual(record["http_status"], 413)

    def test_error_constructor_keeps_configured_error_status(self) -> None:
        record = self.group("set_error")[0]
        self.assertEqual(record["action"], "error")
        self.assertEqual(record["requested"], "error")
        self.assertEqual(record["http_status"], 503)


if __name__ == "__main__":
    unittest.main()
