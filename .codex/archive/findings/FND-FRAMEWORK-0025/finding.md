# FND-FRAMEWORK-0025 — Codex Security rank-input helper omits all Framework PR #30 staged CI and test files

## Identity

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0025 |
| Category | tooling |
| Repository / ownership | framework / external_tool |
| Priority / severity | P2 / not_applicable |
| Confidence / status | reproduced / accepted_risk |
| Feasibility | blocked_external_dependency |
| Release blocker | false |
| Security relevant | true |

## Summary, observation, expected behavior, and impact

The Codex Security rank-input helper completed successfully in local-patch mode
for Framework PR #30 but emitted zero worklist rows even though Git reported
fourteen explicitly staged refactor files. Its static EXCLUDED_DIRS excludes ci
and tests, which removes the changed executable CI helpers and regression tests
from the generated worklist.

The generated worklist would therefore have omitted the following staged files:

| Path |
| --- |
| ci/lib/generated_report_utils.py |
| ci/lib/report_output_paths.py |
| ci/lib/runtime_path_safety.py |
| ci/provisioning/import-mrts-cases.py |
| ci/reporting/generate-case-matrix.py |
| ci/reporting/generate-connector-work-queue.py |
| ci/reporting/generate-mrts-native-report.py |
| ci/reporting/generate-phase-work-queue.py |
| ci/reporting/update-runtime-snapshot.py |
| reports/audits/change-records/20260719-01-remediate-framework-sonarcloud-quality-gate.de.md |
| reports/audits/change-records/20260719-01-remediate-framework-sonarcloud-quality-gate.md |
| tests/protocol_client/test_check_protocol_evidence.py |
| tests/security_regression/git_provenance_test_support.py |
| tests/security_regression/test_modsecurity_v3_git_ref_provenance.py |

A manually reconstructed exact staged-file inventory restored all fourteen files
to rank_input.jsonl and deep_review_input.jsonl. Each file now has a full-file
review receipt, so no PR #30 code was left unreviewed. The external-tool defect
is nevertheless independently actionable.

For a local-patch security-diff scan, the helper must emit a review row for
every changed CI and test file, including paths under ci and tests, or fail
loudly and nonzero with a coverage diagnostic. An automated regression must
compare its emitted worklist against the authoritative staged Git inventory
before downstream review consumes it.

A successful but empty worklist can falsely suggest that no relevant code exists
and could omit security-sensitive CI helpers or regression controls from
review. This record does not establish an exploitable Framework vulnerability.
Manual recovery contains the current PR #30 scan, so this finding is not a
release blocker for that PR; future scans remain at risk until the external
helper and its regression coverage are corrected.

## 2026-07-26 current-user local archive decision

The current user directed this finding to be removed from the active local
backlog because no Framework-owned repair path is presently available. Its
status is therefore `accepted_risk` for **local test-only archival**, not
`closed`, `fixed`, or `verified`. The exact decision receipt is
`.codex/runs/20260726-framework-archive-current-dispositions/evidence/archive-decision.md`
(SHA-256 `4f314bd2ca703eb0509d71546648bfb0367c3d35f2ff1a1e13c56b7f9bedcc30`).

The external Codex Security helper may still silently omit changed `ci` and
`tests` paths. Restore this full triplet to `.codex/findings/` and obtain an
external helper repair plus its coverage regression before a production,
release, or reliance decision. No fixture digest, release tag, or other
substitute is accepted as evidence for a genuine normal NGINX upstream digest.

## Scope, preconditions, reproduction, and evidence

The reproduction requires the Framework PR #30 task worktree with fourteen
explicitly staged ACMR refactor files relative to
504c8f164d4dab4bc857718af0233557ad48f727, and the Codex Security
generate_rank_input.py helper invoked with make-diff-rank-input in local-patch
mode. The helper retains static EXCLUDED_DIRS entries for ci and tests.

1. generate_rank_input.py make-diff-rank-input --repo /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/tmp/worktrees/framework-pr30-duplication-master --base 504c8f164d4dab4bc857718af0233557ad48f727 --mode local-patch
2. rtk git -C /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/tmp/worktrees/framework-pr30-duplication-master diff --cached --name-only --diff-filter=ACMR 504c8f164d4dab4bc857718af0233557ad48f727
3. rtk wc -l /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/security-diff-scan-504c8f1/artifacts/02_discovery/rank_input.jsonl /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/security-diff-scan-504c8f1/artifacts/02_discovery/deep_review_input.jsonl

Retained evidence:

- Run: 20260719T230508Z-framework-pr30-duplication-master-37469460
- Artifact: /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/security-diff-scan-504c8f1/artifacts/02_discovery/plugin_rank_input_zero_result.md
- SHA-256: da798f36a3f592140bdbae7e167cea0675bcaf5a3ce0cac679502a4f74ec6ffe
- Command: generate_rank_input.py make-diff-rank-input --repo /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/tmp/worktrees/framework-pr30-duplication-master --base 504c8f164d4dab4bc857718af0233557ad48f727 --mode local-patch
- Working directory: /root/git/ModSecurity-conector
- Exit code: 0
- Observed: 2026-07-19
- Retention: retained
- Result: the helper completed successfully with zero rows despite fourteen
  staged Framework PR #30 refactor files; the retained result records the
  static ci and tests exclusion cause.

