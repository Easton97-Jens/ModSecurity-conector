# NGINX configuration reference

**Language:** English | [Deutsch](configuration-reference.de.md)

## Scope and source of truth

Selected integration mode: `native-nginx-http-module`. This file is generated from registered parsers, configuration structures, checked service contracts, and active examples.
Compatibility entries are explicitly labelled and are not part of the selected core path.

## Configuration inventory

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`access_log`](#access-log) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`error_log`](#error-log) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`gzip`](#gzip) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`listen`](#listen) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`load_module`](#load-module) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`modsecurity`](#modsecurity) | Host / Connector | boolean | no | off | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Gates connector transaction creation; it is not SecRuleEngine. |
| [`modsecurity_phase4_body_limit`](#modsecurity-phase4-body-limit) | Host / Connector | positive decimal byte count | no | 1048576 | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Bounds response bytes offered to P4 processing by the native connector. |
| [`modsecurity_phase4_content_types_file`](#modsecurity-phase4-content-types-file) | Host / Connector | path | no | host defaults when omitted | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Loads the MIME-token allowlist from a bounded POSIX regular file to scope P4 response-body inspection. |
| [`modsecurity_phase4_log`](#modsecurity-phase4-log) | Host / Connector | registered but always rejected path | no | no usable value | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Rejects native NGINX event-file logging before descriptor creation because the host file registry cannot provide the Common Runtime security contract. |
| [`modsecurity_phase4_mode`](#modsecurity-phase4-mode) | Host / Connector | enum | no | safe | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Before response headers/body are committed, minimal, safe, and strict all resolve a P4 intervention as deny_if_possible, so NGINX can still return the requested engine status (or 403 fallback). Once headers are committed or the body started, minimal and safe both use the common log_only action; they record the late decision without a later status rewrite. Strict instead resolves to abort_connection: the native body filter marks the connection as errored, records connection_aborted, and returns NGX_ERROR. The known host boundary is that NGINX invokes the P4 engine finish only at last_buf/last_in_chain after bounded in-scope body accumulation, so a response may already be visible. Strict can therefore terminate a connection, but cannot guarantee a later 403 or replace an already-sent status line. |
| [`modsecurity_rules`](#modsecurity-rules) | Host / Connector | string | no | none; optional | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Loads inline content through libmodsecurity during configuration loading. |
| [`modsecurity_rules_file`](#modsecurity-rules-file) | Host / Connector | path | no | none; optional | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | During NGINX configuration loading, ngx_conf_set_rules_file passes the supplied path to libmodsecurity's msc_rules_add_file. The NGINX setter neither canonicalizes nor requires an absolute path; use an absolute path to avoid a process-working-directory dependency. A missing, unreadable, or invalid top-level rule file returns the libmodsecurity loader error and fails the configuration check/reload. Include and IncludeOptional inside that file are then interpreted by libmodsecurity, not expanded by the NGINX parser. Unlike modsecurity_rules, which sends one inline configuration string to msc_rules_add, this directive sends a file path to msc_rules_add_file; both contribute to the configured rule set and its normal parent/child merge. |
| [`modsecurity_rules_remote`](#modsecurity-rules-remote) | Host / Connector | registered but always rejected directive | no | no usable value | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Policy A rejects remote-rule configuration before a rule loader or network operation. |
| [`modsecurity_transaction_id`](#modsecurity-transaction-id) | Host / Connector | string/expression | no | none; connector creates a fallback identifier | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Supplies the engine and event correlation identifier for a transaction. |
| [`modsecurity_use_error_log`](#modsecurity-use-error-log) | Host / Connector | boolean | no | on | NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location) | Controls forwarding of libmodsecurity messages to the host error log; it does not switch rule evaluation. |
| [`proxy_pass`](#proxy-pass) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`server`](#server) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`server_name`](#server-name) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |

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
| Minimal | [minimal/nginx.conf](minimal/nginx.conf) | Active starter configuration |
| Safe full lifecycle | [safe/nginx.conf](safe/nginx.conf) | Selected bounded reference |
| Strict | [strict/nginx.conf](strict/nginx.conf) | Parser-supported or explicitly optional boundary |
| DetectionOnly | [detection-only/nginx.conf](detection-only/nginx.conf) | Engine evaluates/logs without disruptive action |
| Disabled | [disabled/nginx.conf](disabled/nginx.conf) | Connector or engine path disabled |

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
nginx -t
```

Repository targets: `make check-config-nginx` and `make check-config-all-connectors`.

## Option details

<a id="access-log"></a>
## `access_log`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
access_log <host-specific-value>
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

nginx -t

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="error-log"></a>
## `error_log`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
error_log <host-specific-value>
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

nginx -t

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="gzip"></a>
## `gzip`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
gzip <host-specific-value>
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

nginx -t

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="listen"></a>
## `listen`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
listen <host-specific-value>
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

nginx -t

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="load-module"></a>
## `load_module`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
load_module <host-specific-value>
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

nginx -t

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="modsecurity"></a>
## `modsecurity`

### Short description

Gates connector transaction creation; it is not SecRuleEngine.

### Syntax

```text
modsecurity on | off;
```

### Valid contexts

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| boolean | on \| off (the shared parser additionally accepts true/false/1/0/yes/no where the host passes it through) | no |

### Default

off

Source: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_ENABLE`.

### Inheritance and merge

http → server → location; a child inherits if it does not set a value.

Merge: ngx_conf_merge_* combines scalar/pointer configuration, while msc_rules_merge combines parent and child rules.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

Gates connector transaction creation; it is not SecRuleEngine.

### Validation and errors

ngx_conf_set_common_flag_slot rejects invalid values during nginx -t; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_FLAG is the registered context mask.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/minimal/nginx.conf](../../examples/nginx/minimal/nginx.conf).

### Safety and operations

off bypasses connector P1–P4 processing even if a rule file is configured.

<a id="modsecurity-phase4-body-limit"></a>
## `modsecurity_phase4_body_limit`

### Short description

Bounds response bytes offered to P4 processing by the native connector.

### Syntax

```text
modsecurity_phase4_body_limit <positive-bytes>;
```

### Valid contexts

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| positive decimal byte count | positive integer | no |

### Default

1048576

Source: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_BODY_LIMIT`.

### Inheritance and merge

http → server → location; a child inherits if it does not set a value.

Merge: ngx_conf_merge_* combines scalar/pointer configuration, while msc_rules_merge combines parent and child rules.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

Bounds response bytes offered to P4 processing by the native connector.

### Validation and errors

ngx_conf_set_phase4_body_limit rejects invalid values during nginx -t; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_TAKE1 is the registered context mask.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

A larger limit raises memory/CPU exposure; zero is invalid in the native setters.

<a id="modsecurity-phase4-content-types-file"></a>
## `modsecurity_phase4_content_types_file`

### Short description

Loads the MIME-token allowlist from a bounded POSIX regular file to scope P4 response-body inspection.

### Syntax

```text
modsecurity_phase4_content_types_file <value>;
```

### Valid contexts

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| path | on POSIX, one readable regular MIME-token file no larger than 64 KiB; rejected on Win32 | no |

### Default

host defaults when omitted

Source: `connector-specific default content-type loader`.

### Inheritance and merge

http → server → location; a child inherits if it does not set a value.

Merge: ngx_conf_merge_* combines scalar/pointer configuration, while msc_rules_merge combines parent and child rules.

### Phases and runtime effect

P4 only. The MIME-token allowlist determines which response bodies enter the bounded native P4 path.

Loads the MIME-token allowlist from a bounded POSIX regular file to scope P4 response-body inspection.

### Validation and errors

ngx_conf_set_phase4_content_types_file rejects invalid values during nginx -t. On POSIX it opens the path nonblocking, checks that the opened descriptor is regular, caps it at 64 KiB, requires an exact read, and rejects invalid MIME tokens. On Win32 it fails closed.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

Use an atomically replaced regular configuration file in a trusted directory. FIFOs, devices, sockets, directories, oversized files, partial reads, and invalid MIME tokens are rejected.

<a id="modsecurity-phase4-log"></a>
## `modsecurity_phase4_log`

### Short description

Rejects native NGINX event-file logging before descriptor creation because the host file registry cannot provide the Common Runtime security contract.

### Syntax

```text
modsecurity_phase4_log <value>;
```

### Valid contexts

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| registered but always rejected path | no path is accepted | no |

### Default

no usable value

Source: `security policy: native NGINX event-file logging disabled`.

### Inheritance and merge

No event-file value can be inherited or merged because every use is rejected.

Merge: No event-file value can be merged because every use is rejected before descriptor creation.

### Phases and runtime effect

No event-file sink is reachable through this directive. The Common Runtime event lifecycle remains the supported secure event path.

Rejects native NGINX event-file logging before descriptor creation because the host file registry cannot provide the Common Runtime security contract.

### Validation and errors

ngx_conf_set_phase4_log rejects every path during nginx -t with the native event-file security-policy error.

### Example

There is no accepted example: every configured value is rejected by security policy.

Source-backed example: `connectors/nginx/src/ngx_http_modsecurity_module.c`.

### Safety and operations

Do not re-enable this native host writer without a no-follow, regular-file, owner, and private-mode descriptor contract. Use the Common Runtime event lifecycle instead.

<a id="modsecurity-phase4-mode"></a>
## `modsecurity_phase4_mode`

### Short description

Before response headers/body are committed, minimal, safe, and strict all resolve a P4 intervention as deny_if_possible, so NGINX can still return the requested engine status (or 403 fallback). Once headers are committed or the body started, minimal and safe both use the common log_only action; they record the late decision without a later status rewrite. Strict instead resolves to abort_connection: the native body filter marks the connection as errored, records connection_aborted, and returns NGX_ERROR. The known host boundary is that NGINX invokes the P4 engine finish only at last_buf/last_in_chain after bounded in-scope body accumulation, so a response may already be visible. Strict can therefore terminate a connection, but cannot guarantee a later 403 or replace an already-sent status line.

### Syntax

```text
modsecurity_phase4_mode minimal | safe | strict;
```

### Valid contexts

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| enum | minimal \| safe \| strict; before commit all use deny_if_possible, after commit minimal/safe are log_only and strict is abort_connection | no |

### Default

safe

Source: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE`.

### Inheritance and merge

http → server → location; a child inherits if it does not set a value.

Merge: ngx_conf_merge_* combines scalar/pointer configuration, while msc_rules_merge combines parent and child rules.

### Phases and runtime effect

P4 only. The response-body filter accumulates bounded in-scope bytes and finishes the engine at EOS (last_buf/last_in_chain); header/body commitment determines whether a status or only a late transport action remains possible.

Before response headers/body are committed, minimal, safe, and strict all resolve a P4 intervention as deny_if_possible, so NGINX can still return the requested engine status (or 403 fallback). Once headers are committed or the body started, minimal and safe both use the common log_only action; they record the late decision without a later status rewrite. Strict instead resolves to abort_connection: the native body filter marks the connection as errored, records connection_aborted, and returns NGX_ERROR. The known host boundary is that NGINX invokes the P4 engine finish only at last_buf/last_in_chain after bounded in-scope body accumulation, so a response may already be visible. Strict can therefore terminate a connection, but cannot guarantee a later 403 or replace an already-sent status line.

### Validation and errors

ngx_conf_set_phase4_mode accepts only minimal|safe|strict during nginx -t. Runtime late behavior is source-defined: non-strict post-commit paths emit log_only; strict marks the connection errored and returns NGX_ERROR, without manufacturing a later 403.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

safe/minimal retain late-decision evidence without interrupting an already-started response. strict requests a connection abort after commit, which can expose clients to a partial response; it is not a reliable post-commit HTTP-status enforcement mode.

<a id="modsecurity-rules"></a>
## `modsecurity_rules`

### Short description

Loads inline content through libmodsecurity during configuration loading.

### Syntax

```text
modsecurity_rules <value>;
```

### Valid contexts

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string | one inline ModSecurity rule/configuration string | no |

### Default

none; optional

Source: `parser registration has no default`.

### Inheritance and merge

http → server → location; a child inherits if it does not set a value.

Merge: ngx_conf_merge_* combines scalar/pointer configuration, while msc_rules_merge combines parent and child rules.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

Loads inline content through libmodsecurity during configuration loading.

### Validation and errors

ngx_conf_set_rules rejects invalid values during nginx -t; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_TAKE1 is the registered context mask.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

Inline rules are executable policy; restrict who may alter host configuration.

<a id="modsecurity-rules-file"></a>
## `modsecurity_rules_file`

### Short description

During NGINX configuration loading, ngx_conf_set_rules_file passes the supplied path to libmodsecurity's msc_rules_add_file. The NGINX setter neither canonicalizes nor requires an absolute path; use an absolute path to avoid a process-working-directory dependency. A missing, unreadable, or invalid top-level rule file returns the libmodsecurity loader error and fails the configuration check/reload. Include and IncludeOptional inside that file are then interpreted by libmodsecurity, not expanded by the NGINX parser. Unlike modsecurity_rules, which sends one inline configuration string to msc_rules_add, this directive sends a file path to msc_rules_add_file; both contribute to the configured rule set and its normal parent/child merge.

### Syntax

```text
modsecurity_rules_file <value>;
```

### Valid contexts

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| path | one readable libmodsecurity configuration/rules path; absolute paths are recommended, while relative-path resolution is delegated to libmodsecurity | no |

### Default

none; optional

Source: `parser registration has no default`.

### Inheritance and merge

http → server → location; a child inherits if it does not set a value.

Merge: ngx_conf_merge_* combines scalar/pointer configuration, while msc_rules_merge combines parent and child rules.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

During NGINX configuration loading, ngx_conf_set_rules_file passes the supplied path to libmodsecurity's msc_rules_add_file. The NGINX setter neither canonicalizes nor requires an absolute path; use an absolute path to avoid a process-working-directory dependency. A missing, unreadable, or invalid top-level rule file returns the libmodsecurity loader error and fails the configuration check/reload. Include and IncludeOptional inside that file are then interpreted by libmodsecurity, not expanded by the NGINX parser. Unlike modsecurity_rules, which sends one inline configuration string to msc_rules_add, this directive sends a file path to msc_rules_add_file; both contribute to the configured rule set and its normal parent/child merge.

### Validation and errors

ngx_conf_set_rules_file calls msc_rules_add_file while nginx -t/configuration loading runs. A missing, unreadable, or syntactically invalid top-level rule file (including an engine Include failure) returns the loader error and rejects the NGINX configuration.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/minimal/nginx.conf](../../examples/nginx/minimal/nginx.conf).

### Safety and operations

Keep the file, its parent directories, and any engine-included files non-writable by untrusted identities. Prefer an absolute path so a changed working directory cannot select unintended policy.

<a id="modsecurity-rules-remote"></a>
## `modsecurity_rules_remote`

### Short description

Policy A rejects remote-rule configuration before a rule loader or network operation.

### Syntax

```text
modsecurity_rules_remote <key> <url>;
```

### Valid contexts

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| registered but always rejected directive | no key/URL pair is accepted | no |

### Default

no usable value

Source: `security policy: remote rule loading disabled`.

### Inheritance and merge

No remote value can be inherited or merged because every use is rejected.

Merge: No remote value can be merged because every use is rejected before rule loading.

### Phases and runtime effect

No rule-loader or network path is reachable through this directive.

Policy A rejects remote-rule configuration before a rule loader or network operation.

### Validation and errors

ngx_conf_set_rules_remote rejects every key/URL pair during nginx -t before a rule loader or network operation.

### Example

There is no accepted example: every configured value is rejected by security policy.

Source-backed example: `connectors/nginx/src/ngx_http_modsecurity_module.c`.

### Safety and operations

Remote loading is technically disabled for every connector; do not rely on a remote URL or key.

<a id="modsecurity-transaction-id"></a>
## `modsecurity_transaction_id`

### Short description

Supplies the engine and event correlation identifier for a transaction.

### Syntax

```text
modsecurity_transaction_id <value>;
```

### Valid contexts

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/expression | non-empty host-specific transaction identifier | no |

### Default

none; connector creates a fallback identifier

Source: `connector transaction creation path`.

### Inheritance and merge

http → server → location; a child inherits if it does not set a value.

Merge: ngx_conf_merge_* combines scalar/pointer configuration, while msc_rules_merge combines parent and child rules.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

Supplies the engine and event correlation identifier for a transaction.

### Validation and errors

ngx_conf_set_transaction_id rejects invalid values during nginx -t; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_TAKE1 is the registered context mask.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

Do not put credentials or sensitive request data in a correlation identifier.

<a id="modsecurity-use-error-log"></a>
## `modsecurity_use_error_log`

### Short description

Controls forwarding of libmodsecurity messages to the host error log; it does not switch rule evaluation.

### Syntax

```text
modsecurity_use_error_log on | off;
```

### Valid contexts

- NGX_HTTP_MAIN_CONF (http), NGX_HTTP_SRV_CONF (server), NGX_HTTP_LOC_CONF (location)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| boolean | on \| off | no |

### Default

on

Source: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_USE_ERROR_LOG`.

### Inheritance and merge

http → server → location; a child inherits if it does not set a value.

Merge: ngx_conf_merge_* combines scalar/pointer configuration, while msc_rules_merge combines parent and child rules.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

Controls forwarding of libmodsecurity messages to the host error log; it does not switch rule evaluation.

### Validation and errors

ngx_conf_set_common_flag_slot rejects invalid values during nginx -t; NGX_HTTP_LOC_CONF|NGX_HTTP_SRV_CONF|NGX_HTTP_MAIN_CONF|NGX_CONF_FLAG is the registered context mask.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

Error logs can contain security metadata; protect and rotate them.

<a id="proxy-pass"></a>
## `proxy_pass`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
proxy_pass <host-specific-value>
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

nginx -t

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

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

nginx -t

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="server-name"></a>
## `server_name`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
server_name <host-specific-value>
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

nginx -t

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/nginx/safe/nginx.conf](../../examples/nginx/safe/nginx.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.
