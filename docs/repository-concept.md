# Repository concept

**Language:** English | [Deutsch](repository-concept.de.md)

## Authority, scope, and claim discipline

This document is the binding target concept for the product monorepo. It
defines how the six connector products, the shared product contract, and the
independent test Framework fit together. It supplements, rather than replaces,
the current-state [architecture](architecture.md), the connector guides,
configuration references, and evidence reports. When those sources conflict,
compare the relevant code, tests, current evidence, and accepted decisions;
make the conflict visible rather than silently choosing a claim.

The concept covers Apache, NGINX, HAProxy, Envoy, Traefik, and lighttpd. It is
not a production-readiness, production-hardening, CRS-completeness, complete
HTTP/2/HTTP/3, complete-matrix, or strict-post-commit-enforcement claim.

### Claim labels

Use the following labels in this document and in future decisions. A label
describes the strength and scope of the cited repository evidence; it never
widens a claim beyond that evidence.

| Label | Meaning | Prohibited inference |
| --- | --- | --- |
| `verified` | Directly established by inspected source/contract material or by an explicitly scoped canonical evidence record with a profile and run ID. | Production readiness or coverage outside the cited scope. |
| `documented_not_runtime_verified` | Documented by prose, configuration, metadata, or a generated/informational record without matching current runtime proof for the stated behavior. | Treating a capability declaration, build, or configuration load as PASS. |
| `compatibility_only` | Retained alternate or historical route whose semantics and evidence do not substitute for the selected route. | Relabeling it as selected-route P1--P4 evidence. |
| `unknown` | The inspected repository material does not establish the fact or the current promotion state. | Guessing host behavior, ownership, or readiness. |
| `out_of_scope` | Deliberately outside the selected six-connector HTTP/1.1 core or this documentation change. | Calling it unsupported, implemented, or verified without separate work. |

### Source hierarchy and evidence boundary

| Source class | Authority for this concept | Current status |
| --- | --- | --- |
| Product source, checked-in contracts, and focused tests | Implementation ownership, lifecycle invariants, and build/contract behavior. | `verified` for the cited source contract; not runtime proof by itself. |
| Current architecture and connector guides | Current selected route and documented boundary. | `verified` as documentation structure; runtime claims still require run evidence. |
| `reports/current/core-completion.md` and `reports/current/readiness.md` | Bounded selected-core report statement for run `six-connectors-core-final-20260712T164725Z-e16e7f1`. | `documented_not_runtime_verified` here because raw canonical artifacts were not independently revalidated; never a production claim. |
| `connectors/*/capabilities.json` and generated capability catalogs | Capability and source-boundary declarations. | `documented_not_runtime_verified`; never a runtime promotion on their own. |
| `reports/testing/generated/` | Generator-managed report snapshots. | `unknown` for current promotion when report freshness says `stale`, `skipped`, or `skipped_stale_input`. |
| `.codex/context/` and local `AGENTS.md` | Local work assistance and Codex instructions. | `out_of_scope` as a versioned product source; they do not replace this concept. |

## Product vision and explicit non-goals

The repository is one product monorepo for libmodsecurity-based connector
products. It solves the shared product problem of applying a common
ModSecurity transaction contract to six different HTTP server or proxy host
APIs, while keeping host-specific hooks, filters, services, middleware,
configuration, build, packaging, installation, and client-visible actions
with the appropriate adapter.

libmodsecurity supplies the rule engine and transaction-facing operations. It
does not supply an Apache module, NGINX module, HAProxy filter, Envoy external
processor, Traefik middleware, or lighttpd module for this repository. The
connector and `common/` layers map bounded host data to the engine and map an
engine request for intervention back to a host action.

The Framework submodule is an independent reusable-test repository. It owns
reusable cases, runners, normalizers, catalog selection, schemas, and report
generation. The parent owns the actual connector product, its host-specific
execution seam, and the canonical host artifacts that a Framework workflow
may normalize and validate.

This repository is not a second general-purpose test platform, a replacement
for libmodsecurity, a universal host ABI, a place for generated runtime output,
or a guarantee that every host, protocol, rule set, configuration, or late
intervention mode is supported in production.

## Monorepo boundary and change routing

The boundary is intentionally simple:

```text
Parent repository:
How is the product built and attached to the selected host?

Framework repository:
How is the product checked for correct, secure, and consistent behavior?
```

