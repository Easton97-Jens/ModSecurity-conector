# FND-SONAR-0006 — Parent PR #59 exact head has eight task-owned SonarQube Cloud maintainability CODE_SMELLs

## Classification

| Field | Value |
| --- | --- |
| ID | FND-SONAR-0006 |
| Category | sonarqube_finding |
| SonarQube Cloud classification | maintainability |
| Repository / ownership | parent / parent |
| Priority | P2 |
| Security severity | not_applicable |
| Confidence | validated |
| Status | verified (not closed) |
| Feasibility | already_fixed |
| Release blocker | false |
| Security relevant | false |
| Connector / protocol / profile | null / null / null |
| Final disposition | verified_on_parent_master_5a22cbf5206dbc2b7f53a9f961d72e37d567e188_not_closed |

The SonarQube Cloud scanner labels are six CRITICAL and two MAJOR observations. They are scanner labels only, not security severities: this is a non-security maintainability finding with severity not_applicable, security_relevant false, and release_blocker false.

## Summary

The retained SonarQube Cloud issue query for Parent PR #59 head 841d5d66ba6db852cbc3c0a906e56d74583beb89 against base 6f80c90592fdd1f2eb990fe1514fdfc4efbf01e8 reports eight task-owned CODE_SMELL observations on changed Parent lines. The Quality Gate is OK; all observations are non-security maintainability findings. Exact source b9b22cc36958ba506278f3aa3fbc1d383ea6a151 delivered a behavior-preserving, non-suppressive remediation and was protected-squash-merged as Parent master 5a22cbf5206dbc2b7f53a9f961d72e37d567e188. The retained post-merge receipt records the required controls and zero remaining original keys on master; this finding is verified, not closed.

## Observed and expected behavior

The exact-head issue query reports total=8, open_security_hotspots=0, and open_vulnerabilities=0. The retained receipt classifies every result as a SonarQube Cloud CODE_SMELL maintainability finding, and its ownership assessment says all components are changed Parent paths and all reported lines are inside the current PR diff. It records Quality Gate OK, new reliability, security, and maintainability ratings of 1, duplicated-lines density 0.0, and security-hotspots reviewed 100.0.

The focused PR #59 remediation at b9b22cc36958ba506278f3aa3fbc1d383ea6a151 preserves observable behavior while reducing the rule-specific complexity, nesting, exception-test, and duplicated-literal smells. Its fresh PR Quality Gate was OK, and the resulting-master query at 5a22cbf5206dbc2b7f53a9f961d72e37d567e188 shows all eight observations as zero remaining, without NOSONAR, rule disabling, exclusions, a Quality Gate change, or a false-positive disposition.

## Impact

The Quality Gate remains passing, and these observations are neither a security condition nor a release blocker. If left unresolved, they increase complexity and maintenance cost in report-layout, lifecycle, receipt, and evidence-test code. CRITICAL and MAJOR must not be reinterpreted as security severity or as release-blocker status.

## Affected files, rules, and exact issue inventory

Affected files:

- ci/checks/documentation/check-generated-report-layout.py
- ci/evidence/reports/generate-full-matrix-job-completeness.py
- ci/runtime/lifecycle/run-verified-report-run.py
- tests/test_generated_report_evidence_integrity.py
- ci/lib/verified_full_matrix_receipt.py

Affected rule/symbol identifiers are python:S3776, python:S1066, python:S5778, python:S1192, and the SonarQube Cloud PR #59 exact-head issue query.

| Key | Rule | Scanner label | File | Line | Message |
| --- | --- | --- | --- | ---: | --- |
| AZ98bS-YZDHgEby5GFdC | python:S3776 | CRITICAL | ci/checks/documentation/check-generated-report-layout.py | 1128 | Reduce cognitive complexity from 36 to 15 |
| AZ98bS_lZDHgEby5GFdG | python:S3776 | CRITICAL | ci/evidence/reports/generate-full-matrix-job-completeness.py | 496 | Reduce cognitive complexity from 20 to 15 |
| AZ98bS_GZDHgEby5GFdE | python:S3776 | CRITICAL | ci/runtime/lifecycle/run-verified-report-run.py | 636 | Reduce cognitive complexity from 18 to 15 |
| AZ98bS_GZDHgEby5GFdF | python:S3776 | CRITICAL | ci/runtime/lifecycle/run-verified-report-run.py | 798 | Reduce cognitive complexity from 18 to 15 |
| AZ98bS_GZDHgEby5GFdD | python:S1066 | MAJOR | ci/runtime/lifecycle/run-verified-report-run.py | 1751 | Merge the nested if statement with its enclosing condition |
| AZ98bTAcZDHgEby5GFdI | python:S5778 | MAJOR | tests/test_generated_report_evidence_integrity.py | 729 | Keep only one potentially throwing invocation in the exception test |
| AZ98bS59ZDHgEby5GFc_ | python:S1192 | CRITICAL | ci/lib/verified_full_matrix_receipt.py | 57 | Define a constant for the duplicated verified_run_id error literal |
| AZ98bS59ZDHgEby5GFdA | python:S3776 | CRITICAL | ci/lib/verified_full_matrix_receipt.py | 457 | Reduce cognitive complexity from 24 to 15 |

