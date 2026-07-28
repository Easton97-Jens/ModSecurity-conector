# Change Record: Parent compiler-guide literal deduplication for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260727-sonar-compiler-guides-literal-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-compiler-guides-literal-deduplication |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent SonarQube Cloud python:S1192 Code Smells: 43 current OPEN receipt keys in scripts/generate_compiler_guides.py. |
| Boundary | Parent compiler-guide generator, this English/German Change Record pair, and their indexes. Generated guide files, connector or runtime behavior, Framework, MRTS, Gitlinks, workflows, SonarQube Cloud configuration, Quality Gates, suppressions, external issue state, push, pull request, and merge remain unchanged. |

## Motivation and problem statement

The current SonarQube Cloud receipt inventory reports 43 open python:S1192
findings in the Parent compiler-guide generator. Repeated static guide
metadata, command fragments, source descriptions, and verification strings
obscure the source of the rendered values and make future edits error-prone.

## Acceptance criteria

- Address exactly the 43 receipt-backed python:S1192 occurrences in the
  compiler-guide generator by reusing semantically identical module constants.
- Preserve generated English and German compiler guides byte-for-byte.
- Pass the native compiler-guide verification, the receipt-level static audit,
  whitespace review, and repository documentation checks.
- Maintain an equivalent English/German Change Record pair and do not claim
  any SonarQube Cloud issue closed before a new exact candidate-head analysis.

## Implementation decision and rationale

The repeated values are represented by module-local constants whose values are
identical to the prior literals. Existing data structures, rendering order,
branch selection, generated paths, and command text remain unchanged. The
generator continues to be the single source for all rendered guide material;
no generated file is edited directly.

## Changed files

- scripts/generate_compiler_guides.py
- reports/audits/change-records/CR-20260727-sonar-compiler-guides-literal-deduplication.md
- reports/audits/change-records/CR-20260727-sonar-compiler-guides-literal-deduplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Commands executed

- rtk proxy make check-compiler-guides
- Receipt-backed AST literal audit for the 43 current python:S1192 keys
- rtk proxy git diff --check
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-doc-links

The isolated task worktree initialized the Parent-recorded Framework Gitlink
at 47e50e7bc43ba7a3b5bad1a9448111794f664cc0 only as a documentation-check
dependency. No Framework source, Parent Gitlink, Framework branch, or
Framework pull request changed.

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Compiler-guide verification | passed: make check-compiler-guides completed 21 tests, including idempotent generation and byte-for-byte generated-guide comparison. |
| Receipt-backed AST literal audit | passed: sonar_receipt_issues=43 and issue_literals_still_duplicated=0. |
| git diff --check | passed: no whitespace error. |
| Direct source-diff review | passed: only semantically identical module-local constants and their direct uses changed in the generator. |
| make check-bilingual-docs | passed: bilingual docs ok. |
| make check-doc-links | passed: repository path references: PASS and doc links ok. |

## Security impact

The focused security assessment is not_applicable. This is an
output-equivalent documentation-generator refactor; it changes no runtime
path validation, network, subprocess, connector, credential, permission, or
security control. No security finding is claimed fixed.

## Documentation status

The generator verification confirms that the emitted English/German guide
content is unchanged. This paired Change Record documents the source-only
deduplication. The completed repository documentation checks report bilingual
docs ok, repository path references PASS, and doc links ok.

## Runtime evidence

No connector, host, protocol, or production runtime behavior changed or is
claimed. Generator verification is source and documentation evidence, not
runtime evidence.

## Known limitations

SonarQube Cloud has not yet analyzed this candidate head. The 43 current
findings can disappear only after a fresh analysis of the exact delivered
commit.

## Remaining risks

A mistaken replacement could change a generated guide value or command. The
native generator check performs byte-for-byte output comparison, and the
source diff is limited to values backed by the current receipt.

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

The task-worktree candidate contains only the compiler-guide literal
deduplication and its required bilingual traceability material. The
authoritative Parent checkout, Framework source, MRTS source, Parent Gitlink,
scanner controls, and external SonarQube Cloud issue states remain unchanged.
