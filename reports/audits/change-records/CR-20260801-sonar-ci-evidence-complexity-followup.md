# Change Record: Parent CI evidence SonarQube Cloud complexity follow-up

**Language:** English | [Deutsch](CR-20260801-sonar-ci-evidence-complexity-followup.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-sonar-ci-evidence-complexity-followup` |
| Date (UTC) | 2026-08-01 |
| Base revision | `caabf33c11d6002f9a1661f215ed195d6e141253` |
| Tracking | `FND-SONAR-0031` — 15 current `python:S3776` receipts and one 23-line duplicate block in `ci/evidence`. |
| Boundary | Parent `ci/evidence/**`, `ci/lib/focused_analysis_utils.py`, direct Parent tests, and this English/German Change Record/index pair. Framework, MRTS, Gitlinks, workflows, scanner settings, Quality Gates, exclusions, suppressions, and `master` remain unchanged. |
| Delivery tracking | Task branch `agent/ci-evidence-sonar-remediation-followup-20260801`; a Draft PR is authorized but has not yet been created at record authoring. |

## Motivation and problem statement

The current Parent `ci/evidence` component contains fifteen OPEN CRITICAL
`python:S3776` cognitive-complexity receipts and 23 duplicated lines (0.1%).
The affected report generators classify runtime evidence, render operator
reports, and write below safe output roots. The remediation must reduce the
real source causes while preserving schemas, ordering, redaction, path
containment, and fail-closed evidence behavior.

## Implementation decision and rationale

The patch decomposes each selected function at an existing responsibility
boundary: data collection, pure classification, rendering, or lifecycle
ownership. The duplicate final-audit CLI lifecycle is replaced by the existing
safe report lifecycle with a fixed post-write callback. This keeps safe-root
registration and `write_text_file` in their existing order rather than adding
a second output path.

The runtime-mismatch helpers retain strict HAProxy XML decision predicates,
including exact boolean checks, one decision record, a non-disruptive pass,
and empty match fields. Refresh placeholders continue to use the established
safe writer. The NGINX classifier order is aligned with its existing unit
contract. No generated report, runtime-evidence artifact, scanner setting,
rule, gate, exclusion, suppression, `NOSONAR`, workflow, Framework/MRTS
source, or Gitlink is changed.

## Acceptance criteria

- All fifteen retained issue keys and the duplicate block have a concrete,
  behavior-preserving source disposition in the task-owned diff.
- Focused tests preserve report schemas, ordering, fallback, safe output,
  path normalization, and fail-closed runtime-evidence controls.
- The exact Draft PR head reports zero OPEN/CONFIRMED SonarQube Cloud new
  issues, zero New-Code duplication, and a passing Quality Gate without a
  scanner-control change.
- The user has not authorized a `master` integration; no merge is claimed by
  this record.

## Changed files

- Eleven Parent `ci/evidence/reports/*.py` generators, including refresh,
  runtime mismatch, final audit, Phase-4, NGINX, body-processor,
  intervention, response-header, rule-chain, remaining-failure, and roadmap
  reports.
- `ci/lib/focused_analysis_utils.py` for the narrowly scoped post-write seam.
- `tests/test_focused_analysis_utils.py`,
  `tests/test_report_conditional_remediation.py`, and
  `tests/test_remaining_failure_analysis.py` for direct regression and
  fail-closed controls.
- This English/German Change Record pair and the paired indexes.

## Commands executed

| Command or check | Result |
| --- | --- |
| `python3 -m py_compile` over all changed Python sources and direct tests | passed. |
| Focused Python aggregate over the changed report/evidence families | passed: 161 tests in the task worktree, including direct Phase-4 metadata/classification priority and legitimate-control coverage. |
| `python3 -m unittest -q tests.test_runtime_env_snapshot_contract` in the canonical Parent checkout | passed: 9 tests. |
| `git diff --check` | passed before traceability additions; it must be rerun before delivery. |
| Focused post-change Codex Security diff review | passed: no reportable diff-induced finding. |
| Broad `make lint` with a task-owned external build root | stopped at pre-existing Apache C17 warnings/errors outside this change; it does not validate or invalidate the selected report patch. |

## Security impact

This is maintainability work inside a security-relevant evidence boundary. The
review verifies that safe-root registration still precedes every output path,
the final-audit callback executes only after the secure report pair is written,
refresh placeholders still use the safe writer, and HAProxy XML evidence
remains fail-closed. No new shell execution, direct unsafe write, untrusted
path widening, or evidence-classification bypass was introduced.

## Runtime evidence

The focused tests exercise report-source contracts using task-owned temporary
fixtures. They include safe-output and path controls, fail-closed XML
decision-negative cases, ordering and fallback contracts, and final-audit
release gate results. They do not claim a full connector matrix or a live
runtime report regeneration.

## Known limitations

The temporary task worktree deliberately has no initialized Framework
submodule. The separately attempted whole snapshot-contract suite therefore
has one environment-only case,
`test_with_runner_consumes_the_prepared_snapshot_without_reading_shared_env`,
which exits `77` there because
`modules/ModSecurity-test-Framework/ci/lib/common.sh` is absent. The same
unchanged test suite passes in the canonical Parent checkout, distinguishing a
worktree prerequisite from a source-patch regression.

`make check-generated-report-layout` is not a passing control: both the task
worktree and canonical checkout report the same stale/missing historical
generated-report evidence. It was not repaired because no generated report or
evidence artifact is in scope.

## Checks not run and rationale

Full connector builds, runtime matrices, and Framework/MRTS checks are not run:
this is a Parent report-source refactor with no Framework/MRTS change. Hosted
Actions and exact-head SonarQube Cloud analysis cannot run until the authorized
Draft PR exists, and a master analysis cannot be requested without a later,
separate master-integration authorization.

## Remaining risks and verification state

The local source and focused tests support the intended behavior, but only an
exact-head GitHub Actions and SonarQube Cloud readback can prove the requested
New-Code result. This record does not claim a commit, push, PR number, review,
hosted check, SonarQube Cloud PR analysis, merge, resulting master SHA, or
master workflow result.

## Final diff and review status

Before delivery, the task-owned diff must receive a final `git diff --check`,
documentation-pair verification, staged-file secret scan, and exact remote
identity preflight. The final security review will be reconciled against that
diff. The task remains Parent-only; no Framework/MRTS/Gitlink change is
permitted.

## Delivery authorization

The current user authorized one Parent Draft PR for this remediation. That
authorization does not allow a direct `master` push, force-push, merge,
Framework/MRTS action, Gitlink change, branch deletion, release, or deployment.
Any later integration requires a current, explicit `master` authorization and
a new exact-head verification.
