# NGINX Architecture

**Language:** English | [Deutsch](architecture.de.md)

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
- Build and smoke flow: `docs/build/compilers/nginx.md`.
- Generated detail report:
  `reports/testing/generated/nginx-runtime-results.generated.md`.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.

## Boundaries

The shared `common/` layer may contain directive names, option defaults, and
data shapes. It does not own NGINX phases, filters, request body handling,
response body handling, transaction ownership, or server lifecycle behavior.

## Common SDK adoption layer

The NGINX architecture keeps NGINX API handling local while moving shared
semantics into the Common SDK. Location configuration embeds `msconnector_config`,
NGINX directive registrations use Common directive macros/spec/adapters, and thin
mapper functions convert `ngx_http_request_t` plus response state into
`msconnector_request`/`msconnector_response` under Common mapper contracts. Body
payloads are not emitted in events, JSONL, or logs; only metadata such as sizes
and truncation state may be represented. C17 compile checks cover this adoption
surface when NGINX/libmodsecurity headers exist, while C23/future-C checks are
optional and compiler-dependent. These checks are compile/structure evidence only.
