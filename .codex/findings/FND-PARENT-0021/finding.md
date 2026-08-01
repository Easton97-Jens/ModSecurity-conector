# FND-PARENT-0021 — Storage-budget finalization cannot clean task-owned validation and build artifacts

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | FND-PARENT-0021 |
| Title / Titel | Storage-budget finalization cannot clean task-owned validation and build artifacts |
| Category / Kategorie | storage_cleanup |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priority / Priorität | P2 |
| Severity / Schweregrad | not_applicable |
| Confidence / Konfidenz | reproduced |
| Status | blocked |
| Feasibility status / Machbarkeitsstatus | out_of_scope |
| Release blocker / Release-Blocker | false |
| Security relevance / Security-Relevanz | false |

## Summary / Zusammenfassung

Current integration runs cannot be sealed by the repository-local
storage-budget helper. It correctly fails closed instead of deleting data:
validation-tmp cannot be registered recursively, generated engine binaries and
the Go cache are not private enough for automatic cleanup, and a task-owned
Framework source worktree contains a tracked symlink that recursive cleanup
must not follow. The task-owned evidence remains retained and no automatic or
manual deletion was performed.

## Observed behavior / Beobachtetes Verhalten

After the evidence checksum was refreshed and the five build directories were
re-registered as recursive temporary paths, a dry run had zero planned
deletions. It rejected the non-empty validation-tmp directory without recursive
registration and rejected build/engine-service/traefik-engine-service,
build/engine-service-clang/traefik-engine-service, and
build/native-middleware/gocache because their permissions were not private
enough.

On 2026-07-20, the PR #34 task made its registered Framework worktree private
and reran finalization. The helper then rejected, without following it, the
tracked symlink
`tests/mrts/infra-overlays/nginx-pr24/infra/modules-enabled/mod-http-geoip2.conf`
and produced no deletion plan.

## Expected behavior / Erwartetes Verhalten

The helper must continue to fail closed for untrusted or non-private paths. A
separately authorized storage-control-plane change may make the documented
task-owned validation and build outputs eligible for safe finalization only
with an exact recursive-path policy, private artifact permissions,
retained-evidence integrity, and the existing no-symlink, no-foreign-process,
and root-containment controls intact.

## Impact / Auswirkung

The task runs remain active instead of finalized and their registered temporary
artifacts remain on disk. The current PR #34 run is at 8.429 GiB with 54.245
GiB free and meets the 15 GiB final target, so no foreign cleanup or
deletion-bypass is justified. This is a local tooling/cleanup limitation, not
a product or security-control failure.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- .codex/bin/storage-budget
- .codex/context/storage-policy.md

### Symbols / Symbole

- command_register
- RECURSIVE_DIRECTORY_NAMES
- removal_plan_no_follow
- assert_private_owned

## Preconditions / Voraussetzungen

- A private current task run contains validation-tmp and build artifacts created
  by the authorized validation commands.
- The active manifest registers validation-tmp as a non-recursive temporary
  directory and the documented build directories as recursive temporary paths.
- The storage-budget helper enforces its recursive-directory allowlist and
  private-ownership checks.
- A registered task-owned Framework source worktree can contain a tracked
  symlink that the helper must not follow during recursive cleanup.

## Reproduction / Reproduktion

1. Register the retained evidence directory after all evidence writes.
2. Register the five documented build roots as recursive temporary paths and
   leave validation-tmp registered as a normal temporary path.
3. Run:
   rtk run '/root/git/ModSecurity-conector/.codex/bin/storage-budget finalize --run 20260718T053406Z-pr-51-master-integration-546d9dc2 --dry-run --json'
4. Observe zero planned deletions and the validation-tmp/private-permission
   fail-closed errors.
5. For the private registered Framework PR #34 worktree, run:
   rtk proxy /root/git/ModSecurity-conector/.codex/bin/storage-budget finalize --run 20260720T042405Z-framework-pr-34-master-integration-31a1528d --dry-run --json
6. Observe exit 2, zero planned deletions, and the fail-closed rejection of
   `tests/mrts/infra-overlays/nginx-pr24/infra/modules-enabled/mod-http-geoip2.conf`
   as a symlink.

## Evidence / Evidence

- Run ID: 20260718T053406Z-pr-51-master-integration-546d9dc2
  - Artifact:
    /var/tmp/codex/ModSecurity-conector/runs/20260718T053406Z-pr-51-master-integration-546d9dc2/evidence/validation/storage-finalization-fail-closed.md
  - Type: storage_finalization_fail_closed_record; SHA-256:
    146abee82f088548838293ceb760e7d919611cc39f9549832e7b400e61032719
  - Command:
    rtk run '/root/git/ModSecurity-conector/.codex/bin/storage-budget finalize --run 20260718T053406Z-pr-51-master-integration-546d9dc2 --dry-run --json'
  - Working directory: /root/git/ModSecurity-conector; exit code: 2
  - Observed at: 2026-07-18T07:05:32Z; retention:
    retained_task_evidence
