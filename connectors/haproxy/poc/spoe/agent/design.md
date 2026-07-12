# HAProxy SPOA Agent Design Plan

**Language:** English | [Deutsch](design.de.md)

## Status

documentation_only: true
implementation_status: not_started
runtime_verified: false
language_selected: false
decision_status: undecided
promoted: false

## Purpose
This document only describes what tasks a later SPOA agent
would have to fulfill. It contains no implementation and proves none
Functionality.

## Role of the agent
- The agent would be an external component in the SPOE/SPOA audit trail.
  (Proven by repository)
- It would potentially receive SPOE/SPOP messages later.
  (To be verified externally.)
- He would potentially check request data later.
  (To be checked.)
- It would potentially return a result to HAProxy later.
  (To be verified externally.)
- Everything is planned only / Still to be checked.

## Non-targets
- No productive integration.
- Do not set language.
- Do not fully implement any protocol.
- Do not implement ModSecurity call.
- No CRS loading.
- Claim no response body support.
- No performance promise.
- Do not finalize fail-open/fail-closed.

## Open design decisions

| decision | Status | Why relevant | Open points |
|---|---|---|---|
| programming language | Still to be checked. | Affects tooling, runtime model, maintainability. | Do not finally select a language. |
| SPOP protocol library or custom implementation | To be verified externally. | Core of SPOE/SPOA communication. | API maturity, compatibility, failure modes. |
| Request field model | Still to be checked. | Defines available test basis in the agent. | Field completeness not proven. |
| Request body handling | Still to be checked. | Relevance for deeper rule checking. | Availability/size limits unclear. |
| Response header handling | Still to be checked. | Relevance for later extended audit trails. | Timing/coverage unclear. |
| Response body handling | Still to be checked. | Relevance to full semantics. | To be verified externally; not minimal scope. |
| ModSecurity/libmodsecurity binding | Still to be checked. | Central to true WAF semantics. | Not available from the current repository. |
| Intervention Mapping | Still to be checked. | Required for block/allow/redirect/log. | To be verified externally. |
| Error behavior | Still to be checked. | Stability and safety in the event of an incident. | Fail-open/fail-closed not finalized. |
| Logging | Still to be checked. | Traceability and evidence management. | Mandatory fields/format to be verified externally. |
| Report output | Still to be checked. | Comparable PoC results. | Fields/schema final not set. |
| Testability | Still to be checked. | Verification without production claim. | Harness coupling and measurement criteria open. |

## Planned minimal data model

| field | Purpose | Status | border |
|---|---|---|---|
| method | Request method for basic check | Still to be checked. | Complete semantics not proven. |
| uri | Entire Destination URI | Still to be checked. | Exact normalization to be verified externally. |
| path | Path-based rules | Still to be checked. | Derivation/normalization unclear. |
| query | Query-based rules | Still to be checked. | Field coverage not proven. |
| headers | Header based rules | Still to be checked. | Canonicalization/multiple values ​​unclear. |
| client_ip | Basic context | Still to be checked. | Source/trust model to be verified externally. |
| request_body | Potentially for Body Rules | Still to be checked. | Availability/size/streaming unclear. |
| transaction_id | Correlation Logs/Decisions | Still to be checked. | Origin/format not final. |
| decision | allow/block/log (planned decision) | Still to be checked. | Mapping not finalized. |
| status_code | Scheduled Return Status | Still to be checked. | Verify HAProxy/SPOE semantics externally. |
| log_message | Traceability | Still to be checked. | Minimum content/PII rules open. |

Addition:
- response_body: Not in minimum scope / Still to be checked.
- intervention mapping: To be checked.

## Planned decision flow
(everything planned only)

1. Agent receives request from HAProxy/SPOE. (planned only)
2. Agent extracts available request metadata. (planned only)
3. Agent evaluates minimal test case. (planned only)
4. Agent generates planned decision: allow/block/log. (planned only)
5. Agent returns result to HAProxy. (planned only)
6. Agent writes logs. (planned only)
7. Harness collects logs. (planned only)

## ModSecurity connection
- A real libmodsecurity connection is not yet implemented in this PoC.
- Whether and how libmodsecurity is called correctly from a SPOA agent
  can still be checked.
- CRS cover is not part of the minimal design.
- Complete ModSecurity semantics cannot be proven from the current one
  Repository.

## Intervention Mapping

| ModSecurity result | Scheduled HAProxy/SPOE result | Status | Open points |
|---|---|---|---|
| allow | pass-through (planned only) | Still to be checked. | To be verified externally. |
| block/deny | deny/block signal (planned only) | Still to be checked. | To be verified externally. |
| redirect | redirect signal (planned only) | Still to be checked. | To be verified externally. |
| log only | log signal (planned only) | Still to be checked. | To be verified externally. |
| error | error/fallback signal (planned only) | Still to be checked. | Fail-open/fail-closed open. |

## Logging/Reporting
- What would be necessary later would be at least:
  - request identifier / transaction_id,
  - decision,
  - status_code,
  - log_message,
  - Timing/correlation.
  (To be checked.)
- There is currently no runtime report. (Proven by repository)
- `reports/testing/haproxy-spoe-poc-results.generated.md` is planned only.
  (Proven by repository)

## Risks

| Risk | Status | Meaning |
|---|---|---|
| SPOP protocol incompletely understood | open | To be verified externally. |
| Request Body unclear | open | Still to be checked. |
| Response body unclear | open | Still to be checked. |
| libmodsecurity lifecycle unclear | open | Still to be checked. |
| Intervention mapping unclear | open | Still to be checked. |
| Error behavior unclear | open | Still to be checked. |
| Performance unknown | open | Still to be checked. |

## Acceptance criteria for this document
- It does not contain any implementation.
- It does not select a language final.
- It does not claim runtime capability.
- It clearly marks all open points.
- It remains compatible with the SPOE/SPOA PoC plan.

## Next step
A documentation-only harness design plan below
Create `connectors/haproxy/poc/spoe/harness/design.md` without any code
write.
