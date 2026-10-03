# Documentation and examples usability refresh

**Language:** English | [Deutsch](CR-20260921-root-readme-refresh.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260921-root-readme-refresh` |
| Date (UTC) | 2026-09-21 |
| Base revision | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |

## Motivation and problem statement

The user requested a complete refresh of the English/German root READMEs and
then expanded the request to the project documentation and the checked-in
`examples/` tree so the repository is easier to understand for new users and
remains aligned with the current implementation.

The existing material was technically detailed but often started at an
evidence-, policy-, or implementation-internal level. Important distinctions
such as six host families versus ten logical profiles, configuration layers,
Phase-4 `off` / `safe` / `strict`, example selection, and the difference
between static/build/config checks and runtime evidence were not consistently
introduced before detailed reference material.

The user additionally requested that the `licenses/` area be reduced to a
clear provenance function: explain where external material comes from, which
upstream revision/license information forms the documented basis, and how the
local repository differs from those upstream sources. The license reference
area must not read as a repository-wide license declaration.

## Acceptance criteria

The documentation must provide a clear path from root README to getting
started, examples, connector selection, configuration, build, testing/evidence,
and safe operation. English and German companions must remain structurally and
factually equivalent. All six host families and ten logical solutions must be
discoverable from the examples and connector guides.

The refresh must preserve current source-of-truth boundaries and must not
change connector runtime behavior, configuration defaults, build targets,
workflows, dependencies, submodule pointers, generated-reference contracts, or
runtime/evidence results. Technical reference depth must be retained rather
than replaced by simplified but incomplete prose.

## Implementation decision and rationale

The documentation is organized as two layers. Reader-facing entry pages and
host guides now begin with concise task-oriented orientation. Detailed
source-backed reference sections remain intact behind those entry points.

The root README, documentation index, getting-started guide, examples index,
core conceptual guides, connector index and six connector guides, and all six
host example guides now explain what to read first, which profile to choose,
what each validation layer proves, and where configuration/security boundaries
live. Source-tree READMEs for Common, connectors, config, reports, and SECURITY
now point users to the appropriate reader-facing material before code-adjacent
detail.

The first PR head also exposed a real bilingual-check failure caused by the
English quick-start command using `cd ModSecurity-connector` while the
repository directory is `ModSecurity-conector`. This refresh corrects the
English command so the EN/DE fenced command content is identical.

The `licenses/` documentation is simplified to origin/reference information.
Apache and NGINX record their upstream base revision and retained upstream
license/attribution files while explicitly stating that the local connector
trees contain repository-local and additional upstream-derived changes.
ModSecurity v2/v3 are documented only as external engine references. The root
README now states that these upstream references do not define a repository-wide
license and that no top-level `LICENSE` file exists at this revision.

## Changed files

- `README.de.md`
- `README.md`
- `SECURITY.de.md`
- `SECURITY.md`
- `common/README.de.md`
- `common/README.md`
- `config/README.de.md`
- `config/README.md`
- `connectors/README.de.md`
- `connectors/README.md`
- `docs/README.de.md`
- `docs/README.md`
- `docs/architecture.de.md`
- `docs/architecture.md`
- `docs/build/README.de.md`
- `docs/build/README.md`
- `docs/build/compilers/README.de.md`
- `docs/build/compilers/README.md`
- `docs/build/compilers/apache.de.md`
- `docs/build/compilers/apache.md`
- `docs/build/compilers/envoy.de.md`
- `docs/build/compilers/envoy.md`
- `docs/build/compilers/haproxy.de.md`
- `docs/build/compilers/haproxy.md`
- `docs/build/compilers/libmodsecurity.de.md`
- `docs/build/compilers/libmodsecurity.md`
- `docs/build/compilers/lighttpd.de.md`
- `docs/build/compilers/lighttpd.md`
- `docs/build/compilers/nginx.de.md`
- `docs/build/compilers/nginx.md`
- `docs/build/compilers/overview.de.md`
- `docs/build/compilers/overview.md`
- `docs/build/compilers/traefik.de.md`
- `docs/build/compilers/traefik.md`
- `docs/change-traceability.de.md`
- `docs/change-traceability.md`
- `docs/configuration.de.md`
- `docs/configuration.md`
- `docs/connectors/README.de.md`
- `docs/connectors/README.md`
- `docs/connectors/apache.de.md`
- `docs/connectors/apache.md`
- `docs/connectors/envoy.de.md`
- `docs/connectors/envoy.md`
- `docs/connectors/haproxy.de.md`
- `docs/connectors/haproxy.md`
- `docs/connectors/lighttpd.de.md`
- `docs/connectors/lighttpd.md`
- `docs/connectors/nginx.de.md`
- `docs/connectors/nginx.md`
- `docs/connectors/runtime-failure-policy.de.md`
- `docs/connectors/runtime-failure-policy.md`
- `docs/connectors/traefik.de.md`
- `docs/connectors/traefik.md`
- `docs/decisions/ADR-003-shared-p1-p4-lifecycle-semantics.de.md`
- `docs/decisions/ADR-003-shared-p1-p4-lifecycle-semantics.md`
- `docs/decisions/README.de.md`
- `docs/decisions/README.md`
- `docs/getting-started.de.md`
- `docs/getting-started.md`
- `docs/operations-and-security.de.md`
- `docs/operations-and-security.md`
- `docs/phase4-mode-budget.de.md`
- `docs/phase4-mode-budget.md`
- `docs/reference/glossary.de.md`
- `docs/reference/glossary.md`
- `docs/reference/variables.de.md`
- `docs/reference/variables.md`
- `docs/reference/with-crs-no-mrts-profile-contract.de.md`
- `docs/reference/with-crs-no-mrts-profile-contract.md`
- `docs/repository-concept.de.md`
- `docs/repository-concept.md`
- `docs/security/ci-security-tooling.de.md`
- `docs/security/ci-security-tooling.md`
- `docs/security/trusted-nginx-root-broker.de.md`
- `docs/security/trusted-nginx-root-broker.md`
- `docs/testing-and-evidence.de.md`
- `docs/testing-and-evidence.md`
- `examples/README.de.md`
- `examples/README.md`
- `examples/apache/README.de.md`
- `examples/apache/README.md`
- `examples/common/README.de.md`
- `examples/common/README.md`
- `examples/common/common-connector-configuration.de.md`
- `examples/common/common-connector-configuration.md`
- `examples/common/modsecurity-directives.de.md`
- `examples/common/modsecurity-directives.md`
- `examples/common/rule-examples.de.md`
- `examples/common/rule-examples.md`
- `examples/envoy/README.de.md`
- `examples/envoy/README.md`
- `examples/haproxy/README.de.md`
- `examples/haproxy/README.md`
- `examples/lighttpd/README.de.md`
- `examples/lighttpd/README.md`
- `examples/nginx/README.de.md`
- `examples/nginx/README.md`
- `examples/traefik/README.de.md`
- `examples/traefik/README.md`
- `licenses/README.de.md`
- `licenses/README.md`
- `licenses/apache/ORIGIN.de.md`
- `licenses/apache/ORIGIN.md`
- `licenses/modsecurity/README.de.md`
- `licenses/modsecurity/README.md`
- `licenses/nginx/ORIGIN.de.md`
- `licenses/nginx/ORIGIN.md`
- `reports/README.de.md`
- `reports/README.md`
- `reports/audits/change-records/CR-20260921-root-readme-refresh.de.md`
- `reports/audits/change-records/CR-20260921-root-readme-refresh.md`

## Commands executed

No repository-native local shell command was executed because the change was
prepared through the GitHub connector without a local checkout.

For the first PR head `8e0086b2d194828144d303d8a887cfb285e00ec6`,
GitHub Actions reported successful CodeQL, OpenSSF Scorecard, Secret scanning,
Security workflow lint, protocol-contract, Envoy, HAProxy, lighttpd, trusted
NGINX exact-head, and report-governance workflows. The lint,
quick-framework-check, test-common, test-apache, and test-nginx workflows
failed at the shared bilingual documentation check with the specific message
`README.md: fenced code-block content differs from README.de.md`. Inspection
identified the English directory-name typo described above. These are results
for that prior head only; they are not current-head results for the expanded
documentation commit.

For the second documentation head `bb98e75da5bd472215a6194462e24fa7356da4b4`,
the root fenced-command mismatch was no longer the reported blocker. The shared
No-CRS documentation consistency check instead reported that the repository
overview pair was missing the required literals `minimal_runtime_smoke` and
`capabilities.json`. The successor documentation restores both concepts with
reader-facing explanations instead of weakening the checker. Those results are
also prior-head evidence only.

## Security impact

Documentation only. No product source, parser, runtime policy, default,
permission, workflow, dependency, network exposure, credential flow, or
evidence-retention behavior is changed.

The refreshed documentation makes existing security boundaries more explicit:
private listeners/UDS where appropriate, bounded resources, external
build/runtime/evidence paths, least-privilege filesystem/service ownership, and
the prohibition on putting credentials, cookies, authorization values, private
keys, sensitive bodies, or personal data into run IDs, versioned files, logs,
or review evidence.

## Runtime evidence

No new runtime evidence was collected or claimed. This documentation change
does not establish host, protocol, CRS, production-readiness,
strict-intervention, or deployment results.

## Known limitations

Generated documentation under `docs/generated/` remains intentionally untouched because repository policy requires changes through its generator/source contract. Compiler-specific deep references, decision records, and specialized CI/security contracts remain technical, but now begin with reader orientation or are reached through clearer task-oriented entry pages.

The examples remain configuration references, not production deployment
manifests. Host-specific installation paths, ports, module ABI, service
identity, TLS, rules files, sockets, permissions, and logging/retention still
require operator review.

The `licenses/` files record observed upstream origin/license information and
provenance boundaries. They are not a legal determination for every repository
file and do not replace file-level/source-map review.

## Remaining risks

Future source, target, profile, or policy changes can reintroduce documentation
drift if the reader-facing navigation is not updated with the owning technical
contract. Repository bilingual/link checks and review of exact-head CI remain
the primary controls.

## Checks not run and rationale

Local `make check-bilingual-docs`, `make check-doc-links`, `git diff
--check`, and `git status --short` were not run because this connector
workflow has no local checkout. Builds, host runtime tests, CRS runs,
sanitizers, and protocol matrices were not run because the change is
documentation-only.

Current-head hosted CI is not pre-claimed. It must evaluate the expanded
documentation commit, including the corrected root README fenced command.

## Final diff and review status

This work extends Draft PR #383 on branch `docs-refresh-root-readmes`. The
change remains documentation-only and does not authorize or perform a merge.
The prior-head CI failure was reviewed and its README command mismatch is
corrected in the prepared successor. Current-head checks and review remain
separate delivery evidence.
