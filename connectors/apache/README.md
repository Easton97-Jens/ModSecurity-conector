# Apache Connector

Status: scaffolded

This directory is reserved for an Apache adapter for libmodsecurity v3.

Implemented now:

- Documentation of observed local Apache connector concepts.
- Directory layout for future source and connector-specific tests.
- A PoC build-preparation helper in `ci/prepare-apache-build.sh`.
- A local runtime smoke harness under `connectors/apache/harness/`.
- Use of all shared minimal cases under `tests/common/cases/minimal/`.
- Use of source-derived shared imported cases, including raw JSON body,
  simple multipart text-field, and response-body pass-through smokes.
- A local source-built httpd run observed the YAML-expected HTTP status for all
  current shared minimal cases on 2026-05-15.

Not implemented:

- No Apache module source.
- No source import from `ModSecurity-apache`.
- No claim that the Apache connector is complete beyond the documented shared
  minimal/imported smokes.

Primary local reference: `/root/conecter/ModSecurity-apache`.

Build and runtime artifacts must stay under `BUILD_ROOT`, defaulting locally to
`/src/ModSecurity-conector-build`.

See `docs/apache-poc.md` and `connectors/apache/harness/README.md`.
