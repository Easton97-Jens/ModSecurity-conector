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
  claimed by this source/provenance update. The retained direct H1
  post-suppression Memcheck artifact below is pre-hardening, noncanonical
  historical evidence, not final proof of the current connector or harness.

## Selective Upstream Security Intake

The adapter-owned source keeps the upstream base
`9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` and the earlier local Phase-4
overlay from PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac`. The current
selective intake is recorded per file in [the origin map](ORIGIN.md) and
[`SOURCE_MAP.json`](SOURCE_MAP.json):

- [PR #384](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/384)
  at `65de4cd8739209f22d924d85548bd012a4d94607` distinguishes final body
  processing from partial ingestion. In the current adapter, the final
  `msc_process_request_body()`/`msc_process_response_body()` calls and the
  `msc_append_request_body()`, `msc_request_body_from_file()`, and
  `msc_append_response_body()` ingestion calls all require the libmodsecurity
  success return value `1`; any other return, including `0`, fails closed.
  The upstream `ProcessPartial` limit-truncation interpretation is therefore
  not a nonfatal path in this adapter.
- [PR #385](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/385)
  at `471a2a54843bb8f560758a7e75b146db2243ab29` supplies selected
  response-header and pre-commit redirect-replacement handling. A task-local
  extension requires connector-owned `Location` provenance before it regards
  Phase-3 output as a response replacement, rejects redirect URL CR/LF before
  installation, and suppresses fictional synthetic `Connection`/`Keep-Alive`
  fields on native HTTP/3 as well as HTTP/2; these source-level changes are not
  HTTP/2 or HTTP/3 runtime proof.
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
  imported. The retained direct H1 post-suppression artifact below is
  pre-hardening and noncanonical; no canonical Memcheck, Helgrind, or soak
  result is claimed.

The intake does not change the documented Phase-4 result model: a Safe late
result is `log_only` with the visible status unchanged, while a Strict late
result is `abort_connection` after commit rather than a fabricated second
response.

It also restores a pre-task Parent content-type ingestion regression. Bounded
response bytes now reach ModSecurity irrespective of configured connector
Content-Type scope; when that inspection detects an out-of-scope intervention,
the connector maps it to `log_only` with `content_type_not_in_scope`. This does
not relax #384: final response processing and response-body ingestion remain
fail-closed for a result other than `1`. Request-body memory and file ingestion
use the same strict return contract.

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

### Parent response and harness hardening

The current Parent-only Phase-3 hardening treats a response as replaced only
when `intervention_redirect_location_installed` records that the connector
redirect helper installed its own `Location`. A pre-existing upstream
`Location` on a status-only intervention is not sufficient and instead uses
NGINX finalization. A redirect URL containing CR or LF fails closed with
`NGX_HTTP_BAD_REQUEST` before buffer allocation or `Location` installation.

The direct harness requires root execution and fails closed unless root resolves
and verifies `NGINX_WORKER_USER` as a distinct local account and resolves its
group. It renders `user <resolved-user> <resolved-group>;` explicitly in the
generated NGINX configuration. It separates root-owned private runtime
material, harness logs including `NGINX_PHASE4_LOG_FILE`, and
`NGINX_MEMCHECK_EVIDENCE_DIR` from the only worker-owned paths:
`NGINX_WORKER_STATE_ROOT` and the `NGINX_SERVER_LOG_ROOT` access/error/audit
leaves. `NGINX_MEMCHECK_EVIDENCE_DIR` is private below
`LOG_DIR/memcheck-evidence/<case>`; only the separate `worker-state` and
`server-logs` trees are below the worker-traversable harness root. Overlapping
paths or worker visibility of private output block the harness. The opt-in
docroot projection described below is a separate root-owned static boundary,
not another worker-owned harness output.

The Memcheck summarizer treats evidence as trusted only when its root and
parent are effective-UID-owned real directories that are not group- or
other-writable, every metadata/log/output path is a direct child, and every
input is a private single-link regular file opened with no-follow protection
and checked for replacement while read. Unsafe evidence is rejected or marked
incomplete rather than promoted to a clean result.

The retained receipt
`$RUN/evidence/direct-nginx-h1-memcheck-evidence-remediation-20260801.md`
(SHA-256
`37f01fe3d1851d43ae21d2b705b02bf01f204ff5cb19b41354e5b801a4b158a8`)
records `passed_noncanonical_diagnostic` for one bounded three-second
`allow_without_marker` no-CRS H1 case under deliberate `umask 022`. The root
run used the distinct verified `nobody` worker, kept the private output root
mode `0700`, and kept worker state/server-log leaves mode `0700` and owned by
`nobody:nogroup`; the summarizer accepted two private Valgrind inputs and
wrote its role, lifecycle, JSON, and text outputs mode `0600`. Its 28 requests
had no request or worker-summary failures, and its clean complete summary had
zero errors and zero definitely/indirectly lost bytes.

This is direct runtime evidence for the remediated harness/evidence boundary,
not current C redirect behavior: it uses the retained SHA-verified NGINX
`1.31.2` pre-current-C diagnostic artifact. A separate fresh C-source build
validated the prior C code, but this receipt does not execute that code. The
exact final security scan and final PR-head CI/Sonar evidence remain pending.

### Parent NGINX harness output-path authority

`FND-PARENT-0084` is `validated`, with its Parent task remediation
`in_progress`. Before any root-harness `mkdir`, install, `chown`, `chmod`,
`rm`, or output redirection, every generic/private bootstrap, parent
multi-case, and per-case work/output root must validate as a strict descendant
of `VERIFIED_RUN_ROOT`. The same authority gate constrains configurable
diagnostic, worker-preflight, protocol-artifact, lifecycle-evidence, and curl
response/error output paths. `/dev/null` is permitted only as the harness's
internal bounded-soak sink.

The sole deliberate exception is opt-in `NGINX_DOCROOT_PROJECTION=1`. Its
`NGINX_DOCROOT_PROJECTION_PARENT` is an explicit external parent supplied by a
trusted lifecycle/operator caller, outside the private runtime roots: it must
already exist, be root-owned, symlink-free, non-writable and non-readable by
group or other, and worker-traversable in a `0711`-safe form with traversable
ancestors. The harness validates those structural properties; it does not look
up or enforce lifecycle-manifest registration for either projection value.
`NGINX_DOCROOT_PROJECTION_ROOT` must be the exact fresh direct static child.
The projection helper validates the parent and creates only that child, copies
the allowlisted static files, and makes the child worker-traversable; generic
harness ownership/mode setup never `chown`s or `chmod`s the external parent.
No generic harness output is authorized there.

The retained receipt
`$RUN/evidence/nginx-harness-path-authority-remediation-20260801.md`
(SHA-256
`e1b09454d3dc823b78d83bdae960d431951b432cad57aa05df4434a8bd905c7b`)
records a real parent multi-case (`RUN_ONE_CASE=0`) negative control with
`LOG_DIR=/etc`: the harness exited `77` before normal runtime assertion, and
`/etc` remained mode `0755`, owner/group `0:0`, with no system output, NGINX
process, or listener created.

This receipt proves output-path authority only. The configurable `PYTHON` and
`PATH` launch model remains a trusted operator/CI assumption outside this
finding. Canonical runtime remains blocked, and the fresh C build validates
prior C code rather than this shell-harness control; the retained generic-path
receipt does not promote the new projection exception to canonical runtime
evidence. Neither replaces the final security scan or PR-head evidence.

### Retained pre-hardening H1 Memcheck diagnostic

The initial direct H1 Valgrind run observed one 8-byte `definitely lost`
allocation on the NGINX-core worker-exit path. It is not a connector or
ModSecurity security flaw. The exact generated stack was verified against an
independently SHA-verified official `nginx-1.31.2` archive (observed SHA-256
prefix/suffix `af2a957...473c`).

The retained pre-hardening direct H1 O7 artifact
`direct-nginx-h1-memcheck-suppressed-20260801T234500Z-c8d9e0f1` recorded a
clean result only within its then-current bounded diagnostic boundary:
`status=clean`, `complete=1`, `errors_detected=0`, `error_count=0`,
`definitely_lost_bytes=0`, `indirectly_lost_bytes=0`,
`possibly_lost_bytes=28160`, and `still_reachable_bytes=329918`. Its selected
connector-loaded benign case recorded `48` completed requests with
`request_failures=0`, `worker_summary_failures=0`, and `server_alive=1`. The
isolated lifecycle recorded `shutdown=graceful`, `wait=exited`,
`wrapper_exit_code=0`, and `containment=isolated`; no residual NGINX or
Valgrind process, `nginx.pid`, or test-port binding remained. Those historical
values are retained for provenance only and are not final proof after the
current root/worker and evidence-trust hardening.

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
mode after the root-run distinct-worker check and all three binary/archive
identity gates pass: the selected `NGINX_BINARY` equals
`$NGINX_PREFIX/sbin/nginx`; its `nginx -v` output is exactly
`nginx version: nginx/1.31.2`; and
`$NGINX_BUILD_DIR/verified-archives/nginx-1.31.2.tar.gz` has the
source-controlled SHA-256
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`.
Outside Memcheck mode, normal harness calls retain the existing
caller-selected `NGINX_BINARY` override behavior.

