# Change Record: Runtime event sink error persistence

**Language:** English | [Deutsch](CR-20260922-pr382-runtime-sink-errors.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260922-pr382-runtime-sink-errors` |
| Date (UTC) | `2026-09-22` |
| Base revision | `0532b5eb6dac5840b482dbc936ae1cf7a7ccbeb9` |

## Motivation and problem statement

The Runtime stored event failure as a boolean and replayed every failure as
`MSCONNECTOR_ERROR_EVENT_TOO_LARGE`. Physical write/flush failures consequently
lost their I/O class. A previously emitted terminal event could also bypass a
later failed host-action event during transaction completion. Snapshot cleanup
replaced a propagated failure with a generic incomplete-snapshot error.

## Acceptance criteria

Retain the original event failure class even without a caller error output.
Never retry a failed event or advance the hash on failure. Earlier terminal
emission must not hide a failed later event. Finish, host-rejected finish,
host-action recording and checked cleanup must preserve failure, not success.
Keep original transaction causes, healthy completion and resource cleanup.

## Implementation decision and rationale

Replace the private boolean with its existing enum error code; do not retain
borrowed messages. Both emitters use one checked writer with an always-present
local error output. Replay uses static default error text and the original code.
Move failure precedence ahead of terminal-success shortcuts and split checked
cleanup from snapshot validation. Existing sink ownership, limits, JSONL/hash
format and profile capabilities are unchanged.

## Changed files

- `common/runtime/msconnector_runtime.c`
- `tests/test_runtime_event_sink_failures.py`
- `.github/workflows/lint.yml`
- This record and its German companion.

## Commands executed

Required CI entry point:

```sh
python -m unittest -v tests.test_runtime_event_sink_failures
```

Execution is pending at preparation. Eight test methods compile actual Runtime
structures, emitters, writer and completion functions with real Common error,
allocator, serializer, hash and lifecycle modules. GNU stdio cookies inject
physical write, short-write and flush failures. The original classification
regression is reproduced by a separately compiled negative control. Native
audit/free callbacks are controlled boundaries, not a real engine execution.

## Security impact

A failed metadata sink cannot masquerade as successful transaction completion.
No raw payload, credential, scanner exception or unsupported capability is added.
Original transaction causes and independent limits remain unchanged.

## Runtime evidence

The test layer is compiled Runtime/stdio integration, not live HTTP hosts or a
six-family route matrix. Successful stdio flushing is not a durability/fsync
claim. Negative-control compilation is not a substitute for current-code tests.

## Known limitations

This addresses the identified Runtime I11 failure-latch and completion gaps.
Apache and SPOP physical-sink owners still need separate changes and tests.
Repeated cancellation/phase-invalid operations retain their own API contracts;
this does not claim every error exit is now equivalent across all routes.

## Remaining risks

After a failed required event, finish returns failure without attempting another
native audit. Best-effort destruction still releases native and contract state.
The shared stream's recovery across different transactions and all host-level
interpretations remain separate verification work.

## Checks not run and rationale

No local project commands ran because the mandatory RTK wrapper is unavailable.
Current-head GitHub CI, exact-head Sonar zero and actual host outcomes require
fresh verification. Independent secret scanning remains unresolved.

## Final diff and review status

Prepared as a scoped production/test continuation in Draft PR #382. No merge,
master push, force push, dependency, Framework/MRTS or scanner-policy change.
