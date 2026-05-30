# Apache Planning

Status: scaffolded

Tracked in `modules/ModSecurity-test-Framework/docs/roadmap/todo-inventory.md`.

- Verify license requirements before importing or adapting any code.
- Validate the PoC Autotools/APXS helper on a host with Apache development
  tools installed.
- Define capability flags for request body, response body, audit log, reload,
  and custom transaction ID.
- Port only proven Apache-specific tests into `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/`.
- Document every reused concept as `connector-specific` or `engine-specific`.
- Turn the minimal smoke harness into a connector-specific regression test only
  after a real HTTP `403` pass is observed.

## Coverage / Runtime Decision Matrix

- [x] Coverage decision matrix reviewed.
- [x] No local tests folder.
- [x] External framework test paths referenced.
- [x] `phase1_header_block` runtime smoke PASS documented.
- [x] Current `/src` `make test-no-crs` PASS documented.
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
