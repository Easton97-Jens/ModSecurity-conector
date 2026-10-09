# Change Record: CR-20261009-selected-native-projection-parent-authority

**Language:** English | [Deutsch](CR-20261009-selected-native-projection-parent-authority.de.md)

Dispatcher-only correction of the selected-native projection-parent authority.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-selected-native-projection-parent-authority |
| Date (UTC) | 2026-10-09 |
| Base revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation and problem statement

The actual f639 native dispatch created private 0700 intermediate projection parents despite the wrapper's explicit shared parent. The unchanged projection helper correctly rejects that worker-inaccessible topology. A fresh controlled dispatcher reproduction confirms the wrong parent passed to the driver.

## Acceptance criteria

Use the exact explicit parent for every non-RAW driver without creating/changing it, private intermediates, or run IDs. Reuse actual projection-helper guards and retain private output mode, closed42 selection, required fixtures, original source receipts and NOT_EXECUTED results. Reject unsafe or overlapping authorities before host dispatch.

## Implementation decision and rationale

Load the existing fixed-path projection helper. Require actual Root coordination, an explicit absolute traversal-free parent and VERIFIED_RUN_ROOT. Apply component-NOFOLLOW directory checks, existing ownership/non-enumerability/traversal guards and existing overlap predicate against checkout/build/results/verified/cache/evidence/log/run authorities. The projection path is not constrained to SOURCE.STORAGE: the approved shared parent may be outside the verified project storage root. Runtime outputs retain their existing external/private checks. RAW-only selection does not require a projection.

## Changed files

Only `ci/runtime/lifecycle/run-selected-nginx-native-operations.py`, new `tests/test_nginx_selected_native_projection.py`, and this generated EN/DE Change Record pair in the new isolated worktree.

## Commands executed

RTK-wrapped unit commands and logs are retained externally in `D-selected-native-projection-parent-results.md`. RED: four tests, exit 1, old wrong-parent and missing-guard failures. Intermediate run failed on a new controlled receipt fixture with wrong envelope; corrected to the actual input-fault source envelope, without consumer changes. Final four complete modules: 35 tests, exit 0, no skips. `git diff --check` passed. This pair was created with the repository generator; structural verification is recorded separately.

## Security impact

No projection guard relaxation, chmod/chown of the supplied parent, symlink following, removal, reuse, or public exposure of private output. Real helper checks reject old 0700 topology and reused direct children. Tests preserve original receipt digest binding and exact global run IDs; source rows remain NOT_EXECUTED.

## Runtime evidence

Two actual projection preparations through controlled dispatcher collaborators, plus real reuse rejection and untouched separate FirstByte seed. These fixture copies use the test process's group; no nobody UID/65534 role or native NGINX host evidence is claimed. No native server or build executed. Parent Required remains 97.

## Known limitations

Existing Phase4/MIME projection child names use only run_id and collide under a shared parent. The coordinator separately assigned their case/variant child-name derivation and Framework reader binding; this dispatcher patch does not claim all-group freshness. Combined integration/native checks remain required.

## Remaining risks

Root owns integration with the concurrent dispatcher-quality patch and must provision the actual existing external parent outside VERIFIED_RUN_ROOT. The production helper's existing check/create lifecycle is unchanged. Fresh source/build/authority binding must follow integration.

## Checks not run and rationale

No native runtime, Root/nobody transition, build, protected gate, full CI/Sonar, API writes, MRTS initialization, Git stage/commit/push, or previous/shared worktree edits: outside this bounded slice. Documentation checks requiring initialized submodules remain coordinator work.

## Final diff and review status

Scoped diff reviewed against current producers and unchanged helper contract; unstaged delivery in `parent-native-projection-parent-20261009`. No edits to completed CI/sequence-quality slices. Integration and native rerun belong to Root.
