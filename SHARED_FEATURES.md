# Shared Features

**Language:** English | [Deutsch](SHARED_FEATURES.de.md)

This document expands the root README's `Connector Feature Status` section. It
describes shared connector behavior only when that behavior is visible in the
README, existing documentation, tests, scripts, Makefiles, or source files.
Where the repository only provides general ModSecurity connector background or
environment-specific guidance, that is labeled clearly.

## Confirmed Repository Behavior

The repository is a connector monorepo for libmodsecurity v3 based server
connectors. Apache and NGINX share connector-neutral metadata in `common/`, but
server runtime behavior remains in adapter-owned connector trees.

Confirmed from the root README:

- `common/include/msconnector/` defines shared directive, option/default,
  rule-load-stat, request, response, transaction, intervention, capability,
  origin, logging, and status data shapes.
- `common/src/` contains small connector-neutral helper implementations.
- `connectors/apache/` contains the Apache connector adapter, Autotools/APXS
  build inputs, harness files, metadata, and productive source under
  `connectors/apache/src/`.
- `connectors/nginx/` contains the NGINX connector adapter, module `config`,
  harness files, metadata, and productive source under `connectors/nginx/src/`.
- Connector source is repo-local. Apache and NGINX connector repositories are
  not fetched as runtime defaults.
- Runtime and coverage evidence must not be inferred from generated metadata
  alone.
- XFAIL, pending, future, connector-gap, and runtime-difference cases stay
  evidence classes until explicitly promoted by documented runtime proof.
- `RESPONSE_BODY` remains non-verified and non-promoted.

## Shared Architecture

The shared architecture is metadata-first and connector-neutral. `common/`
does not own Apache or NGINX runtime APIs. It provides data shapes and helper
functions that can be consumed by adapter-owned code and by framework reporting
without pulling server SDKs into the common layer.

Confirmed common paths:

| Path | Confirmed role |
| --- | --- |
| `common/include/msconnector/directives.h` | Shared directive-name constants |
| `common/include/msconnector/options.h` | Shared option/default metadata |
| `common/include/msconnector/rule_load_stats.h` | Shared rule-load-stat data shape |
| `common/include/msconnector/request.h` | Connector-neutral request shape |
| `common/include/msconnector/response.h` | Connector-neutral response shape |
| `common/include/msconnector/transaction.h` | Connector-neutral phase and transaction view |
| `common/include/msconnector/intervention.h` | Connector-neutral intervention shape |
| `common/include/msconnector/status.h` | Connector-neutral status values |
| `common/include/msconnector/capabilities.h` | Connector-neutral capability flags |
| `common/include/msconnector/origin.h` | Connector-neutral origin/provenance shape |
| `common/include/msconnector/logging.h` | Connector-neutral logging shape |
| `common/src/` | Small helper implementations for connector-neutral metadata |

Confirmed non-boundaries from `docs/architecture/common-runtime-boundaries.md`:

- Common does not own Apache hook registration or bucket brigades.
- Common does not own NGINX module registration, phase handlers, or filters.
- Common does not own request body or response body handling.
- Common does not own libmodsecurity object ownership or transaction lifetime.
- Common does not own `RESPONSE_BODY` behavior.

Any future extraction that touches those runtime areas requires separate
design, evidence, and real-world connector smokes.

## Framework and Validation Integration

The framework module lives at:

```text
modules/ModSecurity-test-Framework
```

The root README defines the setup and override pattern:

```sh
git submodule update --init --recursive

FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make quick-check
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make runtime-matrix-all
```

The framework owns YAML cases, runners, normalizers, runtime-matrix logic,
coverage generation, v3 API smoke helpers, and reusable testing documentation.
Connector-specific generated evidence is written under:

```text
reports/testing/
TEST-COVERAGE-SUMMARY.md
```

The public connector targets listed by the README are:

```sh
make setup-dev
make lint
make quick-check
make generate-test-matrix
make check-test-matrix
make runtime-matrix-all
make smoke-apache
make smoke-nginx
make smoke-all
```

