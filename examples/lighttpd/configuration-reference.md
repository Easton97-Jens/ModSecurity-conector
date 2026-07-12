# lighttpd configuration reference

**Language:** English | [Deutsch](configuration-reference.de.md)

## Scope and source of truth

Selected integration mode: `patched-native-lighttpd`. This file is generated from registered parsers, configuration structures, checked service contracts, and active examples.
Compatibility entries are explicitly labelled and are not part of the selected core path.

## Configuration inventory

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`msconnector.config-file`](#msconnector-config-file) | Host / Connector | path | yes | none | T_CONFIG_SCOPE_SERVER | Path to the Common Runtime configuration used by the native plugin. |
| [`msconnector.enabled`](#msconnector-enabled) | Host / Connector | lighttpd boolean | no | off | T_CONFIG_SCOPE_SERVER | Enables the native lighttpd plugin. |
| [`proxy.server`](#proxy-server) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`server.bind`](#server-bind) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`server.compat-module-load`](#server-compat-module-load) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`server.document-root`](#server-document-root) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`server.errorlog`](#server-errorlog) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`server.modules`](#server-modules) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`server.pid-file`](#server-pid-file) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`server.port`](#server-port) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`server.stream-response-body`](#server-stream-response-body) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`server.upload-dirs`](#server-upload-dirs) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`compatibility.accesslog.filename`](#compatibility-accesslog-filename) | Compatibility | lighttpd compatibility host field | no | not part of native mod_msconnector | lighttpd sidecar compatibility configuration | Compatibility-only lighttpd host field. |
| [`compatibility.proxy.server`](#compatibility-proxy-server) | Compatibility | lighttpd compatibility host field | no | not part of native mod_msconnector | lighttpd sidecar compatibility configuration | Compatibility-only lighttpd host field. |
| [`compatibility.server.document-root`](#compatibility-server-document-root) | Compatibility | lighttpd compatibility host field | no | not part of native mod_msconnector | lighttpd sidecar compatibility configuration | Compatibility-only lighttpd host field. |
| [`compatibility.server.errorlog`](#compatibility-server-errorlog) | Compatibility | lighttpd compatibility host field | no | not part of native mod_msconnector | lighttpd sidecar compatibility configuration | Compatibility-only lighttpd host field. |
| [`compatibility.server.modules`](#compatibility-server-modules) | Compatibility | lighttpd compatibility host field | no | not part of native mod_msconnector | lighttpd sidecar compatibility configuration | Compatibility-only lighttpd host field. |
| [`compatibility.server.port`](#compatibility-server-port) | Compatibility | lighttpd compatibility host field | no | not part of native mod_msconnector | lighttpd sidecar compatibility configuration | Compatibility-only lighttpd host field. |
| [`sidecar proxy`](#sidecar-proxy) | Compatibility | compatibility host setup | no | not a native connector option | Compatibility example | Compatibility-only sidecar proxy setup. |

## Layer separation

Host/connector switches bind or configure host integration. They are not the same setting as `SecRuleEngine`.

- [Common Runtime configuration](../common/common-connector-configuration.md) covers only the `key=value` runtime file and is not presented as an unregistered host directive.
- [ModSecurity Engine directives](../common/modsecurity-directives.md) covers `Sec*` directives in the loaded rule file.
- [Rule examples](../common/rule-examples.md) explains DetectionOnly and engine Off.

## Common Runtime relevance

| Key | Local use | Detailed reference |
| --- | --- | --- |
| `enabled` | Selected runtime profile key | [enabled](../common/common-connector-configuration.md#enabled) |
| `use_error_log` | Selected runtime profile key | [use_error_log](../common/common-connector-configuration.md#use-error-log) |
| `rules_inline` | Selected runtime profile key | [rules_inline](../common/common-connector-configuration.md#rules-inline) |
| `rules_file` | Selected runtime profile key | [rules_file](../common/common-connector-configuration.md#rules-file) |
| `rules_remote_key` | Selected runtime profile key | [rules_remote_key](../common/common-connector-configuration.md#rules-remote-key) |
| `rules_remote_url` | Selected runtime profile key | [rules_remote_url](../common/common-connector-configuration.md#rules-remote-url) |
| `transaction_id` | Selected runtime profile key | [transaction_id](../common/common-connector-configuration.md#transaction-id) |
| `transaction_id_header` | Selected runtime profile key | [transaction_id_header](../common/common-connector-configuration.md#transaction-id-header) |
| `phase4_mode` | Selected runtime profile key | [phase4_mode](../common/common-connector-configuration.md#phase4-mode) |
| `phase4_content_types_file` | Selected runtime profile key | [phase4_content_types_file](../common/common-connector-configuration.md#phase4-content-types-file) |
| `event_path` | Selected runtime profile key | [event_path](../common/common-connector-configuration.md#event-path) |
| `phase4_event_log` | Selected runtime profile key | [phase4_event_log](../common/common-connector-configuration.md#phase4-event-log) |
| `request_body_mode` | Selected runtime profile key | [request_body_mode](../common/common-connector-configuration.md#request-body-mode) |
| `response_body_mode` | Selected runtime profile key | [response_body_mode](../common/common-connector-configuration.md#response-body-mode) |
| `request_body_limit` | Selected runtime profile key | [request_body_limit](../common/common-connector-configuration.md#request-body-limit) |
| `response_body_limit` | Selected runtime profile key | [response_body_limit](../common/common-connector-configuration.md#response-body-limit) |
| `body_limit_action` | Selected runtime profile key | [body_limit_action](../common/common-connector-configuration.md#body-limit-action) |
| `late_intervention_timeout` | Selected runtime profile key | [late_intervention_timeout](../common/common-connector-configuration.md#late-intervention-timeout) |
| `default_block_status` | Selected runtime profile key | [default_block_status](../common/common-connector-configuration.md#default-block-status) |
| `default_error_status` | Selected runtime profile key | [default_error_status](../common/common-connector-configuration.md#default-error-status) |
| `max_header_count` | Selected runtime profile key | [max_header_count](../common/common-connector-configuration.md#max-header-count) |
| `max_header_name_size` | Selected runtime profile key | [max_header_name_size](../common/common-connector-configuration.md#max-header-name-size) |
| `max_header_value_size` | Selected runtime profile key | [max_header_value_size](../common/common-connector-configuration.md#max-header-value-size) |
| `max_total_header_bytes` | Selected runtime profile key | [max_total_header_bytes](../common/common-connector-configuration.md#max-total-header-bytes) |
| `max_event_json_bytes` | Selected runtime profile key | [max_event_json_bytes](../common/common-connector-configuration.md#max-event-json-bytes) |

## Engine directives used by profiles

The local rule profiles use `SecRuleEngine` for On, DetectionOnly, and Off. Where body inspection is selected, `SecRequestBodyAccess`, `SecResponseBodyAccess`, MIME scope, limits, and `SecRule` remain ModSecurity Engine directives.

See [Engine reference](../common/modsecurity-directives.md).

## Profiles

| Profile | File | Status |
| --- | --- | --- |
| Minimal | [minimal/lighttpd.conf](minimal/lighttpd.conf) | Active starter configuration |
| Safe full lifecycle | [safe/lighttpd-http1-identity.conf](safe/lighttpd-http1-identity.conf) | Selected bounded reference |
| Strict | [strict/README.md](strict/README.md) | Parser-supported or explicitly optional boundary |
| DetectionOnly | [detection-only/msconnector-runtime.conf](detection-only/msconnector-runtime.conf) | Engine evaluates/logs without disruptive action |
| Disabled | [disabled/lighttpd.conf](disabled/lighttpd.conf) | Connector or engine path disabled |

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
lighttpd -tt -f <config>
```

Repository targets: `make check-config-lighttpd` and `make check-config-all-connectors`.

## Option details

## `msconnector.config-file`

### Short description

Path to the Common Runtime configuration used by the native plugin.

### Syntax

```text
msconnector.config-file = "<runtime-key-value-file>"
```

### Valid contexts

- T_CONFIG_SCOPE_SERVER

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| path | non-empty readable Common Runtime key=value file | yes |

### Default

none

Source: `plugin config_file defaults to NULL`.

### Inheritance and merge

Only defaults are loaded; no documented conditional request-time override.

Merge: Plugin defaults retain the configured string.

### Phases and runtime effect

The referenced Common Runtime file chooses body modes and P1–P4 policy.

Loads and creates the connector-neutral runtime before requests are served.

### Validation and errors

Required only when msconnector.enabled is true; missing, unreadable, or invalid runtime configuration returns HANDLER_ERROR during startup.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/minimal/lighttpd.conf](../../examples/lighttpd/minimal/lighttpd.conf).

### Safety and operations

The runtime file contains executable rule paths and limits; use trusted ownership and permissions.

## `msconnector.enabled`

### Short description

Enables the native lighttpd plugin.

### Syntax

```text
msconnector.enabled = "enable" | "disable"
```

### Valid contexts

- T_CONFIG_SCOPE_SERVER

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| lighttpd boolean | lighttpd boolean values; examples use enable/disable | no |

### Default

off

Source: `ck_calloc plugin_data allocation and default config`.

### Inheritance and merge

Only defaults are loaded; the module has no request-time conditional patch path.

Merge: config_plugin_values_init populates defaults; no documented per-request merge.

### Phases and runtime effect

off disables the module P1/P3 callbacks and any patched P2/P4 callbacks.

Selects whether mod_msconnector initialises Common Runtime.

### Validation and errors

When enabled, lighttpd validates the runtime file during set-defaults; validate host syntax with lighttpd -tt -f <config>.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/minimal/lighttpd.conf](../../examples/lighttpd/minimal/lighttpd.conf).

### Safety and operations

Disabling the module bypasses connector processing even if a rule file exists.

## `proxy.server`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
proxy.server <host-specific-value>
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

lighttpd -tt -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

## `server.bind`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
server.bind <host-specific-value>
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

lighttpd -tt -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

## `server.compat-module-load`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
server.compat-module-load <host-specific-value>
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

lighttpd -tt -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

## `server.document-root`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
server.document-root <host-specific-value>
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

lighttpd -tt -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

## `server.errorlog`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
server.errorlog <host-specific-value>
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

lighttpd -tt -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

## `server.modules`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
server.modules <host-specific-value>
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

lighttpd -tt -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

## `server.pid-file`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
server.pid-file <host-specific-value>
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

lighttpd -tt -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

## `server.port`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
server.port <host-specific-value>
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

lighttpd -tt -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

## `server.stream-response-body`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
server.stream-response-body <host-specific-value>
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

lighttpd -tt -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

## `server.upload-dirs`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
server.upload-dirs <host-specific-value>
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

lighttpd -tt -f <config>

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/lighttpd-http1-identity.conf](../../examples/lighttpd/safe/lighttpd-http1-identity.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

## `compatibility.accesslog.filename`

### Short description

Compatibility-only lighttpd host field.

### Syntax

```text
accesslog.filename = <value>
```

### Valid contexts

- lighttpd sidecar compatibility configuration

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| lighttpd compatibility host field | explicit compatibility example value | no |

### Default

not part of native mod_msconnector

Source: `compatibility example`.

### Inheritance and merge

Host-defined compatibility behavior; not native plugin inheritance.

Merge: Host-defined compatibility behavior; not part of mod_msconnector.

### Phases and runtime effect

No native connector lifecycle claim.

Configures the retained sidecar compatibility example.

### Validation and errors

Validate as ordinary lighttpd proxy configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Safety and operations

Compatibility-only host routing; do not represent it as native ModSecurity configuration.

## `compatibility.proxy.server`

### Short description

Compatibility-only lighttpd host field.

### Syntax

```text
proxy.server = <value>
```

### Valid contexts

- lighttpd sidecar compatibility configuration

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| lighttpd compatibility host field | explicit compatibility example value | no |

### Default

not part of native mod_msconnector

Source: `compatibility example`.

### Inheritance and merge

Host-defined compatibility behavior; not native plugin inheritance.

Merge: Host-defined compatibility behavior; not part of mod_msconnector.

### Phases and runtime effect

No native connector lifecycle claim.

Configures the retained sidecar compatibility example.

### Validation and errors

Validate as ordinary lighttpd proxy configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Safety and operations

Compatibility-only host routing; do not represent it as native ModSecurity configuration.

## `compatibility.server.document-root`

### Short description

Compatibility-only lighttpd host field.

### Syntax

```text
server.document-root = <value>
```

### Valid contexts

- lighttpd sidecar compatibility configuration

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| lighttpd compatibility host field | explicit compatibility example value | no |

### Default

not part of native mod_msconnector

Source: `compatibility example`.

### Inheritance and merge

Host-defined compatibility behavior; not native plugin inheritance.

Merge: Host-defined compatibility behavior; not part of mod_msconnector.

### Phases and runtime effect

No native connector lifecycle claim.

Configures the retained sidecar compatibility example.

### Validation and errors

Validate as ordinary lighttpd proxy configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Safety and operations

Compatibility-only host routing; do not represent it as native ModSecurity configuration.

## `compatibility.server.errorlog`

### Short description

Compatibility-only lighttpd host field.

### Syntax

```text
server.errorlog = <value>
```

### Valid contexts

- lighttpd sidecar compatibility configuration

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| lighttpd compatibility host field | explicit compatibility example value | no |

### Default

not part of native mod_msconnector

Source: `compatibility example`.

### Inheritance and merge

Host-defined compatibility behavior; not native plugin inheritance.

Merge: Host-defined compatibility behavior; not part of mod_msconnector.

### Phases and runtime effect

No native connector lifecycle claim.

Configures the retained sidecar compatibility example.

### Validation and errors

Validate as ordinary lighttpd proxy configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Safety and operations

Compatibility-only host routing; do not represent it as native ModSecurity configuration.

## `compatibility.server.modules`

### Short description

Compatibility-only lighttpd host field.

### Syntax

```text
server.modules = <value>
```

### Valid contexts

- lighttpd sidecar compatibility configuration

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| lighttpd compatibility host field | explicit compatibility example value | no |

### Default

not part of native mod_msconnector

Source: `compatibility example`.

### Inheritance and merge

Host-defined compatibility behavior; not native plugin inheritance.

Merge: Host-defined compatibility behavior; not part of mod_msconnector.

### Phases and runtime effect

No native connector lifecycle claim.

Configures the retained sidecar compatibility example.

### Validation and errors

Validate as ordinary lighttpd proxy configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Safety and operations

Compatibility-only host routing; do not represent it as native ModSecurity configuration.

## `compatibility.server.port`

### Short description

Compatibility-only lighttpd host field.

### Syntax

```text
server.port = <value>
```

### Valid contexts

- lighttpd sidecar compatibility configuration

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| lighttpd compatibility host field | explicit compatibility example value | no |

### Default

not part of native mod_msconnector

Source: `compatibility example`.

### Inheritance and merge

Host-defined compatibility behavior; not native plugin inheritance.

Merge: Host-defined compatibility behavior; not part of mod_msconnector.

### Phases and runtime effect

No native connector lifecycle claim.

Configures the retained sidecar compatibility example.

### Validation and errors

Validate as ordinary lighttpd proxy configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Safety and operations

Compatibility-only host routing; do not represent it as native ModSecurity configuration.

## `sidecar proxy`

### Short description

Compatibility-only sidecar proxy setup.

### Syntax

```text
proxy.server = (...)
```

### Valid contexts

- Compatibility example

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| compatibility host setup | ordinary lighttpd proxy fields | no |

### Default

not a native connector option

Source: `compatibility example`.

### Inheritance and merge

not applicable to native plugin

Merge: not part of mod_msconnector

### Phases and runtime effect

No native mod_msconnector lifecycle claim.

Compatibility-only proxy routing.

### Validation and errors

Validate as ordinary lighttpd proxy configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf](../../examples/lighttpd/compatibility-sidecar/lighttpd-sidecar-proxy.conf).

### Safety and operations

Do not treat a proxy endpoint as a configured native ModSecurity integration.
