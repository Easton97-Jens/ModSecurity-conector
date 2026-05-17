# Upstream Pruning Analysis

Status: implemented

This document records the pruning review for the controlled Apache and NGINX
connector source imports. The review is intentionally conservative: files are
removed only when they are not referenced by build/runtime inputs, not required
for license or origin context, and have a successful isolated `$BUILD_ROOT`
probe. No such safe removal was identified in this pass.

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

| Connector | Imported files | Removed in this pass | Reason |
| --- | ---: | ---: | --- |
| Apache | 25 | 0 | Remaining files are license/origin context, Autotools inputs, module source, or templates referenced by `configure.ac`/test layout |
| NGINX | 12 | 0 | Remaining files are license/origin context, module metadata, or source/dependency files listed by `config` |

Because the imported trees are already minimal, forcing a deletion would risk
losing build coverage without evidence. The cleanup result is therefore a
documented minimal set rather than an artificial reduction.

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
| `src/ddebug.h` | required | Listed in `config` as `ngx_module_deps` | Keep |
| `src/ngx_http_modsecurity_access.c` | required | Listed in `config` as module source | Keep |
| `src/ngx_http_modsecurity_body_filter.c` | required | Listed in `config` as module source | Keep |
| `src/ngx_http_modsecurity_common.h` | required | Listed in `config` as dependency and included by module sources | Keep |
| `src/ngx_http_modsecurity_header_filter.c` | required | Listed in `config` as module source | Keep |
| `src/ngx_http_modsecurity_log.c` | required | Listed in `config` as module source | Keep |
| `src/ngx_http_modsecurity_module.c` | required | Listed in `config` as module source and contains NGINX module entrypoint | Keep |

## Removal Decision

No files were removed. In particular:

- Apache `.in` templates are retained because `configure.ac` references them
  directly through `AC_CONFIG_FILES`.
- NGINX source files are retained because `config` explicitly lists them as
  module sources or dependencies.
- License and attribution files are retained for provenance and redistribution
  clarity.

Any future deletion must be validated in an isolated copy under `$BUILD_ROOT`,
then followed by real-world Apache, NGINX, and combined smoke runs.
