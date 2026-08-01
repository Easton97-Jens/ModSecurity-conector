# NGINX Connector Origin Map

**Language:** English | [Deutsch](ORIGIN.de.md)

Status: adapter-owned source migration complete

Local reference: `<external-source-root>/ModSecurity-nginx`
Upstream source: https://github.com/owasp-modsecurity/ModSecurity-nginx
Source branch: `master`
Source commit: `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`
Source describe: `v1.0.4-14-g9eb44fd`
License: Apache-2.0, retained in `licenses/nginx/LICENSE`
Default imported path: `connectors/nginx`

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-nginx | `<external-source-root>/ModSecurity-nginx` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

Central attribution: `licenses/nginx/`

## Adapter-Owned Source

NGINX now builds from a materialized source tree generated under
`$BUILD_ROOT/nginx-build/connector-src`. The module `config` is adapter-owned
at `connectors/nginx/config`, and productive module source is adapter-owned in
`connectors/nginx/src/`. The former
`connectors/nginx/upstream/` reference tree was removed in phase 10 after the
source migration, materialized-source build, and real NGINX smokes passed.

| Adapter-owned path | Original upstream path | Repo | Base commit | Extra provenance | License | Import reason |
| --- | --- | --- | --- | --- | --- | --- |
| `connectors/nginx/config` | `config` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX dynamic module build metadata |
| `connectors/nginx/src/ngx_http_modsecurity_access.c` | `src/ngx_http_modsecurity_access.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #384 `65de4cd8739209f22d924d85548bd012a4d94607`; PR #386 `a7fd4fcc18dc442b1b093d253f457b9317b7f588` | Apache-2.0 | NGINX access phase integration plus selected final-processing, ProcessPartial-compatible, address, and header-registration handling |
| `connectors/nginx/src/ngx_http_modsecurity_body_filter.c` | `src/ngx_http_modsecurity_body_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac`; PR #384 `65de4cd8739209f22d924d85548bd012a4d94607`; PR #385 `471a2a54843bb8f560758a7e75b146db2243ab29`; PR #386 `a7fd4fcc18dc442b1b093d253f457b9317b7f588`; Parent FND-PARENT-0080 | Apache-2.0 | NGINX response/body filter integration plus phase-4, final-processing, redirect-body replacement, terminal-loop handling, and restored bounded ingestion before connector-scope action mapping |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | `src/ngx_http_modsecurity_common.h` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac`; PR #385 `471a2a54843bb8f560758a7e75b146db2243ab29` | Apache-2.0 | Shared NGINX connector declarations plus phase-4 fields and response-replacement state |
| `connectors/nginx/src/ngx_http_modsecurity_header_filter.c` | `src/ngx_http_modsecurity_header_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #384 `65de4cd8739209f22d924d85548bd012a4d94607`; PR #385 `471a2a54843bb8f560758a7e75b146db2243ab29`; PR #386 `a7fd4fcc18dc442b1b093d253f457b9317b7f588` | Apache-2.0 | NGINX header filter integration plus selected intervention, protocol/header, redirect, and registration hardening |
| `connectors/nginx/src/ngx_http_modsecurity_log.c` | `src/ngx_http_modsecurity_log.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX log phase integration |
| `connectors/nginx/src/ngx_http_modsecurity_module.c` | `src/ngx_http_modsecurity_module.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac`; PR #384 `65de4cd8739209f22d924d85548bd012a4d94607`; PR #385 `471a2a54843bb8f560758a7e75b146db2243ab29` | Apache-2.0 | NGINX module entrypoint/config plus phase-4 directives, transaction lifecycle, and redirect-response handling |
| `connectors/nginx/src/ddebug.h` | `src/ddebug.h` | repo-owned compatibility header | n/a | replaces imported upstream debug helper | Apache-2.0-compatible project code | Keeps the NGINX module build dependency satisfied without retaining the imported debug helper in `upstream/` |
| `connectors/nginx/metadata.c` | n/a | repo-owned adapter metadata | n/a | none | Apache-2.0-compatible project code | Report/build-summary origin metadata |
| `connectors/nginx/metadata.h` | n/a | repo-owned adapter metadata | n/a | none | Apache-2.0-compatible project code | Report/build-summary origin metadata |
| `connectors/nginx/SOURCE_MAP.json` | n/a | repo-owned provenance manifest | n/a | records base, PR #377, selected PRs #384--#386, scoped #387/#388/#389 disposition, and Parent/Finding evidence boundaries | Apache-2.0-compatible project metadata | Source migration and PR provenance map |

