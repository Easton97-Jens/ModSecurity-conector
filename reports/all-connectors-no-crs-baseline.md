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
