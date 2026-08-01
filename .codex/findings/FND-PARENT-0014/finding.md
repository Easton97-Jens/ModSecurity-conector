# FND-PARENT-0014 — Manifest cleanup retains a same-UID leaf-replacement deletion race

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0014` |
| Title / Titel | `Manifest cleanup retains a same-UID leaf-replacement deletion race` |
| Category / Kategorie | `security_candidate` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P1` |
| Severity / Severity | `medium` |
| Confidence / Confidence | `probable` |
| Status | `blocked` |
| Feasibility status / Machbarkeitsstatus | `blocked_missing_evidence` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

The helper revalidates each planned leaf through a pinned parent directory
descriptor, then deletes that name in a later `unlinkat`/`rmdir` operation. A
hostile same-UID process with mutation authority can replace the leaf in the
final interval.

## Observed behavior / Beobachtetes Verhalten

`validate_planned_operations()` compares type, device, inode, owner, group,
and mode through the parent descriptor. `remove_planned_paths_no_follow()`
then calls `os.rmdir()` or `os.unlink()` by the same name and descriptor in a
distinct operation.

## Expected behavior / Erwartetes Verhalten

Descriptor anchoring must still prevent ancestor traversal and deletion outside
the registered run. A strict no-foreign-leaf deletion claim requires an atomic
expected-object deletion primitive or a separately verified trust boundary;
neither is currently proven.

## Impact / Auswirkung

The pinned parent descriptor bounds deletion to the registered run; this is not
an escape to Parent, Framework, MRTS, or arbitrary host paths. It does mean
that strict no-foreign-object deletion is not proven against a hostile same-UID
leaf replacement.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/bin/storage-budget`
- `.codex/tests/test_storage_budget.py`
- `.codex/context/storage-policy.md`

### Symbols / Symbole

- `validate_planned_operations`
- `remove_planned_paths_no_follow`

## Preconditions / Voraussetzungen

- A hostile process shares the effective UID that owns a registered task-run
  directory.
- It can mutate the planned leaf name in the pinned parent directory.
- It replaces the leaf after final validation and before `os.unlink()` or
  `os.rmdir()`.

## Reproduction / Reproduktion

- `validate_planned_operations()` gets final no-follow leaf metadata through
  `operation.parent_descriptor`.
- `remove_planned_paths_no_follow()` performs `os.unlink()` or `os.rmdir()` by
  that name in a later operation.
- The current 49-test suite covers special files, symlinks, mounts, retained
  evidence, and foreign-process references, not deterministic final leaf
  replacement.

## Evidence / Evidence

- Run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/062-same-uid-pathname-toctou-static-review.log`, source-to-sink review,
  SHA-256 `2294d4ff41b1266a34a234da0db62072cadd51199efe37db979114ebcafc2dd2`,
  exit `0`, observed `2026-07-17T14:26:58Z`.
- `logs/043-storage-budget-security-regression-final.log`, SHA-256
  `0b1322f17bb7c1fe5ed71f2b9f94d7eca8c4a01189982289798629a12f6e22ac`, proves
  49 focused current controls but not an atomic final leaf identity boundary.

## Root-cause analysis / Grundursachenanalyse

POSIX pathname removal separates final leaf identity validation from removal.
Parent descriptors prevent parent traversal but do not make later removal
conditional on observed device/inode.

## Proposed remediation / Vorgeschlagene Remediation

Before making a strict claim, preserve the affected object for manual
owner-authorized handling, use a separately trusted cleanup authority, or
establish a compatible atomic expected-object deletion mechanism. Do not weaken
descriptor anchoring, special-file refusal, evidence/process gates, or
dry-run/apply controls.

## Acceptance criteria / Akzeptanzkriterien

- The helper never claims unavailable atomic `unlink-if-inode` or
  `rmdir-if-inode` behavior.
- Either a verified boundary prevents hostile same-UID leaf replacement, or
  automatic deletion of the affected class fails closed.
- Existing anchored-root, symlink, special-file, mount, evidence, process,
  dry-run, apply, and idempotency controls remain covered.

## Validation plan / Validierungsplan

- Validate the selected boundary with a deterministic same-UID replacement
  attempt between final validation and removal.
- Rerun focused storage-budget controls, including normal task-owned regular
  file and empty-directory cases.
- Verify that no Parent, Framework, MRTS, retained-evidence, or out-of-run path
  can be affected.

## Regression tests / Regressionstests

- `.codex/tests/test_storage_budget.py`
- A future deterministic final-leaf replacement control after an architectural
  solution is selected.

## Legitimate control tests / Legitime Kontrolltests

- The retained 49-test storage suite passes normal task-owned cleanup and
  currently covered safety controls.

## Dependencies / Abhängigkeiten

- Evidence for a compatible atomic deletion primitive or a user-authorized
  separately trusted cleanup-boundary design.

## Blockers / Blocker

- No current repository-supported atomic expected-object removal primitive or
  separately owned cleanup authority.

## Related findings / Verwandte Findings

- `FND-HOST-0001`
- `FND-PARENT-0013`

## Residual risk / Restrisiko

The helper is materially safer and root-bounded, but it is not proven to
preserve a foreign same-UID leaf inserted after final validation. No risk has
been accepted.

## History / Historie

- `2026-07-17T14:27:29Z`: `current_task_security_boundary_identified` —
  independent final source review confirmed that final validation and later
  removal are separate leaf-name operations. Existing covered controls remain
  effective, but no atomic same-UID leaf-identity boundary is proven.
