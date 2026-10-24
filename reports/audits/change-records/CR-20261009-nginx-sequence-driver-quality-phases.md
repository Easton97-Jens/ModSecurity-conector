# Change Record: CR-20261009-nginx-sequence-driver-quality-phases

**Language:** English | [Deutsch](CR-20261009-nginx-sequence-driver-quality-phases.de.md)

Bounded sequence-driver refactor against captured Sonar findings, without runtime claims.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-sequence-driver-quality-phases |
| Date (UTC) | 2026-10-09 |
| Base revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation and problem statement

The captured f639 analysis reports S3776 (`run`: 71), six S1192 duplicate artifact/config literals, and S7498 for the observation constructor. The driver combined preparation, fixture setup, execution/cleanup, observations, and receipts.

## Acceptance criteria

Extract bounded phase helpers without changing CLI, case selection, identities, configuration, original evidence bytes, validation error precedence, or FD cleanup boundaries. Preserve strict negative controls. Remote closure must remain unclaimed.

## Implementation decision and rationale

Separate controls/assets/projection, closed fault setup, client capture, execution, observations, receipt construction, and publication. Keep the existing stop/fsync/close nested `finally` in `execute_sequence`; acquisition and config testing still precede that boundary. Name repeated leaves/config locations and use a dictionary literal for the same observation fields. Three closed typed records hold cohesive launch/config-test inputs (`PreparedInvocation`), actual execution/wire outcome (`ExecutionOutcome`), and original snapshot/config/projection receipt context (`ReceiptContext`). All top-level functions have at most seven explicit parameters. No generic kwargs/context bag, invocation framework, or reconnect behavior was introduced.

## Changed files

`ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py`, `tests/test_nginx_begin_driver_evidence.py`, new `tests/test_nginx_sequence_driver_phases.py`, and this generated EN/DE pair. Existing sequence-client/upstream, compiled fixtures, Framework, MRTS, and shared Source remain untouched.

## Commands executed

RTK-wrapped unit commands and exact environments are retained in external `D-sequence-driver-quality-results.md`. Baseline: 22 tests, exit 1, 12 UID-transition subtest failures (compiled BEGIN child exit 70). New characterization before Source edits: four tests, three passing behavioral controls and one intended missing-seam failure. Domain-boundary RED: 14 tests, exit 1, three parameter-count failures and one missing-record error. Parser-failure RED: one test, exit 1, captured wire became null. Final combined non-UID/CI regression after correction: 68 tests, exit 0, no skips. AST syntax and `git diff --check` passed. Generator created this pair; structure check is separately retained. Sonar rule GET attempts failed authentication before analysis; no services or credentials were changed.

## Security impact

Private fresh descriptor flags and exact transaction/phase controls remain unchanged. Tests cover required fixture absence, mismatched transaction controls, original wire retention, same-socket/abort/backpressure parameters, cleanup failure, and fsync failure with guaranteed FD close. Domain checks preserve exact child FD forwarding and ensure the config test receives no pass_fds. Original raw hashes and dict mapping-override semantics remain intact; record fields cannot be reassigned or extended by arbitrary keywords. Validation errors precede host/client failures exactly as before. No PASS promotion or guard suppression.

## Runtime evidence

Pure orchestration doubles, bounded loopback client tests, and existing compiled Common budget tests only. No NGINX/runtime supervisor, protected gate, production build, or native host execution. Parent required count remains 97.

## Known limitations

The sandbox cannot execute the BEGIN fixture's real UID transition; coordinator must rerun those unchanged controls outside the sandbox. Local AST branch inventory is not Sonar Cognitive Complexity or remote closure. Whole-checkout documentation checks already fail on uninitialized Framework link targets in this isolated worktree. Independent review found a refactor regression: parsing inside the capture helper lost captured wire facts when parsing raised. `capture_sequence_wire` now returns the original facts and response bytes before parsing; the execution helper assigns them before invoking the unchanged parser. Error precedence, raw hashes, empty failed requests and absent facts on capture failure are explicitly tested. No generic context, new execution branch, or extra exception handling.

## Remaining risks

Current-source native artifacts and authorities require fresh coordinator validation after integration. Existing pre-execution acquisition/exception boundaries are deliberately preserved, not redesigned. No live timing or independent host-role evidence is claimed.

## Checks not run and rationale

No full CI/Sonar analysis, native build/runtime, dependency installation, external services, MRTS initialization, Git staging/commit/push, or shared Source changes: outside authorized scope. Sonar rule lookup was unavailable because CLI authentication/keychain was unavailable.

## Final diff and review status

Diff reviewed against the original producer ordering and controlled RED/GREEN evidence. Unstaged isolated-worktree delivery; separate Change Record from the earlier CI fixture repair. Coordinator owns integration, outside-sandbox UID rerun, and remote quality closure.