| Boundary | Owner and contents | Does not own | Change destination |
| --- | --- | --- | --- |
| Parent repository | Product connector source, `common/`, build systems, connector configuration, packaging/installation material, connector documentation, product contracts, host-specific harness seams, and artifact producers. | A second reusable case catalog, generic normalizer, or general test platform. | This repository. |
| `modules/ModSecurity-test-Framework` | Reusable test cases, rule catalogs, runner and reusable harness logic, schemas, normalizers, cross-connector comparison, reusable smoke/integration logic, and canonical test-report generation. | Connector implementation, host hook code, host build configuration, or a connector promotion decision. | The Framework repository and its own Change Record. |
| External host and ModSecurity sources | Pinned or selected upstream host/engine inputs, licenses, provenance, and external runtime dependencies. | Parent product source ownership unless imported with explicit attribution. | The relevant external source process and parent provenance records. |
| External build, cache, runtime, log, and evidence roots | Invocation-local outputs selected by documented variables such as `BUILD_ROOT`, `EVIDENCE_ROOT`, and `VERIFIED_RUN_ROOT`. | Versioned source, secrets, or durable product documentation. | Outside either checkout. |
| Generated reports and inventories | Generator-owned output under paths such as `reports/testing/generated/`. | Manual corrections or new runtime results. | Their generator/source contract, never a hand edit. |
| Manually maintained documentation and Change Records | Bilingual product guidance, decisions, current report summaries, and traceability. | Raw payloads, secrets, or a substitute for generated evidence. | This repository with English/German companions. |

Put a connector-neutral product rule in `common/` only when it can compile and
operate without a host SDK. Put a host API action, host object lifetime,
host-config parser, build/packaging behavior, or host-specific runtime seam in
`connectors/<name>/`. Put a reusable case, normalizer, runner, or schema in
the Framework. Keep a small parent test when it protects parent build,
configuration, artifact, path, security, or adapter-seam behavior; do not
copy a Framework catalog case into the parent.

## Component and dependency model

The target is one shared product contract with host-specific adapters, not six
independent products that merely share a name.

```text
                         +-------------------------------+
                         | common/                       |
                         | neutral types, lifecycle,      |
                         | limits, decisions, redaction   |
                         +---------------+---------------+
                                         ^
                                         |
        +----------------+---------------+---------------+----------------+
        |                |               |               |                |
 connectors/apache  connectors/nginx  connectors/haproxy connectors/envoy ...
        |                |               |               |                |
        +----------------+---------------+---------------+----------------+
                                         |
                              selected host API / service

 Parent build, configuration, and host-specific artifact producers
                                         |
                                         v
 Framework cases, normalization, validation, and generated reports
```

| Component | Responsibility | Allowed dependencies | Forbidden coupling |
| --- | --- | --- | --- |
| `common/` | Host-neutral C-first contracts, runtime support, lifecycle phases, limits, decision/event shapes, logging/redaction, and mapper contracts. | libmodsecurity-facing neutral code and standard C facilities. | Host SDK objects, host hooks, filter registration, server ABI, host buffer ownership, or host-specific late action. |
| `connectors/apache/` | Apache module, APR/request-pool handling, hooks/filters, Apache configuration, APXS build, packaging/install inputs, and Apache seam. | `common/`, libmodsecurity, Apache/APR APIs, parent build/configuration. | NGINX/HAProxy/Envoy/Traefik/lighttpd API assumptions or a duplicated shared contract. |
| `connectors/nginx/` | NGINX HTTP module, request/location configuration, filter/access wiring, NGINX pools, build and install inputs. | `common/`, libmodsecurity, NGINX APIs, parent build/configuration. | Apache expression semantics, other host SDKs, or retained host buffers in Common. |
| `connectors/haproxy/` | Native HTX overlay/filter, HAProxy mapping, configuration, build/harness seam, and separated historical SPOP material. | `common/`, libmodsecurity, HAProxy HTX APIs, parent build/configuration. | Treating `spoe-spop-agent` as the native HTX product route. |
| `connectors/envoy/` | Envoy `ext_proc` service, protocol mapping, generated host configuration material, build/harness seam, and `ext_authz` compatibility material. | `common/`, libmodsecurity, Envoy/gRPC/Go interfaces, parent build/configuration. | Treating `ext_authz` as `ext_proc` response-phase evidence. |
| `connectors/traefik/` | Native middleware, local UDS engine-service client/server boundary, Traefik configuration/build seam, and `forwardAuth` compatibility material. | `common/`, libmodsecurity, Go and Traefik plugin interfaces, parent build/configuration. | Treating `forwardAuth` as native middleware response-phase evidence. |
| `connectors/lighttpd/` | Patched native lighttpd module, mapper and patched-host boundary, configuration/build seam, and separated stock/sidecar compatibility material. | `common/`, libmodsecurity, selected lighttpd APIs, parent build/configuration. | Treating stock/sidecar behavior as `patched-native` evidence. |
| `ci/` | Parent orchestration, safe path checks, source/contract checks, lifecycle stage invocation, artifact producers, and report consumers. | Parent code, root Makefile, and explicitly delegated Framework tools. | Replacing the Framework's reusable catalog/normalization role or embedding host product logic that belongs in a connector. |
| `config/` | Versioned declarative test/configuration inputs and import status. | Parent documentation and checkers. | Runtime secrets, generated evidence, or a host implementation. |
| `tests/` | Focused parent product-contract, path/security, artifact, and adapter-seam tests. | Parent `ci/`, root Makefile, and declared Framework fixtures where needed. | A second reusable case corpus or canonical host-runtime result. |
| `reports/` | Current manually maintained reports, Change Records, generated report locations, and source-backed inventories. | Source contracts and Framework generators. | Manual modification of generated outputs or storage of raw payloads/secrets. |
| Framework submodule | Reusable tests, catalogs, normalizers, schemas, runners, and report generation. | Declared connector inputs and artifact contracts. | Parent connector source or host-specific product build ownership. |

