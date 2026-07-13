# Configuration

**Language:** English | [Deutsch](configuration.de.md)

## Scope

Configuration has three separate layers. A setting at one layer is not an
implicit setting at another layer, and no setting alone proves a runtime
outcome.

| Layer | Purpose | Canonical detail |
| --- | --- | --- |
| Host or connector | Registers and configures a selected host integration | The relevant connector guide and its complete example reference |
| Common Runtime | Parses the selected local key/value service configuration where a route uses it | [Common Runtime reference](../examples/common/common-connector-configuration.md) |
| ModSecurity Engine | Loads and evaluates <code>Sec*</code> rules | [Engine-directive reference](../examples/common/modsecurity-directives.md) |

## Configuration principles

Use a configuration profile only with the connector and host syntax for which
it is written. Keep build, cache, runtime, log, and evidence output outside
the repository checkout. Supply secrets through an appropriate external secret
mechanism; do not place them in checked-in examples, rules, or generated
evidence.

<code>SecRuleEngine</code>, a host connector enable/disable switch, body-access
controls, and a P4 mode are distinct controls. In particular, an enabled host
connector can load a ruleset with <code>SecRuleEngine Off</code>, and
<code>DetectionOnly</code> evaluates/logs without applying disruptive rule
actions.

## Profiles and late behavior

| Profile | Intended use | Boundary |
| --- | --- | --- |
| Minimal | Smallest selected host/service shape | It is a syntax/configuration starting point, not lifecycle evidence |
| Safe | Selected P1--P4-safe reference | Post-commit observations remain conservative and payload-safe |
| Strict | Explicitly separate optional profile | It is not proof of a client-visible late abort |
| DetectionOnly | Rules evaluate and log | Disruptive rule actions are not applied |
| Disabled | Engine or host integration is disabled as documented | It does not test the enabled connector route |

The checked-in profile files are the source of truth. Their complete connector
syntax, defaults, contexts, merge rules, placeholders, and validation notes are
generated from source contracts and examples.

## Complete connector references

| Connector | Full directive/configuration reference |
| --- | --- |
| Apache | [Apache](../examples/apache/configuration-reference.md) |
| NGINX | [NGINX](../examples/nginx/configuration-reference.md) |
| HAProxy | [HAProxy](../examples/haproxy/configuration-reference.md) |
| Envoy | [Envoy](../examples/envoy/configuration-reference.md) |
| Traefik | [Traefik](../examples/traefik/configuration-reference.md) |
| lighttpd | [lighttpd](../examples/lighttpd/configuration-reference.md) |

Compatibility entries in those references are deliberately marked. They do not
change the selected integration mode or establish support for an unselected
path.

## Variables, placeholders, and validation

The detailed repository and harness variable reference is
[Variables](reference/variables.md). It defines allowed format, default,
setter, scope, effect, examples, and safety notes for each documented variable
or placeholder.

Validate a selected host configuration with <code>make check-config-&lt;connector&gt;</code>
where the target exists. A successful config load does not execute traffic,
validate rules beyond that check's scope, or promote a runtime result. Use the
[testing and evidence guide](testing-and-evidence.md) for the distinction.

## Directive parity and compatibility

Directive names may be shared while host parser syntax, context, inheritance,
and evaluation semantics differ. Apache expression syntax is not an NGINX
directive, and Common Runtime keys must not be documented as unregistered host
directives. Keep compatibility paths separate from the selected native route;
their examples describe only their stated boundary.

| Surface | Apache | NGINX | Boundary |
| --- | --- | --- |
| <code>modsecurity</code>, rules, rules file, remote rules | Registered host directives | Registered host directives | Rule loading remains connector-owned |
| <code>modsecurity_transaction_id</code> | Static-string semantics | Per-request complex-value semantics | Same name does not mean identical evaluation |
| <code>modsecurity_transaction_id_expr</code> | Registered Apache expression directive | Not registered | Do not copy Apache expression syntax to NGINX |
| Bounded P4 controls | Registered host directives | Registered host directives | Body limit/scope does not promote full response-body support |
| HAProxy configuration | Native HTX host configuration | Not applicable | Historical SPOE/SPOP remains a separate compatibility surface |

Shared directive metadata is connector-neutral; host registration, merge,
lifetimes, hooks, filters, and actual runtime effects remain connector-owned.

## Related references

- [Architecture](architecture.md)
- [Connector guides](connectors/README.md)
- [Common rule examples](../examples/common/rule-examples.md)
- [Glossary](reference/glossary.md)
