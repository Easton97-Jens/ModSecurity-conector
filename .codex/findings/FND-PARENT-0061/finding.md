# FND-PARENT-0061 — Worker-wrapper death before FIFO completion can stall the full-matrix scheduler

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0061 |
| Category | lifecycle_defect |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / not_applicable / validated |
| Status / feasibility | fixed / feasible_now |
| Release blocker / security relevant | yes / no |
| Scope | Parent full-matrix worker-completion FIFO watchdog boundary |

## Fixed local behavior, scope, and non-security classification

Before the local watchdog remediation, a worker wrapper killed after fake Make
started but before it emitted its FIFO completion token left the parent
scheduler indefinitely blocked on read <&8. The wrapper could no longer report
completion, while the parent had no bounded failure path for the missing token.

The local fix bounds that failure path. With
VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS=1, a wrapper death before FIFO
completion causes the runner to exit 77 rather than wait indefinitely. Once
the child exits, the FD 9 full-matrix lock becomes reusable. This is a
lifecycle/reliability defect, not a security finding, and is fixed locally but
not hosted verified or closed.

Affected files and symbols are:

- ci/runtime/lifecycle/run-full-matrix-parallel.sh — worker wrapper, FIFO
  completion token, read <&8, timeout, and FD 9 lock reuse; and
- tests/test_full_matrix_parallel_scheduler.py — the focused wrapper-death
  lifecycle regression.

## Evidence and reproduction

The Parent confirmed that the following focused test passes:

    tests.test_full_matrix_parallel_scheduler.test_scheduler_times_out_when_a_job_wrapper_dies_before_completion

It starts fake Make, kills the wrapper before FIFO completion, sets
VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS=1, and observes runner exit 77.
After the child exits, it also observes that FD 9 is reusable. This is
parent-supplied task-conversation evidence only; no filesystem receipt or
hosted-successor result was supplied.

The original condition is reproduced by starting fake Make, killing the worker
wrapper before its FIFO completion token, and observing the pre-watchdog parent
remain blocked on read <&8. The fixed local behavior instead exits through the
bounded timeout path and releases the inherited lock only after the child exits.

## Impact, cause, and remediation

A failed worker wrapper could indefinitely stall a full-matrix run, delay or
prevent release evidence, and leave the scheduler unavailable to follow-up
work. This is therefore a P1 lifecycle/reliability release blocker.

The root cause was reliance on a FIFO completion token without a bounded
failure path. If the worker wrapper died after fake Make started but before
token emission, read <&8 had no token to consume and the parent waited
indefinitely.

The local watchdog remediation bounds the missing-token wait and reports the
controlled failure with exit 77. It retains the focused wrapper-death
regression and the FD 9 reuse control. Fresh hosted-successor evidence is
required before verified or closed status; no hosted verification, closure, or
delivery disposition is claimed.

## Acceptance and validation

Acceptance requires:

- a wrapper death after fake Make starts and before FIFO completion does not
  leave the scheduler indefinitely blocked on read <&8;
- with VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS=1, the runner exits 77;
- after the child exits, the FD 9 lock is reusable;
- the focused worker-wrapper lifecycle regression passes; and
- scheduler cap, FND-PARENT-0058 port-plan, FND-PARENT-0059 lock, manifest,
  and result-policy controls remain effective.

Retain an exact local receipt for the focused test and rerun applicable combined
scheduler controls. Obtain fresh hosted-successor full-matrix and
protected-integration evidence before verified or closed status. The local
passing result supports fixed only.

## Dependencies, residual risk, and history

The local watchdog remediation depends on retaining the focused regression and
the FND-PARENT-0059 FD 9 lock-reuse control. FND-PARENT-0058 port allocation
and FND-PARENT-0060 work-conserving refill remain separate lifecycle controls;
FND-SONAR-0016 remains the aggregate Quality-Gate record.

The local remediation is parent-confirmed task-conversation evidence only. No
retained filesystem receipt or hosted-successor result has been supplied.
Consequently the finding is P1 fixed / feasible_now and a release blocker, not
verified, closed, deferred, or risk accepted.

Recorded 2026-07-26T21:23:07Z as
local_watchdog_remediation_validated_hosted_successor_pending.
