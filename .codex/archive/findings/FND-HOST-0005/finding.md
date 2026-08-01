# FND-HOST-0005 — Historical shared temporary-root usage no longer blocks storage finalization for the GitHub Code Scanning disposition run

## Identity

| Field | Record |
| --- | --- |
| Category | storage_cleanup |
| Repository / ownership | host_environment / host_environment |
| Priority / severity / confidence | P2 / not_applicable / confirmed |
| Lifecycle status | verified |
| Feasibility / storage status | already_fixed / ok |
| Current-task disposition | verified_current_storage_target |
| Release blocker / security relevance | false / false |
| Related findings | FND-PARENT-0021, FND-PARENT-0022 |

## Summary and observed behavior

The historical run 20260718T084215Z-github-code-scanning-disposition-14-15-babc842c exceeded the 15 GiB final target without owning a registered cleanup path. On 2026-07-26, a current read-only storage-budget check reported status ok at 9.570 GiB. The original capacity condition therefore no longer reproduces.

The historical dry run exited 2 at 15.630 GiB with an empty deletion plan. The task-owned current evidence run completed dry-run and apply finalization at 9.572 GiB with status ok, an empty plan, and zero deleted paths. No shared, foreign, cache, evidence, Framework, MRTS, product, or gitlink path was deleted.

## Expected behavior and controls

Storage finalization may remove only current-run, manifest-registered, task-owned temporary paths after fail-closed checks pass. Shared, foreign, cache, retained-evidence, Framework, MRTS, product, and gitlink paths must never be deleted merely to reach a capacity target.

The historical disposition-run manifest continues to have no registered_paths or managed_paths. It was not retroactively modified. The helper keeps its empty plan rather than extending cleanup authority to shared data.

## Evidence and reproduction

- Historical run ID: 20260718T084215Z-github-code-scanning-disposition-14-15-babc842c
  - Artifact: /var/tmp/codex/ModSecurity-conector/runs/20260718T084215Z-github-code-scanning-disposition-14-15-babc842c/evidence/storage-finalize-dry-run.md
  - SHA-256: 773148f2094aba5b2bb9ac51516a7caee7e682859fe46fe9d27cf953eb484855
  - Result: dry-run exit 2, temporary_exceed, no deletion plan.
- Current revalidation run ID: 20260726T171843Z-fnd-host-remediation-20260726-cf748da4
  - Artifact: /var/tmp/codex/ModSecurity-conector/runs/20260726T171843Z-fnd-host-remediation-20260726-cf748da4/evidence/fnd-host-0001-0005-current-revalidation.md
  - SHA-256: eec6402faaa6981206613db5d9368f1298c7f4e0216fc8e21f2522de29f9e852
  - Recorded commands: storage-budget check --json; task-owned dry-run and apply finalization.
  - Result: check exit 0 / status ok at 9.570 GiB; finalization exit 0 / status ok at 9.572 GiB; empty plan and zero deleted paths.
- The focused storage-helper suite passed all 49 tests, including symlink, special-file, registered-only, retained-evidence, ownership, mount, and foreign-process controls.

Reproduce only with a read-only check. Before any future apply action, inspect a task-owned run manifest and dry-run plan. Do not add historical cleanup registrations or delete shared data.

## Root cause, remediation, and validation

The historical capacity condition resulted from shared-root usage above the target while the historical run owned no cleanup path. Current root usage is below the target, and no Parent source change is required.

Acceptance evidence:

1. A current read-only check is below the configured final target.
2. A task-owned dry-run and apply finalization had an empty deletion plan.
3. Retained evidence and all Parent, Framework, MRTS, shared, cache, product, and gitlink paths remained untouched.

Continue safe read-only monitoring. Any future cleanup remains a separately authorized host/storage-owner action limited to manifest-registered task-owned paths.

## Regression and legitimate controls

- Regression: .codex/tests/test_storage_budget.py passed 49 tests.
- Legitimate control: a registered private task path can be planned only after all fail-closed checks pass.
- Negative control: unregistered shared, foreign, cache, evidence, symlinked, special, mounted, or foreign-process-held paths remain ineligible for automatic cleanup.

## Dependencies, blockers, and residual risk

There is no active capacity dependency or blocker. The historical run remains intentionally unmodified because it owns no cleanup registration. Future shared-root growth must be monitored; any ownership-aware cleanup needs separate authorization.

## Current user-directed archive

The current user directed a lossless archive of this non-blocking verified
storage-capacity finding. Its lifecycle remains `verified`; this is not a new
closure, release approval, or authorization to clean shared data. Restore the
complete triplet and rerun the read-only storage and safe-finalization controls
if the capacity condition becomes material again.

Archive decision evidence: run
`20260726T180544Z-fnd-host-archive-20260726-8b20e52d`, artifact
`evidence/fnd-host-user-directed-archive-scope-disposition.md`, SHA-256
`50f77adb2bfbe8dbea9341bb4012ed67acaa4bf43a540ef3268f7ef2121c666b`.

## History

- 2026-07-18T09:43:15Z: recorded as blocked_environment / temporary_exceed after a retained dry-run showed no planned deletion.
- 2026-07-26T17:20:59Z: current capacity condition verified. The root was below target, and the task-owned finalization controls completed with an empty plan and zero deletions. Status changed to verified, not closed.
