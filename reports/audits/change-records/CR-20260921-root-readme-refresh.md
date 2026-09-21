# Root README refresh

**Language:** English | [Deutsch](CR-20260921-root-readme-refresh.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260921-root-readme-refresh` |
| Date (UTC) | 2026-09-21 |
| Base revision | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |

## Motivation and problem statement

The root README pair had accumulated correct but highly evidence-internal
language and no longer provided a concise project overview for new readers. It
also described only the six selected host-family routes even though the
canonical connector documentation distinguishes ten logical profiles, and it
did not surface the current Phase-4 `off` / `safe` / `strict` contract as a
first-class entry point.

The user requested a complete refresh of `README.md` and `README.de.md` against
the current repository state.

## Acceptance criteria

The English and German root READMEs must remain structurally equivalent, explain
the six host families and ten logical profiles, describe the current Phase-4
mode boundary without widening runtime claims, provide a usable quick start and
common target map, point to the canonical detailed documentation, preserve the
Parent/Framework ownership boundary, and retain explicit evidence/security
limitations.

No connector behavior, build target, configuration default, workflow,
dependency, submodule pointer, or runtime/evidence result may be changed or
promoted by this documentation-only change.

## Implementation decision and rationale

The root README pair is rewritten as an onboarding and navigation layer rather
than duplicating every detailed connector guide. Stable facts are stated
directly; volatile details such as exact Python/Go patch versions are linked to
their checked-in source files instead of being copied into prose.

The README now distinguishes host-family core routes from logical profiles,
adds the shared P1-P4 phase model and the current Phase-4 budget modes, keeps
run/evidence boundaries explicit, and groups repository layout, quick start,
common workflows, configuration, security, development rules, documentation,
and provenance into dedicated sections.

## Changed files

- `README.md`
- `README.de.md`
- `reports/audits/change-records/CR-20260921-root-readme-refresh.md`
- `reports/audits/change-records/CR-20260921-root-readme-refresh.de.md`

## Commands executed

No repository-native shell command was executed because this change was
prepared through the GitHub connector without a local repository checkout.
Repository state, current documentation contracts, target names, current
Phase-4 semantics, toolchain source files, and the current `master` revision
were read from GitHub before editing.

## Security impact

Documentation only. No source, runtime behavior, validation rule, default,
credential flow, permission, workflow, dependency, network exposure, logging
path, or evidence-retention behavior is modified. The new README strengthens
the existing warning not to place secrets or sensitive traffic data in run
identifiers, command lines, checked-in configuration, logs, or review evidence.

## Runtime evidence

No runtime evidence was collected or claimed. No host, protocol, CRS,
production-readiness, strict-intervention, or deployment result is inferred
from this documentation change.

## Known limitations

The root README intentionally summarizes the repository. Connector-specific
syntax, compatibility routes, capability state, host prerequisites, protocol
limits, and current run results remain authoritative in the linked connector,
configuration, build, testing/evidence, operations/security, and report
documents.

## Remaining risks

The main residual risk is future documentation drift if root navigation is not
updated when target names, profile identities, or policy contracts change.
Repository documentation/link checks and review of the exact PR head remain the
appropriate controls.

## Checks not run and rationale

`make check-bilingual-docs`, `make check-doc-links`, `git diff --check`, and
`git status --short` were not run because the GitHub connector does not provide
a local shell checkout. Hosted checks, if triggered by the Draft PR, are
separate exact-head evidence and are not pre-claimed here.

No build, configuration load, unit/integration test, host runtime, CRS run,
sanitizer, SonarQube check, or protocol matrix was run because the change is
documentation-only and no such result is needed to describe a runtime change
that does not exist.

## Final diff and review status

The scoped change is limited to the English/German root README pair and this
required English/German Change Record pair. The content was reconciled against
current `master` documentation and the current Phase-4 contract before branch
publication. No merge, production approval, hosted-check success, or runtime
verification is asserted.
