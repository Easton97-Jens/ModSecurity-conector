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
- Obtain fresh exact-head SonarQube Cloud and hosted-check evidence before
  treating any selected key as resolved or delivery as verified.

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
  passed after the normal current-master update: 8 tests in 1.144 seconds.
- Cross-tree AST/source inventory passed: exactly 19 `assertEqual` calls are
  exact expected-to-actual operand reversals, with every other operand
  expression preserved.
- Final `git diff --check` is rerun after this delivery-evidence update.

## Tests and actual results

| Command or check | Result |
| --- | --- |
| `rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> -m unittest -v tests.test_envoy_transport_hardening_contract` | passed: 8 tests in 1.144 seconds after the current-master update. |
| Cross-tree AST/source operand inventory | passed: 19 exact expected-to-actual reversals; all other `self.assertEqual` operand pairs are unchanged. |
| `git diff --check origin/master...HEAD` | rerun after this Change Record update. |

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
  record; they require a pushed exact PR head and external evidence.

## Known limitations

This batch addresses only 19 selected `python:S3415` observations. It does not
claim to clear the broader SonarQube Cloud backlog or validate unavailable
connector runtime environments.

## Remaining risks

An accidental change beyond the selected top-level operand order could make
failure diagnostics misleading. The exact source inventory, focused module,
and final diff review reduce that risk. Fresh hosted exact-head analysis
remains required before delivery is verified.

### Current Parent-master update — 2026-07-24

Existing Draft PR #107 was normally updated without a rebase by merging Parent
master `a60dd0380332a24cf231a36775256d21a812c027`. The resulting local merge
commit `345b699eef301e6088286048cf13ba08f29345a9` reconciled the shared
Change Record indexes by retaining all current-master entries and this #107
entry. It does not modify Framework or MRTS; it only inherits existing master
history. The current PR-base diff remains this Parent test, this
English/German Change Record pair, and the two indexes, with no Framework,
MRTS, gitlink, Envoy runtime/helper source, scanner, Gate, suppression, or
security-control change authored by this PR update.

The current merged-tree affected module passed eight tests, and the independent
cross-tree AST/source inventory verified exactly 19 expected-to-actual operand
reversals. Hosted check, SonarQube Cloud, Quality Gate, review, readiness, and
merge results are claimed only through observed exact-head PR delivery
metadata.

## Final diff and review status

The Parent-only PR #107 is the delivery vehicle and now contains the normal
current-master update merge `345b699eef301e6088286048cf13ba08f29345a9` plus
this paired delivery-evidence update. This record claims neither review
approval, merge, nor a default-branch change. Before protected merge, the PR
must be non-draft and its current exact remote head must have passing hosted
checks and SonarQube Cloud analysis plus refreshed review state; those observed
facts belong to delivery metadata rather than an unobserved claim in this
record.
