# Change Record: CR-20261008-nginx-post-return-engine-budget

**Language:** English | [Deutsch](CR-20261008-nginx-post-return-engine-budget.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-post-return-engine-budget |
| Date (UTC) | 2026-10-08 |
| Base revision | `49e2011b21893d1d30fdeedbe177deb48af0e4ce` |

## Motivation and problem statement

Two Required native timeout records need a genuine Engine timing contract. A slow upstream is not an Engine timeout. The approved NGX-specific budget remains disabled by default.

## Acceptance criteria

Measure CLOCK_MONOTONIC around the actual four terminal process APIs; only a valid return1 and elapsed time strictly above the configured budget seals ENGINE_TIMEOUT before Common completion. Invalid returns retain their native error classification.

## Implementation decision and rationale

`modsecurity_engine_call_budget_ms` accepts decimal milliseconds, zero disables measurement, and location/server/main inheritance uses the standard unset sentinel. Detection is post-return, never a hard interruption. The P3 path emits technical failures and prevents duplicate timeout events.

## Changed files

NGINX SOURCE_MAP, common header, access/header/body/module call sites; budget bridge and actual technical emitter tests; request C fixture scaffolding. Existing pure arithmetic header and full P3 source-caller tests were committed separately.

## Commands executed

The RTK-wrapped Python unittest selection for test_nginx_engine_budget_bridge, test_nginx_native_technical_events, test_nginx_p3_technical_source, test_nginx_request_native_results and test_nginx_request_error_events freshly passed38 tests (root-budget-callers-final-focus.log, exit0). The earlier full source slice passed71 controlled C17 tests. URI/request-error/native-limit focus freshly passed32 tests. These runs use actual Common state and JSONL serialization with C17 warnings as errors.

## Security impact

No rule ID is invented; an invalid or failed native return is not hidden by elapsed time. Clock failure is CONNECTOR, not timeout. Phase completion and downstream forwarding remain sealed behind actual success.

## Runtime evidence

No new native binary/module execution is claimed. Existing diagnostic runtime has old artifact provenance and does not certify these changes.

## Known limitations

Only synchronous P1/P2/P3/P4 terminal process calls are covered, not connection/URI/append/logging/getters/cleanup. A hanging Engine call is not interrupted.

## Remaining risks

Clock behavior, directive inheritance and native before/after-commit wire effects still need fresh artifact/config/runtime proof. Source tests alone cannot close Required coverage.

## Checks not run and rationale

Fresh full build, real bounded fault invocations, integrated97 Canonical, remote CI/Sonar and protected Trusted Base execution: source and canonical integration are still in progress.

## Final diff and review status

Focused source-budget/emitter slice; unrelated BEGIN/finish/cleanup/orchestration work is intentionally unstaged. Required selection, MRTS and Gitlinks remain unchanged.
