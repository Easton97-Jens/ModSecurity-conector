# HAProxy Build Status

The complete repository-supported HAProxy compile and local verification flow
is documented in the root guide:

- [`COMPILE_HAPROXY.md`](../../../COMPILE_HAPROXY.md)

This connector-local page records connector-specific status only. It should not
duplicate the full root compile guide.

## Current Status

- Build status: local diagnostic build available.
- Runtime status: partial runtime-smoke evidence for
  `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`.
- CRS verified: scoped only to `haproxy_crs_sqli_anomaly_block`.
- RESPONSE_BODY: not verified.
- Full matrix: partial / not fully verified.

## What Exists

- repo-owned HAProxy metadata
- local SPOA agent starter
- minimal diagnostic SPOP handshake subset
- local libmodsecurity binding self-tests
- framework-owned HAProxy runtime smoke and matrix writers

## What Is Not Claimed

- productive HAProxy adapter ownership
- complete SPOE/SPOA protocol implementation
- broad No-CRS YAML execution
- broad With-CRS YAML execution
- RESPONSE_BODY blocking
- audit/log coverage
- full-matrix promotion

## Evidence

Use the root compile guide for commands. Current evidence is written under
`/src/ModSecurity-conector-build/results/` and summarized in:

- `/src/ModSecurity-conector-build/results/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`