## Connector contract and finished product

Every `connectors/<name>/` directory is the host-specific product adapter. It
must adapt shared rules; it must not independently reinvent shared lifecycle,
limit, decision, logging/redaction, error, or ownership semantics. Source,
build, configuration, packaging, installation, documentation, and a
Framework-facing execution seam together define the product for that host.

| Finished-product requirement | Required meaning | Evidence boundary |
| --- | --- | --- |
| Reproducible build | A documented target can build the selected connector with its declared inputs. | A build is not host traffic evidence. |
| Documented dependencies | Host, libmodsecurity, toolchain, and external roots are named without secret or workstation assumptions. | Discovery is not a runtime result. |
| Documented installation and packaging | The host-specific load/install path is explicit. | Installation text is not an installed-host assertion. |
| Versioned configuration | Selected host and Common/engine inputs are versioned and referenced. | A configuration file is not a capability result. |
| Complete host attachment | The selected host integration has its hooks, filter/service/middleware, mapper, and action path. | Source presence is not a lifecycle PASS. |
| P1--P4 lifecycle in supported scope | The host maps only the documented phase scope and EOS/commit boundaries. | Scope excludes unselected protocol or strict behavior. |
| Ownership and cleanup | Resource owners, borrowed data, error paths, and one-time finish/destroy rules are documented. | A static rule is not resilience evidence. |
| Defined intervention and errors | Requested engine action and actual host action/error mapping are distinguishable. | An engine decision does not prove a client-visible action. |
| English and German documentation | Reader-facing product guidance has complete paired versions. | Structural parity alone does not prove semantic behavior. |
| Framework integration | The connector supplies an adapter seam and artifacts consumable by the Framework. | A Framework starter or generated report is not host promotion. |
| Test and evidence path | Build/configuration/smoke/lifecycle/evidence targets and result boundaries are documented. | One layer does not promote another. |
| No unsupported readiness claim | Known evidence limits and `NOT EXECUTED` work remain visible. | No connector becomes production ready by declaration. |

## Actual data flow and lifecycle

The following is the actual shared shape evidenced by the Common runtime,
connector guides, and selected-run contract. A host can use a hook, filter,
service, or middleware, but it may not bypass the ownership and phase rules.

```text
Client
  -> selected Host or Proxy
  -> Connector hook, filter, service, or middleware
  -> Host mapper
  -> Common Runtime and/or libmodsecurity
  -> requested decision and host intervention or forwarding
  -> logging and cleanup
  -> invocation-local raw evidence
  -> Framework normalization
  -> validation and reports
```

The Common runtime owns its engine, rules, configuration strings, and internal
transaction metadata. It borrows a mapped request/response or body chunk only
for the corresponding call. The host owns its objects, buffers, wire behavior,
and committed-response semantics.

| Step | Data consumed and committed boundary | One-time rule | Result boundary |
| --- | --- | --- | --- |
| P1 | Connection metadata, URI, and request headers before an eligible request action. | Process connection/URI/headers once per transaction; do not reuse a completed request context. | A pre-request decision can be host-actionable only before that host commits the relevant response. |
| P2 | Bounded request-body chunks; the phase finishes at the selected request EOS. | Chunks may repeat; `finish_request_body` is exactly once and no append follows it. | A selected P2 result does not prove general host streaming or forwarding behavior. |
| P3 | Response status and headers before or at the host's header-commit boundary. | Process response headers once before P4. | A requested action is only client-visible when the host can still change the response. |
| P4 | Bounded response-body chunks after P3; the phase finishes at selected response EOS. Apache incrementally appends data but retains its normalized response brigade through first EOS before release. | Chunks may repeat; `finish_response_body` or unobserved completion is exactly once and no append follows it. Apache releases or discards its saved brigade exactly once after the P4 decision. | Post-commit action is host-specific; Safe records a conservative actual result rather than rewriting a committed response. Apache's normal all-response-gate deny is resolved before original output release. |
| Logging and cleanup | Final transaction state, bounded metadata, actual host action, and artifact provenance. | `finish` freezes the Common flow; destroy is idempotent at the ownership boundary. | Logs/events are payload-safe scoped artifacts, not a general runtime guarantee. |

