<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# HAProxy testing

**Language:** English | [Deutsch](testing.de.md)

## Scope

This guide describes the current selected HTTP/1.1 P1–P4 core. It does not claim production readiness, complete CRS, HTTP/2, or HTTP/3 verification, or Strict verification for every connector.

## Levels

Run `make build-haproxy`, `make check-config-haproxy`, any available start/runtime smoke, and `make full-lifecycle-haproxy` as separate levels. Build, configuration, and start are not rule-engine PASS.

## No-CRS core rules and cases

These rule IDs belong to the repository-owned No-CRS test profile, not OWASP CRS.

| Rule ID | Phase | Purpose |
| ---: | --- | --- |
| `1100001` | P1 | Request-header deny |
| `1100101` | P2 | Request-body deny |
| `1100201` | P3 | Response-header deny |
| `1100301` | P4 | Response-body deny or Safe late intervention |

## Evidence and run boundary

Case IDs identify a capability and expected state. A selected case needs attributable result/event evidence, profile identity, and the configured run ID. A PASS aggregate must not be inferred from build output.

## Statuses

`PASS`, `FAIL`, `BLOCKED`, `NOT EXECUTED`, `NOT APPLICABLE`, and `UNSUPPORTED` are defined in [test levels](../../testing/test-levels.md).