- Run: 20260719T230508Z-framework-pr30-duplication-master-37469460
- Artifact: /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/security-diff-scan-504c8f1/artifacts/02_discovery/manual_worklist_recovery.md
- SHA-256: 58ac2336e4a735138bed74717eb3af37698f99a4e2ca9c22b400029859f666ac
- Command: rtk git -C /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/tmp/worktrees/framework-pr30-duplication-master diff --cached --name-only --diff-filter=ACMR 504c8f164d4dab4bc857718af0233557ad48f727; recover rank_input.jsonl and deep_review_input.jsonl from the exact sorted inventory
- Working directory: /root/git/ModSecurity-conector
- Exit code: 0
- Observed: 2026-07-19
- Retention: retained
- Result: the manual recovery confirms that all fourteen staged files were
  deliberately returned to the downstream security-diff worklist.

## Root cause and proposed remediation

The external Codex Security helper applies a static directory exclusion policy
that treats ci and tests as non-reviewable in local-patch mode. That policy is
incompatible with this Framework repository, where CI helpers and regression
tests implement and verify security-relevant controls. Successful completion
does not compare its empty selection with the authoritative staged Git
inventory and therefore does not fail closed.

In the external Codex Security tooling, remove the unconditional local-patch
exclusion of changed ci and tests paths, or make a zero-coverage condition a
nonzero failure with a precise diagnostic. Add an automated fixture that stages
changed ci and tests files, asserts complete rank-input coverage, and verifies
that the downstream deep-review input preserves the same path set. No
external-tool remediation is in scope for Framework PR #30.

## Acceptance criteria and validation plan

- [pending] The local-patch rank-input helper emits rows for every changed CI
  and test file, including all paths under ci and tests, or exits nonzero with
  a precise coverage diagnostic.
- [pending] An automated regression stages representative ci and tests files
  and proves that rank_input.jsonl and deep_review_input.jsonl preserve the
  complete authoritative Git path set.
- [pending] The scanner validates its generated worklist against the
  authoritative staged Git inventory before it can report a no-files result.
- [pending] A rerun on the fourteen-file PR #30 fixture reports all fourteen
  reviewable paths without manual replacement.
- [pending] No Framework source, test, CI, SonarQube setting, security control,
  Parent gitlink, or MRTS state is weakened or changed to hide this tooling
  defect.

Run an external-tool regression fixture with changed ci and tests paths and
compare its rank-input output with git diff --cached --name-only
--diff-filter=ACMR. Assert that a nonempty staged diff whose generated
worklist is empty fails nonzero and includes a coverage diagnostic. Then rerun
a focused security-diff scan and verify complete work-ledger receipts for each
emitted path. Keep the manual fourteen-file recovery evidence for Framework
PR #30 until the external-tool repair has independently passed.

## Regression and legitimate-control tests

Regression tests:

- Codex Security external-tool local-patch rank-input coverage fixture for
  changed ci and tests files.
- Codex Security external-tool worklist-versus-staged-Git-inventory parity
  test.

Legitimate controls:

- A nonempty staged diff containing ci and tests paths produces matching
  rank-input and deep-review worklist rows.
- A genuinely empty staged diff may report zero rows without a false coverage
  failure.
- A nonempty staged diff whose generated worklist is empty fails with a precise
  coverage diagnostic.

## Dependencies, boundaries, related findings, and residual risk

Dependencies are the Codex Security external-tool maintainer and release
process, a controlled external-tool regression fixture, and the retained
Framework PR #30 local-patch scan evidence. There are no current blockers or
duplicate records.

This is not a duplicate of FND-FRAMEWORK-0023 or FND-FRAMEWORK-0024. Those
findings own a SonarQube duplication remediation and a Change Record contract
failure in Framework PR #30. This finding owns the independently reproducible
external scanner worklist-selection defect that could have excluded their
changed CI and test code from security review.

Until the external helper is repaired and regression-tested, future local-patch
security-diff scans can silently omit changed CI and test controls. The current
PR #30 scan remains covered because the exact staged Git inventory was manually
reconstructed into fourteen worklist rows and all fourteen files are assigned
full-file review receipts. This finding is accepted only for local test-only
archival; it is not technically fixed, verified, or closed.

## History

- 2026-07-19 — local_patch_rank_input_omission_reproduced: the Codex Security
  helper completed at exit code 0 with zero rows against base
  504c8f164d4dab4bc857718af0233557ad48f727 while the Framework PR #30 task
  worktree held fourteen staged ACMR files. Static EXCLUDED_DIRS entries for ci
  and tests caused the omission.
- 2026-07-19 — manual_exact_inventory_recovery_completed: the exact sorted
  staged Git inventory was restored into rank_input.jsonl and
  deep_review_input.jsonl with fourteen rows each. The current PR #30 scan
  therefore has no unreviewed staged code, while the external-tool remediation
  remains out of scope.
- 2026-07-26T18:48:26Z — current_user_local_archive_risk_accepted: the current
  user accepted the unresolved external-helper residual risk for local
  test-only archival. Production, release, and technical-closure claims remain
  prohibited until the helper and coverage regression are independently fixed
  and verified.
