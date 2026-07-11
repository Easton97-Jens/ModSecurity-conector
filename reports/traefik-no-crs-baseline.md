> Generated capability snapshot — do not edit runtime status manually.

# Traefik No-CRS Baseline

**Language:** English | [Deutsch](traefik-no-crs-baseline.de.md)

Generated on `2026-07-10` from the checked-in `connectors/<name>/capabilities.json` manifests. No canonical No-CRS `result.json` was used because no canonical run had been executed.

Overall canonical status: `NOT EXECUTED`

Host model: `HTTP forwardAuth service`

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
| Phase 3 | UNSUPPORTED | Capability manifest |
| Phase 4 | UNSUPPORTED | Capability manifest |
| Events | IMPLEMENTED, NOT ASSERTED | Metadata-only JSONL must be asserted by a canonical run |
| Lifecycle | IMPLEMENTED, NOT ASSERTED | Cleanup and failure cases require canonical case results |
| Status | NOT EXECUTED | Missing evidence is never inferred as PASS |

## Architecture boundary

Traefik can buffer forwardAuth bodies, but the selected native configuration does not enable forwardBody and uses request_body_mode=none.

The pre-upstream forwardAuth model cannot observe the later upstream response.

## Canonical Phase-4 facets

Every response-phase facet below is `unsupported_by_host_model`. The selected
Traefik `forwardAuth` integration runs before upstream handling and cannot
inspect the later upstream response body. This is an architectural boundary of
this integration, not missing run evidence.

| Facet | Capability state | Consequence for the canonical catalog |
|---|---|---|
| Response body availability (`response_body_buffered`) | `unsupported_by_host_model` | The authorization call has no later upstream response body to inspect. |
| Phase-4 invocation (`phase4`) | `unsupported_by_host_model` | A response-body Phase-4 call cannot occur through this path. |
| Rule evaluation (`phase4_rule_evaluation`) | `unsupported_by_host_model` | Rule `1100301` cannot be observed in a later upstream response. |
| Pre-commit denial (`phase4_pre_commit_deny`) | `unsupported_by_host_model` | This path has no response-phase point at which to alter an upstream response. |
| Late intervention (`late_intervention`) | `unsupported_by_host_model` | The authorization decision finishes before the upstream response begins. |
| Safe late intervention (`late_intervention_log_only`) | `unsupported_by_host_model` | No committed upstream response is available to record as log-only. |
| Strict late intervention (`late_intervention_abort`) | `unsupported_by_host_model` | The service cannot abort Traefik's later downstream response as a Phase-4 action. |
| Status metadata (`late_intervention_status_metadata`) | `unsupported_by_host_model` | There is no response-phase event from which to distinguish WAF, original, and visible response statuses. |

All Phase-4 cases must therefore be reported as `UNSUPPORTED`, never as `PASS`
or `NOT EXECUTED`. A different future Traefik integration is outside this
evidence scope. Events and reports remain metadata-only; they must not contain
a body payload or match value.

Expected evidence root:

```text
$EVIDENCE_ROOT/traefik/<run-id>/
```

## Claims deliberately not made

- production readiness or production hardening
- runtime security or security verification
- CRS verification or CRS completeness
- extended/full-matrix verification
- response-body verification across all connectors
- a canonical No-CRS PASS
