# Apache ModSecurity Examples

**Language:** English | [Deutsch](README.de.md)

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

Apache request-only and bounded Phase 4 examples. Production-style, but not proof of every Apache distribution package, MPM, or complete RESPONSE_BODY support.

## Purpose

These examples show production-style Apache httpd configuration for
request-only ModSecurity and bounded Phase 4 / RESPONSE_BODY evidence.

## Needed Components

Apache httpd/APXS and `mod_security3.so` built for the same Apache ABI, libmodsecurity v3, ModSecurity rules, optional CRS, and writable Apache/ModSecurity log locations.

## Files

- `apache-modsecurity-request-only.conf`: Apache module and request-only
  connector directives.
- `modsecurity-request-only.conf`: libmodsecurity request-phase rules config.
- `apache-modsecurity-phase4-buffered.conf`: Apache connector directives for
  bounded Phase 4 buffering.
- `modsecurity-phase4.conf`: libmodsecurity response-body rules config.

## Production Paths

The examples use common Debian-style paths:

- `/usr/lib/apache2/modules/mod_security3.so`
- `/etc/modsecurity/modsecurity-request-only.conf`
- `/etc/modsecurity/modsecurity-phase4.conf`
- `/etc/modsecurity/crs/`
- `/var/log/modsecurity/apache-phase4.jsonl`
- `/var/log/modsecurity/apache-audit.log`
- `/var/log/apache2/access.log`
- `/var/log/apache2/error.log`

Adjust paths for distributions that use `/etc/httpd` and `/var/log/httpd`.

## Request-Only Mode

Request-only mode enables ModSecurity for request phases and keeps
`SecResponseBodyAccess Off`. It is the conservative default when late response
disruption is not acceptable.

```bash
apachectl configtest
apachectl graceful
```

## Phase 4 / RESPONSE_BODY Mode

The Phase 4 example enables `SecResponseBodyAccess On`, MIME restrictions,
`SecResponseBodyLimit`, `SecResponseBodyLimitAction ProcessPartial`, and the
Apache connector `modsecurity_phase4_body_limit`. If Apache can inspect the
buffered response before commit, a disruptive Phase 4 rule can return a
blocking status. If a response has already committed, strict-abort behavior is
runtime evidence, not a clean full-body promotion.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented as runtime evidence only.

## Variable And Placeholder Reference

