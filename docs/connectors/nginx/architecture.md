<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# NGINX architecture

**Language:** English | [Deutsch](architecture.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Host integration

native NGINX HTTP module. Common receives only neutral mapped values; host APIs, allocation, and callback lifetime remain outside Common.

## Transaction lifecycle

| Phase | Meaning |
| --- | --- |
| P1 | Request headers before the upstream request |
| P2 | Request body; finish at request EOS |
| P3 | Response headers |
| P4 | Response body; finish at response EOS |

## Data flow and engine binding

The adapter passes borrowed header and body slices to Common. Common calls the engine through its neutral interface; host-specific types, buffers, and callbacks are never passed into Common.

## Ownership and lifetime

Body chunks are not fully buffered by the connector. Events and reports retain no raw request or response body. Adapter cleanup follows the host lifecycle end and remains attributable to the same transaction.
