# Compile HAProxy

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

Explain how to use the repository's HAProxy ModSecurity SPOA process with an external HAProxy deployment.

## Current Status / Supported Claim

The HAProxy path uses HAProxy SPOE/SPOP plus a repository-built `haproxy-modsecurity-spoa` process linked to libmodsecurity. RESPONSE_BODY remains bounded runtime evidence only.

## External Use Overview

HAProxy can be distro-provided or locally built. This repository builds the SPOA process. HAProxy loads SPOE configuration, connects over SPOP to the SPOA process, the SPOA process loads ModSecurity rules and libmodsecurity, and decision/audit logs are written by the SPOA path.

## Components Needed Outside This Repository

- HAProxy with SPOE/SPOP support.
- libmodsecurity v3 headers/libraries available to build and run the SPOA process.
- `haproxy-modsecurity-spoa` built from `connectors/haproxy`.
- HAProxy config, SPOE config, SPOA agent config, ModSecurity rules, optional CRS, and writable decision/audit logs.
- An operator-provided service unit or process manager for the SPOA process.

## Option A: Use Distribution Packages Where Compatible

Use distribution HAProxy and libmodsecurity packages when they are compatible with your target system. Package names vary; verify HAProxy SPOE support and libmodsecurity development/runtime files before building the SPOA process.

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

Repository build commands:

```sh
make prepare-runtime-components
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-spoa-runtime
```

The built SPOA binary path is controlled by the connector Makefile defaults, including `BUILD_ROOT` and `HAPROXY_SPOA_RUNTIME_DIR`. Replace install placeholders with the actual built path.

## Install The Built Artifact Into An External System

```sh
sudo install -d -m 0755 /etc/haproxy /etc/modsecurity /var/log/haproxy-modsecurity
sudo install -m 0755 <built-haproxy-modsecurity-spoa> /usr/local/sbin/haproxy-modsecurity-spoa
sudo install -m 0644 examples/haproxy/spoe-modsecurity.conf /etc/haproxy/spoe-modsecurity.conf
sudo install -m 0644 examples/haproxy/modsecurity-agent.conf /etc/haproxy/modsecurity-agent.conf
sudo install -m 0644 examples/haproxy/haproxy-request-only.cfg /etc/haproxy/haproxy.cfg
```

`<built-haproxy-modsecurity-spoa>` must be replaced with the verified built binary path.

## Wire Configuration

HAProxy loads `spoe-modsecurity.conf` through the `filter spoe engine modsecurity` configuration. HAProxy sends request metadata to the SPOP backend. The SPOA process loads the agent config and ModSecurity rules, then returns variables that HAProxy uses to allow, deny, redirect, or drop.

## Start / Reload / Restart

Validate and reload HAProxy:

```sh
sudo haproxy -c -f /etc/haproxy/haproxy.cfg
sudo systemctl reload haproxy
```

No systemd unit is provided by this repository for `haproxy-modsecurity-spoa`. Start the SPOA binary with the configuration method supported by the built binary; see `examples/haproxy/modsecurity-agent.conf`. The source supports `--config PATH`, so an operator-managed invocation may look like:

```sh
sudo /usr/local/sbin/haproxy-modsecurity-spoa --config /etc/haproxy/modsecurity-agent.conf
```

Use a process manager of your choice for restarts.

## Logs And Runtime Evidence In A Real Deployment

Inspect HAProxy logs, `/var/log/haproxy-modsecurity/decision.jsonl`, `/var/log/haproxy-modsecurity/audit.log`, and the SPOA diagnostic log configured by the agent file.

## Example Configs

Use the files in [examples/haproxy/](examples/haproxy/README.md) as starting points for external configuration. They are not automatically installed by the repository.

## Optional Repository Validation

These commands validate repository evidence. They are not the external installation procedure.

```sh
git submodule update --init --recursive
make setup-dev
make lint
git diff --check
```
```sh
make smoke-haproxy
make test-haproxy-no-crs
make test-haproxy-with-crs
```

## Troubleshooting

Check SPOP backend reachability, SPOE config syntax, HAProxy frame/body limits, libmodsecurity library paths, ModSecurity rule paths, and writable decision/audit log directories.

## Non-Claims / Limits

- RESPONSE_BODY / Phase 4 is bounded runtime evidence only, not promoted support.
- Force-all FAIL rows are not production support.
- No systemd unit is provided by this repository.

## Related Docs

- [examples/haproxy/README.md](examples/haproxy/README.md)
- `connectors/haproxy/docs/build.md`
- `connectors/haproxy/docs/validation.md`
