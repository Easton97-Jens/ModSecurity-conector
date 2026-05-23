# Shared Features

This document describes the shared functions and concepts in the ModSecurity
connector monorepo. It is based on the current repository state and on the
available source code and documentation. Where the codebase does not prove a
shared runtime implementation, that is stated explicitly.

## Overview

In this project, “Shared Features” does not mean that every Apache and Nginx
runtime path is common code. The shared layer is mainly made of
connector-neutral data shapes, directive names, option values, rule-load
statistics, metadata, and test/reporting concepts. The real server
integrations remain adapter-owned:

- Apache owns its hooks, filters, APXS/Autotools build logic, and
  configuration parser under `connectors/apache/`.
- Nginx owns its Nginx phase handlers, header/body filters, third-party module
  build logic, and configuration parser under `connectors/nginx/`.
- `common/` contains neutral headers and small helper functions, but no Apache
  or Nginx SDK types and no libmodsecurity transaction logic.

Shared features matter because both productive connectors should expose the
same ModSecurity concepts: enablement, rules files, inline rules, remote rules,
transaction ID, error-log policy, rule-load metadata, and comparable test
reporting. Shared metadata prevents directive names and status terms from
drifting between connectors without mixing the very different server APIs.

Relevant cross-project parts:

| Path | Role |
| --- | --- |
| `common/include/msconnector/directives.h` | Shared directive names |
| `common/include/msconnector/options.h` | Shared boolean values, defaults, and option names |
| `common/include/msconnector/rule_load_stats.h` | Shared data shape for loaded rules |
| `common/include/msconnector/request.h` | Neutral request data shape |
| `common/include/msconnector/response.h` | Neutral response data shape |
| `common/include/msconnector/transaction.h` | Neutral phase and transaction view |
| `common/include/msconnector/intervention.h` | Neutral intervention data shape |
| `common/include/msconnector/status.h` | Neutral status values |
| `common/include/msconnector/capabilities.h` | Neutral capability flags |
| `common/include/msconnector/origin.h` | Neutral origin/provenance data shape |
| `common/src/` | Small implementations for status, intervention, origin, and capabilities |
| `modules/ModSecurity-test-Framework/` | Shared YAML cases, runners, normalizers, and smoke helpers |

## Shared Architecture

The architecture is intentionally split in two:

1. `common/` defines neutral shapes and constants.
2. `connectors/apache/` and `connectors/nginx/` translate concrete server
   state into libmodsecurity calls.

`docs/architecture/architecture.md` describes the intended flow:

1. A server hook or filter receives request/response state.
2. The connector adapter translates that state into a form that can be passed
   to libmodsecurity.
3. The adapter calls the libmodsecurity-v3 C API in phase order.
4. Interventions are translated back into server behavior.
5. Connector-specific tests prove timing, artifacts, and HTTP behavior.

The shared headers contain no Apache types such as `request_rec`, no Nginx
types such as `ngx_http_request_t`, and no ownership rules for `ModSecurity`,
`RulesSet`, or `Transaction`. This boundary is documented explicitly in
`docs/architecture/common-runtime-boundaries.md`.

### Relationship to libmodsecurity

Both connectors use libmodsecurity v3 through the public C API. The local
sources show, among others, these kinds of calls:

- initialization with `msc_init`
- connector information through `msc_set_connector_info`
- log callback through `msc_set_log_cb`
- rules creation through `msc_create_rules_set`
- rules loading through `msc_rules_add`, `msc_rules_add_file`, and
  `msc_rules_add_remote`
- rules merge through `msc_rules_merge`
- transaction creation through `msc_new_transaction` or
  `msc_new_transaction_with_id`
- request phases through `msc_process_connection`, `msc_process_uri`,
  `msc_add_request_header`/`msc_add_n_request_header`,
  `msc_process_request_headers`, `msc_append_request_body`, and
  `msc_process_request_body`
- response phases through `msc_add_response_header`/
  `msc_add_n_response_header`, `msc_process_response_headers`,
  `msc_append_response_body`, and `msc_process_response_body`
- logging through `msc_process_logging`
- interventions through `msc_intervention`

This API usage is conceptually shared, but the concrete hooks, timing, buffers,
and error paths are connector-specific.

### Shared Initialization

Both productive connectors create a ModSecurity instance and set connector
information:

- Apache uses `msc_apache_init`, `msc_init`, `msc_set_connector_info`, and
  `msc_set_log_cb` in `connectors/apache/src/mod_security3.c`.
- Nginx uses `ngx_http_modsecurity_create_main_conf`, `msc_init`,
  `msc_set_connector_info`, and `msc_set_log_cb` in
  `connectors/nginx/src/ngx_http_modsecurity_module.c`.

