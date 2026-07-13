# NGINX Connector

**Language:** English | [Deutsch](README.de.md)

Status: adapter-owned source migration

This directory contains the NGINX proof-of-concept harness, adapter-owned NGINX
connector source, and upstream attribution files for the ModSecurity-nginx
connector. It is still validated by real-world smokes rather than a production
support claim.

Implemented now:

- Documentation of observed local NGINX connector concepts.
- Adapter-owned source under `src/`, plus root-level `config` and metadata,
  derived from ModSecurity-nginx base commit
  `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`.
- Shared directive-name metadata from `common/include/msconnector/directives.h`.
- Shared option/default metadata for enablement, error-log forwarding, and
  phase-4 mode from `common/include/msconnector/options.h`.
- Selected source changes from ModSecurity-nginx PR #377
  (https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377) applied to
  adapter-owned source for phase-4 / late intervention handling.
- A connector-specific runtime harness under `harness/`.
- Shared YAML case consumption through `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.
- Source-derived shared imported cases for raw JSON body matching, simple
  multipart text-field matching, and response-body pass-through.

Not implemented:

- No broad NGINX module rewrite beyond the controlled adapter-owned migration.
- No full NGINX regression suite.
- No runtime pass is claimed beyond environments where the NGINX smoke runner
  observes the YAML-expected real HTTP behavior for the shared YAML cases.
- Full response-body promotion is not claimed. Phase 4 / RESPONSE_BODY remains
  non-promoted; source-level strict-mode wiring is not canonical runtime
  evidence.

## Supported Directives

The adapter-owned NGINX connector currently registers:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_transaction_id`
- `modsecurity_use_error_log on|off`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`
- `modsecurity_phase4_body_limit <bytes>`

`modsecurity_transaction_id` uses an NGINX complex value and may evaluate
per-request variables. Apache-style `modsecurity_transaction_id_expr` is not
registered for NGINX; use `modsecurity_transaction_id` with NGINX variables
instead. The Phase 4 directives are bounded runtime controls.
Phase 4 / RESPONSE_BODY remains non-promoted; source-level strict-mode wiring
does not establish a late-abort result.

Primary local reference: `<external-source-root>/ModSecurity-nginx`.
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-nginx.

The adapter-owned build layout lives under `connectors/nginx/`: module `config`
is at `connectors/nginx/config`, productive sources are under
`connectors/nginx/src/`, and support metadata is at the connector root. The
former `connectors/nginx/upstream/` directory was removed after
materialized-source NGINX builds and smokes passed. Durable attribution stays in
`licenses/nginx/`, `connectors/nginx/ORIGIN.md`, and
`connectors/nginx/SOURCE_MAP.json`.

The build helper is `modules/ModSecurity-test-Framework/ci/provisioning/prepare-nginx-build.sh`. For the monorepo default it
materializes `$BUILD_ROOT/nginx-build/connector-src` from adapter-owned
`connectors/nginx/config` and `connectors/nginx/src` files only, then builds the
connector as a dynamic NGINX module against an official `nginx/nginx` GitHub
release archive. Explicit
`MODSECURITY_NGINX_SOURCE_DIR` overrides still use a sanitized external source
copy.

The current NGINX common-header build contract passes:

```sh
MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include
```

`connectors/nginx/config` consumes this value when constructing NGINX include
paths.

Observed historically on 2026-05-15: `NGINX_RELEASE_TAG=latest` resolved to
`release-1.31.0`, built `nginx/1.31.0`, built
`ngx_http_modsecurity_module.so`, and the harness observed the YAML-expected
HTTP status for all current shared minimal cases. This is not current canonical
Phase-4 facet evidence.

## Test Ownership And Runtime Claims

Executable NGINX connector tests are maintained in the framework module, not
under `connectors/nginx/tests`. The local connector test folder was removed and
must not be reintroduced.

Relevant framework paths:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Historical generated evidence keeps NGINX `partial`:

- Default runtime smoke: `60/60 PASS`.
- Force-all runtime evidence: `140 attempted / 95 PASS / 39 FAIL /
  0 BLOCKED / 6 NOT_EXECUTABLE`.

## Coverage / Runtime Decision Matrix

See the [canonical NGINX guide](../../docs/connectors/nginx.md) for the
evidence boundary and current configuration reference.

NGINX currently remains `partial`: default smoke is clean, force-all evidence
still records FAIL and NOT_EXECUTABLE rows, generated coverage reporting is not
automatic runtime promotion, and RESPONSE_BODY remains non-promoted.

See [configuration](../../docs/configuration.md) for the current Apache/NGINX
directive matrix.

## Common SDK adoption scope

NGINX now maps connector-neutral semantics through `common/` for configuration,
directive names/specs/adapters, request/response mapper contracts, header
helpers, event/limit-facing contracts, and C-standard checks where implemented.
NGINX-specific API ownership remains in `ngx_command_t`, `ngx_http_request_t`,
`ngx_chain_t`/`ngx_buf_t`, access/header/body filters, pools, return codes, and
module build glue. The C17 check is compile-only and reports `BLOCKED`/exit 77
when NGINX or libmodsecurity headers are unavailable; optional C23/future-C
checks depend on compiler support. No production, CRS, full-matrix, or runtime
verification is claimed here.

NGINX Common SDK module builds that use a copied connector source tree must set `MSCONNECTOR_COMMON_SRC` (or `CONNECTOR_COMMON_SRC` / `COMMON_SRC_ROOT`) to the repository Common source root; `MSCONNECTOR_COMMON_INC` remains the Common include root. If unset, the config only falls back to `$ngx_addon_dir/../../common/src` when that path exists.

## Canonical Phase-4 boundary

NGINX uses a bounded native response-body filter.  Its presence does not prove
either a real Phase-4 rule evaluation or a mutable response status at the
moment of intervention.  `phase4_pre_commit_deny` is therefore
`not_implemented`: the native Phase-4 decision is made in the body filter,
after the response-header path.  `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `late_intervention`, `late_intervention_log_only`,
`late_intervention_abort`, and `late_intervention_status_metadata` remain
`implemented_not_asserted` until a current canonical real-host run proves the
individual behavior.

A rule match must be reported independently from a visible 403.  Canonical
events preserve the original host status, requested WAF status, visible client
status, requested action, actual action, header/commit timing, and connection
abort result.  This NGINX body-filter path does not claim a pre-commit deny. A
post-commit safe result is `log_only` with an unchanged visible status; a
strict result is `abort_connection` with an already-visible status and a
confirmed aborted connection.  Neither is a disguised successful 403 case.

The canonical Phase-4 cases are evidence-gated and include rule observation,
pre-commit deny, safe log-only, strict abort, and status/action metadata.  No
response-body payload may enter an event or report.
