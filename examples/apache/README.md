# Apache native-module examples

**Language:** English | [Deutsch](README.de.md)

Use the native httpd module built for the installed Apache ABI. These HTTP/1.1
references cover request headers/body (P1/P2) and response headers/body (P3/P4).

## Files

| Configuration | Purpose |
| --- | --- |
| [off/httpd.conf](off/httpd.conf) | Native intervention handling with the additional late policy off |
| [safe/httpd.conf](safe/httpd.conf) | Safe P1–P4 starting reference |
| [strict/httpd.conf](strict/httpd.conf) | Strict late-action policy |
| [all/httpd.conf](all/httpd.conf) | Full parameter layout using `modsecurity_phase4_mode strict` |
| [detection-only/httpd.conf](detection-only/httpd.conf) | Active connector with DetectionOnly rules |
| [disabled/httpd.conf](disabled/httpd.conf) | Connector disabled with `modsecurity off` |

`all` names the layout. The accepted Phase-4 values are `off`, `safe`, and `strict`.

## Values to adapt

Set the installed module path, `modsecurity_rules_file`, listener/upstream,
and log destinations. `/etc/modsecurity` and `/var/log` paths are installation
examples. Configure body access, MIME scope, inspection limits, and limit
actions in engine rules. Remove the obsolete `modsecurity_phase4_body_limit`.

For `modsecurity_phase4_log`, protect and rotate request metadata. A root-owned
parent directory must be protected against group/other writes. Pre-create the
regular log file with Apache-worker ownership and preserve that ownership on
rotation. The opener sets mode `0600`.

The correlation overrides in `all/httpd.conf` remain commented. Enable
`modsecurity_transaction_id_expr` or `modsecurity_transaction_id` only with a
validated, unique host-generated value. Read the generated
[configuration reference](configuration-reference.md) for syntax, defaults,
and merge behavior.

## Profiles

### DetectionOnly profile

DetectionOnly evaluates rules and records matches while suppressing disruptive
engine actions. Use [rules/detection-only.conf](rules/detection-only.conf).

### Disabled profile

`modsecurity off` prevents connector transaction creation. With the connector
active, [rules/engine-off.conf](rules/engine-off.conf) disables engine rule
evaluation through `SecRuleEngine Off`.

## P1--P4 Safe intent

[rules/request-only.conf](rules/request-only.conf) enables request inspection.
[rules/p1-p4-safe.conf](rules/p1-p4-safe.conf) adds response inspection and local
illustration rule `9002801`. Apache appends each data bucket to the engine,
forwards it, and resolves the final body decision at EOS. After response
commitment, Safe records a disruptive result as `log_only` and continues.

## Strict profile boundary <a id="strict-profile-boundary"></a>

Strict selects the native connection-abort path after commitment. Validate the
client-visible outcome on the installed host before relying on it. The focused
regression entry point is
`ci/runtime/lifecycle/run-apache-phase4-response-regression.sh`.

## No-CRS rules

Install a reviewed copy of the [No-CRS baseline](../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)
at the configured rules path. Its IDs `1100001`, `1100101`, `1100201`, and
`1100301` correspond to P1, P2, P3, and P4. The local rule `9002801` is an
illustration. Rule IDs and engine examples are explained in the
[shared rule guide](../common/rule-examples.md).

## Validation

After installing the selected files and adapting paths, check the complete
Apache configuration.

~~~sh
apachectl -t
~~~

After an intentional reload, inspect the error, decision, and audit logs.
Runtime enforcement requires profile-specific traffic evidence. See the
[Apache connector guide](../../connectors/apache/README.md) and
[examples index](../README.md).