## Preconditions and reproduction

Preconditions:

- The retained receipt is bound to Parent PR #59 head 841d5d66ba6db852cbc3c0a906e56d74583beb89 and base 6f80c90592fdd1f2eb990fe1514fdfc4efbf01e8.
- The receipt records Quality Gate OK, zero open security hotspots, and zero open vulnerabilities for that exact-head query.
- The receipt's ownership assessment establishes that all eight components are changed Parent paths and all listed lines are within the current diff.
- Any remediation remains Parent-owned, behavior-preserving, and non-suppressive; Framework and MRTS are out of scope.

To reproduce the recorded observation:

1. Read the retained JSON below and confirm pull_request=59, the exact head and base SHAs, quality_gate.status=OK, and issue_query.total=8.
2. Run the recorded integrity command and compare its SHA-256 result.
3. For a remediation result, obtain a fresh SonarQube Cloud PR analysis bound to the exact remediation head and check the Quality Gate plus every key in the inventory table.

## Evidence

| Field | Value |
| --- | --- |
| Run ID | 20260720T141403Z-pr55-pr59-master-integration-8a0b8640 |
| Artifact | /var/tmp/codex/ModSecurity-conector/runs/20260720T141403Z-pr55-pr59-master-integration-8a0b8640/evidence/sonar-pr59-841d5d6-maintainability.json |
| Artifact type | exact_pr_head_sonarqube_cloud_maintainability_issue_query |
| SHA-256 | 538bb94b4716979d1b75fb95b4cff97a3d4d47710b2592fc35ce5b285c2e4222 |
| Integrity command | rtk sha256sum /var/tmp/codex/ModSecurity-conector/runs/20260720T141403Z-pr55-pr59-master-integration-8a0b8640/evidence/sonar-pr59-841d5d6-maintainability.json |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-20T14:35:23Z |
| Retention | retained_task_evidence |

The retained JSON is the exact-head SonarQube Cloud PR #59 issue-query receipt.

The second retained receipt records the local remediation at source commit b9b22cc36958ba506278f3aa3fbc1d383ea6a151 (`refactor: resolve PR 59 Sonar maintainability findings`). It is local validation evidence, not a fresh remote SonarQube Cloud result.

| Field | Value |
| --- | --- |
| Source commit | b9b22cc36958ba506278f3aa3fbc1d383ea6a151 |
| Artifact | /var/tmp/codex/ModSecurity-conector/runs/20260720T141403Z-pr55-pr59-master-integration-8a0b8640/evidence/pr59-b9b22cc-local-sonar-remediation-validation.json |
| Artifact type | local_sonar_maintainability_remediation_validation |
| SHA-256 | c78e125ceb25956b25cd248bad1d04e83221a1bf2a332360148dc67005ed9e53 |
| Observed at | 2026-07-20T14:48:00Z |
| Retention | retained_task_evidence |
| Local result | 57/57 evidence-integrity tests passed; shell syntax passed; bilingual documentation 11/11 passed; git diff --check passed; independent focused five-file receipt/path/TOCTOU security review passed. |

The third retained receipt is the protected-merge and resulting-master verification. It supersedes the earlier local-only delivery wording in this record.

| Field | Value |
| --- | --- |
| Exact source / merge method | b9b22cc36958ba506278f3aa3fbc1d383ea6a151 / protected squash merge with `--match-head-commit` |
| Resulting Parent master | 5a22cbf5206dbc2b7f53a9f961d72e37d567e188 |
| Artifact | /var/tmp/codex/ModSecurity-conector/runs/20260720T141403Z-pr55-pr59-master-integration-8a0b8640/evidence/pr59-5a22cbf-postmerge-validation.json |
| Artifact type | postmerge_pr59_master_verification |
| SHA-256 | 7749e6c6fd1ab198b54eb9704221d30aa150954db6130bec0317801a8afddc51 |
| Observed at | 2026-07-20T15:13:08Z |
| Result | 57/57 evidence-integrity, 11/11 bilingual documentation, shell syntax, and merge-diff whitespace controls passed; the PR Quality Gate was OK and all eight original keys query zero on master. |
| Independent boundary | FND-SONAR-0001 remains an unaccepted master Quality Gate failure; it is not attributed to this finding. |

## Root-cause analysis

The exact-head query identifies independently scoped maintainability smells: five cognitive-complexity locations, one nested-condition rule, one exception-test rule, and one duplicated-literal rule. The evidence establishes task ownership and classification, but does not establish a security vulnerability or hotspot. Detailed source-level refactoring design remains part of the planned remediation.

## Remediation and completed verification

Commit b9b22cc36958ba506278f3aa3fbc1d383ea6a151 applied a small behavior-preserving Parent-only refactor for each reported location:

- Extract or simplify helpers while preserving inputs, outputs, error handling, ordering, and fail-closed behavior.
- Merge the nested condition only when it is logically equivalent.
- Keep one potentially throwing call in the exception assertion while retaining the test's intended coverage.
- Replace the duplicated verified_run_id error literal with one named constant.
- Preserve focused regression coverage for report layout, full-matrix receipt, verified-report lifecycle, and evidence integrity.

