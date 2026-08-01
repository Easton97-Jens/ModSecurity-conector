# FND-SONAR-0003 — Exact Framework PR head has a SonarQube Cloud Critical S5443 security signal in a CRS regression assertion

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-SONAR-0003` |
| Category | `sonarqube_finding` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity | `P1` / `not_applicable` |
| Confidence / status | `validated` / `fixed` |
| Feasibility | `feasible_now` |
| Release blocker | `true` |
| Security relevant | `true` |

## Summary and observed behavior

SonarQube Cloud initially marked Draft PR #27 head `15e9a034…` with Critical `python:S5443` and Security Impact High, causing New Code Security Rating D. Exact-head check run `88088009441` failed with one vulnerability annotation at `tests/ci_security/test_ci_security_contract.py:287`: `self.assertNotIn("/tmp/crs-version-pinning", script)`. Follow-up Framework commit `66d90872cfc0125536267d574b776d2e88d26b23` now passes exact-head SonarQube Cloud check `88089324795` with Security Rating A and zero open pull-request vulnerabilities.

Source-to-sink validation proves that the line is a negative `unittest` comparison over already-read checked-in script text: it neither creates/opens a file nor starts a process. The scanner signal is test-only, not a product vulnerability. The replacement checks the actual retired predictable `crs-version-pinning.$$` form and retains the positive safe-root and private-`mktemp` controls.

## Expected behavior, impact, and scope

The regression test must prove that the production script does not use the retired predictable path, while no test expression may be misclassified as an unsafe public-directory file operation. The exact remote PR-head SonarQube Quality Gate must pass without suppressing, excluding, disabling, or weakening any control.

The scanner classification temporarily failed a required external gate. It is now fixed on the exact PR head without a suppression, exclusion, disabled scanner, weakened test, or weakened Quality Gate. This is Framework-only scope; it neither authorizes a Parent product or gitlink change nor any MRTS action. `FND-SONAR-0002` remains a separate historical default-branch SonarQube backlog.

## Evidence, root cause, and remediation

Retained evidence comprises `sonar-pr27-final-head-failure.md`, SHA-256 `52187029ea9ce58070f5150655dc77766c301552c601c365b5234e4212379a95`, and final remote disposition `framework-pr27-final-remote-status.md`, SHA-256 `ccedabbe5e020bf43eb91ccf93b1e1484b8d11471e2817b6d078a95eeddb3552`. The first source-to-sink analysis confirms no writable-directory file-creation, file-open, or subprocess sink at the flagged line.

The implemented correction preserves the regression through the exact former predictable suffix, retains all safe private `mktemp` controls, and passes focused CI-security tests, `make lint`, CodeQL, actionlint, zizmor, OSV, Scorecard, Gitleaks, and exact-head SonarQube Cloud. The final Sonar result contains 17 non-security new issues but passes Quality Gate, Security, Reliability, and Maintainability ratings; no unnecessary semantic-checker refactor was bundled.

## Acceptance criteria and validation

- Source-to-sink validation establishes the signal as test-only.
- The test rejects exact retired pattern `crs-version-pinning.$$` and still requires safe runtime-path and private `mktemp` controls.
- Focused regression and legitimate-control tests pass without control weakening.
- Exact final Draft PR #27 head has a passing SonarQube Cloud Quality Gate, Security Rating A, and zero open pull-request vulnerabilities.

The record remains `fixed`, not closed, until a merged-current-master verification. Separate exact-head required-CI blockers `FND-FRAMEWORK-0001` and `FND-GITHUB-0002` prevent `verified_pr` but are not caused by this remediation.

## Residual risk and history

The task-owned scanner signal no longer reproduces on the exact PR head. The external PR remains `partial` because common-structure and Dependency Review fail independently; this record is not closed prior to merged-current-master verification. `2026-07-18T14:12:00Z`: signal triaged. `2026-07-18T14:26:12Z`: source-to-sink validation and exact-head remote gate fixed the test-only signal.
