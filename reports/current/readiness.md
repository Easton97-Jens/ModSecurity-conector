# Connector readiness

**Language:** English | [Deutsch](readiness.de.md)

## Current evidence boundary

The selected real HTTP/1.1 host paths completed the shared canonical run
`six-connectors-core-final-20260712T164725Z-e16e7f1`. Every selected runner
and the aggregate `full-lifecycle-all-connectors` target exited `0`; the
read-only `make check-six-connector-core-completion` gate passed.

This is bounded Common/libmodsecurity host evidence for the selected core. It
does not replace run-local artifacts and does not establish a complete
connector matrix, a capability promotion, or a production outcome.

| Connector | Selected integration | Selected HTTP/1.1 core | Extended catalog | Scope boundary |
| --- | --- | --- | --- | --- |
| Apache | `native-httpd-module` | PASS | NOT EXECUTED | Selected P1--P4 core only |
| NGINX | `native-nginx-http-module` | PASS | NOT EXECUTED | Selected P1--P4 core only |
| HAProxy | `native-htx-filter` | PASS | NOT EXECUTED | Selected P1--P4 core only |
| Envoy | `ext_proc` | PASS | NOT EXECUTED | Selected P1--P4 core only |
| Traefik | `native-traefik-middleware` | PASS | NOT EXECUTED | Selected P1--P4 core only |
| lighttpd | `patched-native-lighttpd` | PASS | NOT EXECUTED | Selected P1--P4 core only |

The core covers the selected P1, P2, P3, P4 rule 1100301, Safe late-action,
first-byte-before-EOS, no-full-response-buffer, event-privacy, and cleanup
observations. The precise evidence rows and host-path details are in
[core completion](core-completion.md).

## Current technical boundaries

- A selected P4 Safe result is a post-commit requested `deny` with actual
  `log_only`, visible HTTP 200, sent headers/body, and no connection abort.
- Response-body chunks are ingested incrementally; the selected Phase-4 rule
  is evaluated at end of stream. This is not a per-chunk decision claim.
- Strict post-commit enforcement, HTTP/2, HTTP/3, compression handling, and
  the extended catalog remain separate hardening or evidence work.
- Capability declarations remain machine-readable in the generated
  [connector capability catalog](../testing/generated/canonical/connector-capabilities.generated.md).
  They are not substituted by prose status labels.

## Current sources of truth

| Topic | Canonical source |
| --- | --- |
| Selected six-connector core evidence | [core completion](core-completion.md) |
| Architecture, runtime-root, transport, and evidence audit | [architecture and evidence audit](../audits/architecture-and-evidence.md) |
| Generated capability declarations | [connector capability catalog](../testing/generated/canonical/connector-capabilities.generated.md) |
| Connector configuration options | [configuration inventory](../connector-configuration-inventory.json) and the linked example references |

Historical planning, pre-core snapshots, and per-connector No-CRS prose
snapshots were consolidated into these current sources. Git history retains
their chronology without keeping competing current status documents.

## Claims deliberately not made

- production readiness, production hardening, runtime security, or security
  verification;
- CRS verification, CRS completeness, or complete full-matrix verification;
- complete HTTP/2 or HTTP/3 verification; or
- strict post-commit enforcement outside the selected compact core.
