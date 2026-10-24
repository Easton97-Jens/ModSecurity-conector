# Change Record: CR-20261008-scheduler-refill-causal-barrier

**Language:** English | [Deutsch](CR-20261008-scheduler-refill-causal-barrier.de.md)

Causal fixture synchronization only; no production scheduler change.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-scheduler-refill-causal-barrier |
| Date (UTC) | 2026-10-08 |
| Base revision | `d76cb01c84350dbaeb380929bcc80a9c7719789e` |

## Motivation and problem statement

The refill test compared fake-make timestamps across a 0.8/0.05-second sleep
window. Real metadata and subprocess startup could exhaust that window without
a proved scheduler violation. A fixed sleep does not establish causal overlap.

## Acceptance criteria

A first Apache fixture may finish successfully only after the queued Apache
has really started while the earlier NGINX job frees a slot. Keep cap 2, four
starts/ends, the original timestamp relation, maximum activity 2, final activity
0 and four manifests. Missing queued start must fail within a bounded interval.

## Implementation decision and rationale

Use marker-based synchronization only in the fake-make fixture. The first
Apache publishes its start and waits for queued Apache; the initial NGINX waits
for that first start before completing. The queued Apache publishes its actual
start after recording the activity event. No production scheduler is changed.
The positive fixture has a 15-second barrier and a 60-second outer bound.
A separate 0.1-second negative control proves missing queued start yields 97
and restores fixture activity to zero, rather than silently accepting a batch.

## Changed files

`tests/test_full_matrix_parallel_scheduler.py` and this EN/DE record pair.
Locks, scheduler implementation, production timeout/cap policy, Required
selection, connector source, Framework, MRTS and validators remain unchanged.

## Commands executed

All payloads ran through `rtk proxy` with external neutral test roots.
`python -m unittest -v` for the marker-requiring refill test before fixture
support: 1 failure, 4.898 seconds, exit 1. After support: 1 test, 5.433 seconds,
exit 0. Complete `tests.test_full_matrix_parallel_scheduler`: 16 tests,
29.728 seconds, exit 0, including lost-job/lock guards and barrier failure.
`make check-bilingual-docs check-doc-links`, archive-only
`new-change-record.py check` and `git diff --check`: exit 0.

## Security impact

No production isolation, lock, guardrail or concurrency check is relaxed.
The fake fixture strengthens the causal claim and checks its bounded failure
cleanup. It introduces no service, network, toolchain or global configuration.

## Runtime evidence

Real scheduler subprocesses with controlled fake smoke jobs prove this test
layer. They are not NGINX HTTP, native fault, canonical or protected evidence.
All 97 selected Required final records still require fresh run-bound proof.

## Known limitations

Marker synchronization is intentionally fixture-only. The original combined
failure established unreliable timing, not a production scheduling defect.
Full combined Parent validation and NGINX execution still follow this slice.
The negative fixture control is not a run of a deliberately broken product
batch-scheduler mutant.

## Remaining risks

Independent integrated runtime or CI failures may remain. Original 52 baseline
IDs and 45 missing-record targets are preserved. Existing genuine artifacts
retain their original build identities; no source/release relabeling is done.

## Checks not run and rationale

Fresh complete Parent focus, native NGINX E2E, current remote CI/Sonar and the
protected Exact-Head run are not certified by these tests. They require their
own clean-tuple and artifact gates. Ruff remains unavailable separately.

## Final diff and review status

Only the test fixture and paired record are in this separate slice.
Independent read-only review found no regression; documentation/archive/diff
gates passed before commit. PR #396 remains Draft; no merge, force push or
history rewrite.
