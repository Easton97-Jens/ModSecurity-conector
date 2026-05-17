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

## Reproduction

```sh
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-all
BUILD_ROOT=/src/ModSecurity-conector-build make probe-response-body || true
```

Generated build, runtime, log, and result artifacts must stay under
`BUILD_ROOT`.
