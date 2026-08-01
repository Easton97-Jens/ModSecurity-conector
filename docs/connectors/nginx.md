# NGINX Connector

**Language:** English | [Deutsch](nginx.de.md)

## Overview

NGINX uses the selected <code>native-nginx-http-module</code> route. The
dynamic HTTP module maps NGINX request/response state to libmodsecurity v3
through connector-owned phases and filters. This guide covers the selected
HTTP/1.1 P1--P4 core only and makes no production, CRS, complete-matrix,
HTTP/2, HTTP/3, or strict-for-all-connectors claim.

## Architecture and ownership

Productive source lives under <code>connectors/nginx/src/</code>; module build
metadata is under <code>connectors/nginx/config</code>. NGINX owns main/location
configuration create/merge, access and log phases, header/body filters,
subrequest/end-of-stream treatment, dynamic module loading, and host action
mapping. Common provides neutral configuration, parser, mapping, limit, event,
and metadata contracts without owning <code>ngx_http_request_t</code> or an
NGINX filter.

| Lifecycle area | Selected NGINX responsibility | Boundary |
| --- | --- | --- |
| P1/P2 | Access-phase request mapping and body completion | Do not finalize a body before its selected end-of-stream |
| P3 | Response header filter mapping | Determine pre-commit state from the host response |
| P4 | Bounded body-filter ingestion and one-time EOS finalization | Preserve actual action and visible status after commitment |
| Logging | Payload-free event/result metadata | JSON/event truncation is distinct from body truncation |

## Selective upstream intake

The Parent-owned connector remains based on ModSecurity-nginx
`9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` with its earlier local PR #377
overlay `3d72b004ff27a78ea19c6b945870e2cae62a97ac`. The current source intake is
selective and recorded in [the origin map](../../connectors/nginx/ORIGIN.md):

