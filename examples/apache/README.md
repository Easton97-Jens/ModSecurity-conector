# Apache native-module examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

Integration mode: native httpd module. The [minimal reference](minimal/httpd.conf)
is request oriented; the [Safe reference](safe/httpd.conf) selects the native
HTTP/1.1 P1--P4 configuration shape. P1 is request headers, P2 request body,
P3 response headers, and P4 response body.

Safe is the selected configuration for Apache's EOS-only all-response Phase-4
gate. The filter appends data buckets incrementally, but retains every
normalized response brigade through first EOS before it releases any original
byte. It then completes response-body processing and resolves intervention
once. This does not promise per-chunk rule evaluation or client-visible
progressive response streaming. A normal deny is resolved before original
output release; Safe <code>log_only</code> is only a defensive fallback for a
separately proven already-committed response. The [Strict profile boundary](#strict-profile-boundary)
documents the parser-supported optional fallback value but does not claim a
client-visible abort.

## Files

| Path | Type | Purpose |
| --- | --- | --- |
| [minimal/httpd.conf](minimal/httpd.conf) | Host configuration | Request-oriented starting point. |
| [safe/httpd.conf](safe/httpd.conf) | Host configuration | Bounded native P1--P4 Safe reference. |
| [detection-only/httpd.conf](detection-only/httpd.conf) | Host configuration | Native connector with DetectionOnly engine rules; see [DetectionOnly profile](#detectiononly-profile). |
| [disabled/httpd.conf](disabled/httpd.conf) | Host configuration | Connector disabled at the Apache layer; see [Disabled profile](#disabled-profile). |
| [rules/request-only.conf](rules/request-only.conf) | Rules | Request-only rule-engine settings. |
| [rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) | Rules | Bounded response-body settings and local P4 illustration. |
| [rules/detection-only.conf](rules/detection-only.conf) | Rules | DetectionOnly engine settings. |
| [rules/engine-off.conf](rules/engine-off.conf) | Rules | Engine-Off settings, distinct from disabling the connector. |
| [No-CRS rules](#no-crs-rules) | Documentation | No-CRS source and rule-ID meanings. |
| [P1--P4 Safe intent](#p1-p4-safe-intent) | Documentation | Configuration intent, not a test result. |

All paths in this table are repository-relative from examples/apache. Paths in
the configuration, including /usr/lib/apache2/modules/mod_security3.so,
/etc/modsecurity, and /var/log, are host-installation examples.

## Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example, effect, and security |
| --- | --- | --- | --- |
| security3_module | Module loaded by LoadModule | Required; no repository default; Apache package or local build; server scope | mod_security3.so at an installed module path. A wrong ABI or path prevents startup. |
| modsecurity_rules_file | Readable libmodsecurity rules file | Required; no repository default; host config; module scope | /etc/modsecurity/modsecurity-phase4.conf. A reviewed ruleset can block traffic. |
| modsecurity_phase4_mode | Defensive late-P4 fallback: minimal, safe, or strict | Safe file only; host config; module scope | safe. A normal gated deny is resolved before release; this setting only selects an unexpected, already-committed fallback. |
| modsecurity_phase4_content_types_file | Deprecated legacy response-MIME file | Optional compatibility parser; host config; module scope | Do not configure it for new Apache profiles: it cannot narrow the all-response gate. Use `SecResponseBodyMimeType` to select engine inspection. |
| modsecurity_phase4_log | Decision JSONL destination | Optional; host config; module scope | /var/log/modsecurity/apache-phase4.jsonl. Protect and rotate request metadata. |
| modsecurity_phase4_body_limit and SecResponseBodyLimit | Positive P4 byte limits | Required for bounded Safe use; host and rules files; no automatic alignment | The connector default is 1048576 bytes. It is a hard fail-closed all-response-gate limit; a libModSecurity `ProcessPartial` policy does not release an uninspected connector tail. |
| SecRequestBodyAccess and SecResponseBodyAccess | Request/response body switches | Required in matching rules; rule-engine scope | On in Safe rules; response access is Off in request-only. |
| SecResponseBodyMimeType and SecResponseBodyLimitAction | Engine P4 scope and over-limit policy | Required in Safe rules; rule-engine scope | Explicit text/JSON types select engine inspection; they do not narrow Apache's all-response gate. Do not infer binary behavior. |
| SecAuditLog | Audit-log destination | Optional; rules file; rule-engine scope | /var/log/modsecurity/apache-audit.log. Apply access control and retention policy. |

Rule ID 9002801 is local to p1-p4-safe.conf. It is not an OWASP CRS or No-CRS
baseline ID; see [No-CRS rules](#no-crs-rules).

## Configuration reference

The generated [configuration reference](configuration-reference.md) documents
all 11 registered Apache directives, the host fields used here, and their
parser/default/merge anchors.

| Setting | Layer | Task |
| --- | --- | --- |
| `modsecurity on|off` | Host / Connector | Enables or disables Apache transaction creation. |
| `SecRuleEngine` | ModSecurity Engine | Evaluates loaded rules and selects enforcement, DetectionOnly, or Off. |
| `SecRequestBodyAccess` | ModSecurity Engine | Makes P2 request-body input available to the engine. |
| `SecResponseBodyAccess` | ModSecurity Engine | Makes eligible P4 response-body input available to the engine. |
| `modsecurity_phase4_mode` | Connector / Common policy | Selects only a defensive already-committed fallback; an ordinary gated P4 deny resolves before original output release. |

`modsecurity on` with `SecRuleEngine Off` creates the connector path but disables
engine rule evaluation. `modsecurity off` prevents the engine from receiving a
connector transaction even when a rules file says `SecRuleEngine On`.

## Profiles

### DetectionOnly profile

`detection-only/httpd.conf` keeps `modsecurity on` and selects the
DetectionOnly rules file. DetectionOnly loads and evaluates engine rules and
records matches, but it does not apply disruptive engine actions.

After adapting the host paths, use the connector validation command below.
This profile is configuration guidance, not runtime evidence.

### Disabled profile

`disabled/httpd.conf` sets `modsecurity off`, so Apache creates no connector
transaction. This is distinct from `SecRuleEngine Off`, which leaves an active
host connector but disables rule evaluation inside the engine.

After adapting the host paths, use the connector validation command below. Do
not infer P1--P4 behavior from a disabled profile.

## P1--P4 Safe intent

The Safe reference configures native httpd-module processing for P1 through P4
and a 1048576-byte all-response gate. Apache saves all normalized output
brigades through first EOS, including an empty response's EOS; a normal P4 deny
discards that saved original response and sends the terminal error before it
can be released. The C API makes libModSecurity's effective MIME decision
opaque to the connector, so `SecResponseBodyMimeType` selects engine inspection
without creating a gate bypass. The deprecated
`modsecurity_phase4_content_types_file` is intentionally absent from the Safe
configuration.

This section records configuration intent, not a run result. Input ingestion
remains incremental across multiple brigades, but the native path deliberately
does not promise client-visible progressive response streaming. Failure to
append, save, or finish the body discards the saved response and fails closed.
Only a genuinely already-committed response can use Safe log-only or Strict
abort fallback behavior. No Strict example is supplied here.

## No-CRS rules

The reusable No-CRS source is
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
It is repository-relative and should be copied or installed by the operator as
a reviewed host rules file, for example /etc/modsecurity/no-crs-baseline.conf.

| Rule ID | Phase | Purpose |
| ---: | ---: | --- |
| 1100001 | P1 | Request-header deny |
| 1100101 | P2 | Request-body deny |
| 1100201 | P3 | Response-header deny |
| 1100301 | P4 | Response-body decision used by the Safe boundary |

The checked-in p1-p4-safe.conf is an illustrative Apache rules file. Its
9002801 rule is local to that example and is not an OWASP CRS or No-CRS
baseline ID.

## Validation

Install or include the selected files, adapt every host path, and check the
complete installed Apache configuration:

~~~sh
apachectl -t
~~~

After an intentional reload, inspect the Apache error log, decision log, and
audit log. A syntax check does not prove P1--P4 behavior, a client-visible P4
status, CRS coverage, or production readiness.

## Strict profile boundary <a id="strict-profile-boundary"></a>

`modsecurity_phase4_mode strict` is parser-supported, but this repository has
no Apache host evidence for a client-visible late abort. Strict is therefore
optional and intentionally has no runnable configuration here. It applies only
when commit is independently proven; it does not convert a normal pre-release
P4 deny into a late abort.

Start from `safe/httpd.conf`, set `modsecurity_phase4_mode strict`, validate
with `apachectl -t`, and record host-specific evidence before relying on a
post-commit action.

The focused H1/H2 evidence placeholder is
`ci/runtime/lifecycle/run-apache-phase4-response-regression.sh`. Record only
run-scoped artifacts after executing it; this configuration documentation does
not claim that either protocol has passed.

## Related material

- [Apache connector source and validation boundary](../../connectors/apache/README.md)
- [Repository examples overview](../README.md)
