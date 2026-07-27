# Change Record: Parent no-CRS selected-runner assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-tests-no-crs-selected-runner-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-tests-no-crs-selected-runner-assert-order |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smells AZ-KYVRQfYmbqbBXVNDt (30), AZ-KYVRQfYmbqbBXVNDu (46), AZ-KYVRQfYmbqbBXVNDv (133), AZ-KYVRQfYmbqbBXVNDw (139), AZ-KYVRQfYmbqbBXVNDx (168), AZ-KYVRQfYmbqbBXVNDy (193), AZ-KYVRQfYmbqbBXVNDz (194), AZ-KYVRQfYmbqbBXVND0 (218), AZ-KYVRQfYmbqbBXVND1 (219), AZ-KYVRQfYmbqbBXVND2 (282), AZ-KYVRQfYmbqbBXVND3 (316), AZ-KYVRQfYmbqbBXVND4 (340), and AZ-KYVRQfYmbqbBXVND5 (360). |
| Boundary | Parent test source plus this English/German Change Record pair and indexes. No-CRS runner behavior, Makefiles, Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |

## Motivation and decision

Thirteen selected assertions put an expected literal or constructed expected
string before the observed command/result value. Only their first two
arguments now follow `actual, expected`; every existing third diagnostic
argument is unchanged. The hostile Make-value and shell-injection test inputs,
their expected blocked output, and the sentinel assertions are not changed.

## Validation

| Check | Result |
| --- | --- |
| Three focused Parent-only methods before the edit | passed: 3 tests in 0.235s. |
| The same methods after the edit | passed: 3 tests in 0.223s. |
| Structural AST inventory | passed: exactly 13 selected lines have an observed value first and literal/constructed expected value second. |
| Bilingual Change Record validation | passed: `tests.test_bilingual_docs`, 13 tests in 0.033s. |
| `git diff --check` | passed after the full B06 traceability pair and indexes were added. |

## Security impact and limitations

`not_applicable` to production code: this is test-diagnostic ordering only.
The focused methods retain their hostile Make-value checks and shell-injection
sentinel assertions, which passed before and after the edit. The local
candidate is uncommitted; no hosted Sonar analysis, GitHub CI, commit, push,
pull request, or master merge has occurred. The listed keys remain OPEN until
a delivered head is analyzed.
