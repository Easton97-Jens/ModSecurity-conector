# Refactor Phase 9 Review

Status: implemented

Phase 9 migrates NGINX connector build inputs from the imported upstream source
tree into adapter-owned source while keeping Apache, YAML semantics,
`verified_variables`, and `RESPONSE_BODY` classification unchanged.

## Migrated Files

These files moved from `connectors/nginx/upstream/` to `connectors/nginx/src/`:

| Adapter-owned path | Base source | Extra provenance |
| --- | --- | --- |
| `connectors/nginx/config` | ModSecurity-nginx `config` at `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none |
| `connectors/nginx/src/ngx_http_modsecurity_access.c` | ModSecurity-nginx `src/ngx_http_modsecurity_access.c` | none |
| `connectors/nginx/src/ngx_http_modsecurity_body_filter.c` | ModSecurity-nginx `src/ngx_http_modsecurity_body_filter.c` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | ModSecurity-nginx `src/ngx_http_modsecurity_common.h` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` |
| `connectors/nginx/src/ngx_http_modsecurity_header_filter.c` | ModSecurity-nginx `src/ngx_http_modsecurity_header_filter.c` | none |
| `connectors/nginx/src/ngx_http_modsecurity_log.c` | ModSecurity-nginx `src/ngx_http_modsecurity_log.c` | none |
| `connectors/nginx/src/ngx_http_modsecurity_module.c` | ModSecurity-nginx `src/ngx_http_modsecurity_module.c` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac` |

Phase 10 later removed the retained `connectors/nginx/upstream/` attribution
tree after the build was proven from adapter-owned source and durable
attribution remained in `licenses/nginx/`, `connectors/nginx/ORIGIN.md`, and
`connectors/nginx/SOURCE_MAP.json`.

## PR #377 Intake

PR: https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377

Observed PR head commit: `3d72b004ff27a78ea19c6b945870e2cae62a97ac`

Relevant source changes were applied only to adapter-owned NGINX files:

- body filter phase-4 handling;
- common header fields for phase-4 mode/configuration;
- module directives including `modsecurity_phase4_mode`,
  `modsecurity_phase4_content_types_file`, and `modsecurity_phase4_log`.

Raw PR tests and documentation were not copied into the active smoke suite.

## Build Input

The monorepo-default NGINX source is `connectors/nginx/src`. The build harness
materializes `$BUILD_ROOT/nginx-build/connector-src` from adapter-owned NGINX
`config` and source files plus generated manifests. After Phase 10 the manifest
is expected to contain no NGINX `upstream-derived` entries.

External `MODSECURITY_NGINX_SOURCE_DIR` overrides still use the sanitized
external-source copy path.

## Response-Body Status

This phase does not promote `RESPONSE_BODY`. The PR #377 source changes may
improve NGINX phase-4 behavior, but `RESPONSE_BODY` remains former expected-failure/mapped-only
until a separate evidence phase proves stable Apache and NGINX HTTP behavior
for a common blocking case.

## Deferred

- Apache remains untouched.
- No Common extraction of NGINX hooks, filters, body handling, response-body
  semantics, transaction ownership, or intervention finalization.
- No raw upstream or PR tests are copied.
- No YAML active-case semantics change.

## Validation

The required validation for this phase is:

```sh
REFRESH=1 BUILD_ROOT=/src/ModSecurity-conector-phase9-build make smoke-nginx
BUILD_ROOT=/src/ModSecurity-conector-phase9-build make smoke-all
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-all
BUILD_ROOT=/src/ModSecurity-conector-phase9-build make probe-response-body || true
```

`probe-response-body` is evidence-only and does not affect
`verified_variables`.
