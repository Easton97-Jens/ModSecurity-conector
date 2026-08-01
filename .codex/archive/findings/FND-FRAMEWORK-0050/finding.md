# FND-FRAMEWORK-0050 — Framework test assertions reverse actual and expected arguments

## Classification

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0050 |
| Category | sonarqube_finding |
| SonarQube Cloud classification | maintainability |
| Repository / ownership | framework / framework |
| Priority / severity | P2 / not_applicable |
| Confidence / status | validated / fixed |
| Feasibility | feasible_now |
| Release blocker / security relevant | true / false |
| Final disposition | framework_pr47_s3415_local_remediation_fixed_pending_exact_head_hosted_confirmation |

### PR #47 follow-up — 2026-07-26

The exact initial head `3bbb2e806f4892e8f92476e35740d149b8b9b17b` of
Framework PR #47 has one task-owned `python:S3415` diagnostic in
`tests/ci_security/test_ci_security_contract.py`. It is the same unittest
`actual, expected` positional-order root cause as this canonical record and is
therefore deduplicated here.

The retained SonarQube Cloud inventory is
`/var/tmp/codex/ModSecurity-conector/runs/20260726T105400Z-framework-pr47-sonar-merge/evidence/sonar-pr47-initial-issue-inventory.json`,
SHA-256 `d98ef7664e411e8d6f820eec8a4b8b82e9501fcf5aabf42e9b7a1cd857006937`.
The local repair corrects the assertion order and extends direct rejection
coverage. The focused CI-security contract suite and workflow/documentation
controls passed locally. A fresh SonarQube Cloud analysis for the subsequently
submitted exact PR head remains required; no test or scanner control changed.

## Summary, observed behavior, and impact

### Framework PR #43 exact-head verification — 2026-07-23

