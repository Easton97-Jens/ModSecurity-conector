# NGINX Architecture

Status: adapter-owned runtime path, evidence-scoped

The NGINX connector is an NGINX HTTP dynamic module using libmodsecurity v3
public C APIs. Productive source lives under `connectors/nginx/src/`; module
build metadata lives in `connectors/nginx/config`.

## Runtime Shape

```text
HTTP client -> source-built NGINX -> ngx_http_modsecurity_module.so -> libmodsecurity -> HTTP response
```

NGINX owns server-specific behavior:

- access phase handler
- log phase handler
- header filter
- body filter
- main and location configuration create/merge
- dynamic-module build and loading
- bounded Phase 4 strict-abort evidence

These surfaces are not connector-neutral and must remain under
`connectors/nginx/`.

## Current Evidence

- Default runtime smoke: `60/60 PASS`.
- Force-all runtime evidence: `140 attempted / 95 PASS / 39 FAIL /
  0 BLOCKED / 6 NOT_EXECUTABLE`.
- Build and smoke flow: `COMPILE_NGINX.md`.
- Generated detail report:
  `reports/testing/generated/nginx-runtime-results.generated.md`.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.

## Boundaries

The shared `common/` layer may contain directive names, option defaults, and
data shapes. It does not own NGINX phases, filters, request body handling,
response body handling, transaction ownership, or server lifecycle behavior.