This retained diagnostic remains pre-hardening and noncanonical while canonical
provisioning/lifecycle containment and its worker-visible docroot projection
are in progress. It does not establish `runtime-smoke-nginx`, H2/H3, remote
CI, SonarQube, pull-request, or delivery success. The separate retained
remediation receipt above covers only the harness/evidence boundary with a
pre-current-C artifact. A separate fresh C build validated prior C code, but
neither receipt replaces the exact final security scan or final PR-head
CI/Sonar evidence.

## Supported Directives

The adapter-owned NGINX connector currently registers:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote` (rejected: remote rule loading is disabled by the common security policy)
- `modsecurity_transaction_id`
- `modsecurity_use_error_log on|off`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`
- `modsecurity_phase4_body_limit <bytes>`

`modsecurity_phase4_body_limit` defaults to 1048576 bytes (1 MiB). The
Common configuration validator rejects a selected value above 10485760 bytes
(10 MiB), so a native response filter cannot be configured with an unbounded
Phase-4 byte budget.

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

## Full-smoke pinned release provenance

The Parent full-smoke workflow builds the selected direct GitHub release asset
with this atomic tuple:

```sh
BUILD_NGINX_FROM_SOURCE=1
# Framework-synchronized NGINX release tuple; do not duplicate it here.
NGINX_REQUIRE_PINNED_PROVENANCE=1
```

It resolves the direct release-asset URL from the fixed repository, tag, and
asset name. The full-smoke resolver rejects `latest` and `/releases/latest`
before any cache, network, download, or extraction operation. Its cache
identity binds the complete provenance tuple, including the tag/ref equality
and SHA-256; later updates must change and review every tuple value atomically.
`NGINX_REQUIRE_PINNED_PROVENANCE=1` rejects inherited native binary/module
overrides, so a system or MRTS NGINX binary is not accepted as full-smoke
evidence.

A managed full-smoke runtime-evidence record must identify the release, ref,
and asset; expected and actual archive SHA-256 values; source version and
directory; binary path, SHA-256, and version readback; configure arguments;
build, Framework, and Parent identifiers; and generated time. This is the
required evidence schema, not a claim that a current runtime record exists.

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
Phase-4 facet evidence and is not an accepted full-smoke provenance setting.

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

The final-processing guard and body-ingestion guard use the same strict native
success contract: every relevant libmodsecurity call must return exactly `1`.
An ingestion failure, including a zero return, is a generic fail-closed
`500`/intervention path; it is not treated as a nonfatal `ProcessPartial`
limit decision. This preserves the Safe/Strict Phase-4 outcome model without
silently passing an incompletely ingested body to final processing.
