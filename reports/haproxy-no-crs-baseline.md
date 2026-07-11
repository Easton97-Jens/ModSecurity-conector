> Generated capability snapshot — do not edit runtime status manually.

# HAProxy No-CRS Baseline

**Language:** English | [Deutsch](haproxy-no-crs-baseline.de.md)

Generated on `2026-07-11` from the checked-in `connectors/<name>/capabilities.json` manifests. No canonical No-CRS `result.json` was used because no canonical run had been executed.

Overall canonical status: `NOT EXECUTED`

Host model: `HAProxy SPOE/SPOP agent`

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
| Phase 4 | NOT IMPLEMENTED | Selected SPOP path has no response-body route |
| Events | IMPLEMENTED, NOT ASSERTED | Metadata-only JSONL must be asserted by a canonical run |
| Lifecycle | IMPLEMENTED, NOT ASSERTED | Cleanup and failure cases require canonical case results |
| Status | NOT EXECUTED | Missing evidence is never inferred as PASS |

## Architecture boundary

The selected SPOP path has a bounded request sample but no response-body route;
streaming, drop, and abort decisions are not implemented. An optional HAProxy
3.2.21 HTX observer source exists separately, but it is nonselected,
bodyless-request-only, and not canonical evidence.

Host and agent are separate processes and require distinct logs in one manifest.

## Canonical Phase-4 facets

The selected SPOP response-body path, `phase4`, and
`phase4_rule_evaluation` are `not_implemented`. The optional HTX observer
source is not selected by this host model, bypasses body-bearing requests, and
is not canonical Phase-4 runtime evidence. No current canonical HAProxy host
run has observed rule `1100301`. The semantic pre-commit, late-action, and
status-metadata facets are `not_implemented` because the runner observes no
client-visible response outcome, actual commitment timing, or post-commit host
point.

| Facet | Capability state | Required runtime evidence before it can be asserted |
|---|---|---|
| Response body availability (`response_body_buffered`) | `not_implemented` | The selected SPOP path has no response-body delivery; the optional HTX observer is nonselected and bodyless-request-only. |
| Phase-4 invocation (`phase4`) | `not_implemented` | No selected SPOP response-body/EOS path exists; the optional HTX observer does not promote this state. |
| Rule evaluation (`phase4_rule_evaluation`) | `not_implemented` | No selected SPOP response-body path exists; no canonical HAProxy host evidence proves rule `1100301`. |
| Pre-commit denial (`phase4_pre_commit_deny`) | `not_implemented` | The agent emits policy-derived fields, but no host runner observes visible client status and actual commitment timing. |
| Late intervention (`late_intervention`) | `not_implemented` | The current response-decision path is modeled before commitment and has no post-commit host point. |
| Safe late intervention (`late_intervention_log_only`) | `not_implemented` | No post-commit safe `log_only` action or host-observed unchanged-visible-status result exists. |
| Strict late intervention (`late_intervention_abort`) | `not_implemented` | No controlled post-commit `abort_connection` action or host-observed connection-abort result exists. |
| Status metadata (`late_intervention_status_metadata`) | `not_implemented` | Policy-derived diagnostics do not supply host-observed original/visible status and timing. |

The shared catalog keeps rule observation separate from transport behavior:
`phase4_rule_observed` does not require a visible `403`. HAProxy does not yet
implement the semantic pre-commit, post-commit `log_only`, post-commit abort,
or status-metadata cases, so they remain `NOT_EXECUTED`. No body payload or
match value belongs in the event or this report.

Expected evidence root:

```text
$EVIDENCE_ROOT/haproxy/<run-id>/
```

## Claims deliberately not made

- production readiness or production hardening
- runtime security or security verification
- CRS verification or CRS completeness
- extended/full-matrix verification
- response-body verification across all connectors
- a canonical No-CRS PASS