## Phase 13 Layout Moves

| Former path | Current path | Materialized path |
| --- | --- | --- |
| `connectors/nginx/src/config` | `connectors/nginx/config` | `config` |
| `connectors/nginx/src/metadata.*` | `connectors/nginx/metadata.*` | not materialized |
| `connectors/nginx/src/SOURCE_MAP.json` | `connectors/nginx/SOURCE_MAP.json` | not materialized |
| `connectors/nginx/src/README.md` | `connectors/nginx/README.md` and docs | not materialized |

## PR #377 Intake

PR: https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377

Observed PR head commit: `3d72b004ff27a78ea19c6b945870e2cae62a97ac`

The PR source changes were applied only to adapter-owned NGINX source files:

- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_module.c`

The imported PR tests/docs were not copied into the active smoke suite.
Phase-4 / `RESPONSE_BODY` remains non-promoted; the focused NGINX-only evidence
recorded below does not add `RESPONSE_BODY` to `verified_variables` or replace
a separate Apache+NGINX real-world promotion.

## Selective PR #384--#387 Intake

The imported base remains `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`, and
the earlier local PR #377 provenance remains
`3d72b004ff27a78ea19c6b945870e2cae62a97ac`. The following upstream material
is selectively adapted into the adapter-owned Parent source; it is not a
claim that the upstream pull requests are merged or that their test evidence
ran in this repository.

| Upstream input | Observed head | Parent selection |
| --- | --- | --- |
| [PR #384](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/384) | `65de4cd8739209f22d924d85548bd012a4d94607` | Retains fail-closed handling for unambiguous final request/response processing and unsafe intervention failures. `msc_append_request_body()`, `msc_request_body_from_file()`, and `msc_append_response_body()` remain nonfatal because `ProcessPartial` uses the same return signal for by-design truncation; the subsequent final processing remains responsible for inspection. |
| [PR #385](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/385) | `471a2a54843bb8f560758a7e75b146db2243ab29` | Selects response-header fidelity and Phase-3 redirect replacement: retain `Location`, clear discarded entity metadata, and drain the replaced body. The Parent task additionally suppresses fictitious synthetic `Connection`/`Keep-Alive` headers for native HTTP/3, alongside the selected negotiated-protocol mapping; this is task-local hardening, not live HTTP/3 evidence. |
| [PR #386](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/386) | `a7fd4fcc18dc442b1b093d253f457b9317b7f588` | Selects value-free warning visibility for header-registration failure, empty-address guarding, and a terminal body-filter stop that still forwards the remaining NGINX chain. |
| [PR #387](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/387) | `4c1f0362ca0f25ef216ce59cad5fa6c9703c1438` | Selects the test-design direction for a Parent-owned opt-in bounded native soak (`make soak-nginx`) and opt-in H1 Memcheck diagnostic (`make memcheck-nginx`) through the existing harness. Both remain outside default smoke/test/CI and write bounded payload-free summaries. The source-controlled soak selector permits from one to eight unique IDs from its explicit canonical catalog and rejects empty, duplicate, or noncatalog selections before case discovery. Upstream Dockerfiles, workflows, Valgrind/Helgrind configuration, and soak tooling are not imported. The direct H1 post-suppression diagnostic below is clean only within its bounded noncanonical scope; no canonical Memcheck, Helgrind, or soak success is asserted. |

### Parent Phase-4 content-type ingestion restoration

This task restores a pre-task Parent regression in the body filter: bounded
response bytes reach ModSecurity irrespective of configured connector
Content-Type scope. Scope is applied when mapping a detected intervention; an
out-of-scope intervention becomes `log_only` with
`content_type_not_in_scope`. The repair does not weaken the selected #384
final-processing boundary: a final `msc_process_response_body()` result other
than `1` remains fail-closed, while `ProcessPartial` append/from-file behavior
remains intentionally nonfatal.

Focused task evidence is deliberately narrower than promotion evidence. The
strict isolated rebuild and C17, C23, and c2y passed; the newly materialized
build-source SHA matched the task filter; and the selected native
no-CRS/no-MRTS H1 out-of-scope case passed. The task-worktree correction is
not canonical finding closure: FND-PARENT-0080 remains recorded as
`validated` because current `master` retains the earlier behavior. This origin
map neither closes it nor asserts a final integrated task head.

The selected Parent Safe/Strict outcomes were also observed: Safe retained
`log_only` with the already-visible status unchanged, and Strict used
`abort_connection` after commitment. The full selected runner still exits
nonzero because read-only Framework fixture assertions expect the Safe mode as
the reason and jointly expect a stable `403`/obsolete action despite the
Strict connection abort. FND-FRAMEWORK-0058 is therefore `blocked` and
`out_of_scope` here; no Framework change is asserted.

The Phase-4 modes remain unchanged by this intake: Safe late handling records
`log_only` with the already-visible status unchanged, while Strict late
handling uses `abort_connection` rather than fabricating a second response.
The focused H1 observations above do not establish canonical lifecycle,
transport, or broad promotion evidence.

### Direct H1 Memcheck evidence and local suppression

The initial direct H1 Valgrind Memcheck diagnostic observed one 8-byte
`definitely lost` NGINX-core worker-exit allocation. It is not a connector or
ModSecurity security finding. The exact generated stack was verified against
an independently SHA-verified official `nginx-1.31.2` archive (observed
SHA-256 prefix/suffix `af2a957...473c`).

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

`connectors/nginx/harness/valgrind-nginx-core-1.31.2.supp` is a local,
source-controlled task file; it is not copied from upstream. It matches only
`Memcheck:Leak` with `match-leak-kinds: definite` and this exact NGINX-core
stack:

```text
malloc -> ngx_alloc -> ngx_set_environment -> ngx_worker_process_init
-> ngx_worker_process_cycle -> ngx_spawn_process
-> ngx_start_worker_processes -> ngx_master_process_cycle -> main
```

The artifact records `suppressed: 1 from 1`. Possible losses remain visible in
the payload-free summary, rather than being suppressed. A changed stack, a
connector/libmodsecurity diagnostic, or an invalid-access diagnostic cannot
match this local suppression and remains a failing Memcheck result.

This source-controlled suppression is used only in opt-in `NGINX_MEMCHECK=1`
mode after all three runtime identity gates pass: the selected `NGINX_BINARY`
equals `$NGINX_PREFIX/sbin/nginx`; its `nginx -v` output is exactly
`nginx version: nginx/1.31.2`; and
`$NGINX_BUILD_DIR/verified-archives/nginx-1.31.2.tar.gz` has the
source-controlled SHA-256
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`.
Outside Memcheck mode, normal harness calls retain the existing
caller-selected `NGINX_BINARY` override behavior.

