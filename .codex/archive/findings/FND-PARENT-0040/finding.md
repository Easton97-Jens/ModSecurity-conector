# FND-PARENT-0040 — SonarCloud flags a tainted raw-matrix fixture rewrite in PR #59

## Classification

| Field | Value |
| --- | --- |
| Category | sonarqube_finding |
| Repository / ownership | Parent / parent |
| Priority / severity | P1 / not_applicable |
| Confidence / status | validated / closed (archived) |
| Release blocker | no |
| Security relevant | yes |
| Feasibility | feasible_now |
| Exact delivery | PR #59 source `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` → Parent master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` |

## Summary

SonarCloud originally reported one open Blocker `pythonsecurity:S2083` at
`tests/test_generated_report_evidence_integrity.py:53` on PR #59 head
`34a1756635ccf30ebd74f61d5222e80230ceea17`. The fixture-only remediation
`f00eb11a25172959d50aa3e213fd1d7ace209599` is an ancestor of exact PR #59
source `b9b22cc36958ba506278f3aa3fbc1d383ea6a151`. Before its protected squash
merge, the PR Quality Gate was `OK`, the open-issue total was zero including
the original `AZ961LPTghuOJKVukVIk` S2083, all non-skipped checks and
review/thread controls passed, and no suppression, waiver, false-positive
disposition, or risk acceptance was used.

The source tree equals resulting Parent master
`5a22cbf5206dbc2b7f53a9f961d72e37d567e188`. Retained detached-master
validation passed the 57/57 evidence-integrity suite. The 2026-07-26 closure
audit rechecked both retained artifact hashes and confirmed that the sole
affected test file is unchanged from that resulting-master proof. This finding
is **closed** and no longer its own release blocker. The independent
`FND-SONAR-0001` master Quality Gate failure remains unaccepted and is not
attributed to this finding.

## Observed and expected behavior

On observed head `34a1756`, `replace_raw_matrix_job()` parsed the raw matrix
with `read_text()` and wrote serialized rows with `write_text()`. Its two
callers use a known temporary fixture manifest. The fixture already constructs
the complete twelve-row matrix in memory. The required behavior is therefore to
update that controlled collection and write the fixed JSONL manifest without
rereading a taint-classified serialized record.

## Affected files and symbols

- `tests/test_generated_report_evidence_integrity.py` —
  `replace_raw_matrix_job`, `GeneratedReportEvidenceIntegrityTests.build_valid_run`,
  `GeneratedReportEvidenceIntegrityTests.raw_matrix_job`,
  `test_direct_summary_path_is_accepted`, and
  `test_summary_hash_mismatch_is_rejected_for_each_canonical_path`

## Impact, preconditions, and reproduction

The original proven impact was a failed mandatory SonarCloud Security Rating A
gate, not a confirmed runtime compromise: only trusted test code calls the
helper under `TemporaryDirectory`, and no deployed caller or untrusted request
route reaches it. The exact source and resulting-master controls now verify
that the scanner finding no longer reproduces without suppressing it.

The original reproduction queried SonarCloud issue
`AZ961LPTghuOJKVukVIk` for PR #59 and observed `pythonsecurity:S2083`, type
`VULNERABILITY`, status `OPEN`, source at line 49, and sink at line 53. Fresh
exact-source evidence instead observed Quality Gate `OK` and zero open PR #59
issues, including that original S2083. Local Git evidence also confirms:

- `f00eb11a25172959d50aa3e213fd1d7ace209599` is an ancestor of
  `b9b22cc36958ba506278f3aa3fbc1d383ea6a151`.
- `git diff --quiet b9b22cc36958ba506278f3aa3fbc1d383ea6a151
  5a22cbf5206dbc2b7f53a9f961d72e37d567e188` succeeds.

## Evidence

| Run ID | Artifact | SHA-256 | Result |
| --- | --- | --- | --- |
| 20260719T151258Z-pr59-docs-security-diff-34a1756-fdbfdba6 | `/var/tmp/codex/ModSecurity-conector/runs/20260719T151258Z-pr59-docs-security-diff-34a1756-fdbfdba6/evidence/pr59-34a-sonar-open-issues.json` | `5e412d7b97c5a716460f2c15088288d2d0abc69e80a5dfdd69657024ab905e5e` | Original evidence: exactly one open Blocker `pythonsecurity:S2083` at test line 53. |
| 20260720T141403Z-pr55-pr59-master-integration-8a0b8640 | `/var/tmp/codex/ModSecurity-conector/runs/20260720T141403Z-pr55-pr59-master-integration-8a0b8640/evidence/pr59-5a22cbf-postmerge-validation.json` | `7749e6c6fd1ab198b54eb9704221d30aa150954db6130bec0317801a8afddc51` | Exact source `b9b22cc` passed Quality Gate `OK`, zero open issues including S2083, all non-skipped checks, required contexts, and review/thread controls; protected squash merge produced equal-tree master `5a22cbf`; detached-master controls passed 57/57 integrity, 11/11 bilingual, shell syntax, whitespace diff, and clean/no-`.pyc`. |

## Root cause and remediation

