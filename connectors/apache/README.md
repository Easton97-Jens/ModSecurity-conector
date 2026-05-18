# Apache Connector

Status: adapter-owned source migration complete

This directory is reserved for an Apache adapter for libmodsecurity v3.

Implemented now:

- Documentation of observed local Apache connector concepts.
- Adapter-owned Apache connector layout under `connectors/apache/`, with
  productive source under `connectors/apache/src/`.
- A PoC build-preparation helper in `ci/prepare-apache-build.sh`.
- A local runtime smoke harness under `connectors/apache/harness/`.
- Use of all shared minimal cases under `tests/common/cases/minimal/`.
- Use of source-derived shared imported cases, including raw JSON body,
  simple multipart text-field, and response-body pass-through smokes.
- A local source-built httpd run observed the YAML-expected HTTP status for all
  current shared minimal cases on 2026-05-15.

Not implemented:

- No maintained Apache module rewrite beyond path ownership and provenance
  migration.
- No claim that the Apache connector is complete beyond the documented shared
  minimal/imported smokes.

Primary local reference: `/root/conecter/ModSecurity-apache`.
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-apache.

The Apache adapter-owned build layout lives under `connectors/apache/` and is
materialized to `$BUILD_ROOT/apache-build/connector-src` before Autotools/APXS
builds run. The former `connectors/apache/upstream/` tree was removed after the
Phase 11 materialized build and Apache smoke passed. Phase 13 keeps
`connectors/apache/src/` limited to productive C sources; build files live at
the connector root, retained Autotools test templates live under
`connectors/apache/tests/`, and durable attribution lives in
`licenses/apache/`, `connectors/apache/ORIGIN.md`, and
`connectors/apache/SOURCE_MAP.json`.

Build and runtime artifacts must stay under `BUILD_ROOT`, defaulting locally to
`/src/ModSecurity-conector-build`.

See `docs/connectors/apache-poc.md` and `connectors/apache/harness/README.md`.