The README's evidence rule is important: `make smoke-all` is authoritative only
when it is actually executed successfully. Generated coverage is reporting, not
runtime proof by itself.

Current reference points:

| Topic | Reference |
| --- | --- |
| YAML schema shape | `modules/ModSecurity-test-Framework/docs/imports/common/schema.md` |
| Shared fixtures | `modules/ModSecurity-test-Framework/docs/imports/common/fixtures.md` |
| Smoke target semantics | `modules/ModSecurity-test-Framework/docs/testing/fast-checks.md` |
| Capability model | `docs/architecture/capability-model.md` |
| Status model | `docs/architecture/status-model.md` |
| Origin/provenance and licenses | `docs/licensing/license-and-origin.md` |
| Real-world connector path | `reports/testing/real-world-connector-validation.md` |
| Case matrix | `reports/testing/case-matrix.md` and `reports/testing/generated/case-matrix.generated.md` |
| PR/source evidence | `reports/testing/evidence/pr-evidence-summary.md` |

## Shared Build Variables

The README documents the shared source-build variable pattern:

```sh
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build
SOURCE_ROOT=$BUILD_ROOT/sources
MODSECURITY_GIT_REF=v3/master
MODSECURITY_SOURCE_DIR=$SOURCE_ROOT/ModSecurity_V3
```

These variables apply to both Apache and NGINX framework-backed build paths:

| Variable | Shared meaning |
| --- | --- |
| `BUILD_ROOT` | Local build/output location, not a cache contract |
| `SOURCE_ROOT` | Source checkout area used by helper scripts |
| `MODSECURITY_GIT_REF` | libmodsecurity v3 git ref |
| `MODSECURITY_SOURCE_DIR` | libmodsecurity v3 source directory |
| `FRAMEWORK_ROOT` | Optional test-framework override |

Apache and NGINX add connector-specific variables in their helper scripts, but
the README-level convention is that generated build and runtime output stays
under `BUILD_ROOT`.

## Shared Directive Support

The root README's shared feature table describes the current implemented state
only. The common directive metadata comes from
`common/include/msconnector/directives.h`, while server-specific directive
registration remains adapter-owned.

Confirmed shared directives:

| Feature | Apache | NGINX | Notes |
| --- | --- | --- | --- |
| `modsecurity on|off` | Supported | Supported | Shared directive name; server-specific registration remains adapter-owned. |
| Inline rules | Supported | Supported | `modsecurity_rules`; rules loading and error paths remain connector-specific. |
| Rules file | Supported | Supported | `modsecurity_rules_file`; successful loads count toward rule-load metadata. |
| Remote rules | Supported | Supported | `modsecurity_rules_remote`; remote loading remains connector-specific. |
| Error-log forwarding policy | Supported | Supported | `modsecurity_use_error_log on|off`; default is on. Audit logs, interventions, and request/response handling are unchanged. |
| Rule-load stats metadata | Supported | Supported | Common data shape in `common/include/msconnector/rule_load_stats.h`; metadata only. |
| Common directive metadata | Used | Used | Shared directive-name constants are used by both connectors. |
| Common option metadata | Partial | Partial | Apache uses common bool/default metadata for error-log policy. NGINX uses common defaults for enablement, error-log forwarding, and phase-4 mode. |

## Transaction ID Behavior

Transaction ID behavior is shared as a feature area, but not as identical
syntax.

Confirmed current behavior:

- Apache supports `modsecurity_transaction_id <string>`.
- Apache supports `modsecurity_transaction_id_expr <apache-expression>`.
- NGINX supports `modsecurity_transaction_id` as an NGINX complex value.

Apache semantics from the README and `docs/connectors/directive-parity.md`:

- `modsecurity_transaction_id` keeps static-string semantics.
- `modsecurity_transaction_id_expr` is an opt-in Apache string expression.
- Confirmed expression syntax includes `%{REQUEST_URI}`.
- Static and expression transaction IDs are mutually exclusive in the same
  Apache context.