| Host distinction | Selected documented behavior | Status |
| --- | --- | --- |
| Apache | Request/output filters borrow APR buckets; P2 finishes at EOS; P4 incrementally appends data but retains the normalized response brigade through first EOS before decision/release. `r->sent_bodyct`/`eos_sent` are not commit proof for this filter. | `verified` source contract; selected core evidence is scoped. |
| NGINX | The host first supplies the request body; the connector iterates it, so P2 is not end-to-end request streaming. Response chains use filter/EOS handling. | `verified` source contract; do not claim request streaming. |
| HAProxy | Native HTX forwards current blocks and finalizes at HTTP end; native HTX and SPOP are separate. | `verified` source contract. |
| Envoy | `ext_proc` maps a streamed gRPC exchange; request/response EOS or trailers close the relevant phase. | `verified` source contract; `ext_authz` is `compatibility_only`. |
| Traefik | Native middleware and its local UDS engine service maintain a per-request transaction; response-writer commitment limits late action. | `verified` source contract; `forwardAuth` is `compatibility_only`. |
| lighttpd | Patched native hooks receive borrowed identity entity ranges and one EOS; short writes or unselected modes must not cause duplicate ingestion. | `verified` source contract for the selected patch; broad fault tolerance is `out_of_scope`. |

For the recorded selected core, `reports/current/core-completion.md` says P1,
P2, P3, P4 rule evaluation, Safe late action, first byte before upstream EOS,
no connector-owned full response buffer, and cleanup passed for run
`six-connectors-core-final-20260712T164725Z-e16e7f1`. That is a historical,
`documented_not_runtime_verified` cross-connector report claim here because
this task did not independently revalidate raw canonical artifacts. It does
not describe the current Apache Phase-4 all-response gate: Apache deliberately
retains normalized output through first EOS and does not claim first-byte-
before-EOS or no-full-buffer behavior. The report remains limited to the listed
HTTP/1.1 core paths and cases. It does not assert per-chunk P4 decisions,
HTTP/2/HTTP/3, CRS, a complete catalog, strict post-commit enforcement, or
production readiness.

## Ownership and cleanup invariants

Ownership is a product contract. A connector must release every resource on
success, terminal intervention, parser failure, host cancellation, and startup
failure without retaining a host pointer past its valid callback.

| Resource | Owner | Borrower or consumer | Required cleanup invariant |
| --- | --- | --- | --- |
| Host request/response object | Selected host | Connector mapper and Common call boundary | Never retain the host object in `common/`; release it by the host's lifecycle. |
| Apache APR pools, request context, and brigades | Apache/request pool | Apache adapter during hook/filter execution | Allocate request-lifetime state in the request pool; retain the normalized P4 response brigade through first EOS only for the documented all-response gate; discard it on deny/error and release the transaction at request cleanup. |
| NGINX request pool, location configuration, and chains | NGINX | NGINX adapter and Common call boundary | Store request context/redirect copy in `r->pool`; do not retain chain-buffer pointers after the filter call; clean transaction with request pool cleanup. |
| HAProxy HTX blocks and filter context | HAProxy owns HTX; filter owns its own context/snapshots | HTX adapter and Common call boundary | Borrow only current HTX data; free transaction and bounded snapshots on detach, reset, reply, and error. |
| ModSecurity/Common transaction | Common runtime transaction object and native engine transaction | Connector invokes phase APIs | Finish only after required EOS state, then destroy exactly once; cleanup native transaction even on an error path. |
| Engine/runtime, rules, and runtime configuration strings | `common/` runtime | Connector setup/shutdown | Create once for the configured owner scope; close event file, engine, rules, and copied configuration during runtime destroy. |
| Intervention and redirect URL | Host adapter owns host materialization; Common decision only carries bounded data | Host action mapper | Copy redirect/location into the host-owned request lifetime before use; do not retain caller-owned URL pointers. |
| Request/response body buffers | Host | Common append call | Pass bounded views/copies only for the call and track counters/truncation. A connector must not retain a cross-callback full response buffer except for a documented host enforcement boundary: Apache's request-pool P4 gate retains normalized output through EOS under a finite fail-closed limit. |
| Go request state and CGo slices | Envoy/Traefik service or middleware request scope | Common/libmodsecurity bridge | Copy transient Go slice data for a CGo call when needed; remove stream/request map state and finish/destroy transaction on EOF, error, or normal completion. |
| UDS listener, connection, and service session | Traefik native service process | Middleware and per-request protocol | Restrict socket permissions and locality; close connection/session and server-side transaction on normal finish, client EOF, protocol error, or startup failure. |
| Raw evidence and logs | Invocation-selected external evidence/log root | Parent producer and Framework consumer | Keep payload-free, scoped by connector/profile/run ID, redact secrets, and do not commit runtime outputs. |

The Common API rejects body append after finalization, response body work before
response headers, duplicate host-action recording, and transaction finish with
an unfinished selected streaming/EOS phase. Those are `verified` source
invariants. A connector must preserve them even where its host callback model
differs.

## Connector profile crosswalk

The selected route, its compatibility term, and its evidence are separate
columns on purpose. Do not infer selected-route support from an alternate
profile or stale capability manifest.

