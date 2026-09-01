from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SOURCE = ROOT / "common" / "runtime" / "msconnector_runtime.c"
INTERVENTION_HEADER = ROOT / "common" / "include" / "msconnector" / "intervention.h"
INTERVENTION_SOURCE = ROOT / "common" / "src" / "intervention.c"


class ModSecurityRequestBodyLimitStatusContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = RUNTIME_SOURCE.read_text(encoding="utf-8")
        cls.header = INTERVENTION_HEADER.read_text(encoding="utf-8")
        cls.intervention_source = INTERVENTION_SOURCE.read_text(encoding="utf-8")
        match = re.search(
            r"int msconnector_intervention_is_request_body_limit_rejection\([\s\S]*?\n}\n\nint msconnector_intervention_normalize_status",
            cls.intervention_source,
        )
        assert match is not None
        cls.status_mapper = match.group(0)
        native_status_match = re.search(
            r"static int native_intervention_status\([\s\S]*?\n}\n\nstatic int native_decision",
            cls.source,
        )
        assert native_status_match is not None
        cls.native_status_mapper = native_status_match.group(0)

    def test_exact_request_body_limit_signature_maps_to_413(self) -> None:
        self.assertIn(
            "#define MSCONNECTOR_REQUEST_BODY_LIMIT_REJECTION_LOG",
            self.header,
        )
        self.assertIn(
            '"Request body limit is marked to reject the request"',
            self.header,
        )
        for condition in (
            "intervention->disruptive != 0",
            "phase == MSCONNECTOR_PHASE_REQUEST_BODY",
            "intervention->status == 403",
            "intervention->redirect_url == 0",
            "intervention->log_message != 0",
            "MSCONNECTOR_REQUEST_BODY_LIMIT_REJECTION_LOG",
        ):
            self.assertIn(condition, self.status_mapper)
        self.assertIn("return 413;", self.native_status_mapper)

    def test_nonmatching_interventions_preserve_the_engine_status(self) -> None:
        self.assertIn(
            "return intervention == NULL ? 0 : intervention->status;",
            self.native_status_mapper,
        )
        self.assertNotIn("strstr(", self.status_mapper)

    def test_native_decision_normalizes_the_constrained_status_before_mapping(self) -> None:
        invocation = self.source.index(
            "int intervention_status = msconnector_intervention_normalize_status("
        )
        native_status = self.source.index(
            "native_intervention_status(phase, &intervention)", invocation
        )
        decision_mapping = self.source.index(
            "msconnector_decision_from_intervention(", native_status
        )
        self.assertLess(invocation, native_status)
        self.assertLess(native_status, decision_mapping)

    def test_exact_limit_signature_uses_the_rule_id_free_body_limit_decision(self) -> None:
        self.assertIn(
            "body_limit = native_is_request_body_limit_rejection(phase, &intervention);",
            self.source,
        )
        self.assertIn(
            "msconnector_intervention_is_request_body_limit_rejection(phase,",
            self.source,
        )
        self.assertIn(
            "msconnector_decision_set_body_limit(decision, native->reason);",
            self.source,
        )

    def test_body_limit_terminal_and_host_actions_remain_413_denies(self) -> None:
        self.assertIn(
            "contract->error_class == MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT",
            self.source,
        )
        self.assertIn("return 413;", self.source)
        self.assertIn("msconnector_decision_is_body_limit(decision)", self.source)
        self.assertIn("visible_http_status != 413", self.source)
        self.assertIn("a body-limit decision requires an HTTP 413 deny action", self.source)


if __name__ == "__main__":
    unittest.main()
