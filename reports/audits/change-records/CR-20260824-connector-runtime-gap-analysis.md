# Change Record CR-20260824: Connector runtime-verification gap analysis

**Language:** English | [Deutsch](CR-20260824-connector-runtime-gap-analysis.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260824-connector-runtime-gap-analysis` |
| Date (UTC) | `2026-08-24` |
| Base revision | `a6b4ced4876a19666f7c7203ed9e719674c69ec1` |
| Retained runtime-evidence revision | `232b020cac23d5edc0e18adaf502468bb3012237` |
| Scope | Parent-only EN/DE documentation of a read-only, code-near gap analysis for ten connector paths. No product, connector, test, harness, workflow, CI, governance, dependency, toolchain, Framework, MRTS, Gitlink, or runtime-host change. |
| Delivery boundary | One documentation-only branch and Draft PR. No merge, bypass, protection/ruleset change, or check manipulation is authorized. |

## Motivation and problem statement

The requested target is `fully_runtime_verified` for Apache, NGINX, HAProxy
HTX, HAProxy SPOE/SPOP, Envoy ext_authz, Envoy ext_proc, Traefik forwardAuth,
Traefik Native UDS, lighttpd Stock, and lighttpd Patched. The retained evidence
does not establish that target for any of the ten paths.

This record preserves the source-defined phase model, source/evidence boundary,
current and target matrices, implementation backlog, dependencies, and open
architecture decisions. It never promotes a source capability, a build result,
or a retained historical host run into a current full-runtime pass.

## Acceptance criteria

- Preserve repository-defined P1, P2, P3, and P4 semantics.
- Cover all ten paths with source ownership, host/build/config/start/process
  evidence, phase/error/lifecycle evidence, and current status.
- Provide equivalent current-state and target-state matrices.
- Provide a prioritized backlog, dependencies, exact source anchors, shared and
  host-specific work, per-connector acceptance, risks, and open decisions.
- Explain the response-capable companion required by Envoy ext_authz and
  Traefik forwardAuth rather than treating P3/P4 as permanently
  `not_applicable`.
- State all unrun builds, host runs, strict-intervention checks, and error-path
  checks honestly.
- Change only this English/German Change Record pair and the English/German
  archive-index entries.

## Evidence boundary and status convention

The source analysis applies to base revision
`a6b4ced4876a19666f7c7203ed9e719674c69ec1`. Retained build/runtime reports
use `232b020cac23d5edc0e18adaf502468bb3012237`; they do not prove a newer
source tree.

| Symbol | Meaning |
| --- | --- |
| `✓M` | Retained real-host result in the supplied matrix. |
| `src` | Current-base source inspection only, not a runtime pass. |
| `NR` | Applicable evidence was not run or is insufficient. |
| `B` | Concrete retained block or failure. |
| `—` | Structurally unavailable in the selected path; a target gap, not a universal exemption. |
| `H` | Target requires a host-confirmed connection abort or stream reset. |
| `C-V` | Target verification requires the named response-capable composite. |

`Cleanup ✓M` means retained harness process teardown only. It does not prove
timeout, disconnect, error, or follow-up cleanup.

## Canonical phase semantics

The authoritative semantics are in `common/include/msconnector/phase.h`,
`common/runtime/msconnector_runtime.c`, `examples/common/rule-examples.md`,
and `common/rules/modsecurity_p1_p4_vectors.conf`.

| User phase | Meaning | Canonical vector |
| --- | --- | --- |
| P1 | Request headers | `1101001` |
| P2 | Request body through request EOS | `1102001` |
| P3 | Response headers before/at response commit | `1103001` |
| P4 | Response body through response EOS | `1104001`, `1104002`, `1104003` |

`CONNECTION` and `URI` are internal preceding runtime steps, not a
redefinition of P1. P4 Safe preserves a truthful client-visible response after
commit and records a non-disruptive/log-only outcome. P4 Strict is verified
only when the host actually performs and reports the requested abort/reset.

## Source flow and ownership map

| Connector | Source flow | Current boundary |
| --- | --- | --- |
| Apache | `mod_security3.c` request hooks → `msc_filters.c` request/response filters → Common runtime → host action/event/cleanup | P1–P4 source paths exist; Strict/error host proof is incomplete. |
| NGINX | `ngx_http_modsecurity_access.c` → request-body callback → header filter → body filter | Retained result is single-process sandbox, not normal Master/Worker. |
| HAProxy HTX | `haproxy_modsecurity_htx_filter.c`: begin, request payload, response headers, response payload, finish | `report_late_decision` is not demonstrated Strict host action. |
| HAProxy SPOE/SPOP | `haproxy_spop_diagnostic_runtime.c`: `accept_loop` → HELLO/frames/cache → reply/disconnect | Serial blocking accept/read and peer-close handling block robust lifecycle proof. |
| Envoy ext_authz | `envoy_ext_authz_service_main.c` → `http_authorization_service.c` → Begin/Decide/Finish/Destroy | Request-phase-only service never receives upstream response. |
| Envoy ext_proc | `processor.go`: `Service.Process`/`stream.Recv` → stream state → engine → gRPC response → close | Idle receive streams lack deadline/capacity proof. |
| Traefik forwardAuth | `traefik_forwardauth_service_main.c` → authorization service → forward-auth response | Request-only; current configuration does not forward request body. |
| Traefik Native UDS | `middleware.go` → `engine_uds.go` → `traefik_engine_service.c` → Common runtime | Source-confirmed P2-before-P3 ordering gap for early downstream responses. |
| lighttpd Stock | `mod_msconnector.c` and mapper → Common runtime | Build fails; Stock configuration disables request/response body modes. |
| lighttpd Patched | Stream-hook ABI → `handle_request_body`/`handle_response_body` → Common runtime | Source path exists; real host P2–P4 proof is incomplete. |

## Current-state matrix: source, host, and process

| Connector | Source | Retained host version | Build | Config | Start | Process model |
| --- | --- | ---:|---|---|---|---|
| Apache | `connectors/apache` | 2.4.66 | ✓M | ✓M | ✓M | httpd module; normal process detail NR |
| NGINX | `connectors/nginx` | 1.31.4 | ✓M | ✓M | ✓M | single-process sandbox ✓M; Master/Worker NR |
| HAProxy HTX | `connectors/haproxy/htx-overlay` | 3.2.22 | ✓M | ✓M | ✓M | in-host HTX filter |
| HAProxy SPOE/SPOP | `connectors/haproxy/src` | 3.2.22 | ✓M | ✓M | ✓M | external listener; serial accept/HELLO |
| Envoy ext_authz | `connectors/envoy/src` + Common | 1.39 | ✓M | ✓M | ✓M | Envoy plus TCP authorization service |
| Envoy ext_proc | `connectors/envoy/ext_proc` | 1.39 | ✓M | ✓M | ✓M | gRPC bidi; one transaction per stream |
| Traefik forwardAuth | `connectors/traefik/src` + Common | 3.7.11 | ✓M | ✓M | ✓M | Traefik plus request-only service |
| Traefik Native UDS | Native middleware and UDS service | 3.7.11 | ✓M | ✓M | ✓M | plugin plus UDS per request |
| lighttpd Stock | `connectors/lighttpd/module` | 1.4.85 | B: FND-GS-0001 | NR | NR | not started |
| lighttpd Patched | stream-hook patch and module | 1.4.85 | ✓M | ✓M | ✓M | patched stream hooks |

## Current-state matrix: runtime and lifecycle

| Connector | Allow | P1 | P2 | P3 | P4 Safe | P4 Strict | Engine down | Timeout | Invalid response | Disconnect/Cancel | Follow-up | Cleanup | Current status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | ✓M 200 | ✓M 403/r1001 | ✓M 403/r1200 | ✓M 403/r1301 | ✓M 200 Pass/Safe; correlation gap | NR | NR | NR | NR | NR | NR | ✓M | partial |
| NGINX | ✓M 200 | ✓M 403/r1000001 | NR | NR | NR | NR | NR | NR | NR | NR | NR | ✓M | partial |
| HAProxy HTX | ✓M 200 | ✓M 403/429 | ✓M 403 | ✓M 403 | ✓M 200 Log-only | NR | NR | NR | NR | NR | NR | ✓M | partial |
| HAProxy SPOE/SPOP | ✓M 200 | ✓M 403 | ✓M query 403 | NR | NR | NR | NR | NR | NR | B: SIGPIPE/EPipe | B after peer-close | ✓M, not error path | partial / security gap |
| Envoy ext_authz | ✓M 200 | ✓M 403/r1000001 | NR | — | — | — | NR | NR | NR | NR | NR | ✓M | partial, request-only |
| Envoy ext_proc | ✓M 200 | ✓M 403/302 | ✓M 403 | ✓M 403/302 | ✓M 200 Log-only | NR | NR | B: idle streams | NR | ✓M cancel | NR | ✓M | partial |
| Traefik forwardAuth | ✓M 200 | ✓M 403/r1000001 | — | — | — | — | NR | NR | NR | NR | NR | ✓M | partial, request-only |
| Traefik Native UDS | ✓M 200 | ✓M 403/429 | ✓M 403, ordering gap | ✓M 403 | ✓M 200 Log-only | NR | NR | src only | NR | NR | NR | ✓M | partial / P0 blocker |
| lighttpd Stock | NR | NR | — | NR | — | — | NR | NR | NR | NR | NR | NR | failed build |
| lighttpd Patched | ✓M 200 | ✓M 403/r1000001 | NR | NR | NR | NR | NR | NR | NR | NR | NR | ✓M | partial |

## Target-state matrix: source, host, and startup

| Connector | Source | Host version | Build | Config | Start/readiness | Required process model |
| --- | --- | --- | --- | --- | --- | --- |
| Apache | exact SHA and patch inventory | pinned | native pass | native validation | PID/listener/ready | real httpd |
| NGINX | exact SHA and patch inventory | pinned | native pass | native validation | PID/listener/ready | real Master/Worker |
| HAProxy HTX | exact overlay/host SHA | pinned | native pass | host config validation | PID/listener/ready | HTX filter in host |
| HAProxy SPOE/SPOP | exact SHA | pinned | native pass | SPOE/SPOP validation | agent and HAProxy ready | bounded concurrent connections |
| Envoy ext_authz | exact composite SHA | pinned | native pass | Envoy plus companion | both ready | ext_authz plus response observer |
| Envoy ext_proc | exact SHA | pinned | native pass | Envoy/gRPC validation | both ready | bounded gRPC streams |
| Traefik forwardAuth | exact composite SHA | pinned | native pass | forwardAuth plus observer | both ready | forwardAuth plus response observer |
| Traefik Native UDS | exact SHA | pinned | native pass | Traefik/UDS validation | plugin and UDS ready | no P3 before P2 EOS |
| lighttpd Stock | exact SHA and chosen host path | pinned | repaired native pass | repaired validation | real host ready | stream-capable Stock path or companion |
| lighttpd Patched | exact patch/host SHA | pinned | native pass | native validation | PID/listener/ready | patched stream hooks |

## Target-state matrix: runtime and lifecycle

`V` requires the same transaction's actual client result, rule ID, correlated
Common event, actual host action, and lifecycle evidence. `H` additionally
requires a host-confirmed abort/reset. A host lacking that primitive cannot
receive a full target pass until its integration changes.

| Connector | Allow | P1 | P2 | P3 | P4 Safe | P4 Strict | Engine down | Timeout | Invalid response | Disconnect/Cancel | Follow-up | Cleanup | Target status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| NGINX | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| HAProxy HTX | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| HAProxy SPOE/SPOP | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| Envoy ext_authz | V | V | V | C-V | C-V | C-H | V | V | V | V | V | V | `fully_runtime_verified` |
| Envoy ext_proc | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| Traefik forwardAuth | V | V | C-V | C-V | C-V | C-H | V | V | V | V | V | V | `fully_runtime_verified` |
| Traefik Native UDS | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| lighttpd Stock | V after repair | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |
| lighttpd Patched | V | V | V | V | V | H | V | V | V | V | V | V | `fully_runtime_verified` |

## Prioritized implementation backlog

| Priority | Package | Source anchors | Required result |
| --- | --- | --- | --- |
| P0 | Native UDS P2-before-P3 ordering | `middleware.go`: `Middleware.ServeHTTP`, `streamState.processResponseHeaders`, `processBody`; `engine_uds.go` | A body-matching request cannot reach an early response before P2 resolves; no synthetic EOS. |
| P1 | Common lifecycle and correlation | `event.h`, `integrity_event.h`, `decision.h`, `msconnector_runtime.[ch]`, `event.c` | Explicit terminal error/cancel/cleanup, exactly-once lifecycle, `decision_id`, neutral Allow/Log-only result. |
| P1 | SPOP transport robustness | `read_full`, `write_full`, `recv_frame`, `send_agent_disconnect`, `handle_connection`, `accept_loop`, `transaction_cache` | Per-socket deadline, no SIGPIPE process exit, bounded concurrency, working follow-up HELLO/Allow/Deny. |
| P1 | Envoy ext_proc idle streams | `processor.go`, `config.go`, `main.go`, `processor_test.go` | Idle `Recv` deadline, active-stream bound, cancel and follow-up evidence. |
| P1 | Stock lighttpd build | `mod_msconnector.c`, `build/build_module.sh` | Repair implicit `mod_msconnector_emit_host_transaction_id` declaration, then choose stream-capable path. |
| P1 | Envoy ext_authz composite | ext_authz service, authorization service, ext_proc processor, bounded coordinator | P1/P2 precheck and P3/P4 observer share one transaction. |
| P1 | Traefik forwardAuth composite | forwardAuth service, Native middleware/UDS, bounded coordinator | A logically complete P1–P4 forwardAuth path. |
| P2 | P4 Strict actions | Apache/NGINX filters, HAProxy mappings, Envoy/Traefik observers, lighttpd path | Client-visible abort/reset and actual action event. |
| P2 | Evidence contract | canonical vectors, event validator, all host harnesses, `capabilities.json`, EN/DE docs | Immutable source/config/process/client/event/action/cleanup manifest. |

## Work allocation and concrete source anchors

The following are future implementation packages, not changes made by this
record. `Common` work is implemented once; a host adapter must not recreate its
own phase or evidence semantics. Host timers, stream resets, socket cleanup,
and process evidence remain connector/host responsibilities.

| Class | Package and concrete anchors | Required result and acceptance |
| --- | --- | --- |
| Common | **C1 Lifecycle:** `common/include/msconnector/{phase.h,transaction_state.h,flow_guard.h}`, `common/runtime/msconnector_runtime.{h,c}`: `msconnector_runtime_transaction_begin`, `append_request_body_chunk`, `finish_request_body`, `process_response_headers`, `append_response_body_chunk`, `finish_response_body`, `finish`, `destroy`; `common/src/flow_guard.c` | Explicit P1–P4/EOS/error/cancel/disconnect states; duplicate and out-of-order calls rejected; exactly-once terminal cleanup. |
| Common | **C2 P4 Safe/Strict:** `common/src/late_intervention.c`, `common/runtime/msconnector_runtime.c`: `set_response_commit_state`, `record_host_action`; `common/src/event.c`: `msconnector_event_set_phase4_hard_abort_after_200` | Safe records a truthful non-disruptive outcome; Strict is emitted only after the adapter reports the actual abort/reset. Common never performs the host action. |
| Common | **C3 correlation:** `common/include/msconnector/{decision.h,event.h}`, `common/src/{decision.c,event.c,integrity_event.c,transaction_id.c}`, runtime `record_host_action` | Add opaque `decision_id` and parent-decision reference; produce a bounded neutral result for Allow/Log-only; preserve transaction/phase/rule/action correlation across parallel requests. |
| Common | **C4 terminal errors and limits:** `common/include/msconnector/{error.h,limits.h,resource_limits.h,request_mapper_contract.h,response_mapper_contract.h}`, `common/src/{error.c,resource_limits.c,request_mapper_contract.c,response_mapper_contract.c}`, runtime transaction APIs | A neutral terminal-error/cancel API and one canonical limit contract. Each error class produces one correlated terminal event and no false EOS/success. |
| Connector/host | **H1 real-host evidence:** existing connector-owned `harness/` scripts/configurations, `common/rules/modsecurity_p1_p4_vectors.conf`, `capabilities.json` | For each exact source/host/configuration: build, config validation, readiness, client result, Rule-ID/decision/event/action correlation, error/timeout/cancel/follow-up, and cleanup evidence. This is future test/harness work, not a CI change. |
| Documentation | **D1 evidence recording:** this EN/DE record and the paired archive index | Update a capability only after immutable source/config/process/client/event/action/cleanup artifacts exist; never infer `fully_runtime_verified` from a framework report or a source path. |

## Per-connector implementation and acceptance plan

Each row lists the next source-owned work and the minimum missing proof before
that path may be promoted. All rows also require the common C1–C4 contract and
H1 evidence above; “Strict” always means an observed host action, not a Common
intent or a log field.

| Connector | Connector-specific implementation anchors | Promotion acceptance for this path |
| --- | --- | --- |
| Apache | `connectors/apache/src/mod_security3.c`: request hooks and `hook_insert_filter`; `msc_filters.c`: `msc_finalize_request_body`, `apache_input_filter_handle_eos`, response filters; `harness/run_apache_smoke.sh` | Repeat Allow/P1/P2/P3/P4 Safe on the exact host, implement/prove post-commit Strict action, then engine-down, deadline, malformed host/engine result, disconnect, follow-up, and exactly-once cleanup. |
| NGINX | `connectors/nginx/src/ngx_http_modsecurity_{access,header_filter,body_filter}.c`, including the Phase-4 action/log helpers; `harness/run_nginx_smoke.sh` | Replace sandbox-only evidence with a normal master/worker host; add real P2/P3/P4 Safe and Strict, every required error case, correlation, and teardown/follow-up proof. |
| HAProxy HTX | `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`: `haproxy_modsecurity_htx_process_response_headers`, request/response payload appenders, `haproxy_modsecurity_htx_report_late_decision`, `haproxy_modsecurity_htx_finish_context` | Bind `report_late_decision` to a host-confirmed Strict action, then show actual client effects and all engine/timeout/invalid/cancel/follow-up/cleanup cases in a real HTX host. |
| HAProxy SPOE/SPOP | `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`: `read_full`, `write_full`, `recv_frame`, `send_agent_disconnect`, `handle_connection`, `accept_loop`, `transaction_cache` | Add accepted-socket deadlines and bounded concurrency; prevent SIGPIPE/EPipe termination; then prove response phases, Safe/Strict, peer-close recovery and an independent follow-up HELLO/Allow/Deny after timeout/error. |
| Envoy ext_authz | `connectors/envoy/src/envoy_ext_authz_service_main.c`; `common/runtime/http_authorization_service.{h,c}`: `authorization_process_runtime_request`, `handle_authorization_request`; `connectors/envoy/config/{envoy-ext-authz.conf,envoy-ext-authz-smoke.yaml.in}` | Keep ext_authz as request precheck and add the bounded response observer/composite. Prove one host-minted lease joins P1/P2 with P3/P4, including Strict client effect and all lifecycle/error cases. ext_authz alone cannot pass P3/P4. |
| Envoy ext_proc | `connectors/envoy/ext_proc/internal/processor/{processor.go,config.go}`, `cmd/msconnector-envoy-ext-proc/main.go`; `Service.Process`, `processStream`, `receiveProcessingRequest`; `processor_test.go` | Bound idle `Recv` and active streams, prove cancel/timeout release and next-stream recovery, then complete Strict/error/follow-up evidence without claiming an unobserved downstream reset. |
| Traefik forwardAuth | `connectors/traefik/src/traefik_forwardauth_service_main.c`, `connectors/traefik/config/{traefik-forwardauth.conf,traefik-forwardauth-dynamic.yaml}`, Common authorization service; companion `connectors/traefik/native_middleware/{middleware.go,engine_uds.go}` | Decide and document body forwarding for P2, then bind forwardAuth to a response-capable companion using a server-minted lease. Prove P3/P4/Strict and all error/lifecycle cases as one transaction; request-only forwardAuth alone cannot pass them. |
| Traefik Native UDS | `connectors/traefik/native_middleware/middleware.go`: `Middleware.ServeHTTP`, `streamState.processResponseHeaders`, request/response body handling; `engine_uds.go`: `SetResponseCommit`, `AcknowledgeLateLogOnly`; `src/traefik_engine_service.c` | First repair the P0 guarantee that P2 reaches its valid EOS before P3 can be processed. Then make commit/late acknowledgements observable, prove a real Strict primitive or retain Safe only, and run full error/cancel/follow-up cleanup evidence. |
| lighttpd Stock | `connectors/lighttpd/module/mod_msconnector.c`: `mod_msconnector_emit_host_transaction_id`, `mod_msconnector_handle_request_body`, `mod_msconnector_handle_response_body`; `build/build_module.sh` | Repair the implicit-declaration build failure and select a stream-capable Stock integration path. Only then can build/config/start and P1–P4/Safe/Strict/error/lifecycle evidence be collected. |
| lighttpd Patched | Patched stream-hook ABI plus `connectors/lighttpd/module/mod_msconnector.c`: request/response body handlers; patched-host build/config/harness | Preserve the patched ABI contract, add real P2/P3/P4 Safe and Strict plus failure/cancel/follow-up/cleanup proof, and tie every host action to the common decision/event record. |

## Dependencies and recommended order

```text
Native UDS P0 ordering
  -> common lifecycle/event/correlation
     -> host Strict actions and uniform error evidence
     -> full ten-path runtime matrix

SPOP transport repair -> SPOP response phases -> SPOP full matrix
ext_proc idle repair  -> Envoy composite       -> ext_authz full matrix
Stock build repair    -> stream-capable path   -> Stock full matrix
```

First freeze source/evidence identity; then fix Native UDS P0; introduce common
lifecycle/correlation/limits/error interfaces; resolve Stock/SPOP/ext_proc
blockers; validate source-capable adapters; implement request-only composites;
prove real P4 Strict action; execute the full host matrix; then update
capability claims from the resulting evidence.

## Envoy ext_authz and Traefik forwardAuth architecture

`common/runtime/http_authorization_service.h` defines a request-phase-only
service. The handler maps one request, calls Begin, Decide, Finish, and
Destroy, and returns an authorization response before an upstream response can
exist. Neither ext_authz nor forwardAuth can independently observe P3/P4.

The required solution is one bounded host-owned transaction coordinator, not a
second uncorrelated transaction:

1. The request-side precheck opens the Common transaction and processes P1/P2.
2. A trusted response observer processes P3/P4 for that same transaction.
3. The host reports requested/actual action, commit state, transport result,
   error, timeout, and cleanup exactly once.
4. The coordinator removes state after terminal outcome, timeout, cancel,
   disconnect, duplicate detection, or capacity eviction.

Do not use `x-request-id`, URI, method, or a client header as the sole
correlation key. The host must mint a one-time, opaque, bounded lease, bind it
to the host request/stream and deadline, and use protected metadata. If a
header is unavoidable, strip inbound copies, protect it, and remove it before
upstream/client exposure. No URI or reused-client-ID fallback is adequate.

The preferred Envoy design is ext_authz precheck plus ext_proc response
observer. The preferred Traefik design is forwardAuth plus a native
response-observing middleware/UDS path. Existing ext_proc/Native UDS evidence
cannot be borrowed until the composite proves one transaction end to end.

## Security impact

This documentation-only change changes no parser, authorization rule, network
listener, timeout, secret, privilege, request/response path, or security
control.

The analysis records two source-backed future-remediation risks:

- Concurrent finding `FND-PARENT-0220` describes a P0/high Native Traefik UDS
  ordering defect: an early downstream response can reach P3 before an
  unread P2 body reaches EOS. This record neither changes nor closes it.
- A bounded read-only security scan recorded a medium-confidence SPOP
  availability candidate: serial `accept_loop` plus blocking frame reads can
  let a partial frame stall the listener. It is distinct from retained
  `FND-GS-0002` SIGPIPE/EPipe peer-close behavior. No runtime exploit ran.

Future remediation must preserve payload-free bounded events, server-owned
correlation, truthful response-commit semantics, and no false successful EOS.

## Changed files

- `reports/audits/change-records/CR-20260824-connector-runtime-gap-analysis.md`
- `reports/audits/change-records/CR-20260824-connector-runtime-gap-analysis.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

No product, connector, test, harness, CI/workflow, governance, Framework, MRTS,
Gitlink, dependency, or generated runtime file is changed.

## Commands executed and actual results

| Check | Actual result |
| --- | --- |
| Read-only remote preflight | Passed: fetch and effective push URL are `git@github.com:Easton97-Jens/ModSecurity-conector.git`; repository is exact, non-archived, default branch `master`, viewer permission `ADMIN`. |
| Base/destination readback | Passed: remote and local `origin/master` resolve to `a6b4ced4876a19666f7c7203ed9e719674c69ec1`; task branch was absent before creation. |
| Ruleset readback | Passed: active `Protect master` ruleset `19138299` has no bypass actors, requires PR/thread resolution, and requires six strict checks. |
| Base required-check snapshot | Passed for base SHA: `actions`, `bounded-c-cpp`, `envoy-go`, `traefik-go`, `actionlint`, and `zizmor` were `completed/success`. This is not future PR-head evidence. |
| Mixed-worktree boundary | Passed: existing foreign changes were excluded by a clean task worktree. |
| Manual bilingual parity | Passed: both records have 24 corresponding top-level sections; base/evidence SHAs, connector matrices, finding IDs, branch, and target status were reviewed in both languages. |
| Scoped diff review | Passed: the task worktree contains exactly the four planned documentation paths and `git diff --check` is clean. |
| Documentation checks | Not run: the repository targets invoke CI-owned scripts outside this documentation-only exception. Manual EN/DE heading/fact parity and scoped Git checks are run instead. |

## Runtime evidence

No build, host process, runtime harness, or connector test was run for this
documentation-only change. The retained inputs are the supplied
`14-security-posture.md`, `15-supply-chain-state.md`,
`16-runtime-readiness.md`, `19-findings-inventory.md`, and
`25-build-runtime-matrix.md` set plus supplied finding records. They establish
partial host results only at their recorded revision.

## Checks not run and rationale

- No connector build, host start, smoke test, runtime matrix, timeout,
  strict-intervention, or error-path test ran: the user authorized
  documentation delivery, not product/runtime execution.
- No product test or harness was changed.
- `make check-bilingual-docs` and `make check-doc-links` were not run because
  their targets invoke CI-owned scripts, which remain outside the narrowly
  authorized delivery-preflight exception.
- Fresh PR-head hosted checks and SonarQube results do not exist at first
  authoring and are not asserted. They are observed only after PR creation.

## Known limitations

This is a gap-analysis and delivery artifact, not an implementation. All ten
paths remain below target until target-matrix conditions are proved for exact
current source, host, configuration, and process evidence. Retained evidence
predates the base revision and cannot be promoted without rerun.

## Residual risks

P4 Strict may be impossible after response commit in a particular host until a
verifiable abort/reset primitive exists. Request-only protocols need stateful
companions and introduce bounded-state, timeout, restart, duplicate, and
cleanup risks. Native UDS P0 ordering and SPOP availability risks block a
trustworthy full promotion until remediated or explicitly risk-accepted by a
future user.

## Final diff and review status

The intended diff is limited to the four files listed above in a clean,
task-owned worktree based on verified `master`. This record does not authorize
a merge, direct `master` push, force push, workflow/configuration change,
check bypass, Framework delivery, or remediation of a recorded finding.

## Delivery status

The current user authorized one documentation branch, commit, push, and Draft
PR. The branch is `agent/connector-runtime-gap-analysis-20260824`; target is
`master`. Commit SHA, PR number/URL, and exact-head check outcomes are not
invented here and are recorded only after they exist.
