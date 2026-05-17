# Apache Adapter-Owned Migration Plan

Status: planned

Apache remains on the controlled imported source tree in Phase 10. This plan
defines the evidence required before Apache can follow the NGINX
adapter-owned/materialized source path.

## Current State

| Area | Current location | Phase 10 decision |
| --- | --- | --- |
| Apache module sources | `connectors/apache/upstream/src/*.c`, `*.h` | Keep in upstream import until adapter-owned copy builds and smokes pass |
| Autotools entrypoints | `connectors/apache/upstream/autogen.sh`, `configure.ac`, `Makefile.am` | Keep; Autotools/APXS behavior is higher risk |
| Build macros/templates | `connectors/apache/upstream/build/*.m4`, `.in` templates | Keep; referenced by `configure.ac` and generated build flow |
| Adapter metadata | `connectors/apache/src/metadata.*` | Already adapter-owned, validation-only |

## Migration Groups

| Group | Candidate files | Risk | Probe requirement |
| --- | --- | --- | --- |
| Source files | `src/mod_security3.*`, `src/msc_config.*`, `src/msc_filters.*`, `src/msc_utils.*` | High: hook registration, bucket brigades, filters, intervention handling, and Apache request metadata live here | Copy to `connectors/apache/src` only in a dedicated phase, materialize under `$BUILD_ROOT/apache-build/connector-src`, build, then run `smoke-apache` and `smoke-all` |
| Autotools/APXS files | `autogen.sh`, `configure.ac`, `Makefile.am`, `build/*.m4`, `build/apxs-wrapper.in` | Medium/high: configure-generated paths and APXS discovery are fragile | First prove a disposable materialized Autotools tree with no checkout writes |
| Test/config templates | `t/conf/*.in`, `tests/**/*.in` | Medium: kept because `configure.ac` references them | Keep until configure output is proven without the upstream layout |
| License/context files | `LICENSE`, `AUTHORS`, `CHANGES`, `README.md` | Low if durable attribution remains | Keep in `licenses/apache/` and `connectors/apache/ORIGIN.md`; remove upstream-adjacent copies only after source tree is no longer retained |

## Probe Criteria

A future Apache migration phase may switch the default build only after all of
these pass:

```sh
REFRESH=1 BUILD_ROOT=/src/ModSecurity-conector-apache-adapter-build make smoke-apache
BUILD_ROOT=/src/ModSecurity-conector-apache-adapter-build make smoke-all
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-all
```

The materialized Apache source must live under
`$BUILD_ROOT/apache-build/connector-src`, must not write generated Autotools
files into the checkout, and must preserve `connectors/apache/ORIGIN.md` plus
`licenses/apache/`.

## Explicit Deferrals

- No Apache source moves in Phase 10.
- No Apache hook/filter/bucket/intervention behavior is rewritten.
- No Apache common extraction is attempted.
- No response-body behavior is promoted; `RESPONSE_BODY` remains
  xfail/mapped-only.
