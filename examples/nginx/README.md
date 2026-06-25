Language: English | [Deutsch](README.de.md)

# NGINX ModSecurity Examples

## Table of Contents

- [Status](#status)
- [Purpose](#purpose)
- [Needed Components](#needed-components)
- [Files](#files)
- [Production Paths](#production-paths)
- [Request-Only Mode](#request-only-mode)
- [Phase 4 / RESPONSE_BODY Mode](#phase-4-response_body-mode)
- [Variable And Placeholder Reference](#variable-and-placeholder-reference)
- [Logging And Evidence](#logging-and-evidence)
- [Security Notes](#security-notes)
- [External Usage](#external-usage)
- [Non-Claims](#non-claims)
- [Related Docs](#related-docs)

## Status

NGINX dynamic-module request-only and bounded strict-abort examples. Production-style, but not proof of every NGINX build, module ABI, or complete RESPONSE_BODY support.

## Purpose

These examples show production-style NGINX configuration for request-only
ModSecurity and bounded strict-abort Phase 4 / RESPONSE_BODY evidence.

## Needed Components

NGINX and `ngx_http_modsecurity_module.so` built for a compatible NGINX ABI, libmodsecurity v3, ModSecurity rules, optional CRS, and writable NGINX/ModSecurity log locations.

## Files

- `nginx-modsecurity-request-only.conf`: NGINX module and request-only
  directives.
- `modsecurity-request-only.conf`: libmodsecurity request-phase rules config.
- `nginx-modsecurity-phase4-strict-abort.conf`: NGINX connector directives for
  bounded strict-abort Phase 4 behavior.
- `modsecurity-phase4.conf`: libmodsecurity response-body rules config.

## Production Paths

The examples use common NGINX and ModSecurity paths:

- `modules/ngx_http_modsecurity_module.so`
- `/etc/nginx/nginx.conf`
- `/etc/modsecurity/modsecurity-request-only.conf`
- `/etc/modsecurity/modsecurity-phase4.conf`
- `/etc/modsecurity/crs/`
- `/var/log/modsecurity/nginx-phase4.jsonl`
- `/var/log/modsecurity/nginx-audit.log`
- `/var/log/nginx/access.log`
- `/var/log/nginx/error.log`

## Request-Only Mode

Request-only mode loads `ngx_http_modsecurity_module`, enables `modsecurity on`,
and points `modsecurity_rules_file` at a config with `SecResponseBodyAccess
Off`.

```bash
nginx -t
nginx -s reload
```

## Phase 4 / RESPONSE_BODY Mode

The strict-abort example enables `SecResponseBodyAccess On` and
`modsecurity_phase4_mode strict`. The connector can record late interventions
and abort an already-started transfer. That is runtime evidence, not full
buffering parity and not a promoted RESPONSE_BODY capability.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented as runtime evidence only.

## Variable And Placeholder Reference

| Name | Type | Required | Example value | Used in | Meaning | Change requires restart/reload | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `load_module` | NGINX directive | Yes | `modules/ngx_http_modsecurity_module.so` | `nginx-modsecurity-*.conf` | Loads the NGINX connector module. | restart | Dynamic modules are loaded at master start. |
| `modsecurity` | NGINX directive | Yes | `on` | `nginx-modsecurity-*.conf` | Enables ModSecurity in the configured scope. | reload | Use in `http`, `server`, or `location` as appropriate. |
| `modsecurity_rules_file` | NGINX directive | Yes | `/etc/modsecurity/modsecurity-request-only.conf` | `nginx-modsecurity-*.conf` | Points NGINX to the libmodsecurity rules file. | reload | Use the Phase 4 rules file only for bounded response evidence. |
| `modsecurity_phase4_mode` | NGINX directive | Phase 4 only | `strict` | `nginx-modsecurity-phase4-strict-abort.conf` | Selects strict-abort response behavior. | reload | May abort an already-started response. |
| `modsecurity_phase4_content_types_file` | NGINX directive | Phase 4 only | `/etc/modsecurity/phase4-content-types.conf` | `nginx-modsecurity-phase4-strict-abort.conf` | Optional allow-list for response-body MIME types. | reload | Keep narrow in production. |
| `modsecurity_phase4_log` | NGINX directive | Phase 4 only | `/var/log/modsecurity/nginx-phase4.jsonl` | `nginx-modsecurity-phase4-strict-abort.conf` | JSONL connector decision evidence. | reload | Rotate with normal log rotation. |
| `gzip` | NGINX directive | No | `off` | `nginx-modsecurity-phase4-strict-abort.conf` | Keeps compression disabled during validation. | reload | Verify byte ordering before enabling compression. |
| `proxy_pass` | NGINX directive | Yes | `http://app_backend` | `nginx-modsecurity-*.conf` | Example upstream application route. | reload | Replace with production upstreams. |
| `SecRuleEngine` | ModSecurity directive | Yes | `On` | `modsecurity-*.conf` | Enables rule execution. | reload | Use `DetectionOnly` for non-disruptive rollout. |
| `SecRequestBodyAccess` | ModSecurity directive | Yes | `On` | `modsecurity-*.conf` | Enables request-body processing. | reload | Request body support is separate from RESPONSE_BODY. |
| `SecResponseBodyAccess` | ModSecurity directive | Yes | `Off` or `On` | `modsecurity-*.conf` | Enables or disables RESPONSE_BODY processing. | reload | `On` remains bounded strict-abort evidence. |
| `SecResponseBodyMimeType` | ModSecurity directive | Phase 4 only | `text/plain text/html application/json` | `modsecurity-phase4.conf` | Limits inspected response MIME types. | reload | Keep explicit to avoid binary responses. |
| `SecResponseBodyLimit` | ModSecurity directive | Phase 4 only | `1048576` | `modsecurity-phase4.conf` | Bounds libmodsecurity response-body buffering. | reload | Do not rely on unbounded buffering. |
| `SecResponseBodyLimitAction` | ModSecurity directive | Phase 4 only | `ProcessPartial` | `modsecurity-phase4.conf` | Defines behavior when the body exceeds the limit. | reload | Keep aligned with production risk policy. |
| `IncludeOptional` | ModSecurity directive | No | `/etc/modsecurity/crs/rules/*.conf` | `modsecurity-*.conf` | Includes CRS files if present. | reload | Missing CRS files do not block startup. |
| `SecAuditEngine` | ModSecurity directive | No | `RelevantOnly` | `modsecurity-*.conf` | Enables audit logging for relevant transactions. | reload | Use with log rotation. |
| `SecAuditLog` | ModSecurity directive | No | `/var/log/modsecurity/nginx-audit.log` | `modsecurity-*.conf` | Audit log destination. | reload | Ensure NGINX workers can write it. |
| `RESPONSE_BODY` | ModSecurity collection | Phase 4 only | `@contains response-attack` | `modsecurity-phase4.conf` | Example outbound rule target. | reload | Replace the example rule with production rules. |

## Logging And Evidence

Connector Phase 4 decisions are JSON lines in `nginx-phase4.jsonl`. Audit
records are generated by libmodsecurity through `SecAuditLog`. Access and error
logs remain under `/var/log/nginx`.

## Security Notes

Keep request-only mode as the baseline, verify module ABI compatibility with
the deployed NGINX binary, validate response-body behavior with compression
disabled first, and preserve strict-abort evidence when testing outbound rules.


## External Usage

This directory contains example configs for external usage. They are starting points only and are not universal production defaults. The matching compile guide explains how to build or prepare the required artifact: `ngx_http_modsecurity_module.so`. Copy or adapt only the files that match your deployment; paths such as `/etc/...`, `/usr/lib/...`, `127.0.0.1`, ports, backend URLs, and log paths are placeholders unless they match your system.

Service context: NGINX. After adapting the files, nginx -t and reload the NGINX service. Inspect NGINX error/access logs and ModSecurity audit logs.

## Non-Claims

- These examples are not a blanket production-readiness certification.
- They do not prove every package/version/layout.
- Phase 4 / RESPONSE_BODY examples are bounded runtime evidence only, not promoted full support.

## Related Docs

- [COMPILE_NGINX.md](../../COMPILE_NGINX.md)
- `connectors/nginx/docs/build.md`
- `connectors/nginx/docs/validation.md`
- `reports/testing/nginx-poc.md`
