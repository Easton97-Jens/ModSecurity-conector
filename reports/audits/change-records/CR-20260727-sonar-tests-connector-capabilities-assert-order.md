# Change Record: Parent connector-capabilities assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-tests-connector-capabilities-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-tests-connector-capabilities-assert-order |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smells AZ-KYVU7fYmbqbBXVNGk (142), AZ-KYVU7fYmbqbBXVNGl (144), AZ-KYVU7fYmbqbBXVNGm (145), AZ-KYVU7fYmbqbBXVNGn (146), AZ-KYVU7fYmbqbBXVNGo (148), AZ-KYVU7fYmbqbBXVNGp (149), AZ-KYVU7fYmbqbBXVNGq (150), AZ-KYVU7fYmbqbBXVNGr (151), AZ-KYVU7fYmbqbBXVNGs (176), AZ-KYVU7fYmbqbBXVNGt (177), and AZ-KYVU7fYmbqbBXVNGu (178). |
| Boundary | Parent test source plus this English/German Change Record pair and indexes. Production connector-capabilities behavior, Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |

## Motivation and decision

Eleven selected `unittest` assertions placed an expected literal before a
dictionary-subscript observed value. This change reverses only those first two
arguments so diagnostics follow `actual, expected`; the same key lookup,
predicate, expected literal, temporary Git fixture, and capability/provenance
semantics are retained. The adjacent variable-expected assertions at lines 143
and 147 are not inventory rows and remain unchanged.

## Acceptance criteria

- Correct only the eleven listed S3415 assertions.
- Preserve both temporary Git-repository fixtures and their Gitlink/provenance assertions.
- Pass the two affected Parent-only test methods before and after the edit.
- Pass a structural AST check for exactly the eleven actual-first assertions, bilingual documentation validation, and `git diff --check`.
- Keep Framework/MRTS source and Gitlinks untouched.

## Changed files

- tests/test_connector_capabilities.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Validation

| Check | Result |
| --- | --- |
| First focused method before the edit | passed: 1 test in 0.246s. |
| Second focused method before its three-line edit | passed: 1 test in 0.169s. |
| Both focused methods after the full eleven-line edit | passed: 2 tests in 0.376s. |
| Structural AST inventory | passed: exactly lines 142, 144-146, 148-151, and 176-178 have a subscript actual value followed by a literal expected value. |
| Bilingual Change Record validation | passed: `tests.test_bilingual_docs`, 13 tests in 0.034s. |
| `git diff --check` | passed after the full B04 traceability pair and indexes were added. |

## Security impact

`not_applicable`: this is test-diagnostic argument ordering only. The tests
retain their temporary repositories, Git metadata checks, and Parent-only
source behavior. No production or security control changed and no security
finding is claimed fixed.

## Limitations and delivery state

The complete `tests.test_connector_capabilities` module is not used as B04
evidence because an unrelated method needs the intentionally uninitialized
Framework Gitlink. The two changed methods create their own temporary
framework-shaped repositories and passed independently. The local candidate is
uncommitted; no hosted Sonar analysis, GitHub CI, commit, push, pull request,
or master merge has occurred. The listed keys remain OPEN until a delivered
head is analyzed.