The retained receipts record forbidden_controls_changed=false. No NOSONAR, rule suppression, rule disabling, exclusion, Quality Gate change, or false-positive disposition was used. Fresh non-skipped CI, CodeQL, PR Sonar Quality Gate OK, and zero-review/thread controls preceded the protected merge; the exact resulting-master evidence then passed. The finding is verified, not closed.

## Acceptance criteria

1. Passed: a fresh SonarQube Cloud PR analysis was bound to exact source b9b22cc36958ba506278f3aa3fbc1d383ea6a151 and reported Quality Gate OK.
2. Passed: the resulting-master query at 5a22cbf5206dbc2b7f53a9f961d72e37d567e188 reports all eight listed keys as zero remaining, with no suppression, exclusion, rule disablement, Quality Gate change, or false-positive disposition.
3. Passed: the retained post-merge receipt records 57/57 focused evidence-integrity tests, shell syntax, 11/11 bilingual documentation tests, and merge-diff whitespace validation passing; the independent focused five-file receipt/path/TOCTOU security review also passed.
4. Passed: the refactors preserved public and operational behavior, including validation, error handling, output, ordering, and fail-closed controls.
5. Passed: evidence remains SHA-addressed and the English, German, index, backlog, and roadmap records are synchronized.

## Validation plan

1. Completed in the retained local receipt: each focused refactor was inspected against the original conditional, error, output, ordering, and validation behavior.
2. Completed in the retained local receipt: the smallest relevant local regression tests and legitimate controls ran and their exact results were retained.
3. Completed: SonarQube Cloud reported Quality Gate OK for exact source b9b22cc36958ba506278f3aa3fbc1d383ea6a151, and the resulting-master query reports all eight original issue keys as zero.
4. Completed: the retained evidence records no prohibited control change; the fresh GitHub, CodeQL, PR Sonar, review, and thread controls passed before the protected merge.

## Regression and legitimate-control tests

The retained local receipt reports this regression and legitimate-control evidence:

- `tests/test_generated_report_evidence_integrity.py`: 57/57 tests passed, including valid full-matrix control and receipt/path/hash/symlink/TOCTOU negative controls.
- `sh -n ci/runtime/lifecycle/run-full-matrix-parallel.sh`: passed.
- `tests.test_bilingual_docs`: 11/11 tests passed.
- `git diff --check`: passed.
- Independent focused five-file receipt/path/TOCTOU security review: passed; final TOCTOU revalidation and fail-closed controls were preserved.

The retained local and resulting-master results support the verified status. Closure remains a separate lifecycle decision and is not implied by this merge.

## Dependencies, blockers, and related findings

- Dependency: none remaining for verification; FND-SONAR-0001 is a separate, unaccepted Parent-master Quality Gate blocker.
- Blocked by: none.
- Duplicates: none. The eight keys were checked against the existing FND-SONAR records and are unique.
- Related findings: FND-SONAR-0001 and FND-PARENT-0040; both are distinct from this non-security P2 maintainability finding.
- Source run: 20260720T141403Z-pr55-pr59-master-integration-8a0b8640.

## Residual risk

The eight original task-owned keys are verified absent on Parent master 5a22cbf5206dbc2b7f53a9f961d72e37d567e188, with no risk acceptance, suppression, or scanner-control change. This finding remains verified rather than closed pending a separate lifecycle decision. FND-SONAR-0001 remains an independent, unaccepted Parent-master Quality Gate failure and leaves aggregate delivery partial; it is not attributed to this finding.

## History

| At | Event | Detail |
| --- | --- | --- |
| 2026-07-20T14:39:40Z | exact_pr59_head_maintainability_finding_created | Created after independent SHA-256 verification of the retained exact-head receipt. Eight unique task-owned Parent CODE_SMELLs were deduplicated against existing FND-SONAR records; six CRITICAL and two MAJOR values are non-security scanner labels only. |
| 2026-07-20T15:03:04Z | local_non_suppressive_remediation_fixed | Source commit b9b22cc36958ba506278f3aa3fbc1d383ea6a151 is recorded fixed after retained local evidence: 57/57 evidence-integrity tests, shell syntax, bilingual documentation 11/11, git diff --check, and independent focused five-file receipt/path/TOCTOU security review passed. Fresh remote exact-head validation remains required; status is not verified or closed. |
| 2026-07-20T15:13:08Z | verified_on_protected_pr59_squash_merge_parent_master | Exact source b9b22cc36958ba506278f3aa3fbc1d383ea6a151 was protected-squash-merged as Parent master 5a22cbf5206dbc2b7f53a9f961d72e37d567e188. Fresh non-skipped CI, CodeQL, PR Sonar Quality Gate OK, and zero-review/thread controls passed before merge; retained resulting-master evidence records 57/57 evidence-integrity, 11/11 bilingual, shell syntax, and diff controls passing plus zero of the eight original keys. No suppression, scanner/gate change, false-positive disposition, or risk acceptance occurred. FND-SONAR-0001 remains independent and unaccepted. Status is verified, not closed. |
