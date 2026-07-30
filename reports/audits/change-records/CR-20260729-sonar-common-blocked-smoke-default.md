# Change Record: Parent Common blocked-runtime-smoke default dispatch for SonarQube Cloud S131

**Language:** English | [Deutsch](CR-20260729-sonar-common-blocked-smoke-default.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-common-blocked-smoke-default |
| Date (UTC) | 2026-07-29 |
| Base revision | 9f23ae2c5fe908cef38f203be03f93fda75a8dd7 |
| Synchronized validation base | fda62539b6f0a710865707e3003b73ed4469f20e |
| Tracking | SonarQube Cloud `shelldre:S131` at `common/scripts/run_blocked_runtime_smoke.sh:119`. No hosted PR or exact-head status is claimed. |
| Boundary | Parent `common` blocked runtime-smoke dispatcher, its focused dispatch regression test, and paired Change Record/index documents. Framework, MRTS, Gitlinks, workflows, SonarQube policy, and `master` are not modified. |

## Motivation and problem statement

The selected-connector configuration `case` at the tracked Sonar location had
no `*)` arm. The outer connector dispatch also had an empty catch-all arm;
its final fallback happened later, which preserved behavior but did not make
unsupported connector handling explicit at that boundary.

## Acceptance criteria

- The tracked selected-connector configuration `case` contains a fail-closed
  `*)` arm that reaches a controlled blocked-dependency result.
- Every outer connector `case` value, including an unknown value, reaches a controlled blocked-dependency result.
- The known Envoy, Traefik, and Lighttpd route remains unchanged.
- The script remains POSIX-shell syntactically valid; focused controls cover
  both the unknown-connector dispatch and the inner-case default structure.

## Implementation decision and rationale

The tracked inner `case` now has a `*)` arm that calls the existing
`connector_skip_missing_dependency` fallback with the already resolved
runtime metadata. The outer catch-all also calls that fallback explicitly.
Both paths are fail-closed and preserve the known-connector branch and runtime
input boundary.

## Security impact

The relevant controlled input is the connector name. The invariant is that an
unsupported or incompletely configured value never selects a runtime harness,
creates output paths, or executes an unrecognized command. Both default arms
return through the existing blocked-dependency control before such operations.
The focused dispatch test uses a stubbed helper only for outer-path argument
routing; a separate structural focused control asserts the actual inner
configuration `case` has the fail-closed default. Known branches are
source-preserved.

## Changed files

- `common/scripts/run_blocked_runtime_smoke.sh`
- `tests/test_run_blocked_runtime_smoke.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260729-sonar-common-blocked-smoke-default.md`
- `reports/audits/change-records/CR-20260729-sonar-common-blocked-smoke-default.de.md`

## Commands executed

| Command or control | Actual result |
| --- | --- |
| `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_run_blocked_runtime_smoke` | passed, 2 tests. |
| `dash -n common/scripts/run_blocked_runtime_smoke.sh` | passed. |
| `shellcheck --shell=sh --severity=warning --exclude=SC1007 common/scripts/run_blocked_runtime_smoke.sh` | passed; SC1007 is an unchanged POSIX `CDPATH=` parsing warning at lines 14–17. |
| `git diff --check` | passed. |

## Tests and actual results

| Control | Result |
| --- | --- |
| Unknown connector dispatch | passed: the synthetic helper received the configured blocked reason and dependency; this is an outer-path argument-routing control. |
| Selected-connector configuration default | passed: a focused structural control confirms the tracked inner `case` contains the fail-closed helper invocation. |
| POSIX shell syntax | passed. |

## Runtime evidence

The focused dispatch test executes the real script with a temporary, minimal
helper and connector tree. It reaches the outer unknown-connector default arm
without requiring Framework/MRTS runtime dependencies. The structural control
is intentionally tied to the actual S131 configuration `case`; it does not
claim a full runtime execution of that otherwise outer-guarded branch.

## Checks not run and rationale

- Full connector runtime matrices were not run because the changed fallback deliberately blocks before any supported runtime path; no known connector branch changed.
- Full-repository bilingual and documentation-link checks are evaluated in a registered isolated worktree with the pinned Framework checkout; they do not authorize a Framework, MRTS, or Gitlink change.
- Exact-head hosted GitHub Actions, SonarQube Cloud PR analysis, review, thread, and ruleset evidence remain mandatory before a master integration.

## Known limitations

The pre-existing `CDPATH=` assignments produce ShellCheck SC1007 warnings even though `dash -n` accepts the POSIX shell syntax. This batch does not rewrite those unrelated assignments.

## Remaining risks

The full runtime matrix remains separately useful for supported connector
routes, but it is not evidence for these fallbacks because the changed paths
block before any supported runtime harness. Exact-head hosted analysis and
applicable project checks remain mandatory before the tracked S131 finding can
be treated as resolved. The defaults preserve controlled skip semantics rather
than attempting unsupported connector execution.

## Final diff and review status

The scoped diff contains two fail-closed default-dispatch changes, two focused
regression controls, and paired traceability. This record does not assert a
remote update or master merge. Before every delivery action, the exact
synchronized candidate, current PR head, reviews, threads, required checks,
and SonarQube Cloud result must be read again.
