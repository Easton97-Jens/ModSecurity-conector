# Change Record: CR-20261015-i12-exact-parser-exit

**Language:** English | [Deutsch](CR-20261015-i12-exact-parser-exit.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-i12-exact-parser-exit |
| Date (UTC) | 2026-10-15 |
| Base revision | `a2d545ac7ec4abce23595e1c033f094104617201` |

## Motivation and problem statement

The stricter parser qualifier admitted only rejection exit1. Official lighttpd1.4.85 server.c returns-1 after module set-default rejection, producing actual POSIX process exit255. Exact source-reviewed255 expectations must be representable without changing measured exits or normalizing all nonzero values.

## Acceptance criteria

Require an exact integer exit in0..255, acceptance0, rejection1..255. Preserve actual exit equality, independent expectation provenance, explicit Root review, physical parser receipts and every existing required producer.

## Implementation decision and rationale

Replace the two-value expectation tuple with bounded typed acceptance/rejection validation. Boolean and float expected exits are rejected. A source-reviewed255 expectation accepts only actual255; actual1 remains FAIL. No HTTP/body lifecycle scope changes.

## Changed files

ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py and tests/test_i12_lifecycle_ledger.py; this EN/DE record.

## Commands executed

RTK-wrapped two new regressions reproduce baseline rejection of255 and incorrect bool/float oracle admission. After correction, shared lifecycle/oracle/workflow suites:47 PASS. Actionlint on the SDK workflow also passes.

## Security impact

All exact process/source/image/absence/cleanup guards remain enforced. The implementation does not approve any oracle correction; each original ID requires its own independent reconciliation. No gate, warning or isolation relaxation.

## Runtime evidence

Run i12-lighttpd-412-completion-20261015/shared/parser-exact-exit-final.log retains47 successful tests. Existing seven diagnostic parser receipts observed255; stricter fresh per-ID packets and separate corrections remain follow-up work in#412. Synthetic validator fixtures prove only the validator.

## Known limitations

Parser qualifications remain configuration_control with full_lifecycle_qualified=false. This change adds no host PASS or automatic original-oracle resolution.

## Remaining risks

Reviewed source expectations can still be wrong; physical exact receipts and independent Root source review remain mandatory.

## Checks not run and rationale

No release, master integration, Framework/MRTS edits or other-connector host matrix. Hosted final-head CI remains pending normal publication.

## Final diff and review status

Root reviewed the narrow shared defect and preserved concurrent remote#410 parser hardening through normal merge. Product fixes travel separately through#382.
