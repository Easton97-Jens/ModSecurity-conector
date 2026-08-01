# FND-PARENT-0029 — SonarQube Cloud reports inconsistent Apache candidate return shapes

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | FND-PARENT-0029 |
| Title / Titel | SonarQube Cloud reports inconsistent Apache candidate return shapes |
| Category / Kategorie | sonarqube_finding |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priority / Priorität | P1 |
| Severity / Schweregrad | not_applicable |
| Confidence / Konfidenz | confirmed |
| Status | closed |
| Feasibility status / Machbarkeitsstatus | feasible_now |
| Release blocker / Release-Blocker | true |
| Security relevance / Security-Relevanz | false |

## Summary / Zusammenfassung

SonarQube Cloud PR analysis for draft PR #56 reports one open task-owned
`python:S8495` code smell at `apache_development_candidates()`. The Quality
Gate is OK, but its zero-, one-, and two-or-more-element tuple return paths
block `verified_pr` under the local Sonar delivery policy.

## Observed behavior / Beobachtetes Verhalten

At PR #56 head `63f4c9694f3f1c1372ce6db86ea1f88a38f01a92`,
`ci/tools/run-check-status.py:222-234` returns `(value,)`,
`tuple(shlex.split(...))`, `()`, or `("apxs", "apxs2")` depending on a
Parent-controlled environment selection. SonarQube Cloud issue
`AZ90uTmr7VSiD7VvMb8Y` is `OPEN` at line 222 with rule `python:S8495`,
severity `MAJOR`, and `HIGH` reliability and maintainability impacts.

## Expected behavior / Erwartetes Verhalten

The Parent-owned candidate selector preserves the documented `APXS_BIN` →
`APXS` → `CI_APXS_BIN_CANDIDATES` → default precedence while assigning one
candidate sequence and returning it through one canonical path. The current
exact PR head must have no unresolved task-owned Sonar issue.

## Impact / Auswirkung

The focused behavior controls currently pass, but the task-owned external
reliability/maintainability issue blocks the requested `verified_pr`
disposition. This is not a recurrence of the untrusted-child-output security
bypass tracked by `FND-PARENT-0025`.

## Affected files and symbols / Betroffene Dateien und Symbole

- `ci/tools/run-check-status.py` — `apache_development_candidates`,
  `apache_development_available`, and `main`.
- `tests/test_optional_prerequisite_status.py` — focused regression and
  legitimate-control coverage.
- Source commit: `63f4c9694f3f1c1372ce6db86ea1f88a38f01a92`.
- Flow: `Makefile:1134` → `run-check-status.py` →
  `apache_development_available()` → `apache_development_candidates()` →
  Parent optional-prerequisite status disposition.

## Evidence / Evidence

- Run ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/FND-PARENT-0029-sonar-return-shape/sonar-open-issue.json`
  - Type: `sonarqube_cloud_pr_issue_query`; SHA-256:
    `e0f0bbcb9f9895461c07a4453471ed016acc9208e8fc974e9c5209f0596d7a71`
  - Command:
    `rtk curl -fsS 'https://sonarcloud.io/api/issues/search?projectKeys=Easton97-Jens_ModSecurity-conector&pullRequest=56&resolved=false&ps=100'`
  - Exit code: `0`; observed `2026-07-18T12:40:03Z`; retention:
    `retained_task_evidence`.

## Root-cause analysis / Grundursachenanalyse

The status-channel remediation introduced several semantically valid but
structurally divergent tuple returns. SonarQube Cloud flags the varying tuple
arity conservatively as a reliability and maintainability pitfall. No child
output is used as control data and no security-bypass recurrence was observed.

## Proposed remediation / Vorgeschlagene Remediation

Use one explicitly typed local candidate sequence and one return, preserve
selection precedence and malformed-configuration behavior, and add an AST
single-return regression plus a real configured-APXS Parent preflight control.
Do not suppress Sonar, disable the rule, or alter the status-channel trust
boundary.

## Acceptance criteria / Akzeptanzkriterien

- `apache_development_candidates()` returns its sequence only once.
- All existing candidate precedence and malformed-configuration semantics
  remain intact.
- The focused suite covers the canonical return and a valid configured APXS
  control.
- The exact #56 PR head has no unresolved task-owned SonarCloud issue and no
  scanner suppression, rule disablement, or risk acceptance occurred.
- Child stdout and stderr still cannot authorize an allowed blocked result.

## Validation plan / Validierungsplan

1. Run `tests.test_optional_prerequisite_status`, including the AST and
   configured-APXS controls.
2. Review the diff for a behavioral change or status-channel trust regression.
3. Push only the isolated #56 follow-up; verify local/remote/PR-head equality,
   exact-head CI, Sonar issues, and the Quality Gate.

## Related findings / Verwandte Findings

- `FND-PARENT-0025` — different root cause: untrusted child output could
  authorize an allowed blocked status.

## Residual risk / Restrisiko

The status-channel remediation is locally fixed, but the draft PR cannot be
called `verified_pr` until the isolated return-shape follow-up receives a
clean exact-head SonarCloud and CI cycle. No risk is accepted.

## History / Historie

- `2026-07-18T12:40:03Z`: `sonarcloud_task_owned_issue_triaged` — direct
  SonarQube Cloud PR API evidence confirmed open issue `AZ90uTmr7VSiD7VvMb8Y`
  on the #56 source commit. No suppression or risk acceptance is authorized.

## Closed disposition — 2026-08-01

[PR #56](https://github.com/Easton97-Jens/ModSecurity-conector/pull/56) merged
normally into `master` as `a73c33529f4b900e0e5722f6c8eae2ae47e41c1f`; that
merge is reachable from current `origin/master`
`59aba762f2d852fd917079ca8519e4ea7f49169c`. The current source has one
canonical candidate return, the two specified optional-prerequisite regression
and legitimate-control tests pass, and current SonarCloud queries report both
the original key and unresolved `python:S8495` result set as empty. No
suppression, rule disablement, or risk acceptance was used.
