# NGINX Planning

**Language:** English | [Deutsch](TODO.de.md)

Status: native NGINX module; canonical capability manifest present
Canonical No-CRS status: `supported_not_verified` / `NOT EXECUTED`

Framework catalog and integration guidance is in
`modules/ModSecurity-test-Framework/docs/catalog-and-cases.md` and
`modules/ModSecurity-test-Framework/docs/connector-integration.md`.

- Verify license requirements before importing or adapting any code.
- Decide dynamic vs static module build strategy.
- Define capability flags for request body, response body, HTTP/2, audit log,
  reload, and custom transaction ID.
- Keep nginx-tests-derived cases in `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`.
- Document filter ordering before implementation.

## Coverage / Runtime Decision Matrix

The checked-in `capabilities.json` is the source contract for the new baseline.
It records the native Phase 1-4 paths as `implemented_not_asserted`, except
for `phase4_pre_commit_deny`, which is `not_implemented` because the body
filter runs after the response-header path. No value is promoted to `verified`
until a current canonical result exists under
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
- [x] Inspect the current pinned host for an applicable HTTP/2 lane: its
      `nginx -V` configuration has no `--with-http_v2_module`, so no HTTP/2
      lifecycle case is executed or claimed for that host build.
- [ ] RESPONSE_BODY blocking verified.
- [ ] Audit/log evidence documented.
- [ ] Negative/pass-through case documented.
- [x] Connector status remains `partial` until matrix is complete.
- [ ] `make no-crs-baseline-nginx` produces current canonical evidence.
- [ ] `make evidence-check-nginx` validates schema, claims, layout, events, and
      capability consistency for that same run.

## Canonical Phase-4 evidence

The source contract keeps the executable response-body and late-intervention
facets at `implemented_not_asserted` until one current canonical NGINX host
run proves each behavior separately. `phase4_pre_commit_deny` is explicitly
`not_implemented`: the native body filter has no pre-header response-body
decision point.

- [ ] Record `phase4_rule_observed` with rule `1100301`; a rule observation
      must not be rewritten as a visible 403 requirement.
- [x] Keep `phase4_deny_before_commit` out of the NGINX runner selection: the
      Phase-4 body-filter timing cannot establish an uncommitted response.
- [ ] Verify safe post-commit behavior as requested `deny`, actual `log_only`,
      unchanged visible status, and `late_intervention=true`.
- [ ] Verify strict post-commit behavior as actual `abort_connection` with
      `connection_aborted=true`; a prior client status may remain visible.
- [ ] Verify metadata-only events with original host status, requested WAF
      status, visible client status, requested action, and actual action.
- [ ] Preserve `NOT EXECUTED` when a current canonical run is absent; do not
      infer `PASS` from filter wiring or from a Phase-4 rule ID.
