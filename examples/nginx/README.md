# NGINX native-module examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

Integration mode: native NGINX HTTP module. [minimal/nginx.conf](minimal/nginx.conf)
is request-only. [safe/nginx.conf](safe/nginx.conf) is the bounded HTTP/1.1
P1--P4 Safe reference. [strict/nginx.conf](strict/nginx.conf) records a
parser-supported configuration shape, not a claim that a late abort or status
rewrite was observed.

The P4 body filter runs after the response-header path. Safe therefore records
late outcomes without portraying them as a clean client-visible 403. The
reference turns gzip off until the byte representation seen by the installed
module is validated. It does not promise per-chunk P4 evaluation or a full
connector response buffer.

## Files

| Path | Type | Purpose |
| --- | --- | --- |
| [minimal/nginx.conf](minimal/nginx.conf) | Host configuration | Request-only native module reference. |
| [safe/nginx.conf](safe/nginx.conf) | Host configuration | Bounded P1--P4 Safe reference. |
| [strict/nginx.conf](strict/nginx.conf) | Host configuration | Explicitly limited Strict configuration shape. |
| [rules/request-only.conf](rules/request-only.conf) | Rules | Request-only settings. |
| [rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) | Rules | Bounded P4 settings and local illustration. |
| [rules/README.md](rules/README.md) | Documentation | No-CRS source and rule IDs. |
| [expected/p1-p4-safe.md](expected/p1-p4-safe.md) | Documentation | Intent only, not test evidence. |

The listed paths are repository-relative from examples/nginx. Module, rules,
logs, listener, and upstream values inside them are host examples.

## Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example, effect, and security |
| --- | --- | --- | --- |
| load_module path | Installed NGINX dynamic module | Required; no repository default; operator; main scope | modules/ngx_http_modsecurity_module.so. Use a module built for the exact NGINX ABI. |
| modsecurity_rules_file | Readable libmodsecurity rules file | Required; no repository default; host config; http scope | /etc/modsecurity/modsecurity-phase4.conf. A reviewed ruleset can block traffic. |
| modsecurity_phase4_mode | P4 policy: minimal, safe, or strict | Required in Safe or Strict file; host config; http scope | safe in safe/nginx.conf. Strict is configuration-only here. |
| modsecurity_phase4_content_types_file | Explicit response MIME-type list | Optional; host config; http scope | /etc/modsecurity/phase4-content-types.conf. A missing file fails validation. |
| modsecurity_phase4_log | Decision JSONL destination | Optional; host config; http scope | /var/log/modsecurity/nginx-phase4.jsonl. Protect and rotate request metadata. |
| app_backend and 127.0.0.1:8081 | Upstream group and local TCP endpoint | Required in these proxy references; host config; http scope | Replace with the intended upstream. Loopback avoids accidental exposure during a local test. |
| listen 8080 and server_name example.test | Listener and virtual-host selector | Required in these files; host config; server scope | Replace for the installed host; a public bind changes exposure. |
| SecResponseBodyLimit | Positive P4 byte bound | Required in bounded P4 rules; rules file; rule-engine scope | 1048576 bytes. Do not infer unbounded behavior from this reference. |

Rule ID 9001801 is illustrative only, not an OWASP CRS or No-CRS baseline ID;
see [rules/README.md](rules/README.md).

## Configuration reference

The generated [configuration reference](configuration-reference.md) documents
all 10 registered `ngx_command_t` directives, their `http → server → location`
contexts, and the surrounding example host fields.

| Setting | Layer | Task |
| --- | --- | --- |
| `modsecurity on|off` | Host / Connector | Enables or disables NGINX connector processing in the merged context. |
| `SecRuleEngine` | ModSecurity Engine | Evaluates loaded rules and selects enforcement, DetectionOnly, or Off. |
| `SecRequestBodyAccess` | ModSecurity Engine | Makes P2 request-body input available to the engine. |
| `SecResponseBodyAccess` | ModSecurity Engine | Makes eligible P4 response-body input available to the engine. |
| `modsecurity_phase4_mode` | Connector / Common policy | Selects requested late-P4 policy; Safe does not promise a late 403. |

`modsecurity off` stops the NGINX access-handler connector path; configured
rules can still have been loaded during configuration parsing. `SecRuleEngine`
is an engine setting and does not load or enable the NGINX module by itself.

## Validation

Copy or include the selected file in the installed NGINX configuration, adapt
all host values, then check the complete installed configuration:

~~~sh
nginx -t
~~~

Inspect the NGINX error log and configured ModSecurity logs after a deliberate
reload. Validation proves syntax and readable dependencies only; it does not
prove P1--P4 outcomes, a visible late P4 status, Strict abort, production
readiness, or CRS coverage.

## Related material

- [NGINX connector source and validation boundary](../../connectors/nginx/README.md)
- [Repository examples overview](../README.md)
