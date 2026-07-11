> Generated capability snapshot — do not edit runtime status manually.

# lighttpd No-CRS Baseline

**Language:** English | [Deutsch](lighttpd-no-crs-baseline.de.md)

Generated on `2026-07-10` from the checked-in `connectors/<name>/capabilities.json` manifests. No canonical No-CRS `result.json` was used because no canonical run had been executed.

Overall canonical status: `NOT EXECUTED`

Host model: `native lighttpd plugin`

| Dimension | Canonical status | Manifest boundary |
|---|---|---|
| Source contract | IMPLEMENTED, NOT ASSERTED | Source, metadata, and host wiring are present |
| Build / link | IMPLEMENTED, NOT ASSERTED | A current canonical build result is absent |
| Config load | IMPLEMENTED, NOT ASSERTED | A current canonical config result is absent |
| Request-free start | IMPLEMENTED, NOT ASSERTED | A current canonical start result is absent |
| Minimal runtime | IMPLEMENTED, NOT ASSERTED | Earlier targeted evidence is not imported into this baseline |
| No-CRS baseline | NOT EXECUTED | No canonical `result.json` exists |
| Phase 1 | IMPLEMENTED, NOT ASSERTED | Capability manifest |
| Phase 2 | NOT IMPLEMENTED | Capability manifest |
| Phase 3 | IMPLEMENTED, NOT ASSERTED | Capability manifest |
| Phase 4 | NOT IMPLEMENTED | Capability manifest |
| Events | IMPLEMENTED, NOT ASSERTED | Metadata-only JSONL must be asserted by a canonical run |
| Lifecycle | IMPLEMENTED, NOT ASSERTED | Cleanup and failure cases require canonical case results |
| Status | NOT EXECUTED | Missing evidence is never inferred as PASS |

## Architecture boundary

Request and response bodies are deliberately not implemented.

The response-header hook exists, but no real Phase-3 rule has behaviorally asserted it.

## Canonical Phase-4 facets

Every response-body and response-phase facet below is `not_implemented` in the
current native module. The absence of a native response-body hook is an
implementation gap, not a proven lighttpd host-model impossibility.

| Facet | Capability state | Consequence for the canonical catalog |
|---|---|---|
| Response body availability (`response_body_buffered`) | `not_implemented` | The native module supplies no response body to ModSecurity. |
| Phase-4 invocation (`phase4`) | `not_implemented` | No real response-body Phase-4 call exists. |
| Rule evaluation (`phase4_rule_evaluation`) | `not_implemented` | Rule `1100301` cannot run against a native response body. |
| Pre-commit denial (`phase4_pre_commit_deny`) | `not_implemented` | No response-body decision point is implemented before commitment. |
| Late intervention (`late_intervention`) | `not_implemented` | No post-commit response-body policy point is implemented. |
| Safe late intervention (`late_intervention_log_only`) | `not_implemented` | No committed response-body denial can be recorded as log-only. |
| Strict late intervention (`late_intervention_abort`) | `not_implemented` | No committed response-body abort action is implemented. |
| Status metadata (`late_intervention_status_metadata`) | `not_implemented` | No Phase-4 event source distinguishes WAF, original, and visible response statuses. |

Phase-4 cases remain `NOT EXECUTED` (or are not selectable) until a real native
response-body implementation exists. They must not be labelled `UNSUPPORTED`
without evidence that lighttpd's host model cannot provide a suitable hook.
Events and reports remain metadata-only; they must not contain a body payload
or match value.

Expected evidence root:

```text
$EVIDENCE_ROOT/lighttpd/<run-id>/
```

## Claims deliberately not made

- production readiness or production hardening
- runtime security or security verification
- CRS verification or CRS completeness
- extended/full-matrix verification
- response-body verification across all connectors
- a canonical No-CRS PASS
