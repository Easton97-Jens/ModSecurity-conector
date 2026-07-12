# HAProxy configuration reference

**Language:** English | [Deutsch](configuration-reference.de.md)

## Scope and source of truth

Selected integration mode: `native-htx-filter`. This file is generated from registered parsers, configuration structures, checked service contracts, and active examples.
Compatibility entries are explicitly labelled and are not part of the selected core path.

## Configuration inventory

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`bind`](#bind) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`default_backend`](#default-backend) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`filter modsecurity-htx`](#filter-modsecurity-htx) | Host / Connector | HAProxy filter declaration | yes | not applicable; a filter is active only when declared | The selected and checked-in native use is a HAProxy frontend. The local parser does not assert additional host scopes. | Native HTX full-lifecycle filter declaration. |
| [`log`](#log) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`mode`](#mode) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`phase4-mode`](#phase4-mode) | Host / Connector | enum | no | safe | The selected and checked-in native use is a HAProxy frontend. The local parser does not assert additional host scopes. | Native HTX late-P4 policy argument. |
| [`rules-file`](#rules-file) | Host / Connector | path | yes | none; required | The selected and checked-in native use is a HAProxy frontend. The local parser does not assert additional host scopes. | Required native HTX rule-file argument. |
| [`server`](#server) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`timeout client`](#timeout-client) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`timeout connect`](#timeout-connect) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`timeout server`](#timeout-server) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`filter spoe`](#filter-spoe) | Compatibility | compatibility filter | no | not part of the native HTX path | Compatibility frontend only | Compatibility-only SPOE filter. |
| [`legacy-phase4-strict-abort`](#legacy-phase4-strict-abort) | Compatibility | historical configuration | no | not available | Historical compatibility documentation only | Disabled historical compatibility material. |
| [`spoe-agent:audit-log`](#spoe-agent-audit-log) | Compatibility | string/path | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:case`](#spoe-agent-case) | Compatibility | string/path | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:crs-root`](#spoe-agent-crs-root) | Compatibility | string/path | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:debug`](#spoe-agent-debug) | Compatibility | boolean | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:decision-log`](#spoe-agent-decision-log) | Compatibility | string/path | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:enable-response-headers`](#spoe-agent-enable-response-headers) | Compatibility | boolean | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support. |
| [`spoe-agent:expected-status`](#spoe-agent-expected-status) | Compatibility | integer | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:fail-mode`](#spoe-agent-fail-mode) | Compatibility | compatibility policy string | no | closed | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:host`](#spoe-agent-host) | Compatibility | string/path | no | 127.0.0.1 | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:listen`](#spoe-agent-listen) | Compatibility | string/path | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:log-file`](#spoe-agent-log-file) | Compatibility | string/path | no | - | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:max-transactions`](#spoe-agent-max-transactions) | Compatibility | integer | no | 4096 | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:mode`](#spoe-agent-mode) | Compatibility | compatibility policy string | no | block | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:modsecurity-conf`](#spoe-agent-modsecurity-conf) | Compatibility | string/path | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:pid-file`](#spoe-agent-pid-file) | Compatibility | string/path | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:port`](#spoe-agent-port) | Compatibility | integer | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:port-file`](#spoe-agent-port-file) | Compatibility | string/path | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:ready-file`](#spoe-agent-ready-file) | Compatibility | string/path | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:request-body-limit`](#spoe-agent-request-body-limit) | Compatibility | integer | no | 65532 | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:response-body-limit`](#spoe-agent-response-body-limit) | Compatibility | integer | no | 0 | SPOE/SPOP compatibility agent key=value file | Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support. |
| [`spoe-agent:response-body-timeout`](#spoe-agent-response-body-timeout) | Compatibility | integer | no | 0 | SPOE/SPOP compatibility agent key=value file | Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support. |
| [`spoe-agent:response-phases`](#spoe-agent-response-phases) | Compatibility | boolean | no | false | SPOE/SPOP compatibility agent key=value file | Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support. |
| [`spoe-agent:rules-dir`](#spoe-agent-rules-dir) | Compatibility | string/path | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:rules-file`](#spoe-agent-rules-file) | Compatibility | string/path | no | unset unless configured | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:runtime-mode`](#spoe-agent-runtime-mode) | Compatibility | compatibility policy string | no | production | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:spoe-timeout`](#spoe-agent-spoe-timeout) | Compatibility | integer | no | 2000 | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:variant`](#spoe-agent-variant) | Compatibility | string/path | no | - | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |
| [`spoe-agent:worker-count`](#spoe-agent-worker-count) | Compatibility | integer | no | 1 | SPOE/SPOP compatibility agent key=value file | SPOP compatibility-agent configuration; it is not a native HTX filter option. |

## Layer separation

Host/connector switches bind or configure host integration. They are not the same setting as `SecRuleEngine`.

- [Common Runtime configuration](../common/common-connector-configuration.md) covers only the `key=value` runtime file and is not presented as an unregistered host directive.
- [ModSecurity Engine directives](../common/modsecurity-directives.md) covers `Sec*` directives in the loaded rule file.
- [Rule examples](../common/rule-examples.md) explains DetectionOnly and engine Off.

## Common Runtime relevance

The selected native path does not parse a Common Runtime `key=value` file; shared model fields are exposed only through registered host directives.

## Engine directives used by profiles

The local rule profiles use `SecRuleEngine` for On, DetectionOnly, and Off. Where body inspection is selected, `SecRequestBodyAccess`, `SecResponseBodyAccess`, MIME scope, limits, and `SecRule` remain ModSecurity Engine directives.

See [Engine reference](../common/modsecurity-directives.md).

## Profiles

| Profile | File | Status |
| --- | --- | --- |
| Minimal | [minimal/haproxy-htx.cfg](minimal/haproxy-htx.cfg) | Active starter configuration |
| Safe full lifecycle | [safe/haproxy-htx.cfg](safe/haproxy-htx.cfg) | Selected bounded reference |
| Strict | [README.md#strict-profile-boundary](README.md#strict-profile-boundary) | Parser-supported or explicitly optional boundary |
| DetectionOnly | [detection-only/haproxy-htx.cfg](detection-only/haproxy-htx.cfg) | Engine evaluates/logs without disruptive action |
| Disabled | [disabled/haproxy-htx.cfg](disabled/haproxy-htx.cfg) | Connector or engine path disabled |

## Configuration combinations

| Connector | Engine | Request body | Response body | Result |
| --- | --- | --- | --- | --- |
| off | On | any | any | No connector transaction; engine setting is not reached. |
| on | Off | any | any | Connector reaches the engine, but engine rule processing is disabled. |
| on | DetectionOnly | enabled | enabled | Rules can match/log without disruptive enforcement. |
| on | On | Off | On | P2 body is unavailable to the engine; P4 remains host/capability dependent. |
| on | On | On | Off | P4 body is unavailable to the engine. |
| on | On | On | On + safe | Late post-commit P4 results are recorded without a promised later status change. |
| on | On | On | On + strict | Only use a host-specific strict outcome where source/evidence supports it; no synthetic late 403. |
| on | On | over limit + process_partial | over limit + reject | The body policy determines bounded engine input; exact host response handling remains connector-specific. |

## Validation

```sh
haproxy -c -f <config>
```

Repository targets: `make check-config-haproxy` and `make check-config-all-connectors`.

## Option details

<a id="bind"></a>
## `bind`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
bind <host-specific-value>
```

### Valid contexts

- The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| host-owned configuration field | the explicit value in the selected checked-in example | no |

### Default

No connector default; this host field is explicit in the example.

Source: `active example configuration`.

### Inheritance and merge

Host-defined; not implemented by this connector.

Merge: Host-defined; not implemented by this connector.

### Phases and runtime effect

Host setup/routing/logging; it does not itself configure ModSecurity rule-engine phases.

Provides surrounding host setup used by the selected connector example.

### Validation and errors

haproxy -c -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="default-backend"></a>
## `default_backend`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
default_backend <host-specific-value>
```

### Valid contexts

- The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| host-owned configuration field | the explicit value in the selected checked-in example | no |

### Default

No connector default; this host field is explicit in the example.

Source: `active example configuration`.

### Inheritance and merge

Host-defined; not implemented by this connector.

Merge: Host-defined; not implemented by this connector.

### Phases and runtime effect

Host setup/routing/logging; it does not itself configure ModSecurity rule-engine phases.

Provides surrounding host setup used by the selected connector example.

### Validation and errors

haproxy -c -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="filter-modsecurity-htx"></a>
## `filter modsecurity-htx`

### Short description

Native HTX full-lifecycle filter declaration.

### Syntax

```text
filter modsecurity-htx rules-file <path> [phase4-mode minimal|safe|strict]
```

### Valid contexts

- The selected and checked-in native use is a HAProxy frontend. The local parser does not assert additional host scopes.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| HAProxy filter declaration | one required rules-file argument; optional phase4-mode | yes |

### Default

not applicable; a filter is active only when declared

Source: `native HTX keyword parser`.

### Inheritance and merge

No connector-local inheritance callback is registered; each filter declaration owns one filter configuration.

Merge: No connector-local merge; filter arguments initialise a per-filter common configuration.

### Phases and runtime effect

P1–P4 native HTX callbacks are attached only when this filter is declared.

Registers the repository's native HTX filter and creates the config passed to the lifecycle callbacks.

### Validation and errors

The patched HAProxy parser rejects missing/unknown arguments; validate with haproxy -c -f <config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Safety and operations

A stock HAProxy binary does not provide this keyword; do not silently substitute SPOE.

<a id="log"></a>
## `log`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
log <host-specific-value>
```

### Valid contexts

- The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| host-owned configuration field | the explicit value in the selected checked-in example | no |

### Default

No connector default; this host field is explicit in the example.

Source: `active example configuration`.

### Inheritance and merge

Host-defined; not implemented by this connector.

Merge: Host-defined; not implemented by this connector.

### Phases and runtime effect

Host setup/routing/logging; it does not itself configure ModSecurity rule-engine phases.

Provides surrounding host setup used by the selected connector example.

### Validation and errors

haproxy -c -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="mode"></a>
## `mode`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
mode <host-specific-value>
```

### Valid contexts

- The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| host-owned configuration field | the explicit value in the selected checked-in example | no |

### Default

No connector default; this host field is explicit in the example.

Source: `active example configuration`.

### Inheritance and merge

Host-defined; not implemented by this connector.

Merge: Host-defined; not implemented by this connector.

### Phases and runtime effect

Host setup/routing/logging; it does not itself configure ModSecurity rule-engine phases.

Provides surrounding host setup used by the selected connector example.

### Validation and errors

haproxy -c -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="phase4-mode"></a>
## `phase4-mode`

### Short description

Native HTX late-P4 policy argument.

### Syntax

```text
phase4-mode minimal | safe | strict
```

### Valid contexts

- The selected and checked-in native use is a HAProxy frontend. The local parser does not assert additional host scopes.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| enum | minimal \| safe \| strict | no |

### Default

safe

Source: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE`.

### Inheritance and merge

No connector-local inheritance callback is registered; each filter declaration owns one filter configuration.

Merge: No connector-local merge; filter arguments initialise a per-filter common configuration.

### Phases and runtime effect

P4 only. The current HTX host action distinguishes strict from non-strict; minimal and safe share the non-strict late log-only path.

Initialises common_config.phase4_mode for the filter.

### Validation and errors

Unknown mode fails parsing. The selected host uses haproxy -c -f <config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Safety and operations

strict records an abort policy request but the native HTX path currently records host action not_attempted; it is not an abort guarantee.

<a id="rules-file"></a>
## `rules-file`

### Short description

Required native HTX rule-file argument.

### Syntax

```text
rules-file <path>
```

### Valid contexts

- The selected and checked-in native use is a HAProxy frontend. The local parser does not assert additional host scopes.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| path | one readable rules/configuration path | yes |

### Default

none; required

Source: `native HTX parser requires rules-file`.

### Inheritance and merge

No connector-local inheritance callback is registered; each filter declaration owns one filter configuration.

Merge: No connector-local merge; filter arguments initialise a per-filter common configuration.

### Phases and runtime effect

Rules can evaluate P1–P4 through the declared HTX filter.

Loads rules with msc_rules_add_file during filter initialisation.

### Validation and errors

Missing argument or rule-load failure fails native filter initialisation.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Safety and operations

Protect policy-file ownership and permissions.

<a id="server"></a>
## `server`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
server <host-specific-value>
```

### Valid contexts

- The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| host-owned configuration field | the explicit value in the selected checked-in example | no |

### Default

No connector default; this host field is explicit in the example.

Source: `active example configuration`.

### Inheritance and merge

Host-defined; not implemented by this connector.

Merge: Host-defined; not implemented by this connector.

### Phases and runtime effect

Host setup/routing/logging; it does not itself configure ModSecurity rule-engine phases.

Provides surrounding host setup used by the selected connector example.

### Validation and errors

haproxy -c -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="timeout-client"></a>
## `timeout client`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
timeout client <host-specific-value>
```

### Valid contexts

- The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| host-owned configuration field | the explicit value in the selected checked-in example | no |

### Default

No connector default; this host field is explicit in the example.

Source: `active example configuration`.

### Inheritance and merge

Host-defined; not implemented by this connector.

Merge: Host-defined; not implemented by this connector.

### Phases and runtime effect

Host setup/routing/logging; it does not itself configure ModSecurity rule-engine phases.

Provides surrounding host setup used by the selected connector example.

### Validation and errors

haproxy -c -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="timeout-connect"></a>
## `timeout connect`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
timeout connect <host-specific-value>
```

### Valid contexts

- The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| host-owned configuration field | the explicit value in the selected checked-in example | no |

### Default

No connector default; this host field is explicit in the example.

Source: `active example configuration`.

### Inheritance and merge

Host-defined; not implemented by this connector.

Merge: Host-defined; not implemented by this connector.

### Phases and runtime effect

Host setup/routing/logging; it does not itself configure ModSecurity rule-engine phases.

Provides surrounding host setup used by the selected connector example.

### Validation and errors

haproxy -c -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="timeout-server"></a>
## `timeout server`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
timeout server <host-specific-value>
```

### Valid contexts

- The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts.

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| host-owned configuration field | the explicit value in the selected checked-in example | no |

### Default

No connector default; this host field is explicit in the example.

Source: `active example configuration`.

### Inheritance and merge

Host-defined; not implemented by this connector.

Merge: Host-defined; not implemented by this connector.

### Phases and runtime effect

Host setup/routing/logging; it does not itself configure ModSecurity rule-engine phases.

Provides surrounding host setup used by the selected connector example.

### Validation and errors

haproxy -c -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/safe/haproxy-htx.cfg](../../examples/haproxy/safe/haproxy-htx.cfg).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="filter-spoe"></a>
## `filter spoe`

### Short description

Compatibility-only SPOE filter.

### Syntax

```text
filter spoe engine <name> config <file>
```

### Valid contexts

- Compatibility frontend only

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| compatibility filter | HAProxy SPOE syntax only | no |

### Default

not part of the native HTX path

Source: `compatibility example`.

### Inheritance and merge

not documented as native inheritance

Merge: not part of native HTX merge

### Phases and runtime effect

Compatibility request path; it is not a native HTX P3/P4 configuration.

Routes to the separate SPOE/SPOP compatibility service.

### Validation and errors

Separate compatibility smoke/configuration only.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/haproxy-request-only.cfg](../../examples/haproxy/compatibility-spoe/haproxy-request-only.cfg).

### Safety and operations

Do not promote this historical path as the selected native core.

<a id="legacy-phase4-strict-abort"></a>
## `legacy-phase4-strict-abort`

### Short description

Disabled historical compatibility material.

### Syntax

```text
legacy / disabled example
```

### Valid contexts

- Historical compatibility documentation only

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| historical configuration | not an active selected option | no |

### Default

not available

Source: `legacy example header`.

### Inheritance and merge

not applicable

Merge: not applicable

### Phases and runtime effect

No selected response-body P4 path.

Retained solely to explain retired compatibility material.

### Validation and errors

Do not use for native validation.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/legacy-phase4-strict-abort.cfg](../../examples/haproxy/compatibility-spoe/legacy-phase4-strict-abort.cfg).

### Safety and operations

Never use as P4 or strict-abort evidence.

<a id="spoe-agent-audit-log"></a>
## `spoe-agent:audit-log`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
audit-log=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-case"></a>
## `spoe-agent:case`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
case=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-crs-root"></a>
## `spoe-agent:crs-root`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
crs-root=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-debug"></a>
## `spoe-agent:debug`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
debug=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| boolean | on/off-style compatibility boolean | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-decision-log"></a>
## `spoe-agent:decision-log`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
decision-log=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-enable-response-headers"></a>
## `spoe-agent:enable-response-headers`

### Short description

Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support.

### Syntax

```text
enable-response-headers=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| boolean | on/off-style compatibility boolean | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-expected-status"></a>
## `spoe-agent:expected-status`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
expected-status=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| integer | decimal integer | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-fail-mode"></a>
## `spoe-agent:fail-mode`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
fail-mode=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| compatibility policy string | parser-supported compatibility value | no |

### Default

closed

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-host"></a>
## `spoe-agent:host`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
host=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

127.0.0.1

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-listen"></a>
## `spoe-agent:listen`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
listen=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-log-file"></a>
## `spoe-agent:log-file`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
log-file=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

-

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-max-transactions"></a>
## `spoe-agent:max-transactions`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
max-transactions=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| integer | decimal integer | no |

### Default

4096

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-mode"></a>
## `spoe-agent:mode`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
mode=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| compatibility policy string | parser-supported compatibility value | no |

### Default

block

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-modsecurity-conf"></a>
## `spoe-agent:modsecurity-conf`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
modsecurity-conf=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-pid-file"></a>
## `spoe-agent:pid-file`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
pid-file=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-port"></a>
## `spoe-agent:port`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
port=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| integer | decimal integer | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-port-file"></a>
## `spoe-agent:port-file`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
port-file=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-ready-file"></a>
## `spoe-agent:ready-file`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
ready-file=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-request-body-limit"></a>
## `spoe-agent:request-body-limit`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
request-body-limit=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| integer | decimal integer | no |

### Default

65532

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-response-body-limit"></a>
## `spoe-agent:response-body-limit`

### Short description

Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support.

### Syntax

```text
response-body-limit=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| integer | decimal integer | no |

### Default

0

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-response-body-timeout"></a>
## `spoe-agent:response-body-timeout`

### Short description

Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support.

### Syntax

```text
response-body-timeout=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| integer | decimal integer | no |

### Default

0

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-response-phases"></a>
## `spoe-agent:response-phases`

### Short description

Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support.

### Syntax

```text
response-phases=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| boolean | on/off-style compatibility boolean | no |

### Default

false

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

Compatibility response control. The selected SPOE messages do not supply a response body, so this is not native P4 support.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-rules-dir"></a>
## `spoe-agent:rules-dir`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
rules-dir=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-rules-file"></a>
## `spoe-agent:rules-file`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
rules-file=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

unset unless configured

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-runtime-mode"></a>
## `spoe-agent:runtime-mode`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
runtime-mode=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| compatibility policy string | parser-supported compatibility value | no |

### Default

production

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-spoe-timeout"></a>
## `spoe-agent:spoe-timeout`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
spoe-timeout=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| integer | decimal integer | no |

### Default

2000

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-variant"></a>
## `spoe-agent:variant`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
variant=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/path | parser-supported compatibility value | no |

### Default

-

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.

<a id="spoe-agent-worker-count"></a>
## `spoe-agent:worker-count`

### Short description

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Syntax

```text
worker-count=<value>
```

### Valid contexts

- SPOE/SPOP compatibility agent key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| integer | decimal integer | no |

### Default

1

Source: `config_init() where stated; otherwise zero/empty initialization`.

### Inheritance and merge

No native HTX inheritance; one compatibility-agent config file.

Merge: No merge; config_set applies one parsed value.

### Phases and runtime effect

Compatibility request/response-header path only; no native response-body lifecycle claim.

SPOP compatibility-agent configuration; it is not a native HTX filter option.

### Validation and errors

Unknown keys fail compatibility-agent configuration parsing.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/haproxy/compatibility-spoe/modsecurity-agent.conf](../../examples/haproxy/compatibility-spoe/modsecurity-agent.conf).

### Safety and operations

Compatibility logs, ports, rules, and fail policy require operator review; do not promote this path to the selected native core.
