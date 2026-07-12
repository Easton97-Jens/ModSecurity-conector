<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# lighttpd limitations

**Language:** English | [Deutsch](limitations.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Boundaries

Host-patch, compression, optional protocol profiles, and strict enforcement remain explicitly bounded by current evidence.

## Not covered by this guide

Strict transport enforcement beyond the selected evidence, complete HTTP/2 or HTTP/3 verification, CRS verification, full extended-matrix execution, compression behavior, and production suitability remain separate work.

## Compatibility paths

Compatibility configurations are kept separately in `examples/` and must not be cited as selected full-lifecycle proof.
