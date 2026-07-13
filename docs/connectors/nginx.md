# NGINX Connector

**Language:** English | [Deutsch](nginx.de.md)

## Overview

NGINX uses the selected <code>native-nginx-http-module</code> route. The
dynamic HTTP module maps NGINX request/response state to libmodsecurity v3
through connector-owned phases and filters. This guide covers the selected
HTTP/1.1 P1--P4 core only and makes no production, CRS, complete-matrix,
HTTP/2, HTTP/3, or strict-for-all-connectors claim.

## Architecture and ownership

Productive source lives under <code>connectors/nginx/src/</code>; module build
metadata is under <code>connectors/nginx/config</code>. NGINX owns main/location
configuration create/merge, access and log phases, header/body filters,
subrequest/end-of-stream treatment, dynamic module loading, and host action
mapping. Common provides neutral configuration, parser, mapping, limit, event,
and metadata contracts without owning <code>ngx_http_request_t</code> or an
NGINX filter.

| Lifecycle area | Selected NGINX responsibility | Boundary |
| --- | --- | --- |
| P1/P2 | Access-phase request mapping and body completion | Do not finalize a body before its selected end-of-stream |
| P3 | Response header filter mapping | Determine pre-commit state from the host response |
| P4 | Bounded body-filter ingestion and one-time EOS finalization | Preserve actual action and visible status after commitment |
| Logging | Payload-free event/result metadata | JSON/event truncation is distinct from body truncation |

## Build

Use [the NGINX compiler guide](../build/compilers/nginx.md) for source build,
dynamic-module inputs, component roots, and diagnostics. Required C17 checks
are structural/compile evidence; optional newer-language probes do not imply
runtime verification. The [NGINX source guide](../../connectors/nginx/README.md)
remains the code-adjacent entry point.

## Configuration

The complete NGINX syntax, values, defaults, contexts, merge behavior,
validation guidance, and profile examples are in the
[NGINX configuration reference](../../examples/nginx/configuration-reference.md).
Use NGINX variables only where the registered directive documents them.
<code>modsecurity_transaction_id_expr</code> is Apache-specific and is not an
NGINX directive.

## P1--P4 lifecycle and protocol boundary

P3 decisions belong to the response-header path before headers are committed.
The response-body filter is a separate P4 timing model. A P4 rule match does
not make a visible 403, abort, or HTTP/2 result without the corresponding
host/client artifacts.

| P4 question | Required observation |
| --- | --- |
| Rule observed | Selected native rule and phase-4 metadata |
| Pre-commit deny | A host path that is actually pre-commit for the selected response |
| Safe late result | Requested action, actual <code>log_only</code>, unchanged visible status, and late flag |
| Strict late result | Actual abort action, retained already-visible status, and client/host evidence |

An HTTP/2 build flag is not transport evidence. Where a host run records an
HTTP/2 applicability artifact, an unavailable feature remains not applicable
and an unexecuted protocol case remains not executed.

## Testing and evidence

Use <code>make check-config-nginx</code> for configuration validation and
<code>make full-lifecycle-nginx</code> for a selected native host run. Inspect
the selected run ID's result, event, effective configuration, host version,
and protocol applicability artifacts. The shared model is documented in
[Testing and evidence](../testing-and-evidence.md).

## Operations and troubleshooting

Use an external build/runtime/evidence root. For a module/configuration error,
inspect the source build inputs, dynamic module compatibility, and config-check
output. For P4 or protocol questions, inspect the response filter's recorded
commit/EOS context rather than extrapolating from a source option or an HTTP
status alone.

## Limitations and compatibility

NGINX syntax, contexts, inheritance, and expression semantics are
host-specific. Do not copy Apache expression directives into NGINX. Response-
body, strict late action, first-byte, no-full-buffer, and protocol properties
remain individually evidence-gated.

## Related references

- [Architecture](../architecture.md)
- [Configuration](../configuration.md)
- [Operations and security](../operations-and-security.md)
- [NGINX configuration reference](../../examples/nginx/configuration-reference.md)
