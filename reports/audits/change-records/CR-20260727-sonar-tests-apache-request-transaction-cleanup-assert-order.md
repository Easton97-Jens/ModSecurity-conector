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

## Motivation and problem statement

The concrete Sonar rule, Parent test scope, and behavior-preservation rationale
are recorded in the preceding `## Motivation and decision` section. This
structural correction does not change the documented source or test behavior.

## Acceptance criteria

- Preserve the exact remediation and focused validation already recorded.
- Retain equivalent technical facts in this English/German Change Record pair.
- Do not convert blocked, unrun, or pending hosted evidence into a pass.

## Implementation decision and rationale

Keep the existing rationale and validation intact, and restore the canonical
Change Record headings instead of weakening the documentation checker or
creating a record-specific exception.

## Changed files

The original versioned scope is recorded in `## Identity` and the preceding
implementation narrative. This follow-up changes only the structure of this
Change Record pair.

## Commands executed

The exact commands and observed outcomes remain in `## Validation`; this
structural correction does not reclassify any result.

## Security impact

The existing section below remains authoritative for this record's specific
boundary. This normalization changes no security control.

## Security impact and limitations

`not_applicable`: this is test-diagnostic ordering only. The test still reads
the same Parent Apache C/header/check-script sources; no production request or
transaction behavior changed. The local candidate is uncommitted and no hosted
Sonar analysis, GitHub CI, commit, push, pull request, or master merge has
occurred. The Sonar key remains OPEN until a delivered head is analyzed.

## Runtime evidence

No additional runtime evidence is claimed by this structural correction; the
existing validation retains only its recorded Parent test-module scope.

## Known limitations

The record's focused validation is intentionally narrower than a native Apache
build or hosted analysis.

## Remaining risks

No new risk is introduced by record normalization. Hosted analysis remains
limited to results actually observed for a later delivery head.

## Checks not run and rationale

No additional connector runtime, native Apache build, or hosted check is run
for this documentation-only correction.

## Final diff and review status

The earlier delivery wording is a snapshot of the original local validation.
This record does not assert a final PR verification, merge, or Sonar issue
closure for a later delivery head.
