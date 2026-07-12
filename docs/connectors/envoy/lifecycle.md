<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Envoy lifecycle

**Language:** English | [Deutsch](lifecycle.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Phases and EOS

| Phase | Meaning |
| --- | --- |
| P1 | Request headers |
| P2 | Request body; finish at request EOS |
| P3 | Response headers |
| P4 | Response body; finish at response EOS |

## Pre-commit and post-commit

Before response commitment, a host may take a supported pre-commit action. After commitment, Safe records `log_only`; Safe does not claim a rewritten visible status. Safe is the selected documented core mode. Strict enforcement and `ext_authz` compatibility are separate work.

## First byte, buffering, and cleanup

The selected evidence requires first-byte-before-EOS observation where applicable and rejects a connector-owned full response buffer. Lifecycle counters, events, and cleanup must be attributable to the same transaction.
