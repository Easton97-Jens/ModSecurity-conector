# Change Record: Parent transport-lifecycle artifacts assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-tests-transport-lifecycle-artifacts-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-tests-transport-lifecycle-artifacts-assert-order |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smells AZ-KYVOjfYmbqbBXVNC1 (61), AZ-KYVOjfYmbqbBXVNC2 (62), AZ-KYVOjfYmbqbBXVNC3 (64), AZ-KYVOjfYmbqbBXVNC4 (68), AZ-KYVOjfYmbqbBXVNC5 (69), AZ-KYVOjfYmbqbBXVNC6 (70), AZ-KYVOjfYmbqbBXVNC7 (71), AZ-KYVOjfYmbqbBXVNC8 (72), AZ-KYVOjfYmbqbBXVNC9 (76), AZ-KYVOjfYmbqbBXVNC- (77), AZ-KYVOjfYmbqbBXVNDA (151), and AZ-KYVOjfYmbqbBXVNDB (177). |
| Boundary | Parent test source plus this English/German Change Record pair and indexes. Transport artifact production helpers, Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |

## Motivation and decision

Twelve selected assertions put literals before observed artifact fields or
in-memory counts. This change reverses only those first two arguments to
`actual, expected`. The Framework-subprocess assertion at line 126 remains
unchanged, and the line-178 assertion with a `source.read_bytes()` expected
operand remains deferred for separate evaluation-order review.

## Validation

| Check | Result |
| --- | --- |
| Three focused Parent-only methods before the edit | passed: 3 tests in 0.004s. |
| The same methods after the edit | passed: 3 tests in 0.004s. |
| Structural AST inventory | passed: exactly the 12 selected lines are actual-first; lines 126 and 178 remain in their original order. |
| Bilingual Change Record validation | passed: `tests.test_bilingual_docs`, 13 tests in 0.035s. |
| `git diff --check` | passed after the full B07 traceability pair and indexes were added. |

## Security impact and limitations

`not_applicable` to production code: this is test-diagnostic ordering only.
Payload-redaction, hash-only retention, and forbidden-payload assertions remain
intact and passed before and after the edit. The local candidate is uncommitted;
no hosted Sonar analysis, GitHub CI, commit, push, pull request, or master
merge has occurred. The listed keys remain OPEN until a delivered head is
analyzed.
