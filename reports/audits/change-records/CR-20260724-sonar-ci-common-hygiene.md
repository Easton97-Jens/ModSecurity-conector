# Change Record: Parent CI/Common SonarQube Cloud hygiene remediation

**Language:** English | [Deutsch](CR-20260724-sonar-ci-common-hygiene.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260724-sonar-ci-common-hygiene |
| Date (UTC) | 2026-07-24 |
| Base revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
| Tracking | Five live Parent SonarQube Cloud Code Smells: AZ9cRyZWHhV2CayPTPwW, AZ7POyUhBW70q7L2nMJP, AZ8d8_z6E36x1qGA4xhZ, AZ9cRyZ9HhV2CayPTPwb, and AZ9cRyWTHhV2CayPTPuh. |
| Boundary | Parent ci/ checker source plus this English/German traceability pair and indexes. Framework, MRTS, gitlinks, scanner configuration, Quality Gates, suppressions, runtime connector behavior, and generated artifacts remain unchanged. |

## Motivation and problem statement

The selected SonarQube Cloud rows identify two unused private helper parameters (python:S1172) and three repeated static literals (python:S1192) in Parent CI, evidence, Common-SDK contract, and documentation checkers. The rows are maintainability Code Smells; the three S1192 rows have Sonar priority CRITICAL but only a maintainability impact, not a validated security impact.

## Acceptance criteria

- Remove only the two parameters proven unused and update their only local callers.
- Name each repeated literal once without changing its string value, checker result, control ordering, output text, or source-contract assertion.
- Pass focused Parent unit/check targets, syntax parsing, source-occurrence review, bytecode scan, and diff hygiene checks.
- Maintain complete English/German Change Records and indexes.
- Obtain exact-head GitHub and SonarQube Cloud Draft-PR evidence before describing any selected key as verified.

## Implementation decision and rationale

promotion_errors no longer accepts its unused run_dir parameter, and network_cache_status no longer accepts its unused env parameter. Repo-wide call-graph review found one local caller for each helper.

DEFAULT_WEB_SERVER_STATUSES, SUCCESS_RETURN_LITERAL, and NOT_EXECUTED_STATUS replace only same-meaning occurrences of "403,501", "return 0", and "NOT EXECUTED". The deterministic reverse-order control input "501,403" remains explicit. All former source-contract probes and error text retain their exact values.

## Security impact

The normal security assessment is not_applicable: this mechanical patch does not alter file/path handling, subprocesses, credentials, permissions, parsing, logging, scanner controls, or connector enforcement. It changes only internal unused signatures and module-local immutable constants while preserving the existing security-oriented Common-SDK source probes. No security finding is claimed fixed.

## Changed files

- ci/checks/evidence/check-full-lifecycle-evidence.py
- ci/checks/evidence/check-runtime-producer-readiness.py
- ci/checks/common/check-block-status-generator.py
- ci/checks/common/check-common-sdk-contract.py
- ci/checks/documentation/check-no-crs-doc-consistency.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

The focused commands used the Parent .venv Python,
PYTHONDONTWRITEBYTECODE=1, PYTHONNOUSERSITE=1, and a task-owned external
TMPDIR:

- rtk proxy -- env ... <Parent .venv python> -m unittest -v tests.test_full_lifecycle_evidence
- rtk proxy -- env ... <Parent .venv python> -m unittest -v tests.test_runtime_producer_readiness_path_policy
- rtk proxy -- env ... make PYTHON=<Parent .venv python> check-block-status-generator
- rtk proxy -- env ... make PYTHON=<Parent .venv python> check-common-sdk-contract
- rtk proxy -- env ... make PYTHON=<Parent .venv python> check-no-crs-doc-consistency
- rtk proxy -- env ... <Parent .venv python> -c <AST parse for the five changed modules>
- rtk proxy -- git diff --check

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused full-lifecycle unit module | passed: tests.test_full_lifecycle_evidence, 17 tests. |
| Focused runtime producer path-policy unit module | passed: tests.test_runtime_producer_readiness_path_policy, 4 tests. |
| check-block-status-generator | passed: block_status_generator: pass. |
| check-common-sdk-contract | passed: common-sdk-contract: pass. |
| check-no-crs-doc-consistency | passed: no-crs-doc-consistency: PASS. |
| AST parse of all five changed Python modules | passed. |
| Focused source-occurrence review | passed: each selected literal remains once as a module constant; both helper definitions and calls contain only their used parameters. |
| git diff --check and tracked-worktree pyc scan | passed: no whitespace errors and no bytecode files. |
| tests.test_bilingual_docs | passed: 11 tests. |
| Direct repository Change Record pair validation | passed: required sections, identity values, heading levels, and table structure match for this EN/DE pair. |

## Runtime evidence

No connector runtime behavior changed or is claimed. The checks are Parent-local source/evidence/documentation controls, not host-traffic or production-runtime evidence.

## Checks not run and rationale

- make check-runtime-producer-readiness was not run because its Make target requires check-framework; the focused Parent test module covers the changed build_payload path and Framework is out of scope.
- Connector builds, host runtime smoke tests, protocol matrices, Framework, and MRTS checks were not run because no connector/runtime code changed and Framework/MRTS are excluded.
- make check-bilingual-docs is blocked_environment only by 20 existing missing Framework-gitlink link targets. The same run reports no error in this new Change Record pair, and the direct pair validation passed.
- make check-doc-links is blocked_environment only by 16 existing missing Framework-gitlink link targets; no Framework source, gitlink, or generated artifact was changed to bypass it.
- Hosted GitHub/SonarQube Cloud exact-head verification is pending Draft-PR delivery.

## Known limitations

This batch corrects only five selected Parent SonarQube Cloud findings. It does not claim to remediate the broader 1,474-item SonarQube Cloud backlog.

## Remaining risks

An accidental constant/value mismatch could weaken a static checker. The focused checker executions, exact source-occurrence review, AST parsing, and diff review reduce that risk. Hosted exact-head analysis remains required.

## Final diff and review status

Local source implementation and focused validation are complete in an isolated Parent worktree based on 5b8db00d44ab24f3a9f4216a00f7edee977b6898. This record is not yet a delivery claim: a commit, push, unmerged Draft PR, and current-head GitHub/SonarQube Cloud/review verification remain pending.