| Name | Type | Required | Example value | Used in | Meaning | Change requires restart/reload | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `security3_module` | Apache module name | Yes | `mod_security3.so` | `apache-modsecurity-*.conf` | Loads the Apache connector. | restart or graceful reload | Path is distribution-specific. |
| `modsecurity` | Apache directive | Yes | `on` | `apache-modsecurity-*.conf` | Enables ModSecurity in the configured scope. | graceful reload | Use inside global config or vhost scope. |
| `modsecurity_rules_file` | Apache directive | Yes | `/etc/modsecurity/modsecurity-request-only.conf` | `apache-modsecurity-*.conf` | Points Apache to the libmodsecurity rules file. | graceful reload | Use the Phase 4 rules file only for bounded response evidence. |
| `modsecurity_use_error_log` | Apache directive | No | `on` | `apache-modsecurity-*.conf` | Sends connector diagnostics to Apache error log. | graceful reload | Useful during rollout. |
| `modsecurity_phase4_mode` | Apache directive | Phase 4 only | `safe` | `apache-modsecurity-phase4-buffered.conf` | Selects connector Phase 4 behavior. | graceful reload | Safe mode prefers clean blocking before response commit. |
| `modsecurity_phase4_content_types_file` | Apache directive | Phase 4 only | `/etc/modsecurity/phase4-content-types.conf` | `apache-modsecurity-phase4-buffered.conf` | Optional allow-list for response-body MIME types. | graceful reload | Keep narrow in production. |
| `modsecurity_phase4_log` | Apache directive | Phase 4 only | `/var/log/modsecurity/apache-phase4.jsonl` | `apache-modsecurity-phase4-buffered.conf` | JSONL connector decision evidence. | graceful reload | Rotate with normal log rotation. |
| `modsecurity_phase4_body_limit` | Apache directive | Phase 4 only | `1048576` | `apache-modsecurity-phase4-buffered.conf` | Bounds connector response buffering. | graceful reload | Keep aligned with `SecResponseBodyLimit`. |
| `SecRuleEngine` | ModSecurity directive | Yes | `On` | `modsecurity-*.conf` | Enables rule execution. | graceful reload | Use `DetectionOnly` for non-disruptive rollout. |
| `SecRequestBodyAccess` | ModSecurity directive | Yes | `On` | `modsecurity-*.conf` | Enables request-body processing. | graceful reload | Request body support is promoted separately from RESPONSE_BODY. |
| `SecResponseBodyAccess` | ModSecurity directive | Yes | `Off` or `On` | `modsecurity-*.conf` | Enables or disables RESPONSE_BODY processing. | graceful reload | `On` is bounded evidence only in these examples. |
| `SecResponseBodyMimeType` | ModSecurity directive | Phase 4 only | `text/plain text/html application/json` | `modsecurity-phase4.conf` | Limits inspected response MIME types. | graceful reload | Keep explicit to avoid binary responses. |
| `SecResponseBodyLimit` | ModSecurity directive | Phase 4 only | `1048576` | `modsecurity-phase4.conf` | Bounds libmodsecurity response-body buffering. | graceful reload | Keep aligned with connector limit. |
| `SecResponseBodyLimitAction` | ModSecurity directive | Phase 4 only | `ProcessPartial` | `modsecurity-phase4.conf` | Defines behavior when the body exceeds the limit. | graceful reload | Avoid unbounded buffering. |
| `IncludeOptional` | ModSecurity directive | No | `/etc/modsecurity/crs/rules/*.conf` | `modsecurity-*.conf` | Includes CRS files if present. | graceful reload | Missing CRS files do not block startup. |
| `SecAuditEngine` | ModSecurity directive | No | `RelevantOnly` | `modsecurity-*.conf` | Enables audit logging for relevant transactions. | graceful reload | Use with log rotation. |
| `SecAuditLog` | ModSecurity directive | No | `/var/log/modsecurity/apache-audit.log` | `modsecurity-*.conf` | Audit log destination. | graceful reload | Ensure directory permissions allow Apache writes. |
| `RESPONSE_BODY` | ModSecurity collection | Phase 4 only | `@contains response-attack` | `modsecurity-phase4.conf` | Example outbound rule target. | graceful reload | Replace the example rule with production rules. |

## Logging And Evidence

Connector decisions are written to `apache-phase4.jsonl` when Phase 4 connector
logging is enabled. Audit records are written by libmodsecurity through
`SecAuditLog`. Apache access and error logs remain under the Apache log
directory.

## Security Notes

Start with request-only mode, enable audit logging, validate CRS includes, and
disable compression until the deployment proves whether the connector sees
compressed or uncompressed response bytes.


## External Usage

This directory contains example configs for external usage. They are starting points only and are not universal production defaults. The matching compile guide explains how to build or prepare the required artifact: `mod_security3.so`. Copy or adapt only the files that match your deployment; paths such as `/etc/...`, `/usr/lib/...`, `127.0.0.1`, ports, backend URLs, and log paths are placeholders unless they match your system.

Service context: Apache/httpd. After adapting the files, apachectl configtest and reload the Apache service. Inspect Apache error/access logs and ModSecurity audit logs.

## Non-Claims

- These examples are not a blanket production-readiness certification.
- They do not prove every package/version/layout.
- Phase 4 / RESPONSE_BODY examples are bounded runtime evidence only, not promoted full support.

## Related Docs

- [COMPILE_APACHE.md](../../COMPILE_APACHE.md)
- `connectors/apache/docs/build.md`
- `connectors/apache/docs/validation.md`
- `reports/testing/apache-poc.md`
