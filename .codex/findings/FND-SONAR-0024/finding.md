# Finding FND-SONAR-0024: Native ModSecurity oracle main exceeds Sonar Cognitive Complexity threshold

**Language:** English | [Deutsch](finding.de.md)

## Classification

| Field | Value |
| --- | --- |
| Category | `maintainability` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P2` / `not_applicable` / `confirmed` |
| Status / feasibility | `verified` / `feasible_now` |
| Release blocker / security relevant | no / no |
| Sonar inventory | `c:S3776`, `AZ7b3dgOcO69wzd-_jHu` |

## Summary, behavior, and impact

The inventory-bound `c:S3776` code smell reported Cognitive Complexity `30`
where `25` is allowed in native Oracle `main`. It is maintainability-only and
does not itself establish a security vulnerability. The local task patch
extracts the linear request-phase sequence into `process_request` and
centralizes resource teardown in `cleanup_oracle`, while retaining CLI parsing,
result JSON, phase ordering, reason strings, and exit states.

Protected-squash PR #200 from exact head
`5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` produced Parent master
`13890da56ad19a105629243349f39ea8c084f396`. The native Oracle and focused
reliability-test blobs equal the reviewed candidate; compiler and real-
LibModSecurity controls preserve exercised behavior, all 14 master workflows
passed, and default-branch analysis
`c1f32224-aa05-4202-9b10-65c15165ff35` no longer reports
`AZ7b3dgOcO69wzd-_jHu`. The independent non-ignored global Quality Gate
`ERROR` is not an acceptance criterion for this non-security finding, so its
status is `verified`, not `closed`.

## Scope, reproduction, and evidence

- Affected files/symbols: `ci/tools/native_modsecurity_oracle.c`,
  `tests/test_sonar_reliability_contract.py`, `main`, `process_request`, and
  `cleanup_oracle`.
- Preconditions: the inventory revision with complexity `30` is analyzed and
  normal request inputs/rules/expected-status arguments are passed.
- Reproduce by reviewing `c:S3776` key `AZ7b3dgOcO69wzd-_jHu`, compiling C17
  GCC/Clang warning-as-error builds, and running allowed 200, header-blocked
  403, and setup-error controls against real LibModSecurity.

Run ID: `ci-tools-sonar-remediation-20260730`.

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| `.codex/plans/ci-tools-sonar-remediation.md` | `0029f0724d663e1d84408d56af69e71724a79f79dbb24c862aa0f628ffc0852c` | Records `AZ7b3dgOcO69wzd-_jHu`, complexity `30`, and required semantic preservation. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/security-diff-scan-20260730T100735Z/report.md` | `9d4b50736c29628147b053cd869e9253c1f95bf681e849174829929ec99b69d7` | Complete focused review finds no reportable diff-introduced security item and records preserved phases/results/cleanup. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/runtime/native-final-clang-block-result.json` | `ae386940e02a5c12915ce68992b0ef64d562fc6b5fad0cfc4a80ea14fdc8d72e` | Real 3.0.14 request-header control returns pass, expected/actual `403`, `native_match: true`, phase `request_headers`. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/runtime/native-final-gcc-missing-headers-result.json` | `4c4901048beaeb13e485761315a8d1f40ff3756d3616b29add1e257d80d994e0` | Expected setup-error contract returns exit `2` and reason `adding request headers failed`. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/evidence/pr200-exact-head-verification.md` | `42ba7a4ff8ff0172997a935f04a7fdf560b7b6ce9c70daab97fa24e69024f3be` | Exact Draft-PR #200 head is OPEN/Draft/CLEAN and MERGEABLE; required checks and SonarQube Cloud Quality Gate/readbacks pass with zero PR issues, including original `c:S3776` key `AZ7b3dgOcO69wzd-_jHu`. |
| `/var/tmp/codex/ModSecurity-conector/runs/ci-tools-sonar-remediation-20260730/evidence/pr200-66db7e3f-exact-head-verification.md` | `33cc911a5ee393fb44906c3e4dac76634df86d99fe07b3e105be9962148c840a` | Refreshed Draft-PR #200 head `66db7e3f2de324c960d8db36b4b6760d958cd7e1` against master `726322b17d6423c7f9e3bba0e6affc051dbf94cd` is OPEN/Draft/CLEAN and MERGEABLE; required checks and SonarQube Cloud Quality Gate/readbacks pass with zero PR issues, including original `c:S3776` key `AZ7b3dgOcO69wzd-_jHu`. |

## Root cause, remediation, and controls

`main` mixed argument decoding, rules setup, request-phase progression, result
generation, and cleanup in one control-flow unit. The task patch extracts only
the linear phase sequence and uses one-owner cleanup; `main` still owns CLI
parsing, setup, final result writing, and exit classification. No Sonar rule,
Quality Gate, exclusion, `NOSONAR`, or suppression changes.

Acceptance is demonstrated on exact resulting master: the original issue and
no task-owned replacement are absent from default-branch analysis; request/
JSON/reason/exit/cleanup semantics, C17 GCC/Clang controls, real
200/403/setup-error controls, and hosted checks were preserved without bypass.
Regression:
`tests/test_sonar_reliability_contract.py`; legitimate controls are the three
real library paths.

## Dependencies, blockers, related findings, and residual risk

Exact Draft-PR and resulting-master hosted analyses are retained. Integration
and resulting-master revalidation are complete; there is no technical blocker
for this verified finding. `FND-SONAR-0016` is aggregate Sonar context,
`FND-SONAR-0023` is the independent result-writer cause, and
`FND-PARENT-0036` remains the separate historical lifetime finding. The
one-owner cleanup improvement does not prove that natural append failure is
reproducible. No risk acceptance was made; the protected master integration is
recorded as evidence.

## History

- `2026-07-30T10:46:48Z`: allocated as the distinct `c:S3776` source boundary;
  local compiler, source-contract, and real-libmodsecurity controls pass,
  hosted exact-head Sonar verification was pending at that time.
- `2026-07-30T11:07:21Z`: exact Draft-PR #200 head `2bc97ac058725fdba6a36ad93307487c160b1f05` passed
  required GitHub checks and SonarQube Cloud Quality Gate/readbacks. Original
  `c:S3776` key `AZ7b3dgOcO69wzd-_jHu` is absent from the PR issue query; status
  remains `fixed` pending authorized integration and resulting-master
  verification.
- `2026-07-30T11:33:48Z`: after master advanced to `726322b17d6423c7f9e3bba0e6affc051dbf94cd`, refreshed exact Draft-PR #200 head `66db7e3f2de324c960d8db36b4b6760d958cd7e1` passed required GitHub checks and SonarQube Cloud Quality Gate/readbacks. Original `c:S3776` key `AZ7b3dgOcO69wzd-_jHu` is absent from the zero-issue PR query; status remains `fixed` pending authorized integration and resulting-master verification.

## Resulting-master disposition

Protected-squash PR #200 exact head `5b7487824ae5ca4a14a48b0d743cf4a1cc817da0` produced Parent master
`13890da56ad19a105629243349f39ea8c084f396` at `2026-07-30T12:11:32Z`. The native Oracle and focused
reliability-test blobs equal the reviewed candidate; the retained phase, JSON,
exit-state, compiler, and real-LibModSecurity controls therefore apply to this
exact source. All 14 master workflows passed, and default-branch analysis
`c1f32224-aa05-4202-9b10-65c15165ff35` no longer reports `AZ7b3dgOcO69wzd-_jHu`.

The project-wide Quality Gate remains non-ignored `ERROR` for retained
unrelated conditions, but that is not an acceptance criterion for this
non-security maintainability finding. The original key is absent on resulting
master with preserved controls, so the status advances to `verified`, not
`closed`. The related FND-PARENT-0036 lifetime finding remains `fixed`.
Receipt SHA-256: `69cdb1bbdc92c4faa82e2e722dd27d5eac32b3d33df50cc64fc7ed110d9da48a`.
