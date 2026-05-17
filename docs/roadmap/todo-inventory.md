# TODO Inventory

Status: implemented

This inventory tracks actionable work markers and status-labelled planning
entries. It intentionally excludes runtime status strings such as shell
`blocked()` functions, JSON counters, and ordinary result vocabulary.

## Summary

| Category | Count | Notes |
| --- | ---: | --- |
| Owned open/planned items | 23 | Common, schema, normalizer, connector, and future-connector planning |
| Owned xfail/mapped evidence | 4 | `RESPONSE_BODY`, `v3_action_nolog_pass_no_audit`, RAW-ARGS, response-body pass-through caveat |
| Resolved owned items | 1 | Common metadata helper implementations added in Refactor Phase 3 |
| Imported upstream markers | 20 | Kept untouched under `connectors/*/upstream/` and classified as upstream-reference |
| Obsolete/resolved markers cleaned | 11 | Owned `TODO:` headings replaced with tracked inventory references |

## Inventory

| file | line | marker | text | category | status | priority | owner_area | action |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `common/docs/design.md` | 58 | open work | Define ownership rules for header and body buffers | refactor | planned | P1 | common | Design before moving adapter logic into `common/` |
| `common/docs/design.md` | 59 | open work | Decide where neutral status values become part of future adapter APIs | refactor | planned | P2 | common | Revisit during first adapter API proposal |
| `common/docs/design.md` | 60 | open work | Add compile tests proving headers remain connector-independent | test | planned | P2 | common | Add when Common headers become build inputs |
| `common/src/README.md` | 19 | phase 3 resolved | Add implementation files only after a connector-neutral need exists | refactor | resolved | P3 | common | Metadata-only Common C helpers now exist; broader runtime extraction remains deferred |
| `tests/common/schema/README.md` | 67 | open work | Define a machine-readable JSON schema | test | planned | P1 | tests/common | Add schema after YAML shape stabilizes |
| `tests/common/schema/README.md` | 68 | open work | Reject connector-specific fields in common schema validation | test | planned | P1 | tests/common | Add with machine-readable schema |
| `tests/normalizers/README.md` | 18 | open work | Header order normalization | test | planned | P2 | normalizers | Add artifact-specific parser |
| `tests/normalizers/README.md` | 19 | open work | Audit log section parsing | audit-log | planned | P2 | normalizers | Add stable section-aware parser |
| `tests/normalizers/README.md` | 20 | open work | Connector-specific log formats | connector | deferred | P3 | connector tests | Keep in connector-specific normalizers |
| `connectors/apache/TODO.md` | 1 | planning file | Apache-specific build/runtime/refactor items | connector | planned | P1 | apache | Keep as connector-local checklist linked to this inventory |
| `connectors/nginx/TODO.md` | 1 | planning file | NGINX-specific build/runtime/refactor items | connector | planned | P1 | nginx | Keep as connector-local checklist linked to this inventory |
| `connectors/haproxy/TODO.md` | 3 | `Status: unknown` | Integration path undecided | future-connector | planned | P2 | haproxy | Decide after Common stabilization |
| `connectors/envoy/TODO.md` | 3 | `Status: unknown` | Integration path undecided | future-connector | planned | P2 | envoy | Decide after Common stabilization |
| `connectors/lighttpd/TODO.md` | 3 | `Status: unknown` | Integration path undecided | future-connector | planned | P2 | lighttpd | Decide after Common stabilization |
| `connectors/traefik/TODO.md` | 3 | `Status: unknown` | Integration path undecided | future-connector | planned | P2 | traefik | Decide after Common stabilization |
| `connectors/apache/docs/architecture.md` | 16 | open work | Exact hook order for a new adapter | connector | planned | P1 | apache | Document before maintained Apache adapter changes |
| `connectors/apache/docs/build.md` | 56 | open work | Minimum Apache/APR/APR-util/PCRE requirements | ci | planned | P2 | apache | Record from reproducible build matrix |
| `connectors/nginx/docs/architecture.md` | 17 | open work | Exact phase/filter ordering for this repo | connector | planned | P1 | nginx | Document before maintained NGINX adapter changes |
| `connectors/nginx/docs/build.md` | 44 | open work | Supported NGINX versions and static module proof | ci | planned | P2 | nginx | Keep dynamic module as active PoC path |
| `connectors/*/docs/build.md` | 7 | open work | Future connector build docs | future-connector | planned | P2 | future-connectors | Fill only when a connector path is selected |
| `docs/testing/v3-api-smoke-test.md` | 281 | open work | Keep v3 build-copy path reproducible and document fallback behavior | test | planned | P2 | v3-api-smoke | Keep API smoke separate from connector proof |
| `docs/imports/import-analysis-modsecurity-v2.md` | 57 | open work | Per-test map from v2 Perl structures to v3 YAML cases | test | planned | P2 | imports | Continue source-derived mapping only |
| `docs/roadmap/roadmap.md` | 12 | RAW-ARGS | PR #3564-dependent RAW argument collection cases | raw-args | mapped | P1 | tests/common | Activate only after local source support plus Apache/NGINX PASS |
| `docs/evidence/raw-args-pr3564.md` | 8 | PR #3564 | RAW argument collection evidence | raw-args | mapped | P1 | evidence | Keep mapped-only until support is proven |
| `docs/testing/response-body-blocking-investigation.md` | 1 | xfail | Response-body blocking probe | response-body | xfail | P1 | connectors | Do not promote until both connectors return stable HTTP 403 |
| `tests/common/cases/xfail/response_body_basic_block.yaml` | 1 | xfail case | Shared response-body blocking probe | response-body | xfail | P1 | tests/common | Explicit probe only; excluded from normal discovery |
| `tests/common/cases/xfail/v3_action_nolog_pass_no_audit.yaml` | 1 | xfail case | `nolog,pass` audit absence differs locally vs CI | audit-log | xfail | P2 | tests/common | Keep probeable but not active common PASS |
| `connectors/apache/upstream/README.md` | 104 | upstream TODO | Imported upstream README placeholder | docs | deferred | P3 | upstream-reference | Do not edit imported upstream docs |
| `connectors/apache/upstream/README.md` | 119 | upstream TODO | Imported upstream README placeholder | docs | deferred | P3 | upstream-reference | Do not edit imported upstream docs |
| `connectors/apache/upstream/README.md` | 157 | upstream TODO | Imported upstream TODO template marker | docs | deferred | P3 | upstream-reference | Do not edit imported upstream docs |
| `connectors/apache/upstream/src/msc_filters.c` | 65 | upstream FIXME | Apache response/body filter sanity note | response-body | mapped | P2 | upstream-reference | Leave untouched; track during response-filter refactor |
| `connectors/apache/upstream/tests/run-regression-tests.pl.in` | 482 | upstream TODO | Use `select()`/`poll()` in upstream harness | cleanup | deferred | P3 | upstream-reference | Not used by active smokes |
| `connectors/apache/upstream/tests/regression/server_root/conf/httpd.conf.in` | 3 | upstream TODO | Upstream regression template configurability | cleanup | deferred | P3 | upstream-reference | Retained as configure template |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_module.c` | 226 | upstream FIXME | Audit log response-code accuracy | audit-log | mapped | P2 | upstream-reference | Relevant to audit metadata review; do not edit imported code |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_module.c` | 600 | upstream TODO | Log phase parity with Apache | audit-log | mapped | P2 | upstream-reference | Track before logging helper extraction |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_header_filter.c` | 423 | upstream XXX | `NOT_MODIFIED` header-filter behavior | response-body | mapped | P2 | upstream-reference | Relevant to response-filter evidence |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_header_filter.c` | 439 | upstream XXX | Already processed request question | response-body | mapped | P2 | upstream-reference | Relevant to response-filter evidence |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_header_filter.c` | 440 | upstream XXX | `ModSecurity off` behavior | response-body | mapped | P2 | upstream-reference | Relevant to response-filter evidence |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_header_filter.c` | 445 | upstream FIXME | Verify already processed request state | response-body | mapped | P2 | upstream-reference | Relevant to response-filter evidence |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_header_filter.c` | 454 | upstream FIXME | `SecResponseBody` disabled flag handling | response-body | mapped | P2 | upstream-reference | Relevant to PR #377 evidence |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_body_filter.c` | 27 | upstream XXX | Multiple body-filter behavior | response-body | mapped | P2 | upstream-reference | Relevant to response-filter evidence |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_body_filter.c` | 156 | upstream XXX | Last buffer / last chain handling | response-body | mapped | P2 | upstream-reference | Relevant to PR #377 evidence |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_body_filter.c` | 166 | upstream XXX | ModSecurity body transfer and content-length adjustment | response-body | mapped | P1 | upstream-reference | Relevant to PR #377 evidence |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_body_filter.c` | 184 | upstream XXX | Filter return behavior | response-body | mapped | P2 | upstream-reference | Relevant to response-filter evidence |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_access.c` | 80 | upstream FIXME | Address metadata type choice | connector | mapped | P3 | upstream-reference | Candidate for request metadata mapping review |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_access.c` | 95 | upstream FIXME | Earlier NGINX hook phase | connector | mapped | P2 | upstream-reference | Candidate for phase timing review |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_access.c` | 172 | upstream FIXME | Finalizing request safely | connector | mapped | P1 | upstream-reference | Relevant before intervention extraction |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_access.c` | 291 | upstream FIXME | Empty upstream marker | cleanup | deferred | P3 | upstream-reference | Leave untouched |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_access.c` | 338 | upstream TODO | `request_body_in_single_buf` benefit | request-body | mapped | P2 | upstream-reference | Candidate for request-body buffering review |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_access.c` | 386 | upstream TODO | Stream chunks as they arrive | request-body | mapped | P2 | upstream-reference | Streaming remains out of active scope |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_access.c` | 425 | upstream XXX | Chain processing and intervention timing | connector | mapped | P2 | upstream-reference | Candidate for intervention review |
| `connectors/nginx/upstream/src/ngx_http_modsecurity_access.c` | 445 | upstream XXX | Body mutation/content-length adjustment | response-body | mapped | P1 | upstream-reference | Relevant to response-filter evidence |

## Cleaned Markers

The following owned markers were removed or replaced by inventory references:

- `common/docs/design.md` old `## TODO` heading.
- `common/src/README.md` old `TODO:` heading.
- `tests/common/schema/README.md` old `TODO:` heading.
- `tests/normalizers/README.md` old `TODO:` heading.
- Connector-local `TODO.md` titles now use “Planning” while retaining the file
  names expected by workflow structure checks.
- Connector build/architecture docs now use “Open work” wording and point here.
- Apache and NGINX PoC docs now use “Tracked Open Work” and point here instead
  of keeping standalone TODO lists.
