# P1–P4 connector parity: current-master baseline and execution plan

**Language:** English | [Deutsch](p1-p4-connector-parity-baseline.de.md)

## Purpose, scope, and evidence boundary

This report is the code-near baseline for the user-requested P1–P4 parity
program. It records the observed state of Parent `master` at
`6ccfd8de555855ac540fc4d3d9e330f82d5e8cff` on 2026-08-26 and defines the
work needed to reach the requested end state. It is not a claim that the
program is complete.

The selected scope is the ten Parent connector paths: Apache, NGINX, HAProxy
HTX, HAProxy SPOE/SPOP, Envoy ext_authz, Envoy ext_proc, Traefik forwardAuth,
Traefik Native UDS, Stock lighttpd, and Patched lighttpd. CI workflows,
branch rules, required checks, Framework/MRTS source, Gitlinks, and hosted
test configuration are outside scope. This report is based on current-source,
capability-file, harness, and documentation inspection; no connector build or
real-host P1–P4 matrix run is asserted here.

The common evidence model requires more than an HTTP status: a run must bind
the rule ID, connector event, requested decision, observed host action, and
cleanup result to one transaction. Bodies are represented only by bounded
metadata, digests, lengths, and EOS state; raw body payloads must not be
written to event JSONL.

## Canonical phase contract

`common/include/msconnector/phase.h` and
`common/rules/p1_p4_traffic_vectors.json` define the repository meanings of
the four phases:

| Phase | Canonical point | Current vector rule IDs |
| --- | --- | --- |
| P1 | Request headers | `1101001` |
| P2 | Actual request body, finalized at EOS | `1102001`, `1102002` |
| P3 | Upstream response headers | `1103001` |
| P4 | Response body, finalized at EOS | `1104001`, `1104002`, `1104003` |

The target contract must preserve this ordering and the common decision kinds,
limits, timeout semantics, fail mode, deterministic cleanup, and correlation
fields. In particular, a P4 Safe decision may be recorded as `log_only`; P4
Strict needs a deterministic, client-visible real-host outcome and cannot be
inferred merely from a driver-side abort or reset.

## Current implementation and evidence matrix

Every row below is below the requested `fully_runtime_verified` state. A
source-side implementation or harness entry point is not equivalent to a
canonical runtime proof.

| Connector path | Source and local entry points | Observed P1–P4 state | Required work before acceptance |
| --- | --- | --- | --- |
| Apache | `connectors/apache/src/mod_security3.c`, `connectors/apache/src/msc_filters.c`; `connectors/apache/Makefile.am`; `connectors/apache/harness/run_apache_smoke.sh` | P1–P4 adapters exist but capabilities state `implemented_not_asserted`. | Produce canonical real-host P1–P4 Safe/Strict evidence; implement and prove client/upstream abort handling, currently `not_implemented`. |
| NGINX | `connectors/nginx/src/ngx_http_modsecurity_module.c`, access/header/body filter adapters; `connectors/nginx/harness/run_nginx_smoke.sh` | P1–P4 adapters exist but are `implemented_not_asserted`; P4 is subject to late-intervention constraints after response headers. | Prove real-host P1–P4 Safe/Strict behavior and close client/upstream-abort and pre-commit P4-deny gaps without weakening the master/worker model. |
| HAProxy HTX | `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`; `connectors/haproxy/Makefile`; `connectors/haproxy/harness/run_haproxy_htx_runtime.sh` | P1–P3 are exercised by local harness cases; P4 is observed after forwarding, Safe resolves `log_only`, and Strict has no host action. | Create a pre-commit response-body enforcement design and prove client-visible Strict behavior, errors, follow-up traffic, and cleanup. |
| HAProxy SPOE/SPOP | `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`, `connectors/haproxy/src/haproxy_modsecurity_binding.c`; `connectors/haproxy/Makefile`; `connectors/haproxy/harness/run_haproxy_smoke.sh` | P1/P2 and optional P3 headers exist; P4 response-body handling and Safe/Strict support are `not_implemented`. | Add a response-body-capable path, bounded server-side I/O, disconnect handling, and complete P4/error/cleanup proof. |
| Envoy ext_authz | `connectors/envoy/src/envoy_ext_authz_service_main.c` through `common/runtime/http_authorization_service.c`; `connectors/envoy/Makefile`; `connectors/envoy/config/envoy-ext-authz.conf` | Request authorization is available; buffered P2 is configuration-dependent; P3/P4 are unavailable to this pre-upstream protocol. | Provide and test one response-capable companion or combined path. It must be one end-to-end connector solution, not a permanent `not_applicable` exception. |
| Envoy ext_proc | `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go`, `internal/processor/common_runtime_engine.go`; `connectors/envoy/Makefile`; `config/envoy-ext-proc-streaming.yaml.in` | P1–P4 streaming wiring exists; post-commit Safe is `log_only`; Strict abort is explicitly not attempted. | Define and prove deterministic client-visible Strict behavior, server-side idle bounds, all error paths, subsequent traffic, and cleanup. |
| Traefik forwardAuth | `connectors/traefik/src/traefik_forwardauth_service_main.c` through `common/runtime/http_authorization_service.c`; `connectors/traefik/Makefile`; `connectors/traefik/config/traefik-forwardauth.conf` | P1 exists; the standard profile has `request_body_mode=none`; P3/P4 cannot be seen by pre-upstream forwardAuth. | Add a response-capable companion or combined path and prove full P1–P4, Safe/Strict, errors, and cleanup as one connector solution. |
| Traefik Native UDS | `connectors/traefik/native_middleware/middleware.go`, `engine_uds.go`; `connectors/traefik/Makefile`; `connectors/traefik/scripts/runtime-native-middleware.sh` | P1–P4 source wiring exists; post-commit Safe is `log_only`; Strict abort is `NOT EXECUTED`. | Prove deterministic Strict outcome plus engine-down, invalid-response, disconnect, follow-up, and cleanup behavior with a real host. |
| Stock lighttpd | `connectors/lighttpd/module/mod_msconnector.c`; `connectors/lighttpd/Makefile`; `connectors/lighttpd/build/build_module.sh` | P1 and response-header wiring exist; the selected Stock ABI has `request_body_mode=none` and no response-body hook. | Choose an ABI-correct full-body strategy; the current Stock path cannot meet universal P2/P4 acceptance without a supported response-capable solution. |
| Patched lighttpd | `connectors/lighttpd/module/mod_msconnector.c`; `connectors/lighttpd/patches/0001-lighttpd-msconnector-stream-hooks.patch`; `connectors/lighttpd/Makefile` | P1–P4 source hooks exist, with post-commit Safe source wiring; Strict is `NOT EXECUTED`. | Supply canonical real-host P1–P4/Safe/Strict, first-byte, disconnect/abort, follow-up, and cleanup evidence. |

