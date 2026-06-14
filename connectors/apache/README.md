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
- No full RESPONSE_BODY promotion. Bounded Phase 4 strict-abort evidence is
  documented as runtime evidence only.

## Supported Directives

The adapter-owned Apache connector currently registers:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_use_error_log on|off`
- `modsecurity_transaction_id <string>`
- `modsecurity_transaction_id_expr <apache-expression>`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`
- `modsecurity_phase4_body_limit <bytes>`

`modsecurity_transaction_id` accepts a static string and keeps the existing
static semantics. `modsecurity_transaction_id_expr` accepts an Apache string
expression, for example `%{REQUEST_URI}`, and evaluates it per request. The two
directives are mutually exclusive in the same Apache context; normal
child-context overrides apply during config merge. If neither directive is set,
or if the expression evaluates to an empty value or fails, the connector keeps
the existing `UNIQUE_ID` fallback and then creates a transaction without an
explicit ID if `UNIQUE_ID` is absent or empty.

`modsecurity_use_error_log off` suppresses Apache error-log forwarding from the
libmodsecurity log callback only. It does not change audit logging,
intervention behavior, request or response handling, hooks, filters, buckets,
or transaction ownership.

The Phase 4 directives are bounded runtime controls. Phase 4 / RESPONSE_BODY
remains non-promoted; bounded strict-abort evidence is documented/reported as
runtime evidence only.

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

## Test Ownership And Runtime Claims

Executable Apache connector tests are maintained in the framework module, not
under `connectors/apache/tests`. The local connector test folder was removed
and must not be reintroduced.

Relevant framework paths:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Current generated evidence keeps Apache `partial`:

- Default runtime smoke: `54/54 PASS`.
- Force-all runtime evidence: `133 attempted / 100 PASS / 27 FAIL /
  0 BLOCKED / 6 NOT_EXECUTABLE`.

## Coverage / Runtime Decision Matrix

See `docs/coverage-decision-matrix.md`.

Apache currently remains `partial`: default smoke is clean, force-all evidence
still records FAIL and NOT_EXECUTABLE rows, generated coverage reporting is not
automatic runtime promotion, and RESPONSE_BODY remains non-promoted.

See `docs/connectors/directive-parity.md` and
`connectors/apache/harness/README.md`.
