# PR Evidence Summary

Status: implemented

This repository keeps source-derived smoke evidence for ModSecurity connector
compatibility topics. The relevant upstream discussions are:

| Topic | Upstream PR | Repository |
| --- | --- | --- |
| RAW argument collections | https://github.com/owasp-modsecurity/ModSecurity/pull/3564 | https://github.com/owasp-modsecurity/ModSecurity |
| NGINX phase-4 / `RESPONSE_BODY` behavior | https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377 | https://github.com/owasp-modsecurity/ModSecurity-nginx |

## Real-World Connector Path

Connector evidence is counted only when the request travels through:

```text
Client -> Apache/NGINX -> connector module -> libmodsecurity -> rule variables -> HTTP response
```

The connector-free v3 API smoke under `src/v3-api-smoke/` is useful API
evidence, but it is not Apache or NGINX connector proof.

## Currently Verified Variable Families

The active Apache and NGINX smokes currently verify these families through real
connector paths when `make smoke-all` passes:

- `ARGS`
- `ARGS_NAMES`
- `REQUEST_HEADERS`
- `REQUEST_BODY`
- `REQUEST_COOKIES`
- `REQUEST_URI`
- `FILES`
- `XML`
- `AUDIT_LOG`
- `RESPONSE_HEADERS`

`RESPONSE_BODY` is not verified. It remains xfail/mapped-only; see
`../testing/response-body-blocking-investigation.md`.

## PR #377 Source Status

ModSecurity-nginx PR #377 was fetched only under `$BUILD_ROOT` for review.
Observed PR head: `3d72b004ff27a78ea19c6b945870e2cae62a97ac`.

Relevant source changes are applied to adapter-owned NGINX files:

- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_module.c`

The PR source intake is not counted as response-body validation. Active
connector success still requires real HTTP behavior through Apache and NGINX,
and `RESPONSE_BODY` remains absent from `verified_variables`.

Phase 10 added source-derived PR #377 test mapping in
`../testing/pr377-test-import-map.md`. The imported NGINX-only probes cover
minimal/safe/out-of-scope phase-4 log behavior with HTTP 200 pass-through.
Strict aborts, invalid config, large-response, and shared response-body blocking
remain xfail or mapped-only.

## Reproduction

```sh
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-all
BUILD_ROOT=/src/ModSecurity-conector-build make probe-response-body || true
```

Generated build, runtime, log, and result artifacts must stay under
`BUILD_ROOT`.
