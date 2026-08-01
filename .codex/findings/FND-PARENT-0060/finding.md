# FND-PARENT-0060 — Full-matrix batch scheduler is not work-conserving at its concurrency cap

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0060 |
| Category | lifecycle_defect |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / not_applicable / validated |
| Status / feasibility | fixed / feasible_now |
| Release blocker / security relevant | yes / no |
| Scope | Parent full-matrix completion scheduling and capacity refill |

## Fixed local behavior, scope, and non-security classification

The prior full-matrix scheduler was not work-conserving at its configured
concurrency cap. Its batch scheduler filled a batch and waited for the whole
batch, rather than admitting the next queued job when an individual child
completed. With cap=2, a fast job could finish and free a core while its slow
sibling still ran; a third queued job then could not start until the slow
sibling exited.

The expected invariant is completion-driven admission: a completed child frees
one slot, and the next queued job starts promptly while the active-job count
remains at or below the cap. The local completion-driven remediation and its
focused regression are parent-confirmed as passing. This is a
lifecycle/reliability defect, not a security finding. It remains independently
remediable from FND-PARENT-0058's port allocation boundary and
FND-PARENT-0059's FD 9 lock-admission boundary, and is fixed locally but not
hosted verified or closed.

Affected files and symbols are:

- ci/runtime/lifecycle/run-full-matrix-parallel.sh — run_planned_jobs and its
  batch-wide wait;
- tests/test_full_matrix_parallel_scheduler.py —
  test_parallel_scheduler_refills_a_freed_slot_before_a_slow_sibling_exits;
  and
- the full-matrix concurrency cap.

## Evidence and reproduction

The Parent supplied a task-conversation static review of
ci/runtime/lifecycle/run-full-matrix-parallel.sh, run_planned_jobs, cited as
lines 680-732. The review concludes that cap=2 waits for the entire started
batch: a fast child completing before a slow sibling does not cause the third
queued job to start.

The earlier reviewer command exited 0 with eight tests passing:

    PYTHONDONTWRITEBYTECODE=1 python3 -B tests/test_full_matrix_parallel_scheduler.py

That historical result did not expose the defect: its eight tests did not cover
three unequal-duration jobs at cap=2. The Parent now confirms that
test_parallel_scheduler_refills_a_freed_slot_before_a_slow_sibling_exits passes
and that a 107-test combined scheduler run passed. These local results validate
the remediation, but they are task-conversation evidence only; no filesystem
receipt or hosted-successor result was supplied.

To reproduce the defect, configure cap=2 and submit a slow job, a fast job,
and a third queued job. Once the fast job completes while the slow job is still
active, observe that the third job remains queued. The fixed local scheduler
instead starts that third job before the slow sibling exits.

## Impact, cause, and remediation

The scheduler can leave configured capacity idle, lengthen a full-matrix run,
and increase the chance of timeouts or delayed release evidence despite queued
work. The defect is therefore a P1 lifecycle/reliability release blocker.

Its root cause is whole-batch synchronization in run_planned_jobs. The
scheduler uses completion of the slowest child as the admission boundary rather
than reaping individual children and refilling the freed slot.

The local remediation is completion-driven: it tracks and reaps individual
child completions, admits the next queued job whenever a slot is free, and
preserves the configured cap. The deterministic cap=2,
three-unequal-job regression now passes locally. FND-PARENT-0058 port-plan
controls, FND-PARENT-0059 live-lock and inherited-FD 9 controls, and
manifest/result controls must remain preserved. Fresh hosted-successor evidence
is required before verified or closed status.

## Acceptance and validation

Acceptance requires:

- with cap=2 and three unequal-duration jobs, the queued third job starts
  after the fast sibling completes and before the slow sibling exits;
- the scheduler never exceeds two active jobs;
- FND-PARENT-0058 port-allocation controls remain effective;
- FND-PARENT-0059 live-lock and inherited-FD 9 controls remain effective;
- manifest and result-policy controls remain effective; and
- test_parallel_scheduler_refills_a_freed_slot_before_a_slow_sibling_exits
  exposes the former batch-wide wait and passes with the local remediation.

The local focused regression and parent-confirmed 107-test combined scheduler
run support fixed. Retain exact local receipts and exercise the cap, port,
lock, manifest, and result-policy controls. Fresh exact-successor full-matrix
and hosted evidence are required before verified or closed status. The earlier
eight-test reviewer command remains a historical coverage-gap observation, not
the proof of the local fix.

## Dependencies, residual risk, and history

Dependencies are the retained Parent scheduler remediation and deterministic
regression, while FND-PARENT-0058, FND-PARENT-0059, and FND-PARENT-0061 remain
independent controls that must be preserved. FND-SONAR-0016 remains the
aggregate Quality-Gate record.

The local remediation, named regression, and 107-test combined run are
parent-confirmed task-conversation evidence only; no retained filesystem
receipt or hosted-successor evidence has been supplied. Consequently the
finding is P1 fixed / feasible_now and a release blocker, not verified, closed,
deferred, or risk accepted.

Recorded 2026-07-26T20:48:02Z as
validated_non_work_conserving_batch_scheduler_allocated.
Updated 2026-07-26T21:23:07Z as
local_completion_driven_refill_validated_hosted_successor_pending.
