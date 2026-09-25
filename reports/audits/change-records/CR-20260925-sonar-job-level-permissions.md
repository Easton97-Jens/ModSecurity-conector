# Change Record: SonarQube Cloud GitHub Actions job-level permissions remediation

**Language:** English | [Deutsch](CR-20260925-sonar-job-level-permissions.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260925-sonar-job-level-permissions |
| Date (UTC) | 2026-09-25 |
| Base revision | `34aa7da8eea8c7a820c3951ee6c9846567e95b8a` |
| Finding | `FND-SONAR-0090`; GitHub Actions job-level token-permission vulnerability pattern (`githubactions:S8264`) |
| User authorization | Inspect the supplied open SonarCloud findings and fix them in a GitHub Draft PR. |
| Delivery status | Scoped Parent repair on `fix/sonar-job-level-permissions`; Draft PR delivery is authorized, but merge, auto-merge, direct `master` writes, Framework/MRTS changes, rule suppression, issue acceptance, and Quality-Gate changes are not. |

## Motivation and problem statement

The exact `master` SonarQube Cloud check for
`34aa7da8eea8c7a820c3951ee6c9846567e95b8a` fails the Quality Gate because
the Security Rating on New Code is `C`, while the required rating is `A`.
The preceding `master` revision `5170d24801243cdcd7bf1bca6123bf8cb2c72386`
passed, and the first observed failing `master` analysis is
`7dd47a0ba9a94c8aec110630d417dd5e7bd6d271`.

The supplied SonarCloud issue page is not directly readable through the
available environment, so no unobserved Sonar issue key is claimed. Current
Sonar GitHub Actions rules classify read permissions inherited from workflow
scope instead of declared at job scope as the `githubactions:S8264`
vulnerability pattern. Repository inspection found that all versioned GitHub
Actions workflows set `contents: read` at workflow scope and that multiple
jobs rely on that inherited permission.

## Acceptance criteria

- Every versioned GitHub Actions workflow has a default-deny top-level
  `permissions: {}` declaration.
- Every job explicitly declares its own permission boundary.
- Jobs that previously inherited `contents: read` receive exactly
  `contents: read` at job scope.
- Existing job-specific write permissions remain byte-for-byte equivalent in
  capability and are not broadened.
- A focused CI-security regression rejects future workflows that reintroduce
  inherited top-level read access or omit an explicit job permission boundary.
- No Sonar rule, exclusion, suppression, accepted issue, Quality Gate, branch
  protection, authentication, or validation control is weakened.

## Implementation decision and rationale

The repair changes authorization scope, not effective job capability. The
former workflow-level `contents: read` default is replaced by
`permissions: {}`. Jobs that had no direct permission mapping receive a
job-local `contents: read` mapping; jobs with existing explicit mappings keep
those mappings unchanged.

The CI-security contract now understands inline empty permission mappings and
requires default-deny workflow scope plus an explicit permission declaration
for every job. Existing exact write-permission allowlisting remains in place.

## Security impact

This is a least-privilege CI hardening change. It prevents a newly added job
from silently inheriting repository read permission and makes every existing
job's token boundary reviewable where the job is defined. No job gains a
capability it did not effectively have before this change. Existing narrowly
allowlisted write jobs remain unchanged.

## Changed files

- All versioned files under `.github/workflows/*.yml`
- `tests/test_ci_security_workflows.py`
- `reports/audits/change-records/CR-20260925-sonar-job-level-permissions.md`
- `reports/audits/change-records/CR-20260925-sonar-job-level-permissions.de.md`

Framework source, the Parent Framework Gitlink, and nested MRTS are unchanged.

## Commands executed

| Check | Result | Observed result |
| --- | --- | --- |
| Pre-fix exact-`master` SonarQube Cloud readback through the GitHub check | failed as expected | Security Rating on New Code `C`; required `A`. |
| Historical exact-`master` comparison | passed / failed boundary identified | `5170d248...` passed; `7dd47a0...` and `34aa7da...` fail on the same Security Rating condition. |
| Repository-wide workflow permission inventory | passed | Workflow-level `contents: read` inheritance and the jobs relying on it were identified; existing write grants are job-scoped. |
| Source transformation invariants | passed | Top-level scope becomes default-deny; formerly inherited read jobs receive explicit job-local read scope; existing direct permission blocks are preserved. |
| Initial Draft-PR head `64b38a34...` hosted checks | mixed during repair | Permission regression test, `zizmor`, report governance, protocol contract, CodeQL actions, and PR-diff checks exercised the new workflow scope; two task-owned contract/documentation mismatches were identified for this follow-up. The CRS/no-MRTS runtime matrix separately fails its pre-existing MRTS revision assertion (`615b13ba...` expected, `8a6bb546...` checked out) before runtime execution. |

## Runtime evidence

No connector runtime behavior changes. Runtime evidence is not applicable to
this GitHub Actions token-scope repair.

## Checks not run and rationale

Local repository commands were not executed because the current execution
surface provides GitHub repository operations rather than the repository's
required RTK/local command environment. Hosted checks on Draft PR #386 did run
against `64b38a34...`; they exposed the two task-owned contract/documentation
mismatches corrected by this follow-up and the separate pre-existing MRTS pin
mismatch described above. The exact successor head must be read back again.

## Known limitations

The SonarCloud issue-list payload itself was not available through the current
environment, so this record does not fabricate an issue key. The remediation
is bound to the observed failing Security Rating, the current Sonar rule
semantics, and the repository-wide matching workflow pattern.

## Remaining risks

`FND-SONAR-0090` is `fixed` by source change but not `verified` until the
exact Draft-PR head has a terminal SonarQube Cloud analysis and the expected
hosted CI-security checks complete successfully. A separate remaining Sonar
finding, if any, must be handled from fresh exact-head evidence rather than by
weakening the scanner or Quality Gate.

## Final diff and review status

The scoped diff changes only GitHub Actions token-permission placement, its
static regression contract, and this bilingual Change Record. The first
published head `64b38a34...` provided real hosted feedback; this follow-up
aligns the negative permission mutation and the mandatory Change-Record schema
without changing workflow capabilities. No merge is authorized or performed.
