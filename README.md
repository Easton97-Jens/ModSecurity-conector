# ModSecurity Connector Monorepo

This repository contains connector-focused code and integration scaffolding for
libmodsecurity v3 based server connectors. The reusable test framework lives in
the `modules/ModSecurity-test-Framework` module; this repository keeps the
connector source trees, connector metadata, harness integration, and generated
connector evidence.

## Connector Architecture

The repository is split into a connector-neutral C layer and adapter-owned
connector trees:

- `common/include/msconnector/` defines shared directive, option/default,
  rule-load-stat, request, response, transaction, intervention, capability,
  origin, logging, and status data shapes.
- `common/src/` contains small connector-neutral helper implementations.
- `connectors/apache/` contains the Apache connector adapter, Autotools/APXS
  build inputs, harness files, metadata, and productive source under
  `connectors/apache/src/`.
- `connectors/nginx/` contains the NGINX connector adapter, module `config`,
  harness files, metadata, and productive source under `connectors/nginx/src/`.
- `connectors/{envoy,haproxy,lighttpd,traefik}/` are scaffolded future
  connector areas with documentation and TODOs.

Connector source is repo-local. Apache and NGINX connector repositories are not
fetched as runtime defaults.

## Supported Connectors

| Connector | Status | Primary path |
| --- | --- | --- |
| Apache | adapter-owned scaffold with source-build smoke harness | `connectors/apache/` |
| NGINX | adapter-owned scaffold with source-build smoke harness | `connectors/nginx/` |
| Envoy | placeholder scaffold | `connectors/envoy/` |
| HAProxy | placeholder scaffold | `connectors/haproxy/` |
| Lighttpd | placeholder scaffold | `connectors/lighttpd/` |
| Traefik | placeholder scaffold | `connectors/traefik/` |

## Connector Feature Status

The Apache and NGINX connectors share connector-neutral metadata in `common/`,
but keep server runtime behavior in their adapter-owned trees. The tables below
describe the current implemented state only.

### Shared Features

| Feature | Apache | NGINX | Notes |
| --- | --- | --- | --- |
| <code>modsecurity on&#124;off</code> | Supported | Supported | Shared directive name from `common/include/msconnector/directives.h`; server-specific directive registration remains adapter-owned. |
| Inline rules | Supported | Supported | `modsecurity_rules`; rules loading and error paths remain connector-specific. |
| Rules file | Supported | Supported | `modsecurity_rules_file`; values count toward rule-load metadata after successful loads. |
| Remote rules | Supported | Supported | `modsecurity_rules_remote`; remote loading remains connector-specific. |
| Transaction ID | Supported | Supported | Apache accepts a static string or a separate Apache expression directive; NGINX accepts an NGINX complex value. |
| Error-log forwarding policy | Supported | Supported | <code>modsecurity_use_error_log on&#124;off</code>; default is on. Audit logs, interventions, and request/response handling are unchanged. |
| Rule-load stats metadata | Supported | Supported | Common data shape in `common/include/msconnector/rule_load_stats.h`; metadata only. |
| Common directive metadata | Used | Used | Shared directive-name constants are used by both connectors. |
| Common option metadata | Partial | Partial | Apache uses common bool/default metadata for error-log policy. NGINX uses common defaults for enablement, error-log forwarding, and phase-4 mode. |

### Apache

