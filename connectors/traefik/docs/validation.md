# Traefik Validation

Status: decision-service-starter
Runtime status: not-verified

Traefik runtime validation has not been run. Global validation gates and status
vocabulary are defined in
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md` and
`connectors/_template/docs/coverage-decision-matrix.md`.

## Current Traefik Evidence

- Metadata build starter: PASS for metadata compile smoke.
- Decision-service starter build: PASS for local compile smoke.
- Decision-service self-test: PASS for in-memory allow/block decisions.
- No-CRS: not run.
- With-CRS: not run.
- RESPONSE_BODY: not verified.
- Negative/pass-through: not verified.
- Audit/log: not verified.

Framework-owned paths and targets for future validation:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

The local decision-service self-test is not a framework runtime result and is
not evidence of Traefik `forwardAuth`, CRS, or libmodsecurity behavior. Traefik
cannot be promoted beyond decision-service-starter without connector-specific
runtime evidence.
