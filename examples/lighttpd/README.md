# lighttpd native-module examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

Integration mode: native lighttpd module named mod_msconnector. The
[minimal reference](minimal/lighttpd.conf) is for the stock host/module shape
and keeps both body modes none. The [Safe reference](safe/lighttpd-http1-identity.conf)
and matching [runtime file](safe/msconnector-runtime.conf) require the matching
patched lighttpd 1.4.84 host and module. They limit scope to proxied HTTP/1.1
identity entity data.

The Safe reference configures the P1--P4 shape with phase4_mode safe. P1 is
request headers, P2 request body, P3 response headers, and P4 response body.
It is not a claim of client-observed P4 behavior, full response buffering,
HTTP/2, HTTP/3, compression, file/zero-copy handling, or Strict abort. The
[Strict profile boundary](#strict-profile-boundary) documents the optional boundary without
claiming an implemented host abort.

The retained [sidecar proxy](#sidecar-compatibility) is not native module
configuration and has no native lifecycle claim.

## Files

| Path | Type | Purpose |
| --- | --- | --- |
| [minimal/lighttpd.conf](minimal/lighttpd.conf) | Host configuration | Stock native module with bodies disabled. |
| [minimal/msconnector-runtime.conf](minimal/msconnector-runtime.conf) | Runtime configuration | Rules and bounded header metadata for minimal mode. |
| [safe/lighttpd-http1-identity.conf](safe/lighttpd-http1-identity.conf) | Host configuration | Patched native HTTP/1.1 identity-entity reference. |
| [safe/msconnector-runtime.conf](safe/msconnector-runtime.conf) | Runtime configuration | Streaming body modes and Safe P4 policy. |
| [detection-only/msconnector-runtime.conf](detection-only/msconnector-runtime.conf) | Runtime configuration | Stock body modes with DetectionOnly rules; see [DetectionOnly profile](#detectiononly-profile). |
| [disabled/lighttpd.conf](disabled/lighttpd.conf) | Host configuration | Native plugin disabled; see [Disabled profile](#disabled-profile). |
| [rules/detection-only.conf](rules/detection-only.conf) | Rules | DetectionOnly engine settings. |
| [rules/engine-off.conf](rules/engine-off.conf) | Rules | Engine-Off settings, distinct from disabling the connector. |
| [No-CRS rules](#no-crs-rules) | Documentation | No-CRS source and phase IDs. |
| [P1--P4 Safe intent](#p1-p4-safe-intent) | Documentation | Configuration intent, not run evidence. |
| [Sidecar compatibility](#sidecar-compatibility) | Compatibility | Illustrative non-native proxy setup. |

All listed paths are repository-relative from examples/lighttpd. Paths inside
the configurations are host-installation or host-runtime examples.

## Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example, effect, and security |
| --- | --- | --- | --- |
| server.modules | Ordered installed lighttpd module names | Required; host configuration; server scope | mod_msconnector for minimal and mod_proxy plus mod_msconnector for Safe. Use the matching module ABI. |
| server.document-root, errorlog, pid-file, upload-dirs | Absolute host paths | Required in these references; host configuration; server scope | /srv/lighttpd/htdocs, /srv/lighttpd/log/error.log, /srv/lighttpd/run/lighttpd.pid, /srv/lighttpd/runtime/uploads. Create them with suitable service permissions. |
| server.bind and server.port | Listener host and decimal port | Required; host configuration; server scope | 127.0.0.1 and 8080. A public bind changes exposure. |
| msconnector.config-file | Absolute runtime key=value file path | Required; host configuration; module scope | /etc/lighttpd/msconnector-runtime.conf. The file must be readable by the host process. |
| rules_file | Installed reviewed rules file | Required; runtime configuration; engine scope | /etc/modsecurity/no-crs-baseline.conf. Rules can block traffic. |
| transaction_id_header | HTTP correlation-header name | Required; runtime configuration; transaction scope | x-modsec-transaction-id. Metadata only; do not use it for secrets. |
| request_body_mode and response_body_mode | none, buffered, or streaming according to host capability | Required; runtime configuration; engine scope | none for stock minimal; streaming for matching patched Safe. Do not enable streaming on a stock host. |
| request_body_limit, response_body_limit, body_limit_action | Positive byte limits and reject or process_partial policy | Required where bodies are enabled; runtime configuration; engine scope | 1048576 and reject. Bounds do not imply full connector buffering. |
| phase4_mode | P4 policy: minimal, safe, or strict | Required in these runtime files; runtime configuration; engine scope | safe for patched Safe. It does not prove a status rewrite or abort. |
| server.stream-response-body and proxy.server | Patched delivery setting and local upstream route | Required only for Safe host file; host configuration; server scope | 1 and 127.0.0.1:8081. Identity HTTP/1.1 only; do not infer gzip/br or HTTP/2 behavior. |
| event_path | Writable JSONL metadata destination | Required in these references; runtime configuration; engine scope | /var/log/lighttpd/msconnector-events.jsonl. Protect and rotate it; do not write bodies or secrets. |

## Configuration reference

The generated [configuration reference](configuration-reference.md) documents
the two registered `msconnector.*` keys, all current Common Runtime keys, and
the separately labelled sidecar compatibility configuration.

| Setting | Layer | Task |
| --- | --- | --- |
| `msconnector.enabled` | Host / Connector | Enables or disables native plugin startup. |
| `SecRuleEngine` | ModSecurity Engine | Selects enforcement, DetectionOnly, or Off in the runtime rules file. |
| `request_body_mode` | Common Runtime | Selects stock-none or patched streaming P2 input. |
| `response_body_mode` | Common Runtime | Selects stock-none or patched streaming P4 input. |
| `phase4_mode` | Common Runtime | Selects late-P4 policy; source does not implement a strict host abort. |

`msconnector.enabled = "disable"` prevents Common Runtime startup. With the
plugin enabled, `SecRuleEngine Off` keeps host callbacks but disables engine
rule evaluation. The sidecar proxy has no native lifecycle claim.

## Profiles

### DetectionOnly profile

`detection-only/msconnector-runtime.conf` retains stock body modes `none` and
selects DetectionOnly rules. DetectionOnly loads and evaluates engine rules and
records matches, but it does not apply disruptive engine actions.

After adapting the host paths, use the connector validation command below.
This profile is configuration guidance, not runtime evidence.

### Disabled profile

`disabled/lighttpd.conf` sets `msconnector.enabled = "disable"` and no runtime
file is required. This is distinct from `SecRuleEngine Off`, which leaves an
active host connector but disables rule evaluation inside the engine.

After adapting the host paths, use the connector validation command below. Do
not infer P1--P4 behavior from a disabled profile.

## P1--P4 Safe intent

The Safe reference is limited to the matching patched lighttpd 1.4.84 native
host and identity HTTP/1.1 entity data through mod_proxy. It selects streaming
body modes and phase4_mode safe. It neither enables compressed entities nor
claims HTTP/2, HTTP/3, file, or zero-copy response inspection.

A late P4 decision is a Safe log-only boundary, not a claimed visible 403 or
Strict abort. The stock minimal reference keeps bodies disabled. No Strict
example is supplied.

## No-CRS rules

The native module reads the reviewed installed rules file named by
msconnector.config-file. The repository source for the No-CRS profile is
[modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).

| Rule ID | Phase | Purpose |
| ---: | ---: | --- |
| 1100001 | P1 | Request-header deny |
| 1100101 | P2 | Request-body deny |
| 1100201 | P3 | Response-header deny |
| 1100301 | P4 | Response-body decision used by the Safe boundary |

## Sidecar compatibility

The retained configuration is an illustrative lighttpd proxy setup. It does
not load mod_msconnector.so and therefore is not the native lighttpd core
reference. Use [minimal/](minimal/) for the stock native module shape or
[safe/](safe/) for the patched HTTP/1.1 identity-entity reference.

### Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example and boundary |
| --- | --- | --- |
| server.modules | Installed lighttpd proxy and logging modules | Required; host config; server scope | mod_accesslog and mod_proxy. This is not mod_msconnector. |
| server.document-root and log paths | Host filesystem paths | Required; host config; server scope | /var/empty and relative log names. Replace with writable operator paths. |
| server.port | Decimal TCP listener port | Required; host config; server scope | 8080. Bind a private listener for a local exercise. |
| proxy.server host and port | Upstream endpoint | Required; host config; proxy scope | 127.0.0.1:8081. Replace with the intended backend. |
| $HTTP host expression | lighttpd request Host-header selector | Required in this example; host config; conditional scope | Matches every host. It is a host-language variable, not a shell variable or secret. |

A separate operator-supplied sidecar remains outside lifecycle claims made by
the native examples.

## Validation

Install the matching lighttpd module and configuration files, adapt all paths,
then check the installed host configuration. The path below is an installation
example:

~~~sh
lighttpd -tt -f /etc/lighttpd/lighttpd.conf
~~~

For the Safe reference, also verify the exact patched host/module pair and a
private local upstream before starting it. A configuration check proves syntax
and readable inputs only; it does not prove P1--P4 outcomes, Safe host actions,
Strict behavior, production readiness, or CRS coverage.

## Strict profile boundary <a id="strict-profile-boundary"></a>

Common Runtime accepts `phase4_mode=strict`, but the native lighttpd module
does not implement a strict transport abort. Strict is optional and no runnable
strict host profile is supplied.

Validate the matching host/module pair and Common Runtime configuration before
testing a strict value; do not describe it as an implemented client abort.

## Related material

- [lighttpd connector source and patched-host boundary](../../connectors/lighttpd/README.md)
- [Repository examples overview](../README.md)