The cross-connector harnesses and evidence rules are rooted in
`connectors/composite_harness/`, while `docs/testing-and-evidence.md` defines
the separation between static claims and run-bound evidence. The current
coverage report has no `runtime_verified=true` complete matrix; its existing
results are not a promotion of the ten-path P1–P4 goal.

## Shared work packages and dependencies

1. **Reconcile the source ownership first.** Open Draft PRs #344, #345, and
   #346 overlap the common contract, connector implementations, and failure
   cleanup needed here. This branch is intentionally based on current
   `master` and does not copy, merge, rebase, or claim the unmerged work.
   A user-approved integration or supersession decision is required before
   competing source edits begin.
2. **Make the common contract authoritative.** Align transaction state,
   decision-to-event mapping, phase ordering, bounded request/response
   metadata, timeouts, fail-open/fail-closed policy, and cleanup receipt
   schema. The existing `FND-PARENT-0234` concern—an event claiming host
   action before host confirmation—remains release-blocking until a
   source-and-runtime fix is verified.
3. **Close architectural phase gaps.** Implement response-capable combined
   paths for Envoy ext_authz and Traefik forwardAuth; design a full
   response-body path for SPOE/SPOP and an ABI-correct solution for Stock
   lighttpd. These paths cannot remain `not_applicable` under the requested
   universal goal.
4. **Standardize Safe and Strict.** Preserve Safe as explicit post-commit
   observation where intervention is no longer possible. For Strict, define
   the earliest enforceable point and prove the resulting host/client
   transport behavior rather than accepting a connector-local reset as proof.
5. **Normalize failures and resource lifecycle.** For every path, prove engine
   down, timeout, malformed response, client disconnect/cancel, a valid
   subsequent request, and cleanup of processes, ports, UDS paths, streams,
   and task-owned artifacts.
6. **Promote only run-bound evidence.** Each path must separately build,
   validate configuration, start/readiness-check a real host, run Allow, P1,
   P2 with an actual body, P3, P4 Safe, P4 Strict, every required failure
   case, and cleanup. Only then may its status become
   `fully_runtime_verified`.

## Security review baseline

No new validated finding is created by this static baseline. The existing
`FND-PARENT-0234` is retained rather than duplicated. Focused source review
also identified three plausible HAProxy SPOP candidates that require runtime
validation before finding creation or remediation claims: blocking peer I/O
despite a parsed timeout option, a peer-disconnect `SIGPIPE`/`EPIPE` path, and
header-count validation that may log a mapping error without rejecting the
transaction. The chosen defaults bind SPOP to loopback, which limits but does
not remove the need to test those paths. No security control, logging bound,
or cleanup check is weakened by this documentation milestone.

## Acceptance and next execution gate

The final program is accepted only when every listed connector path has one
real-host evidence bundle for Build, configuration, readiness, Allow, P1, P2,
P3, P4 Safe, P4 Strict, engine down, timeout, invalid response, disconnect or
cancel, follow-up traffic, and cleanup—with correlation fields that prove the
actual host action. There may be no `not_run`, `not_applicable`,
`partially_runtime_verified`, or `failed_build` cell in that final matrix.

This milestone completes Prompt 1's baseline analysis and prioritized plan;
it does not begin broad source refactoring. The next source milestone is
blocked only by the overlapping unmerged PR ownership decision, not by a claim
that the missing capabilities are unsupported. An isolated task-owned local
storage preflight has passed for future builds and runtime evidence; no build,
host process, or local connector-runtime matrix has been started in this
documentation-only change.
