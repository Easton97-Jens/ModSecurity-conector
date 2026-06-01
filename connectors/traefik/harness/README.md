# Traefik Harness

Status: contract only
Runtime status: not-verified

A Traefik runtime harness is not implemented. The metadata build starter and
local decision-service starter do not start Traefik and do not execute framework
YAML cases.

Current local self-test:

- `make -C connectors/traefik self-test-decision-service`

The self-test covers only in-memory allow/block decision logic. It does not
prove a Traefik `forwardAuth` deployment, HTTP service behavior, CRS execution,
libmodsecurity integration, or Traefik traffic handling.

Future harness work must document:

- Traefik binary, container, or source-build used by the harness
- Traefik configuration file
- selected ModSecurity integration point
- `forwardAuth`, plugin, middleware, sidecar, or custom-module configuration if
  that path is selected
- decision-service endpoint if an external decision service is selected
- evidence paths written by the harness
- result JSON path
- PASS/FAIL/BLOCKED counts
- No-CRS and With-CRS separation
- RESPONSE_BODY, negative/pass-through, and audit/log evidence when evaluated

No Traefik runtime result is claimed here.
