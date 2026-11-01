# Change Record: CR-20261030-nginx-request-error-status

**Language:** English | [Deutsch](CR-20261030-nginx-request-error-status.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261030-nginx-request-error-status |
| Date (UTC) | 2026-10-30 |
| Base revision | `8c7e8c44cf69ac4e9d7ffb9101365c552f2ca7cf` |

## Motivation and problem statement

Real H1 injection of the two internal Common input faults returned HTTP 500
and CONNECTOR_ERROR while the native event omitted the known terminal status
(`http_status=0`). A separate Framework expectation still selected the legacy
`phase1_error` event name. Common intentionally emits the canonical
`connector_error` event with typed `phase=request_headers`.

## Acceptance criteria

Report a selected terminal status from 400 through 599 without inventing a
visible response, completed transport or actual action. Preserve timeout 504,
late/control result 0, HTTP fail-closed behavior and one-attempt event writing.
Consumers must check the canonical event, exact phase, message ID and status.

## Implementation decision and rationale

The Product producer copies the already selected bounded request-error status
into HTTP metadata. It leaves transport and visible-status fields untouched.
This closes an observability gap; it changes neither wire status selection nor
request lifecycle. Common canonicalization remains authoritative; Framework
consumers migrate to that contract instead of reverting Product normalization.
See [the event contract](../../../docs/pr-382-event-contract.md).

## Changed files

`connectors/nginx/src/ngx_http_modsecurity_access.c` and this EN/DE record.
Producer regressions, strict consumers and their negative fixtures belong to
Framework PR #142. This Product correction is a separate commit from ownership
migration and Framework pin changes.

## Commands executed

- Existing producer regression: 15 methods; six expanded assertions reproduced
  missing known 500/400/413 metadata before the fix.
- The same real extracted Product producer and Common writer: 15 PASS after
  the fix (1.631 seconds), including known 500/400/413, timeout 504 and late or
  control result 0; visible status, action and transport assertions remain.
- Existing Framework driver and public consumer: 9 and 4 methods PASS.
  Combined scoped proof: 28 methods / 156 expanded subtests, zero skips.
- Real pre-fix H1 baseline: PASS. Both injected faults: wire HTTP 500 with
  native fault ledger and completed cleanup, failed stale event selection.
- Product diff whitespace check: PASS.

## Security impact

Only existing bounded metadata becomes observable. The correction cannot
promote absent transport evidence to a visible response or successful action.
Malformed client input remains protocol error/HTTP 400; internal pointer faults
remain connector error/HTTP 500. No validation, isolation or warning changes.

## Runtime evidence

Synthetic receipts are retained in the external task evidence directory under
`nginx-canonical-event-regression`; no customer traffic is included. The prior
runtime failures remain recorded. Compile/unit evidence is distinct from the
required new native module and H1 runtime verification.

## Known limitations

A known selected status is not proof of delivery. HTTP control codes outside
400..599 remain 0. The existing timeout-specific 504 behavior is retained.

## Remaining risks

Reverting the two assignments restores the omission without changing wire
behavior; there is no configuration or storage migration.

## Checks not run and rationale

Fresh rebuilt H1 runtime and current-head hosted checks/SonarCloud are pending
at this source-record point. No complete historical or on-demand campaign ran.

## Final diff and review status

The exact producer omission and canonical-event distinction were independently
reviewed against actual C execution and checked-in contracts. Conditional user
merge authority requires clean current-head SonarCloud, no new open findings
and all repository gates; this record does not assert those pending results.
