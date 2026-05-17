# Upstream Pruning Analysis

Status: implemented

This document records the pruning review for the controlled Apache and NGINX
connector source imports. The review is intentionally conservative: files are
removed only when they have a functional replacement, are not required for
license or origin context, and have a successful isolated `$BUILD_ROOT` probe.
Phase 4 removed one NGINX debug helper after adding a repo-owned build-copy
overlay. Phase 5 reviewed the remaining source helpers and found no additional
safe replacement candidate.

Phase 8 adds a shadow build-source layer. The monorepo-default NGINX build now
uses `$BUILD_ROOT/nginx-build/connector-src`, generated from the remaining
imported upstream source plus adapter-owned overlays. This is not a new pruning
event; no additional upstream files are removed from the checkout.

## Evidence Used

- File inventory from `connectors/apache/upstream/` and
  `connectors/nginx/upstream/`.
- Apache Autotools inputs: `configure.ac`, `Makefile.am`, `build/*.m4`, and
  `build/apxs-wrapper.in`.
- NGINX module metadata: `connectors/nginx/upstream/config`.
- Current smoke harness behavior in `ci/prepare-apache-build.sh` and
  `ci/prepare-nginx-build.sh`.
- Existing real-world smoke path, which copies these source trees to
  `$BUILD_ROOT` before building.

## Result

| Connector | Imported files | Removed after phase 4 | Removed after phase 5 | Reason |
| --- | ---: | ---: | ---: | --- |
| Apache | 25 | 0 | 0 | Remaining files are license/origin context, Autotools inputs, module source, or templates referenced by `configure.ac`/test layout |
| NGINX | 12 | 1 | 0 | `src/ddebug.h` was replaced by repo-owned `connectors/nginx/src/ddebug.h`; remaining files are license/origin context, module metadata, or production source/dependency files listed by `config` |

The imported trees remain intentionally small. The only reduction is backed by a
repo-owned replacement and real-world smoke validation. Phase 5 intentionally
does not delete another file because the reviewed candidates are production
request/response, config, lifecycle, or audit paths.

## Apache File Classification

Source: `connectors/apache/upstream/`

| File | Classification | Evidence | Decision |
| --- | --- | --- | --- |
| `AUTHORS` | documentation-only | Upstream attribution required for controlled import | Keep |
| `CHANGES` | documentation-only | Upstream change context retained with imported source | Keep |
| `LICENSE` | required | License text for Apache-2.0 imported files | Keep |
| `README.md` | documentation-only | Upstream build and usage context | Keep |
| `Makefile.am` | required | Automake input for connector build | Keep |
| `autogen.sh` | build-only | Bootstraps Autotools files in build copy | Keep |
| `configure.ac` | required | Defines build checks and generated templates | Keep |
| `build/apxs-wrapper.in` | build-only | APXS wrapper template used by Autotools build | Keep |
| `build/ax_prog_apache.m4` | build-only | Apache detection macro | Keep |
| `build/find_apxs.m4` | build-only | APXS detection macro | Keep |
| `build/find_libmodsec.m4` | build-only | libmodsecurity detection macro | Keep |
| `src/mod_security3.c` | required | Apache module entrypoint | Keep |
| `src/mod_security3.h` | required | Apache module declarations | Keep |
| `src/msc_config.c` | required | Apache directive/configuration implementation | Keep |
| `src/msc_config.h` | required | Apache configuration declarations | Keep |
| `src/msc_filters.c` | required | Apache input/output filter implementation | Keep |
| `src/msc_filters.h` | required | Apache filter declarations | Keep |
| `src/msc_utils.c` | required | Apache connector utility implementation | Keep |
| `src/msc_utils.h` | required | Apache connector utility declarations | Keep |
| `t/conf/extra.conf.in` | build-only | Keeps upstream `t/conf` test-template layout; references generated `modules.conf` | Keep |
| `tests/run-regression-tests.pl.in` | build-only | Listed in `configure.ac` `AC_CONFIG_FILES` | Keep |
| `tests/regression/misc/40-secRemoteRules.t.in` | build-only | Listed in `configure.ac` `AC_CONFIG_FILES` | Keep |
| `tests/regression/misc/50-ipmatchfromfile-external.t.in` | build-only | Listed in `configure.ac` `AC_CONFIG_FILES` | Keep |
| `tests/regression/misc/60-pmfromfile-external.t.in` | build-only | Listed in `configure.ac` `AC_CONFIG_FILES` | Keep |
| `tests/regression/server_root/conf/httpd.conf.in` | build-only | Listed in `configure.ac` `AC_CONFIG_FILES` | Keep |