| Connector | Selected product path | Compatibility path | Host integration and engine boundary | Supported selected phase scope | Runtime/evidence status | Known boundary | Build, check, smoke, and lifecycle targets |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | `native-httpd-module` | No separate named alternate route is selected; the deprecated legacy MIME directive is not a gate-bypass route. | Native httpd module with Common/libmodsecurity mapping. | P1--P4; P4 is an EOS-only all-response gate. | Current report says `PASS`; it is `documented_not_runtime_verified` here, as are capability declarations. | Normal P4 deny is pre-release; only independently committed output can use Safe log-only or Strict abort fallback. H1/H2 runner existence is not evidence. | `build-apache`, `check-config-apache`, `start-smoke-apache`, `runtime-smoke-apache`, `full-lifecycle-apache`, `evidence-check-apache` |
| NGINX | `native-nginx-http-module` | No separate named alternate route is selected; Apache syntax is not compatible. | Native NGINX HTTP module with Common/libmodsecurity mapping. | P1--P4; host-prepared P2 body and filter/EOS P4. | Current report says `PASS`; it is `documented_not_runtime_verified` here, as are capability declarations. | Request body is not end-to-end streamed by the selected adapter; strict/protocol claims remain separate. | `build-nginx`, `check-config-nginx`, `start-smoke-nginx`, `runtime-smoke-nginx`, `full-lifecycle-nginx`, `evidence-check-nginx` |
| HAProxy | `native-htx-filter` | `spoe-spop-agent` is `compatibility_only`. | Native HTX filter and Common/libmodsecurity mapping. | P1--P4 on HTX/EOS selected core. | Current report says `PASS`; it is `documented_not_runtime_verified`; manifest mode divergence is also `documented_not_runtime_verified`. | Safe P4 is `log_only`; strict post-commit action is `not_attempted` in the selected guide. | `build-haproxy`, `check-config-haproxy`, `start-smoke-haproxy`, `runtime-smoke-haproxy`, `full-lifecycle-haproxy-htx`, `evidence-check-haproxy` |
| Envoy | `ext_proc` | `ext_authz` / `http-ext-authz-service` is `compatibility_only`. | Streamed Envoy external processor service maps gRPC messages to Common/libmodsecurity. | P1--P4 through selected stream/EOS boundary. | Current report says `PASS`; it is `documented_not_runtime_verified`; manifest mode divergence and generated capability status are also so labeled. | Strict reset/cancellation is not established by a service decision alone. | `build-envoy`, `check-config-envoy`, `start-smoke-envoy`, `runtime-smoke-envoy`, `full-lifecycle-envoy-ext-proc`, `evidence-check-envoy` |
| Traefik | `native-middleware` / `native-traefik-middleware` | `forwardAuth` / `http-forwardauth-service` is `compatibility_only`. | Native Go middleware communicates with a private UDS Common/libmodsecurity engine service. | P1--P4 with response-writer/EOS boundary. | Current report says `PASS`; it is `documented_not_runtime_verified`; manifest mode divergence and generated capability status are also so labeled. | Safe P4 is `log_only`; native strict abort remains separate evidence work. | `build-traefik`, `check-config-traefik`, `start-smoke-traefik`, `runtime-smoke-traefik`, `full-lifecycle-traefik-native`, `evidence-check-traefik` |
| lighttpd | `patched-native` / `patched-native-lighttpd` | Stock-native, sidecar, and legacy bridge material is `compatibility_only`. | Version-pinned patched lighttpd module maps selected borrowed entity ranges to Common/libmodsecurity. | P1--P4 for selected HTTP/1 identity entity ranges and EOS. | Current report says `PASS`; it is `documented_not_runtime_verified`; manifest mode divergence and generated capability status are also so labeled. | Compression, HTTP/2, unselected buffering, and strict client abort are `out_of_scope`. | `build-lighttpd`, `check-config-lighttpd`, `start-smoke-lighttpd`, `runtime-smoke-lighttpd`, `full-lifecycle-lighttpd-patched`, `evidence-check-lighttpd` |

The root Makefile retains aliases such as `full-lifecycle-haproxy`,
`full-lifecycle-envoy`, `full-lifecycle-traefik`, and
`full-lifecycle-lighttpd` for their selected targets. Use the explicit target
identity in evidence and documentation so a compatibility execution cannot be
misclassified as full lifecycle.

## Configuration contract and security-relevant defaults

Configuration has separate host/connector, Common Runtime, and ModSecurity
Engine layers. A value at one layer does not implicitly configure another.

