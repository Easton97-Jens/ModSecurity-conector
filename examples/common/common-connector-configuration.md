# Common connector configuration

**Language:** English | [Deutsch](common-connector-configuration.de.md)

## Scope

This is the complete current `key=value` parser surface of `common/runtime/msconnector_runtime.c`. It is not a claim that every host exposes every key as a host directive.

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`body_limit_action`](#body-limit-action) | Common Runtime | enum | no | reject | Common Runtime key=value file | Controls whether an over-limit chunk is rejected or truncated before engine input. |
| [`default_block_status`](#default-block-status) | Common Runtime | HTTP status | no | 403 | Common Runtime key=value file | Fallback status for supported pre-commit block actions. |
| [`default_error_status`](#default-error-status) | Common Runtime | HTTP error status | no | 500 | Common Runtime key=value file | Fallback status for runtime errors. |
| [`enabled`](#enabled) | Common Runtime | boolean | no | off | Common Runtime key=value file | Enables the Common Runtime; enabled runtime requires an inline, file, or remote rule source. |
| [`event_path`](#event-path) | Common Runtime | path | no | none | Common Runtime key=value file | Appends metadata-only JSONL events when configured. |
| [`late_intervention_timeout`](#late-intervention-timeout) | Common Runtime | non-negative decimal milliseconds | no | 0 | Common Runtime key=value file | Stores an optional late-intervention budget; Common owns no timer/cancellation primitive. |
| [`max_event_json_bytes`](#max-event-json-bytes) | Common Runtime | positive decimal bytes | no | 16384 | Common Runtime key=value file | Bounds serialized metadata event size. |
| [`max_header_count`](#max-header-count) | Common Runtime | positive decimal count | no | 256 | Common Runtime key=value file | Bounds accepted header count. |
| [`max_header_name_size`](#max-header-name-size) | Common Runtime | positive decimal bytes | no | 256 | Common Runtime key=value file | Bounds each header-name size. |
| [`max_header_value_size`](#max-header-value-size) | Common Runtime | positive decimal bytes | no | 8192 | Common Runtime key=value file | Bounds each header-value size. |
| [`max_total_header_bytes`](#max-total-header-bytes) | Common Runtime | positive decimal bytes | no | 65536 | Common Runtime key=value file | Bounds total header bytes. |
| [`phase4_content_types_file`](#phase4-content-types-file) | Common Runtime | path | no | none | Common Runtime key=value file | Stores a content-type file path; consumption is connector-specific. |
| [`phase4_event_log`](#phase4-event-log) | Common Runtime | path alias | no | none | Common Runtime key=value file | Alias for event_path. |
| [`phase4_mode`](#phase4-mode) | Common Runtime | enum | no | safe | Common Runtime key=value file | Stores the late P4 policy. Common alone owns no host abort primitive. |
| [`request_body_limit`](#request-body-limit) | Common Runtime | positive decimal bytes | no | 1048576 | Common Runtime key=value file | Bounds request bytes offered to the engine. |
| [`request_body_mode`](#request-body-mode) | Common Runtime | enum | no | buffered | Common Runtime key=value file | Selects the Common request-body handling mode; a particular host may support only a subset. |
| [`response_body_limit`](#response-body-limit) | Common Runtime | positive decimal bytes | no | 1048576 | Common Runtime key=value file | Bounds response bytes offered to the engine. |
| [`response_body_mode`](#response-body-mode) | Common Runtime | enum | no | none | Common Runtime key=value file | Selects the Common response-body handling mode; a particular host may support only a subset. |
| [`rules_file`](#rules-file) | Common Runtime | path | no | none | Common Runtime key=value file | Loads rules from a local file. |
| [`rules_inline`](#rules-inline) | Common Runtime | string | no | none | Common Runtime key=value file | Adds inline rule configuration. |
| [`rules_remote_key`](#rules-remote-key) | Common Runtime | string | no | none | Common Runtime key=value file | Supplies one half of a remote-rule pair. |
| [`rules_remote_url`](#rules-remote-url) | Common Runtime | URL | no | none | Common Runtime key=value file | Supplies the remote-rule endpoint; the selected examples do not exercise it. |
| [`transaction_id`](#transaction-id) | Common Runtime | string | no | none | Common Runtime key=value file | Sets a static runtime transaction identifier. |
| [`transaction_id_header`](#transaction-id-header) | Common Runtime | header name | no | x-request-id | Common Runtime key=value file | Selects the fallback correlation-header name. |
| [`use_error_log`](#use-error-log) | Common Runtime | boolean | no | on | Common Runtime key=value file | Stores the Common logging preference. A connector must consume it before a host logging effect can be claimed. |

## Option details

## `body_limit_action`

### Short description

Controls whether an over-limit chunk is rejected or truncated before engine input.

### Syntax

```text
body_limit_action=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| enum | reject \| process_partial (accepted spelling variants are parser-specific) | no |

### Default

reject

Source: `common/src/config.c:msconnector_config_apply_defaults`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Controls whether an over-limit chunk is rejected or truncated before engine input.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Controls whether an over-limit chunk is rejected or truncated before engine input.

## `default_block_status`

### Short description

Fallback status for supported pre-commit block actions.

### Syntax

```text
default_block_status=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| HTTP status | allowed blocking status | no |

### Default

403

Source: `common/include/msconnector/block_statuses.h:MSCONNECTOR_DEFAULT_BLOCK_STATUS`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Fallback status for supported pre-commit block actions.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Fallback status for supported pre-commit block actions.

## `default_error_status`

### Short description

Fallback status for runtime errors.

### Syntax

```text
default_error_status=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| HTTP error status | valid HTTP error status | no |

### Default

500

Source: `common/include/msconnector/block_statuses.h:MSCONNECTOR_DEFAULT_ERROR_STATUS`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Fallback status for runtime errors.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Fallback status for runtime errors.

## `enabled`

### Short description

Enables the Common Runtime; enabled runtime requires an inline, file, or remote rule source.

### Syntax

```text
enabled=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| boolean | on \| off \| true \| false \| 1 \| 0 \| yes \| no | no |

### Default

off

Source: `common/src/config.c:msconnector_config_apply_defaults`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Enables the Common Runtime; enabled runtime requires an inline, file, or remote rule source.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Enables the Common Runtime; enabled runtime requires an inline, file, or remote rule source.

## `event_path`

### Short description

Appends metadata-only JSONL events when configured.

### Syntax

```text
event_path=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| path | path without a parent-directory segment | no |

### Default

none

Source: `runtime parser has no default`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Appends metadata-only JSONL events when configured.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Appends metadata-only JSONL events when configured.

## `late_intervention_timeout`

### Short description

Stores an optional late-intervention budget; Common owns no timer/cancellation primitive.

### Syntax

```text
late_intervention_timeout=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| non-negative decimal milliseconds | 0 or positive integer | no |

### Default

0

Source: `common/src/config.c:msconnector_config_apply_defaults`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Stores an optional late-intervention budget; Common owns no timer/cancellation primitive.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Stores an optional late-intervention budget; Common owns no timer/cancellation primitive.

## `max_event_json_bytes`

### Short description

Bounds serialized metadata event size.

### Syntax

```text
max_event_json_bytes=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| positive decimal bytes | positive integer | no |

### Default

16384

Source: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_EVENT_JSON_BYTES`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Bounds serialized metadata event size.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Bounds serialized metadata event size.

## `max_header_count`

### Short description

Bounds accepted header count.

### Syntax

```text
max_header_count=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| positive decimal count | positive integer | no |

### Default

256

Source: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_COUNT`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Bounds accepted header count.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Bounds accepted header count.

## `max_header_name_size`

### Short description

Bounds each header-name size.

### Syntax

```text
max_header_name_size=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| positive decimal bytes | positive integer | no |

### Default

256

Source: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_NAME_LENGTH`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Bounds each header-name size.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Bounds each header-name size.

## `max_header_value_size`

### Short description

Bounds each header-value size.

### Syntax

```text
max_header_value_size=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| positive decimal bytes | positive integer | no |

### Default

8192

Source: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_HEADER_VALUE_LENGTH`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Bounds each header-value size.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Bounds each header-value size.

## `max_total_header_bytes`

### Short description

Bounds total header bytes.

### Syntax

```text
max_total_header_bytes=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| positive decimal bytes | positive integer | no |

### Default

65536

Source: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_TOTAL_HEADER_BYTES`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Bounds total header bytes.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Bounds total header bytes.

## `phase4_content_types_file`

### Short description

Stores a content-type file path; consumption is connector-specific.

### Syntax

```text
phase4_content_types_file=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| path | one configuration path | no |

### Default

none

Source: `runtime parser has no default`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Stores a content-type file path; consumption is connector-specific.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Stores a content-type file path; consumption is connector-specific.

## `phase4_event_log`

### Short description

Alias for event_path.

### Syntax

```text
phase4_event_log=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| path alias | same grammar as event_path | no |

### Default

none

Source: `runtime parser has no default`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Alias for event_path.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Alias for event_path.

## `phase4_mode`

### Short description

Stores the late P4 policy. Common alone owns no host abort primitive.

### Syntax

```text
phase4_mode=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| enum | minimal \| safe \| strict | no |

### Default

safe

Source: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_PHASE4_MODE`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Stores the late P4 policy. Common alone owns no host abort primitive.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Stores the late P4 policy. Common alone owns no host abort primitive.

## `request_body_limit`

### Short description

Bounds request bytes offered to the engine.

### Syntax

```text
request_body_limit=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| positive decimal bytes | positive integer | no |

### Default

1048576

Source: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_BODY_BUFFER_SIZE`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Bounds request bytes offered to the engine.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Bounds request bytes offered to the engine.

## `request_body_mode`

### Short description

Selects the Common request-body handling mode; a particular host may support only a subset.

### Syntax

```text
request_body_mode=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| enum | none \| buffered \| streaming | no |

### Default

buffered

Source: `common/runtime/msconnector_runtime.c:runtime_defaults`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Selects the Common request-body handling mode; a particular host may support only a subset.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Selects the Common request-body handling mode; a particular host may support only a subset.

## `response_body_limit`

### Short description

Bounds response bytes offered to the engine.

### Syntax

```text
response_body_limit=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| positive decimal bytes | positive integer | no |

### Default

1048576

Source: `common/include/msconnector/limits.h:MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Bounds response bytes offered to the engine.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Bounds response bytes offered to the engine.

## `response_body_mode`

### Short description

Selects the Common response-body handling mode; a particular host may support only a subset.

### Syntax

```text
response_body_mode=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| enum | none \| buffered \| streaming | no |

### Default

none

Source: `common/runtime/msconnector_runtime.c:runtime_defaults`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Selects the Common response-body handling mode; a particular host may support only a subset.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Selects the Common response-body handling mode; a particular host may support only a subset.

## `rules_file`

### Short description

Loads rules from a local file.

### Syntax

```text
rules_file=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| path | one readable rule/configuration file | no |

### Default

none

Source: `runtime parser has no default`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Loads rules from a local file.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Loads rules from a local file.

## `rules_inline`

### Short description

Adds inline rule configuration.

### Syntax

```text
rules_inline=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string | one inline rule/configuration string | no |

### Default

none

Source: `runtime parser has no default`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Adds inline rule configuration.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Adds inline rule configuration.

## `rules_remote_key`

### Short description

Supplies one half of a remote-rule pair.

### Syntax

```text
rules_remote_key=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string | remote key paired with rules_remote_url | no |

### Default

none

Source: `runtime parser has no default`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Supplies one half of a remote-rule pair.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Supplies one half of a remote-rule pair.

## `rules_remote_url`

### Short description

Supplies the remote-rule endpoint; the selected examples do not exercise it.

### Syntax

```text
rules_remote_url=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| URL | remote URL paired with rules_remote_key | no |

### Default

none

Source: `runtime parser has no default`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Supplies the remote-rule endpoint; the selected examples do not exercise it.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Supplies the remote-rule endpoint; the selected examples do not exercise it.

## `transaction_id`

### Short description

Sets a static runtime transaction identifier.

### Syntax

```text
transaction_id=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| string | non-empty text | no |

### Default

none

Source: `runtime parser has no default`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Sets a static runtime transaction identifier.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Sets a static runtime transaction identifier.

## `transaction_id_header`

### Short description

Selects the fallback correlation-header name.

### Syntax

```text
transaction_id_header=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| header name | non-empty HTTP header name | no |

### Default

x-request-id

Source: `common/runtime/msconnector_runtime.c:runtime_defaults`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Selects the fallback correlation-header name.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Selects the fallback correlation-header name.

## `use_error_log`

### Short description

Stores the Common logging preference. A connector must consume it before a host logging effect can be claimed.

### Syntax

```text
use_error_log=<value>
```

### Valid contexts

- Common Runtime key=value file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| boolean | on \| off \| true \| false \| 1 \| 0 \| yes \| no | no |

### Default

on

Source: `common/include/msconnector/options.h:MSCONNECTOR_DEFAULT_USE_ERROR_LOG`.

### Inheritance and merge

No file-level inheritance; host integrations may merge their own configuration before starting Common Runtime.

Merge: When a host uses msconnector_config, scalar child values override parent values; runtime files are parsed as one concrete configuration.

### Phases and runtime effect

See runtime effect; body modes/limits affect P2 and P4, header limits affect P1 and P3.

Stores the Common logging preference. A connector must consume it before a host logging effect can be claimed.

### Validation and errors

Unknown keys, empty values, malformed assignments, and key-specific invalid values fail the runtime configuration check.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/lighttpd/safe/msconnector-runtime.conf](../../examples/lighttpd/safe/msconnector-runtime.conf).

### Safety and operations

Limits bound resource use. Stores the Common logging preference. A connector must consume it before a host logging effect can be claimed.
