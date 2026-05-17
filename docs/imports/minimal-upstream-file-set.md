# Minimal Upstream File Set

Status: implemented

This document defines the current minimal imported Apache and NGINX connector
source sets used by the monorepo smoke builds. The files remain
connector-specific. Phase 9 migrates the NGINX module source into
adapter-owned `connectors/nginx/src` while retaining upstream attribution files.
No Apache hook, NGINX filter, body, transaction, or Common runtime logic was
merged across connectors.

## Apache Connector

Minimal imported tree: `connectors/apache/upstream/`

Required for build and module creation:

- `autogen.sh`
- `configure.ac`
- `Makefile.am`
- `build/apxs-wrapper.in`
- `build/ax_prog_apache.m4`
- `build/find_apxs.m4`
- `build/find_libmodsec.m4`
- `src/mod_security3.c`
- `src/mod_security3.h`
- `src/msc_config.c`
- `src/msc_config.h`
- `src/msc_filters.c`
- `src/msc_filters.h`
- `src/msc_utils.c`
- `src/msc_utils.h`

Build-only templates retained because `configure.ac` or the upstream test
layout references them:

- `t/conf/extra.conf.in`
- `tests/run-regression-tests.pl.in`
- `tests/regression/misc/40-secRemoteRules.t.in`
- `tests/regression/misc/50-ipmatchfromfile-external.t.in`
- `tests/regression/misc/60-pmfromfile-external.t.in`
- `tests/regression/server_root/conf/httpd.conf.in`

License and provenance context:

- `LICENSE`
- `AUTHORS`
- `CHANGES`
- `README.md`

## NGINX Connector

Minimal retained upstream tree: `connectors/nginx/upstream/`

Required for attribution/reference:

- `LICENSE`
- `AUTHORS`
- `CHANGES`
- `README.md`

Adapter-owned NGINX module build inputs:

- `connectors/nginx/src/config`
- `connectors/nginx/src/ngx_http_modsecurity_access.c`
- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_log.c`
- `connectors/nginx/src/ngx_http_modsecurity_module.c`
- `connectors/nginx/src/ddebug.h`
- `connectors/nginx/src/SOURCE_MAP.json`

PR #377 provenance:

- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`,
  `connectors/nginx/src/ngx_http_modsecurity_common.h`, and
  `connectors/nginx/src/ngx_http_modsecurity_module.c` include source changes
  from ModSecurity-nginx PR #377 commit
  `3d72b004ff27a78ea19c6b945870e2cae62a97ac`.
- Those changes are source-level phase-4 evidence only. `RESPONSE_BODY` remains
  xfail/mapped-only and excluded from `verified_variables`.

Materialized build input:

- Monorepo-default NGINX builds use
  `$BUILD_ROOT/nginx-build/connector-src`.
- The materializer copies retained upstream attribution files, overlays
  adapter-owned `connectors/nginx/src`, maps adapter `config` to root `config`,
  and writes `MATERIALIZED_SOURCE.md` plus `materialized-source.json`.
- External NGINX source builds still use a sanitized external-source copy; if
  the selected external source tree lacks `src/ddebug.h`,
  `ci/prepare-nginx-build.sh` overlays the repo-owned header into the generated
  external build copy.

## Future Common Extraction Candidates

These are candidates only. They must not be moved until behavior is proven with
real-world connector smokes after extraction.

| Category | Apache source area | NGINX source area | Current decision |
| --- | --- | --- | --- |
| Debug compatibility | none | repo-owned `connectors/nginx/src/ddebug.h` | Replaced imported upstream debug helper |
| Ruleset loading | `src/msc_config.*` | `src/ngx_http_modsecurity_module.c` | Keep connector-specific |
| Transaction lifecycle | `src/mod_security3.c`, `src/msc_filters.*` | access/header/body/log sources | Keep connector-specific |
| Intervention handling | `src/mod_security3.c`, `src/msc_utils.*` | `src/ngx_http_modsecurity_module.c` | Keep connector-specific |
| Audit/logging | Apache log hook/filter code | `src/ngx_http_modsecurity_log.c` | Keep connector-specific |
| Request metadata mapping | Apache request/filter code | `src/ngx_http_modsecurity_access.c` | Keep connector-specific |
| Response metadata mapping | Apache output filter code | NGINX header/body filters | Keep connector-specific |
| Config model | Apache per-dir/server config | NGINX main/location config | Keep connector-specific |
| Error handling | Apache utility and hook paths | NGINX return/finalize paths | Keep connector-specific |

## Pruning Rule

Do not remove a file from an imported upstream tree unless all of the following
are true:

- It is not referenced by build metadata or source includes.
- It is not needed for license, attribution, or source-origin context.
- It is not a documented future common-extraction candidate.
- A disposable probe under `$BUILD_ROOT` proves that Apache, NGINX, and
  combined smokes still pass without it.

The phase-4 review found one safe replacement: the NGINX debug compatibility
header. Phase 9 migrated NGINX productive source into adapter-owned files and
reduced `connectors/nginx/upstream/` to attribution/reference files only.

## Phase 8 Shadow Build Source

Phase 8 does not remove additional upstream files. It changes the monorepo
default NGINX build input from a direct sanitized upstream copy to
`$BUILD_ROOT/nginx-build/connector-src`. That generated source tree contains
manifests identifying `adapter-owned`, `upstream-derived`, and
`generated-overlay` files.

Apache also gets `$BUILD_ROOT/apache-build/connector-src` manifests, but its
module build still uses `$BUILD_ROOT/apache-build/ModSecurity-apache` until a
separate Autotools/APXS proof switches the default.

## Phase 9 NGINX Source Migration

Phase 9 moves the NGINX module `config` and all remaining module source files
from `connectors/nginx/upstream/` to `connectors/nginx/src/`, then removes the
upstream copies after a materialized-source NGINX smoke passes. The retained
NGINX upstream tree is now a minimal attribution/reference set.

## Phase 5 Review Result

Phase 5 reviewed a second possible reduction and made no additional upstream
changes. The remaining small helpers are not standalone debug/build shims:

- Apache `id()` appears unused, but removing it would edit the imported
  `msc_utils.c/.h` pair for no functional replacement.
- Apache `send_error_bucket()` owns Apache bucket/error response behavior.
- NGINX `ngx_str_to_char()` is shared by config parsing and request metadata
  mapping.
- NGINX PCRE pool helpers are part of rules/config lifecycle.
- NGINX response-header resolver helpers and log callback are active
  response/audit paths.

Those areas stay connector-specific until repo-owned adapter implementations
exist and before/after real-world smokes prove equivalence.
