# ModSecurity engine directives used by examples

**Language:** English | [Deutsch](modsecurity-directives.de.md)

## Scope

Only directives actually used in checked-in example rule files are listed. They belong to libmodsecurity, not to an Apache, NGINX, HAProxy, Envoy, Traefik, or lighttpd host parser.

| Option | Layer | Type | Required | Default | Context | Short description |
| --- | --- | --- | --- | --- | --- | --- |
| [`IncludeOptional`](#includeoptional) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | Loads optional engine configuration/rules if present. |
| [`SecAuditEngine`](#secauditengine) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | Enables the selected audit-log policy. |
| [`SecAuditLog`](#secauditlog) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | Sets the engine audit-log path. |
| [`SecAuditLogParts`](#secauditlogparts) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | Selects audit-log parts. |
| [`SecAuditLogType`](#secauditlogtype) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | Sets the selected audit-log write mode. |
| [`SecRequestBodyAccess`](#secrequestbodyaccess) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | On makes request-body input available to engine P2 only when the host supplies it; Off leaves P1 headers available but removes body input from P2. Request inspection limits and actions belong to SecRequestBodyLimit, SecRequestBodyNoFilesLimit, and SecRequestBodyLimitAction. Incremental connector working buffers do not set a total-body limit; separate host authorization-buffer constraints remain documented limitations. |
| [`SecRequestBodyLimit`](#secrequestbodylimit) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | Exclusively sets the engine request-body inspection limit; the connector has no corresponding option, default, or second enforcement logic. |
| [`SecRequestBodyLimitAction`](#secrequestbodylimitaction) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | Exclusively selects the native request-limit action. The connector preserves actual engine results, including DetectionOnly behavior, without choosing rejection or a prefix. |
| [`SecRequestBodyNoFilesLimit`](#secrequestbodynofileslimit) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | Sets the engine limit for request-body data excluding uploaded files; this independent native constraint also applies to non-file request data. |
| [`SecResponseBodyAccess`](#secresponsebodyaccess) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | On makes P4 possible only when the host supplies response bytes that are in scope; Off removes response-body input from P4. It does not widen SecResponseBodyMimeType, override SecResponseBodyLimit/SecResponseBodyLimitAction, or force a status change after headers commit. With the selected safe late-intervention policy, a post-commit disruptive result is recorded as log_only rather than a promised later 403; response capture can add bounded memory, CPU, and sensitive-data exposure. |
| [`SecResponseBodyLimit`](#secresponsebodylimit) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | Exclusively sets the response-body inspection limit; the connector has no corresponding option, default, or second enforcement logic. |
| [`SecResponseBodyLimitAction`](#secresponsebodylimitaction) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | Exclusively selects Reject or ProcessPartial when the engine inspection limit is exceeded; the connector forwards native results and interventions. |
| [`SecResponseBodyMimeType`](#secresponsebodymimetype) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | Scopes engine response-body inspection by MIME type. |
| [`SecRule`](#secrule) | ModSecurity Engine | ModSecurity engine directive | no | No default is inferred from examples. | Loaded ModSecurity configuration/rule file | Defines a rule from a variable, operator, and comma-separated actions. The local illustration uses RESPONSE_BODY, @contains, id, phase, deny, log, and status; redirect and transformations are separate action forms whose validity and observable effect remain engine/host- and commit-boundary dependent. |
| [`SecRuleEngine`](#secruleengine) | ModSecurity Engine | ModSecurity engine directive | no | The used examples select On; no repository source establishes a global engine default. | Loaded ModSecurity configuration/rule file | Controls rule execution/disruptive action inside libmodsecurity, independently of the host connector switch. |

## Rule syntax walkthrough

```apache
SecRule RESPONSE_BODY "@contains response-attack" \
    "id:1100301,phase:4,deny,log,status:403"
```

`RESPONSE_BODY` is the variable, `@contains` is the operator, and `response-attack` is its argument. Actions assign a unique `id`, select `phase:4`, request `deny`, record `log`, and request `status:403` before host commit.
After response commit a connector cannot reliably replace the visible status line. `SecResponseBodyAccess On` and a P4 rule therefore do not guarantee a later 403 response.
`VARIABLE` selects the data to inspect, `OPERATOR` defines the comparison, and `ACTIONS` is the comma-separated control list. `id` uniquely identifies the rule, `phase` selects evaluation timing, `deny` requests a disruptive decision, and `log` records the match. `status` applies only while the host can still change the HTTP status; `redirect` additionally needs a target and has the same commit-boundary constraint. Transformations are explicit actions that alter input before the operator, so keep them minimal and reviewable. The illustrated rule does not use redirect or a transformation action.

## Option details

<a id="includeoptional"></a>
## `IncludeOptional`

### Short description

Loads optional engine configuration/rules if present.

### Syntax

```text
IncludeOptional <path-or-glob>
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | path or glob | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

See directive runtime effect.

Loads optional engine configuration/rules if present.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/p1-p4-safe.conf](../../examples/apache/rules/p1-p4-safe.conf).

### Safety and operations

Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.

<a id="secauditengine"></a>
## `SecAuditEngine`

### Short description

Enables the selected audit-log policy.

### Syntax

```text
SecAuditEngine RelevantOnly
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | engine audit mode | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

See directive runtime effect.

Enables the selected audit-log policy.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/p1-p4-safe.conf](../../examples/apache/rules/p1-p4-safe.conf).

### Safety and operations

Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.

<a id="secauditlog"></a>
## `SecAuditLog`

### Short description

Sets the engine audit-log path.

### Syntax

```text
SecAuditLog <path>
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | path | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

See directive runtime effect.

Sets the engine audit-log path.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/p1-p4-safe.conf](../../examples/apache/rules/p1-p4-safe.conf).

### Safety and operations

Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.

<a id="secauditlogparts"></a>
## `SecAuditLogParts`

### Short description

Selects audit-log parts.

### Syntax

```text
SecAuditLogParts <parts>
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | audit part letters | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

See directive runtime effect.

Selects audit-log parts.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/p1-p4-safe.conf](../../examples/apache/rules/p1-p4-safe.conf).

### Safety and operations

Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.

<a id="secauditlogtype"></a>
## `SecAuditLogType`

### Short description

Sets the selected audit-log write mode.

### Syntax

```text
SecAuditLogType Serial
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | audit log type | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

See directive runtime effect.

Sets the selected audit-log write mode.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/p1-p4-safe.conf](../../examples/apache/rules/p1-p4-safe.conf).

### Safety and operations

Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.

<a id="secrequestbodyaccess"></a>
## `SecRequestBodyAccess`

### Short description

On makes request-body input available to engine P2 only when the host supplies it; Off leaves P1 headers available but removes body input from P2. Request inspection limits and actions belong to SecRequestBodyLimit, SecRequestBodyNoFilesLimit, and SecRequestBodyLimitAction. Incremental connector working buffers do not set a total-body limit; separate host authorization-buffer constraints remain documented limitations.

### Syntax

```text
SecRequestBodyAccess On | Off
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | On \| Off | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

P2. On permits body inspection only after the connector has supplied request bytes; body mode selects input availability, while native request-limit directives govern engine inspection.

On makes request-body input available to engine P2 only when the host supplies it; Off leaves P1 headers available but removes body input from P2. Request inspection limits and actions belong to SecRequestBodyLimit, SecRequestBodyNoFilesLimit, and SecRequestBodyLimitAction. Incremental connector working buffers do not set a total-body limit; separate host authorization-buffer constraints remain documented limitations.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file. A syntactically valid On still cannot create P2 input when the selected host path does not expose a request body.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Safety and operations

Request bodies may contain credentials or personal data. Configure native engine body limits, appropriate MIME/parser policy, and protected audit/debug logs; no performance quantity is inferred here.

<a id="secrequestbodylimit"></a>
## `SecRequestBodyLimit`

### Short description

Exclusively sets the engine request-body inspection limit; the connector has no corresponding option, default, or second enforcement logic.

### Syntax

```text
SecRequestBodyLimit <bytes>
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | positive byte count | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

See directive runtime effect.

Exclusively sets the engine request-body inspection limit; the connector has no corresponding option, default, or second enforcement logic.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Safety and operations

Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.

<a id="secrequestbodylimitaction"></a>
## `SecRequestBodyLimitAction`

### Short description

Exclusively selects the native request-limit action. The connector preserves actual engine results, including DetectionOnly behavior, without choosing rejection or a prefix.

### Syntax

```text
SecRequestBodyLimitAction ProcessPartial | Reject
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | ProcessPartial \| Reject | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

See directive runtime effect.

Exclusively selects the native request-limit action. The connector preserves actual engine results, including DetectionOnly behavior, without choosing rejection or a prefix.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Safety and operations

Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.

<a id="secrequestbodynofileslimit"></a>
## `SecRequestBodyNoFilesLimit`

### Short description

Sets the engine limit for request-body data excluding uploaded files; this independent native constraint also applies to non-file request data.

### Syntax

```text
SecRequestBodyNoFilesLimit <bytes>
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | positive byte count | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

See directive runtime effect.

Sets the engine limit for request-body data excluding uploaded files; this independent native constraint also applies to non-file request data.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Safety and operations

Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.

<a id="secresponsebodyaccess"></a>
## `SecResponseBodyAccess`

### Short description

On makes P4 possible only when the host supplies response bytes that are in scope; Off removes response-body input from P4. It does not widen SecResponseBodyMimeType, override SecResponseBodyLimit/SecResponseBodyLimitAction, or force a status change after headers commit. With the selected safe late-intervention policy, a post-commit disruptive result is recorded as log_only rather than a promised later 403; response capture can add bounded memory, CPU, and sensitive-data exposure.

### Syntax

```text
SecResponseBodyAccess On | Off
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | On \| Off | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

P4. On is necessary but not sufficient: the connector must expose response bytes, the MIME type must be in SecResponseBodyMimeType scope, and SecResponseBodyLimit/SecResponseBodyLimitAction apply. Technical frame and storage controls remain independent.

On makes P4 possible only when the host supplies response bytes that are in scope; Off removes response-body input from P4. It does not widen SecResponseBodyMimeType, override SecResponseBodyLimit/SecResponseBodyLimitAction, or force a status change after headers commit. With the selected safe late-intervention policy, a post-commit disruptive result is recorded as log_only rather than a promised later 403; response capture can add bounded memory, CPU, and sensitive-data exposure.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file. At runtime, an engine-excluded response MIME type, disabled host body path, or exceeded limit can leave P4 without the expected complete body input.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Safety and operations

Response bodies can be large and sensitive. Keep MIME scope and response limits narrow, protect logs, and do not equate safe post-commit evidence with a client-visible later 403.

<a id="secresponsebodylimit"></a>
## `SecResponseBodyLimit`

### Short description

Exclusively sets the response-body inspection limit; the connector has no corresponding option, default, or second enforcement logic.

### Syntax

```text
SecResponseBodyLimit <bytes>
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | positive byte count | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

See directive runtime effect.

Exclusively sets the response-body inspection limit; the connector has no corresponding option, default, or second enforcement logic.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Safety and operations

Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.

<a id="secresponsebodylimitaction"></a>
## `SecResponseBodyLimitAction`

### Short description

Exclusively selects Reject or ProcessPartial when the engine inspection limit is exceeded; the connector forwards native results and interventions.

### Syntax

```text
SecResponseBodyLimitAction ProcessPartial | Reject
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | ProcessPartial \| Reject | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

See directive runtime effect.

Exclusively selects Reject or ProcessPartial when the engine inspection limit is exceeded; the connector forwards native results and interventions.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Safety and operations

Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.

<a id="secresponsebodymimetype"></a>
## `SecResponseBodyMimeType`

### Short description

Scopes engine response-body inspection by MIME type.

### Syntax

```text
SecResponseBodyMimeType <type/subtype> [...]
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | one or more MIME types | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

See directive runtime effect.

Scopes engine response-body inspection by MIME type.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Safety and operations

Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.

<a id="secrule"></a>
## `SecRule`

### Short description

Defines a rule from a variable, operator, and comma-separated actions. The local illustration uses RESPONSE_BODY, @contains, id, phase, deny, log, and status; redirect and transformations are separate action forms whose validity and observable effect remain engine/host- and commit-boundary dependent.

### Syntax

```text
SecRule VARIABLE "OPERATOR" "id:<id>,phase:<n>,actions"
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | rule expression | no |

### Default

No default is inferred from examples.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

The phase action selects the evaluation point; the local RESPONSE_BODY example uses P4. A disruptive action can affect the visible HTTP result only while the host can still intervene.

Defines a rule from a variable, operator, and comma-separated actions. The local illustration uses RESPONSE_BODY, @contains, id, phase, deny, log, and status; redirect and transformations are separate action forms whose validity and observable effect remain engine/host- and commit-boundary dependent.

### Validation and errors

The host/libmodsecurity rejects malformed variable/operator/action syntax, duplicate or invalid identifiers, and invalid action combinations when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Safety and operations

Rules are executable security policy. Give each rule a stable id, keep transformations explicit and minimal, protect rule-file ownership, and verify disruptive/redirect behavior on the selected host before relying on it.

<a id="secruleengine"></a>
## `SecRuleEngine`

### Short description

Controls rule execution/disruptive action inside libmodsecurity, independently of the host connector switch.

### Syntax

```text
SecRuleEngine On | Off | DetectionOnly
```

### Valid contexts

- Loaded ModSecurity configuration/rule file

### Values

| Type | Allowed values | Required |
| --- | --- | --- |
| ModSecurity engine directive | On \| Off \| DetectionOnly | no |

### Default

The used examples select On; no repository source establishes a global engine default.

Source: `not inferred; only checked-in example usage is documented`.

### Inheritance and merge

Engine-specific; not a host connector merge setting.

Merge: Engine-specific; include order and rule configuration determine effective behavior.

### Phases and runtime effect

See directive runtime effect.

Controls rule execution/disruptive action inside libmodsecurity, independently of the host connector switch.

### Validation and errors

The host/libmodsecurity rejects invalid engine syntax when loading the rule file.

### Example

Selected value: use the syntax above and the source-backed file below.

Source-backed example: [examples/apache/rules/detection-only.conf](../../examples/apache/rules/detection-only.conf).

### Safety and operations

Engine policy can inspect, log, detect, or disrupt traffic; protect rule and audit-log paths.
