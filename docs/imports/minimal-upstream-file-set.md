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

Repo-owned build-copy overlay:

- `connectors/nginx/src/ddebug.h` is copied to
  `$BUILD_ROOT/nginx-build/ModSecurity-nginx/src/ddebug.h` when the selected
  connector source tree does not provide that header. This keeps the upstream
  `config` dependency satisfied while reducing `connectors/nginx/upstream/`.

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
