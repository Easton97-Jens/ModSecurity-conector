# Connector Directive Parity

Status: current adapter-owned Apache and NGINX code

This document records directive support in the local adapter-owned connectors.
It describes the current code state only; it does not promote deferred runtime
paths or claim future parity work as implemented.

## Directive Matrix

| Directive | Apache | NGINX | Apache Semantics | NGINX Semantics | Notes / Risk |
| --- | --- | --- | --- | --- | --- |
| `modsecurity` | Supported | Supported | `on` or `off`; available in server and directory context. | `on` or `off`; available in main, server, and location context. | SAFE: shared directive metadata. |
| `modsecurity_rules` | Supported | Supported | Loads inline ModSecurity rules into the Apache context rules set. | Loads inline ModSecurity rules into the NGINX context rules set. | CAREFUL: rules-loading behavior remains connector-owned. |
| `modsecurity_rules_file` | Supported | Supported | Loads ModSecurity rules from a local file. | Loads ModSecurity rules from a local file. | CAREFUL: rules-loading behavior remains connector-owned. |
| `modsecurity_rules_remote` | Supported | Supported | Loads remote rules using the configured key and URL arguments. | Loads remote rules using the configured key and URL arguments. | CAREFUL: remote rules-loading behavior remains connector-owned. |
| `modsecurity_use_error_log` | Supported | Supported | `on` or `off`; default is on. `off` suppresses Apache error-log forwarding from the libmodsecurity log callback only. | `on` or `off`; default is on. `off` suppresses the connector's NGINX error-log write from the libmodsecurity log callback. | CAREFUL: logging policy only; audit log, intervention, request, and response behavior are unchanged. |
| `modsecurity_transaction_id` | Supported | Supported | Static string only. If unset, Apache keeps the existing `UNIQUE_ID` fallback, then creates a transaction without an explicit ID. | NGINX complex value. Values may be evaluated per request by NGINX. | CAREFUL: transaction-ID selection is per connector. Apache does not do expression or environment interpolation. |
| `modsecurity_phase4_mode` | Not supported | Supported | Not implemented. | Selects phase-4 response-body mode: `minimal`, `safe`, or `strict`; default is `safe`. | RISKY: response-body, filter, and intervention paths. Apache parity is intentionally deferred. |
| `modsecurity_phase4_content_types_file` | Not supported | Supported | Not implemented. | Loads the phase-4 response content-type allow list from a file. | RISKY: response-body content-type gating. Apache parity is intentionally deferred. |
| `modsecurity_phase4_log` | Not supported | Supported | Not implemented. | Configures phase-4 diagnostic logging. | RISKY: phase-4 runtime diagnostics. Apache parity is intentionally deferred. |

## Apache Directives

The Apache connector currently registers:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_use_error_log on|off`
- `modsecurity_transaction_id <string>`

`modsecurity_transaction_id` is intentionally minimal: it accepts a static
string. It does not evaluate Apache expressions, expand environment variables,
or attempt NGINX complex-value parity. If the directive is not set, Apache keeps
the existing `UNIQUE_ID` fallback and then falls back to creating a transaction
without an explicit ID.

`modsecurity_use_error_log off` only suppresses Apache error-log forwarding from
the libmodsecurity log callback. It does not change audit logging,
interventions, hooks, filters, buckets, transaction ownership, or request and
response handling.

Apache does not currently implement the NGINX phase-4 directives:

- `modsecurity_phase4_mode`
- `modsecurity_phase4_content_types_file`
- `modsecurity_phase4_log`

## NGINX Directives

The NGINX connector currently registers:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_transaction_id`
- `modsecurity_use_error_log on|off`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`

NGINX `modsecurity_transaction_id` uses an NGINX complex value and may evaluate
per-request variables. The NGINX phase-4 directives remain NGINX-specific
runtime controls and are not a common connector contract.

## Deferred and Risky Areas

Apache phase-4 parity is intentionally not implemented yet. Response body
behavior remains not promoted, and `RESPONSE_BODY` is not treated as a verified
blocking capability by this documentation update.

Bucket brigades, input and output filters, intervention runtime paths, hook
registration, transaction ownership, and request/response lifecycle behavior
remain connector-specific runtime areas. They are outside this documentation
change and must not be moved to `common/` without a separate design and smoke
evidence.

## Common Metadata

`common/include/msconnector/directives.h` contains shared directive-name
metadata used by both Apache and NGINX.

`common/include/msconnector/options.h` contains shared option/default metadata.
NGINX currently uses the common defaults for enablement, error-log forwarding,
and phase-4 mode. Apache uses common bool values for error-log policy.

These headers contain no Apache types, no NGINX types, no hooks, no filters, no
bucket brigades, no transaction ownership, and no request or response-body
runtime behavior.
