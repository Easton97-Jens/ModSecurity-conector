# HAProxy examples

**Language:** English | [Deutsch](README.de.md)

Choose native HTX or SPOE/SPOP with its native HTX response companion. Both
require the patched HAProxy filter parser. These references cover HTTP/1.1.

## Files

| Layout | Native HTX | SPOE/SPOP with response companion |
| --- | --- | --- |
| `off` | [haproxy-htx.cfg](off/haproxy-htx.cfg) | [bundle](spoe-spop/off/) |
| `safe` | [haproxy-htx.cfg](safe/haproxy-htx.cfg) | [bundle](spoe-spop/safe/) |
| `strict` | [haproxy-htx.cfg](strict/haproxy-htx.cfg) | [bundle](spoe-spop/strict/) |
| `all` | [haproxy-htx.cfg](all/haproxy-htx.cfg) | [bundle](spoe-spop/all/) |

`off` preserves native intervention handling. `all` exposes the complete
configuration and selects the accepted `phase4-mode strict` value.

## Values to adapt

Set `rules-file`, listener, upstream, and connect/client/server timeouts for the
installation. The references use `127.0.0.1:8080`, `127.0.0.1:8081`, and
`/etc/modsecurity/no-crs-baseline.conf`. Body access, inspection limits, and
limit actions belong in engine rules. Syntax, defaults, and route-specific
settings are in the generated [configuration reference](configuration-reference.md).

## Profiles

### DetectionOnly profile

[detection-only/haproxy-htx.cfg](detection-only/haproxy-htx.cfg) keeps the filter
active and uses [DetectionOnly rules](rules/detection-only.conf), which evaluate
and log matches while suppressing disruptive engine actions.

### Disabled profile

[disabled/haproxy-htx.cfg](disabled/haproxy-htx.cfg) omits the native filter.
With the filter active, [rules/engine-off.conf](rules/engine-off.conf) disables
engine evaluation through `SecRuleEngine Off`.

## P1--P4 semantics and topology

| Phase | Native HTX | SPOE/SPOP solution |
| --- | --- | --- |
| P1 | Request headers to engine | SPOE request message to SPOP agent |
| P2 | Request body and EOS to engine | Bounded buffered `req.body` to agent |
| P3 | Response headers to engine | HTX companion claims opaque MRC1 handle over private UDS |
| P4 | Response chunks and EOS to engine | HTX companion sends bounded chunks and exactly one EOS |

Safe records a late P4 decision as log-only after response output has started.
The SPOE request route retains its host buffering and frame limits.

## Strict profile boundary <a id="strict-profile-boundary"></a>

The parser accepts `phase4-mode strict`. The current host path records a
post-commit abort request as `not_attempted` when it cannot perform the abort
safely. Validate client-visible behavior on the selected host/profile.

## SPOE/SPOP response-companion solution

Each bundle contains `haproxy.cfg`, `spoe.cfg`, and `spoa-agent.conf`. Adapt the
private socket and log paths together with the process identity.

| Parameter | Reference value |
| --- | --- |
| `tune.bufsize` / `max-frame-size` | 65536 / 65532 |
| `response-body-timeout` / `spoe-timeout` | 2000 / 2000 ms |
| `max-transactions` / `worker-count` | 64 / 8 |
| `response-companion-uid/gid` | 1000 / 1000, matching agent identity |

`response-companion=native-htx`, private UDS, matching UID/GID, bounded frames,
EOS, and timeouts are mandatory startup requirements. Correlation or companion
failure is fail-closed with cleanup. Only opaque handles cross the UDS.

## No-CRS rules

Install a reviewed copy of the [No-CRS baseline](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)
at the configured rules path. IDs `1100001`, `1100101`, `1100201`, and `1100301`
correspond to P1, P2, P3, and P4. See the
[shared rule guide](../common/rule-examples.md).

## SPOE/SPOP compatibility material

The historical [request-only](compatibility-spoe/haproxy-request-only.cfg) and
[response-header](compatibility-spoe/haproxy-response-headers.cfg) illustrations
use [SPOE mapping](compatibility-spoe/spoe-modsecurity.conf) and
[SPOA process settings](compatibility-spoe/modsecurity-agent.conf).
Response-body controls are disabled with `response-body-timeout=0`.
The [legacy strict-abort sample](compatibility-spoe/legacy-phase4-strict-abort.cfg)
is disabled. Use the response-companion bundles above for P3/P4 body handling.

For compatibility files, align the SPOP backend with agent `listen`, group and
returned-variable names with enforcement expressions, and all rules/log paths.
The sample SPOP endpoint is `127.0.0.1:12345`. Retain frame bounds and protect
metadata logs. Detailed fields are in the configuration reference.

## Validation

After adapting the selected files, use the installed patched host checker.

~~~sh
haproxy -c -f /etc/haproxy/haproxy.cfg
~~~

Select the actual installed configuration path. Runtime enforcement requires
profile-specific traffic evidence. See the
[HAProxy connector guide](../../connectors/haproxy/README.md) and
[examples index](../README.md).