This direct H1 diagnostic remains noncanonical. Canonical provisioning and
lifecycle containment, including the worker-visible docroot projection, remain
in progress; therefore this direct result does not establish
`runtime-smoke-nginx`, H2/H3, remote-rule, remote-CI, SonarQube, pull-request,
or delivery success.

## Scope Separation

- [#388](https://github.com/owasp-modsecurity/ModSecurity-nginx/issues/388) is
  `not_applicable` to this Parent adapter-source intake.
- [PR #389](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/389)
  is `out_of_scope` for this Parent-only NGINX connector task.

## Durable Attribution Files

| Attribution path | Original path | Repo | Commit | License | Import reason |
| --- | --- | --- | --- | --- | --- |
| `licenses/nginx/LICENSE` | `LICENSE` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | License text for NGINX-derived adapter source |
| `licenses/nginx/AUTHORS` | `AUTHORS` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream attribution |
| `licenses/nginx/CHANGES` | `CHANGES` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream change context |

## Excluded Upstream Files

The NGINX test harness, `.git`, `.github`, CI files, release scripts, Windows
build files, raw upstream tests, and build/runtime artifacts are not imported.
In particular, the upstream PR #387 Dockerfiles, workflow, Valgrind/Helgrind
configuration, and soak script remain upstream-only.
The previous upstream `config` and `src/*` files were migrated to
`connectors/nginx/src/`; the former `connectors/nginx/upstream/` directory was
removed after passing materialized-source NGINX smokes.

## Central Attribution Copies

The NGINX upstream `LICENSE`, `AUTHORS`, and `CHANGES` files are mirrored under
`licenses/nginx/` for repository-level license review. The central license
directory is the durable attribution source; this origin map records how those
files relate to the adapter-owned source tree.

## Pruning Review

The Framework's current [connector integration guide](../../modules/ModSecurity-test-Framework/docs/connector-integration.md)
records the applicable source/catalog boundary.

`connectors/nginx/upstream/` was removed in phase 10. Future NGINX source
reductions should update `connectors/nginx/SOURCE_MAP.json`,
`licenses/nginx/`, and this origin map, then prove `smoke-nginx` and
`smoke-all` still pass.