- [PR #384](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/384)
  at `65de4cd8739209f22d924d85548bd012a4d94607` keeps unambiguous final body
  processing fail-closed without converting `ProcessPartial` append/from-file
  truncation into a generic failure.
- [PR #385](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/385)
  at `471a2a54843bb8f560758a7e75b146db2243ab29` supplies selected
  response-header and redirect-replacement handling. The Parent task also
  excludes fictional synthetic `Connection`/`Keep-Alive` fields for native
  HTTP/3 as task-local hardening.
- [PR #386](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/386)
  at `a7fd4fcc18dc442b1b093d253f457b9317b7f588` supplies selected
  header-registration visibility, address, and body-loop handling.
- [PR #387](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/387)
  at `4c1f0362ca0f25ef216ce59cad5fa6c9703c1438` informs the Parent-owned
  opt-in bounded native soak (`make soak-nginx`) and H1 Memcheck diagnostic
  (`make memcheck-nginx`). Both remain outside default smoke/test/CI and write
  bounded payload-free summaries. The source-controlled soak selector permits
  from one to eight unique IDs from its explicit canonical catalog and rejects
  empty, duplicate, or noncatalog selections before case discovery; no upstream Docker, workflow,
  Valgrind/Helgrind configuration, or runtime result is imported or claimed.

The focused task evidence includes a strict isolated rebuild, passed C17/C23/
c2y checks, a newly materialized build-source SHA matching the task filter, and
a passed selected native no-CRS/no-MRTS H1 out-of-scope case. It does not claim
canonical lifecycle, HTTP/2, HTTP/3, remote-rule, soak, a canonical Memcheck,
Helgrind, or delivery success.

## Build

Use [the NGINX compiler guide](../build/compilers/nginx.md) for source build,
dynamic-module inputs, component roots, and diagnostics. Required C17 checks
are structural/compile evidence; optional newer-language probes do not imply
runtime verification. The [NGINX source guide](../../connectors/nginx/README.md)
remains the code-adjacent entry point.

For this task, the strict isolated rebuild and C17, C23, and c2y passed; the
new materialized build-source SHA matched the task filter. That observed build
evidence does not replace a canonical lifecycle run or a final exact-head
proof.

## Configuration

The complete NGINX syntax, values, defaults, contexts, merge behavior,
validation guidance, and profile examples are in the
[NGINX configuration reference](../../examples/nginx/configuration-reference.md).
Use NGINX variables only where the registered directive documents them.
<code>modsecurity_transaction_id_expr</code> is Apache-specific and is not an
NGINX directive.

## P1--P4 lifecycle and protocol boundary

P3 decisions belong to the response-header path before headers are committed.
The response-body filter is a separate P4 timing model. A P4 rule match does
not make a visible 403, abort, HTTP/2, or HTTP/3 result without the corresponding
host/client artifacts.

The task restores a pre-task Parent content-type ingestion regression: bounded
response bytes reach ModSecurity irrespective of connector Content-Type scope.
Scope is applied only when a detected intervention is mapped, so an out-of-
scope intervention becomes <code>log_only</code> with
<code>content_type_not_in_scope</code>. This preserves the selected #384
boundary: final <code>msc_process_response_body()</code> with a result other
than <code>1</code> remains fail-closed, whereas append/from-file
<code>ProcessPartial</code> behavior remains intentionally nonfatal.

At source level, a pre-commit redirect preserves its `Location` header,
discards obsolete entity metadata, and causes the body filter to drain the
replaced response body. A terminal P4 finalization guard stops reinspection but
still forwards the remaining NGINX chain. Neither statement is a client-visible
redirect, body-filter, Safe, or Strict runtime result.

| P4 question | Required observation |
| --- | --- |
| Rule observed | Selected native rule and phase-4 metadata |
| Pre-commit deny | A host path that is actually pre-commit for the selected response |
| Safe late result | Requested action, actual <code>log_only</code>, unchanged visible status, and late flag |
| Strict late result | Actual abort action, retained already-visible status, and client/host evidence |

The selected native no-CRS/no-MRTS H1 out-of-scope case passed. The selected
Parent Safe/Strict outcomes were observed as Safe <code>log_only</code> with
unchanged visible status and Strict post-commit <code>abort_connection</code>.
The full selected runner nevertheless exits nonzero because read-only Framework
fixtures contradict those contracts: Safe expects the mode as its reason, and
Strict jointly expects a stable <code>403</code>/obsolete action despite the
connection abort. This is `FND-FRAMEWORK-0058` (`blocked`, `out_of_scope`); no
Framework edit is asserted and the observations do not promote the result to a
canonical lifecycle pass.

An HTTP/2 or HTTP/3 build flag is not transport evidence. Source-level
negotiated-version mapping and omission of synthetic HTTP/1.x hop-by-hop
headers do not establish a host transport result. Where a host run records an
HTTP/2 or HTTP/3 applicability artifact, an unavailable feature remains not
applicable and an unexecuted protocol case remains not executed.

## Testing and evidence

Use <code>make check-config-nginx</code> for configuration validation and
<code>make full-lifecycle-nginx</code> for a selected native host run. Inspect
the selected run ID's result, event, effective configuration, host version,
and protocol applicability artifacts. The shared model is documented in
[Testing and evidence](../testing-and-evidence.md).

Canonical lifecycle containment and its narrow worker-visible docroot
projection are still in progress under `FND-PARENT-0078`. Therefore this guide
does not report <code>runtime-smoke-nginx</code>, soak, canonical Memcheck,
H2/H3, remote-CI, SonarQube, pull-request, or delivery success.

### Direct H1 Memcheck diagnostic boundary

The initial direct H1 Valgrind Memcheck diagnostic observed an 8-byte
`definitely lost` allocation on the NGINX-core worker-exit path. It is not a
connector or ModSecurity security flaw. The exact generated stack was verified
against an independently SHA-verified official `nginx-1.31.2` archive
(observed SHA-256 prefix/suffix `af2a957...473c`).

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

The local source-controlled
[`valgrind-nginx-core-1.31.2.supp`](../../connectors/nginx/harness/valgrind-nginx-core-1.31.2.supp)
is not copied from upstream. It matches only a definite `Memcheck:Leak` with
the exact NGINX-core chain `malloc -> ngx_alloc -> ngx_set_environment ->
ngx_worker_process_init -> ngx_worker_process_cycle -> ngx_spawn_process ->
ngx_start_worker_processes -> ngx_master_process_cycle -> main`. The artifact
records `suppressed: 1 from 1`. Possible losses remain reported in the
payload-free summary rather than being suppressed. A changed stack, connector
or libmodsecurity diagnostic, or invalid-access diagnostic does not match and
remains failing.

The source-controlled suppression is used only in opt-in `NGINX_MEMCHECK=1`
mode after all three runtime identity gates pass: the selected `NGINX_BINARY`
equals `$NGINX_PREFIX/sbin/nginx`; its `nginx -v` output is exactly
`nginx version: nginx/1.31.2`; and
`$NGINX_BUILD_DIR/verified-archives/nginx-1.31.2.tar.gz` has the
source-controlled SHA-256
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`.
Outside Memcheck mode, normal harness calls retain the existing
caller-selected `NGINX_BINARY` override behavior.

This is noncanonical diagnostic evidence: it does not bypass the
`FND-PARENT-0078` provisioning/lifecycle block or establish a runtime-smoke,
H2/H3, remote-rule, remote-CI, SonarQube, pull-request, or delivery result.

## Operations and troubleshooting

Use an external build/runtime/evidence root. For a module/configuration error,
inspect the source build inputs, dynamic module compatibility, and config-check
output. For P4 or protocol questions, inspect the response filter's recorded
commit/EOS context rather than extrapolating from a source option or an HTTP
status alone.

## Limitations and compatibility

NGINX syntax, contexts, inheritance, and expression semantics are
host-specific. Do not copy Apache expression directives into NGINX. Response-
body, strict late action, first-byte, no-full-buffer, and protocol properties
remain individually evidence-gated. The opt-in bounded native soak and H1
Memcheck diagnostic are source-wired lifecycle probes when run, not a
leak-freedom or transport claim; native execution remains separately required.
`FND-PARENT-0080` remains `validated` in canonical Parent tracking because
current `master` retains the earlier in-scope ingestion behavior; the
task-worktree correction still requires final current-head proof.
`FND-PARENT-0078` remains in progress.

## Related references

- [Architecture](../architecture.md)
- [Configuration](../configuration.md)
- [Operations and security](../operations-and-security.md)
- [NGINX configuration reference](../../examples/nginx/configuration-reference.md)
