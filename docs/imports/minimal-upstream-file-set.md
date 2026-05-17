# Minimal Upstream File Set

Status: implemented

This document defines the current minimal imported Apache and NGINX connector
source sets used by the monorepo smoke builds. The files remain
connector-specific. Phase 4 replaces one NGINX debug helper with repo-owned
adapter-near code; no hook, filter, body, transaction, or Common runtime logic
was extracted.

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

Minimal imported tree: `connectors/nginx/upstream/`

Required for NGINX module build and runtime smoke:

- `config`
- `src/ngx_http_modsecurity_access.c`
- `src/ngx_http_modsecurity_body_filter.c`
- `src/ngx_http_modsecurity_common.h`
- `src/ngx_http_modsecurity_header_filter.c`
- `src/ngx_http_modsecurity_log.c`
- `src/ngx_http_modsecurity_module.c`

Repo-owned materialized-source overlay:

- `connectors/nginx/src/ddebug.h` is copied to
  `$BUILD_ROOT/nginx-build/connector-src/src/ddebug.h` for monorepo-default
  builds. This keeps the upstream `config` dependency satisfied while reducing
  `connectors/nginx/upstream/`.
- External NGINX source builds keep the older fallback: if the selected external
  source tree lacks `src/ddebug.h`, `ci/prepare-nginx-build.sh` overlays the
  repo-owned header into the generated external build copy.

License and provenance context:

- `LICENSE`
- `AUTHORS`
- `CHANGES`
- `README.md`

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
header. All remaining imported files stay under the pruning rule above.

## Phase 8 Shadow Build Source

Phase 8 does not remove additional upstream files. It changes the monorepo
default NGINX build input from a direct sanitized upstream copy to
`$BUILD_ROOT/nginx-build/connector-src`. That generated source tree contains
manifests identifying `adapter-owned`, `upstream-derived`, and
`generated-overlay` files.

Apache also gets `$BUILD_ROOT/apache-build/connector-src` manifests, but its
module build still uses `$BUILD_ROOT/apache-build/ModSecurity-apache` until a
separate Autotools/APXS proof switches the default.

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