The initialization is therefore conceptually similar, but it is not
implemented as a shared function in `common/src/`.

### Shared Loading of Configuration and Rules

Both connectors register shared directive names from
`common/include/msconnector/directives.h`:

- `modsecurity`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_transaction_id`
- `modsecurity_use_error_log`

Nginx additionally registers Nginx-specific phase-4 directives:

- `modsecurity_phase4_mode`
- `modsecurity_phase4_content_types_file`
- `modsecurity_phase4_log`

Both connectors load rules through libmodsecurity, but through their own parser
functions:

- Apache: `connectors/apache/src/msc_config.c`
- Nginx: `connectors/nginx/src/ngx_http_modsecurity_module.c`

## Configuration Handling

The shared configuration layer is a metadata and directive-name layer. The
actual server configuration remains connector-specific.

### Shared Directives

`common/include/msconnector/directives.h` defines the directive names. This
lets Apache and Nginx use the same spellings in code:

```c
#define MSCONNECTOR_DIRECTIVE_MODSECURITY "modsecurity"
#define MSCONNECTOR_DIRECTIVE_RULES "modsecurity_rules"
#define MSCONNECTOR_DIRECTIVE_RULES_FILE "modsecurity_rules_file"
#define MSCONNECTOR_DIRECTIVE_RULES_REMOTE "modsecurity_rules_remote"
#define MSCONNECTOR_DIRECTIVE_TRANSACTION_ID "modsecurity_transaction_id"
#define MSCONNECTOR_DIRECTIVE_USE_ERROR_LOG "modsecurity_use_error_log"
```

Registration is still different:

- Apache uses `AP_INIT_TAKE1` and `AP_INIT_TAKE2` in
  `connectors/apache/src/msc_config.c`.
- Nginx uses a `ngx_command_t` array in
  `connectors/nginx/src/ngx_http_modsecurity_module.c`.

### Enabling and Disabling

The `modsecurity on|off` directive exists in both connectors. The shared
default in `common/include/msconnector/options.h` is:

```c
#define MSCONNECTOR_DEFAULT_ENABLE MSCONNECTOR_BOOL_OFF
```

This means that without explicit enablement, the connector does not process
requests as ModSecurity-protected requests. The concrete scope differs:

- Apache registers the directive for server and directory contexts
  (`RSRC_CONF | ACCESS_CONF`).
- Nginx registers it for main, server, and location contexts
  (`NGX_HTTP_MAIN_CONF`, `NGX_HTTP_SRV_CONF`, `NGX_HTTP_LOC_CONF`).

### Rules Files and Inline Rules

Both connectors support:

- `modsecurity_rules` for inline rules
- `modsecurity_rules_file` for local rules files
- `modsecurity_rules_remote` for remote rules

Loaded rules are held in a RulesSet and merged during configuration merges.
Load errors are not swallowed:

- Apache returns the libmodsecurity error string from the configuration handler
  when `msc_rules_add*` returns a negative value.
- Nginx also returns an error from the configuration parser on load failures,
  causing `nginx -t` or startup to fail.

### Rule-Load Statistics

`common/include/msconnector/rule_load_stats.h` defines:

```c
typedef struct msconnector_rule_load_stats {
    unsigned inline_rules;
    unsigned file_rules;
    unsigned remote_rules;
} msconnector_rule_load_stats;
```

These values count loaded rules, not the number of directives. They are
increased only after successful `msc_rules_add*` calls.

Current state:

- Apache stores the values in `msc_conf_t` and adds them during directory
  configuration merge. They are not currently emitted in the post-config log.
- Nginx keeps local counters `rules_inline`, `rules_file`, and `rules_remote`,
  and copies them into `msconnector_rule_load_stats` through a small helper.
  Nginx emits these values in the startup log.

The statistics do not change runtime decisions. They are metadata.

### Transaction ID

Both connectors support `modsecurity_transaction_id`, but with different
semantics:

- Apache accepts a static string. If the directive is not set, the connector
  tries to use `UNIQUE_ID`, then falls back to a transaction without an
  explicit ID.
- Nginx uses an Nginx complex value. This allows Nginx variables to be
  evaluated per request.

This is a known, documented difference, not a shared runtime implementation.

### Error-Log Policy

`modsecurity_use_error_log on|off` exists in both connectors. The default in
`common/include/msconnector/options.h` is:

```c
#define MSCONNECTOR_DEFAULT_USE_ERROR_LOG MSCONNECTOR_BOOL_ON
```

`off` suppresses forwarding of the libmodsecurity log callback to the relevant
server error log. It does not disable:

- audit logging
- interventions
- request processing
- response processing
- rules loading
- transaction creation

## Request Processing

Both connectors map incoming requests to libmodsecurity transactions. The
shared conceptual steps are:

1. Create a transaction.
2. Process connection metadata.
3. Process URI, method, and HTTP version.
4. Pass request headers to libmodsecurity.
5. Pass request body data to libmodsecurity when present and accessible.
6. Check interventions after relevant phases.

### Apache

Apache registers, among others, the following in
`connectors/apache/src/mod_security3.c`:

- `ap_hook_pre_config`
- `ap_hook_post_config`
- `ap_hook_post_read_request`
- `ap_hook_fixups`
- `ap_hook_insert_filter`
- `ap_hook_log_transaction`
- input filter `MODSECURITY_IN`
- output filter `MODSECURITY_OUT`

The transaction is created in `create_tx_context`. Request headers are iterated
from `r->headers_in` in `process_request_headers` and passed to
libmodsecurity. Request body data flows through the input filter in
`connectors/apache/src/msc_filters.c`, which calls `msc_append_request_body`
and `msc_process_request_body`.

### Nginx

Nginx registers handlers in `ngx_http_modsecurity_init` for:

- `NGX_HTTP_ACCESS_PHASE`
- `NGX_HTTP_LOG_PHASE`
- header filter
- body filter

The transaction is created in `ngx_http_modsecurity_create_ctx`. In the access
handler, Nginx processes:

- client/server address and ports
- hostname, when available and when the libmodsecurity version supports it
- URI, method, and HTTP version
- request headers through `r->headers_in.headers`
- request body through `ngx_http_read_client_request_body`, in-memory buffers,
  or a temporary file

### Similarities and Differences

The shared concept is the libmodsecurity phase model. Timing, buffering, and
server APIs differ:

- Apache works with `request_rec`, APR tables, and bucket brigades.
- Nginx works with `ngx_http_request_t`, Nginx lists, chains, and request-body
  callbacks.
- Apache has a static transaction-ID option with a `UNIQUE_ID` fallback.
- Nginx can derive transaction IDs from Nginx variables per request.

`common/include/msconnector/request.h` defines a neutral request data shape,
but the productive connectors currently use their own server data directly in
their adapter paths. The neutral data shape is not a fully extracted runtime
API.

## Response Processing

Both connectors contain code that passes response headers and response bodies
to libmodsecurity. The project documents this area carefully because response
body blocking and late interventions strongly depend on the server filter
model.

### Apache

The Apache output filter in `connectors/apache/src/msc_filters.c`:

- reads `r->err_headers_out`
- reads `r->headers_out`
- calls `msc_add_response_header`
- calls `msc_process_response_headers`
- iterates over the bucket brigade
- calls `msc_append_response_body`
- calls `msc_process_response_body`
- checks interventions

The README states that Apache response-body behavior is not promoted, and that
`RESPONSE_BODY` is not treated as a verified blocking capability.

### Nginx

The Nginx header filter in
`connectors/nginx/src/ngx_http_modsecurity_header_filter.c` passes standard
and list headers to libmodsecurity and calls `msc_process_response_headers`.

The Nginx body filter in
`connectors/nginx/src/ngx_http_modsecurity_body_filter.c` passes response body
chunks to `msc_append_response_body` and calls `msc_process_response_body` at
the end. Nginx also has Nginx-specific phase-4 directives for late intervention
behavior:

- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`

