<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Six-connector core lifecycle

**Language:** English | [Deutsch](core-lifecycle.de.md)

## Scope

The selected current core covers HTTP/1.1 P1–P4, Safe post-commit P4 semantics, first byte before EOS evidence, and no connector-owned full response buffer for Apache, NGINX, HAProxy, Envoy, Traefik, and lighttpd.

The selected current core covers HTTP/1.1 P1–P4, Safe post-commit P4 semantics, first byte before EOS evidence, and no connector-owned full response buffer for Apache, NGINX, HAProxy, Envoy, Traefik, and lighttpd.

This guide describes the current selected six-connector HTTP/1.1 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Variables and paths

Recurring values such as `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT`, and `NO_CRS_RUN_ID` are defined in the [central variables reference](../configuration/variables.md). Repository-relative paths start at the repository root; run, cache, and evidence paths are outside the Git worktree.

## Status and exit values

`PASS` means a checked claim was met; `FAIL` a negative check; `BLOCKED` a missing prerequisite; `NOT EXECUTED` no execution; `NOT APPLICABLE` no applicability; and `UNSUPPORTED` no host-provided capability. Process code `0` means technical completion, `1` a general error, `2` a validation/aggregate error, and `77` a declared missing optional prerequisite.

## Validation

Run the documented Make target from the repository root and keep the generated evidence boundary with the result.