The Apache connector is an adapter-owned Apache module under
`connectors/apache/`. It currently supports:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_use_error_log on|off`
- `modsecurity_transaction_id <string>`
- `modsecurity_transaction_id_expr <apache-expression>`

`modsecurity_transaction_id` keeps the existing static-string semantics.
`modsecurity_transaction_id_expr` is an opt-in Apache string expression, for
example `%{REQUEST_URI}`, evaluated per request. Static and expression
transaction IDs are mutually exclusive in the same Apache context; normal
child-context overrides apply during config merge. If neither directive is set,
or if the expression evaluates to an empty value or fails, Apache keeps the
existing `UNIQUE_ID` fallback and then creates a transaction without an
explicit ID if no usable `UNIQUE_ID` value is available.

`modsecurity_use_error_log off` suppresses Apache error-log forwarding from the
libmodsecurity log callback only. It does not change audit logging,
interventions, hooks, filters, buckets, transaction ownership, or request and
response handling.

Apache tracks rule-load stats internally in `msc_conf_t`. It does not currently
report those stats in the post-config log. Apache does not implement NGINX
phase-4 parity yet.

### NGINX

The NGINX connector is an adapter-owned dynamic NGINX module under
`connectors/nginx/`. It currently supports:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_transaction_id`
- `modsecurity_use_error_log on|off`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`

`modsecurity_transaction_id` uses an NGINX complex value and may evaluate
per-request NGINX variables. NGINX exposes rule-load stats in its existing
startup log through the common rule-load-stats helper without changing the log
text, format, level, or order.

The phase-4 directives are NGINX-specific runtime controls. They are not a
common connector contract and are not implemented by Apache.

### Known Differences And Deferred Areas

| Area | Current state |
| --- | --- |
| Transaction ID mapping | Apache supports static strings plus opt-in Apache string expressions through `modsecurity_transaction_id_expr`; NGINX supports complex values through `modsecurity_transaction_id`. |
| Apache phase-4 directives | `modsecurity_phase4_mode`, `modsecurity_phase4_content_types_file`, and `modsecurity_phase4_log` are not implemented for Apache. |
| Apache response body behavior | Not promoted; `RESPONSE_BODY` remains non-verified and non-promoted. |
| Apache bucket/filter/intervention paths | Intentionally not refactored in this common-metadata work. |
| Common layer | Contains connector-neutral metadata and data shapes only; it does not own Apache or NGINX runtime APIs. |
| Rule-load stats reporting | NGINX reports via its existing startup log; Apache keeps stats as internal metadata until display aggregation and merge semantics are explicitly designed. |

## Connector Metadata

Adapter metadata is owned by each connector:

- `connectors/apache/metadata.c`
- `connectors/nginx/metadata.c`
- `connectors/*/ORIGIN.md`
- `licenses/*/ORIGIN.md`
- `config/testing/import-status.json`

The metadata drift checks compare connector source attribution with the
connector and framework documentation without linking connector runtime code.

## Build And Runtime Integration

The public connector targets remain stable and delegate to the framework module
where appropriate:

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

Source-build variables remain configurable:

```sh
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build
SOURCE_ROOT=$BUILD_ROOT/sources
MODSECURITY_GIT_REF=v3/master
MODSECURITY_SOURCE_DIR=$SOURCE_ROOT/ModSecurity_V3
```

`BUILD_ROOT` is a local build/output location, not a cache contract. Full
runtime validation is local and evidence-based; `make smoke-all` is
authoritative only when it is actually executed successfully.

## Build Documentation

Detailed build and feature documentation:

- [Compile Nginx](./COMPILE_NGINX.md)
- [Compile Apache](./COMPILE_APACHE.md)
- [Shared Features](./SHARED_FEATURES.md)

## Framework Module Integration

Initialize the framework module before running framework-backed targets:

```sh
git submodule update --init --recursive
```

The default module path is:

```sh
modules/ModSecurity-test-Framework
```

Override it when using a separate checkout:

```sh
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make quick-check
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make runtime-matrix-all
```

The framework owns YAML cases, runners, normalizers, runtime-matrix logic,
coverage generation, v3 API smoke helpers, and reusable testing documentation.
Connector-specific generated evidence is written in this repository under
`reports/testing/`, with a generated root copy at `TEST-COVERAGE-SUMMARY.md`.

## Documentation Links

- Architecture docs: `docs/architecture/`
- Connector docs: `docs/connectors/`
- Licensing and origin index: `docs/licensing/license-and-origin.md`
- Framework docs: `modules/ModSecurity-test-Framework/README.md`
- Connector test evidence: `reports/testing/`
- Generated coverage summary: `TEST-COVERAGE-SUMMARY.md`

## Local Development

Typical local setup:

```sh
git submodule update --init --recursive
make setup-dev
make lint
make quick-check
make generate-test-matrix
make check-test-matrix
```

Runtime and coverage evidence must not be inferred from generated metadata
alone. XFAIL, pending, future, connector-gap, and runtime-difference cases stay
evidence classes until explicitly promoted by documented runtime proof.
RESPONSE_BODY remains non-verified and non-promoted.
