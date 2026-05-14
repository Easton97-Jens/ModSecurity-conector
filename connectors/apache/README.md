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
- A local source-built httpd run observed HTTP `403` for that minimal case on
  2026-05-14.

Not implemented:

- No Apache module source.
- No source import from `ModSecurity-apache`.
- No claim that the Apache connector is complete beyond the documented minimal
  smoke.

Primary local reference: `/root/conecter/ModSecurity-apache`.

Build and runtime artifacts must stay under `BUILD_ROOT`, defaulting locally to
`/src/ModSecurity-conector-build`.

See `docs/apache-poc.md` and `connectors/apache/harness/README.md`.
