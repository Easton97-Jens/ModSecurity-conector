<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Overview of the six compiler paths

**Language:** English | [Deutsch](overview.de.md)

## Target map

| Connector | Preparation | Build | Config check | Selected full lifecycle |
| --- | --- | --- | --- | --- |
| [Apache HTTP Server](apache.md) | `prepare-runtime-components` | `build-apache` | `check-config-apache` | `full-lifecycle-apache` |
| [NGINX](nginx.md) | `prepare-runtime-components` | `build-nginx` | `check-config-nginx` | `full-lifecycle-nginx` |
| [HAProxy](haproxy.md) | `prepare-runtime-components` | `build-haproxy` | `check-config-haproxy` | `full-lifecycle-haproxy-htx` |
| [Envoy](envoy.md) | `prepare-envoy-runtime` | `build-envoy` | `check-config-envoy` | `full-lifecycle-envoy-ext-proc` |
| [Traefik](traefik.md) | `prepare-traefik-runtime` | `build-traefik` | `check-config-traefik` | `full-lifecycle-traefik-native` |
| [lighttpd](lighttpd.md) | `prepare-lighttpd-runtime-build` | `build-lighttpd` | `check-config-lighttpd` | `full-lifecycle-lighttpd-patched` |

Detailed guides contain complete commands, expected files, exit-code boundaries, and package checks. Before a run, execute `make runtime-components-inventory` and `make runtime-components-sources`; their prepared records are authoritative when pins change.

## Three paths, three different statements

| Path | Suitable for | System-wide changes | Host from source? | Core path possible? | Evidence possible? |
| --- | --- | --- | --- | --- | --- |
| Repository test path | Development and CI | No | Repository-controlled | Yes | Yes, after full lifecycle and evidence check |
| Local source build | Development and integration | Optional | Documented per connector | Yes | Yes, selected run only |
| Package path | Quick local start | Yes | Usually no | Connector-dependent | Only matching profile and run |

## Shared boundary

Targets create reproducible development, test, and build artifacts. They are not an assessment of a production package or hardened deployment guidance. A package, compile, or individual smoke is not promoted to production, CRS, security, or full-matrix evidence.
