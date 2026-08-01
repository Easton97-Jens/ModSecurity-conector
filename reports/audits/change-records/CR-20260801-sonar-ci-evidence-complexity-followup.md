# Change Record: Parent CI evidence SonarQube Cloud complexity follow-up

**Language:** English | [Deutsch](CR-20260801-sonar-ci-evidence-complexity-followup.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-sonar-ci-evidence-complexity-followup` |
| Date (UTC) | 2026-08-01 |
| Base revision | `caabf33c11d6002f9a1661f215ed195d6e141253` |
| Tracking | `FND-SONAR-0031` — 15 current `python:S3776` receipts and one 23-line duplicate block in `ci/evidence`. |
| Boundary | Parent `ci/evidence/**`, `ci/lib/focused_analysis_utils.py`, direct Parent tests, and this English/German Change Record/index pair. Framework, MRTS, Gitlinks, workflows, scanner settings, Quality Gates, exclusions, and suppressions remain unchanged. `master` is not changed directly; its only authorized change is the protected PR integration described below. |
| Delivery tracking | Task branch `agent/ci-evidence-sonar-remediation-followup-20260801`; PR [#225](https://github.com/Easton97-Jens/ModSecurity-conector/pull/225) is open. The current user explicitly authorized this one Parent PR's integration into `master`; no merge has occurred at this record update. |

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
- The exact current PR head reports zero OPEN/CONFIRMED SonarQube Cloud new
  issues, zero New-Code duplication, and a passing Quality Gate without a
  scanner-control change.
- The current user authorized “bringe das pr 225 in den master”. Integration
  may occur only through the repository-approved protected, exact-head PR
  mechanism after fresh checks, reviews, conversations, SonarQube Cloud, and
  resulting-`master` verification; no merge is claimed by this record.

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
| `git merge --no-edit origin/master` | completed as normal task-branch synchronization twice: `62f7e13f35edd3f73661f724fd5208dcf1584d18` is incorporated by `ade8b066e9ffb0e17d9971cb6a9ab9ab4bf2e1c0`, then current `7016a66f3702523098811b45139133c77dee88fb` by `290843bda5b922dad59a9a9f80688ebf422b960c`; neither operation changed `master` directly. |

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
this is a Parent report-source refactor with no Framework/MRTS change. The
latest branch synchronization and this truthful delivery-record update require
a fresh exact-head GitHub Actions and SonarQube Cloud cycle. Resulting-`master`
workflows and SonarQube Cloud analysis are pending the separately protected
integration operation; they are not inferred from PR checks.

## Remaining risks and verification state

The local source and focused tests support the intended behavior, but the
branch synchronization invalidates earlier PR-check evidence for merge
eligibility. At this record update the task branch contains synchronization
commit `290843bda5b922dad59a9a9f80688ebf422b960c`; the documentation update
itself creates a later PR head that requires another complete exact-head
GitHub Actions and SonarQube Cloud readback. This record does not claim an
actual merge, resulting master SHA, or master-workflow result.

## Final diff and review status

After the first normal master synchronization, the 161-test focused aggregate
and the 9-test canonical snapshot contract were rerun successfully. The later
normal synchronization to `7016a66f3702523098811b45139133c77dee88fb` and this
delivery-record correction require the focused tests, final `git diff --check`,
documentation-pair verification, staged-file secret scan, exact remote identity
preflight, and security-diff review to be freshly reconciled before protected
integration. The task remains Parent-only; no Framework/MRTS/Gitlink change is
permitted.

## Delivery authorization

The current user explicitly authorized “bringe das pr 225 in den master” for
this one Parent PR. The authorization permits only the normal protected PR
integration after a new exact-head verification; it does not permit a direct
`master` push, force-push, administrative bypass, Framework/MRTS action,
Gitlink change, branch deletion, release, or deployment. The merge remains
unclaimed until GitHub records it and the resulting `master` checks pass.
