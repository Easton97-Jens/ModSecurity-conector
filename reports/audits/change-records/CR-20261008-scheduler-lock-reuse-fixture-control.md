# Change Record: CR-20261008-scheduler-lock-reuse-fixture-control

**Language:** English | [Deutsch](CR-20261008-scheduler-lock-reuse-fixture-control.de.md)

Test-only fault/positive-control separation; no product runtime claim.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-scheduler-lock-reuse-fixture-control |
| Date (UTC) | 2026-10-08 |
| Base revision | `5e22a9f0cc9b688ddc271012467b053bca8d1bfb` |

## Motivation and problem statement

The lost-wrapper fixture inherited its deliberate one-second job timeout into
its separate lock-reuse control. Exit 77 from a real completion timeout was
retried as if it proved lock contention; discarded diagnostics made the final
failure misleading. No remaining production lock defect is established.

## Acceptance criteria

Keep the original lost-wrapper timeout and live-owner/descendant lock guards.
The reuse control must not mutate fault inputs or retry a completion timeout.
Use its own bounded job budget and preserve observed conflict diagnostics.

## Implementation decision and rationale

Copy the fixture environment and set the positive reuse control to 30 seconds.
Retry exit 77 only when stderr reports `another full-matrix run owns`.
Keep the original one-second fault unchanged. Three deterministic controls
prove input preservation, timeout rejection and legitimate contention retry.

## Changed files

`tests/test_full_matrix_parallel_scheduler.py` and this EN/DE Change Record
pair only. No product scheduler, lock, timeout policy, connector, Framework,
MRTS, capability, selection or canonical validator changes.

## Commands executed

All command payloads ran through `rtk proxy` with external neutral test roots.
`python -m unittest -v` for the two new negative controls: 2 failures, exit 1
before the helper correction. The initial six-name green invocation had five
passing tests and one nonexistent-name loader error, exit 1; not certified.
Corrected six-test invocation: 6 tests, 11.709 seconds, exit 0, including actual
lost-wrapper timeout, live-owner rejection and descendant lock lifetime.
`make check-bilingual-docs check-doc-links`, archive-only `new-change-record.py
check`, shell syntax/ShellCheck of the external focus launcher and
`git diff --check`: exit 0. Scoped diff and independent read-only review found
no blocking issue.

## Security impact

No production lock or security check is relaxed. A non-lock exit 77 now fails
the test immediately instead of being silently retried. Fault and positive
control inputs remain separate; the actual inherited-lock guard is retained.

## Runtime evidence

Real scheduler subprocesses exercised the focused process/lock controls.
These are test fixtures, not NGINX requests or coverage evidence. All 97 selected
Required final records still need fresh run-bound evidence; no canonical PASS
or protected HostGate claim is made.

## Known limitations

The old combined log cannot distinguish actual lock contention from a later
positive-control job timeout. The separate refill timing failure is not fixed
by this change and the complete Parent focus still requires a fresh rerun.

## Remaining risks

A full combined test/runtime run may uncover independent failures. Original
52 baseline IDs and 45 missing-record targets are unchanged. PR #396 remains
Draft; this record is not delivery, current CI or Sonar closure evidence.

## Checks not run and rationale

No fresh full Parent focus, NGINX E2E or protected Exact-Head run for this
slice; they follow independent fixture repairs and final clean-tuple gates.
Ruff is unavailable separately; no tool or dependency installation is made.

## Final diff and review status

Scoped test-only diff inspected; independent read-only review found no blockers.
Archive, bilingual and link checks passed before the separate commit.
No history rewrite, broad staging, framework pin or MRTS modification.
