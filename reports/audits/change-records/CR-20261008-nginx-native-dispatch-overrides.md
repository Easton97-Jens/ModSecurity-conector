# Change Record: CR-20261008-nginx-native-dispatch-overrides

**Language:** English | [Deutsch](CR-20261008-nginx-native-dispatch-overrides.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-native-dispatch-overrides |
| Date (UTC) | 2026-10-08 |
| Base revision | `9dcd35c7e380c1fc46d12bfd1fa53cfacb999775` |

## Motivation and problem statement

Read-only registry audit found three stale Parent dispatcher descriptors: body pointer rejection actually occurs in Phase1; before-commit soft-budget timeout occurs in Phase1; clean shutdown has visible HTTP200 independently of process exit0. Exact descriptor comparison rejected the current Framework catalog before native invocation.

## Acceptance criteria

Match all42 current Framework descriptors exactly, including these three approved overrides. Reject absent, wrong or boolean phase/status overrides. Preserve generic case expectations, all other dispatch controls and strict missing fault fixtures. No build or native runtime.

## Implementation decision and rationale

Only the dispatcher CONTRACTS override table is corrected: body_size_nonzero_with_null_data phase1/status400; engine_timeout_before_commit phase1/status504/noRule/native504/engine_timeout; clean_shutdown native status200. All existing operations, actual CLI, source sealing, fault requirements and selected-case guards remain unchanged. No catalog or schema is changed.

## Changed files

`ci/runtime/lifecycle/run-selected-nginx-native-operations.py`, existing `tests/test_nginx_native_operation_dispatch.py` and this EN/DE pair only. Central collector, wrapper, Root integration, Framework, MRTS and Gitlinks are untouched.

## Commands executed

Test-first `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 NGINX_NATIVE_REGISTRY_FRAMEWORK_ROOT=<current-framework-root> python -m unittest tests.test_nginx_native_operation_dispatch.DispatcherTests.test_current_native_phase_and_clean_shutdown_overrides tests.test_nginx_native_operation_dispatch.DispatcherTests.test_exact_current_framework_registry_selects_all42 -v` exited1: three mismatched descriptor assertions and actual catalog selection rejection.

After the bounded correction, `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 NGINX_NATIVE_REGISTRY_FRAMEWORK_ROOT=<current-framework-root> python -m unittest tests.test_nginx_native_operation_dispatch tests.test_nginx_selected_native_wiring tests.test_nginx_native_operation_collection -v` exited0: 29 controlled tests, no skips. The actual current Framework catalog was read, not recreated from dispatcher constants. Tests used the Parent-owned Python environment. Parent archive and whitespace checks are reported in the handoff.

## Security impact

No validation relaxation or product security remediation. Exact closed descriptor comparison still rejects degraded or injected overrides, including boolean values pretending to be phase integers. Fault-library authority and original-byte retention remain strict.

## Runtime evidence

Pure descriptor, orchestration and retained-file fixtures only. No NGINX build/process/request, canonical PASS or Exact-Head runtime claim.

## Known limitations

The catalog parity test requires an actual current Framework checkout, or explicit NGINX_NATIVE_REGISTRY_FRAMEWORK_ROOT; it skips when neither exists. The recorded29-test invocation supplied the current checkout and had no skips.

## Remaining risks

Source whitelist, canonical fact-contract integration and serialized native verification remain coordinator-owned. Matching descriptors establishes planning/wiring only.

## Checks not run and rationale

No build, native runtime, full E2E or remote CI/Sonar: outside this bounded ownership. No package installation, pin, history rewrite or Root worktree mutation.

## Final diff and review status

Four scoped files reviewed. No invocation algorithm, selection scope, generic Framework expectation or native event was changed. Normal isolated commit handed to coordinator.
