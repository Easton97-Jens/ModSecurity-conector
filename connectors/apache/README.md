# Apache Connector

Status: adapter-owned source migration complete

This directory is reserved for an Apache adapter for libmodsecurity v3.

Implemented now:

- Documentation of observed local Apache connector concepts.
- Adapter-owned Apache connector layout under `connectors/apache/`, with
  productive source under `connectors/apache/src/`.
- Shared directive-name metadata from `common/include/msconnector/directives.h`.
- A PoC build-preparation helper in `modules/ModSecurity-test-Framework/ci/prepare-apache-build.sh`.
- A local runtime smoke harness under `connectors/apache/harness/`.
- Use of all shared minimal cases under `modules/ModSecurity-test-Framework/tests/cases/`.
- Use of source-derived shared imported cases, including raw JSON body,
  simple multipart text-field, and response-body pass-through smokes.
- A local source-built httpd run observed the YAML-expected HTTP status for all
  current shared minimal cases on 2026-05-15.

Not implemented:

- No maintained Apache module rewrite beyond path ownership and provenance
  migration.
- No claim that the Apache connector is complete beyond the documented shared
  minimal/imported smokes.
- No Apache support for the NGINX phase-4 directives
  `modsecurity_phase4_mode`, `modsecurity_phase4_content_types_file`, or
  `modsecurity_phase4_log`.

## Supported Directives

The adapter-owned Apache connector currently registers:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_use_error_log on|off`
- `modsecurity_transaction_id <string>`

`modsecurity_transaction_id` accepts a static string only. It does not evaluate
Apache expressions, expand environment variables, or attempt NGINX
complex-value parity. If the directive is unset, the connector keeps the
existing `UNIQUE_ID` fallback and then creates a transaction without an explicit
ID if `UNIQUE_ID` is absent or empty.

`modsecurity_use_error_log off` suppresses Apache error-log forwarding from the
libmodsecurity log callback only. It does not change audit logging,
intervention behavior, request or response handling, hooks, filters, buckets,
or transaction ownership.

Primary local reference: `/root/conecter/ModSecurity-apache`.
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-apache.

The Apache adapter-owned build layout lives under `connectors/apache/` and is
materialized to `$BUILD_ROOT/apache-build/connector-src` before Autotools/APXS
builds run. The former `connectors/apache/upstream/` tree was removed after the
Phase 11 materialized build and Apache smoke passed. Phase 13 keeps
`connectors/apache/src/` limited to productive C sources; build files live at
the connector root, retained Autotools test templates live under
`modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/`, and durable attribution lives in
`licenses/apache/`, `connectors/apache/ORIGIN.md`, and
`connectors/apache/SOURCE_MAP.json`.

Build and runtime artifacts must stay under `BUILD_ROOT`, defaulting locally to
`/src/ModSecurity-conector-build`.

See `docs/connectors/directive-parity.md` and
`connectors/apache/harness/README.md`.
