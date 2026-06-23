# Compile Lighttpd

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

Explain the external Lighttpd integration pattern documented by this repository without claiming production readiness.

## Current Status / Supported Claim

Lighttpd is a sidecar_proxy / Phase 1 path. A native Lighttpd ModSecurity module is not implemented. The `-tt`, `-D`, and `-f` flags are documented by `lighttpd(8)` and are used here as operator-style commands; operators must still validate them against the staged or packaged binary in their environment.

## External Use Overview

The external pattern is `sidecar_proxy` plus an operator-provided decision service or sidecar. This repository provides example configuration and smoke paths, but not a complete production service.

## Components Needed Outside This Repository

- Lighttpd runtime, either staged by this repository or supplied by the operator.
- Lighttpd proxy config.
- Reachable sidecar/decision backend.
- libmodsecurity if the backend uses it.
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
ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
```

This prepares/stages the repository-supported runtime component or build path where implemented. It is not a global production installation.

## Install The Built Artifact Into An External System

No production install target is provided by this repository for this path. Copy or reference the staged runtime binary and configuration according to your process manager and deployment layout. Use placeholders such as `<lighttpd-bin>` until you have resolved the actual staged or packaged binary path.

## Wire Configuration

Adapt the example config for your listener, backend, decision service address, rules, CRS, and log paths. Do not assume the repository starts a production decision service.

## Start / Reload / Restart

Production-style placeholder command:

```sh
<lighttpd-bin> -tt -f examples/lighttpd/lighttpd-sidecar-proxy.conf
<lighttpd-bin> -D -f examples/lighttpd/lighttpd-sidecar-proxy.conf
```

Replace the placeholder binary with the actual runtime binary. Decision service startup is operator-provided unless a real production service command exists in your deployment.

## Logs And Runtime Evidence In A Real Deployment

Inspect runtime logs, decision-service logs, and ModSecurity audit/decision logs when the selected backend supports them. Preserve the runtime binary path, config file, rules file, CRS version, and sidecar command used.

## Example Configs

Use the files in [examples/lighttpd/README.md](examples/lighttpd/README.md) as starting points for external configuration. They are not automatically installed by the repository.

## Optional Repository Validation

These commands validate repository evidence. They are not the external installation procedure.

```sh
git submodule update --init --recursive
make setup-dev
make lint
git diff --check
```
```sh
ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
make smoke-lighttpd
make smoke-lighttpd-modsecurity
make smoke-lighttpd-crs
```

## Troubleshooting

Check missing runtime binary, unreachable decision service, missing libmodsecurity backend, missing CRS/rules, and unwritable logs. Treat blocked runs as blocked, not success.

## Non-Claims / Limits

- Lighttpd can be staged from a pinned source tarball here, or operators can use their own compatible Lighttpd.
- There is no native Lighttpd ModSecurity connector in this repository.
- The current pattern is `sidecar_proxy` / Phase 1 and is not production-ready proof.
- FastCGI/SCGI/mod_magnet/Lua are not implemented here.
- RESPONSE_BODY is not verified or promoted.
- Force-all FAIL rows are not production support.

## Related Docs

- [examples/lighttpd/README.md](examples/lighttpd/README.md)
- `connectors/lighttpd/docs/build.md`
- `connectors/lighttpd/docs/validation.md`
