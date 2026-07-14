# Change Record: Reconcile the Common design note with current product routes

**Language:** English | [Deutsch](CR-20260714-common-design-note.de.md)

## Identity

| Field | Value |
| --- | --- |
| Title | Reconcile the Common design note with current product routes |
| Change ID | CR-20260714-common-design-note |
| Date (UTC) | 2026-07-14T10:29:29Z |
| Author or executing agent | Codex |
| Base revision | db3f1747bddd2d36470f61c9b04029876f864667 |
| Related issue or pull request | None |
| Final revision | not committed |

## Motivation and problem statement

The `Common design note` row in `docs/repository-concept.md` recorded a
medium-priority Parent-only deviation: `common/docs/design.md` was marked
`scaffolded` and retained historical sidecar/open-connector material that could
contradict current selected native routes. In particular, the historical
lighttpd `integration_mode=sidecar_proxy` description conflicted with the
current `patched-native-lighttpd` route. This change makes the paired Common
design notes an accurate, bounded guide to the current Common ownership
boundary and explicitly routes current architecture claims to the binding
product documentation.

## Affected components and security boundaries

The scope is the Parent repository's `common/docs/` architecture note, its
documentation contract test, and affected bilingual documentation and
Change-Record indexes. The boundary is that `common/` remains host-neutral:
host SDK objects, hooks, filters, host lifetimes, and client-visible actions
remain in `connectors/<name>/`; reusable test cases, runners, normalizers, and
schemas remain in the Framework. No Framework files, generated reports,
runtime artifacts, connector source, or configuration changed.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| The paired Common design notes state the current host-neutral boundary and link to the binding architecture and repository concept. | met | `tests.test_bilingual_docs` and `make check-bilingual-docs` |
| Historical routes cannot be presented as selected current routes; explicitly labeled historical or compatibility material remains distinguishable. | met | Focused positive, rejection, and boundary test cases |
| The documented `Common design note` deviation is updated only after its focused and required checks pass. | met | Updated `docs/repository-concept.md` and successful focused checks |
| English and German documentation, links, and whitespace checks pass. | met | Documentation checks and `git diff --check` |
| No runtime, production-readiness, or Framework claim is added. | met | Manual final review and no runtime evidence |

## Alternatives investigated

The capability-integration-mode deviation was not selected because it spans
four connector manifests and generator behavior. Runtime-report provenance,
generated-report freshness, the test boundary, and generator ownership require
Parent-and-Framework work or fresh runtime artifacts. Connector self-sufficiency
requires a connector-by-connector build, packaging, and installation audit.
Creating an ADR was not selected because no current decision authority was
provided to accept a retrospective durable decision. Rewriting or moving
historical runtime material without a current-boundary contract would leave the
same ambiguity.

## Implementation decision and rationale

The scaffolded note was replaced by a concise bilingual current-boundary note:
Common's C-first, bounded-data, ownership, and evidence limits; the selected
six connector routes; and links to the binding product concept, architecture,
and testing/evidence documentation. A focused Parent documentation contract is
now part of the existing `check-bilingual-docs` gate, so it also runs through
`make lint` and `make quick-check`. It rejects a scaffolded status, an
incorrect selected route, or an unqualified historical integration mode, while
allowing an explicitly marked historical or `compatibility_only` reference.
This is a documentation/contract correction, not a runtime or product-code
change.

## Changed files

- `ci/checks/documentation/check-bilingual-docs.py`
- `tests/test_bilingual_docs.py`
- `common/docs/design.md`
- `common/docs/design.de.md`
- `common/README.md`
- `common/README.de.md`
- `docs/repository-concept.md`
- `docs/repository-concept.de.md`
- `reports/audits/change-records/CR-20260714-common-design-note.md`
- `reports/audits/change-records/CR-20260714-common-design-note.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

No local, unversioned configuration was intentionally changed. Separate
Apache and `Makefile` work appeared after the initial clean status check; it
was not modified or included in this change.

## Tests added or changed

`tests/test_bilingual_docs.py` adds three cases for the Common design note:
a positive current-document case, a rejection case for `scaffolded`, an
incorrect selected lighttpd route, and an unqualified
`integration_mode=sidecar_proxy`, and a boundary case that accepts an
explicitly historical `compatibility_only` reference.

## Commands executed

| Exact command | Exit code or result | Sanitized relevant summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v tests.test_bilingual_docs` | `1`, then `0` | The first focused run exposed a whitespace-normalization error in the new required-content check; after the correction, all 9 tests passed. | None | None |
| `make check-bilingual-docs` | `0` | Bilingual documentation, including the new Common note contract and Change Record pair, passed. | None | None |
| `make check-doc-links` | `0` | Parent repository references and Framework documentation links passed. | None | None |
| `make check-variable-documentation` | `0` | 85 documented variable references scanned successfully. | None | None |
| `make check-common-sdk-contract` | `0` | Common host-SDK boundary contract passed. | None | None |
| `make check-common-security-contract` | `0` | Common security/data-flow contract passed. | None | None |
| `make check-common-flow-integrity` | `0` | Common flow/ownership integrity contract passed. | None | None |
| `make quick-check` | `blocked_by_resource_limit` | The run entered external runtime-component preparation and compilation. It was interrupted with `SIGINT` after the largest measured temporary-root snapshot reached `1744452` KiB; the detached command wrapper did not surface an exit code. | None | None |
| `git diff --check` | `0` | No whitespace errors in the tracked worktree diff. | None | None |
| `git status --short` | `0` | Scope review completed; separate Apache and `Makefile` changes remain unmodified. | None | None |

## Security impact

No runtime security behavior, default, input limit, logging format, or trust
relationship changed. The corrected note reduces the risk that maintainers
mistake a historical sidecar route for a current selected route and thereby
misapply ownership or evidence claims. The Common security and flow-integrity
contracts remain passing.

## Documentation changes

The paired Common design note now records the current boundary and selected
routes; the paired Common README indexes it. The paired repository concept
marks only this deviation as addressed. The paired Change Record and index
record the change. `docs/architecture.md` and `.de.md`, connector guides, and
runtime documentation were reviewed but required no change because their
current route descriptions were already authoritative.

## Runtime evidence

No runtime evidence was collected or claimed for this change. Documentation,
source, and contract checks do not establish host traffic or runtime behavior.

## Known limitations

This change does not reconcile capability manifests, refresh generated reports,
create canonical runtime evidence, alter compatibility implementations, or
audit connector packaging and installation. The Common route table is a
documentation contract, not a capability or runtime result.

## Remaining risks

Future selected-route changes must update the binding concept, connector guide,
and Common note together when applicable. The interrupted `make quick-check`
does not provide a full lint result; the smaller relevant checks above passed.

## Checks not run and rationale

`make lint` was not rerun independently because `make quick-check` includes it
and the observed runtime-component compilation exceeded the 1536 MiB temporary
storage warning threshold. Runtime, smoke, lifecycle, and connector build runs
were not run because this change does not change runtime or build behavior and
must not manufacture runtime evidence.

## Final diff and review status

The scoped final review found only the listed Common documentation, contract,
test, concept, and Change-Record updates. `git diff --check` passed. The
Framework submodule diff and status were empty. The worktree also contains
separate Apache cleanup and `Makefile` changes that appeared after the initial
clean status check; they were preserved and excluded from this Change Record.
The record matches the scoped implementation and actual outcomes. Intended
commit subject: `Align Common design note with selected product routes`.
