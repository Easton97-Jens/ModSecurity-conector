# HAProxy Build Status

The complete repository-supported HAProxy compile and local verification flow
is documented in the root guide:

- [`COMPILE_HAPROXY.md`](../../../COMPILE_HAPROXY.md)

This connector-local page records connector-specific status only. It should not
duplicate the full root compile guide.

## Current Status

- Build status: local request-side runtime build available.
- Runtime status: partial live request-side YAML evidence.
- CRS verified: scoped to live With-CRS `crs_sqli_anomaly_block`.
- RESPONSE_BODY: not verified.
- Full matrix: partial / not fully verified.

## What Exists

- repo-owned HAProxy metadata
- local SPOA agent starter
- request-side SPOP runtime subset
- local libmodsecurity binding self-tests
- framework-owned HAProxy runtime smoke and matrix generation

## What Is Not Claimed

- productive HAProxy adapter ownership
- complete production SPOE/SPOA protocol implementation
- response phase execution
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

Current counts:

- No-CRS: 46 PASS, 0 FAIL, 8 BLOCKED.
- With-CRS: 48 PASS, 0 FAIL, 7 BLOCKED.

The verified request-side variables are `REQUEST_URI`, `REQUEST_HEADERS`,
`REQUEST_HEADERS_NAMES`, `ARGS`, `ARGS_NAMES`, `REQUEST_COOKIES`,
`REQUEST_COOKIES_NAMES`, `REQUEST_BODY`, `FILES`, and `XML`.
