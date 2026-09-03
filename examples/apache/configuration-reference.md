# Apache configuration reference

**Language:** English | [Deutsch](configuration-reference.de.md)

## Scope and source of truth

Selected integration mode: `native-httpd-module`. This file is generated from registered parsers, configuration structures, checked service contracts, and active examples.
Compatibility entries are explicitly labelled and are not part of the selected core path.

## Configuration inventory

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`CustomLog`](#customlog) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`ErrorLog`](#errorlog) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`LoadModule`](#loadmodule) | Host | host-owned configuration field | no | No connector default; this host field is explicit in the example. | The context shown in the checked-in example; consult the pinned host documentation for all host-specific contexts. | Host-owned setting appearing in the checked-in example; it is not a connector directive. |
| [`modsecurity`](#modsecurity) | Host / Connector | boolean | no | off | Apache RSRC_CONF \| ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules) | Gates connector transaction creation; it is not SecRuleEngine. |
| [`modsecurity_phase4_body_limit`](#modsecurity-phase4-body-limit) | Host / Connector | positive decimal byte count | no | 1048576 | Apache RSRC_CONF \| ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules) | Bounds Apache response bytes offered to P4 across current normalized brigades. The configurable default is 1048576 bytes; independently, a fixed non-configurable 4096-normalized-bucket ceiling spans filter calls. A limit breach fails closed before the current offending bucket is forwarded; already committed output is not rewritten. |
| [`modsecurity_phase4_content_types_file`](#modsecurity-phase4-content-types-file) | Host / Connector | deprecated path | no | none; deprecated Apache compatibility input | Apache RSRC_CONF \| ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules) | Deprecated Apache compatibility parser for a legacy MIME list. It does not narrow the universal P4 inspection path; use SecResponseBodyMimeType to select libModSecurity inspection. |
| [`modsecurity_phase4_log`](#modsecurity-phase4-log) | Host / Connector | path | no | none | Apache RSRC_CONF \| ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules) | Sets a connector event path; current Apache and NGINX paths also use it for earlier rule/intervention metadata, not only P4. |
| [`modsecurity_phase4_mode`](#modsecurity-phase4-mode) | Host / Connector | enum | no | safe | Apache RSRC_CONF \| ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules) | Apache appends each normalized response bucket exactly once and forwards non-terminal output to the next filter without waiting for EOS. It finishes P4 exactly once at actual EOS. After the next-filter commitment boundary, minimal/safe record log_only and strict requests abort_connection instead of a late status rewrite. |
| [`modsecurity_rules`](#modsecurity-rules) | Host / Connector | string | no | none; optional | Apache RSRC_CONF \| ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules) | Loads inline content through libmodsecurity during configuration loading. |
| [`modsecurity_rules_file`](#modsecurity-rules-file) | Host / Connector | path | no | none; optional | Apache RSRC_CONF \| ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules) | Loads a local rule file through libmodsecurity during configuration loading. |
| [`modsecurity_rules_remote`](#modsecurity-rules-remote) | Host / Connector | registered but always rejected directive | no | no usable value | Apache RSRC_CONF \| ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules) | Policy A rejects remote-rule configuration before a rule loader or network operation. |
| [`modsecurity_transaction_id`](#modsecurity-transaction-id) | Host / Connector | string/expression | no | none; connector creates a fallback identifier | Apache RSRC_CONF \| ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules) | Supplies the engine and event correlation identifier for a transaction. |
| [`modsecurity_transaction_id_expr`](#modsecurity-transaction-id-expr) | Host / Connector | Apache string expression | no | none | Apache RSRC_CONF \| ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules) | Evaluates an Apache expression per request for the transaction identifier. |
| [`modsecurity_use_error_log`](#modsecurity-use-error-log) | Host / Connector | boolean | no | on | Apache RSRC_CONF \| ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules) | Controls forwarding of libmodsecurity messages to the host error log; it does not switch rule evaluation. |

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
| Minimal | [minimal/httpd.conf](minimal/httpd.conf) | Active starter configuration |
| Safe full lifecycle | [safe/httpd.conf](safe/httpd.conf) | Selected bounded reference |
| Strict | [strict/httpd.conf](strict/httpd.conf) | Parser-supported or explicitly optional boundary |
| DetectionOnly | [detection-only/httpd.conf](detection-only/httpd.conf) | Engine evaluates/logs without disruptive action |
| Disabled | [disabled/httpd.conf](disabled/httpd.conf) | Connector or engine path disabled |

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
apachectl -t
```

Repository targets: `make check-config-apache` and `make check-config-all-connectors`.

## Option details

<a id="customlog"></a>
## `CustomLog`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
CustomLog <host-specific-value>
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

apachectl -t

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="errorlog"></a>
## `ErrorLog`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
ErrorLog <host-specific-value>
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

apachectl -t

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="loadmodule"></a>
## `LoadModule`

### Short description

Host-owned setting appearing in the checked-in example; it is not a connector directive.

### Syntax

```text
LoadModule <host-specific-value>
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

apachectl -t

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Safety and operations

Network addresses, paths, and logging destinations must be selected and access-controlled by the operator.

<a id="modsecurity"></a>
## `modsecurity`

### Short description

Gates connector transaction creation; it is not SecRuleEngine.

### Syntax

```text
modsecurity On | Off
```

### Valid contexts

- Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| boolean | on \| off (the shared parser additionally accepts true/false/1/0/yes/no where the host passes it through) | no |

### Default

off

Source: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_ENABLE`.

### Inheritance and merge

Parent value is available to the child unless a child value is set; see the Apache directory-config merge function.

Merge: Common scalar values use child-over-parent merge; rule sets are merged through msc_rules_merge. Transaction-id expression/static-id are mutually exclusive.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

Gates connector transaction creation; it is not SecRuleEngine.

### Validation and errors

msc_config_modsec_state returns an Apache configuration error for its documented invalid input; validate the installed configuration with apachectl -t.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/minimal/httpd.conf](../../examples/apache/minimal/httpd.conf).

### Safety and operations

off bypasses connector P1–P4 processing even if a rule file is configured.

<a id="modsecurity-phase4-body-limit"></a>
## `modsecurity_phase4_body_limit`

### Short description

Bounds Apache response bytes offered to P4 across current normalized brigades. The configurable default is 1048576 bytes; independently, a fixed non-configurable 4096-normalized-bucket ceiling spans filter calls. A limit breach fails closed before the current offending bucket is forwarded; already committed output is not rewritten.

### Syntax

```text
modsecurity_phase4_body_limit <positive-bytes>
```

### Valid contexts

- Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| positive decimal byte count | positive integer | no |

### Default

1048576

Source: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_BODY_LIMIT`.

### Inheritance and merge

Parent value is available to the child unless a child value is set; see the Apache directory-config merge function.

Merge: Common scalar values use child-over-parent merge; rule sets are merged through msc_rules_merge. Transaction-id expression/static-id are mutually exclusive.

### Phases and runtime effect

P4 only. The byte limit and fixed bucket ceiling span filter calls. The adapter retains only the terminal EOS fragment for the one-shot finish; the bucket count resets on release or discard.

Bounds Apache response bytes offered to P4 across current normalized brigades. The configurable default is 1048576 bytes; independently, a fixed non-configurable 4096-normalized-bucket ceiling spans filter calls. A limit breach fails closed before the current offending bucket is forwarded; already committed output is not rewritten.

### Validation and errors

msc_config_phase4_body_limit returns an Apache configuration error for its documented invalid input; validate the installed configuration with apachectl -t.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Safety and operations

The byte and fixed bucket ceilings bound payload and per-transaction APR-object/setaside memory/CPU exposure. Each accepted current bucket is appended once before direct forwarding; do not retain a full response or forward an uninspected tail.

<a id="modsecurity-phase4-content-types-file"></a>
## `modsecurity_phase4_content_types_file`

### Short description

Deprecated Apache compatibility parser for a legacy MIME list. It does not narrow the universal P4 inspection path; use SecResponseBodyMimeType to select libModSecurity inspection.

### Syntax

```text
modsecurity_phase4_content_types_file <value>
```

### Valid contexts

- Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| deprecated path | one readable legacy file with MIME tokens | no |

### Default

none; deprecated Apache compatibility input

Source: `Apache compatibility parser; deprecated`.

### Inheritance and merge

Parent value is available to the child unless a child value is set; see the Apache directory-config merge function.

Merge: Common scalar values use child-over-parent merge; rule sets are merged through msc_rules_merge. Transaction-id expression/static-id are mutually exclusive.

### Phases and runtime effect

P4 only. The parser is retained for compatibility but cannot select which Apache responses bypass the bounded inspection path.

Deprecated Apache compatibility parser for a legacy MIME list. It does not narrow the universal P4 inspection path; use SecResponseBodyMimeType to select libModSecurity inspection.

### Validation and errors

msc_config_phase4_content_types_file returns an Apache configuration error for its documented invalid input; validate the installed configuration with apachectl -t.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: `connectors/apache/src/msc_config.c`.

### Safety and operations

Do not use this legacy list to permit an uninspected pass-through route. The connector cannot safely query libModSecurity's effective MIME selection, so every response passes through the bounded P4 path.

<a id="modsecurity-phase4-log"></a>
## `modsecurity_phase4_log`

### Short description

Sets a connector event path; current Apache and NGINX paths also use it for earlier rule/intervention metadata, not only P4.

### Syntax

```text
modsecurity_phase4_log <value>
```

### Valid contexts

- Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| path | one connector JSONL event/intervention-log path | no |

### Default

none

Source: `parser registration has no default`.

### Inheritance and merge

Parent value is available to the child unless a child value is set; see the Apache directory-config merge function.

Merge: Common scalar values use child-over-parent merge; rule sets are merged through msc_rules_merge. Transaction-id expression/static-id are mutually exclusive.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

Sets a connector event path; current Apache and NGINX paths also use it for earlier rule/intervention metadata, not only P4.

### Validation and errors

msc_config_phase4_log returns an Apache configuration error for its documented invalid input; validate the installed configuration with apachectl -t.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Safety and operations

Treat JSONL metadata as sensitive operational data and set safe ownership/rotation.

<a id="modsecurity-phase4-mode"></a>
## `modsecurity_phase4_mode`

### Short description

Apache appends each normalized response bucket exactly once and forwards non-terminal output to the next filter without waiting for EOS. It finishes P4 exactly once at actual EOS. After the next-filter commitment boundary, minimal/safe record log_only and strict requests abort_connection instead of a late status rewrite.

### Syntax

```text
modsecurity_phase4_mode minimal | safe | strict
```

### Valid contexts

- Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| enum | minimal \| safe \| strict | no |

### Default

safe

Source: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE`.

### Inheritance and merge

Parent value is available to the child unless a child value is set; see the Apache directory-config merge function.

Merge: Common scalar values use child-over-parent merge; rule sets are merged through msc_rules_merge. Transaction-id expression/static-id are mutually exclusive.

### Phases and runtime effect

P4 only. Apache commits at the next-filter boundary before it forwards a current non-terminal brigade; this setting controls the canonical pre- and post-commit decision mapping.

Apache appends each normalized response bucket exactly once and forwards non-terminal output to the next filter without waiting for EOS. It finishes P4 exactly once at actual EOS. After the next-filter commitment boundary, minimal/safe record log_only and strict requests abort_connection instead of a late status rewrite.

### Validation and errors

msc_config_phase4_mode returns an Apache configuration error for its documented invalid input; validate the installed configuration with apachectl -t.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Safety and operations

Already forwarded response bytes cannot be rewritten. Safe records a post-commit disruptive decision as log_only; strict requests the configured host abort action rather than synthesizing a later 403.

<a id="modsecurity-rules"></a>
## `modsecurity_rules`

### Short description

Loads inline content through libmodsecurity during configuration loading.

### Syntax

```text
modsecurity_rules <value>
```

### Valid contexts

- Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string | one inline ModSecurity rule/configuration string | no |

### Default

none; optional

Source: `parser registration has no default`.

### Inheritance and merge

Parent value is available to the child unless a child value is set; see the Apache directory-config merge function.

Merge: Common scalar values use child-over-parent merge; rule sets are merged through msc_rules_merge. Transaction-id expression/static-id are mutually exclusive.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

Loads inline content through libmodsecurity during configuration loading.

### Validation and errors

msc_config_load_rules returns an Apache configuration error for its documented invalid input; validate the installed configuration with apachectl -t.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Safety and operations

Inline rules are executable policy; restrict who may alter host configuration.

<a id="modsecurity-rules-file"></a>
## `modsecurity_rules_file`

### Short description

Loads a local rule file through libmodsecurity during configuration loading.

### Syntax

```text
modsecurity_rules_file <value>
```

### Valid contexts

- Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| path | readable ModSecurity configuration/rules file path | no |

### Default

none; optional

Source: `parser registration has no default`.

### Inheritance and merge

Parent value is available to the child unless a child value is set; see the Apache directory-config merge function.

Merge: Common scalar values use child-over-parent merge; rule sets are merged through msc_rules_merge. Transaction-id expression/static-id are mutually exclusive.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

Loads a local rule file through libmodsecurity during configuration loading.

### Validation and errors

msc_config_load_rules_file returns an Apache configuration error for its documented invalid input; validate the installed configuration with apachectl -t.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/minimal/httpd.conf](../../examples/apache/minimal/httpd.conf).

### Safety and operations

Keep the file and parent directories non-writable by untrusted identities.

<a id="modsecurity-rules-remote"></a>
## `modsecurity_rules_remote`

### Short description

Policy A rejects remote-rule configuration before a rule loader or network operation.

### Syntax

```text
modsecurity_rules_remote <key> <url>
```

### Valid contexts

- Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)

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

msc_config_load_rules_remote rejects every key/URL pair during apachectl -t before a rule loader or network operation.

### Example

There is no accepted example: every configured value is rejected by security policy.

Source-backed example: `connectors/apache/src/msc_config.c`.

### Safety and operations

Remote loading is technically disabled for every connector; do not rely on a remote URL or key.

<a id="modsecurity-transaction-id"></a>
## `modsecurity_transaction_id`

### Short description

Supplies the engine and event correlation identifier for a transaction.

### Syntax

```text
modsecurity_transaction_id <value>
```

### Valid contexts

- Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string/expression | non-empty host-specific transaction identifier | no |

### Default

none; connector creates a fallback identifier

Source: `connector transaction creation path`.

### Inheritance and merge

Parent value is available to the child unless a child value is set; see the Apache directory-config merge function.

Merge: Common scalar values use child-over-parent merge; rule sets are merged through msc_rules_merge. Transaction-id expression/static-id are mutually exclusive.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

Supplies the engine and event correlation identifier for a transaction.

### Validation and errors

msc_config_transaction_id returns an Apache configuration error for its documented invalid input; validate the installed configuration with apachectl -t.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Safety and operations

Do not put credentials or sensitive request data in a correlation identifier.

<a id="modsecurity-transaction-id-expr"></a>
## `modsecurity_transaction_id_expr`

### Short description

Evaluates an Apache expression per request for the transaction identifier.

### Syntax

```text
modsecurity_transaction_id_expr <apache-string-expression>
```

### Valid contexts

- Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| Apache string expression | one non-empty Apache expression | no |

### Default

none

Source: `Apache parser registration has no default`.

### Inheritance and merge

Parent value is available to the child unless a child value is set; see the Apache directory-config merge function.

Merge: Common scalar values use child-over-parent merge; rule sets are merged through msc_rules_merge. Transaction-id expression/static-id are mutually exclusive.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

Evaluates an Apache expression per request for the transaction identifier.

### Validation and errors

msc_config_transaction_id_expr returns an Apache configuration error for its documented invalid input; validate the installed configuration with apachectl -t.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/safe/httpd.conf](../../examples/apache/safe/httpd.conf).

### Safety and operations

Treat expression inputs as metadata; avoid exposing secrets in logs.

<a id="modsecurity-use-error-log"></a>
## `modsecurity_use_error_log`

### Short description

Controls forwarding of libmodsecurity messages to the host error log; it does not switch rule evaluation.

### Syntax

```text
modsecurity_use_error_log <value>
```

### Valid contexts

- Apache RSRC_CONF | ACCESS_CONF (server/vhost and per-directory contexts supported by Apache's context rules)

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| boolean | on \| off | no |

### Default

on

Source: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_USE_ERROR_LOG`.

### Inheritance and merge

Parent value is available to the child unless a child value is set; see the Apache directory-config merge function.

Merge: Common scalar values use child-over-parent merge; rule sets are merged through msc_rules_merge. Transaction-id expression/static-id are mutually exclusive.

### Phases and runtime effect

P1 controls integration; rules and P4 controls affect the stated phase only.

Controls forwarding of libmodsecurity messages to the host error log; it does not switch rule evaluation.

### Validation and errors

msc_config_use_error_log returns an Apache configuration error for its documented invalid input; validate the installed configuration with apachectl -t.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/minimal/httpd.conf](../../examples/apache/minimal/httpd.conf).

### Safety and operations

Error logs can contain security metadata; protect and rotate them.
