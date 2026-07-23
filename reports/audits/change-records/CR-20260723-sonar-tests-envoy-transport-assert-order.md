# Change Record: Parent Envoy transport assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260723-sonar-tests-envoy-transport-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-sonar-tests-envoy-transport-assert-order |
| Date (UTC) | 2026-07-23 |
| Base revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
| Tracking | Nineteen Parent-only `python:S3415` Code Smells in `tests/test_envoy_transport_hardening_contract.py`. |
| Boundary | Parent test source plus this English/German traceability pair and indexes. Framework, MRTS, gitlinks, Envoy runtime/helper source, scanner configuration, Quality Gates, suppressions, and runtime behavior remain unchanged. |

## Motivation and problem statement

SonarQube Cloud reports existing `unittest.TestCase.assertEqual` calls whose
expected and actual operands are reversed. The assertions already express the
intended predicates; swapping only their first two top-level operands aligns
failure diagnostics with the project convention without changing the equality
comparison or its pass/fail outcome.

The selected current keys are `AZ-KYVTIfYmbqbBXVNFo`,
`AZ-KYVTIfYmbqbBXVNFp`, `AZ-KYVTIfYmbqbBXVNFq`,
`AZ-KYVTIfYmbqbBXVNFr`, `AZ-KYVTIfYmbqbBXVNFs`,
`AZ-KYVTIfYmbqbBXVNFt`, `AZ-KYVTIfYmbqbBXVNFu`,
`AZ-KYVTIfYmbqbBXVNFv`, `AZ-KYVTIfYmbqbBXVNFw`,
`AZ-KYVTIfYmbqbBXVNFx`, `AZ-KYVTIfYmbqbBXVNFy`,
`AZ-KYVTIfYmbqbBXVNFz`, `AZ-KYVTIfYmbqbBXVNF0`,
`AZ-KYVTIfYmbqbBXVNF1`, `AZ-KYVTIfYmbqbBXVNF2`,
`AZ-KYVTIfYmbqbBXVNF3`, `AZ-KYVTIfYmbqbBXVNF4`,
`AZ-KYVTIfYmbqbBXVNF5`, and `AZ-KYVTIfYmbqbBXVNF6`.

## Acceptance criteria

- Swap exactly the first two operands of the 19 selected `assertEqual` calls.
- Preserve all assertion operand expressions, predicates, fixture behavior,
  controlled loopback interactions, test inputs, and expected values.
- Pass the complete affected test module without generated checkout artifacts.
- Keep both Change Record languages and both indexes equivalent.
- Obtain fresh exact-head SonarQube Cloud and hosted-check evidence for an
  open, unmerged Draft PR before treating any selected key as resolved.

## Implementation decision and rationale

The contract now supplies each observed HTTP status, parsed evidence field,
record field, receive-limit list, body-byte result, and event-line count first,
followed by its fixed expected value. The inner order of every expression and
all test setup remain intact. No assertion is added, deleted, weakened, or
suppressed, and no production Envoy behavior changes.

This batch deliberately covers only these 19 reviewed Parent test findings.
Other SonarQube Cloud observations remain separate work.

## Security impact

The test module covers controlled loopback transport and temporary-file
evidence contracts, but this change is diagnostic ordering only. No socket
behavior, parser, untrusted input path, temporary-file policy, authorization
decision, evidence rule, runtime helper, configuration, or security control
changes. This maintainability-only batch does not claim to fix a security
finding.

## Changed files

- tests/test_envoy_transport_hardening_contract.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

- The complete affected `tests.test_envoy_transport_hardening_contract` module
  passed after the correction: 8 tests in 1.141 seconds.
- AST/source inventory passed: exactly the 19 selected `assertEqual` calls
  retain their operands and use actual-first order.
- `git diff --check` passed.

## Tests and actual results

| Command or check | Result |
| --- | --- |
| `rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> -m unittest -v tests.test_envoy_transport_hardening_contract` | passed: 8 tests in 1.141 seconds. |
| AST/source operand inventory of lines 50, 51, 75, 111, 194, 195, 200, 204-209, 212, 227, and 292-295 | passed: 19 selected calls, all actual-first. |
| `git diff --check` | passed. |

## Runtime evidence

No connector runtime behavior changed or is claimed. The affected module uses
bounded loopback fixtures and temporary test files; it is not a production
Envoy deployment or a Framework/MRTS run.

## Checks not run and rationale

- No full connector build or runtime matrix: the change only reorders test
  diagnostic operands and the complete affected module passed.
- No Framework or MRTS test or modification: they are excluded from this
  Parent-only task.
- Hosted checks and SonarQube Cloud PR analysis are not claimed by this local
  record; they require a pushed exact Draft-PR head and external evidence.

## Known limitations

This batch addresses only 19 selected `python:S3415` observations. It does not
claim to clear the broader SonarQube Cloud backlog or validate unavailable
connector runtime environments.

## Remaining risks

An accidental change beyond the selected top-level operand order could make
failure diagnostics misleading. The exact source inventory, focused module,
and final diff review reduce that risk. Fresh hosted exact-head analysis
remains required before delivery is verified.

## Final diff and review status

Local source correction and its focused test passed on a Parent-only task
branch based on `5b8db00d44ab24f3a9f4216a00f7edee977b6898`. This record makes
no unobserved hosted-check, SonarQube Cloud, review, merge, or default-branch
claim. The intended delivery is an open unmerged Draft PR only.