These directives are explicitly Nginx-specific and are not part of a shared
Apache/Nginx contract.

### Shared Limitations

The available documentation indicates:

- Response header processing is implemented in both connectors.
- Response body paths exist in both connectors.
- Stable response-body blocking is not promoted as a shared verified
  capability.
- Filter timing differences can lead to different behavior, especially after
  headers have already been sent.

## Logging and Audit Logging

Both connectors set a libmodsecurity log callback:

- Apache: `modsecurity_log_cb`
- Nginx: `ngx_http_modsecurity_log`

These callbacks write to the corresponding server error log unless
`modsecurity_use_error_log` is set to `off`.

Audit logging is not produced by a custom shared connector layer. It is
controlled by libmodsecurity and the loaded ModSecurity rules, for example with
directives such as:

```apache
SecAuditEngine RelevantOnly
SecAuditLogType Serial
SecAuditLog /var/log/modsec_audit.log
```

The smoke harnesses materialize audit log paths in generated runtime
directories:

- Nginx harness: `connectors/nginx/harness/run_nginx_smoke.sh`
- Apache harness: `connectors/apache/harness/run_apache_smoke.sh`

Debugging guidance:

- If error-log messages are missing, check `modsecurity_use_error_log` first.
- If audit logs are missing, first check `SecAuditEngine`, `SecAuditLog`, file
  permissions, and the worker user.
