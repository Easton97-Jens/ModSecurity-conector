# Change Record: Parent connector-capabilities follow-up assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-tests-connector-capabilities-followup-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-tests-connector-capabilities-followup-assert-order |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smells AZ-KYVU7fYmbqbBXVNGv (210), AZ-KYVU7fYmbqbBXVNGw (211), AZ-KYVU7fYmbqbBXVNGx (212), AZ-KYVU7fYmbqbBXVNGy (240), AZ-KYVU7fYmbqbBXVNGz (241), AZ-KYVU7fYmbqbBXVNG0 (243), AZ-KYVU7fYmbqbBXVNG1 (244), AZ-KYVU7fYmbqbBXVNG2 (247), AZ-KYVU7fYmbqbBXVNG3 (248), AZ-KYVU7fYmbqbBXVNG4 (286), AZ-KYVU7fYmbqbBXVNG5 (306), AZ-KYVU7fYmbqbBXVNG6 (311), AZ-KYVU7fYmbqbBXVNG7 (315), AZ-KYVU7fYmbqbBXVNG8 (319), AZ-KYVU7fYmbqbBXVNG9 (323), AZ-KYVU7fYmbqbBXVNG- (327), and AZ-KYVU7fYmbqbBXVNG_ (332). |
| Boundary | Parent test source plus this English/German Change Record pair and indexes. Connector-capabilities production behavior, Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |

## Motivation and decision

Seventeen selected assertions put constant expected capability/provenance
states before observed manifest, provenance, record, merge, or evidence
fields. This change reverses only those first two arguments to `actual,
expected`. The methods retain their temporary fixture repositories, gitlink
provenance cases, staleness checks, and runtime-merge assertions unchanged.

## Validation

| Check | Result |
| --- | --- |
| Four focused Parent-only methods before the edit | passed: 4 tests in 0.523s. |
| The same methods after the edit | passed: 4 tests in 0.536s. |
| Structural AST inventory | passed: exactly 17 selected lines have a dictionary-subscript actual value followed by a constant expected value. |
| Bilingual Change Record validation | passed: `tests.test_bilingual_docs`, 13 tests in 0.033s. |
| `git diff --check` | passed after the full B08 traceability pair and indexes were added. |

## Security impact and limitations

`not_applicable` to production code: this is test-diagnostic ordering only.
The tests retain their provenance and runtime-result integrity assertions. The
local candidate is uncommitted; no hosted Sonar analysis, GitHub CI, commit,
push, pull request, or master merge has occurred. The listed keys remain OPEN
until a delivered head is analyzed.
