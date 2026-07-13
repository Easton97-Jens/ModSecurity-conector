# HAProxy native HTX examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

Integration mode: native HTX filter. The native [minimal](minimal/haproxy-htx.cfg)
and [Safe](safe/haproxy-htx.cfg) references are distinct from the preserved
[SPOE/SPOP compatibility material](#spoespop-compatibility).

The Safe file selects phase4-mode safe for the selected HTTP/1.1 P1--P4 core.
It is a configuration reference for the patched host filter, not a claim that
stock HAProxy loads it. P1, P2, P3, and P4 mean request headers, request body,
response headers, and response body. At the late P4 boundary Safe preserves a
response instead of fabricating a status change. This directory does not claim
a complete response buffer, per-chunk rule execution, or a client-observed
Strict abort. The [Strict profile boundary](#strict-profile-boundary) records the optional
parser boundary without claiming a native host abort.

## Files

| Path | Type | Purpose |
| --- | --- | --- |
| [minimal/haproxy-htx.cfg](minimal/haproxy-htx.cfg) | Host configuration | Native HTX parser-supported minimal P4 mode. |
| [safe/haproxy-htx.cfg](safe/haproxy-htx.cfg) | Host configuration | Native HTTP/1.1 P1--P4 Safe reference. |
| [detection-only/haproxy-htx.cfg](detection-only/haproxy-htx.cfg) | Host configuration | Native connector with DetectionOnly rules; see [DetectionOnly profile](#detectiononly-profile). |
| [disabled/haproxy-htx.cfg](disabled/haproxy-htx.cfg) | Host configuration | Native filter omitted; see [Disabled profile](#disabled-profile). |
| [rules/detection-only.conf](rules/detection-only.conf) | Rules | DetectionOnly engine settings. |
| [rules/engine-off.conf](rules/engine-off.conf) | Rules | Engine-Off settings, distinct from disabling the connector. |
| [No-CRS rules](#no-crs-rules) | Documentation | Canonical No-CRS rules-file source and IDs. |
| [P1--P4 Safe intent](#p1-p4-safe-intent) | Documentation | Configuration intent, not a run result. |
| [SPOE/SPOP compatibility](#spoespop-compatibility) | Compatibility | Former SPOE/SPOP path, deliberately separate. |

The native references use host installation values: listener 127.0.0.1:8080,
upstream 127.0.0.1:8081, and rules file
/etc/modsecurity/no-crs-baseline.conf. None is a repository-relative path.

## Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example, effect, and security |
| --- | --- | --- | --- |
| filter modsecurity-htx | Patched HAProxy filter directive | Required; no stock-host default; configured in frontend scope | The patched host must provide this parser. A stock binary rejecting it is a configuration incompatibility, not a reason to fall back silently. |
| rules-file | Readable installed rules file | Required; no repository default; filter argument; frontend scope | /etc/modsecurity/no-crs-baseline.conf. A reviewed ruleset can block traffic. |
| phase4-mode | P4 policy: minimal, safe, or strict | Optional filter argument; set in frontend scope; the Safe file sets safe | safe. It records a late P4 result without treating it as a status rewrite. |
| bind address | Listener TCP address | Required; host config; frontend scope | 127.0.0.1:8080. Choose a private address for local testing; a public bind changes exposure. |
| upstream server | Backend host and TCP port | Required; host config; backend scope | 127.0.0.1:8081. Replace with the intended application endpoint. |
| timeout connect/client/server | Positive HAProxy duration | Required in these references; host config; defaults scope | 2s and 5s. Tune for the application; timeouts are not WAF decisions. |

The No-CRS rule IDs and their phase meanings are in
[No-CRS rules](#no-crs-rules). The historical SPOE options and their separate
limits remain in [SPOE/SPOP compatibility](#spoespop-compatibility).

## Configuration reference

The generated [configuration reference](configuration-reference.md) separates
the native HTX parser from the SPOE/SPOP compatibility files.

| Setting | Layer | Task |
| --- | --- | --- |
| `filter modsecurity-htx` | Host / Connector | Attaches the selected native HTX lifecycle filter. |
| `SecRuleEngine` | ModSecurity Engine | Evaluates rules loaded through `rules-file`. |
| `SecRequestBodyAccess` | ModSecurity Engine | Allows P2 input when native HTX supplies it. |
| `SecResponseBodyAccess` | ModSecurity Engine | Allows P4 input when native HTX supplies it. |
| `phase4-mode` | Connector / Common policy | Requests minimal, safe, or strict late-P4 policy. |

Removing the native filter disables the connector path. `SecRuleEngine Off`
does not remove the filter, but it disables engine rule processing. `filter
spoe` remains a separate compatibility route, not a native HTX setting.

## Profiles

### DetectionOnly profile

`detection-only/haproxy-htx.cfg` keeps the native HTX filter and selects the
DetectionOnly rules file. DetectionOnly loads and evaluates engine rules and
records matches, but it does not apply disruptive engine actions.

After adapting the host paths, use the connector validation command below.
This profile is configuration guidance, not runtime evidence.

### Disabled profile

`disabled/haproxy-htx.cfg` omits `filter modsecurity-htx`; SPOE is not
substituted. This is distinct from `SecRuleEngine Off`, which leaves an active
host connector but disables rule evaluation inside the engine.

After adapting the host paths, use the connector validation command below. Do
not infer P1--P4 behavior from a disabled profile.

## P1--P4 Safe intent

The native HTX Safe reference selects phase4-mode safe. It is meant for the
patched native filter path, not the SPOE/SPOP compatibility service. A P4
decision after a response has started is recorded as Safe log-only behavior;
the configuration does not promise a status replacement or a Strict abort.

The minimal reference exposes the parser-supported minimal mode. There is no
Strict example because a checked-in filter option is not proof of a
client-observed post-commit abort.

## No-CRS rules

The native HTX references consume an installed copy of the repository-owned
[No-CRS baseline rules](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf).
The rules-file value in the HAProxy filter is a host installation path, not a
path relative to the HAProxy process.

| Rule ID | Phase | Purpose |
| ---: | ---: | --- |
| 1100001 | P1 | Request-header deny |
| 1100101 | P2 | Request-body deny |
| 1100201 | P3 | Response-header deny |
| 1100301 | P4 | Response-body decision used by the Safe boundary |

## SPOE/SPOP compatibility

The preserved files below are former HAProxy SPOE/SPOP examples. They are
separate from the native HTX P1--P4 Safe reference in [safe/](safe/).

| File | Scope |
| --- | --- |
| [haproxy-request-only.cfg](compatibility-spoe/haproxy-request-only.cfg) | Request SPOE group for P1/P2-style request decisions. |
| [haproxy-response-headers.cfg](compatibility-spoe/haproxy-response-headers.cfg) | Adds response-header SPOE; it is not response-body processing. |
| [spoe-modsecurity.conf](compatibility-spoe/spoe-modsecurity.conf) | SPOE agent, group, message, and returned-variable mapping. |
| [modsecurity-agent.conf](compatibility-spoe/modsecurity-agent.conf) | SPOA process settings. |
| [legacy-phase4-strict-abort.cfg](compatibility-spoe/legacy-phase4-strict-abort.cfg) | Disabled historical sample; never use as P4 evidence. |

### Values to adapt

| Name | Purpose and format | Required/default, setter, scope | Example and boundary |
| --- | --- | --- |
| filter spoe engine modsecurity config | HAProxy SPOE filter and readable agent file | Required; host configuration; frontend scope | /etc/haproxy/spoe-modsecurity.conf. This selects compatibility SPOE, not native HTX. |
| send-spoe-group | Request or response-header SPOE message group | Required for its matching file; host configuration; request/response scope | request-check or response-check. response-check does not send a response body. |
| be_spoa_modsecurity | SPOP backend name and endpoint | Required; host configuration; backend scope | 127.0.0.1:12345. It must match the agent listen value. |
| groups and register-var-names | SPOE group names and returned transaction variables | Required; spoe-modsecurity.conf; agent scope | request-check response-check and blocked/action/status fields. Names must match HAProxy enforcement expressions. |
| max-frame-size | Positive SPOE frame byte limit | Required; spoe-modsecurity.conf; agent scope | 65532. It bounds a frame; it does not create P4 body support. |
| rules-file | Readable agent rules file | Required; modsecurity-agent.conf; SPOA scope | /etc/modsecurity/haproxy-rules.conf. A reviewed ruleset can block traffic. |
| decision-log, audit-log, log-file | Writable process log paths | decision-log required; others optional; SPOA scope | /var/log/haproxy-modsecurity. Protect metadata and do not log secrets. |
| response-body-limit and response-body-timeout | Compatibility response-body controls | Explicitly disabled; SPOA scope | 0 and 0. They must not be presented as P4 support. |

The SPOP address 127.0.0.1:12345, HAProxy listener 127.0.0.1:8080, upstream
127.0.0.1:8081, and /etc or /var/log paths are host examples, not
repository-relative paths.

This path must not be used to claim native HTX behavior, P4 response-body
handling, Safe late behavior, Strict abort behavior, first-byte-before-EOS
behavior, or no-full-response-buffer behavior.

## Validation

Place the selected reference in an installed patched HAProxy configuration,
adapt rules-file and addresses, then run the installed host checker:

~~~sh
haproxy -c -f /etc/haproxy/haproxy.cfg
~~~

The path is a distribution example; select the real host configuration path.
A successful check proves that this HAProxy binary parsed the file. It does not
prove P1--P4 outcomes, P4 client behavior, Strict aborts, production readiness,
or that the SPOE/SPOP compatibility path has native HTX properties.

## Strict profile boundary <a id="strict-profile-boundary"></a>

The native HTX parser accepts `phase4-mode strict`, but the current host path
records the requested abort as `not_attempted`. Strict is optional and no
runnable profile is claimed here.

Set the optional argument on the native filter, validate with `haproxy -c -f
<config>`, and do not represent it as a client-visible abort without new host
evidence.

## Related material

- [HAProxy connector source and native HTX boundary](../../connectors/haproxy/README.md)
- [Repository examples overview](../README.md)
