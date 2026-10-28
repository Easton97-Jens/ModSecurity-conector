# Current documentation and conflict reconciliation

**Language:** English | [Deutsch](CR-20261028-documentation-reconciliation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261028-documentation-reconciliation` |
| Date (UTC) | 2026-10-28 |
| Pull request | #383 |
| Branch | `docs-refresh-root-readmes` |
| Previous documentation head | `ab01cc60e638f03915fc0cc4f1541d91f9c6a62e` |
| Reconciled master | `15cea9e4d778fa1ec6e27e6fe084b347010f1367` |
| Previous common base | `820b6975495bdf0f90aca67eee86e27a3b7d329b` |

## Motivation and acceptance criteria

The user requested completion of the documentation on the new repository state
and resolution of PR #383's merge conflicts. The earlier October documentation
head had completed its observed workflows successfully, but master advanced
with source, configuration, testing, toolchain, and evidence changes. Those
old-head results do not validate the new merge result.

The final documentation must preserve current master source and generated
contracts, explain the current behavior to newcomers, keep complete English
and German companions, and resolve the Git conflict without force-pushing or
merging the PR into master. Removed connector body-limit settings must not be
restored as compatibility options. Current active-test selection and closed
specialist-campaign boundaries must remain explicit.

## Implementation and conflict decisions

The proposed merge tree starts from the exact current master tree. It retains
all current product source, tests, workflows, version pins, gitlinks, generated
references, and new technical/evidence documents. It then reapplies reviewed
reader-facing documentation changes.

Where master had advanced technical documentation, the current master content
is retained rather than replaced by an older whole file. Stable prior
orientation additions remain where the underlying master document did not
change. Root READMEs, the documentation index, getting-started guide,
configuration guide, and examples index are rewritten against the current
contracts. A new migration guide explains the removed settings, unchanged
host/transport controls, active testing, version pins, and generated-file
ownership.

This deliberately replaces the old blanket file-count description of the PR.
The final GitHub diff, not a historical count, defines its actual scope.
Conflict resolution preserves newer detailed guides and generated outputs even
when this removes an obsolete PR-only introductory edit to that file.

## Current behavior documented

Request and response inspection limits/actions belong to libModSecurity.
Removed Common/native/host-service cumulative connector settings fail
configuration; they are not silently accepted aliases. Request no-files limits,
access/MIME settings, native intervention results, and independent
host/transport capacity are distinguished. Phase-4 modes govern supported late
handling, not byte budgets. The shared source default is `off` as defined in
`common/include/msconnector/options.h`.

Normal functional selection uses `config/testing/active-cases.json` with its
core ceiling and separately authorized guarded offline Python exception.
`make check-active-inventory` admits the complete selection without execution;
`make quick-check` includes static checks and admitted functional subsets.
Specialist execution requires its separate current authorization and
`ON_DEMAND_TESTS=1`; this documentation task does not reopen I12 work.

The provenance-only purpose of `licenses/` is retained. Original upstream
LICENSE/AUTHORS/CHANGES material is not rewritten, and no repository-wide
license is declared.

## Changed documentation

New or fully revised entry points in this reconciliation:

- `README.md` / `README.de.md`
- `docs/README.md` / `docs/README.de.md`
- `docs/getting-started.md` / `docs/getting-started.de.md`
- `docs/configuration.md` / `docs/configuration.de.md`
- `docs/migration.md` / `docs/migration.de.md`
- `examples/README.md` / `examples/README.de.md`
- This English/German Change Record pair.

The final PR also retains compatible prior changes to security/origin
explanations, architecture, operations, traceability, decisions, selected
connector-guide introductions, glossary/profile references, and the historical
`CR-20260921-root-readme-refresh` record. That earlier record documents the
previous preparation stages; its old current-state descriptions and file counts
are not a claim about the final reconciled tree.

## Validation actually performed

Repository files, current master and PR metadata, selected source definitions,
and old-head workflow results were read through the GitHub connector. Tree and
blob identities were used to distinguish unchanged technical files from files
that advanced on master. Configuration migration statements were checked against
`docs/phase4-mode-budget.md` and the shared option definition.

No repository-native local shell validation is claimed: this environment did
not obtain a complete local checkout. Hosted validation of the final head is
separate from the old-head successes and must be read from that head's checks.
The PR description records the observed final-head result after publication;
it must not promote pending, skipped, or prerequisite-blocked work to a pass.

## Security and compatibility impact

This change adds no runtime behavior, defaults, permissions, network exposure,
credentials, dependency selection, or test bypass relative to reconciled master.
The master synchronization imports existing reviewed master changes rather
than inventing new source changes in a documentation PR.

The migration guide documents breaking configuration removals already present
in source. It does not authorize arbitrary engine-limit defaults or removal of
real host authorization ceilings. Examples remain operator-adapted references,
not secure deployment manifests.

## Runtime evidence and checks not run

No new host runtime campaign, I12 capture, CRS assessment, protocol matrix,
sanitizer run, or production qualification was performed by the documentation
editing step. No local full `make test`, `make quick-check`, generated-output
regeneration, or all-repository link validation is claimed before hosted checks.
Generated files remain the current master outputs and their normal CI contracts
are not weakened.

## Final review and remaining boundary

The intended delivery is a two-parent merge commit on the existing documentation
branch, preserving the old PR history and including the verified master revision.
No force-push, PR merge, or branch deletion is authorized by this record.

Review the final diff and final-head CI. Runtime claims remain tied to their
actual profile, revision, rules, run ID, and artifacts; a green documentation
change is not production or all-protocol certification.