The helper reread a serialized raw-matrix record before writing a replacement
although the fixture already owned the corresponding in-memory records. The
implemented remediation passes controlled in-memory rows to the rewrite helper
and obtains mutable test jobs with `deepcopy` from the same fixture collection,
preserving JSONL format and direct-summary/hash-mismatch controls. It neither
suppresses nor dismisses SonarCloud and does not change production checker
behavior. The implementation was delivered through exact source `b9b22cc` and
verified on equal-tree Parent master `5a22cbf`.

## Acceptance criteria

- No raw-matrix update helper rereads serialized fixture rows before writing a
  replacement.
- The fixture remains a complete twelve-job matrix with direct-summary and
  hash-mismatch controls preserved.
- `tests.test_generated_report_evidence_integrity` passes with the valid
  full-matrix and negative evidence-integrity controls.
- Exact PR #59 source `b9b22cc` has Quality Gate `OK` and zero open SonarCloud
  issues including the original S2083, without suppression, waiver,
  false-positive disposition, or risk acceptance.
- Protected-merged Parent master `5a22cbf` has the same tree as `b9b22cc` and
  passes the retained 57/57 evidence-integrity suite.

## Validation and regression/control tests

- `git merge-base --is-ancestor f00eb11a25172959d50aa3e213fd1d7ace209599
  b9b22cc36958ba506278f3aa3fbc1d383ea6a151` passed.
- The exact PR Quality Gate and issue query passed; all non-skipped CI,
  required protected contexts, and zero review/thread controls passed before
  the protected squash merge with `--match-head-commit`.
- `tests.test_generated_report_evidence_integrity` passed **57/57** on
  resulting Parent master `5a22cbf`, including valid full-matrix and forged
  result, identity, path, symlink, checksum, incomplete-matrix, seal,
  intermediate/publication, and post-validation/command-receipt swap controls.
- `tests.test_bilingual_docs` passed **11/11**; `sh -n
  ci/runtime/lifecycle/run-full-matrix-parallel.sh` and `git diff --check
  5a22cbf5206dbc2b7f53a9f961d72e37d567e188^
  5a22cbf5206dbc2b7f53a9f961d72e37d567e188` passed.
- A valid full twelve-job matrix and valid direct canonical summary update
  remain accepted; direct and force-all digest mismatches remain rejected.

## Dependencies and blockers

This finding has no remaining release-blocking dependency and is closed.
No suppression, waiver, false-positive disposition, or risk acceptance was
used. `FND-SONAR-0001` remains a separate, unaccepted aggregate Parent-master
SonarCloud Quality Gate blocker; it neither reopens nor is attributed to
FND-PARENT-0040. No Framework, MRTS, or gitlink action occurred.

## Related findings

- `FND-PARENT-0030` — broader strict report-evidence gate boundary.
- `FND-PARENT-0039` — paired Change Record delivery traceability correction.
- `FND-SONAR-0001` — independent unaccepted Parent-master SonarCloud blocker.

## Residual risk

The closed fixture-specific scanner finding has no remaining own release
blocker. Aggregate Parent-master delivery remains partial only because
independent `FND-SONAR-0001` still fails its SonarCloud Quality Gate; that
separate blocker is neither accepted nor suppressed and does not reopen this
finding.

## History

- 2026-07-19T15:15:00Z — `confirmed_exact_head_sonar_blocker`: retained API
  evidence confirmed the single open `pythonsecurity:S2083` issue on the exact
  PR #59 head. The minimal fixture-only remediation began.
- 2026-07-19T15:34:20Z — `fixture_remediation_validated_locally_pending_commit`:
  the helper rewrote only the in-memory twelve-job collection and both callers
  obtained independent jobs. Local tests and dataflow review passed; delivery
  evidence remained pending.
- 2026-07-19T15:47:07Z — `fixture_remediation_committed_locally_pending_push`:
  the reviewed fixture correction was committed as `f00eb11a25172959d50aa3e213fd1d7ace209599`.
- 2026-07-19T15:53:32Z — `fixture_remediation_normal_push_completed`: that
  commit was pushed normally without force; exact-head remote evidence remained
  pending.
- 2026-07-20T15:13:08Z — `verified_on_protected_pr59_squash_merge_parent_master`:
  `f00eb11a` was verified as an ancestor of exact source `b9b22cc`; fresh PR
  evidence passed Quality Gate `OK`, zero open issues including
  `AZ961LPTghuOJKVukVIk`, all non-skipped/required checks, and zero
  review/thread controls. The protected squash merge with `--match-head-commit`
  produced equal-tree Parent master `5a22cbf`. Retained detached-master
  validation passed the original and alternate negative controls plus the
  valid control (57/57), 11/11 bilingual tests, shell syntax, whitespace diff,
  and clean/no-`.pyc` checks. The finding transitions from `fixed` to
  `verified`, never `closed`; its own release blocker is false. `FND-SONAR-0001`
  remains separate and unaccepted.
- 2026-07-26T11:35:17Z — `closed_after_current_path_and_retained_evidence_revalidation`:
  the user-directed closure audit rechecked the original S2083 proof and the
  legitimate full-matrix controls, verified both retained artifact SHA-256
  values, and confirmed that the sole affected file remains unchanged from
  Parent master `5a22cbf` through current Parent HEAD `02642a4`. No source,
  scanner/gate, Framework, MRTS, Gitlink, suppression, waiver, false-positive,
  or risk-acceptance change occurred. The independent `FND-SONAR-0001` remains
  open and does not reopen this finding.
