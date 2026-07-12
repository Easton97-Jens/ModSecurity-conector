<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Common SDK contract

**Language:** English | [Deutsch](sdk.de.md)

## Scope

The SDK provides neutral configuration, request/response mapping contracts, event primitives, and validation helpers. It does not expose Apache, NGINX, HAProxy, Envoy, Traefik, or lighttpd types.

An adapter validates host metadata before passing it to the SDK and keeps ownership at the adapter boundary.

This guide describes the current selected six-connector HTTP/1.1 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Variables and paths

Recurring values such as `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT`, and `NO_CRS_RUN_ID` are defined in the [central variables reference](../../configuration/variables.md). Repository-relative paths start at the repository root; run, cache, and evidence paths are outside the Git worktree.

## Validation

Run the documented Make target from the repository root and keep the generated evidence boundary with the result.
