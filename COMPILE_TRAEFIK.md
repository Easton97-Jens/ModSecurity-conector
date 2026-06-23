# Compile / Prepare Traefik

## Inhaltsverzeichnis

- [Purpose](#purpose)
- [Current Status / Supported Claim](#current-status-supported-claim)
- [External Use Overview](#external-use-overview)
- [Components Needed Outside This Repository](#components-needed-outside-this-repository)
- [Option A: Use Distribution Packages Where Compatible](#option-a-use-distribution-packages-where-compatible)
- [Option B: Build libmodsecurity v3 From Source](#option-b-build-libmodsecurity-v3-from-source)
- [Build / Prepare This Connector Or Runtime Path](#build-prepare-this-connector-or-runtime-path)
- [Install The Built Artifact Into An External System](#install-the-built-artifact-into-an-external-system)
- [Wire Configuration](#wire-configuration)
- [Start / Reload / Restart](#start-reload-restart)
- [Logs And Runtime Evidence In A Real Deployment](#logs-and-runtime-evidence-in-a-real-deployment)
- [Example Configs](#example-configs)
- [Optional Repository Validation](#optional-repository-validation)
- [Troubleshooting](#troubleshooting)
- [Non-Claims / Limits](#non-claims-limits)
- [Related Docs](#related-docs)

## Purpose

Explain the external Traefik integration pattern documented by this repository without claiming production readiness.

## Current Status / Supported Claim

Traefik is a pinned runtime prepare flow in this repository, not a source build. The current status is example/smoke evidence only and not production-ready.

## External Use Overview

The external pattern is `forwardAuth` plus an operator-provided decision service or sidecar. This repository provides example configuration and smoke paths, but not a complete production service.

## Components Needed Outside This Repository

- Traefik runtime binary, from a distribution/vendor package or repository prepare flow.
- A reachable `forwardAuth` decision service.
- libmodsecurity if the decision service uses it.
- ModSecurity rules/CRS and writable logs.

## Option A: Use Distribution Packages Where Compatible

Use a distribution or vendor runtime package when it matches your deployment needs. Package names, service names, and paths are operator-specific and are not guaranteed by this repository.

## Option B: Build libmodsecurity v3 From Source

This repository's local smoke flow prepares libmodsecurity through framework helpers and pinned variables. For an external deployment, the following is a standard upstream-style example, not a repository-owned guarantee. Verify the selected `<modsecurity-v3-ref>`, dependencies, and flags against your operating system and the upstream ModSecurity documentation before use.

```sh
git clone --depth 1 -b <modsecurity-v3-ref> https://github.com/owasp-modsecurity/ModSecurity.git ModSecurity-v3
cd ModSecurity-v3
git submodule update --init --recursive
./build.sh
./configure --prefix=/usr/local/modsecurity
make -j"$(nproc)"
sudo make install
```

Replace `<modsecurity-v3-ref>` with the ref chosen by your deployment or with the repository/framework pin after you have verified it in the framework source. If your distribution provides a compatible `libmodsecurity-dev`, you may not need this source build.

## Build / Prepare This Connector Or Runtime Path

Repository runtime preparation command:

```sh
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
```

This prepares/stages the repository-supported runtime component or build path where implemented. It is not a global production installation.

## Install The Built Artifact Into An External System

No production install target is provided by this repository for this path. Copy or reference the staged runtime binary and configuration according to your process manager and deployment layout. Use placeholders such as `<traefik-bin>` until you have resolved the actual staged or packaged binary path.

## Wire Configuration

Adapt the example config for your listener, backend, decision service address, rules, CRS, and log paths. Do not assume the repository starts a production decision service.

## Start / Reload / Restart

Production-style placeholder command:

```sh
<traefik-bin> --configFile=examples/traefik/traefik-static.yaml
```

Replace the placeholder binary with the actual runtime binary. Decision service startup is operator-provided unless a real production service command exists in your deployment.

## Logs And Runtime Evidence In A Real Deployment

Inspect runtime logs, decision-service logs, and ModSecurity audit/decision logs when the selected backend supports them. Preserve the runtime binary path, config file, rules file, CRS version, and sidecar command used.

## Example Configs

Use the files in [examples/traefik/README.md](examples/traefik/README.md) as starting points for external configuration. They are not automatically installed by the repository.

## Optional Repository Validation

These commands validate repository evidence. They are not the external installation procedure.

```sh
git submodule update --init --recursive
make setup-dev
make lint
git diff --check
```
```sh
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
make smoke-traefik
make smoke-traefik-modsecurity
make smoke-traefik-crs
```

## Troubleshooting

Check missing runtime binary, unreachable decision service, missing libmodsecurity backend, missing CRS/rules, and unwritable logs. Treat blocked runs as blocked, not success.

## Non-Claims / Limits

- Traefik is not compiled from source by this repository.
- This is not production-ready proof.
- No Go plugin implementation is provided here.
- The forwardAuth decision service startup is operator-provided unless your deployment adds one.
- RESPONSE_BODY is not verified or promoted.
- Force-all FAIL rows are not production support.

## Related Docs

- [examples/traefik/README.md](examples/traefik/README.md)
- `connectors/traefik/docs/build.md`
- `connectors/traefik/docs/validation.md`
