# FND-SONAR-0011 — Parent PR #90 exact head has 23 non-gating Major SonarQube Cloud test code smells

## Classification

- **Category:** `sonarqube_finding` (`maintainability_code_smells`)
- **Repository / ownership:** `parent` / `parent`
- **Priority / severity / confidence:** `P3` / `major` / `confirmed`
- **Status / feasibility:** `closed` (archived) / `feasible_now`
- **Release blocker / security relevant:** no / no

## Observation

At exact PR #90 head `06a4e71408a60e5a72a55065a653b9c4e79a1ecf`,
SonarQube Cloud returns 23 open Major `CODE_SMELL` issues, all in Parent test
files. Twenty-two are `python:S3415` assertion-argument-order observations and
one is `python:S5778` for an exception assertion with multiple potentially
throwing calls. They affect `tests/test_go_version_contract.py` (10),
`tests/test_prepare_runtime_components.py` (2), and
`tests/test_update_go_version.py` (11).

This is non-gating: the same exact head has Quality Gate `OK`, New
Maintainability `A`, and 0.0% duplicated new code. It is distinct from the
former Quality Gate blocker in `FND-SONAR-0010`.

## Evidence and disposition

The retained issue summary is
sonar-pr90-06a4e71-open-code-smells.json (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/sonar-pr90-06a4e71-open-code-smells.json`)
(SHA-256 `3dcf58c2a8380955d2db678ddcafd0d2804e57bb87a7145f440fbe064ca17b2d`).
The matching hosted Quality Gate receipt is
hosted-pr90-06a4e71-validation.json (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/hosted-pr90-06a4e71-validation.json`)
(SHA-256 `db38c89e5c1646e343ec022466d7fec899998dda05558ccf85789196d273ea20`).

The current local remediation and its complete security-diff scan are retained
in pr90-sonar-remediation-security-diff-scan-receipt.json (`/var/tmp/codex/ModSecurity-conector/runs/20260723T040316Z-pr90-sonar-master-ba49d4a2/evidence/pr90-sonar-remediation-security-diff-scan-receipt.json`)
(SHA-256 `55999ab8235aea150b5c703250d8fe8bae96328f9528e97a14a120ffb229bea0`).
It covers the exact three-file local patch and reports complete coverage with
zero reportable security findings.

The user explicitly authorized remediation and protected Parent-master
integration. The completed patch made only the 22 required `assertEqual`
operand-order normalizations and isolated the unchanged prerelease fixture from
the expected `MetadataError` invocation. No Sonar rule, Quality Gate,
exclusion, suppression, false-positive marking, or risk acceptance changed.

Exact PR head `0a1f6031418917e20e2e87aaf935b84b89ca3af1` has a live Sonar
issue result of zero open or confirmed leak-period issues and Quality Gate
`OK`, then was protected-squash-merged as Parent master
`ad953cdcbc8c05ede519661ca56c03cf7b1ac7f3`. The retained combined receipt is
pr90-protected-merge-and-master-validation-20260723T045207Z.json (`/var/tmp/codex/ModSecurity-conector/runs/20260723T040316Z-pr90-sonar-master-ba49d4a2/evidence/pr90-protected-merge-and-master-validation-20260723T045207Z.json`)
(SHA-256 `4826baec6075341a6a0c96f36dce51f89bd27381c394bbb63e445938b4da97e4`).
The resulting-master GitHub Actions workflows passed. Its current Sonar master
Quality Gate failure is the independent, pre-existing release blocker
`FND-SONAR-0001`, not a regression from this finding.

## Safe remediation and validation

The completed test-only change preserves every expected/actual pass/fail
predicate and all existing controls. The three affected modules passed 24
focused tests; the focused 100-test PR suite, contracts, selected compilation,
bilingual check, and complete security-diff scan also passed. The fresh hosted
Sonar issue/Quality Gate evidence and protected merge satisfy the finding's
acceptance criteria without a runtime-code or SonarQube Cloud control change.

## History

- `2026-07-22T23:02:27Z`: allocated as a confirmed, non-blocking aggregate
  finding from the exact-head Sonar issue query; no remediation or suppression
  was applied.
- `2026-07-23T04:26:13Z`: user-authorized semantic-preserving remediation is
  locally complete and security-diff scanned; hosted exact-head verification is
  still pending.
- `2026-07-23T04:52:07Z`: exact head `0a1f603` passed required checks and
  SonarQube Cloud with zero open/confirmed leak-period issues, then
  protected-squash-merged as master `ad953cd`; applicable resulting-master
  GitHub Actions passed. The separate current master Quality Gate failure is
  retained under `FND-SONAR-0001`.

- `2026-07-26T14:09:02Z`: Current user authorized closure and archival after the affected current-master regression suites passed in the 144-test control suite; the changed test paths remain unchanged from verified master `ad953cd` through `6ca7e1536ce7e93da68099db9c586b88852ff13e`.