## NGINX File Classification

Source: `connectors/nginx/upstream/`

| File | Classification | Evidence | Decision |
| --- | --- | --- | --- |
| `AUTHORS` | documentation-only | Upstream attribution required for controlled import | Keep |
| `CHANGES` | documentation-only | Upstream change context retained with imported source | Keep |
| `LICENSE` | required | License text for Apache-2.0 imported files | Keep |
| `README.md` | documentation-only | Upstream build and usage context | Keep |
| `config` | required | NGINX module build metadata, source list, dependency list | Keep |
| `src/ngx_http_modsecurity_access.c` | required | Listed in `config` as module source | Keep |
| `src/ngx_http_modsecurity_body_filter.c` | required | Listed in `config` as module source | Keep |
| `src/ngx_http_modsecurity_common.h` | required | Listed in `config` as dependency and included by module sources | Keep |
| `src/ngx_http_modsecurity_header_filter.c` | required | Listed in `config` as module source | Keep |
| `src/ngx_http_modsecurity_log.c` | required | Listed in `config` as module source | Keep |
| `src/ngx_http_modsecurity_module.c` | required | Listed in `config` as module source and contains NGINX module entrypoint | Keep |

## Replaced Files

| File | Previous classification | Replacement | Evidence | Decision |
| --- | --- | --- | --- | --- |
| `connectors/nginx/upstream/src/ddebug.h` | build dependency | `connectors/nginx/src/ddebug.h` copied into the generated build tree when needed | The header only provides debug macros and sanity-check no-ops; it does not own hooks, filters, bodies, transactions, or libmodsecurity lifecycle | Remove imported copy after smoke validation |

## Removal Decision

One file was removed in phase 4. In particular:

- Apache `.in` templates are retained because `configure.ac` references them
  directly through `AC_CONFIG_FILES`.
- NGINX production source files are retained because `config` explicitly lists
  them as module sources or dependencies.
- NGINX `config` still lists `src/ddebug.h`, but the generated build copy now
  receives a repo-owned replacement when the selected source tree lacks it.
- License and attribution files are retained for provenance and redistribution
  clarity.

Any future deletion must be validated in an isolated copy under `$BUILD_ROOT`,
then followed by real-world Apache, NGINX, and combined smoke runs.

## Phase 5 No-Removal Decision

Phase 5 reviewed a second replacement candidate set and made no new removals.

| Candidate | Evidence | Decision |
| --- | --- | --- |
| Apache `id()` helper | No callers outside its declaration/definition, but removal would edit `msc_utils.c/.h`, which also owns `send_error_bucket()` declarations and Apache utility context | Defer as obsolete/reference-only until Apache adapter code is repo-owned |
| Apache `send_error_bucket()` | Called by `msc_filters.c`; creates Apache buckets and controls error response flow | Defer |
| NGINX `ngx_str_to_char()` | Used by config directives, location merge, and request metadata mapping | Defer |
| NGINX PCRE pool helpers | Tied to NGINX pool and rules/config loading lifecycle | Defer |
| NGINX response-header resolver helpers | Direct response header/filter path | Defer |
| NGINX log callback | Audit/log behavior remains evidence-sensitive | Defer |

No phase-5 candidate can be reduced without creating adapter-owned replacement
code in a production connector path. That is intentionally out of scope for
this review.

## Phase 8 Build-Input Reduction

The generated NGINX connector source tree reduces direct build dependence on the
`connectors/nginx/upstream/` directory. The retained upstream tree remains the
reference/provenance source, while the disposable `$BUILD_ROOT` tree records the
actual build-copy composition.

Apache receives the same manifest-only preparation. Its productive module build
still uses the sanitized upstream copy in phase 8.
