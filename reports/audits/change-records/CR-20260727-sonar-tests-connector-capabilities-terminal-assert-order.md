# Change Record: Parent connector-capabilities terminal assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-tests-connector-capabilities-terminal-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-tests-connector-capabilities-terminal-assert-order |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smells AZ-KYVU7fYmbqbBXVNHA (376), AZ-KYVU7fYmbqbBXVNHB (387), AZ-KYVU7fYmbqbBXVNHC (425), AZ-KYVU7fYmbqbBXVNHD (432), AZ-KYVU7fYmbqbBXVNHE (433), AZ-KYVU7fYmbqbBXVNHF (434), and AZ-KYVU7fYmbqbBXVNHI (469). |
| Boundary | Parent test source plus this English/German Change Record pair and indexes. Connector-capabilities production behavior, Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |

## Motivation and decision

Seven selected assertions put literal/list/dictionary/name expected values
before observed merge, result, payload, or return-code values. This change
reverses only those first two arguments to `actual, expected`. The adjacent
validator rows at lines 450 and 454 remain unchanged: the first has a genuine
Framework-Gitlink environment blocker and the second has a `command.index()`
operand requiring separate evaluation-order review.

## Validation

| Check | Result |
| --- | --- |
| Four focused Parent-only methods before the edit | passed: 4 tests in 0.281s. |
| The same methods after the edit | passed: 4 tests in 0.282s. |
| Five-method preflight including line 450 | blocked_environment: exactly the uninitialized Framework canonical validator is missing; line 450 was excluded without a source edit. |
| Structural AST inventory | passed: exactly seven selected lines are actual-first; lines 450 and 454 remain original-order exclusions. |
| Bilingual Change Record validation | passed: `tests.test_bilingual_docs`, 13 tests in 0.035s. |
| `git diff --check` | passed after the full B09 traceability pair and indexes were added. |

## Security impact and limitations

`not_applicable` to production code: this is test-diagnostic ordering only.
The overlay/validation integrity assertions and Framework-boundary refusal are
retained. The local candidate is uncommitted; no hosted Sonar analysis, GitHub
CI, commit, push, pull request, or master merge has occurred. The listed keys
remain OPEN until a delivered head is analyzed.
