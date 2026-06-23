# Envoy ext_authz Example

## Table of Contents

- [Status](#status)
- [Needed Components](#needed-components)
- [Config Files](#config-files)
- [Start / Reload Notes](#start-reload-notes)
- [Logs](#logs)
- [Non-Claims](#non-claims)
- [Related Compile Doc](#related-compile-doc)

## Status

Example only. This does not prove production readiness. The repository prepares a pinned Envoy runtime component and exercises an `ext_authz` smoke path when the required local runtime components exist. Envoy is not compiled from source by this repository.

## Needed Components

- Pinned Envoy binary staged by `make prepare-envoy-runtime`.
- An `ext_authz` authorization service or sidecar path.
- libmodsecurity when `DECISION_BACKEND=libmodsecurity` is used.
- ModSecurity rules and optional CRS when a CRS smoke is used.

## Config Files

- `envoy-ext-authz.yaml`: illustrative Envoy listener, route, and `ext_authz` filter wiring.

## Start / Reload Notes

Validate the config with the staged Envoy binary before running it. Restart or hot-restart Envoy according to the operator's process manager after static config changes. Restart the authorization service after rule, library, or backend changes.

## Logs

Use Envoy access/runtime logs plus authorization-service decision and audit logs. Paths in this directory are illustrative and should be replaced by deployment-local paths.

## Non-Claims

- Not production-ready proof.
- Not full matrix proof.
- Not CRS-complete proof.
- Not response-body verification.
- Not an Envoy source-build recipe.

## Related Compile Doc

See [COMPILE_ENVOY.md](../../COMPILE_ENVOY.md).
