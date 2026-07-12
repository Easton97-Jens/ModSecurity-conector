# HAProxy native HTX examples

**Language:** English | [Deutsch](README.de.md)

## Integration and boundary

Integration mode: native HTX filter. The native [minimal](minimal/haproxy-htx.cfg)
and [Safe](safe/haproxy-htx.cfg) references are distinct from the preserved
[SPOE/SPOP compatibility material](compatibility-spoe/README.md).

The Safe file selects phase4-mode safe for the selected HTTP/1.1 P1--P4 core.
It is a configuration reference for the patched host filter, not a claim that
stock HAProxy loads it. P1, P2, P3, and P4 mean request headers, request body,
response headers, and response body. At the late P4 boundary Safe preserves a
response instead of fabricating a status change. This directory does not claim
a complete response buffer, per-chunk rule execution, or a client-observed
Strict abort. No Strict configuration is supplied.

## Files

| Path | Type | Purpose |
| --- | --- | --- |
| [minimal/haproxy-htx.cfg](minimal/haproxy-htx.cfg) | Host configuration | Native HTX parser-supported minimal P4 mode. |
| [safe/haproxy-htx.cfg](safe/haproxy-htx.cfg) | Host configuration | Native HTTP/1.1 P1--P4 Safe reference. |
| [rules/README.md](rules/README.md) | Documentation | Canonical No-CRS rules-file source and IDs. |
| [expected/p1-p4-safe.md](expected/p1-p4-safe.md) | Documentation | Configuration intent, not a run result. |
| [compatibility-spoe/](compatibility-spoe/README.md) | Compatibility | Former SPOE/SPOP path, deliberately separate. |

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
[rules/README.md](rules/README.md). The historical SPOE options and their
separate limits remain documented beside their compatibility files.

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

## Related material

- [HAProxy connector source and native HTX boundary](../../connectors/haproxy/README.md)
- [Repository examples overview](../README.md)
