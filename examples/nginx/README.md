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
| [detection-only/nginx.conf](detection-only/nginx.conf) | Host configuration | Native connector with DetectionOnly engine rules; see [DetectionOnly profile](#detectiononly-profile). |
| [disabled/nginx.conf](disabled/nginx.conf) | Host configuration | Connector disabled at the NGINX layer; see [Disabled profile](#disabled-profile). |
| [rules/request-only.conf](rules/request-only.conf) | Rules | Request-only settings. |
| [rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) | Rules | Bounded P4 settings and local illustration. |
| [rules/detection-only.conf](rules/detection-only.conf) | Rules | DetectionOnly engine settings. |
| [rules/engine-off.conf](rules/engine-off.conf) | Rules | Engine-Off settings, distinct from disabling the connector. |
| [No-CRS rules](#no-crs-rules) | Documentation | No-CRS source and rule IDs. |
| [P1--P4 Safe intent](#p1-p4-safe-intent) | Documentation | Intent only, not test evidence. |

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
see [No-CRS rules](#no-crs-rules).

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

## Profiles

### DetectionOnly profile

`detection-only/nginx.conf` keeps `modsecurity on` and selects the
DetectionOnly rules file. DetectionOnly loads and evaluates engine rules and
records matches, but it does not apply disruptive engine actions.

After adapting the host paths, use the connector validation command below.
This profile is configuration guidance, not runtime evidence.

### Disabled profile

`disabled/nginx.conf` sets `modsecurity off`, so NGINX does not create a
connector transaction. This is distinct from `SecRuleEngine Off`, which leaves
an active host connector but disables rule evaluation inside the engine.

After adapting the host paths, use the connector validation command below. Do
not infer P1--P4 behavior from a disabled profile.

## P1--P4 Safe intent

The Safe config enables the native module, scopes response inspection to the
listed content types, and uses Safe for a late P4 decision. A late match is not
a promise that the client sees a replacement 403. The reference also keeps
gzip off so the inspected byte representation is not assumed.

The Strict config is an available configuration shape only. It does not prove
a client-observed abort, status rewrite, or complete response buffering.

## No-CRS rules

The reusable No-CRS source is
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
Install a reviewed copy at the rules-file path selected in the NGINX
configuration.

| Rule ID | Phase | Purpose |
| ---: | ---: | --- |
| 1100001 | P1 | Request-header deny |
| 1100101 | P2 | Request-body deny |
| 1100201 | P3 | Response-header deny |
| 1100301 | P4 | Response-body decision used by the Safe boundary |

The illustrative p1-p4-safe.conf uses 9001801 only as a local example. It is
not an OWASP CRS or No-CRS baseline ID.

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

## Strict profile boundary <a id="strict-profile-boundary"></a>

[strict/nginx.conf](strict/nginx.conf) is a parser-supported Strict
configuration shape. It does not claim a visible late status rewrite;
post-commit Strict behavior must be validated against the installed NGINX host.

Adapt paths and endpoints, run `nginx -t`, and treat an abort as a
host-specific outcome rather than a guaranteed later 403.

## Related material

- [NGINX connector source and validation boundary](../../connectors/nginx/README.md)
- [Repository examples overview](../README.md)
