# NGINX Planning

Status: native NGINX module; canonical capability manifest present
Canonical No-CRS status: `supported_not_verified` / `NOT EXECUTED`

Tracked in `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`.

- Verify license requirements before importing or adapting any code.
- Decide dynamic vs static module build strategy.
- Define capability flags for request body, response body, HTTP/2, audit log,
  reload, and custom transaction ID.
- Keep nginx-tests-derived cases in `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`.
- Document filter ordering before implementation.

## Coverage / Runtime Decision Matrix

The checked-in `capabilities.json` is the source contract for the new baseline.
It records the native Phase 1-4 paths as `implemented_not_asserted`; no value is
promoted to `verified` until a current canonical result exists under
`$EVIDENCE_ROOT/nginx/<run-id>/`.

- [x] Coverage decision matrix reviewed.
- [x] No local tests folder.
- [x] External framework test paths referenced.
- [x] `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include` build contract documented.
- [x] Legacy `phase1_header_block` runtime smoke evidence documented.
- [x] Legacy `/src` `make test-no-crs` result documented; it is not the
      canonical No-CRS baseline introduced by this branch.
- [ ] Current `/src` `make test-with-crs` PASS documented; current result is
      FAIL because `action_status_401_phase1_block` expected 401 and observed
      403.
- [x] Current `/src` With-CRS `crs_sqli_anomaly_block` PASS documented.
- [ ] Phase 1 runtime evidence documented for more than the current smoke case.
- [ ] Phase 2 request-body runtime evidence documented.
- [ ] Phase 3 response-header runtime evidence documented.
- [ ] Phase 4 response-body runtime evidence documented.
- [ ] RESPONSE_BODY blocking verified.
- [ ] Audit/log evidence documented.
- [ ] Negative/pass-through case documented.
- [x] Connector status remains `partial` until matrix is complete.
- [ ] `make no-crs-baseline-nginx` produces current canonical evidence.
- [ ] `make evidence-check-nginx` validates schema, claims, layout, events, and
      capability consistency for that same run.
