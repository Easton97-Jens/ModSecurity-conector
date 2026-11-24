# NGINX native-module examples

**Language:** English | [Deutsch](README.de.md)

Use the native HTTP module built for the installed NGINX ABI. These examples
configure HTTP/1.1 request and response inspection through P1–P4.

## Files

| Configuration | Purpose |
| --- | --- |
| [off/nginx.conf](off/nginx.conf) | Native intervention handling with the additional late policy off |
| [safe/nginx.conf](safe/nginx.conf) | Safe P1–P4 starting reference |
| [strict/nginx.conf](strict/nginx.conf) | Strict configuration shape requiring host validation |
| [all/nginx.conf](all/nginx.conf) | Full directive layout using `modsecurity_phase4_mode strict` |
| [detection-only/nginx.conf](detection-only/nginx.conf) | Active connector with DetectionOnly rules |
| [disabled/nginx.conf](disabled/nginx.conf) | Connector disabled with `modsecurity off` |

`all` names the layout. The accepted Phase-4 values are `off`, `safe`, and `strict`.

## Values to adapt

Set the module path, `modsecurity_rules_file`, listener, `server_name`, upstream,
and log destinations for the target installation. Check the actual bind
address before exposing the service. Keep gzip off until the inspected byte
representation has been validated. Body access, MIME selection, inspection
limits, and limit actions belong in engine rules. Remove the obsolete
`modsecurity_phase4_body_limit`.

The optional `modsecurity_phase4_log` sink requires a safe parent directory,
a regular file, suitable ownership, and private descriptor mode `0600`. Rotate
it through a validated configuration reload. Generic NGINX `USR1` reopening is
unsupported. `modsecurity_use_error_log` controls forwarding engine messages
to the NGINX error log.

Enable `modsecurity_transaction_id` only with a unique server-generated value.
The commented `$request_id` expression requires that host variable. Remote-rule
credentials and endpoints require operator configuration. Syntax, contexts,
and defaults are in the generated
[configuration reference](configuration-reference.md).

## Profiles

### DetectionOnly profile

[rules/detection-only.conf](rules/detection-only.conf) evaluates rules and
records matches while suppressing disruptive engine actions.

### Disabled profile

`modsecurity off` stops the access-handler connector path. Rules can still load
during configuration parsing. With the connector active,
[rules/engine-off.conf](rules/engine-off.conf) disables engine evaluation
through `SecRuleEngine Off`.

## P1--P4 Safe intent

[rules/request-only.conf](rules/request-only.conf) enables request inspection.
[rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) adds response inspection and
local illustration rule `9001801`. The P4 body filter runs after the
response-header path. Safe records late outcomes after output has started.
A replacement client-visible 403 requires an earlier decision.

## Strict profile boundary <a id="strict-profile-boundary"></a>

The Strict file is parser-supported. Validate post-commit abort behavior on the
installed NGINX host before relying on it. These files describe configuration
intent. Hosted event-sink checks and protected NGINX attestation retain their
separate execution requirements.

## No-CRS rules

Install a reviewed copy of the [No-CRS baseline](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)
at the configured rules path. Its IDs `1100001`, `1100101`, `1100201`, and
`1100301` correspond to P1, P2, P3, and P4. The local rule `9001801` is an
illustration. See the [shared rule guide](../common/rule-examples.md).

## Validation

After adapting paths and endpoints, check the complete installed configuration.

~~~sh
nginx -t
~~~

After an intentional reload, inspect NGINX and ModSecurity logs. Runtime
enforcement requires profile-specific traffic evidence. See the
[NGINX connector guide](../../connectors/nginx/README.md) and
[examples index](../README.md).
