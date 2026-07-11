> Generated capability snapshot — do not edit runtime status manually.

# Apache No-CRS Baseline

**Language:** English | [Deutsch](apache-no-crs-baseline.de.md)

Generated on `2026-07-10` from the checked-in `connectors/<name>/capabilities.json` manifests. No canonical No-CRS `result.json` was used because no canonical run had been executed.

Overall canonical status: `NOT EXECUTED`

Host model: `native Apache httpd module`

| Dimension | Canonical status | Manifest boundary |
|---|---|---|
| Source contract | IMPLEMENTED, NOT ASSERTED | Source, metadata, and host wiring are present |
| Build / link | IMPLEMENTED, NOT ASSERTED | A current canonical build result is absent |
| Config load | IMPLEMENTED, NOT ASSERTED | A current canonical config result is absent |
| Request-free start | IMPLEMENTED, NOT ASSERTED | A current canonical start result is absent |
| Minimal runtime | IMPLEMENTED, NOT ASSERTED | Earlier targeted evidence is not imported into this baseline |
| No-CRS baseline | NOT EXECUTED | No canonical `result.json` exists |
| Phase 1 | IMPLEMENTED, NOT ASSERTED | Capability manifest |
| Phase 2 | IMPLEMENTED, NOT ASSERTED | Capability manifest |
| Phase 3 | IMPLEMENTED, NOT ASSERTED | Capability manifest |
| Phase 4 | IMPLEMENTED, NOT ASSERTED | Capability manifest |
| Events | IMPLEMENTED, NOT ASSERTED | Metadata-only JSONL must be asserted by a canonical run |
| Lifecycle | IMPLEMENTED, NOT ASSERTED | Cleanup and failure cases require canonical case results |
| Status | NOT EXECUTED | Missing evidence is never inferred as PASS |

## Architecture boundary

Buffered request and response paths are implemented; streaming paths and drop are not implemented.

Phase-4 intervention timing depends on whether Apache has committed the response.

## Canonical Phase-4 facets

The response-body path and every response-phase facet below are
`implemented_not_asserted`. This is a source-and-wiring declaration, not a
Phase-4 `PASS`: no current canonical real-host run has observed rule `1100301`,
a pre-commit denial, or either late-intervention action.

| Facet | Capability state | Required runtime evidence before it can be asserted |
|---|---|---|
| Response body availability (`response_body_buffered`) | `implemented_not_asserted` | A bounded Apache output-filter path is wired; no current canonical real-host evidence proves that it processed a response body. |
| Phase-4 invocation (`phase4`) | `implemented_not_asserted` | The response-body Phase-4 call is wired; no current canonical real-host evidence proves its invocation. |
| Rule evaluation (`phase4_rule_evaluation`) | `implemented_not_asserted` | The output-filter Phase-4 path is present; no current canonical real-host evidence proves that it evaluated rule `1100301`. |
| Pre-commit denial (`phase4_pre_commit_deny`) | `not_implemented` | The response-body decision finalizes at EOS after the header path; the host has no deterministic uncommitted body decision point and does not claim a visible Phase-4 `403`. |
| Late intervention (`late_intervention`) | `implemented_not_asserted` | Late-intervention policy branches are wired; no current canonical real-host evidence proves a disruptive decision after commitment. |
| Safe late intervention (`late_intervention_log_only`) | `implemented_not_asserted` | A safe log-only branch is wired; no current canonical real-host evidence proves `actual_action=log_only` with an unchanged visible status. |
| Strict late intervention (`late_intervention_abort`) | `implemented_not_asserted` | A strict abort branch is wired; no current canonical real-host evidence proves `actual_action=abort_connection` and `connection_aborted=true`. |
| Status metadata (`late_intervention_status_metadata`) | `implemented_not_asserted` | Phase-4 metadata wiring exists; no current canonical event proves separate requested WAF, original host, and visible client statuses or requested and actual actions. |

The shared catalog keeps rule observation separate from transport behavior:
`phase4_rule_observed` does not require a visible `403`; a pre-commit denial
does. After commitment, a `log_only` result may correctly leave a `200` visible,
and an abort does not imply that a client can observe `403`. No body payload or
match value belongs in the event or this report.

Expected evidence root:

```text
$EVIDENCE_ROOT/apache/<run-id>/
```

## Claims deliberately not made

- production readiness or production hardening
- runtime security or security verification
- CRS verification or CRS completeness
- extended/full-matrix verification
- response-body verification across all connectors
- a canonical No-CRS PASS
