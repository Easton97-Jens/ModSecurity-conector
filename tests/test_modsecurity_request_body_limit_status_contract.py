from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SOURCE = ROOT / "common" / "runtime" / "msconnector_runtime.c"


class ModSecurityRequestBodyLimitStatusContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = RUNTIME_SOURCE.read_text(encoding="utf-8")
        match = re.search(
            r"static int native_intervention_status\([\s\S]*?\n}\n\nstatic int native_decision",
            cls.source,
        )
        assert match is not None
        cls.status_mapper = match.group(0)

    def test_exact_request_body_limit_signature_maps_to_413(self) -> None:
        self.assertIn(
            "#define RUNTIME_REQUEST_BODY_LIMIT_REJECTION_LOG",
            self.source,
        )
        self.assertIn(
            '"Request body limit is marked to reject the request"',
            self.source,
        )
        for condition in (
            "intervention->disruptive != 0",
            "phase == MSCONNECTOR_PHASE_REQUEST_BODY",
            "intervention->status == 403",
            "intervention->url == NULL",
            "intervention->log != NULL",
            "strcmp(intervention->log, RUNTIME_REQUEST_BODY_LIMIT_REJECTION_LOG) == 0",
        ):
            self.assertIn(condition, self.status_mapper)
        self.assertRegex(self.status_mapper, r"\{\s*return 413;\s*}")

    def test_nonmatching_interventions_preserve_the_engine_status(self) -> None:
        self.assertIn(
            "return intervention == NULL ? 0 : intervention->status;",
            self.status_mapper,
        )
        self.assertNotIn("strstr(", self.status_mapper)

    def test_native_decision_uses_the_constrained_mapper_before_allowlist_fallback(self) -> None:
        invocation = self.source.index("int intervention_status = native_intervention_status(")
        fallback = self.source.index("msconnector_block_status_is_allowed(intervention_status)")
        self.assertLess(invocation, fallback)
        self.assertIn("phase, &intervention", self.source[invocation:fallback])


if __name__ == "__main__":
    unittest.main()
