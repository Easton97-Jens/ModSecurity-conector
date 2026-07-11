# Apache Connector

**Language:** English | [Deutsch](README.de.md)

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
- A historical local source-built httpd run observed the YAML-expected HTTP
  status for all current shared minimal cases on 2026-05-15. It is not current
  canonical Phase-4 facet evidence.

Not implemented:

- No maintained Apache module rewrite beyond path ownership and provenance
  migration.
- No claim that the Apache connector is complete beyond the documented shared
  minimal/imported smokes.
- No full RESPONSE_BODY promotion. Source-level Phase-4 and strict-mode wiring
  are not canonical runtime evidence.

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
remains non-promoted; source-level strict-mode wiring does not establish a
late-abort result.

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

Historical generated evidence keeps Apache `partial`:

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

## Common SDK adoption boundary

The Apache connector now embeds `msconnector_config` for connector-neutral
configuration values, uses Common directive names/parser helpers for the
adopted directives, and includes Apache-owned request/response mapper facades
that validate `request_rec`-derived metadata against the Common mapper
contracts. Phase-4 metadata events are written through the Common metadata-only
`msconnector_event` JSONL path; request and response body payloads are not
written to those event records.

Apache-specific code remains in the Apache connector: `command_rec`
registration, `request_rec` access, hooks, filters, APR pools, bucket brigades,
APLOG logging, return-code mapping, and APXS/autotools build inputs.

This Common SDK adoption does not claim production readiness, CRS coverage,
full-matrix coverage, or new runtime verification behavior.

## Canonical Phase-4 boundary

Apache uses a native httpd output-filter path that borrows the current bucket,
passes the current brigade onward before EOS, and finishes Phase 4 at EOS.
That is incremental ingestion with end-of-stream evaluation, not per-chunk
rule evaluation. The checked-in manifest intentionally declares
`response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort`, and
`late_intervention_status_metadata` as `implemented_not_asserted`.  No current
canonical real-host evidence promotes any of those facets.

`phase4_pre_commit_deny` is deliberately `not_implemented`: the body decision
is made at EOS after the response-header path, so the native host has no
deterministic uncommitted response-body decision point. A denial branch in
source is not a basis for claiming a visible Phase-4 HTTP status rewrite.

A Phase-4 rule match is not evidence of a client-visible 403.  A canonical
event must keep `original_http_status`, requested WAF status,
`visible_http_status`, `requested_action`, `actual_action`, response-commit
metadata, and `connection_aborted` separate.  Before commitment a deny may be
possible; after commitment the common policy can only record `log_only` in
safe mode or `abort_connection` in strict mode.  Neither outcome may be
reported as a successful pre-commit deny without matching host evidence.

The required applicable cases are `phase4_rule_observed`,
`phase4_deny_after_commit_log_only`, `phase4_deny_after_commit_abort`, and the
two metadata cases. `phase4_deny_before_commit` remains unselected for this
host model. All cases remain evidence-gated rather than inferred from this
source description, and events contain metadata only—never response-body
payloads.
