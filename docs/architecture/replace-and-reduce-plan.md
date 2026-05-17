# Replace-And-Reduce Plan

Status: phase 5 reviewed

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

## Phase 5 Review

Phase 5 searched for one additional low-risk replacement. No second candidate
met the replacement rule: every remaining helper is either embedded in a
production request/response path, tied to server-specific config/lifecycle, or
requires editing an imported source file without a functional replacement need.

| Candidate | Risk | Dependencies | Runtime impact | Build impact | Test coverage | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| Apache `id()` helper in `src/msc_utils.c/.h` | Low as code, but unsafe as a replace target because removal edits an imported source/header pair that also owns Apache error-bucket declarations. | C stdio/varargs and `msc_utils.h`; no callers were found outside its own declaration/definition. | No known runtime use. Removing it would not replace behavior; it would only mutate upstream reference code. | Apache build may tolerate removal, but proof would require editing imported files directly. | No meaningful smoke coverage because the helper is unused. | obsolete / defer |
| Apache `send_error_bucket()` in `src/msc_utils.c` | High. It creates Apache buckets, sets status line, inserts EOS, and passes the brigade down the output filter chain. | Apache request/filter/bucket APIs and `msc_filters.c` error paths. | Direct Apache response/error semantics. | Required by `msc_filters.c`; removal requires a repo-owned Apache adapter implementation. | Blocking smokes cover symptoms, not every Apache output-filter edge. | defer |
| NGINX `ngx_str_to_char()` in `src/ngx_http_modsecurity_module.c` | Medium to high. It is small, but used by config parsing and request metadata mapping. | NGINX pools, `ngx_str_t`, allocation failure sentinel, config and access handler callers. | Request metadata and configuration value conversion. | Exposed in `ngx_http_modsecurity_common.h` and used across multiple module sources. | Active smokes cover common request metadata, but not all allocation/config edge cases. | defer |
| NGINX PCRE pool helpers in `src/ngx_http_modsecurity_module.c` | High. They temporarily replace PCRE allocators around ruleset loading. | NGINX pool lifecycle, PCRE global allocator hooks, rules/config loading. | Config/lifecycle behavior rather than request data path, but failure could destabilize rules loading. | Required by module config initialization. | Build and smoke prove ordinary rules load, not allocator edge cases. | defer |
| NGINX response-header resolver helpers in `src/ngx_http_modsecurity_header_filter.c` | High. They normalize response headers for libmodsecurity. | NGINX header filter API, response header structs, filter order. | Direct response metadata/filter path. | Required by the NGINX header filter source. | `response_header_basic` covers one real path; not enough to replace all resolver behavior. | defer |
| NGINX log callback in `src/ngx_http_modsecurity_log.c` | Medium to high. Audit/log behavior is evidence-sensitive and `nolog` remains xfail. | NGINX logging, libmodsecurity log callback, transaction context. | Audit/log output semantics. | Required by log handler source. | Stable audit field smokes exist, but audit absence differs across environments. | defer |

The phase-5 outcome is therefore a documented hold. The next replacement should
begin only after a repo-owned adapter file exists for one narrow behavior and
before/after real-world smokes prove equivalence.
