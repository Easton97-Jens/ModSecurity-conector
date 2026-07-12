<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Open connector build paths

**Language:** English | [Deutsch](overview.de.md)

## Purpose

Envoy, Traefik, and lighttpd use repository-owned build and runtime
components. This index summarizes only their current selected routes; the
individual guides and the [complete compiler overview](README.md) contain the
details.

| Connector | Guide | explicit runtime preparation | Full lifecycle | selected profile |
| --- | --- | --- | --- | --- |
| [Envoy](envoy.md) | `prepare-envoy-runtime` | `full-lifecycle-envoy-ext-proc` | `ext_proc` |
| [Traefik](traefik.md) | `prepare-traefik-runtime` | `full-lifecycle-traefik-native` | `native-middleware` |
| [lighttpd](lighttpd.md) | `prepare-lighttpd-runtime-build` | `full-lifecycle-lighttpd-patched` | `patched-native` |

## Active route

1. Run `make check-framework`.
2. Run the runtime preparation named in the table when a host or its cache
   input is not already present.
3. Run `make build-<connector>`, `make check-config-<connector>`,
   `make start-smoke-<connector>`, and `make runtime-smoke-<connector>` as
   separate stages.
4. With a safe `NO_CRS_RUN_ID`, run the listed full-lifecycle target, then
   `make evidence-check-<connector>`.

Building Envoy's `ext_authz` service, Traefik's forwardAuth service, or a
lighttpd bridge can be useful compatibility diagnostics. None replaces the
listed ext_proc, native-middleware, or patched-native host route.

## Versions, cache, and boundary

`make runtime-components-inventory` and `make runtime-components-sources`
show the prepared Cache-v2 provenance. A successful download, extraction,
build, configuration load, or start is not production, CRS, HTTP/2, HTTP/3,
Strict, or complete-capability evidence. See the
[variable reference](../../configuration/variables.md) and
[evidence rules](../../evidence/README.md).
