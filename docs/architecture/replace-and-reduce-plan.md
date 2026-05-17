# Replace-And-Reduce Plan

Status: phase 4 started

This plan records candidates for replacing small imported connector source
pieces with repo-owned code. A replacement is allowed only when it avoids
server hook/filter/body/lifecycle semantics and keeps real-world smokes passing.

## Candidate Decisions

| Candidate | Source | Risk | Smoke coverage | Replacement strategy | Decision |
| --- | --- | --- | --- | --- | --- |
| NGINX debug compatibility macros | `connectors/nginx/upstream/src/ddebug.h` | Low. The default behavior is no-op debug macros; it is listed as a build dependency but does not own request, response, transaction, or body semantics. | NGINX module compile plus full Apache/NGINX `smoke-all`; debug-enabled builds remain a future explicit probe. | Add repo-owned `connectors/nginx/src/ddebug.h`, copy it into the generated NGINX connector build tree only when the copied source lacks `src/ddebug.h`, then remove the imported upstream copy. | replace now |
| Apache error bucket helper | `connectors/apache/upstream/src/msc_utils.c` `send_error_bucket()` | High. It creates Apache buckets, sets status line, and affects filter-chain response behavior. | Covered indirectly by blocking smokes, but replacement would touch Apache output semantics. | Keep upstream. Revisit only with a dedicated Apache adapter plan and before/after response/error smoke evidence. | defer |
| Apache `id()` helper | `connectors/apache/upstream/src/msc_utils.c` | Low code risk but no functional replacement need; removal requires editing upstream C file. | Not meaningfully covered because it appears unused. | Leave as imported reference for now. Consider removing only when Apache sources are moved out of upstream into repo-owned adapter code. | defer / possibly obsolete |
| Apache intervention handling | `connectors/apache/upstream/src/mod_security3.c` | High. Translates libmodsecurity intervention into Apache HTTP behavior and redirects. | Covered by many 403/401/302 smokes, but behavior is production path. | Document only. Extract data shape is already represented by Common metadata helpers. | defer |
| NGINX intervention handling | `connectors/nginx/upstream/src/ngx_http_modsecurity_module.c` | High. Tied to NGINX request finalization, redirect headers, early logging, and status updates. | Covered by many blocking/redirect smokes, but behavior is production path. | Document only. No replace until a dedicated NGINX adapter design exists. | defer |
| NGINX log callback | `connectors/nginx/upstream/src/ngx_http_modsecurity_log.c` | Medium to high. Connector-specific log phase and audit behavior are still under active evidence tracking. | Audit-log smokes cover stable fields, but `nolog` remains xfail. | Keep upstream. | defer |
| Rules/config loading | Apache `src/msc_config.*`, NGINX `src/ngx_http_modsecurity_module.c` | High. Server-specific configuration parsing and libmodsecurity ruleset ownership. | Build and smoke setup depend on it. | Keep connector-specific. | defer |
| Request/response filters | Apache filters, NGINX access/header/body filters | High. Directly owns connector data path and `RESPONSE_BODY` remains xfail/mapped-only. | Real-world smokes cover active variables, but phase-4 response-body blocking is not stable common PASS. | Keep upstream. | defer |

## Phase 4 Replacement

The only phase-4 replacement is the NGINX debug compatibility header. The
repo-owned header is adapter-near, not Common C. It exists to reduce imported
reference surface without touching connector runtime behavior.

The build script copies the repo-owned header into `$BUILD_ROOT` only when the
selected NGINX connector source tree does not already provide `src/ddebug.h`.
That keeps explicit external `MODSECURITY_NGINX_SOURCE_DIR` builds compatible
with their own upstream header.
