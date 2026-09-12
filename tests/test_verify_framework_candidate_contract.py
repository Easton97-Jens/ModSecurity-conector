"""Regression tests for the read-only Framework candidate contract verifier."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_framework_candidate_contract",
    ROOT / "ci" / "tools" / "verify-framework-candidate-contract.py",
)
assert SPEC is not None
assert SPEC.loader is not None
VERIFIER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VERIFIER
SPEC.loader.exec_module(VERIFIER)


CANDIDATE_SHA = "d4f7b69dc264852eac74e1439c0887fcb9fbe372"
CANDIDATE_COMMON = """\
NGINX_SOURCE_MODE="github-release"
NGINX_SOURCE_REPO_URL="https://github.com/nginx/nginx"
NGINX_RELEASE_TAG="release-1.31.5"
NGINX_SOURCE_GIT_REF="$NGINX_RELEASE_TAG"
NGINX_RELEASE_ASSET_NAME="nginx-${NGINX_RELEASE_TAG#release-}.tar.gz"
NGINX_SHA256="e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279"
"""


class VerifyFrameworkCandidateContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repo"
        shutil.copytree(
            ROOT,
            self.root,
            ignore=shutil.ignore_patterns(
                ".git", "ModSecurity-test-Framework", "__pycache__", ".pytest_cache"
            ),
        )
        self.common = Path(self.temporary.name) / "framework-common.sh"
        self.common.write_text(CANDIDATE_COMMON, encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def parent_bytes(self) -> dict[Path, bytes]:
        paths = {
            projection.relative_path for projection in VERIFIER.PARENT_NGINX_PROJECTIONS
        }
        paths.update(
            projection.relative_path for projection in VERIFIER.PARENT_NGINX_POLICY_PROJECTIONS
        )
        paths.update(
            {
                ".github/workflows/test-connectors-with-crs-no-mrts.yml",
                "tests/test_ci_security_workflows.py",
            }
        )
        return {self.root / path: (self.root / path).read_bytes() for path in paths}

    def test_current_parent_contract_matches_the_candidate_without_writing(self) -> None:
        before = self.parent_bytes()
        values = VERIFIER.verify_contract(self.root, CANDIDATE_SHA, self.common)
        self.assertEqual(values["release_tag"], "release-1.31.5")
        self.assertEqual(before, self.parent_bytes())
        protected_workflow = (
            self.root / ".github/workflows/nginx-root-broker.yml"
        ).read_text(encoding="utf-8")
        protected_broker = (
            self.root / "ci/runtime/broker/nginx_root_broker.py"
        ).read_text(encoding="utf-8")
        self.assertIn("NGINX_RELEASE_TAG: release-1.31.4", protected_workflow)
        self.assertIn('NGINX_PINNED_RELEASE_TAG = "release-1.31.4"', protected_broker)

    def test_stale_framework_sha_fails_closed_without_parent_writes(self) -> None:
        workflow = self.root / ".github/workflows/test-connectors-with-crs-no-mrts.yml"
        workflow.write_text(
            workflow.read_text(encoding="utf-8").replace(CANDIDATE_SHA, "0" * 40),
            encoding="utf-8",
        )
        before = self.parent_bytes()
        with self.assertRaisesRegex(VERIFIER.ContractError, "CRS/no-MRTS workflow"):
            VERIFIER.verify_contract(self.root, CANDIDATE_SHA, self.common)
        self.assertEqual(before, self.parent_bytes())

    def test_stale_framework_fixture_sha_fails_closed_without_parent_writes(self) -> None:
        fixture = self.root / "tests/test_ci_security_workflows.py"
        fixture.write_text(
            fixture.read_text(encoding="utf-8").replace(CANDIDATE_SHA, "0" * 40, 1),
            encoding="utf-8",
        )
        before = self.parent_bytes()
        with self.assertRaisesRegex(VERIFIER.ContractError, "fixture Framework SHA"):
            VERIFIER.verify_contract(self.root, CANDIDATE_SHA, self.common)
        self.assertEqual(before, self.parent_bytes())

    def test_valid_but_stale_nginx_candidate_fails_closed_without_parent_writes(self) -> None:
        stale = CANDIDATE_COMMON.replace("release-1.31.5", "release-1.31.4").replace(
            "e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279",
            "e6f20b644a17a643f059ae6467a1971fe2811587d025e071068753a1f1e3b3c3",
        )
        self.common.write_text(stale, encoding="utf-8")
        before = self.parent_bytes()
        with self.assertRaisesRegex(VERIFIER.ContractError, "unprotected NGINX handoff mismatch"):
            VERIFIER.verify_contract(self.root, CANDIDATE_SHA, self.common)
        self.assertEqual(before, self.parent_bytes())

    def test_malformed_candidate_checksum_fails_before_parent_projection(self) -> None:
        self.common.write_text(
            CANDIDATE_COMMON.replace(
                "e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279",
                "0" * 63,
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.ContractError, "canonical release tuple"):
            VERIFIER.parse_candidate_nginx_handoff(self.common)

    def test_noncanonical_candidate_tuple_fails_before_parent_projection(self) -> None:
        self.common.write_text(
            CANDIDATE_COMMON.replace(
                'NGINX_SOURCE_MODE="github-release"',
                'NGINX_SOURCE_MODE="git"',
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.ContractError, "canonical release tuple"):
            VERIFIER.parse_candidate_nginx_handoff(self.common)

    def test_alternate_nginx_assignment_forms_fail_before_parent_projection(self) -> None:
        cases = (
            '\n NGINX_SHA256="' + "0" * 64 + '"\n',
            '\nexport NGINX_SHA256="' + "0" * 64 + '"\n',
            '\nNGINX_SHA256+="x"\n',
            '\nreadonly NGINX_SHA256="' + "0" * 64 + '"\n',
            '\ndeclare -- NGINX_SHA256="' + "0" * 64 + '"\n',
            '\nlocal NGINX_SHA256="' + "0" * 64 + '"\n',
            '\ntypeset NGINX_SHA256="' + "0" * 64 + '"\n',
            "\nunset -v -- NGINX_SHA256\n",
            '\n: "${NGINX_SHA256:=invalid}"\n',
        )
        for suffix in cases:
            with self.subTest(suffix=suffix):
                self.common.write_text(CANDIDATE_COMMON + suffix, encoding="utf-8")
                with self.assertRaises(VERIFIER.ContractError):
                    VERIFIER.verify_contract(self.root, CANDIDATE_SHA, self.common)

    def test_parent_owned_nginx_provenance_flag_rejects_candidate_assignments(self) -> None:
        cases = (
            "\nNGINX_REQUIRE_PINNED_PROVENANCE=0\n",
            "\nexport NGINX_REQUIRE_PINNED_PROVENANCE=0\n",
            '\n: "${NGINX_REQUIRE_PINNED_PROVENANCE:=0}"\n',
            "\nunset NGINX_REQUIRE_PINNED_PROVENANCE\n",
        )
        for suffix in cases:
            with self.subTest(suffix=suffix):
                self.common.write_text(CANDIDATE_COMMON + suffix, encoding="utf-8")
                with self.assertRaisesRegex(
                    VERIFIER.ContractError, "NGINX_REQUIRE_PINNED_PROVENANCE"
                ):
                    VERIFIER.verify_contract(self.root, CANDIDATE_SHA, self.common)

    def test_parent_nginx_provenance_policy_requires_both_workflows(self) -> None:
        for projection in VERIFIER.PARENT_NGINX_POLICY_PROJECTIONS:
            with self.subTest(relative_path=projection.relative_path):
                target = self.root / projection.relative_path
                original = target.read_text(encoding="utf-8")
                expected = f'{projection.name}: "{projection.expected_value}"'
                self.assertIn(expected, original)
                target.write_text(
                    original.replace(expected, f'{projection.name}: "0"', 1),
                    encoding="utf-8",
                )
                before = self.parent_bytes()
                with self.assertRaisesRegex(VERIFIER.ContractError, "Parent NGINX policy"):
                    VERIFIER.verify_contract(self.root, CANDIDATE_SHA, self.common)
                self.assertEqual(before, self.parent_bytes())
                target.write_text(original, encoding="utf-8")

    def test_safe_framework_parameter_reads_and_bare_exports_are_accepted(self) -> None:
        safe_common = CANDIDATE_COMMON.replace(
            'NGINX_SHA256="e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279"\n',
            'if [ "${NGINX_SHA256+x}" = x ]; then\n'
            '    NGINX_SHA256_WAS_SET=1\n'
            "fi\n"
            'NGINX_SHA256_REQUESTED="${NGINX_SHA256-}"\n'
            'NGINX_SHA256="e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279"\n',
        ) + "export NGINX_SOURCE_MODE NGINX_SHA256\n"
        self.common.write_text(safe_common, encoding="utf-8")
        self.assertEqual(
            VERIFIER.verify_contract(self.root, CANDIDATE_SHA, self.common)["archive_sha256"],
            "e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279",
        )

    def test_each_unprotected_handoff_layer_rejects_a_representative_drift(self) -> None:
        cases = (
            (
                ".github/workflows/test-nginx-exact-head.yml",
                "NGINX_RELEASE_ASSET_NAME: nginx-1.31.5.tar.gz",
                "NGINX_RELEASE_ASSET_NAME: nginx-1.31.4.tar.gz",
                "NGINX_RELEASE_ASSET_NAME",
            ),
            (
                ".github/workflows/test-full-smoke-sequential.yml",
                "NGINX_SOURCE_GIT_REF: release-1.31.5",
                "NGINX_SOURCE_GIT_REF: release-1.31.4",
                "NGINX_SOURCE_GIT_REF",
            ),
            (
                "ci/checks/evidence/check-runtime-producer-readiness.py",
                'CANONICAL_NGINX_ARCHIVE_SHA256 = "e951607d534836624bd36b6b45a71dbfb055237deae3738da6bbf3270dada279"',
                'CANONICAL_NGINX_ARCHIVE_SHA256 = "e6f20b644a17a643f059ae6467a1971fe2811587d025e071068753a1f1e3b3c3"',
                "CANONICAL_NGINX_ARCHIVE_SHA256",
            ),
        )
        for relative_path, expected, replacement, name in cases:
            with self.subTest(relative_path=relative_path, name=name):
                target = self.root / relative_path
                original = target.read_text(encoding="utf-8")
                self.assertIn(expected, original)
                target.write_text(original.replace(expected, replacement, 1), encoding="utf-8")
                before = self.parent_bytes()
                with self.assertRaisesRegex(
                    VERIFIER.ContractError,
                    f"{relative_path}:{name}",
                ):
                    VERIFIER.verify_contract(self.root, CANDIDATE_SHA, self.common)
                self.assertEqual(before, self.parent_bytes())
                target.write_text(original, encoding="utf-8")

    def test_unsafe_candidate_expression_fails_before_parent_projection(self) -> None:
        self.common.write_text(
            CANDIDATE_COMMON.replace(
                'NGINX_SOURCE_GIT_REF="$NGINX_RELEASE_TAG"',
                'NGINX_SOURCE_GIT_REF="$(id)"',
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.ContractError, "candidate NGINX handoff"):
            VERIFIER.verify_contract(self.root, CANDIDATE_SHA, self.common)

    def test_cli_reports_the_verified_candidate(self) -> None:
        self.assertEqual(
            VERIFIER.main(
                (
                    "--repo-root",
                    str(self.root),
                    "--candidate-sha",
                    CANDIDATE_SHA,
                    "--framework-common",
                    str(self.common),
                )
            ),
            0,
        )


if __name__ == "__main__":
    unittest.main()