| Configuration location or input | Owner | Purpose | Status and boundary |
| --- | --- | --- | --- |
| `connectors/<name>/`, `examples/<name>/`, and versioned profile files | Parent connector | Host syntax, host-specific service/middleware/filter configuration, installation/build inputs, and selected profiles. | `verified` as versioned configuration; a load does not prove traffic. |
| `common/runtime/msconnector_runtime.c` and `examples/common/` | Parent `common/` | Neutral `key=value` runtime configuration, limits, event path, and engine rule source. | `verified` parser/source contract; a key is not a host directive. |
| `common/rules/` and connector rule/configuration inputs | Parent connector product | Targeted rules and product-owned selected inputs. | `documented_not_runtime_verified` until used by matching scoped evidence. |
| `modules/ModSecurity-test-Framework/tests/` and Framework variables | Framework | Reusable cases, rules, schemas, catalog selection, runner defaults, and normalization. | Framework-owned test inputs; parent records the host-specific effective configuration. |
| `BUILD_ROOT`, `EVIDENCE_ROOT`, `VERIFIED_RUN_ROOT`, ports, binary paths, and UDS paths | Invocation/CI operator | External build/cache/runtime/log/evidence location and host launch values. | Local/runtime values; never versioned secrets or capability proof. |
| Secrets, credentials, cookies, tokens, and private keys | External secret mechanism | Runtime authentication or private deployment input when required. | `out_of_scope` for versioned examples, reports, and this concept. |

| Control | Source-backed default or selected value | Security effect and classification |
| --- | --- | --- |
| `enabled` | Common Runtime default `off`. | It is fail-open with respect to Common enforcement until explicitly enabled; it is not a repository-wide host failure policy. |
| `request_body_limit`, `response_body_limit`, header limits, and `max_event_json_bytes` | Common Runtime defaults bound body/header/event input. | Bound resource and metadata exposure; a higher value is not safe-buffering proof. |
| `body_limit_action` | Common Runtime default `reject`. | Rejects an over-limit chunk before engine input; the resulting host response remains connector-specific. |
| `default_block_status` and `default_error_status` | Common Runtime defaults `403` and `500`. | Define fallback status values where a host maps them; they do not prove a uniform fail-closed response. |
| `response_body_mode` and `phase4_mode` | Common Runtime defaults `none` and `safe`. | No P4 input is processed by default; Safe late behavior is conservative and after commit can be `log_only`, not a universal fail-open/fail-closed policy. Apache is an explicit exception for normal P4 enforcement: its all-response gate decides before original output release. |
| Envoy `failure_mode_allow` | Selected `ext_proc` templates set `failure_mode_allow: false`. | Selected configuration documents fail-closed processor-reachability handling; it is not evidence for every Envoy deployment. |
| `rules_remote_url` and external downloads | Optional rule/source inputs. | Treat as an external trust boundary: require declared origin, checksum/pin where applicable, and no silent fallback. |

The documented selected core reports Safe P4 as requested `deny`, actual
`log_only`, visible HTTP 200, and no connection abort after a committed
response. This is a bounded late-intervention observation, not a global
availability or security default, and it must not be used to characterize the
current Apache pre-release all-response gate.

## Test, evidence, and report model

| Layer | What it can establish | What it cannot establish |
| --- | --- | --- |
| Syntax check | The checked file parses under the named tool. | Product behavior, host traffic, or security. |
| Contract test | The explicit source, schema, path, privacy, or wiring contract. | A real host execution. |
| Unit test | A focused function or component behavior with test-controlled inputs. | A host lifecycle or production result. |
| Build | The selected source/build stage completes. | Configuration loading or traffic behavior. |
| Configuration check | Selected configuration parses or loads. | Request/response behavior or rule coverage. |
| Smoke test | The narrow host/service exercise named by its target. | Full lifecycle, catalog completeness, or promotion. |
| Runtime test | Its explicitly recorded host observation. | Other profiles, protocols, or unrecorded capabilities. |
| Full-lifecycle test | The selected profile and required artifact production. | Production readiness, complete matrix, CRS, or all protocols. |
| Canonical evidence | A run-scoped result bound to connector, selected profile, rules, configuration, run ID, and required artifacts. | A new run or a wider product claim. |
| Generated report | A generator's representation of its declared inputs. | Current truth when its inputs are stale or absent. |
| Production release decision | A separately reviewed operational decision. | Automatic consequence of any preceding layer. |

The tracked parent test inventory at base revision is classified below. The
classification is a placement review, not a move request; no tests are moved
by this concept change.

| Classification | Tracked parent tests | Rationale and follow-up |
| --- | --- | --- |
| `repository_governance` | `test_bilingual_docs.py`, `test_compiler_guides.py`, `test_make_runtime_defaults.py`, `test_runtime_path_policy.py`, `test_update_github_actions_versions.py` | Protect parent documentation, tooling, path, and workflow contracts; retain in parent. |
| `parent_product_contract` | `test_c_cpp_diagnostics.py`, `test_connector_capabilities.py`, `test_full_lifecycle_profiles.py`, `test_no_crs_selected_runner_wiring.py`, `test_six_connector_core_completion.py` | Protect root lifecycle selection, capability, compiler, and parent orchestration contracts; retain in parent. |
| `connector_local_seam` | `test_envoy_transport_hardening_contract.py`, `test_nginx_phase4_runner_wiring.py`, `test_nginx_protocol_harness_contract.py`, `test_response_header_backend.py`, `test_traefik_native_local_plugin.py`, `test_traefik_transport_hardening_contract.py` | Exercise a host/product integration seam; keep with its parent adapter until a deliberate Framework interface exists. |
| `framework_candidate` | `test_collect_no_crs_source.py`, `test_engine_lifecycle_artifacts.py`, `test_full_lifecycle_evidence.py`, `test_resolve_runtime_paths.py`, `test_runtime_env_snapshot_contract.py`, `test_transport_lifecycle_artifacts.py` | These protect generic normalization, artifacts, or runner isolation while also encoding parent profiles. Split reusable interface logic only through a deliberate Framework change. |
| `unclear` | `test_prepare_runtime_components.py`, `test_runtime_component_cache_contract.py`, `test_runtime_component_cache_identity.py` | Component preparation/cache policy spans parent product and Framework provisioning. Review the durable owner before any move. |

