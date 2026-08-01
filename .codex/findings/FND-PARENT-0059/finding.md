# FND-PARENT-0059 — Legacy stale full-matrix lock can deny scheduler service

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0059 |
| Category | security_validated |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / medium / validated |
| Status / feasibility | fixed / feasible_now |
| Release blocker / security relevant | yes / yes |
| Scope | Local full-matrix scheduler lock and inherited-descriptor boundary |

## Validated behavior, scope, and security invariant

The prior full-matrix scheduler used a mkdir lock directory. If its owner was
terminated with SIGKILL before cleanup, that directory remained. A later
scheduler treated the orphaned path as a live owner and could be denied
service indefinitely.

The invariant is that a live scheduler opens a regular non-symlink
.full-matrix-run.lock under private MATRIX_ROOT on FD 9, acquires flock -n 9,
and holds that FD for its full lifetime. A competing scheduler cannot enter,
release, replace, or bypass a live lock. FD 9 is inherited by running job/Make
descendants. Therefore SIGKILL of the scheduler parent intentionally leaves the
lock active while such a descendant runs; the kernel releases it only when the
final holder exits, after which the same lock path can be reused. No secondary
ownership state or release interface exists.

The final local remediation is implemented directly in
ci/runtime/lifecycle/run-full-matrix-parallel.sh. It uses a POSIX-shell FD 9
and flock -n 9 on the private regular lock file for the whole scheduler and
its inherited job/Make descendants.

## Evidence and reproduction

The Parent's final current-task security review confirms the stale mkdir-lock
condition and the local remediation. The exact parent-confirmed local command
was:

PYTHONDONTWRITEBYTECODE=1 python3 -W error::ResourceWarning -m unittest -v tests.test_full_matrix_parallel_scheduler

It exited 0 with eight scheduler tests passing, including:

- test_scheduler_rejects_a_live_full_matrix_lock_owner
- test_scheduler_lock_outlives_a_sigkilled_parent_until_its_job_descendant_exits

This evidence is retained in the task conversation only; no filesystem receipt
or hosted exact-successor receipt was supplied for this finding. Reproduce the
original condition by acquiring the prior mkdir lock, killing its owner with
SIGKILL before cleanup, and starting a second scheduler. Then exercise the
final implementation for live-owner contention and for inherited FD 9 keeping
the lock active after SIGKILL of the scheduler parent until its last job/Make
descendant exits.

## Impact, cause, and remediation

An orphaned lock can deny subsequent full-matrix runs and invalidate release
evidence. A separate lock-control path could also let a competing process
impersonate release against a live owner. This is a
validated P1 availability/security boundary and release blocker.

The root cause was treating a durable mkdir pathname as proof of liveness.
The release-impersonation review rejected a separate lock-control design.
The final remediation keeps ownership in the running shell and its running
job/Make descendants: FD 9 holds flock -n 9 until the final inherited
descriptor closes. SIGKILL of only the scheduler parent does not bypass that
ownership; the kernel releases the lock after the last holder exits. It must
retain the focused tests and full scheduler isolation.

## Acceptance and validation

Acceptance requires:

- a live owner holding FD 9 and flock -n 9 rejects a competing scheduler
  without release, replacement, or bypass;
- SIGKILL of the scheduler parent leaves the kernel lock active while a
  job/Make descendant retains inherited FD 9; after the final descendant exits,
  the kernel releases the lock and a later scheduler can acquire the same path;
- the lock file is regular and non-symlink below private MATRIX_ROOT;
- only the shell-held FD 9 ownership path remains, with no secondary control
  path or release interface;
- all eight scheduler tests, including the two named regressions, pass; and
- fresh hosted exact-successor evidence confirms the behavior without
  weakening isolation or result policy.

Re-run the named unittest command with a retained local receipt, exercise
live-owner contention and the SIGKILL-parent/inherited-descendant control,
then obtain fresh hosted exact-successor full-matrix, producer, review, and
protected-integration evidence before a fixed or verified disposition.

## Dependencies, residual risk, and history

This finding is related to, but not a duplicate of, FND-PARENT-0058:
0058 owns port-range allocation and ready-artifact scheduling reliability,
while this record owns the shell-held kernel-lock and inherited-descriptor
preservation boundary.
FND-SONAR-0016 remains the aggregate Quality-Gate record.

The eight-test result is parent-confirmed task-conversation evidence only.
Until a local receipt and hosted exact-successor result are retained, the
finding remains P1 in_progress / feasible_now and a release blocker. No risk
acceptance, suppression, Framework/MRTS action, Gitlink update, close, merge,
or delivery is claimed.

Recorded 2026-07-26T20:14:08Z as
stale_full_matrix_lock_dos_validated_and_local_guarded_remediation_recorded.
Updated 2026-07-26T20:37:23Z: SIGKILL of only the scheduler parent does not
release inherited FD 9; the kernel releases the lock only after the final
job/Make descendant exits.
