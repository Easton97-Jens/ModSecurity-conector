# Change Record: Parent CI runtime-readiness remediation-label deduplication for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260729-sonar-ci-runtime-readiness-fix-label.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-runtime-readiness-fix-label` |
| Date (UTC) | `2026-07-29` |
| Base revision | `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc` |
| Boundary | Parent `ci/checks/evidence/check-runtime-producer-readiness.py`, this English/German Change Record pair, and paired indexes only. No `.github/`, test source, Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, or default-branch change is included. |
| SonarQube Cloud linkage | Current `python:S1192` issue `AZ7POyUhBW70q7L2nMJN` for nine equal `"run make prepare-runtime-components"` component remediation labels. |

## Motivation and problem statement

The runtime-producer readiness report presents the same fixed remediation label
for nine required NGINX, Apache, and HAProxy component rows. SonarQube Cloud
reports that repeated source literal as `python:S1192`.

## Implementation decision and rationale

`RUNTIME_COMPONENT_PREPARATION_FIX` now owns the exact existing label and
supplies only those nine component `fix` fields. The distinct
`"make prepare-runtime-components"` value in the NGINX readiness summary is
not part of this change. Component names, ordering, paths, required flags,
path validation, runtime-environment handling, `BLOCKED` calculation, and
exit codes remain unchanged.

## Acceptance criteria

- Only the nine equal component remediation-label references change.
- A controlled complete readiness payload remains byte-for-byte equivalent to
  the current `master` implementation.
- The existing safe external-source control and `/etc`/foreign-root rejection
  tests retain their outcomes.
- A future exact PR head must receive zero new SonarQube Cloud issues and
  `0.0%` New-Code duplication without weakening rules or controls.

## Changed files

- `ci/checks/evidence/check-runtime-producer-readiness.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-runtime-readiness-fix-label.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-runtime-readiness-fix-label.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| Python `3.14.4` `-m py_compile` of the changed checker with a task-owned bytecode-cache root | passed. |
| `python -B -m unittest -v tests.test_runtime_producer_readiness_path_policy` with task-owned temporary storage | passed: 4 tests, including a safe canonical source-root control plus runtime-environment `/etc` and foreign-root rejection. |
| Controlled base-versus-head `build_payload()` parity harness | passed: complete payload equality and unchanged required-component remediation labels. |
| `make check-runtime-producer-readiness` with the same selected Python and task-owned temporary storage | blocked_external_dependency: the checker correctly returned `BLOCKED`/77 because NGINX, Apache, and HAProxy runtime artifacts are not prepared. No component preparation was started. |
| `git diff --check` | passed. |
| Focused full-file security/control review | passed: no plausible security candidate. The fixed label reaches report text only, never a command, path, authorization, status, or exit-code sink. |

## Security impact and residual risk

The checker receives CLI roots, environment values, cached runtime-environment
values, and Framework common-shell output. Its security-relevant invariant is
that missing components or unsafe runtime paths remain `BLOCKED` and cannot
authorize system-write paths. The shared value is source-authored, never
externalized, and is only rendered in report content; it cannot alter the
checker’s validation or control flow.

No security finding is claimed, suppressed, or closed. The residual risk is
limited to an implementation typo or accidental scope expansion, both covered
by the focused diff review and payload-parity check.

## Runtime evidence

No connector runtime, component provisioning, network access, package
installation, or host matrix is claimed. The direct native readiness command
was observed to block correctly when required runtime artifacts are absent;
the focused unit module exercises the relevant legitimate and negative path
controls without provisioning them.

## Known limitations

The focused unit module verifies path-policy behavior rather than a complete
prepared NGINX/Apache/HAProxy installation. Passing the native readiness
command requires separately prepared artifacts and is not a prerequisite for
this equal-string refactor.

## Remaining risks

The exact hosted PR head must still demonstrate that SonarQube Cloud removes
the selected S1192 issue while reporting zero new issues and `0.0%` New-Code
duplication. No local check can substitute for that exact-head result.

## Checks not run and rationale

- No `make prepare-runtime-components`, networked build, package download, or
  runtime matrix was run: those would provision unrelated runtime artifacts
  rather than validate this fixed report-text value.
- No Framework, MRTS, Gitlink, `.github/`, or unrelated Parent source was run
  or changed because the user restricted remediation to Parent `ci/` and
  `scripts/`.
- Hosted SonarQube Cloud, GitHub Actions, review, and merge evidence are not
  inferred locally and require the eventual exact PR head.

## Initial delivery status

The initial source-and-traceability commit
`491367f4708d9f2f67cfa8ec418032e1767a0f67` was pushed on
`agent/parent-ci-runtime-readiness-remediation-20260729`, and Draft PR
[#171](https://github.com/Easton97-Jens/ModSecurity-conector/pull/171) was
opened against `master`. At PR creation, local, remote, and PR head matched
that commit. This delivery-metadata follow-up changes documentation only, so a
fresh exact-head GitHub Actions and SonarQube Cloud cycle is still required.
No merge is authorized or claimed.