All of these root tests are `documented_not_runtime_verified` for runtime
purposes: they are unit/contract tests and were not executed for this
documentation change. Current generated reports must be interpreted with freshness. The generated
`report-freshness.generated.md` identifies the older run
`2026-06-16T19-12-00Z-614c8049` and marks many reports `stale`, `skipped`, or
`skipped_stale_input`. Therefore those snapshots are `unknown` for current
promotion. They neither override nor independently verify the bounded current
core report; refresh them only through their generators after valid inputs are
available.

## Security model

| Boundary | Required rule |
| --- | --- |
| Untrusted HTTP data | Treat request/response method, URI, headers, body ranges, status, and protocol metadata as untrusted; validate bounded neutral mappings before Common/runtime use. |
| Limits and buffering | Enforce documented header/body/event limits and preserve no connector-owned complete response buffer across callbacks, except for a documented host security gate such as Apache P4's finite all-response EOS retention. |
| Paths and symlinks | Use safe external roots; validate artifact/config paths and do not let generated/runtime output escape the selected root. |
| Downloads and provenance | Use explicit workflows, declared source/pins/checksums where provided, and no silent system-binary or network fallback. |
| Intervention ownership | Separate requested engine decision from confirmed host action; copy redirect data into the host owner; do not fabricate a client-visible result after commit. |
| UDS and services | Keep Traefik-style local sockets private, permission-restricted, bounded, and cleaned up on all connection outcomes. |
| TLS redirects and headers | Apply host validation before setting redirect/location output; do not log redirect tokens or untrusted header values without sanitization. |
| Logging and redaction | Keep events/results payload-free and bounded; omit bodies, cookies, authorization, credentials, private keys, and secret configuration. |
| CI and workflows | Pin actions and validate repository paths/contracts; CI success is not a host runtime security claim. |
| Failure policy | Document a host-specific fail-open/fail-closed decision; do not infer one from Common defaults or Safe P4 behavior. |

No confirmed security finding is promoted by this concept. Unconfirmed scanner
candidates or historical notes remain unconfirmed until a source-to-sink
analysis and the applicable evidence record validate them.

## Extension rules for a feature or new connector

Use this order for a new connector or a material cross-connector feature:

1. Describe the host integration model and set the architecture boundary.
2. Declare the selected lifecycle phases, commit boundary, and explicit exclusions.
3. Reuse `common/` contracts for neutral lifecycle, limits, decisions, logging, and errors.
4. Implement host-specific mappers, hooks/filters/services/middleware, and actions in `connectors/<name>/`.
5. Document ownership, borrowed data, intervention/redirect lifetime, and cleanup on success and error paths.
6. Provide reproducible build, packaging/installation, and versioned configuration.
7. Add parent product-contract tests and a host-specific seam only for real host behavior.
8. Create or adapt the Framework adapter; reuse Framework cases, schemas, runners, and normalizers.
9. Analyze trust boundaries, limits, redaction, downloads, UDS/transport permissions, and failure policy.
10. Add complete English and German product, connector, configuration, lifecycle, and limitation documentation.
11. Run the required source/contract/configuration checks and produce scoped runtime evidence when making a runtime claim.
12. Generate reports through their generator and distinguish fresh canonical artifacts from stale snapshots.
13. Update the Change Record and any affected ADR, then reconcile both with the final diff and actual checks.

## Current deviations from the target concept

