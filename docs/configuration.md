# Configuration

**Language:** English | [Deutsch](configuration.de.md)

## Start with the layer you need to change

A host configuration attaches a connector to traffic. Common Runtime settings
configure shared processing where the selected integration uses a runtime
file. ModSecurity rules configure engine inspection and rule evaluation. A
setting at one layer does not automatically change another layer.

| Layer | Purpose | Canonical detail |
| --- | --- | --- |
| Host or connector | Registers and configures a selected host integration | The relevant connector guide and its complete example reference |
| Common Runtime | Parses the selected local key/value service configuration where a route uses it | [Common Runtime reference](../examples/common/common-connector-configuration.md) |
| ModSecurity Engine | Loads and evaluates <code>Sec*</code> rules | [Engine-directive reference](../examples/common/modsecurity-directives.md) |

For a first setup, choose the matching [example](../examples/README.md), then
read its host-specific adaptation and validation instructions. For an existing
setup, read [Migration](migration.md) before copying old options.

## Body inspection is engine-owned

Request limits/actions use `SecRequestBodyLimit`,
`SecRequestBodyNoFilesLimit`, and `SecRequestBodyLimitAction`. Response
limits/actions use `SecResponseBodyLimit` and `SecResponseBodyLimitAction`.
Access remains controlled by `SecRequestBodyAccess` and
`SecResponseBodyAccess`; response MIME selection remains controlled by
`SecResponseBodyMimeType` and `SecResponseBodyMimeTypesClear`.

Connector cumulative settings including `request_body_limit`,
`response_body_limit`, `body_limit_action`, and
`modsecurity_phase4_body_limit` are removed. They are not compatibility aliases
or replacement host-capacity settings. The connector must not supply engine
limit defaults, infer them from rule text, choose Reject/ProcessPartial, or
truncate a body to a connector-defined inspection prefix. Omitted directives
retain native engine semantics.

Per-frame/message limits, bounded working memory, metadata limits, timeouts,
file validation, and the actual authorization-host ceilings remain independent.
The [body-limit contract](phase4-mode-budget.md) and
[ten-profile matrix](body-inspection-review-matrix.md) describe these boundaries.

## Configuration principles

Use a profile only with the connector and host syntax for which it is written.
Keep build, cache, runtime, log, and evidence output outside the checkout.
Supply secrets through an external secret mechanism; do not put them in
checked-in examples, rules, command lines intended for review, or generated
evidence.

`SecRuleEngine`, host connector enable/disable switches, body-access controls,
and Phase-4 modes are distinct. An enabled connector can load a ruleset with
`SecRuleEngine Off`. `DetectionOnly` evaluates/logs without applying disruptive
rule actions; it retains native engine limit semantics.

## Profiles and late behavior

The Phase-4 policy controls supported handling of a response-phase decision,
not MIME selection, body size, or an engine limit action. It cannot take back
bytes already sent to the client.

| Profile | Intended use | Boundary |
| --- | --- | --- |
| Off | No additional Safe/Strict late-action policy; selected host/service shape remains enabled | Native inspection and intervention/error handling remain active as configured |
| Safe | Selected P1–P4 reference with conservative late handling | Does not permit ignoring native Reject results or genuine errors |
| Strict | Requests the selected profile's supported strict host action | Startup can reject unsupported actions; no universal late-abort claim |
| DetectionOnly | Engine rules evaluate and log | Disruptive rule actions are not applied |
| Disabled | Engine or host integration is disabled as documented | Does not test the enabled connector route |

`all` is the complete example layout and not a fourth Phase-4 mode. A layout
using `strict` is not automatically admissible on every host. Shared Phase-4
source defaults use `off`; an explicit example value is not a source default.

The checked-in profile files and generated references are the source of truth
for syntax, defaults, contexts, merge rules, placeholders, and validation.

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
change the selected integration mode or establish support for another path.
A response companion does not remove its authorization host's request buffer
or protocol-sampling limitations.

## Variables, placeholders, and validation

[Variables](reference/variables.md) defines allowed format, defaults, setter,
scope, effects, examples, and safety notes for repository/harness variables.
[Version pins](reference/version-pins.md) explains toolchain and revision
ownership. These inputs are not arbitrary host directives.

Validate selected host configuration with the documented native checker or
`make check-config-<connector>` where the root target exists. Replace the
placeholder with the actual host-family target, such as
`make check-config-nginx`. A successful load neither executes traffic nor
promotes a runtime result. See [Testing and evidence](testing-and-evidence.md).

## Directive parity and compatibility

Shared names do not imply identical host syntax, context, inheritance, or
evaluation. Apache expressions are not NGINX directives. Common Runtime keys
must not be documented as unregistered host directives.

| Surface | Apache | NGINX | Boundary |
| --- | --- | --- | --- |
| <code>modsecurity</code>, rules, rules file | Registered host directives | Registered host directives | Local rule loading remains connector-owned |
| <code>modsecurity_rules_remote</code> | Registered but rejected by the shared security policy | Registered but rejected by the shared security policy | Rejected before a fetch or native remote API call |
| <code>modsecurity_transaction_id</code> | Static-string semantics | Per-request complex-value semantics | The same name does not imply the same evaluation |
| <code>modsecurity_transaction_id_expr</code> | Registered Apache expression directive | Not registered | Do not copy Apache expression syntax to NGINX |
| Phase-4 mode and event logging | Host-specific registered controls | Host-specific registered controls | Removed connector body-size directives are not reintroduced by shared metadata |
| HAProxy configuration | Separate native HTX host configuration | Not applicable | SPOE/SPOP is a separate sample/companion surface |

Shared metadata stays connector-neutral. Host registration, merge behavior,
lifetimes, hooks, filters, and actual runtime actions remain connector-owned.

## Related references

- [Architecture](architecture.md)
- [Connector guides](connectors/README.md)
- [Common rule examples](../examples/common/rule-examples.md)
- [Glossary](reference/glossary.md)
- [Migration](migration.md)
