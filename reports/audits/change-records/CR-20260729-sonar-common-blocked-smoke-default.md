# Change Record: Parent Common blocked-runtime-smoke default dispatch for SonarQube Cloud S131

**Language:** English | [Deutsch](CR-20260729-sonar-common-blocked-smoke-default.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-common-blocked-smoke-default |
| Date (UTC) | 2026-07-29 |
| Base revision | 9f23ae2c5fe908cef38f203be03f93fda75a8dd7 |
| Tracking | SonarQube Cloud `shelldre:S131` at `common/scripts/run_blocked_runtime_smoke.sh:119`. No hosted PR or exact-head status is claimed. |
| Boundary | Parent `common` blocked runtime-smoke dispatcher, its focused dispatch regression test, and paired Change Record/index documents. Framework, MRTS, Gitlinks, workflows, SonarQube policy, and `master` are not modified. |

## Motivation and problem statement

The outer connector dispatch had an empty catch-all arm. Its final fallback happened later, which preserved behavior but did not make unsupported connector handling explicit at the `case` boundary.

## Acceptance criteria

- Every outer connector `case` value, including an unknown value, reaches a controlled blocked-dependency result.
- The known Envoy, Traefik, and Lighttpd route remains unchanged.
- The script remains POSIX-shell syntactically valid and the focused unknown-connector control remains deterministic.

## Implementation decision and rationale

The catch-all arm now calls the same `connector_skip_missing_dependency` fallback that was already used after the dispatch. This makes the terminal behavior explicit without changing the known-connector branch or broadening runtime inputs.

## Security impact

The relevant controlled input is the connector name. The invariant is that an unsupported value never selects a runtime harness, creates output paths, or executes an unrecognized command. The new default arm returns through the existing blocked-dependency control before such operations. The focused test uses a stubbed helper to prove that path; known branches are source-preserved.

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
| `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_run_blocked_runtime_smoke` | passed, 1 test. |
| `dash -n common/scripts/run_blocked_runtime_smoke.sh` | passed. |
| `shellcheck --shell=sh --severity=warning --exclude=SC1007 common/scripts/run_blocked_runtime_smoke.sh` | passed; SC1007 is an unchanged POSIX `CDPATH=` parsing warning at lines 14–17. |
| `git diff --check` | passed. |

## Tests and actual results

| Control | Result |
| --- | --- |
| Unknown connector dispatch | passed: the helper received the configured blocked reason and dependency, and the script exited successfully without starting a harness. |
| POSIX shell syntax | passed. |

## Runtime evidence

The focused test executes the real script with a temporary, minimal helper and connector tree. It reaches the unknown-connector default arm without requiring Framework/MRTS runtime dependencies.

## Checks not run and rationale

- Full connector runtime matrices were not run because the changed fallback deliberately blocks before any supported runtime path; no known connector branch changed.
- `make check-bilingual-docs` is blocked_environment: its only failures are pre-existing links into the deliberately uninitialized Framework submodule. The focused bilingual suite is run before delivery; Framework, MRTS, the submodule, and its Gitlink remain out of scope.
- Hosted GitHub Actions, SonarQube Cloud PR analysis, and review evidence are pending because no Draft PR exists yet.

## Known limitations

The pre-existing `CDPATH=` assignments produce ShellCheck SC1007 warnings even though `dash -n` accepts the POSIX shell syntax. This batch does not rewrite those unrelated assignments.

## Remaining risks

The full runtime matrix and exact-head hosted analysis remain required to treat the Sonar finding as resolved. The default arm preserves the existing controlled skip semantics rather than attempting unsupported connector execution.

## Final diff and review status

The scoped diff contains one default dispatch change, one focused regression test, and paired traceability. No commit, push, PR, or merge has occurred; Draft-PR delivery and exact-head hosted verification remain pending.
