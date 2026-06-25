Language: English | [Deutsch](README.de.md)

# Lighttpd sidecar_proxy Example

## Table of Contents

- [Status](#status)
- [Needed Components](#needed-components)
- [Config Files](#config-files)
- [Start / Reload Notes](#start-reload-notes)
- [Logs](#logs)
- [External Usage](#external-usage)
- [Non-Claims](#non-claims)
- [Related Compile Doc](#related-compile-doc)

## Status

Example only. This does not prove production readiness. The current repository path is `sidecar_proxy` / Phase 1. There is no native Lighttpd ModSecurity connector in this repository.

## Needed Components

- Lighttpd binary built from the pinned source tarball by `ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build`.
- A reachable ModSecurity sidecar/proxy or decision backend.
- libmodsecurity when `DECISION_BACKEND=libmodsecurity` is used.
- ModSecurity rules and optional CRS when a CRS smoke is used.

## Config Files

- `lighttpd-sidecar-proxy.conf`: illustrative Lighttpd frontend/proxy wiring to an application backend. The ModSecurity sidecar path is described as external; no native module is loaded.

## Start / Reload Notes

Validate Lighttpd config with the staged binary before running it. Restart or reload Lighttpd according to local process-management policy after config changes. Restart the sidecar after rule, library, or backend changes.

## Logs

Use Lighttpd access/error logs plus sidecar decision and audit logs. Paths here are illustrative.


## External Usage

This directory contains example configs for external usage. They are starting points only and are not universal production defaults. The matching compile guide explains how to build or prepare the required artifact: `Lighttpd sidecar_proxy config`. Copy or adapt only the files that match your deployment; paths such as `/etc/...`, `/usr/lib/...`, `127.0.0.1`, ports, backend URLs, and log paths are placeholders unless they match your system.

Service context: Lighttpd plus operator-provided sidecar/decision backend. After adapting the files, validate/reload Lighttpd and restart the sidecar/decision backend. Inspect Lighttpd logs plus sidecar audit/decision logs.

## Non-Claims

- Not production-ready proof.
- Not a native Lighttpd ModSecurity module.
- Not FastCGI/SCGI integration.
- Not mod_magnet/Lua integration.
- Not full matrix, CRS-complete, or response-body verification.

## Related Compile Doc

See [COMPILE_LIGHTTPD.md](../../COMPILE_LIGHTTPD.md).
