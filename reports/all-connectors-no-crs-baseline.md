> Generated capability snapshot — do not edit runtime status manually.

# All Connector No-CRS Baseline

**Language:** English | [Deutsch](all-connectors-no-crs-baseline.de.md)

Generated on `2026-07-10` from the checked-in `connectors/<name>/capabilities.json` manifests. No canonical No-CRS `result.json` was used because no canonical run had been executed.

Overall canonical status: `NOT EXECUTED`

| Connector | Build | Config | Start | Minimal runtime | No-CRS baseline | P1 | P2 | P3 | P4 | Events | Lifecycle | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Apache | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| NGINX | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| HAProxy | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| Envoy | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | UNSUPPORTED | UNSUPPORTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| Traefik | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | NOT IMPLEMENTED | UNSUPPORTED | UNSUPPORTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |
| lighttpd | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED | IMPLEMENTED, NOT ASSERTED | NOT IMPLEMENTED | IMPLEMENTED, NOT ASSERTED | NOT IMPLEMENTED | IMPLEMENTED, NOT ASSERTED | IMPLEMENTED, NOT ASSERTED | NOT EXECUTED |

## Interpretation

`IMPLEMENTED, NOT ASSERTED` is a source/capability statement, not runtime PASS.
`UNSUPPORTED` is an honest host-model boundary and is not counted as PASS or
FAIL. `NOT IMPLEMENTED` is a connector gap. `NOT EXECUTED` means that no
canonical result exists.

- Envoy Phase 2 is configured but not exercised.
- Envoy and Traefik cannot observe the later upstream response in the selected authorization models.
- Traefik Phase 2 is not implemented in the selected native configuration.
- lighttpd Phase 3 is implemented but not behaviorally asserted.
- lighttpd request and response bodies are not implemented.
- Legacy smoke, body, CRS, bridge, sidecar, and self-test results are excluded.

## Canonical Phase-4 facets and case outcomes

The following are capability states, not results from the absent canonical run.
They separate response-body availability, rule evaluation, pre-commit denial,
late intervention, and status metadata instead of treating every Phase-4 match
as a visible HTTP `403`.

| Connector | `response_body_buffered` | `phase4` | `phase4_rule_evaluation` | `phase4_pre_commit_deny` |
|---|---|---|---|---|
| Apache | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| NGINX | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| HAProxy | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| Envoy | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` |
| Traefik | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` |
| lighttpd | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |

| Connector | `late_intervention` | `late_intervention_log_only` | `late_intervention_abort` | `late_intervention_status_metadata` |
|---|---|---|---|---|
| Apache | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| NGINX | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| HAProxy | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| Envoy | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` |
| Traefik | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` | `unsupported_by_host_model` |
| lighttpd | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |

`implemented_not_asserted` makes a capability eligible for capability-driven
case selection; it does not make it PASS. With no current run, Apache, NGINX,
and HAProxy have no Phase-4 PASS result in this snapshot. HAProxy's selected
SPOP path has no response-body/Phase-4/rule-observation facets. Its optional
HTX observer source is nonselected, bodyless-request-only, and does not promote
the capability table; the Phase-4 and semantic cases are `NOT_EXECUTED`
because the runner has no host-observed client outcome, commitment timing, or
post-commit point. Envoy and Traefik must report response-phase cases as
`UNSUPPORTED`: their selected `ext_authz` and `forwardAuth` integrations execute
before the upstream response and cannot inspect its body. lighttpd
response-phase cases are `NOT EXECUTED`, not `UNSUPPORTED`, because the current
native module lacks the implementation but there is no demonstrated host-model
impossibility.

The shared cases are `phase4_rule_observed`, `phase4_deny_before_commit`,
`phase4_deny_after_commit_log_only`, `phase4_deny_after_commit_abort`,
`phase4_event_contains_original_status`, and
`phase4_event_contains_late_intervention_action`. The deprecated
`deny_response_body_marker_403` alias may PASS only through the pre-commit
denial case; it must not turn a log-only or abort outcome into a `403` PASS.

For a real Phase-4 result, `http_status` is the WAF-requested status,
`original_http_status` is the status before intervention, and
`visible_http_status` is what the client can observe. `requested_action` and
`actual_action` must likewise remain distinct. `headers_sent`, `body_started`,
`response_committed`, `late_intervention`, `connection_aborted`, and (when
available) `transport_result` describe timing and transport without inventing
an HTTP status. A safe late intervention can therefore PASS with a visible
`200` and `actual_action=log_only`; a strict abort does not require a visible
`403`.

The common late-intervention policy is: before commitment,
`DENY_IF_POSSIBLE`; after commitment in normal or safe mode, `LOG_ONLY`; after
commitment in strict mode, `ABORT_CONNECTION`. Events, case results, manifests,
and reports may contain only metadata, never request/response-body payloads,
match values, rule messages, or intervention logs.

## Expected canonical evidence

Each connector run writes to
`$EVIDENCE_ROOT/<connector>/<run-id>/`. The aggregate may read only the six
canonical `result.json` files. Missing or ambiguous files must remain
`NOT EXECUTED` or error; they cannot become PASS.

## Claims deliberately not made

- production readiness or production hardening
- runtime security or security verification
- CRS verification or CRS completeness
- extended/full-matrix verification
- response-body verification across all connectors
- all connectors fully verified