- Normal child-context overrides apply during config merge.
- If neither directive is set, or if the expression evaluates to an empty value
  or fails, Apache keeps the existing `UNIQUE_ID` fallback and then creates a
  transaction without an explicit ID if no usable `UNIQUE_ID` value is
  available.

NGINX semantics:

- `modsecurity_transaction_id` uses an NGINX complex value.
- Values may be evaluated per request by NGINX.

This is a confirmed difference between connectors.

## Rule-Load Stats Metadata

`common/include/msconnector/rule_load_stats.h` defines the shared data shape:

```c
typedef struct msconnector_rule_load_stats {
    unsigned inline_rules;
    unsigned file_rules;
    unsigned remote_rules;
} msconnector_rule_load_stats;
```

Confirmed semantics from `docs/connectors/rule-load-stats.md`:

- Values count loaded rules, not directive invocations.
- `file_rules` counts rules loaded from rule files; it does not count the
  number of files.
- Stats are increased only after successful `msc_rules_add*` calls.
- Failed load attempts keep the existing error path and do not increase the
  counters.
- No connector uses these stats to decide whether a request should be
  processed, blocked, logged, or inspected.
- NGINX exposes the values through its existing startup log.
- Apache currently keeps the values as internal config metadata only.

Rule-load stats are metadata. They do not change rules loading, rules merging,
request handling, response handling, or any runtime decision.

## Request and Response Processing

General ModSecurity connector background: a server connector typically maps
connection metadata, URI, headers, request body, response headers, response
body, logging, and interventions into libmodsecurity transaction calls.

Confirmed repository boundary: Apache and NGINX runtime processing is
adapter-owned. Common does not own these paths.

Apache owns:

- hook registration
- input and output filters
- bucket brigade behavior
- Apache config parsing
- intervention finalization
- libmodsecurity transaction lifetime

NGINX owns:

- module registration
- access, header, body, and log filters
- phase handlers
- phase-4 late intervention behavior
- libmodsecurity transaction lifetime

The existence of connector-neutral request, response, transaction, and
intervention data shapes in `common/include/msconnector/` does not mean that
the productive Apache and NGINX runtime has been refactored into a common
engine layer.

## Logging and Audit Logging

Confirmed shared policy:

- `modsecurity_use_error_log on|off` exists for both Apache and NGINX.
- The default is on.
- `off` suppresses server error-log forwarding from the libmodsecurity log
  callback only.
- Audit logs, interventions, hooks, filters, buckets, transaction ownership,
  and request/response handling are unchanged.

General ModSecurity background: audit logging is primarily controlled by
libmodsecurity configuration and rules, for example `SecAuditEngine` and
`SecAuditLog`. This repository does not document a separate common audit-log
runtime layer. Audit-log behavior should be validated through real connector
smokes and generated evidence, not inferred from metadata alone.

## NGINX-Specific Phase-4 Controls

The NGINX connector currently supports:

- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`

These are NGINX-specific runtime controls. They are not a common connector
contract and are not implemented by Apache.

The README explicitly lists Apache phase-4 directives as deferred:

- `modsecurity_phase4_mode`
- `modsecurity_phase4_content_types_file`
- `modsecurity_phase4_log`

Response body behavior remains not promoted. `RESPONSE_BODY` remains
non-verified and non-promoted.

## Feature Matrix

This matrix records confirmed repository behavior and the README's current
implemented state only.

| Feature | NGINX | Apache | Notes |
| --- | --- | --- | --- |
| `modsecurity on|off` | Yes | Yes | Shared directive name; runtime registration is adapter-owned. |
| Inline rules | Yes | Yes | `modsecurity_rules`; loading behavior remains connector-owned. |
| Rules file loading | Yes | Yes | `modsecurity_rules_file`; successful loads count toward metadata. |
| Remote rules loading | Yes | Yes | `modsecurity_rules_remote`; remote loading remains connector-owned. |
| Static transaction ID | No | Yes | Apache `modsecurity_transaction_id <string>`. NGINX uses complex values instead. |
| Expression/complex transaction ID | Yes | Yes | NGINX uses `modsecurity_transaction_id`; Apache uses `modsecurity_transaction_id_expr`. Syntax is server-specific. |
| Error-log forwarding policy | Yes | Yes | `modsecurity_use_error_log on|off`; does not affect audit logs or interventions. |
| Rule-load stats metadata | Yes | Yes | Common data shape. NGINX reports at startup; Apache stores internally. |
| Request header processing | Adapter-owned | Adapter-owned | Present in connector runtime paths, not owned by `common/`. |
| Request body processing | Adapter-owned | Adapter-owned | Present in connector runtime paths, not owned by `common/`. |
| Response header processing | Adapter-owned | Adapter-owned | Present in connector runtime paths, not owned by `common/`. |
| Response body processing | Not promoted | Not promoted | `RESPONSE_BODY` remains non-verified and non-promoted. |
| Audit logging | libmodsecurity/rules-driven | libmodsecurity/rules-driven | No common audit-log runtime layer is documented. |
| NGINX phase-4 controls | Yes | No | NGINX-specific runtime controls; Apache parity is deferred. |

## Known Differences and Deferred Areas

Confirmed from the README:

| Area | Current state |
| --- | --- |
| Transaction ID mapping | Apache supports static strings plus opt-in Apache string expressions through `modsecurity_transaction_id_expr`; NGINX supports complex values through `modsecurity_transaction_id`. |
| Apache phase-4 directives | `modsecurity_phase4_mode`, `modsecurity_phase4_content_types_file`, and `modsecurity_phase4_log` are not implemented for Apache. |
| Apache response body behavior | Not promoted; `RESPONSE_BODY` remains non-verified and non-promoted. |
| Apache bucket/filter/intervention paths | Intentionally not refactored in this common-metadata work. |
| Common layer | Contains connector-neutral metadata and data shapes only; it does not own Apache or NGINX runtime APIs. |
| Rule-load stats reporting | NGINX reports via its existing startup log; Apache keeps stats as internal metadata until display aggregation and merge semantics are explicitly designed. |

## Troubleshooting Shared Features

### Shared Cases Do Not Run

Initialize or override the framework module:

```sh
git submodule update --init --recursive
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make quick-check
```

Then run connector-specific smoke targets:

```sh
make smoke-apache
make smoke-nginx
```

### Generated Evidence Looks Stale

Regenerate and check the matrix files through the README-listed targets:

```sh
make generate-test-matrix
make check-test-matrix
```

Remember that generated metadata is not runtime evidence by itself.

### Rules Appear Not to Load

For repository smokes, inspect logs under `BUILD_ROOT`, especially connector
logs below:

```text
$BUILD_ROOT/logs/apache/
$BUILD_ROOT/logs/nginx/
```

Rule-load stats are metadata. NGINX reports them in startup logs; Apache stores
them internally. Failed rule loads should follow connector-specific
configuration error paths.

### Apache and NGINX Behave Differently

First check whether the behavior is documented as a known difference:

- transaction-ID syntax differs
- Apache has `modsecurity_transaction_id_expr`
- NGINX has NGINX-specific phase-4 directives
- `RESPONSE_BODY` is non-verified and non-promoted
- hooks, filters, body handling, intervention finalization, and transaction
  lifetime are adapter-owned

Then validate with the framework-backed smoke targets rather than comparing
generated metadata alone.

## Further Reading

- [Compile Nginx](./docs/build/compilers/nginx.md)
- [Compile Apache](./docs/build/compilers/apache.md)
- `README.md`
- `docs/architecture/architecture.md`
- `docs/architecture/common-runtime-boundaries.md`
- `docs/connectors/directive-parity.md`
- `docs/connectors/rule-load-stats.md`
- `connectors/nginx/README.md`
- `connectors/apache/README.md`
- `connectors/nginx/harness/README.md`
- `connectors/apache/harness/README.md`