The normal Framework-only Draft PR [#43](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/43)
was created from `agent/framework-sonarqube-test-issues-507` against `master`.
Its local worktree, remote branch, and GitHub PR head are all exact commit
`4c55bb2855b8e0196fe54cb0c6f90f43aa993962`; its base is
`935cf14c676a24672be5c336e92cd13457cc35c8`. No merge or master update was
performed.

SonarQube Cloud analyzed that exact PR head at `2026-07-23T10:39:35+0000`.
The Quality Gate is `OK`, the PR has zero open `python:S3415` issues and zero
open issues overall, and its Sonar summary is zero bugs, vulnerabilities, and
code smells. The terminal GitHub PR checks passed, including SonarCloud Code
Analysis, CodeQL for actions/Python/C++, secret scanning, OSV, Scorecard,
structure, action-version, and scaffold-lint checks. The retained delivery
receipt is
`/var/tmp/codex/ModSecurity-conector/runs/20260723T092456Z-framework-sonarqube-test-issues-507-10387697/evidence/framework-pr43-delivery-verification.md`,
SHA-256 `1d70d068c9c3079de55abc76a7271a5fc37b20454a4fb3f99a29cbb68c0d052b`.

This verifies the current 507-key remediation at the submitted Draft-PR head;
it does not authorize a merge or claim to resolve the separate MRTS-only
`FND-SONAR-0002` master condition.

### Resulting-master verification after PR #43 — 2026-07-23

GitHub normally merged PR [#43](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/43)
with exact-head protection at `2026-07-23T11:24:30Z`. Its exact source
`4c55bb2855b8e0196fe54cb0c6f90f43aa993962` is the second parent of resulting
Framework master `f98a8739cb13b583f23d646784b144e596b61441`.

Exact resulting-master SonarQube Cloud analysis
`77e255d6-17a2-4e8a-bb29-6438e91e6fa8` has zero open `python:S3415` issues.
The resulting Quality Gate is `ERROR` solely on New Security Rating C (actual
`3`, threshold `1`) from nine read-only MRTS vulnerability signals tracked by
the independent `FND-SONAR-0002`; it is not evidence of a regression in this
assertion-order remediation. `test-common`, OpenSSF Scorecard, lint, and
CodeQL analysis completed successfully; the PR-only head job was intentionally
skipped on the master trigger. Parent and MRTS stayed unchanged. The retained
post-merge receipt is
`/var/tmp/codex/ModSecurity-conector/runs/20260723T092456Z-framework-sonarqube-test-issues-507-10387697/evidence/framework-pr43-postmerge-master-verification.md`,
SHA-256 `d8a63662d10def3118b5795c90474a0c63ab9a96a82d5e93debb8436c79bd79c`.

### Current master extension — 2026-07-23

The current Framework `master` SonarQube Cloud analysis
`dda3ea04-2721-4ee6-a9c1-74bd2925f139` at exact revision
`935cf14c676a24672be5c336e92cd13457cc35c8` reports 507 unresolved
`python:S3415` MAJOR CODE_SMELL diagnostics. They are Framework-owned test
locations in 29 files: 262 under `tests/security_regression/`, 220 under
`tests/no_crs/`, 23 under `tests/protocol_client/`, and 2 under
`tests/makefile_contract/`. The complete current inventory is retained at
`/var/tmp/codex/ModSecurity-conector/runs/20260723T092456Z-framework-sonarqube-test-issues-507-10387697/evidence/sonar-master-s3415-inventory.md`,
SHA-256
`0e9f549877fc1da2d3c629073e966e51f101348e913641cc7f539b29896379ef`.

The paginated unresolved query returns 500 items on page 1 and 7 on page 2.
Every item carries the same message: “Swap these 2 arguments so they are in
the correct order: actual value, expected value.” This remains the same
canonical assertion-order cause as the historical fifteen PR #42 keys, so it
extends this finding rather than allocating a duplicate. It is not limited to
`assertEqual`: representative current locations also include `assertNotEqual`.

The 507 are non-security maintainability items and are not the reason the
current master Quality Gate is ERROR. The independent Security-C condition is
caused by nine read-only `tools/MRTS/mrts/**` scanner signals and remains
tracked by `FND-SONAR-0002`; this Framework test-order remediation must not
claim to repair it or modify MRTS.

### Historical PR #42 observation

The public SonarQube Cloud query for Framework PR #42 exact head
`1fd3b362e0fed9766c6920e3c7bd1939535850f2` reports fifteen open CODE_SMELL
diagnostics under `python:S3415`. Each identifies a `unittest.assertEqual`
invocation whose expected value is passed before its actual value. That reduces
failure-message clarity without changing the asserted equality relation.

The retained initial inventory is
`/var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/sonar-pr42-initial-issue-inventory.md`,
SHA-256
`7d4c5cff26e885de37c1090713e7fe947e409c1478f3dcd6a69809ddd3401d44`.
It records one issue in `test_fetch_security_tool.py`, seven in
`test_update_workflow_tools.py`, and seven in `test_parser_hardening.py`. All
42 exact-head issues are CODE_SMELL; this finding owns only the fifteen
assertion-order items.

This is a non-security maintainability finding: severity is `not_applicable`
and `security_relevant` is false. It is release-blocking because the user
selected remediation of all 42 PR #42 new issues before master integration.
Reordering the arguments must not weaken the parser-hardening or CI-security
controls exercised by these tests.

The local correction is complete: all fifteen calls now use `actual, expected`
order, the three direct modules passed 49 tests, the full native `make lint`
target passed, and the combined 22-path security scan reported no finding
(report SHA-256
`1b85288ff20d4c4f04443a9f2e4ba6ce07b69967e165dcc2d3c02257dfc6da36`). The
selected local interpreter is CPython `3.14.4` while the checked-in target is
`3.14.6`; neither local result substitutes for fresh exact submitted-head
SonarQube Cloud or hosted Python evidence.

## Expected behavior and proposed remediation

Every affected unittest assertion must use `actual, expected` ordering while
preserving the same relation, messages, fixtures, test execution path, and
security-regression behavior. The historical fifteen PR #42 corrections remain
part of this record; the active scope is the 507 current-master keys. Retain
only the reviewed positional-argument changes; do not change a test
expectation, remove parser-hardening coverage, or suppress the rule. Where an
argument expression has side effects, preserve evaluation order through a
reviewed local temporary instead of blindly swapping expressions.

A fresh exact-head SonarQube Cloud PR analysis must show all fifteen original
`S3415` keys absent without `NOSONAR`, suppression, false-positive marking,
exclusion, rule change, or Quality Gate change.

## Affected files and symbols

- `tests/ci_security/test_fetch_security_tool.py`: `AZ-K30-bbx6VBofpXBhx`
- `tests/ci_security/test_update_workflow_tools.py`: `AZ-K30_Ibx6VBofpXBhz`,
  `AZ-K30_Ibx6VBofpXBh0`, `AZ-K30_Ibx6VBofpXBh1`,
  `AZ-K30_Ibx6VBofpXBh2`, `AZ-K30_Ibx6VBofpXBh3`,
  `AZ-K30_Ibx6VBofpXBh4`, `AZ-K30_Ibx6VBofpXBh5`
- `tests/security_regression/test_parser_hardening.py`:
  `AZ-K306Vbx6VBofpXBhr`, `AZ-K306Vbx6VBofpXBhs`,
  `AZ-K306Vbx6VBofpXBhq`, `AZ-K306Vbx6VBofpXBht`,
  `AZ-K306Vbx6VBofpXBhu`, `AZ-K306Vbx6VBofpXBhv`,
  `AZ-K306Vbx6VBofpXBhw`
- Rule: `python:S3415`

### Current master scope

- Revision / analysis: `935cf14c676a24672be5c336e92cd13457cc35c8` /
  `dda3ea04-2721-4ee6-a9c1-74bd2925f139`.
- Count / ownership: 507 Framework-owned test diagnostics in 29 files;
  `tests/security_regression/` 262, `tests/no_crs/` 220,
  `tests/protocol_client/` 23, and `tests/makefile_contract/` 2.
- Exact paths and line-level inventory: retained in the current-master
  evidence artifact above. The source mapping and diff review must resolve
  every path before delivery.

## Preconditions and reproduction

1. For the active current-master scope, query SonarQube Cloud for project
   `Easton97-Jens_ModSecurity-test-Framework`, `branch=master`,
   `statuses=OPEN`, `rules=python:S3415`, `ps=500`, pages 1 and 2. Verify
   `total=507` (500 then 7) and the exact analysis/revision binding above.
2. Inspect each current reported test source location. Its pre-remediation
   assertion passes expected before actual; preserve side-effect evaluation
   order where present.
3. Historical PR #42 reproduction: query SonarQube Cloud for project
   `Easton97-Jens_ModSecurity-test-Framework`, `pullRequest=42`,
   `issueStatuses=OPEN,CONFIRMED`, `sinceLeakPeriod=true`, and `ps=500`.
4. Read the historical retained inventory and verify SHA-256
   `7d4c5cff26e885de37c1090713e7fe947e409c1478f3dcd6a69809ddd3401d44`.
5. Filter `python:S3415`; the historical initial count is fifteen.
6. Inspect the three historical test files. Before remediation each recorded
   location uses `assertEqual(expected, actual)` ordering.

## Evidence

| Field | Value |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/sonar-pr42-initial-issue-inventory.md |
| Artifact type | task_owned_sonarqube_cloud_pr42_initial_inventory |
| SHA-256 | 7d4c5cff26e885de37c1090713e7fe947e409c1478f3dcd6a69809ddd3401d44 |
| Command | `rtk run curl -fsSL https://sonarcloud.io/api/issues/search --get --data-urlencode componentKeys=Easton97-Jens_ModSecurity-test-Framework --data-urlencode pullRequest=42 --data-urlencode issueStatuses=OPEN,CONFIRMED --data-urlencode sinceLeakPeriod=true --data-urlencode ps=500` |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-22T18:18:47Z |
| Retention status | task_owned_retained_evidence |

| Field | Framework PR #43 exact-head delivery verification |
| --- | --- |
| Run ID | 20260723T092456Z-framework-sonarqube-test-issues-507-10387697 |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260723T092456Z-framework-sonarqube-test-issues-507-10387697/evidence/framework-pr43-delivery-verification.md |
| Artifact type | framework_pr43_exact_head_delivery_verification |
| SHA-256 | 1d70d068c9c3079de55abc76a7271a5fc37b20454a4fb3f99a29cbb68c0d052b |
| Command | Exact local/remote/PR-head comparison; `gh pr checks 43`; SonarQube Cloud PR quality-gate, issue, and pull-request queries |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-23T10:41:53Z |
| Retention status | task_owned_retained_evidence |

| Field | Local remediation validation |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-python314-local-validation.md |
| Artifact type | framework_pr42_local_s3415_and_cpython3146_validation |
| SHA-256 | 4f3f7967438688697da9dcca5cb57bcaf7914c700342d9af8bb07f16a8d63075 |
| Command | Selected CPython 3.14.4 run of the three direct S3415 modules (49 tests), combined checks, and full native make lint for the configured CPython 3.14.6 migration |
| Working directory | framework-worktree-v4 |
| Exit code | 0 |
| Observed at | 2026-07-22T20:14:50Z |
| Retention status | task_owned_retained_evidence |

| Field | Sealed combined 22-path security scan |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/analysis/security-diff-pr42-python314-20260722T200333Z/report.md |
| Artifact type | sealed_codex_security_diff_scan_report |
| SHA-256 | 1b85288ff20d4c4f04443a9f2e4ba6ce07b69967e165dcc2d3c02257dfc6da36 |
| Command | Complete 22-path Codex Security diff scan of the combined local PR #42 remediation and CPython 3.14.6 migration |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-22T20:14:50Z |
| Retention status | sealed_task_evidence |

| Field | Current master S3415 inventory |
| --- | --- |
| Run ID | 20260723T092456Z-framework-sonarqube-test-issues-507-10387697 |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260723T092456Z-framework-sonarqube-test-issues-507-10387697/evidence/sonar-master-s3415-inventory.md |
| Artifact type | current_framework_master_s3415_paginated_inventory |
| SHA-256 | 0e9f549877fc1da2d3c629073e966e51f101348e913641cc7f539b29896379ef |
| Command | RTK-wrapped SonarQube Cloud `project_analyses`, paginated `issues/search`, `qualitygates/project_status`, and GitHub master-ref reads |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-23T09:24:56Z |
| Retention status | task_owned_retained_evidence |

## Root cause

The affected `unittest` assertions were authored with positional `expected,
actual` ordering. Sonar rule `S3415` requires `actual, expected` ordering so
a failed assertion shows the observed value in its intended position. This is
independent from the complex CI-security-contract, Python-version, and updater
refactors in `FND-FRAMEWORK-0044`. The 507 current-master keys are a new
observation of the same cause at a distinct current test set, not a duplicate
record: the canonical finding now retains both the historical 15-key PR #42
observation and the independently actionable 507-key master observation.

## Acceptance criteria and validation plan

1. All 507 current-master locations are mapped and use `actual, expected`
   ordering with no relation, message, fixture, control, or evaluation-order
   change.
2. Side-effecting argument expressions receive reviewed safe treatment rather
   than a blind swap.
3. Focused affected test-family modules pass, including their legitimate
   security-regression controls.
4. `git diff --check`, native Framework lint, and required documentation /
   Change Record checks pass for the task-owned Framework range.
5. The fresh SonarQube Cloud Draft-PR analysis at exact submitted head
   `4c55bb2855b8e0196fe54cb0c6f90f43aa993962` reports none of the original
   507 `S3415` keys, no open PR issue, and no prohibited scanner-control
   change.
6. Parent gitlink and MRTS source remain unchanged; this PR does not claim to
   resolve the independent `FND-SONAR-0002` Security-C gate condition.

Create an isolated worktree from freshly observed remote master; map every
current issue to its source assertion; review the task-owned diff for only
argument order changes and prohibited controls; then run affected modules by
test family, native source-quality and documentation checks. Observe fresh
exact-head GitHub/Sonar evidence after normal Draft-PR submission.

## Regression and legitimate-control tests

Regression tests:

- Changed `tests/security_regression/` modules
- Changed `tests/no_crs/` modules
- Changed `tests/protocol_client/` modules
- Changed `tests/makefile_contract/` modules
- Native `make lint`, Change Record, and documentation checks

Legitimate controls:

- Existing accepted and rejected path-containment, parser/provenance,
  workflow/action-pin, protocol, and Makefile fixtures retain the same
  expected result and diagnostic.

## Dependencies, blockers, related findings, and residual risk

- Dependencies: no delivery dependency remains for this finding: PR #43 is
  merged and its original S3415 scope is verified on resulting Framework
  master.
- Blocked by: no technical blocker for this finding. The independent
  `FND-SONAR-0002` master Quality Gate blocker remains outside this finding.
- Related findings: `FND-FRAMEWORK-0044`, `FND-FRAMEWORK-0046`,
  `FND-FRAMEWORK-0047`, `FND-FRAMEWORK-0048`, `FND-FRAMEWORK-0049`, and
  `FND-SONAR-0002`.
- Residual risk: a bulk positional swap can inadvertently change argument
  evaluation order or test diagnostics. Only reviewed assertion calls may
  change, every affected control family must be rerun, and no scanner/test
  control may be weakened. No risk is accepted.

## History

| At | Event | Detail |
| --- | --- | --- |
| 2026-07-22T18:18:47Z | framework_pr42_s3415_finding_created | Allocated after a complete public exact-head PR #42 issue query and deduplication. Fifteen `python:S3415` CODE_SMELL diagnostics in three test modules form an independently remediable test-maintainability boundary; no source, Git, GitHub, Parent, or MRTS action is claimed by this record. |
| 2026-07-22T20:14:50Z | framework_pr42_s3415_local_fix_and_validation_reconciled | All fifteen positional assertion orders were locally corrected. The direct three-module suite passed 49 tests, full native `make lint` passed, and the complete combined 22-path security scan reported zero findings. The finding is fixed, not verified or closed, until exact submitted-head hosted Sonar evidence is observed. |
| 2026-07-23T09:27:46Z | current_master_s3415_observation_deduplicated_into_canonical_finding | Complete current-master pagination identified 507 distinct current `python:S3415` keys in 29 Framework test files. This is the same assertion-order technical cause as the historical fifteen PR #42 keys, so it extends this canonical record rather than allocating a duplicate. The new current scope is independently actionable; `FND-SONAR-0002` remains the separate MRTS-only Security-C gate dependency. No Framework source, Git, GitHub, Parent, or MRTS action is claimed by this observation. |
| 2026-07-23T10:41:53Z | framework_pr43_exact_head_verified | Framework Draft PR #43 was created normally at exact head `4c55bb2855b8e0196fe54cb0c6f90f43aa993962` against master `935cf14c676a24672be5c336e92cd13457cc35c8`. Local/remote/PR heads matched; all terminal GitHub checks passed; the exact Sonar PR analysis is Quality Gate OK with zero open `python:S3415` and zero open issues. The finding is verified, not closed, and no merge or Parent/MRTS action occurred. |
| 2026-07-23T11:25:34Z | framework_pr43_merged_and_s3415_verified_on_resulting_master | PR #43 exact source `4c55bb2855b8e0196fe54cb0c6f90f43aa993962` merged normally as Framework master `f98a8739cb13b583f23d646784b144e596b61441`. Exact master analysis `77e255d6-17a2-4e8a-bb29-6438e91e6fa8` has zero open `python:S3415` issues. Its Quality Gate ERROR is solely Security C (actual `3`, threshold `1`) from nine read-only MRTS signals tracked by independent `FND-SONAR-0002`; no causal attribution to this finding is made. Parent and MRTS remained unchanged. |
