# Change Record: Parent connector-config-reference literal deduplication for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260727-sonar-config-reference-literal-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-config-reference-literal-deduplication |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent SonarQube Cloud python:S1192 Code Smells: 69 current OPEN receipt keys in ci/checks/documentation/connector_config_reference.py. |
| Boundary | Parent configuration-reference generator/checker, this English/German Change Record pair, and their indexes. Generated configuration-reference files, connector or runtime behavior, Framework, MRTS, Gitlinks, workflows, SonarQube Cloud configuration, Quality Gates, suppressions, external issue state, push, pull request, and merge remain unchanged. |

## Motivation and problem statement

The current SonarQube Cloud receipt inventory reports 69 open python:S1192
findings in the Parent connector-configuration reference generator. Repeated
schema labels, source paths, explanatory text, and option identifiers make
the source harder to maintain while carrying no distinct behavior.

## Acceptance criteria

- Address exactly the 69 receipt-backed python:S1192 occurrences in
  connector_config_reference.py through semantically identical module-local
  constants.
- Preserve schema, option order, JSON or Markdown rendering, and every
  generated configuration-reference file.
- Pass the native configuration-reference generation/checker contract,
  receipt-level static audit, whitespace review, and repository
  documentation checks.
- Maintain an equivalent English/German Change Record pair and do not claim
  any SonarQube Cloud issue closed before a new exact candidate-head analysis.

## Implementation decision and rationale

Only repeated, byte-identical values are named once at module scope and used
at their existing call sites. The extraction, YAML handling, renderer order,
default values, diagnostics, and generator output contracts remain unchanged.
No generated document is edited directly.

## Changed files

- ci/checks/documentation/connector_config_reference.py
- reports/audits/change-records/CR-20260727-sonar-config-reference-literal-deduplication.md
- reports/audits/change-records/CR-20260727-sonar-config-reference-literal-deduplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Commands executed

- rtk proxy make check-connector-config-reference
- Receipt-backed AST literal audit for the 69 current python:S1192 keys
- rtk proxy git diff --check
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-doc-links

The isolated task worktree initializes the Parent-recorded Framework Gitlink
only as a documentation-check dependency. No Framework source, Parent
Gitlink, Framework branch, or Framework pull request changes.

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Configuration-reference generation/checker | passed: 21 generated files are current; the checker passed apache=14, nginx=18, haproxy=41, envoy=141, traefik=71, lighttpd=19, common=25, engine=12. |
| Receipt-backed AST literal audit | passed: receipt_issues=69 and all_literals_singleton. |
| git diff --check | passed: no whitespace error. |
| Direct source-diff review | passed: only byte-identical module-local constants and direct uses changed in the scoped generator. |
| make check-bilingual-docs | passed: bilingual docs ok. |
| make check-doc-links | passed: repository path references: PASS and doc links ok. |

## Security impact

The focused security assessment is not_applicable. This is an
output-equivalent configuration-documentation generator refactor; it changes
no runtime path validation, network, subprocess, connector, credential,
permission, or security control. No security finding is claimed fixed.

## Documentation status

The native configuration-reference check confirms that all 21 generated files
remain current. This paired Change Record documents the source-only
deduplication. The completed repository documentation checks report bilingual
docs ok, repository path references PASS, and doc links ok.

## Runtime evidence

No connector, host, protocol, or production runtime behavior changed or is
claimed. The generator/checker verification is source and documentation
evidence, not runtime evidence.

## Known limitations

SonarQube Cloud has not yet analyzed this candidate head. The 69 current
findings can disappear only after a fresh analysis of the exact delivered
commit.

## Remaining risks

A mistaken extraction could alter a rendered option or diagnostic. The native
generation/checker validates every tracked configuration-reference file, and
the source diff is limited to values backed by the current receipt.

## Checks not run and rationale

- Hosted SonarQube Cloud analysis and GitHub CI are not yet available for this
  uncommitted local candidate.
- Connector builds, host configuration checks, runtime smokes, protocol
  matrices, Framework checks, and MRTS checks are not applicable because no
  connector/runtime implementation or cross-repository source changed.
- No commit, push, pull request, or master merge has occurred at the time of
  this record; later delivery evidence will be recorded only from observed
  results.

## Final diff and review status

The task-worktree candidate contains only the configuration-reference literal
deduplication and its required bilingual traceability material. The
authoritative Parent checkout, Framework source, MRTS source, Parent Gitlink,
scanner controls, and external SonarQube Cloud issue states remain unchanged.
