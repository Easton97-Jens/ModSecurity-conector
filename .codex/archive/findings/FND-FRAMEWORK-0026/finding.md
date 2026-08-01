# FND-FRAMEWORK-0026 — Framework PR #30 C/C++ CodeQL initialization was blocked by an external GitHub service outage

## Identity

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0026 |
| Category | external_dependency |
| Repository / ownership | framework / external_tool |
| Priority / severity | P1 / not_applicable |
| Confidence / status | confirmed / verified |
| Feasibility | already_fixed |
| Release blocker | false |
| Security relevant | true |

## Summary, observation, expected behavior, and impact

The historical exact PR #30 head
`2706506be9e5f4b5bae57ec6d9419a715a8f3544` had a C/C++ CodeQL initialization
failure before source analysis began. CodeQL C/C++ jobs `88253045864` and
`88253302100` failed in `Initialize CodeQL for actual Framework languages`.
GitHub's public annotation reported HTTP 503 while determining feature
enablement: no server was available to service the request.

This was an external hosted dependency failure, not a Framework source or
workflow defect. The changed PR files did not include C/C++ source or the
CodeQL workflow, and no CodeQL source finding was produced. Patching product
code or weakening CodeQL in response would have been inappropriate.

The refreshed exact head `a448d056ef98e745d8551c198b2e56d33fe38194` completed
CodeQL pull-request run `29722369621` successfully for Actions job
`88287878237`, Python job `88287878246`, and C/C++ job `88287878247`. All
terminal non-skipped checks passed. The original external failure no longer
reproduces, so this finding is `verified`; it does not authorize a master merge.

## Scope, preconditions, reproduction, and evidence

The incident requires Framework PR #30 to be analyzed by the CodeQL
pull-request workflow at historical head
`2706506be9e5f4b5bae57ec6d9419a715a8f3544`, while GitHub's CodeQL
feature-enablement service is temporarily unavailable.

1. Read the retained job annotation for jobs `88253045864` and `88253302100`
   in workflow run `29710235017`.
2. Read the exact refreshed-head CodeQL check runs for
   `a448d056ef98e745d8551c198b2e56d33fe38194`, including C/C++ job
   `88287878247`.
3. Compare GitHub's terminal check state with that same PR head SHA.

Retained evidence:

- Run: `20260719T230508Z-framework-pr30-duplication-master-37469460`
- Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/evidence/pr30-codeql-cpp-hosted-503.md`
- SHA-256: `d41e0212f555f36f073bca5d2d25639acdc55ecbcfe309815609051a8ab1750a`
- Command: GitHub Actions job annotation and failed-log readback for CodeQL
  pull-request run `29710235017`; sanitized retained summary
- Working directory: `/root/git/ModSecurity-conector`
- Exit code: `0`
- Observed: `2026-07-20T01:08:00Z`
- Retention: `retained`
- Result: CodeQL C/C++ failed before analysis while feature enablement returned
  HTTP 503; no source finding or debug artifact was produced.

- Run: `20260720T061746Z-framework-pr-30-refresh-remediation-f8407eef`
- Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260720T061746Z-framework-pr-30-refresh-remediation-f8407eef/evidence/pr30-refresh-summary.md`
- SHA-256: `04a0b6891f92b0485c298bb939e57fb464cea2bd5872eb74c65d97f6450f4255`
- Command: GitHub exact-head check-run/review readback for Framework PR #30;
  retained sanitized summary
- Working directory: `/root/git/ModSecurity-conector`
- Exit code: `0`
- Observed: `2026-07-20T06:43:42Z`
- Retention: `retained`
- Result: CodeQL Actions, Python, and C/C++ jobs `88287878237`, `88287878246`,
  and `88287878247` succeeded on exact head
  `a448d056ef98e745d8551c198b2e56d33fe38194`.

## Root cause and proposed remediation

GitHub's hosted CodeQL feature-enablement endpoint returned HTTP 503 during
initialization. The failure occurred before source analysis, so there was no
evidence of a task-owned Framework defect.

Do not patch Framework code or relax a CodeQL control. Refresh or rerun the
exact PR head after hosted-service recovery, then require terminal-success
C/C++ CodeQL together with the other exact-head delivery evidence.

## Acceptance criteria and validation plan

- [complete] The exact refreshed PR head has terminal-success `CodeQL PR (c-cpp)`.
- [complete] CodeQL Actions and Python for the same exact head are terminal-success.
- [complete] No CodeQL workflow, scanner setting, waiver, quality gate, or
  product source changed to bypass the historical HTTP 503.
- [complete] The historical failure and its external root cause remain retained
  and distinct from Framework source findings.

Read back the PR head, CodeQL run, individual jobs, and terminal statuses for
the same SHA. Confirm that the current PR diff contains no CodeQL workflow or
C/C++ workaround, and retain the secret-free historical-failure/current-success
evidence pair.

## Regression and legitimate-control tests

Regression tests:

- GitHub `CodeQL PR (c-cpp)` exact-head check run.
- GitHub `CodeQL PR (actions)` exact-head check run.
- GitHub `CodeQL PR (python)` exact-head check run.

Legitimate controls:

- The exact refreshed head completes CodeQL C/C++ successfully after service recovery.
- The same exact head retains successful CodeQL Actions and Python checks.
- No scanner disablement, waiver, workflow bypass, or source workaround is present.

## Dependencies, boundaries, related findings, and residual risk

Dependencies are GitHub-hosted CodeQL availability and the Framework PR #30
exact-head Actions execution. There are no blockers or duplicate records.

This is not a duplicate of FND-FRAMEWORK-0023 or FND-FRAMEWORK-0024. Those
findings own PR #30 Sonar duplication and Change Record contract defects. This
finding owns the distinct external GitHub CodeQL initialization outage, proven
by the pre-analysis HTTP 503 and later exact-head recovery.

GitHub-hosted CodeQL availability can fail again independently of Framework
source. The historical incident is verified as recovered on exact PR head
`a448d056ef98e745d8551c198b2e56d33fe38194`; a later delivery must collect
fresh exact-head evidence if that SHA changes. No Framework-master integration,
Parent gitlink update, or MRTS action is authorized by this task.

## History

- 2026-07-20T01:08:00Z — hosted_codeql_initialization_outage_confirmed:
  historical CodeQL C/C++ jobs `88253045864` and `88253302100` failed before
  analysis at exact head `2706506be9e5f4b5bae57ec6d9419a715a8f3544`; GitHub
  reported HTTP 503 while determining feature enablement.
- 2026-07-20T06:43:42Z — exact_refreshed_head_codeql_recovery_verified:
  exact refreshed head `a448d056ef98e745d8551c198b2e56d33fe38194` completed
  CodeQL pull-request run `29722369621` for Actions job `88287878237`, Python
  job `88287878246`, and C/C++ job `88287878247`, without a bypass or source
  workaround.