- For Nginx, also check whether `modsecurity_phase4_log` is set when phase-4
  diagnostics are expected.
- For helper builds, build logs and runtime logs are under `BUILD_ROOT`.

## Error Handling

Error handling is conceptually similar, but technically connector-specific.

### Invalid Rules

When loading rules, `msc_rules_add`, `msc_rules_add_file`, and
`msc_rules_add_remote` return a negative value and an error string when
libmodsecurity rejects a rule.

- Apache returns this error string from the configuration handler. This can
  make the Apache configuration test fail.
- Nginx returns an error from the configuration parser. This can make
  `nginx -t` or startup fail.

Rule-load statistics are increased only after successful loads.

### Missing or Invalid Configuration

If `modsecurity` is not enabled, the runtime paths decline processing and let
the request continue through the normal server path. This is not an error; it
is the documented default.

If a rules file cannot be read, a remote rule cannot be loaded, or a rule is
syntactically invalid, the server configuration typically does not load
successfully.

### Internal ModSecurity Errors

Interventions are checked in both connectors after relevant phases:

- Apache uses `process_intervention` and returns HTTP status or redirect
  behavior to Apache for disruptive interventions.
- Nginx uses `ngx_http_modsecurity_process_intervention` and translates status
  or redirect into Nginx behavior. For late response-body interventions,
  additional Nginx-specific phase-4 rules apply.

On internal connector errors, such as a missing transaction context, both
connectors may return server errors or filter errors. These paths are not
unified in `common/`.

## Build and Runtime Dependencies

Shared dependencies:

- C compiler
- Make
- libmodsecurity-v3 headers
- `libmodsecurity.so`
- ModSecurity rules
- correct runtime library search paths

Nginx-specific:

- Nginx source code
- Nginx build dependencies such as PCRE/PCRE2, zlib, and optionally OpenSSL
- Nginx third-party module configuration `connectors/nginx/config`
- dynamic module compatibility between the module and the target Nginx

Apache-specific:

- Apache/httpd
- Apache development package
- `apxs` or `apxs2`
- APR/APR-util
- Autotools for the build from `connectors/apache/`

The available Makefile targets delegate to the test framework:

```sh
make smoke-nginx
make smoke-apache
make smoke-all
make runtime-matrix-all
```

Default build paths are under:

```text
$HOME/.local/state/ModSecurity-conector-build
```

or under an explicitly set `BUILD_ROOT`.

## Security Notes

The connector alone does not protect an application. Effective protection
requires:

- the connector to be enabled
- rules to be loaded
- the correct `SecRuleEngine` mode
- suitable request/response body settings
- writable audit logs
- tested false-positive exceptions

Choose `SecRuleEngine DetectionOnly` and `SecRuleEngine On` deliberately:

- `DetectionOnly` records matches but does not block disruptively.
- `On` allows disruptive behavior such as `deny,status:403`.

For new rule sets, a safe workflow is:

1. Start in a test environment.
2. Inspect audit logs.
3. Identify false positives.
4. Document exceptions.
5. Enable blocking only after that.

Because Apache and Nginx have different hook and filter models, behavior can
differ in edge cases. This is especially true for response body processing,
headers added late by other modules, and interventions after headers have
already been sent to the client.

## Feature Matrix

The following table describes the current state that can be inferred from the
repository code and documentation. “Partial” means that code or tests exist,
but no complete shared or production-generalized guarantee is documented.

| Feature | Nginx | Apache | Notes |
| --- | --- | --- | --- |
| Request Header Inspection | Yes | Yes | Both connectors pass incoming headers to libmodsecurity and invoke request-header processing. |
| Request Body Inspection | Yes | Yes | Both connectors pass request body data to libmodsecurity. Buffering and timing details are server-specific. |
| Response Header Inspection | Yes | Yes | Both connectors contain response-header paths and call `msc_process_response_headers`. |
| Response Body Inspection | Partial | Partial | Code paths exist, but `RESPONSE_BODY` is not promoted as a verified blocking capability in the project documentation. |
| Audit Logging | Partial | Partial | Audit logs are configured through libmodsecurity rules; stable audit-field parity is not implemented as a shared runtime layer. |
| Rules File Loading | Yes | Yes | `modsecurity_rules_file` exists in both connectors and uses libmodsecurity. |
| Inline Rules Loading | Yes | Yes | `modsecurity_rules` exists in both connectors. |
| Remote Rules Loading | Yes | Yes | `modsecurity_rules_remote` exists in both connectors. |
| Blocking Mode | Yes | Yes | Disruptive interventions are evaluated in both connectors; response-body blocking still requires special caution. |
| DetectionOnly Mode | Yes | Yes | Controlled through ModSecurity rules and libmodsecurity, not through a connector-specific directive. |
| Transaction ID | Yes | Yes | Nginx supports complex values; Apache supports static strings with a `UNIQUE_ID` fallback. |
| Error-Log Forwarding Policy | Yes | Yes | `modsecurity_use_error_log on|off`; affects only the error-log callback. |
| Rule-Load-Stats Metadata | Yes | Yes | Shared data shape; Nginx logs the values at startup, Apache keeps them internally. |
| Phase-4 Mode Controls | Yes | No | Nginx-specific directives; no Apache parity in the current code. |

