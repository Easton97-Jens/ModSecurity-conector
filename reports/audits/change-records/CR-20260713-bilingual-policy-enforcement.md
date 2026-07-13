# Change Record: Bilingual policy enforcement

**Language:** English | [Deutsch](CR-20260713-bilingual-policy-enforcement.de.md)

## Identity

| Field | Value |
| --- | --- |
| Title | Bilingual policy enforcement |
| Change ID | CR-20260713-bilingual-policy-enforcement |
| Date (UTC) | 2026-07-13T19:40:08Z |
| Author or executing agent | Codex agent <code>/root</code> |
| Base revision | 056f93232c6f5dba132bfb2204d96ce49707507b |
| Related issue or pull request | None |
| Final revision | Not committed |

## Motivation and problem statement

Make English/German parity a durable, enforceable repository rule rather than a
best-effort documentation convention. The work also removes stale versioned
links to local Codex instructions that cannot be present in a clean checkout.

## Affected components and security boundaries

The change affects reader-facing Markdown, the bilingual documentation checker,
the repository link checker, pull-request guidance, and local Codex workflow
instructions. It does not change connector runtime behavior. Documentation and
Change Records continue to exclude secrets, tokens, cookies, bodies, private
environment values, raw runtime data, builds, and caches.

Independent, concurrently edited Change-Record governance artifacts under
<code>reports/audits/change-records/</code> were preserved. This record covers
the enforcement and language-pair work in this change.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Relevant root-owned reader-facing Markdown has an English/German companion | Met | <code>make check-bilingual-docs</code> passes with the expanded scope. |
| Local Codex configuration remains unpaired while requiring bilingual versioned content | Met | Local workflow files exist; the checker rejects forbidden local German companions. |
| The PR template contains all required English and German sections | Met | Checker unit test and <code>make check-bilingual-docs</code> pass. |
| Required link, whitespace, and status checks have actual recorded outcomes | Met | Focused final commands in this record passed. |

## Alternatives investigated

- Keep the former checker exemptions for connector <code>ORIGIN.md</code> and
  <code>TODO.md</code>. Rejected because they are versioned human-readable
  content covered by the bilingual policy.
- Create <code>AGENTS.de.md</code> or <code>RTK.de.md</code> to repair stale
  links. Rejected because local Codex/RTK configuration must remain unpaired.
- Limit enforcement to language switches. Rejected because the new checker also
  needs scope, structural, Change-Record, and pull-request field checks.

## Implementation decision and rationale

Add a versioned policy pair, strengthen local workflow instructions, complete
the existing connector and license Markdown pairs, and make the checker enforce
those pair rules. Add focused unit tests for the new checker behavior. Replace
versioned links to local <code>AGENTS.md</code> with the versioned policy so a
clean checkout can validate links.

## Changed files

Versioned files in scope include:

- <code>docs/change-traceability.md</code> and
  <code>docs/change-traceability.de.md</code>
- <code>README.md</code>, <code>README.de.md</code>,
  <code>docs/reference/variables.md</code>, and
  <code>docs/reference/variables.de.md</code>
- <code>.github/pull_request_template.md</code>
- <code>ci/checks/documentation/check-bilingual-docs.py</code>,
  <code>ci/checks/documentation/check-repository-path-references.py</code>,
  and <code>tests/test_bilingual_docs.py</code>
- English/German <code>TODO.md</code> pairs under
  <code>connectors/_template/</code> and each selected connector
- English/German <code>ORIGIN.md</code> pairs for the selected connectors
- English/German license and provenance pairs under <code>licenses/</code>
- this English/German Change-Record pair

Intentional local, unversioned files are <code>AGENTS.md</code>,
<code>.codex/context/conventions.md</code>,
<code>.codex/context/definition-of-done.md</code>,
<code>.codex/context/task-workflow.md</code>, and
<code>.codex/context/security-workflow.md</code>.

## Tests added or changed

Added <code>tests/test_bilingual_docs.py</code>. It exercises structural and
fenced-code-block parity for <code>docs/</code>, license scope, forbidden local
companions, required pull-request fields, and matching technical Change-Record
identity values.

## Commands executed

| Exact command | Exit code or result | Sanitized relevant summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| <code>rtk .venv/bin/python -m unittest -v tests.test_bilingual_docs</code> | 0 | Six focused bilingual-checker tests passed. | None | None |
| <code>rtk make check-bilingual-docs</code> | 0 | Expanded pair, structure, Change-Record, pull-request, and local-companion checks reported <code>bilingual docs ok</code>. | None | None |
| <code>rtk make check-doc-links</code> | 0 | Repository path references and Framework document links passed. | None | None |
| <code>rtk git diff --check</code> | 0 | No whitespace diagnostics for tracked changes. | None | None |
| <code>rtk git status --short</code> | 0 | Final status listed the scoped versioned changes and no local German Codex/RTK companions. | None | None |

## Security impact

No connector runtime security behavior changes. The new workflow requires both
languages to document security boundaries, attack preconditions, impact, cause,
correction, regression evidence, and residual risk without sensitive data. The
checker reduces the chance that required security documentation is silently
missing a companion.

## Documentation changes

Added the versioned policy pair and local bilingual workflow guidance. Completed
English/German pairs for connector planning, provenance, and license material.
Updated user-facing pull-request guidance and versioned policy links. Added
English/German Change-Record entries for this non-trivial change.

## Runtime evidence

No runtime evidence was collected or claimed. This documentation and governance
change makes no connector runtime claim.

## Known limitations

- Semantic translation quality still needs author and reviewer judgment; an
  automated checker can verify structure and selected technical facts, not all
  meaning.
- Generated reports may require generator-specific validation in addition to
  the general bilingual checker.
- Local Codex instructions are intentionally unversioned; the versioned policy
  remains the durable repository contract.

## Remaining risks

A future document can still become semantically stale if a review misses a
translation divergence. Required language pairs, structure checks, Change
Records, PR fields, and explicit final checks reduce but do not eliminate that
risk.

## Checks not run and rationale

- <code>make quick-check</code> and <code>make lint</code> were not run because
  the requested focused documentation, link, diff, and status checks cover this
  documentation/governance change.
- Connector builds, configuration checks, lifecycle runs, and runtime tests
  were not run because no runtime behavior changed and those commands can create
  external build or evidence artifacts.

## Final diff and review status

The scoped final diff and both language forms were reviewed. The focused unit,
bilingual-documentation, link, and whitespace checks passed. No commit or pull
request was created. This record is reconciled with the actual final diff and
test outcomes and was rechecked after this record update.
