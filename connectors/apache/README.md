# Apache Connector

Status: scaffolded

This directory is reserved for an Apache adapter for libmodsecurity v3.

Implemented now:

- Documentation of observed local Apache connector concepts.
- Directory layout for future source and connector-specific tests.
- A PoC build-preparation helper in `ci/prepare-apache-build.sh`.
- A local runtime smoke harness under `connectors/apache/harness/`.
- Use of the shared minimal case
  `tests/common/cases/minimal/phase2_args_block.yaml`.

Not implemented:

- No Apache module source.
- No source import from `ModSecurity-apache`.
- No claim that the Apache module builds unless the helper completes.
- No claim that the Apache module loads or blocks unless the harness observes
  HTTP `403`.

Primary local reference: `/root/conecter/ModSecurity-apache`.

Build and runtime artifacts must stay under `BUILD_ROOT`, defaulting locally to
`/src/ModSecurity-conector-build`.

See `docs/apache-poc.md` and `connectors/apache/harness/README.md`.