| Area | Desired state | Current observed state | Deviation | Recommended follow-up | Priority | Repository |
| --- | --- | --- | --- | --- | --- | --- |
| Binding target concept | One explicit product-monorepo target source. | Current architecture is current-state focused; no target concept existed. | Addressed by this document, pending review/acceptance. | Keep this concept current and link future ADRs. | High | Parent |
| ADR process | Small versioned ADR process for durable cross-connector choices. | No ADR directory/process was found. | Addressed by `docs/decisions/README.md`; no retrospective ADRs are created. | Accept `ADR-001` through `ADR-005` only when each decision is ready. | Medium | Parent |
| Capability integration modes | Selected profile and capability metadata agree. | HAProxy, Envoy, Traefik, and lighttpd manifests name legacy/alternate modes while current route docs name selected native routes. | `documented_not_runtime_verified` metadata divergence. | Align metadata/manifests and generators in a separate reviewed change. | High | Parent |
| Runtime report provenance | A current profile-matching canonical artifact set backs any runtime label. | Current reports quote `PASS` for `six-connectors-core-final-20260712T164725Z-e16e7f1`, but raw artifacts were not independently revalidated in this task. | Their result is `documented_not_runtime_verified` here. | Locate/revalidate the raw canonical artifact set before promoting any current runtime status. | High | Parent + Framework |
| Generated report freshness | Current reports derive from fresh inputs for the checked revisions. | Many generated reports cite the older `2026-06-16T19-12-00Z-614c8049` input and are `stale` or skipped. | They are `unknown` for current promotion. | Reproduce/refresh through the generator with valid inputs; do not hand edit. | High | Parent + Framework |
| Common design note | Current design notes describe selected product routes. | `common/docs/design.md` and `common/docs/design.de.md` now state the current Common boundary and distinguish compatibility material from selected routes. | Addressed by `CR-20260714-common-design-note` and the Common design-note contract in `check-bilingual-docs`. | Keep the note synchronized with the binding concept, architecture, and connector guides when selected routes change. | Medium | Parent |
| Test boundary | Generic test logic resides in Framework; parent keeps product contracts and host seams. | Root test README states that rule, but generic normalization/evidence code and Framework-facing tests remain in parent while Framework also contains host-specific provisioning/runners. | `framework_candidate` and `unclear` placement split; no automatic move is justified. | Establish a stable Framework interface, then extract reusable logic while retaining connector profiles and host seams in parent. | Medium | Parent + Framework |
| Generator/output ownership | Framework-owned reports have one declared generator and output owner. | Framework generation writes coverage/runtime output under parent `reports/testing/generated/`; a parent language-switch postprocessor also participates. | Generator/output ownership is split and requires explicit governance. | Record the final ownership contract in an ADR and avoid manual generated-file changes. | Medium | Parent + Framework |
| Connector self-sufficiency | Every connector and `common/` can form a documented buildable/installable product. | Root targets and connector material exist, but packaging/install completeness is not established uniformly by a single current evidence record. | `documented_not_runtime_verified`. | Audit each connector's build/packaging/install contract and record bounded results. | Medium | Parent |
| Uniform observable contracts | Shared phase, limit, intervention, logging, cleanup, configuration, and evidence meaning across hosts. | Host implementations necessarily differ; selected core is bounded and strict/protocol coverage is incomplete. | Differences are allowed only when explicit; broader equivalence is `out_of_scope`. | Add targeted evidence/ADR work for strict behavior and protocol scopes. | Medium | Parent + Framework |

## Definitions and known limits

| Term | Binding definition |
| --- | --- |
| supported | A feature is supported only for the named connector, selected profile, documented scope, and required evidence level; it is never implied by source presence alone. |
| selected profile | The explicit profile/target identity used by the root lifecycle contract for a connector, such as `ext_proc` or `native-htx-filter`. |
| compatibility path | A separately retained alternate, legacy, example, or migration route that cannot substitute for a selected profile. |
| experimental | An explicitly labeled non-stable scope requiring its own evidence and limitations; this document does not silently label any selected core route experimental. |
| runtime verified | A run-scoped claim backed by the required canonical host artifacts, selected profile, effective configuration, rule input, and result/event validation. |
| not executed | A deliberate non-run status; it is not PASS, FAIL, or unsupported. |
| blocked | A declared prerequisite is absent, unsafe, or intentionally unavailable; it is not a negative capability result. |
| unknown | The repository evidence does not establish the current fact, behavior, freshness, or promotion state. |
| production ready | A separate release/operations decision with its own evidence and risk acceptance; no selected core PASS automatically means this. |
| generated evidence | Output produced by a declared generator from identified inputs; it remains valid only within its freshness/provenance contract and is never hand edited. |
| manually maintained documentation | Versioned reader-facing prose or Change Record maintained by people/agents, bilingual when required, and not a replacement for raw or generated runtime artifacts. |

Known limits are restricted to repository evidence: the selected evidence is an
HTTP/1.1 compact core; extended catalogs are `NOT EXECUTED`; generated report
freshness is uneven; strict post-commit enforcement, CRS, complete HTTP/2/3,
compression/unselected buffers, complete matrix coverage, long-running
resilience, and production readiness are `out_of_scope` unless separate
evidence says otherwise. Capability/compatibility declarations must not be
used to bypass those limits.

## Decision process and related references

Use the bilingual [ADR guidance](decisions/README.md) for durable decisions;
the recommended first decisions are the parent/Framework boundary,
host-neutral `common/`, shared P1--P4 semantics, connector self-sufficiency,
and parent-versus-Framework tests. Do not backfill a large historical ADR set
without a focused decision task.

Read this document before a material architecture, lifecycle, connector, test
boundary, or security change. Then read the current
[architecture](architecture.md), [configuration](configuration.md),
[testing and evidence](testing-and-evidence.md),
[operations and security](operations-and-security.md), applicable connector
guide, current report, and related Change Record. The local Codex context is
only working support; this versioned concept is the product's target-state
source.
