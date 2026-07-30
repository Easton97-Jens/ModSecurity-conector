# Change Record: Parent CI No-CRS missing-case diagnostic literal deduplication for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260730-sonar-ci-no-crs-diagnostic-literal.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260730-sonar-ci-no-crs-diagnostic-literal |
| Date (UTC) | 2026-07-30 |
| Base revision | fe4840a0a72449bbdb8f7b2f77f09922c9e66a9f |
| Tracking | Parent SonarQube Cloud issue `AZ9cRycZHhV2CayPTPw4`, `shelldre:S1192`, OPEN, MINOR: define one owner for `FAIL: capability-selected No-CRS runner cases are missing`, previously repeated five times in `ci/runtime/lifecycle/run-connector-stage.sh`. The current master analysis dated `2026-07-30T02:04:34+0000` is bound to this base revision. |
| Boundary | Parent `ci/runtime/lifecycle/run-connector-stage.sh`, its direct Parent test, this English/German Change Record pair, and their additive index entries. `.github`, `scripts`, Framework, MRTS, Gitlinks, connector source, SonarQube Cloud configuration, suppressions, Quality Gates, external issue state, push, pull request, and merge are unchanged at record authoring. |

## Motivation and problem statement

The five generic No-CRS branches emit an identical missing-selected-cases
diagnostic. The SonarQube Cloud finding is a genuine maintainability duplicate,
but those diagnostics sit beside evidence-integrity controls: a generic No-CRS
run must stop before dispatch if its canonical selected-case list is absent.
The refactor therefore cannot centralize, move, or weaken the guard itself.

## Acceptance criteria

- Replace the five duplicate diagnostic literals with one static shell owner.
- Preserve every existing `[ -n "${NO_CRS_SELECTED_CASES:-}" ]` guard, stderr
  redirection, exit status `1`, and generic dispatch target.
- Preserve the full-lifecycle path, which must select its native target without
  requiring the generic selected-case list.
- Add hermetic regression coverage for all generic connector routes with no
  selected cases, plus one generic and one full-lifecycle legitimate control.
- Pass applicable shell syntax, direct Parent tests, whitespace review, and
  direct bilingual-documentation validation without changing scanner policy;
  record repository documentation checks blocked only by the uninitialized
  Framework Gitlink.
- Do not claim the SonarQube Cloud issue resolved until an exact delivered PR
  head receives a fresh analysis.

## Implementation decision and rationale

`NO_CRS_SELECTED_CASES_MISSING_MESSAGE` is assigned once as a readonly static
shell value. Each existing failing branch still performs its own non-empty test
and then writes the same value to stderr before `exit 1`. The refactor does
not extract a helper or move a guard across the generic/full-lifecycle split.

The direct test builds only a temporary framework-presence marker and a
temporary target-recorder script. It invokes the real dispatcher without
initializing Framework or a connector runtime. The test proves six missing-case
routes return `1` with the exact stderr diagnostic, a generic Envoy route
reaches `no-crs-baseline-envoy` for a selected case, and the full-lifecycle
Envoy route reaches `runtime-smoke-envoy-ext-proc` without a selected case.

## Changed files

- ci/runtime/lifecycle/run-connector-stage.sh
- tests/test_no_crs_selected_runner_wiring.py
- reports/audits/change-records/CR-20260730-sonar-ci-no-crs-diagnostic-literal.md
- reports/audits/change-records/CR-20260730-sonar-ci-no-crs-diagnostic-literal.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Commands executed

- `sh -n ci/runtime/lifecycle/run-connector-stage.sh`
- `shellcheck --severity=error ci/runtime/lifecycle/run-connector-stage.sh`
- `/root/git/ModSecurity-conector/.venv/bin/python -m pip check`
- `/root/git/ModSecurity-conector/.venv/bin/python -m py_compile tests/test_no_crs_selected_runner_wiring.py`
- `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_no_crs_selected_runner_wiring.NoCrsSelectedRunnerWiringTest.test_stage_rejects_missing_selected_cases_and_preserves_dispatch_controls`
- `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_no_crs_selected_runner_wiring.NoCrsSelectedRunnerWiringTest.test_remaining_connectors_keep_compatibility_and_native_targets_distinct`
- `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_no_crs_selected_runner_wiring`
- `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_bilingual_docs`
- `make check-bilingual-docs`
- `make check-doc-links`
- `git diff --check`

