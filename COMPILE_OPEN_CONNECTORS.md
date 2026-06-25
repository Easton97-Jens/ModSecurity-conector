Language: English | [Deutsch](COMPILE_OPEN_CONNECTORS.de.md)

# Compile / Prepare Open Connectors

## Table of Contents

- [Purpose](#purpose)
- [Status and Limits](#status-and-limits)
- [Overview: Three Paths](#overview-three-paths)
- [Path 1: Repository Smoke / Validation](#path-1-repository-smoke-validation)
- [Path 2: External Use With Distribution Packages](#path-2-external-use-with-distribution-packages)
- [Path 3: External Use From Source](#path-3-external-use-from-source)
- [Per-Connector Guides](#per-connector-guides)
- [Claims Not Allowed](#claims-not-allowed)

## Purpose

This is a shared index for the open connector runtime paths: Envoy, Traefik, and Lighttpd. Use the per-connector guides for operator steps; this file only summarizes shared repository preparation and evidence rules.

## Status and Limits

Envoy and Traefik are runtime-staged, not source-built by this repository. Lighttpd can be built locally from a pinned source tarball, but its current integration is `sidecar_proxy` / Phase 1, not a native module. PASS in this file means a repository target/evidence path exists when dependencies are present; it is not production readiness.

## Overview: Three Paths

| Path | Purpose | Main use |
| --- | --- | --- |
| Path 1: Repository smoke | Validate repository evidence | Developers / reviewers |
| Path 2: External use with packages | Use operator-provided runtime packages/binaries | Operators using system packages |
| Path 3: External use from source | Build libmodsecurity and applicable sidecar/runtime pieces | Operators needing exact version control |

## Path 1: Repository Smoke / Validation

These commands validate repository evidence. They are not the external installation procedure.

```sh
TMPDIR=/tmp ALLOW_RUNTIME_DOWNLOADS=1 make prepare-envoy-runtime
TMPDIR=/tmp ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
TMPDIR=/tmp ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
TMPDIR=/tmp make smoke-envoy
TMPDIR=/tmp make smoke-traefik
TMPDIR=/tmp make smoke-lighttpd
```

Targeted libmodsecurity and CRS smokes are repository evidence only:

```sh
TMPDIR=/tmp make smoke-envoy-modsecurity
TMPDIR=/tmp make smoke-traefik-modsecurity
TMPDIR=/tmp make smoke-lighttpd-modsecurity
TMPDIR=/tmp make smoke-open-connectors-crs
TMPDIR=/tmp make smoke-open-connectors-crs-secondary
```

## Path 2: External Use With Distribution Packages

Use operator-provided Envoy, Traefik, or Lighttpd packages/binaries where compatible. Package names, service names, runtime directories, and log locations vary by distribution. The repository does not install these components globally. Follow the per-connector guide for ext_authz, forwardAuth, or sidecar_proxy wiring and example configs.

## Path 3: External Use From Source

For Envoy and Traefik, do not treat source-building the proxy itself as repository-supported. Source-based external use applies to libmodsecurity and any operator-provided decision backend. For Lighttpd, the repository helper can build the pinned Lighttpd runtime locally, but that remains a sidecar_proxy path and not a native connector.

## Per-Connector Guides

- [Envoy](COMPILE_ENVOY.md)
- [Traefik](COMPILE_TRAEFIK.md)
- [Lighttpd](COMPILE_LIGHTTPD.md)

## Claims Not Allowed

Open connector evidence must not claim:

- `production_ready = true`
- `full_matrix_ready = true`
- `crs_complete = true`
- `response_body_verified = true`

Lighttpd Phase 1 evidence must also not claim a native Lighttpd module.
