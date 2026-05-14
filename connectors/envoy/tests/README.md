# Envoy Connector Tests

Status: scaffolded

Envoy-specific tests belong here.

Tests that depend on Envoy filter ordering, ext_authz configuration, route
cache behavior, Wasm runtime, or Envoy logs must not be placed in
`tests/common/`.
