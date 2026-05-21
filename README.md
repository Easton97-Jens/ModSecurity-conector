# ModSecurity Connector Monorepo

This repository contains connector-focused code and integration scaffolding for
libmodsecurity v3 based server connectors. The reusable test framework lives in
the `modules/ModSecurity-test-Framework` module; this repository keeps the
connector source trees, connector metadata, harness integration, and generated
connector evidence.

## Connector Architecture

The repository is split into a connector-neutral C layer and adapter-owned
connector trees:

- `common/include/msconnector/` defines shared request, response, transaction,
  intervention, capability, origin, logging, and status data shapes.
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
