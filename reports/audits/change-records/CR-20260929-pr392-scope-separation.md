# Separate PR 392 from the NGINX B09 change

**Language:** English | [Deutsch](CR-20260929-pr392-scope-separation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260929-pr392-scope-separation` |
| Date (UTC) | 2026-09-29 |
| Base revision | `b9208c4cad24a0186e810f25d946f4bca664a278` |
| Delivery target | Existing Parent Draft PR #392; no merge |

## Motivation and problem statement

The user authorized resolving the merge-readiness review. PR #391 owns the
complete proposed B09 classifier and P2-tail change. PR #392 carried a narrower
classifier change and a contradictory assertion for a zero-result error page.
The two independent drafts must not impose opposite contracts on one function.

## Acceptance criteria

PR #392 must have no NGINX production diff against its original master base.
Its B13 and C07 production changes and existing assertions remain intact.
B09 remains open and owned by PR #391; this separation does not claim a fix.

## Implementation decision and rationale

Restore the NGINX header to the exact base blob
`889e3c4765da0166f277f9b10c070543d9acdc16`. Remove only the competing B09 test
method and its unused source path. Retain the B13 boundary/caller assertions
and C07 source assertions. Correct the C07 test's stale reference to a separate
Framework normalizer patch, which is not part of Framework PR #128.
The earlier reported-findings record describes historical preparation; this
record supersedes its B09 delivery scope, not its recorded historical evidence.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `tests/test_reported_security_regressions.py`
- This English/German Change Record pair.

## Commands executed

GitHub API source/blob reads and a scoped source transformation were performed.
The original test file matched its current Git blob identity before editing.
Python AST parsing and preservation of the B13 assertion bodies were checked
as data processing. Local project tests were NOT RUN: required RTK and the
provisioned repository environment are unavailable. New-head CI is pending.

## Security impact

No B09 remediation is shipped by PR #392 alone. The more complete candidate
and B09 regressions remain in PR #391. This is intentional work-item separation,
not risk acceptance, removal of a required global gate, or finding closure.
B13/C07 behavior, dependency pins, CI permissions and submodule gitlinks do not change.

## Runtime evidence

This follow-up creates no live-host evidence. Existing green checks on the
previous head are not claimed for this new commit. Real B13 proxy boundaries
and C07 client/event agreement still require their scoped runtime checks.

## Known limitations

This does not establish that either security finding is fully verified.
The C07 source contract does not execute the sidecar or normalize a real event.

## Remaining risks

After integration of either independent PR, rerun checks on the combined tree.
Do not choose the old contradictory BYPASS assertion when resolving future conflicts.

## Checks not executed and reasons

Native builds, local suites and live hosts were not executed in this editor
because its mandatory command wrapper and provisioned environments are absent.
No skipped or pending check is reported as passing.

## Final diff and review status

The change is limited to scope separation. The existing PR remains a draft;
no merge, force push, quality-gate waiver, severity change or finding closure occurs.
