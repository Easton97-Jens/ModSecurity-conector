# Traefik forwardAuth Example

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

Example only. This does not prove production readiness. The repository prepares a pinned Traefik release archive/binary and exercises a `forwardAuth` smoke path when required local runtime components exist. Traefik is not compiled from source by this repository.

## Needed Components

- Pinned Traefik binary staged by `make prepare-traefik-runtime`.
- A reachable forwardAuth decision service.
- libmodsecurity when `DECISION_BACKEND=libmodsecurity` is used.
- ModSecurity rules and optional CRS when a CRS smoke is used.

## Config Files

- `traefik-static.yaml`: illustrative static entry point and file provider.
- `traefik-dynamic.yaml`: illustrative router/service/middleware using `forwardAuth`.

## Start / Reload Notes

Static config changes require restarting Traefik. File-provider dynamic config may be reloaded by Traefik when watching is enabled. Restart the authorization service after rule, library, or backend changes.

## Logs

Use Traefik logs/access logs plus authorization-service decision and audit logs. Paths here are illustrative.


## External Usage

This directory contains example configs for external usage. They are starting points only and are not universal production defaults. The matching compile guide explains how to build or prepare the required artifact: `Traefik forwardAuth config`. Copy or adapt only the files that match your deployment; paths such as `/etc/...`, `/usr/lib/...`, `127.0.0.1`, ports, backend URLs, and log paths are placeholders unless they match your system.

Service context: Traefik plus operator-provided decision service. After adapting the files, restart Traefik for static config and restart the operator-provided decision service. Inspect Traefik logs plus decision-service audit/decision logs.

## Non-Claims

- Not production-ready proof.
- Not full matrix proof.
- Not CRS-complete proof.
- Not response-body verification.
- Not a Traefik source-build recipe.
- Not a Go plugin implementation.

## Related Compile Doc

See [COMPILE_TRAEFIK.md](../../COMPILE_TRAEFIK.md).
