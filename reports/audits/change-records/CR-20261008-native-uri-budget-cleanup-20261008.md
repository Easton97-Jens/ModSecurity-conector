# Change Record: CR-20261008-native-uri-budget-cleanup-20261008

**Language:** English | [Deutsch](CR-20261008-native-uri-budget-cleanup-20261008.de.md)

Bounded Parent documentation slice; no runtime promotion.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-native-uri-budget-cleanup-20261008 |
| Date (UTC) | 2026-10-08 |
| Base revision | `7c169f5bbe946650431f8e0cdbe2ddc63d3e85c1` |

## Motivation and problem statement

Describe the coordinator's inspected URI, selected-phase budget, and cleanup-order source contracts without turning compile evidence into runtime success.

## Acceptance criteria

Equivalent EN/DE reader documentation names all four measured calls and all unmeasured API groups, exact URI bounds, parser rules, and the pending runtime tuple. No source or Framework change.

## Implementation decision and rationale

Document NGINX-only URI projection (256 raw buffer/255 escaped bytes), fixed 4096-byte writer, preserved query marker, and strict other Common fields. Document per-call CLOCK_MONOTONIC post-return soft budget, disabled inherited default 0, strict elapsed > budget, and exact native success 1. Invalid slow 0/2 returns are not timeout positives. Common cleanup precedes the native void call; do not claim a new post-return cleanup receipt or HTTP proof.

## Changed files

`connectors/nginx/README.md` / `README.de.md`, `docs/connectors/nginx.md` / `nginx.de.md`, and this EN/DE record. No generated configuration reference edited.

## Commands executed

RTK-wrapped source/doc reads and the native `ci/tools/new-change-record.py create` scaffold command were executed. Portable validation commands/results:

- `rtk proxy "${PARENT_PYTHON}" ci/tools/new-change-record.py check`: exit 0, structure PASS (not evidence validation).
- `rtk proxy make check-bilingual-docs PYTHON="${PARENT_PYTHON}"`: exit 2; checker exit 1 with 22 existing missing Framework-submodule link targets in this isolated worktree, none in changed files.
- Direct `check_pairs_and_switches(Path.cwd())` from the native bilingual checker: exit 0, empty errors.
- `rtk git diff --check`: exit 0.

## Security impact

No executable change. Clarifies payload-free URI redaction, unchanged strict validation, and limits of soft budgets. No hard interruption or all-C-API timeout guarantee.

## Runtime evidence

No native runtime executed for this slice. Coordinator reports five URI query-redaction tests and fifteen compiled budget bridge tests green; these are attributed unit/compile evidence, not locally observed runtime results. Original 97 RequiredIDs/45 open remain; new tuple NOT_RUN.

## Known limitations

Source inspected in the coordinator's integration worktree; this documentation commit alone does not integrate that source. Generated directive reference remains the coordinator's responsibility. Existing historical runtime statements are not new-tuple evidence.

## Remaining risks

A hung synchronous call remains uninterruptible. Unmeasured APIs have no selected-call budget. Real host, cleanup-return, and exact-build receipts remain required before runtime promotion.

## Checks not run and rationale

No native build/runtime, Framework tests, MRTS, or publication: documentation-only owned scope and no serialized native slot. Root performs final integrated documentation review.

## Final diff and review status

Local EN/DE scope and diff review completed; record structure and pairing checks passed, full link check limitation retained above. Root performs final integrated review. No PR, merge, push, or external review claimed.
