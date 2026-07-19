# Apache Planning

**Language:** English | [Deutsch](TODO.de.md)

Status: native Apache module; canonical capability manifest present
Canonical No-CRS status: `supported_not_verified` / `NOT EXECUTED`

Framework catalog and integration guidance is in
`modules/ModSecurity-test-Framework/docs/catalog-and-cases.md` and
`modules/ModSecurity-test-Framework/docs/connector-integration.md`.

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

The checked-in `capabilities.json` is the source contract for the new baseline.
It records the native Phase 1-4 paths as `implemented_not_asserted`; no value is
promoted to `verified` until a current canonical result exists under
`$EVIDENCE_ROOT/apache/<run-id>/`.

- [x] Coverage decision matrix reviewed.
- [x] No local tests folder.
- [x] External framework test paths referenced.
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
- [ ] Legitimate Allow control documented; it must release the one retained
      original brigade only after first EOS and Phase-4 completion.
- [x] Connector status remains `partial` until matrix is complete.
- [ ] `make no-crs-baseline-apache` produces current canonical evidence.
- [ ] `make evidence-check-apache` validates schema, claims, layout, events, and
      capability consistency for that same run.

## Canonical Phase-4 evidence

The source contract declares the response-body and late-intervention facets as
`implemented_not_asserted`, not `verified`.  A historical status-only smoke or
a source inspection cannot promote them.

- [ ] Record `phase4_rule_observed` with rule `1100301` through the real
      Apache output-filter path; a visible 200 is valid for this observation.
- [ ] Record `phase4_deny_before_commit` only when no original response EOS or
      body byte was released and the client receives the requested deny status.
- [ ] Record the safe late case only when independent commit proof already
      exists, with requested `deny`, actual `log_only`, unchanged visible
      status, and late-intervention metadata; it is not normal all-response-
      gate behavior.
- [ ] Record the strict late case only with actual `abort_connection` and
      `connection_aborted=true`.
- [ ] Verify separate original host status, requested WAF status, visible
      client status, requested action, and actual action in a metadata-only
      event.
- [ ] Keep an unavailable current run as `NOT EXECUTED`; never convert a rule
      match, log-only result, or abort into a synthetic 403 `PASS`.
- [ ] Execute `ci/runtime/lifecycle/run-apache-phase4-response-regression.sh`
      for the focused H1/H2 evidence placeholder. Its existence is not an H1
      or H2 pass claim.
