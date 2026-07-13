<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Compiler, source-build, and package paths

**Language:** English | [Deutsch](README.de.md)

## Purpose

Each detailed guide describes a repository-controlled test path, a local source
build, and an honest package path. A build, link, config check, start, or
package-install result alone is not runtime, CRS, security, production, or
full-matrix evidence.

## Shared starting point

Before any connector, [build libmodsecurity v3](libmodsecurity.md). The
beginner sequence exists only there; the connector guides then start with their
own host and connector.

## Decision matrix

| Connector | Test path | Source build | Package status | Selected core path |
| --- | --- | --- | --- | --- |
| [Apache HTTP Server](apache.md) | `make build-apache` | `make full-lifecycle-apache` | `package-assisted source build` | `native-httpd-module` |
| [NGINX](nginx.md) | `make build-nginx` | `make full-lifecycle-nginx` | `package-assisted source build` | `native-nginx-http-module` |
| [HAProxy](haproxy.md) | `make build-haproxy` | `make full-lifecycle-haproxy-htx` | `package-assisted source build` | `native-htx-filter` |
| [Envoy](envoy.md) | `make build-envoy` | `make full-lifecycle-envoy-ext-proc` | `package-assisted source build` | `ext_proc` |
| [Traefik](traefik.md) | `make build-traefik` | `make full-lifecycle-traefik-native` | `package-assisted source build` | `native-middleware` |
| [lighttpd](lighttpd.md) | `make build-lighttpd` | `make full-lifecycle-lighttpd-patched` | `selected profile not available package-only` | `patched-native` |

## Decision tree

Only need to test?
→ Use the repository test path.

Developing a build or change?
→ Use the local source build with external `VERIFIED_RUN_PARENT`.

Need system packages for host and dependencies?
→ Check the package path, query availability before installation, and validate v3/ABI.

Does the core path need a host patch, module, middleware, or service?
→ Use a package-assisted source build; do not present a standard package as equivalent.

## Shared prerequisite

```sh
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
```

The external parent stays outside the checkout, holds build, cache, runtime,
log, and evidence files, and should not contain secrets in its name. See the
[connector overview](overview.md), [variable reference](../../reference/variables.md),
and [testing/evidence boundary](../../testing-and-evidence.md).