## Tests and actual results

| Command or check | Result |
| --- | --- |
| POSIX shell parsing | passed: `sh -n` exited 0 for the changed dispatcher. |
| ShellCheck error level | passed: `shellcheck --severity=error` found no error-level issue. The unrestricted command still reports pre-existing non-error SC1007/SC2016 notices at unchanged lines 7, 162, and 185. |
| Python environment integrity | passed: `pip check` reported no broken requirements, and the changed test compiled. |
| New hermetic dispatch regression | passed: one test covers six generic missing-case routes, one generic selected-case control, and one full-lifecycle native-target control through the real dispatcher. |
| Existing target-separation control | passed: the direct wiring test preserves the native/compatibility target distinction and the diagnostic literal. |
| Complete direct test module | blocked external dependency: it ran seven tests and returned 1 only because two Apache fixture subtests require the uninitialized read-only Framework Gitlink (`git submodule status` begins with `-`). The new regression and target-separation control passed separately; C12 did not initialize or modify Framework to bypass the condition. |
| Direct bilingual-documentation test | passed: `tests.test_bilingual_docs` ran 21 tests successfully. |
| Repository documentation checks | blocked external dependency: `make check-bilingual-docs` and `make check-doc-links` stopped only on unchanged missing targets below the intentionally uninitialized Framework Gitlink (20 and 16 diagnostics respectively); neither output names a C12 Change Record, test, or source path. |
| Whitespace | passed: final `git diff --check` reported no error after all C12 documentation updates. |

## Security impact

This is security-relevant CI evidence-integrity maintenance, not a security
finding fix. Controlled connector/stage arguments and No-CRS environment values
retain their existing allowlists and fail-closed generic guard. The closest
sinks remain the quoted generic framework smoke handoff and the
remaining-connector target invocation. A broken refactor could allow an empty
selection to reach an unintended smoke path or could block a valid native
full-lifecycle path; the added hermetic negative and legitimate controls cover
both risks. No command construction, path control, credential handling, or CI
permission changes.

## Documentation status

This complete English/German Change Record pair is the only reader-facing
documentation change. No generated document or report changed. The direct
`tests.test_bilingual_docs` check passed 21 tests. The repository Make targets
are blocked only by unchanged missing targets below the intentionally
uninitialized Framework Gitlink: `make check-bilingual-docs` reported 20 and
`make check-doc-links` reported 16 diagnostics, none for a C12 path.

## Runtime evidence

No connector build, Framework initialization, full lifecycle matrix, or
report-producing runtime execution occurred. The hermetic test exercises only
the dispatch contract and is not evidence of a real connector lifecycle.

## Checks not run and rationale

- `shfmt -d` was not run because `shfmt` is unavailable; no automatic
  formatting was attempted.
- A full connector/runtime matrix was not run because it requires external
  component sources and produces runtime artifacts unrelated to this one
  diagnostic-owner refactor.
- At record authoring, hosted GitHub Actions, SonarQube Cloud PR analysis,
  review, commit, push, pull request, and merge did not yet exist for this
  uncommitted candidate.

## Known limitations

The full direct test module is blocked by the intentionally uninitialized
Framework Gitlink's Apache fixtures. The task preserves this boundary and uses
the independent hermetic test instead of fabricating or modifying Framework
content. At record authoring, SonarQube Cloud had not yet analyzed the
candidate head.

## Remaining risks

Only a static diagnostic owner changed, but moving a generic guard or applying
it to full-lifecycle paths would be a behavioral regression. At record
authoring, final diff review, exact-head hosted checks, and fresh SonarQube
Cloud analysis remained required before the issue could be considered
remediated.

## Final diff and review status

At record authoring, the task worktree contained only the scoped Parent
shell/test change and its required bilingual traceability material. Parent
`master`, Framework, MRTS, Gitlinks, scanner controls, and hosted delivery
state were unchanged.
