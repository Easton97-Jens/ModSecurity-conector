"""Static Parent Makefile contracts for Phase-4 evidence promotion gates."""

from __future__ import annotations

import re
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FullLifecycleGateWiringTest(unittest.TestCase):
    def target_body(self, name: str) -> str:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        match = re.search(
            rf"^{re.escape(name)}:.*?(?=^\S|\Z)",
            makefile,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(match, f"missing Makefile target: {name}")
        return match.group(0)

    def test_strict_phase4_targets_invoke_parent_identity_checks(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn("define RUN_PARENT_FULL_LIFECYCLE_EVIDENCE_CHECK", makefile)
        macro = makefile.split(
            "define RUN_STRICT_FULL_LIFECYCLE_EVIDENCE_CHECK\n", 1
        )[1].split("\nendef", 1)[0]
        self.assertIn(
            "$(call RUN_PARENT_FULL_LIFECYCLE_EVIDENCE_CHECK,profile)", macro
        )
        expected = {
            "check-first-byte-before-response-end": "first-byte",
            "check-no-full-response-buffering": "no-full-buffer",
            "check-full-lifecycle-promotion": "promotion",
        }
        for target, parent_check in expected.items():
            with self.subTest(target=target):
                body = self.target_body(target)
                self.assertIn(
                    f"$(call RUN_PARENT_FULL_LIFECYCLE_EVIDENCE_CHECK,{parent_check})",
                    body,
                )


if __name__ == "__main__":
    unittest.main()
