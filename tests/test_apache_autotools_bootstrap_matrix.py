#!/usr/bin/env python3
"""Guard the direct Apache Autotools P1–P4 pre-commit loopback contract."""

from pathlib import Path
import unittest


ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
CHECK = ROOT / "ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh"


class ApacheAutotoolsBootstrapMatrixTest(unittest.TestCase):
    def test_check_uses_local_rules_for_real_p1_to_p4_precommit_traffic(self) -> None:
        source = CHECK.read_text(encoding="utf-8")

        self.assertIn('Listen 127.0.0.1:$PORT', source)
        self.assertEqual(source.count("curl --noproxy '*'"), 9)
        self.assertIn('modsecurity_rules "SecRequestBodyAccess On"', source)
        self.assertIn('modsecurity_rules "SecResponseBodyAccess On"', source)
        self.assertIn('modsecurity_rules "SecResponseBodyMimeType text/plain"', source)
        self.assertIn('id:100001,phase:1,deny,status:403,log', source)
        self.assertIn('REQUEST_BODY \\"@contains msconnector-p2-only\\"', source)
        self.assertIn('id:100002,phase:2,deny,status:403,log', source)
        self.assertIn('ForceType application/x-apache-p3-block', source)
        self.assertIn('<Files "p4blocked.txt">', source)
        self.assertIn('ForceType text/plain', source)
        self.assertIn('RESPONSE_HEADERS:Content-Type', source)
        self.assertIn('application/x-apache-p3-block', source)
        self.assertIn('id:100003,phase:3,deny,status:403,log', source)
        self.assertIn('RESPONSE_BODY \\"@contains $P4_PRECOMMIT_MARKER\\"', source)
        self.assertIn('id:100004,phase:4,deny,status:403,log', source)
        self.assertIn('modsecurity_phase4_mode safe', source)
        self.assertNotIn('modsecurity_rules_remote', source)

    def test_check_requires_phase_specific_observations_and_a_post_deny_allow(self) -> None:
        source = CHECK.read_text(encoding="utf-8")

        for status in (
            "p2_allowed_status",
            "p2_blocked_status",
            "p3_blocked_status",
            "p4_allowed_status",
            "p4_precommit_status",
            "p4_follow_up_status",
        ):
            with self.subTest(status=status):
                self.assertIn(status, source)
        self.assertIn("P4 pre-commit denial leaked the protected response body", source)
        self.assertIn("P4 follow-up request returned HTTP", source)
        self.assertIn("for expected_rule_id in 100001 100002 100003 100004", source)
        self.assertIn('grep -F "$expected_rule_id" "$PHASE4_LOG"', source)
        self.assertIn("for expected_phase4_event in 100004 response_not_committed deny", source)


if __name__ == "__main__":
    unittest.main()
