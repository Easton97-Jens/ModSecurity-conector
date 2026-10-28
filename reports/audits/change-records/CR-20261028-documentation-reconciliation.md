# Current documentation and conflict reconciliation

**Language:** English | [Deutsch](CR-20261028-documentation-reconciliation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261028-documentation-reconciliation` |
| Date (UTC) | 2026-10-28 |
| Base revision | `ab01cc60e638f03915fc0cc4f1541d91f9c6a62e` |
| Reconciled master | `15cea9e4d778fa1ec6e27e6fe084b347010f1367` |
| Previous common base | `820b6975495bdf0f90aca67eee86e27a3b7d329b` |
| Pull request | #383 |
| Branch | `docs-refresh-root-readmes` |
| Reconciliation merge | `34dffc40f31cdb870e64283ebaee32b8cdd44bca` |

## Motivation and problem statement

The user requested completion of the documentation on the new repository state
and resolution of PR #383's merge conflicts. The earlier documentation head had
completed its observed workflows successfully, but master advanced with source,
configuration, testing, toolchain, and evidence changes. Old-head results do
not validate the new merge result.

Earlier transitional text treated connector response limits as compatibility
or capacity values. Current source instead removes cumulative request and
response connector settings. Standard testing also moved to the active
inventory and its separately authorized offline exception. Entry-level guides
must explain those changes without restoring old behavior or overstating scope.

## Acceptance criteria

Preserve current master source, generated contracts, and new technical/evidence
documents. Explain setup, profile choice, configuration migration, and test
selection clearly in equivalent English/German companions. Retain the ten
logical solutions and their compatibility/companion boundaries. Resolve Git
conflicts without force-pushing, deleting the branch, or merging the PR into
master. Do not weaken checkers or reintroduce removed configuration settings.

## Implementation decision and rationale

The merge tree starts from the exact current master tree, retaining current
product source, tests, workflows, pins, gitlinks, generated references, and
newer detail documents. Compatible reader-orientation additions remain where
the underlying master file did not change. Where technical documentation
advanced, current master details take precedence over obsolete whole-file
replacements from the earlier PR.

Root READMEs, the documentation index, getting-started guide, configuration
guide, and examples index are rewritten against current contracts. The new
migration guide distinguishes engine inspection limits from real host and
transport capacity, explains rejected removed options, identifies the shared
Phase-4 source default `off`, and documents active testing and specialist
opt-in without reopening I12 work.

The provenance-only purpose of `licenses/` remains: upstream origin, recorded
revision/license basis, retained notices, and local differences. Original
upstream LICENSE/AUTHORS/CHANGES files are not rewritten, and no repository-wide
license is declared.

The final diff supersedes the old blanket count of 86 files. The historical
`CR-20260921-root-readme-refresh` record documents earlier preparation stages,
not the current reconciled file count, transitional settings, or validation.

## Changed files

The reconciled PR diff against the selected master contains these documents:

- `README.md` / `README.de.md`
- `SECURITY.md` / `SECURITY.de.md`
- `docs/README.md` / `docs/README.de.md`
- `docs/architecture.md` / `docs/architecture.de.md`
- `docs/change-traceability.md` / `docs/change-traceability.de.md`
- `docs/configuration.md` / `docs/configuration.de.md`
- `docs/connectors/apache.md` / `docs/connectors/apache.de.md`
- `docs/connectors/envoy.md` / `docs/connectors/envoy.de.md`
- `docs/connectors/traefik.md` / `docs/connectors/traefik.de.md`
- `docs/decisions/ADR-003-shared-p1-p4-lifecycle-semantics.md` / `docs/decisions/ADR-003-shared-p1-p4-lifecycle-semantics.de.md`
- `docs/decisions/README.md` / `docs/decisions/README.de.md`
- `docs/getting-started.md` / `docs/getting-started.de.md`
- `docs/migration.md` / `docs/migration.de.md`
- `docs/operations-and-security.md` / `docs/operations-and-security.de.md`
- `docs/reference/glossary.md` / `docs/reference/glossary.de.md`
- `docs/reference/with-crs-no-mrts-profile-contract.md` / `docs/reference/with-crs-no-mrts-profile-contract.de.md`
- `examples/README.md` / `examples/README.de.md`
- `licenses/README.md` / `licenses/README.de.md`
- `licenses/apache/ORIGIN.md` / `licenses/apache/ORIGIN.de.md`
- `licenses/modsecurity/README.md` / `licenses/modsecurity/README.de.md`
- `licenses/nginx/ORIGIN.md` / `licenses/nginx/ORIGIN.de.md`
- `reports/audits/change-records/CR-20260921-root-readme-refresh.md` / `reports/audits/change-records/CR-20260921-root-readme-refresh.de.md`
- `reports/audits/change-records/CR-20261028-documentation-reconciliation.md` / `reports/audits/change-records/CR-20261028-documentation-reconciliation.de.md`

## Commands executed

Repository files, current master/PR metadata, source definitions, and workflow
results were read through the GitHub connector. Git tree/blob identities
separated unchanged technical files from master changes. Removed-option and
engine-ownership statements were checked against `docs/phase4-mode-budget.md`;
the shared default was checked in `common/include/msconnector/options.h`.

The branch was advanced by a non-forced, expected-head-checked ref update to
the two-parent reconciliation merge. GitHub comparison confirmed master as
merge base, zero commits behind, and a Markdown-only diff. GitHub then reported
the PR as mergeable.

Hosted lint for reconciliation head
`34dffc40f31cdb870e64283ebaee32b8cdd44bca` ran
`python ci/checks/documentation/check-bilingual-docs.py` and reported missing
canonical Change Record section/identity labels in this new record. The
successor corrects those labels and separates the required sections without
changing the checker. The same observed lint job reported current generated
configuration outputs and a passing configuration-reference semantics check.
Those are results for that reconciliation head, not a pre-claimed pass for the
successor. No repository-native local test command is claimed.

## Security impact

Relative to reconciled master, only documentation changes. No runtime behavior,
default, permission, network exposure, credential flow, dependency selection,
workflow, test bypass, or retention behavior is added. Master synchronization
imports existing reviewed master work rather than creating source changes in
a documentation PR.

The migration text documents removals already present in source; it does not
authorize arbitrary engine defaults or removal of real authorization-host
ceilings. Examples remain operator-adapted references, not secure deployment
manifests. No credentials or sensitive traffic artifacts are added.

## Runtime evidence

No new host runtime campaign, I12 capture, CRS assessment, protocol matrix, or
production qualification was performed by the documentation editing step.
Existing reports remain tied to their recorded profile, revision, rules, run
ID, and artifacts. Old successful workflows are not final-head runtime proof.

## Known limitations

A complete local repository checkout was not available in this editing
environment. Full repository validation therefore depends on the hosted checks
for the published head. Generated compiler/configuration references remain
current master outputs; no local regeneration is claimed.

Technical references intentionally retain their depth. The new guides are a
navigation and migration layer, not a replacement for host-specific syntax,
actual prerequisites, source contracts, or deployment review.

## Remaining risks

Future source, host, test inventory, or pin changes can reintroduce drift.
Review current source and the final-head checks rather than relying on a fixed
README date, historical file count, or the success of an earlier commit.
Unsupported strict actions and incomplete authorization samples must remain
visible limitations rather than being presented as general runtime support.

## Checks not run and rationale

Local full `make test`, `make quick-check`, `make check-bilingual-docs`,
`make check-doc-links`, `git diff --check`, generated-output regeneration,
all-host campaigns, sanitizers, and protocol matrices were not run because no
complete local checkout/toolchain was established. No validation result is
fabricated from remote source inspection.

The final head's hosted results must be recorded after completion in the PR
validation summary. Pending, skipped, or prerequisite-blocked work is not a
pass. No I12 campaign or extra on-demand suite is authorized by this record.

## Final diff and review status

Reconciliation uses a two-parent merge on the existing documentation branch,
retains the prior PR history, and includes the exact verified master revision.
No force-push, PR merge, or branch deletion was performed. The observed
Change Record format error is repaired in a normal successor commit.

Review the final diff and final-head CI before readiness. A successful
documentation change is not production or all-protocol certification.
