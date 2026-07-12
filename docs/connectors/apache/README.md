<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Apache Connector

**Language:** English | [Deutsch](README.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Selected integration mode

`native-httpd-module` — Apache httpd module built through APXS.

## Current core

HTTP/1.1 P1–P4 with Safe post-commit Phase 4 semantics, first byte before EOS evidence, and no connector-owned full response buffer.

## Quick links

- [Architecture](architecture.md)
- [Build](build.md)
- [Configuration](configuration.md)
- [Lifecycle](lifecycle.md)
- [Testing](testing.md)
- [Operations](operations.md)
- [Limitations](limitations.md)
