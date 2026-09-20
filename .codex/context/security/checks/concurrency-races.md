# Concurrency and Race Check

Assess concurrent requests/streams/sessions, shared maps/caches/counters, cancellation versus response, timeout versus reply, cleanup versus write, reload/restart while active, late callbacks/frames, transaction-ID reuse, socket/path replacement, log rotation, config/rule reload, and response-commit races.

For every race candidate identify shared mutable state, owners, synchronization, lifetime, attacker timing/control, failure effect, and whether isolation holds for a legitimate concurrent control.

Use controlled race/fault-injection tests only; do not create uncontrolled load.
