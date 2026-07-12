# Traefik Strict profile boundary

**Language:** English | [Deutsch](README.de.md)

## Status

Common Runtime accepts `phase4_mode=strict`, but the native Go middleware
downgrades post-commit disruptive P4 decisions to log-only. Strict is optional
and no abort profile is claimed.

## Use

Keep the Safe UDS setup, validate static/dynamic configuration and the engine
service, and require new host evidence before making a strict transport claim.
