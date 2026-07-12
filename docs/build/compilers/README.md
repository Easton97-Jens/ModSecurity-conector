<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Compiler and build paths

**Language:** English | [Deutsch](README.de.md)

## Purpose

This directory documents the current repository paths for build,
configuration-load, start-smoke, minimal runtime smoke, and the selected
No-CRS full-lifecycle run. It is not a procedure for globally installing an
arbitrary distribution host. A successful build, link, or config check is not
production, CRS, HTTP/2, HTTP/3, or full-matrix evidence.

## Selected routes

| Detail guide | Build | selected full-lifecycle target | Host profile |
| --- | --- | --- | --- |
| [Apache HTTP Server](apache.md) | `build-apache` | `full-lifecycle-apache` | `native-httpd-module` |
| [NGINX](nginx.md) | `build-nginx` | `full-lifecycle-nginx` | `native-nginx-http-module` |
| [HAProxy](haproxy.md) | `build-haproxy` | `full-lifecycle-haproxy-htx` | `native-htx-filter` |
| [Envoy](envoy.md) | `build-envoy` | `full-lifecycle-envoy-ext-proc` | `ext_proc` |
| [Traefik](traefik.md) | `build-traefik` | `full-lifecycle-traefik-native` | `native-middleware` |
| [lighttpd](lighttpd.md) | `build-lighttpd` | `full-lifecycle-lighttpd-patched` | `patched-native` |

Each full-lifecycle target sets its host-profile values itself. Do not set the
internal `NO_CRS_ARTIFACT_PROFILE`, `FULL_LIFECYCLE_HOST_PROFILE`, or
`FULL_LIFECYCLE_EXECUTED_TARGET` variables manually to relabel a compatibility
smoke.

## Shared workflow

```sh
make check-framework
make prepare-runtime-components
make build-<connector>
make check-config-<connector>
make start-smoke-<connector>
make runtime-smoke-<connector>
```

`<connector>` is a documentation placeholder for exactly one name in the
table; do not pass it literally to `make`. Canonical evidence uses a safe run
identifier consistently within the invocation:

```sh
run_id="core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-<connector>
NO_CRS_RUN_ID="$run_id" make evidence-check-<connector>
```

The all-six route is `NO_CRS_RUN_ID="$run_id" make
full-lifecycle-all-connectors`. It creates run-specific evidence; it does not
replace inspection of the resulting artifacts.

## Cache-v2, versions, and provenance

`VERIFIED_RUN_PARENT` selects an external writable execution parent. The root
Makefile derives `BUILD_ROOT`, then `CACHE_ROOT=.../cache-v2` and its shared
component cache from it. The cache is reusable input, not canonical evidence.
Prepared components bind sources, versions, checksums, and local overrides;
the effective identity is shown by:

```sh
make runtime-components-inventory
make runtime-components-sources
```

The [variable reference](../../reference/variables.md) defines the format,
default, scope, effect, and security boundary for build, cache, provenance, and
host variables. Use trusted absolute paths outside the checkout for build,
cache, logs, and evidence.

## Documentation boundary

The per-connector guides below link to the current
[build overview](../README.md), [testing and evidence guide](../../testing-and-evidence.md),
connector guides, and examples.
Older integration descriptions are explicitly marked historical or diagnostic
where they remain useful; they are not active profile selectors and cannot
promote a capability.

## Open connector preparation

Envoy, Traefik, and lighttpd use repository-owned build and runtime
components. Their detailed guides remain the sole source of truth; their
preparation targets are:

| Connector | Preparation | Full lifecycle | Host profile |
| --- | --- | --- | --- |
| [Envoy](envoy.md) | `prepare-envoy-runtime` | `full-lifecycle-envoy-ext-proc` | `ext_proc` |
| [Traefik](traefik.md) | `prepare-traefik-runtime` | `full-lifecycle-traefik-native` | `native-middleware` |
| [lighttpd](lighttpd.md) | `prepare-lighttpd-runtime-build` | `full-lifecycle-lighttpd-patched` | `patched-native` |

Compatibility diagnostics through ext_authz, forwardAuth, or a bridge do not
replace the selected ext_proc, native-middleware, or patched-native route.

## Next

Start the detailed guides with [Apache](apache.md).
