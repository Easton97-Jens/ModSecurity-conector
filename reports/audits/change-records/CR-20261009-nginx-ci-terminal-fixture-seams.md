# Change Record: CR-20261009-nginx-ci-terminal-fixture-seams

**Language:** English | [Deutsch](CR-20261009-nginx-ci-terminal-fixture-seams.de.md)

Test-only synchronization with the current native callback and cleanup seams.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-ci-terminal-fixture-seams |
| Date (UTC) | 2026-10-09 |
| Base revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation and problem statement

The captured CI scaffold failure and fresh local reproduction showed missing fields/collaborators in the compiled late-error fixture and two stale inline-source assertions. Production code already delegates cleanup and captures the native append return before checking it.

## Acceptance criteria

Both complete assigned test modules must pass while retaining terminal/no-forward, native-return, EOS, cleanup, and failure-cause checks. No product source, gate parser, required-case selection, or runtime authority may change.

## Implementation decision and rationale

Extend the bounded C fixture with actual context fields, the disabled-budget collaborator, and a separately counted completion-observation collaborator. Exercise its failure before intervention. Follow the actual delegated cleanup function and captured append return; reject missing/late cleanup, missing Common cleanup, ignored/overwritten/hardcoded native returns, and premature append accounting using in-memory mutations.

## Changed files

`tests/test_nginx_late_error_results.py`, `tests/test_nginx_upstream_security_contract.py`, and this generated EN/DE Change Record pair only.

## Commands executed

Run through `rtk proxy`, with bytecode disabled, external `TMPDIR`/`RUNNER_TEMP`, and explicit `FRAMEWORK_ROOT`: `python -m unittest -v tests.test_nginx_late_error_results tests.test_nginx_upstream_security_contract`. Before edits: exit 1, 18 tests, two failures and one setup error (`D-ci-r1-red.log`). After edits: exit 0, 31 tests (`D-ci-r2-green.log`). The fixture compiles with `-std=c17 -Wall -Wextra -Werror`. Generator `create --name nginx-ci-terminal-fixture-seams --base-revision f63996290925f4b0c04d286506171825de9dc2ff --date 2026-10-09` and `git diff --check` both exited 0. Detailed commands and subsequent documentation checks are retained in the external task report.

## Security impact

No production security behavior changes. Negative checks preserve fail-closed native results, cleanup ordering, and terminal re-entry. Sonar missing-count handling remains FAIL; no fabricated zero and no suppression were introduced.

## Runtime evidence

Only compiled control-flow and source-contract evidence. No native NGINX host, server, namespace supervisor, or protected gate was executed. Parent required-case count remains 97.

## Known limitations

Timing and completion-observation production implementations are controlled collaborators, not independently verified here. Full CI and actual runtime validation remain coordinator work. The Change Record structure check passed (exit 0). Whole-checkout bilingual and link checks each exited 1: existing links point into the uninitialized Framework submodule in this isolated worktree. The explicit external Framework override does not rewrite those links; no submodule was initialized.

## Remaining risks

Future source-seam changes can require fixture maintenance. Existing remote Sonar findings and decoration-parser uncertainty are not resolved by these tests.

## Checks not run and rationale

No build, live native/runtime execution, remote API writes, MRTS initialization, dependency installation, stage/commit/push, or shared Source edits: outside this tight test-only scope.

## Final diff and review status

Scoped changes reviewed against actual source and the fresh RED/GREEN evidence. Delivery is an unstaged isolated-worktree diff for coordinator review and integration, not a commit or runtime approval.