## Known Differences Between Nginx and Apache

### Transaction ID

Apache accepts a static string for `modsecurity_transaction_id`. Nginx accepts
an Nginx complex value and can therefore evaluate Nginx variables per request.

### Configuration Scope

Apache uses Apache contexts through `RSRC_CONF | ACCESS_CONF`. Nginx registers
the directives for main, server, and location contexts. The merge logic differs
accordingly.

### Rule-Load-Stats Reporting

Nginx emits rule-load statistics in the startup log. Apache currently stores
the statistics internally in `msc_conf_t`, but does not emit them in the
post-config log.

### Phase-4 Directives

Only Nginx supports:

- `modsecurity_phase4_mode`
- `modsecurity_phase4_content_types_file`
- `modsecurity_phase4_log`

These directives control Nginx-specific behavior for late response-body
interventions. Apache does not implement them.

### Response Body

Both connectors have response-body code paths. However, the project
documentation does not mark response-body blocking as a shared verified
capability. When in doubt, use real runtime smokes and audit/error logs.

## Troubleshooting Shared Features

### Rules Are Not Loaded

Check:

```sh
nginx -t
apachectl configtest
```

Typical causes:

- wrong path in `modsecurity_rules_file`
- missing read permissions
- invalid rule syntax
- non-unique rule ID
- the libmodsecurity version does not support a rule construct being used

For Nginx, the startup log may also show the number of loaded inline, file, and
remote rules. For Apache, that statistic is currently internal.

### Requests Are Not Blocked

Check:

- Is `modsecurity on` set in the relevant scope?
- Is `SecRuleEngine On` set, or only `DetectionOnly`?
- Does the rule actually match the request?
- Is the test hitting the expected `server`/`location` or directory scope?
- Is a request body expected but not sent, or encoded differently?
- Is a response-body rule being tested even though that area is not promoted as
  a shared blocking capability?

A minimal test case using `ARGS:test` is often better for debugging than
starting with a large rule set.

### Audit Logs Do Not Appear

Check:

- `SecAuditEngine` is set.
- `SecAuditLog` points to a writable path.
- The server worker has write permissions.
- SELinux/AppArmor is not blocking the path.
- The rule actually creates an audit-relevant event.
- The rule does not use `nolog`.

`modsecurity_use_error_log off` does not affect the audit log. It can explain
missing error-log messages, but it is not the cause of missing audit logs.

### Different Behavior Between Nginx and Apache

Possible causes:

- different hook timing
- different request-body buffering
- different header normalization or ordering
- Nginx complex value for transaction ID versus static Apache value
- Nginx-specific phase-4 mode
- different libmodsecurity versions or rules files
- different server modules that modify headers before or after ModSecurity

To narrow this down, test both connectors with the same libmodsecurity version,
the same rules file, and a minimal reproducible request.

### Missing Runtime Dependencies

If a module was built but does not load, check:

```sh
ldd /path/to/ngx_http_modsecurity_module.so
ldd /path/to/mod_security3.so
```

If `libmodsecurity.so` is missing, fix the runtime library search path. In
local helper runs, the harnesses set `LD_LIBRARY_PATH` to the staged
libmodsecurity directories under `BUILD_ROOT`.

## Further Reading

- [Compile Nginx](./COMPILE_NGINX.md)
- [Compile Apache](./COMPILE_APACHE.md)
- `README.md`
- `docs/architecture/architecture.md`
- `docs/architecture/common-runtime-boundaries.md`
- `docs/connectors/directive-parity.md`
- `docs/connectors/rule-load-stats.md`
- `connectors/nginx/README.md`
- `connectors/apache/README.md`
- `connectors/nginx/harness/README.md`
- `connectors/apache/harness/README.md`
