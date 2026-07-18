# Apache Connector

**Language:** English | [Deutsch](README.de.md)

Status: adapter-owned source migration complete

This directory is reserved for an Apache adapter for libmodsecurity v3.

Implemented now:

- Documentation of observed local Apache connector concepts.
- Adapter-owned Apache connector layout under `connectors/apache/`, with
  productive source under `connectors/apache/src/`.
- Shared directive-name metadata from `common/include/msconnector/directives.h`.
- A PoC build-preparation helper in `modules/ModSecurity-test-Framework/ci/provisioning/prepare-apache-build.sh`.
- A local runtime smoke harness under `connectors/apache/harness/`.
- Use of all shared minimal cases under `modules/ModSecurity-test-Framework/tests/cases/`.
- Use of source-derived shared imported cases, including raw JSON body,
  simple multipart text-field, and response-body Allow-control smokes.
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

The Phase 4 directives are bounded runtime controls. In particular,
`modsecurity_phase4_content_types_file` is a deprecated compatibility parser:
it cannot narrow the Apache all-response pre-commit gate. Use
`SecResponseBodyMimeType` to select libModSecurity inspection instead. Phase 4
/ RESPONSE_BODY remains non-promoted; source-level strict-mode wiring does not
establish a late-abort result.

Primary local reference: `<external-source-root>/ModSecurity-apache`.
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

See the [canonical Apache guide](../../docs/connectors/apache.md) for the
evidence boundary and current configuration reference.

Apache currently remains `partial`: default smoke is clean, force-all evidence
still records FAIL and NOT_EXECUTABLE rows, generated coverage reporting is not
automatic runtime promotion, and RESPONSE_BODY remains non-promoted.

See [configuration](../../docs/configuration.md) and
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

Apache's output filter is an EOS-only all-response enforcement gate. It
incrementally appends every data bucket to libModSecurity and saves the
normalized Apache brigade in the request pool across filter calls. It forwards
no original response byte, including a response that has no data buckets and
only EOS, until the first EOS has arrived, `msc_process_response_body` has
completed, and the intervention has been resolved. This deliberately trades
client-visible progressive response streaming for a complete Phase-4 decision;
it is not per-chunk rule evaluation.

The connector cannot safely query libModSecurity's effective
`SecResponseBodyMimeType` selection through the C API. It consequently gates
every response MIME type. `SecResponseBodyMimeType` still selects engine
inspection, while the deprecated
`modsecurity_phase4_content_types_file` cannot create an uninspected
pass-through route. The default `modsecurity_phase4_body_limit` is 1048576
bytes (1 MiB). A response that exceeds it fails closed before any original
response byte is released; it is not processed partially and then streamed.

At the normal decision boundary, Apache's `r->sent_bodyct` and `eos_sent` are
not commit proof: upstream modules can set them before this filter has released
anything. The gate instead uses its own released-EOS state and Apache's
`r->bytes_sent`. A normal Phase-4 deny discards the saved original brigade,
preserves the relevant P3 response state, and emits exactly one terminal error
response before original output can be released. On an allow, the retained
brigade (including its EOS) is passed once synchronously and the terminal
output guard is sealed, preventing a later producer from duplicating body or
EOS output. Errors while saving, appending, or finishing the response discard
the retained brigade and fail closed; a genuinely post-commit failure aborts
the connection.

`log_only` in safe/minimal mode and `abort_connection` in strict mode are
defensive late-intervention fallbacks only when independent commit proof already
exists. They do not reinterpret a normal, still-gated Phase-4 deny as log-only
or remove the pre-release deny path.

A normal `r->prev` internal redirect, including a pre-output ErrorDocument,
fails closed because a transaction that processed the source URI, headers, and
body cannot be safely rebound to a different target/ruleset through the public
libModSecurity C API. The sole exception is one synchronous, Apache-core-marked
local ErrorDocument hop while the terminal guard is `EMITTING`; it requires the
Apache `no_local_copy` marker and an immediate predecessor status matching
`REDIRECT_STATUS`, and the guard admits no second hop. This lets the one
legitimate terminal error body be emitted without
opening a normal redirect bypass.

The checked-in manifest intentionally declares the source-wired Phase-4 and
late-intervention facets `implemented_not_asserted` until current real-host
evidence exists. The focused H1/H2 evidence placeholder is
`ci/runtime/lifecycle/run-apache-phase4-response-regression.sh`; record only
its run-scoped artifacts after execution. This source contract does not label
either H1 or H2 as passed.
