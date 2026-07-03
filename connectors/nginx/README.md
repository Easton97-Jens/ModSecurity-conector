# NGINX Connector

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
  non-promoted; bounded strict-abort evidence is documented/reported as runtime
  evidence only.

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

`modsecurity_transaction_id` uses an NGINX complex value and may evaluate
per-request variables. The Phase 4 directives are bounded runtime controls.
Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.

Primary local reference: `/root/conecter/ModSecurity-nginx`.
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-nginx.

The adapter-owned build layout lives under `connectors/nginx/`: module `config`
is at `connectors/nginx/config`, productive sources are under
`connectors/nginx/src/`, and support metadata is at the connector root. The
former `connectors/nginx/upstream/` directory was removed after
materialized-source NGINX builds and smokes passed. Durable attribution stays in
`licenses/nginx/`, `connectors/nginx/ORIGIN.md`, and
`connectors/nginx/SOURCE_MAP.json`.

The build helper is `modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh`. For the monorepo default it
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

Observed locally on 2026-05-15: `NGINX_RELEASE_TAG=latest` resolved to
`release-1.31.0`, built `nginx/1.31.0`, built
`ngx_http_modsecurity_module.so`, and the harness observed the YAML-expected
HTTP status for all current shared minimal cases.

## Test Ownership And Runtime Claims

Executable NGINX connector tests are maintained in the framework module, not
under `connectors/nginx/tests`. The local connector test folder was removed and
must not be reintroduced.

Relevant framework paths:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Current generated evidence keeps NGINX `partial`:

- Default runtime smoke: `60/60 PASS`.
- Force-all runtime evidence: `140 attempted / 95 PASS / 39 FAIL /
  0 BLOCKED / 6 NOT_EXECUTABLE`.

## Coverage / Runtime Decision Matrix

See `docs/coverage-decision-matrix.md`.

NGINX currently remains `partial`: default smoke is clean, force-all evidence
still records FAIL and NOT_EXECUTABLE rows, generated coverage reporting is not
automatic runtime promotion, and RESPONSE_BODY remains non-promoted.

See `docs/connectors/directive-parity.md` for the current Apache/NGINX
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
