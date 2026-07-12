# Apache native-module examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

Integration mode: native httpd module. The [minimal reference](minimal/httpd.conf)
is request oriented; the [Safe reference](safe/httpd.conf) selects the native
HTTP/1.1 P1--P4 configuration shape. P1 is request headers, P2 request body,
P3 response headers, and P4 response body.

Safe is a post-commit policy, not a visible-status guarantee. The filter passes
current data onward and completes response-body processing at EOS. This does
not promise per-chunk rule evaluation or a connector-owned full response
buffer. A late P4 decision must be recorded as log-only unless matching host
evidence establishes something more. No Strict file is supplied: the parser
accepts strict, but this directory does not claim a client-visible abort.

## Files

| Path | Type | Purpose |
| --- | --- | --- |
| [minimal/httpd.conf](minimal/httpd.conf) | Host configuration | Request-oriented starting point. |
| [safe/httpd.conf](safe/httpd.conf) | Host configuration | Bounded native P1--P4 Safe reference. |
| [rules/request-only.conf](rules/request-only.conf) | Rules | Request-only rule-engine settings. |
| [rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) | Rules | Bounded response-body settings and local P4 illustration. |
| [rules/README.md](rules/README.md) | Documentation | No-CRS source and rule-ID meanings. |
| [expected/p1-p4-safe.md](expected/p1-p4-safe.md) | Documentation | Configuration intent, not a test result. |

All paths in this table are repository-relative from examples/apache. Paths in
the configuration, including /usr/lib/apache2/modules/mod_security3.so,
/etc/modsecurity, and /var/log, are host-installation examples.

## Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example, effect, and security |
| --- | --- | --- | --- |
| security3_module | Module loaded by LoadModule | Required; no repository default; Apache package or local build; server scope | mod_security3.so at an installed module path. A wrong ABI or path prevents startup. |
| modsecurity_rules_file | Readable libmodsecurity rules file | Required; no repository default; host config; module scope | /etc/modsecurity/modsecurity-phase4.conf. A reviewed ruleset can block traffic. |
| modsecurity_phase4_mode | Late P4 policy: minimal, safe, or strict | Safe file only; host config; module scope | safe. It avoids representing a late decision as a fabricated status. |
| modsecurity_phase4_content_types_file | Explicit response MIME-type file | Optional; host config; module scope | /etc/modsecurity/phase4-content-types.conf. Keep it narrow; unreadable files fail validation. |
| modsecurity_phase4_log | Decision JSONL destination | Optional; host config; module scope | /var/log/modsecurity/apache-phase4.jsonl. Protect and rotate request metadata. |
| modsecurity_phase4_body_limit and SecResponseBodyLimit | Positive P4 byte limits | Required for bounded Safe use; host and rules files; no automatic alignment | 1048576 bytes. Mismatches change P4 input; never make this unbounded. |
| SecRequestBodyAccess and SecResponseBodyAccess | Request/response body switches | Required in matching rules; rule-engine scope | On in Safe rules; response access is Off in request-only. |
| SecResponseBodyMimeType and SecResponseBodyLimitAction | P4 scope and over-limit policy | Required in Safe rules; rule-engine scope | Explicit text/JSON types and ProcessPartial. Do not infer binary behavior. |
| SecAuditLog | Audit-log destination | Optional; rules file; rule-engine scope | /var/log/modsecurity/apache-audit.log. Apply access control and retention policy. |

Rule ID 9002801 is local to p1-p4-safe.conf. It is not an OWASP CRS or No-CRS
baseline ID; see [rules/README.md](rules/README.md).

## Validation

Install or include the selected files, adapt every host path, and check the
complete installed Apache configuration:

~~~sh
apachectl -t
~~~

After an intentional reload, inspect the Apache error log, decision log, and
audit log. A syntax check does not prove P1--P4 behavior, a client-visible P4
status, CRS coverage, or production readiness.

## Related material

- [Apache connector source and validation boundary](../../connectors/apache/README.md)
- [Repository examples overview](../README.md)
