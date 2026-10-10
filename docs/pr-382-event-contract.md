# PR #382: native results and event contract

**Language:** English | [Deutsch](pr-382-event-contract.de.md)

Status: implementation reference for an incomplete Draft migration, not a
claim of equivalent behavior in every running host. See the
[implementation and verification checklist](pr-382-checklist.md) for remaining
routes, pending checks, and revision-scoped evidence. Updated: 2026-09-22.

## Native results are operation-specific

The direct libModSecurity API and the host callback API have different return
conventions. Apply `common/include/msconnector/native_result.h` only at the
documented native boundary; preserve each surrounding API's own convention.

| Operation | Accepted native results | Required follow-up |
| --- | --- | --- |
| Direct request/response byte append | `0` or `1` | Continue the existing phase lifecycle and collect interventions at its intended boundary. A zero can represent engine-configured `ProcessPartial`; it is not proof that the entire chunk was inspected. |
| Request/response phase processing | `1` only | Reject other results as technical failures. Do not complete a failed phase or turn it into a successful safe-mode observation. |
| `msc_intervention()` in the changed Common/HAProxy paths | `0` or `1` | Distinguish no intervention from a collected intervention; reject undocumented results and release native buffers. |
| `msc_request_body_from_file()` | Separate API contract; changed NGINX path requires `1` | Do not reuse the byte-append rule: zero can also represent file I/O or allocation failure. The strict result check and cumulative file limit are implemented; native file-reader integration remains to be verified. |
| APR, NGINX, HTTP and Common callbacks | Their existing contracts | Do not reinterpret host success/error integers through the native helper. |

A successful native call is not an allow decision. For example, an engine limit
rejection can leave a pending disruptive intervention even when the append API
returns one. A helper or return-value fixture does not prove the timing and
ownership of every caller's intervention handling.

## Error cause and host action remain distinct

The changed Common failure bridge maps `MSCONNECTOR_ERROR_MODSECURITY_FAILURE`
to `MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE`. Timeout, unavailable
engine, connector, protocol and body-limit errors retain separate classes.

For known technical-error events the canonical metadata view uses `status=error`,
`requested_action=error`, a stable error reason, and an empty `rule_id`. A host
may still need to reject or abort; that action does not turn the technical
failure into a ModSecurity rule match. Body-limit policy events and actual rule
interventions are not automatically reclassified as technical errors.

The implemented NGINX late-error path classifies negative interventions before
Safe/Strict rule handling. Native phase failure does not complete the phase.
Mandatory Phase-4 log failures remain terminal. Only synchronous core-generated
terminal error responses may pass the bounded re-entry guard; this is not an
allow decision for the failed upstream chain. These guarantees are covered by
controlled tests, not a complete host/transport equivalence claim.

## Canonical JSONL and missing transport observations

`common/include/msconnector/event_protocol.h` provides the same normalized event
view to the Common JSONL writer and integrity hashing. Original input validation
runs before normalization so malformed or oversized fields cannot be hidden by
replacement values. Query redaction remains active; no body payload is added.

| Input condition | Canonical meaning |
| --- | --- |
| Known rule event with a NULL, empty or `not_observable` transport result | `event=engine_decision`, `message_id=MSCONN_EVENT_ENGINE_DECISION`, empty `actual_action`, and a message stating that host action was not observed. `action` retains the requested action. |
| Known technical error with missing transport observation | Retain the error cause, use `action=error`, and leave `actual_action` empty. |
| Observed late safe rule handling | Keep `actual_action=log_only` and the observed HTTP status. |
| Observed late strict abort after a status other than 200 | Use the generic `MSCONN_EVENT_PHASE4_HARD_ABORT`, not the message claiming an earlier HTTP 200. |
| Unknown application event | Preserve its application-owned semantics rather than treating it as a WAF event. |

The following is an illustrative field excerpt, not a complete serialized event
or a captured runtime result:

```json
{
  "event": "engine_decision",
  "message_id": "MSCONN_EVENT_ENGINE_DECISION",
  "status": "blocked",
  "action": "deny",
  "requested_action": "deny",
  "actual_action": "",
  "http_status": 403,
  "original_http_status": 201,
  "visible_http_status": 201,
  "transport_result": "not_observable"
}
```

Here `status=blocked` classifies the engine's rule decision; it does not assert
that a block reached the client. Do not determine client-visible enforcement
from `status`, `action`, or the requested HTTP status alone.

Normalization does not invent or overwrite timestamps, byte counts, EOS,
commitment, HTTP observations, abort/reset flags, or transport evidence. Event
producers must supply truthful, mutually consistent metadata; the remaining
producer-to-sink review is tracked separately. In particular, this change is
not a blanket correction of every body-limit, cancellation or custom event.

## Migration for log consumers

Consumers must recognize the new engine-decision identifier, tolerate an empty
`actual_action`, and keep requested actions separate from observed outcomes.
Do not infer enforcement from an old phase-event name or an earlier default
message. Compare the relevant metadata fields rather than expecting identical
transaction IDs, timestamps, host names, byte counts or native log prefixes.

The normalized representation also affects integrity hashing. Keep the producer
and verifier on compatible contract versions and validate retained records with
the implementation that produced them. A compatibility/versioning review for
historical consumers remains required before release. The ModSecurity audit log
and native host diagnostics remain separate from the Common metadata JSONL.

## Zero-finding Sonar verification

The user requires zero new PR issues and zero new security hotspots, not merely
a passed Sonar Quality Gate. `ci/checks/common/check-sonar-zero.py` reads the
Sonar GitHub Check for the exact PR head and requires explicit zero issue,
hotspot and annotation counts plus a successful conclusion.

Missing analysis, an older SHA, the wrong provider, missing or ambiguous counts,
a newer unfinished analysis, or any nonzero finding makes this verification
fail. Bounded polling is only for analysis completion, not repeated retries to
hide findings. The gate neither accepts issues nor changes scanner exclusions.
It reads GitHub Checks with job-scoped read permission; no Sonar token is needed
or exposed. This gate does not prove that the entire project's historical issue
inventory is zero, and it does not replace code tests or host integration tests.

## Verification boundaries and remaining work

Compiled Common tests cover native return classification, real JSONL/hash code,
redaction and missing observations. Extracted HAProxy evaluation tests cover
phase order, each injected native-call failure, partial resource ownership and
cleanup order, and bounded rule-ID decoding. Separate compatibility tests compile
and link the actual HAProxy binding against controlled native API seams.
NGINX request/file and late-error/re-entry suites exercise selected actual
functions with controlled host/engine/log collaborators. NGINX and HAProxy
adoption mutations guard source wiring; their passing counts are in the checklist.

Those layers do not establish live HTTP behavior, `strict` reset/abort support,
neighbor-stream survival, or equal logs from every direct/companion/middleware/
sidecar route. Unsupported profiles remain unsupported. The mode defaults,
engine-owned MIME selection, independent transport/resource limits and existing
security gates are not weakened. A late abort cannot retract bytes already sent.

Before release, complete the unchecked items in the checklist: typed request
error events and other native/API routes, producer/sink failure handling,
connector guides, compatibility review and real host matrices. Passing the
repaired adoption checks does not finish those separate implementation items.
