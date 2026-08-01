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
- No broad runtime promotion is claimed. One selected native no-CRS/no-MRTS H1
  Phase-4 out-of-scope case passed under the focused task evidence; that result
  does not establish the canonical lifecycle, a complete matrix, or transport
  coverage.
- Full response-body promotion is not claimed. Phase 4 / RESPONSE_BODY remains
  non-promoted; source-level strict-mode wiring is not canonical runtime
  evidence.
- No HTTP/2, HTTP/3, remote-rule, Helgrind, or canonical Memcheck result is
  claimed by this source/provenance update. The direct H1 post-suppression
  Memcheck result below is clean only within its bounded noncanonical
  NGINX-core diagnostic boundary, not as a connector result.

## Selective Upstream Security Intake

The adapter-owned source keeps the upstream base
`9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` and the earlier local Phase-4
overlay from PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac`. The current
selective intake is recorded per file in [the origin map](ORIGIN.md) and
[`SOURCE_MAP.json`](SOURCE_MAP.json):

- [PR #384](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/384)
  at `65de4cd8739209f22d924d85548bd012a4d94607` distinguishes final body
  processing from partial ingestion. Final
  `msc_process_request_body()`/`msc_process_response_body()` failures fail
  closed, while `msc_append_request_body()`,
  `msc_request_body_from_file()`, and `msc_append_response_body()` retain
  nonfatal `ProcessPartial` handling because that return signal also denotes
  by-design limit truncation.
- [PR #385](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/385)
  at `471a2a54843bb8f560758a7e75b146db2243ab29` supplies selected
  response-header and pre-commit redirect-replacement handling. A task-local
  extension suppresses fictional synthetic `Connection`/`Keep-Alive` fields
  on native HTTP/3 as well as HTTP/2; the negotiated response-version mapping
  and suppression are source-level only, not HTTP/2 or HTTP/3 runtime proof.
- [PR #386](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/386)
  at `a7fd4fcc18dc442b1b093d253f457b9317b7f588` supplies selected
  value-free header-registration warnings, empty-address guards, and terminal
  body-filter forwarding behavior.
- [PR #387](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/387)
  at `4c1f0362ca0f25ef216ce59cad5fa6c9703c1438` informs the Parent-owned
  opt-in bounded native soak (`make soak-nginx`) and H1 Memcheck diagnostic
  (`make memcheck-nginx`) through the existing harness. Both remain outside
  default smoke/test/CI and record bounded payload-free summaries. The
  source-controlled soak selector permits from one to eight unique IDs from
  its explicit canonical catalog and rejects empty, duplicate, or noncatalog
  selections before case discovery. Upstream Dockerfiles, workflows, Valgrind/Helgrind
  configuration, and tooling are not
  imported. The direct H1 post-suppression Memcheck result below is clean only
  within its bounded noncanonical diagnostic boundary; no canonical Memcheck,
  Helgrind, or soak result is claimed.

The intake does not change the documented Phase-4 result model: a Safe late
result is `log_only` with the visible status unchanged, while a Strict late
result is `abort_connection` after commit rather than a fabricated second
response.

It also restores a pre-task Parent content-type ingestion regression. Bounded
response bytes now reach ModSecurity irrespective of configured connector
Content-Type scope; when that inspection detects an out-of-scope intervention,
the connector maps it to `log_only` with `content_type_not_in_scope`. This does
not relax #384: final `msc_process_response_body()` processing remains
fail-closed for a result other than `1`, while append/from-file
`ProcessPartial` handling remains intentionally nonfatal.

The strict isolated rebuild and C17, C23, and c2y passed, and the newly
materialized build-source SHA matched the task filter. The selected native
no-CRS/no-MRTS H1 out-of-scope case passed. The selected Parent Safe/Strict
outcomes were observed as `log_only` with unchanged visible status and
post-commit `abort_connection`, respectively, but the full selected runner
exits nonzero due to read-only Framework fixture contradictions
(`FND-FRAMEWORK-0058`, `blocked`/`out_of_scope`): Safe expects the mode as the
reason, while Strict jointly expects a stable `403`/obsolete action despite a
connection abort. No Framework edit is asserted. These focused observations do
not establish H2/H3, remote-rule, soak, a clean canonical Memcheck, or delivery
evidence.

### Direct H1 Memcheck diagnostic

The initial direct H1 Valgrind run observed one 8-byte `definitely lost`
allocation on the NGINX-core worker-exit path. It is not a connector or
ModSecurity security flaw. The exact generated stack was verified against an
independently SHA-verified official `nginx-1.31.2` archive (observed SHA-256
prefix/suffix `af2a957...473c`).

The bounded post-suppression direct H1 O7 artifact
`direct-nginx-h1-memcheck-suppressed-20260801T234500Z-c8d9e0f1` is clean only
within this direct diagnostic boundary: `status=clean`, `complete=1`,
`errors_detected=0`, `error_count=0`, `definitely_lost_bytes=0`,
`indirectly_lost_bytes=0`, `possibly_lost_bytes=28160`, and
`still_reachable_bytes=329918`. Its selected connector-loaded benign case
completed `48` requests with `request_failures=0`,
`worker_summary_failures=0`, and `server_alive=1`. The isolated lifecycle
recorded `shutdown=graceful`, `wait=exited`, `wrapper_exit_code=0`, and
`containment=isolated`; no residual NGINX or Valgrind process, `nginx.pid`, or
test-port binding remained.

The source-controlled local file
[`harness/valgrind-nginx-core-1.31.2.supp`](harness/valgrind-nginx-core-1.31.2.supp)
is not copied from upstream. It matches only a definite `Memcheck:Leak` on
`malloc -> ngx_alloc -> ngx_set_environment -> ngx_worker_process_init ->
ngx_worker_process_cycle -> ngx_spawn_process -> ngx_start_worker_processes ->
ngx_master_process_cycle -> main`. The artifact records `suppressed: 1 from 1`.
Possible losses remain reported in the payload-free summary rather than being
suppressed. A changed stack, connector/libmodsecurity diagnostic, or
invalid-access diagnostic does not match and remains failing.

The source-controlled suppression is used only in opt-in `NGINX_MEMCHECK=1`
mode after all three runtime identity gates pass: the selected `NGINX_BINARY`
equals `$NGINX_PREFIX/sbin/nginx`; its `nginx -v` output is exactly
`nginx version: nginx/1.31.2`; and
`$NGINX_BUILD_DIR/verified-archives/nginx-1.31.2.tar.gz` has the
source-controlled SHA-256
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`.
Outside Memcheck mode, normal harness calls retain the existing
caller-selected `NGINX_BINARY` override behavior.

The diagnostic remains noncanonical while canonical provisioning/lifecycle
containment and its worker-visible docroot projection are in progress. This
direct result does not establish `runtime-smoke-nginx`, H2/H3, remote CI,
SonarQube, pull-request, or delivery success.

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
Phase 4 / RESPONSE_BODY remains non-promoted. The focused H1 observations above
do not establish a broad late-abort or canonical lifecycle result.

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

The final-processing guard is intentionally narrower than body ingestion:
`ProcessPartial` append/from-file handling does not become a generic 500 path.
It therefore preserves the existing Safe/Strict Phase-4 outcome model rather
than turning a partial-body limit decision into a late intervention claim.