- Run ID: 20260720T042405Z-framework-pr-34-master-integration-31a1528d
  - Artifact:
    /var/tmp/codex/ModSecurity-conector/runs/20260720T042405Z-framework-pr-34-master-integration-31a1528d/evidence/storage-finalization-fail-closed.md
  - Type: storage_finalization_fail_closed_record; SHA-256:
    d71163521ee4d7d01fce2fe728bee6b5bfa1a44ec1c7facf66c89f40e643d100
  - Command:
    rtk proxy /root/git/ModSecurity-conector/.codex/bin/storage-budget finalize --run 20260720T042405Z-framework-pr-34-master-integration-31a1528d --dry-run --json
  - Working directory: /root/git/ModSecurity-conector; exit code: 2
  - Observed at: 2026-07-20T05:05:00Z; retention:
    retained_task_evidence

## Root-cause analysis / Grundursachenanalyse

The cleanup helper's recursive-registration allowlist excludes validation-tmp,
and its private-ownership safeguard rejects build outputs generated with
non-private permissions. Separately, its no-symlink safeguard correctly refuses
a tracked symlink within a task-owned Framework source worktree. Both
protections are working as designed, but their combined policy does not support
finalizing these otherwise task-owned layouts.

## Proposed remediation / Vorgeschlagene Remediation

In a separate explicitly authorized control-plane task, determine whether
validation-tmp belongs to a safe recursive temporary class, ensure affected
test/build outputs are created with helper-acceptable private permissions, and
define a supported retained disposition for source worktrees that contain
tracked symlinks. Add focused storage-budget regression and legitimate-control
tests. Do not weaken evidence checksums, descriptor anchoring,
symlink/special-file rejection, process checks, mount checks, or dry-run/apply
separation.

## Acceptance criteria / Akzeptanzkriterien

- A dry run for a representative private task run yields an exact safe plan for
  all intended task-owned temporary paths or explains a supported retained
  disposition.
- The corresponding apply operation finalizes the manifest only after the same
  plan passes all no-symlink, no-foreign-process, ownership, mount, and
  evidence-integrity checks.
- No Parent, Framework, MRTS, retained-evidence, shared-cache, or foreign task
  path is eligible for deletion.
- Existing fail-closed behavior remains covered for non-private, symlinked,
  special, mounted, foreign-process-held, and out-of-run paths.
- A task-owned source worktree with tracked symlinks has either a verified safe
  retained disposition or a separately authorized, equally safe cleanup path;
  the helper never follows the symlink.

## Validation plan / Validierungsplan

- Create an isolated private test run containing the documented validation and
  build shapes.
- Run the storage-budget dry run and inspect every planned deletion path before
  apply.
- Run apply only after the plan is safe, verify a finalized manifest,
  retained-evidence checksum, and absence of only the permitted temporary
  paths.
- Rerun the focused storage-budget test suite plus negative controls for
  non-private and foreign paths.

## Regression tests / Regressionstests

- .codex/tests/test_storage_budget.py
- A focused test for recursive validation-tmp policy and helper-acceptable task
  build artifact permissions.

## Legitimate control tests / Legitime Kontrolltests

- A normal private task-owned validation/build run finalizes only its registered
  temporary paths while its evidence remains intact.
- Non-private, symlinked, special, mounted, foreign-process-held, and
  out-of-run paths continue to fail closed.

## Dependencies / Abhängigkeiten

- Explicit user authorization for a local storage control-plane change.

## Blockers / Blocker

- The current PR #51 integration task does not authorize changes to
  .codex/bin/storage-budget or storage-policy.md.
- The current Framework PR #34 integration task does not authorize changes to
  .codex/bin/storage-budget or storage-policy.md.

## Related findings / Verwandte Findings

- FND-HOST-0001
- FND-PARENT-0014

## Residual risk / Restrisiko

The task runs are not sealed and their temporary artifacts remain retained, but
no unsafe deletion took place. Evidence is retained and the final storage
target is met. No risk acceptance exists.

## History / Historie

- 2026-07-18T07:05:32Z: current_task_storage_finalization_blocked_fail_closed —
  Dry-run finalization recorded zero planned deletions and refused the non-empty
  non-recursive validation-tmp directory plus three non-private generated
  build/cache paths. No --apply or manual deletion was performed.
- 2026-07-20T05:05:00Z:
  framework_pr34_worktree_storage_finalization_blocked_fail_closed — After the
  registered private Framework PR #34 worktree passed the ownership check,
  dry-run finalization refused its tracked mod-http-geoip2.conf symlink without
  following it. No --apply, manual recursive deletion, or direct worktree
  removal was performed.
