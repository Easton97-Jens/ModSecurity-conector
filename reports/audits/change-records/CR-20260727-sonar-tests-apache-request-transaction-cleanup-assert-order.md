# Change Record: Parent Apache request-transaction cleanup assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-tests-apache-request-transaction-cleanup-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-tests-apache-request-transaction-cleanup-assert-order |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smell AZ-KYVVIfYmbqbBXVNHJ at line 64. |
| Boundary | Parent test source plus this English/German Change Record pair and indexes. Apache production C source, Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |

## Motivation and decision

The selected assertion expected literal `1` before its in-memory
`str.count` observation. This change reverses only those two arguments to
`actual, expected`. The same string, count predicate, and request-cleanup
contract remain unchanged.

## Validation

| Check | Result |
| --- | --- |
| Full Parent-only test module before the edit | passed: 5 tests in 0.004s. |
| Same module after the edit | passed: 5 tests in 0.004s. |
| Structural AST predicate | passed: line 64 has the `str.count` result first and integer literal `1` second. |
| Bilingual Change Record validation | passed: `tests.test_bilingual_docs`, 13 tests in 0.033s. |
| `git diff --check` | passed after the full B05 traceability pair and indexes were added. |

## Security impact and limitations

`not_applicable`: this is test-diagnostic ordering only. The test still reads
the same Parent Apache C/header/check-script sources; no production request or
transaction behavior changed. The local candidate is uncommitted and no hosted
Sonar analysis, GitHub CI, commit, push, pull request, or master merge has
occurred. The Sonar key remains OPEN until a delivered head is analyzed.
