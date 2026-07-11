> Generated file - do not edit manually.
>
> Generated at: `2026-07-11T12:50:57Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/connector_capabilities.py`
> Make target: `capabilities-all-connectors`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `062e5ef84bcb3e385ac7b5335129eb578fe30833`
> Framework SHA: `2414515b17b7853061009f7e8a15563160ba5946`
> Input status: `complete`

# Canonical connector capabilities

**Language:** English | [Deutsch](connector-capabilities.generated.de.md)

This file is rendered deterministically from the six connector-local manifests. It describes host boundaries and implementation states; it does not promote any capability to `verified` without canonical run evidence.

## Capability matrix

| Capability | Apache | NGINX | HAProxy | Envoy | Traefik | lighttpd |
|---|---|---|---|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `implemented_not_asserted` |
| `transport_metadata` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `not_implemented` | `implemented_not_asserted` |
| `request_headers` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `request_body_buffered` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `configured_not_exercised` | `not_implemented` | `not_implemented` |
| `request_body_streaming` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `request_body_incremental_ingest` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `response_headers` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `unsupported_by_host_model` | `unsupported_by_host_model` | `implemented_not_asserted` |
| `response_body_buffered` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `response_body_streaming` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `response_body_incremental_ingest` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `phase1` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `phase2` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `configured_not_exercised` | `not_implemented` | `not_implemented` |
| `phase3` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `unsupported_by_host_model` | `unsupported_by_host_model` | `implemented_not_asserted` |
| `phase4` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `phase4_rule_evaluation` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `phase4_end_of_stream_evaluation` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `phase4_pre_commit_deny` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `late_intervention` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `late_intervention_log_only` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `late_intervention_abort` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `late_intervention_status_metadata` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `content_type_scope` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `header_limits` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `implemented_not_asserted` |
| `request_body_limits` | `not_implemented` | `not_implemented` | `configured_not_exercised` | `configured_not_exercised` | `not_implemented` | `not_implemented` |
| `response_body_limits` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `no_full_response_buffering` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `first_byte_before_response_end` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `http1_content_length` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` |
| `http1_chunked` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` |
| `keep_alive` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` |
| `parallel_requests` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http2` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `unsupported_by_host_model` |
| `client_abort` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `upstream_abort` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `response_body_decompression` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `deny` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `redirect` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `not_implemented` |
| `drop` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `abort_connection` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `log_only` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `transaction_id` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `event_jsonl` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `config_inline_rules` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `config_rules_file` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `config_remote_rules` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |

## Evidence stages

| Stage | Apache | NGINX | HAProxy | Envoy | Traefik | lighttpd |
|---|---|---|---|---|---|---|
| `source_contract` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `compile` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `link` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `config_load` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `start_smoke` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `minimal_runtime_smoke` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `no_crs_baseline` | `supported_not_verified` | `supported_not_verified` | `supported_not_verified` | `supported_not_verified` | `supported_not_verified` | `supported_not_verified` |
| `crs_smoke` | `supported_not_verified` | `supported_not_verified` | `supported_not_verified` | `supported_not_verified` | `supported_not_verified` | `supported_not_verified` |
| `extended_matrix` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |

## Connector details

### Apache

- Host: `apache`
- Integration: `native-httpd-module`
- Metadata: `connectors/apache/metadata.c`
- Source contract: `connectors/apache/metadata.c`, `connectors/apache/src/mod_security3.c`, `connectors/apache/src/msc_filters.c`, `connectors/apache/src/msc_config.c`, `connectors/apache/harness/run_apache_smoke.sh`

Host-model constraints:

- Apache filters borrow the current request/response buckets and pass them onward; libmodsecurity body-rule evaluation may still complete only at EOS, so this is incremental ingestion rather than per-chunk rule execution.
- The connector JSONL writer is currently specific to Phase-4 interventions and does not by itself prove canonical event coverage for request-phase decisions.
- A Phase-4 disruptive result can occur after response commitment and is handled by the configured late-intervention policy.

| Capability | State | Canonical reason (from manifest) |
|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | The native request hooks pass Apache client and server addresses and ports to libmodsecurity; no current canonical capability result is attached. |
| `transport_metadata` | `implemented_not_asserted` | The native filters retain status and commit metadata, but canonical transport evidence is pending. |
| `request_headers` | `implemented_not_asserted` | The native module maps Apache request headers and calls the ModSecurity request-header phase; canonical baseline evidence is pending. |
| `request_body_buffered` | `implemented_not_asserted` | The Apache input filter borrows each current request bucket and completes request-body processing at EOS; canonical body evidence is pending. |
| `request_body_streaming` | `not_implemented` | The connector appends body chunks but completes the ModSecurity body phase as a buffered phase rather than exposing streaming phase semantics. |
| `request_body_incremental_ingest` | `implemented_not_asserted` | The input filter borrows and appends each Apache bucket and finalizes Phase 2 only at EOS; a real-host capability run is pending. |
| `response_headers` | `implemented_not_asserted` | The Apache output filter maps response headers and invokes the response-header phase; canonical Phase-3 evidence is pending. |
| `response_body_buffered` | `implemented_not_asserted` | The output filter appends bounded current response bytes and invokes response-body processing at EOS without retaining a cross-call brigade; canonical Phase-4 evidence is pending. |
| `response_body_streaming` | `not_implemented` | The connector does not claim per-chunk Phase-4 rule evaluation: libmodsecurity may evaluate when the EOS finish call occurs. |
| `response_body_incremental_ingest` | `implemented_not_asserted` | The output filter inspects only the current bucket and passes each brigade onward without retaining a response body; runtime evidence is pending. |
| `phase1` | `implemented_not_asserted` | The early request hook processes URI and request headers before request handling; the canonical Phase-1 baseline has not been run here. |
| `phase2` | `implemented_not_asserted` | The late request hook and input filter complete request-body processing; canonical Phase-2 evidence is pending. |
| `phase3` | `implemented_not_asserted` | The output filter invokes response-header processing before body processing; canonical Phase-3 evidence is pending. |
| `phase4` | `implemented_not_asserted` | The output filter incrementally ingests current body buckets and invokes response-body processing once at EOS; canonical Phase-4 evidence is pending. |
| `phase4_rule_evaluation` | `implemented_not_asserted` | The native output-filter path is wired for incremental ingestion and EOS response-body processing, but no current canonical real-host run proves that Phase-4 rule 1100301 was evaluated. |
| `phase4_end_of_stream_evaluation` | `implemented_not_asserted` | The output filter invokes response-body processing once after its EOS bucket; canonical Phase-4 evidence is pending. |
| `phase4_pre_commit_deny` | `implemented_not_asserted` | The output-filter intervention path has a denial branch, but no current canonical evidence proves a Phase-4 deny before response commitment with a changed visible client status. |
| `late_intervention` | `implemented_not_asserted` | Phase-4 minimal, safe, and strict policy branches distinguish log-only, status denial, and post-commit connection abort; behavioral evidence is pending. |
| `late_intervention_log_only` | `implemented_not_asserted` | The configured safe late-intervention branch is intended to preserve the committed response and record a log-only result, but no canonical event proves requested deny, actual log_only, and an unchanged visible status. |
| `late_intervention_abort` | `implemented_not_asserted` | The configured strict late-intervention branch has a controlled connection-abort path, but no canonical real-host event proves actual abort_connection and connection_aborted=true. |
| `late_intervention_status_metadata` | `implemented_not_asserted` | Phase-4 metadata wiring exists, but no canonical event yet proves separate requested WAF status, original host status, visible client status, requested action, and actual action. |
| `content_type_scope` | `implemented_not_asserted` | The native Phase-4 path checks configured response Content-Type scope before it appends body bytes; evidence is pending. |
| `header_limits` | `not_implemented` | No canonical Apache host-header-limit enforcement case is implemented in the full-lifecycle catalog. |
| `request_body_limits` | `not_implemented` | No connector-local configurable request-body limit action is implemented for the Apache streaming filter. |
| `response_body_limits` | `implemented_not_asserted` | The Phase-4 body limit bounds bytes passed to libmodsecurity, but no canonical limit evidence is attached. |
| `no_full_response_buffering` | `implemented_not_asserted` | The output filter no longer keeps a connector-owned brigade across calls, but a synchronized host runtime proof is pending. |
| `first_byte_before_response_end` | `implemented_not_asserted` | Pass-through source wiring exists, but the canonical synchronized first-byte proof has not run. |
| `http1_content_length` | `configured_not_exercised` | Apache can serve HTTP/1.1 responses; this transport case has not been exercised by the canonical catalog. |
| `http1_chunked` | `configured_not_exercised` | Apache filter wiring can receive chunked output, but no canonical transport result is attached. |
| `keep_alive` | `configured_not_exercised` | No canonical sequential-request keep-alive run is attached. |
| `parallel_requests` | `not_implemented` | The full-lifecycle parallel-request evidence path is not implemented. |
| `http2` | `configured_not_exercised` | No Apache HTTP/2 full-lifecycle run is attached. |
| `client_abort` | `not_implemented` | No canonical Apache client-abort lifecycle case is implemented. |
| `upstream_abort` | `not_implemented` | No canonical Apache upstream-abort lifecycle case is implemented. |
| `response_body_decompression` | `not_implemented` | The connector has no verified response-body decompression contract. |
| `deny` | `implemented_not_asserted` | Disruptive ModSecurity statuses are returned through the Apache hook/filter path; canonical deny evidence is pending. |
| `redirect` | `implemented_not_asserted` | The intervention mapper sets Apache Location output and returns supported redirect statuses; canonical redirect evidence is pending. |
| `drop` | `not_implemented` | The Apache intervention mapper does not preserve a distinct ModSecurity drop action. |
| `abort_connection` | `implemented_not_asserted` | Strict Phase-4 policy has an explicit post-commit connection-abort path; transport-level canonical evidence is pending. |
| `log_only` | `implemented_not_asserted` | Non-disruptive rules remain allowed and Phase-4 policy can record log-only outcomes; canonical evidence is pending. |
| `transaction_id` | `implemented_not_asserted` | Static and Apache-expression transaction IDs are wired into transaction creation; canonical event correlation evidence is pending. |
| `event_jsonl` | `implemented_not_asserted` | A bounded common JSONL event serializer is used for Phase-4 interventions, but request-phase event coverage must still be exercised. |
| `config_inline_rules` | `implemented_not_asserted` | The modsecurity_rules directive loads inline rules through libmodsecurity; canonical config-load evidence is pending. |
| `config_rules_file` | `implemented_not_asserted` | The modsecurity_rules_file directive loads local rules files; canonical positive and negative config evidence is pending. |
| `config_remote_rules` | `implemented_not_asserted` | The modsecurity_rules_remote directive is wired to libmodsecurity; no remote-network capability is asserted by the no-CRS baseline. |

### NGINX

- Host: `nginx`
- Integration: `native-nginx-http-module`
- Metadata: `connectors/nginx/metadata.c`
- Source contract: `connectors/nginx/metadata.c`, `connectors/nginx/src/ngx_http_modsecurity_access.c`, `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`, `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`, `connectors/nginx/src/ngx_http_modsecurity_module.c`, `connectors/nginx/harness/run_nginx_smoke.sh`

Host-model constraints:

- NGINX request and response body filters feed bounded body data into a completed ModSecurity phase; they do not provide streaming phase semantics.
- The connector JSONL writer is currently specific to Phase-4 interventions and does not by itself prove canonical event coverage for request-phase decisions.
- A Phase-4 decision can be observed after NGINX has sent response headers and is then governed by the late-intervention policy.

| Capability | State | Canonical reason (from manifest) |
|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | The native request path maps NGINX connection endpoints into the ModSecurity transaction; canonical evidence is pending. |
| `transport_metadata` | `implemented_not_asserted` | The native filters retain response status and commitment state, but no canonical transport run has recorded it. |
| `request_headers` | `implemented_not_asserted` | The access handler maps NGINX request headers and invokes request-header processing; canonical evidence is pending. |
| `request_body_buffered` | `implemented_not_asserted` | The request-body callback appends buffered NGINX body buffers and completes Phase 2; canonical body evidence is pending. |
| `request_body_streaming` | `not_implemented` | Body buffers are accumulated for a completed request-body phase rather than exposed as streaming ModSecurity phase execution. |
| `request_body_incremental_ingest` | `not_implemented` | The native request-body callback begins after NGINX has collected the host request body; it is not a real incremental host-ingestion path. |
| `response_headers` | `implemented_not_asserted` | The NGINX header filter invokes response-header processing; canonical Phase-3 evidence is pending. |
| `response_body_buffered` | `implemented_not_asserted` | The bounded body filter invokes response-body processing and applies the configured Phase-4 policy; canonical evidence is pending. |
| `response_body_streaming` | `not_implemented` | Response chains are inspected through bounded buffering and do not expose streaming Phase-4 semantics. |
| `response_body_incremental_ingest` | `implemented_not_asserted` | The body filter appends each current NGINX buffer without retaining a cross-call response body, but no native-host evidence run is attached. |
| `phase1` | `implemented_not_asserted` | The access handler processes URI and request headers before upstream handling; canonical Phase-1 evidence is pending. |
| `phase2` | `implemented_not_asserted` | The request-body callback completes ModSecurity request-body processing; canonical Phase-2 evidence is pending. |
| `phase3` | `implemented_not_asserted` | The response header filter invokes ModSecurity Phase 3; canonical behavioral evidence is pending. |
| `phase4` | `implemented_not_asserted` | The response body filter invokes bounded ModSecurity Phase 4; canonical behavioral evidence is pending. |
| `phase4_rule_evaluation` | `implemented_not_asserted` | The bounded native response-body filter is wired to invoke Phase 4, but no current canonical real-host run proves that Phase-4 rule 1100301 was evaluated. |
| `phase4_end_of_stream_evaluation` | `implemented_not_asserted` | The body filter finalizes response-body processing once at last_buf or last_in_chain; canonical host evidence is pending. |
| `phase4_pre_commit_deny` | `not_implemented` | The native Phase-4 decision runs in the NGINX body filter after the response-header path; this connector has no demonstrated pre-commit response-body decision point, so a visible Phase-4 HTTP 403 must not be claimed. |
| `late_intervention` | `implemented_not_asserted` | The body filter distinguishes pre-header denial from post-header log-only or connection-abort policy outcomes; canonical evidence is pending. |
| `late_intervention_log_only` | `implemented_not_asserted` | The safe post-commit policy is wired to record a log-only outcome, but no canonical event proves requested deny, actual log_only, late_intervention=true, and an unchanged visible status. |
| `late_intervention_abort` | `implemented_not_asserted` | The strict post-commit policy has an abort path, but no canonical real-host event proves actual abort_connection and connection_aborted=true. |
| `late_intervention_status_metadata` | `implemented_not_asserted` | The Phase-4 path can emit intervention metadata, but no canonical event yet proves separate requested WAF status, original host status, visible client status, requested action, and actual action. |
| `content_type_scope` | `implemented_not_asserted` | The Phase-4 filter checks its configured response Content-Type scope before appending body bytes; real-host coverage is pending. |
| `header_limits` | `not_implemented` | No canonical NGINX connector path asserts the shared header-limit behavior in the full-lifecycle catalog. |
| `request_body_limits` | `not_implemented` | The current request-body path is host-buffered and has no connector-level incremental limit outcome contract. |
| `response_body_limits` | `implemented_not_asserted` | The response filter bounds bytes supplied to ModSecurity with the configured Phase-4 limit, but limit-mode evidence is pending. |
| `no_full_response_buffering` | `implemented_not_asserted` | The response filter processes and forwards current chain buffers rather than accumulating a connector-owned full response; synchronized proof is pending. |
| `first_byte_before_response_end` | `implemented_not_asserted` | The pass-through filter wiring permits downstream delivery before end of stream, but the synchronized first-byte test has not run. |
| `http1_content_length` | `configured_not_exercised` | The native NGINX module can run behind HTTP/1.1 Content-Length responses, but the canonical transport case has not run. |
| `http1_chunked` | `configured_not_exercised` | The body-filter path can receive HTTP/1.1 chunked response buffers, but no canonical transport result is attached. |
| `keep_alive` | `configured_not_exercised` | No canonical sequential-request keep-alive run is attached to the native module. |
| `parallel_requests` | `not_implemented` | The canonical parallel full-lifecycle isolation evidence path is not implemented for this connector. |
| `http2` | `configured_not_exercised` | The module can be built into an HTTP/2-capable NGINX host, but no canonical HTTP/2 lifecycle evidence is attached. |
| `client_abort` | `not_implemented` | No native NGINX client-abort cleanup case currently records the canonical transport metadata. |
| `upstream_abort` | `not_implemented` | No native NGINX upstream-abort cleanup case currently records the canonical transport metadata. |
| `response_body_decompression` | `not_implemented` | The connector has no asserted response-body decompression contract. |
| `deny` | `implemented_not_asserted` | Disruptive statuses are returned from access and filter phases; canonical deny evidence is pending. |
| `redirect` | `implemented_not_asserted` | The intervention mapper creates an NGINX Location header and returns redirect status before headers are sent; canonical evidence is pending. |
| `drop` | `not_implemented` | The NGINX intervention mapper does not preserve a distinct ModSecurity drop action. |
| `abort_connection` | `implemented_not_asserted` | The strict Phase-4 branch has an explicit connection-abort outcome after headers are sent; transport evidence is pending. |
| `log_only` | `implemented_not_asserted` | Non-disruptive rules pass and late Phase-4 policy records log-only outcomes; canonical evidence is pending. |
| `transaction_id` | `implemented_not_asserted` | NGINX complex-value transaction IDs are used when creating transactions; canonical event correlation evidence is pending. |
| `event_jsonl` | `implemented_not_asserted` | The Phase-4 filter serializes bounded common JSONL events, but request-phase canonical event coverage is not yet asserted. |
| `config_inline_rules` | `implemented_not_asserted` | The modsecurity_rules directive loads inline rules through libmodsecurity; canonical config evidence is pending. |
| `config_rules_file` | `implemented_not_asserted` | The modsecurity_rules_file directive loads local rules files; canonical positive and negative evidence is pending. |
| `config_remote_rules` | `implemented_not_asserted` | The modsecurity_rules_remote directive is wired to libmodsecurity; the no-CRS baseline does not exercise external networking. |

### HAProxy

- Host: `haproxy`
- Integration: `spoe-spop-agent`
- Metadata: `connectors/haproxy/metadata.c`
- Source contract: `connectors/haproxy/metadata.c`, `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`, `connectors/haproxy/src/haproxy_modsecurity_binding.c`, `connectors/haproxy/src/haproxy_modsecurity_mapper.c`, `connectors/haproxy/harness/run_haproxy_smoke.sh`

Host-model constraints:

- HAProxy and the repository-owned SPOP agent are separate processes; host and agent liveness and logs are distinct evidence.
- Response phases run only when the HAProxy configuration sends the corresponding response notification to the agent.
- The selected SPOE/SPOP configuration sends response headers only; the prior wait-for-body response sample is deliberately disabled because it is not a low-latency response stream.
- Starter and binding self-tests are not HAProxy host-runtime evidence.

| Capability | State | Canonical reason (from manifest) |
|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | The SPOP request message carries client and server endpoints into the libmodsecurity binding; canonical evidence is pending. |
| `transport_metadata` | `not_implemented` | SPOP decision messages do not expose client-visible response commitment, stream lifecycle, or transport-outcome metadata. |
| `request_headers` | `implemented_not_asserted` | HAProxy request headers are encoded in the SPOP message and mapped into the transaction; canonical evidence is pending. |
| `request_body_buffered` | `implemented_not_asserted` | The HAProxy configuration buffers the request and passes a bounded req.body sample to the agent; canonical Phase-2 evidence is pending. |
| `request_body_streaming` | `not_implemented` | The current SPOP message carries one bounded body sample rather than a streaming body protocol. |
| `request_body_incremental_ingest` | `not_implemented` | The current SPOP request message carries one bounded req.body sample rather than incrementally ingested request chunks. |
| `response_headers` | `implemented_not_asserted` | An optional HAProxy response-check message maps response headers and the agent invokes Phase 3; canonical host evidence is pending. |
| `response_body_buffered` | `not_implemented` | The selected SPOE/SPOP host configuration deliberately does not send response bodies; the former wait-for-body sample was disabled because it violates the low-latency contract. |
| `response_body_streaming` | `not_implemented` | The selected SPOE/SPOP configuration has no wired native response-chunk callback or streaming transaction protocol; the optional HTX observer source is nonselected and bodyless-request-only. |
| `response_body_incremental_ingest` | `not_implemented` | No native HAProxy response-chunk callback is wired into the selected SPOP path; an optional source-only HTX observer exists but explicitly bypasses body-bearing requests. |
| `phase1` | `implemented_not_asserted` | The request-check group executes connection, URI, and request-header processing in the agent; canonical evidence is pending. |
| `phase2` | `implemented_not_asserted` | The agent appends the bounded request body and invokes request-body processing; canonical evidence is pending. |
| `phase3` | `implemented_not_asserted` | The optional response-check group invokes response-header processing; canonical host evidence is pending. |
| `phase4` | `not_implemented` | No native HAProxy response-body callback is wired into the selected SPOE/SPOP host configuration; the optional HTX observer source is not selected or canonical evidence. |
| `phase4_rule_evaluation` | `not_implemented` | Without a native HAProxy response-body stream, Phase-4 rule evaluation must not be claimed from the disabled response sample. |
| `phase4_end_of_stream_evaluation` | `not_implemented` | The selected host configuration has no response-body stream or end-of-stream signal for Phase-4 completion. |
| `phase4_pre_commit_deny` | `not_implemented` | The current agent emits policy-derived pre-commit fields but the HAProxy host runner does not capture a client-visible Phase-4 deny and actual commitment timing, so this semantic capability is not implemented. |
| `late_intervention` | `not_implemented` | The current SPOE/SPOP response decision path is modeled before response commitment and implements no post-commit late-intervention point. |
| `late_intervention_log_only` | `not_implemented` | The current HAProxy/SPOA path has no post-commit log-only action or host-observed unchanged-visible-status result. |
| `late_intervention_abort` | `not_implemented` | The current HAProxy/SPOA path implements no controlled post-commit abort_connection action and no host-observed connection-abort result. |
| `late_intervention_status_metadata` | `not_implemented` | Current diagnostics are policy-derived and the host runner does not capture original and visible client statuses plus actual commitment timing, so semantic late-intervention status metadata is not implemented. |
| `content_type_scope` | `not_implemented` | The experimental bounded response-sample branch does not implement a canonical Content-Type scope gate. |
| `header_limits` | `not_implemented` | No connector-local HAProxy/SPOP header-limit enforcement contract is implemented. |
| `request_body_limits` | `configured_not_exercised` | The SPOP request-body sample is bounded by configuration, but no canonical host limit case has exercised its behavior. |
| `response_body_limits` | `not_implemented` | No selected HAProxy response-body path exists on which to enforce a response-body limit. |
| `no_full_response_buffering` | `not_implemented` | No native HAProxy response-body path exists yet to prove the required no-full-response-buffering contract. |
| `first_byte_before_response_end` | `not_implemented` | No native HAProxy response-body path exists yet to observe a client first byte before upstream end of stream. |
| `http1_content_length` | `configured_not_exercised` | HAProxy can proxy HTTP/1.1 responses, but no canonical SPOP host transport case covers Content-Length handling. |
| `http1_chunked` | `configured_not_exercised` | HAProxy can proxy chunked HTTP/1.1 responses, but no canonical SPOP host transport case covers them. |
| `keep_alive` | `configured_not_exercised` | No canonical sequential-request keep-alive run is attached to the HAProxy/SPOP path. |
| `parallel_requests` | `not_implemented` | The HAProxy/SPOP full-lifecycle catalog has no parallel-request evidence path. |
| `http2` | `configured_not_exercised` | HAProxy HTTP/2 transport behavior is not exercised by a canonical SPOP full-lifecycle case. |
| `client_abort` | `not_implemented` | No HAProxy/SPOP client-abort lifecycle case or host-observed outcome is implemented. |
| `upstream_abort` | `not_implemented` | No HAProxy/SPOP upstream-abort lifecycle case or host-observed outcome is implemented. |
| `response_body_decompression` | `not_implemented` | The selected SPOE/SPOP configuration has no response-body decompression contract. |
| `deny` | `implemented_not_asserted` | The agent exports blocked/status variables and HAProxy maps them to explicit deny rules; canonical evidence is pending. |
| `redirect` | `implemented_not_asserted` | The agent exports redirect URL/action variables and HAProxy has an explicit request redirect rule; canonical evidence is pending. |
| `drop` | `not_implemented` | Although the harness contains a silent-drop host rule, the libmodsecurity binding does not currently preserve a distinct drop action into agent variables. |
| `abort_connection` | `not_implemented` | The production binding does not expose a distinct abort-connection decision across SPOP. |
| `log_only` | `implemented_not_asserted` | Non-disruptive ModSecurity decisions leave the HAProxy request allowed; explicit log-only behavioral evidence is pending. |
| `transaction_id` | `implemented_not_asserted` | HAProxy unique IDs are carried as request IDs into the transaction and decision log; canonical correlation evidence is pending. |
| `event_jsonl` | `implemented_not_asserted` | The production SPOP agent writes bounded metadata-only decision JSONL; canonical event-field and payload-absence evidence is pending. |
| `config_inline_rules` | `not_implemented` | Inline rules are used only by binding self-tests and are not exposed by the production HAProxy/SPOP configuration path. |
| `config_rules_file` | `implemented_not_asserted` | The production agent accepts a startup rules file and loads it into libmodsecurity; canonical config evidence is pending. |
| `config_remote_rules` | `not_implemented` | The production HAProxy/SPOP configuration has no remote-rules option. |

### Envoy

- Host: `envoy`
- Integration: `http-ext-authz-service`
- Metadata: `connectors/envoy/metadata.c`
- Source contract: `connectors/envoy/metadata.c`, `connectors/envoy/config/envoy-ext-authz-smoke.yaml.in`, `connectors/envoy/config/envoy-ext-authz.conf`, `connectors/envoy/src/envoy_ext_authz_service_main.c`, `connectors/envoy/src/envoy_modsecurity_mapper.c`, `connectors/envoy/harness/run_envoy_connector_runtime.sh`

Host-model constraints:

- The selected Envoy HTTP ext_authz service observes a pre-upstream authorization request and cannot inspect the later upstream response headers or body.
- The checked-in ext_authz configuration buffers at most 4096 request-body bytes with partial messages disabled; the existing minimal smoke sends no request body.
- Only the headers allowed by the ext_authz authorization_request configuration are forwarded to the authorization service.
- The authorization service currently sees the Envoy-to-service socket endpoints and does not map original downstream connection endpoints into Common connection metadata.

| Capability | State | Canonical reason (from manifest) |
|---|---|---|
| `connection_metadata` | `not_implemented` | The HTTP authorization service maps its local Envoy peer socket rather than the original downstream connection metadata. |
| `transport_metadata` | `not_implemented` | The pre-upstream ext_authz service does not observe client-visible upstream-response commitment or transport outcomes. |
| `request_headers` | `implemented_not_asserted` | The ext_authz HTTP request forwards an allowlisted header set into the Common Runtime mapper; canonical header coverage is pending. |
| `request_body_buffered` | `configured_not_exercised` | Envoy with_request_body and the connector buffered body mode are both configured at 4096 bytes, but the existing host smoke sends no body. |
| `request_body_streaming` | `unsupported_by_host_model` | The selected ext_authz integration deliberately uses the with_request_body buffered authorization request, not a streaming body protocol. |
| `request_body_incremental_ingest` | `unsupported_by_host_model` | The selected ext_authz integration uses a bounded buffered authorization body, not incremental request-body ingestion. |
| `response_headers` | `unsupported_by_host_model` | HTTP ext_authz runs before the upstream request and does not receive the later upstream response headers. |
| `response_body_buffered` | `unsupported_by_host_model` | HTTP ext_authz does not receive the later upstream response body. |
| `response_body_streaming` | `unsupported_by_host_model` | HTTP ext_authz does not receive an upstream response body stream. |
| `response_body_incremental_ingest` | `unsupported_by_host_model` | The pre-upstream ext_authz service never receives an upstream response-body stream. |
| `phase1` | `implemented_not_asserted` | The authorization service maps request headers into the Common Runtime Phase-1 path; a canonical baseline result is pending. |
| `phase2` | `configured_not_exercised` | Buffered request-body forwarding and Common Runtime Phase 2 are configured, but no existing host smoke proves that Envoy delivered the body. |
| `phase3` | `unsupported_by_host_model` | The pre-upstream ext_authz call cannot inspect upstream response headers. |
| `phase4` | `unsupported_by_host_model` | The pre-upstream ext_authz call cannot inspect upstream response bodies. |
| `phase4_rule_evaluation` | `unsupported_by_host_model` | The selected Envoy ext_authz integration executes before the upstream response and does not expose upstream response-body data for Phase-4 rule evaluation. |
| `phase4_end_of_stream_evaluation` | `unsupported_by_host_model` | HTTP ext_authz never receives the later upstream response stream or its end-of-stream event. |
| `phase4_pre_commit_deny` | `unsupported_by_host_model` | Because ext_authz never sees the later upstream response, it has no Phase-4 response point at which to deny before the response commits. |
| `late_intervention` | `unsupported_by_host_model` | The authorization decision completes before the upstream response starts, so there is no response-phase late intervention point. |
| `late_intervention_log_only` | `unsupported_by_host_model` | The selected pre-upstream ext_authz host model has no committed upstream response on which to apply a late log-only intervention. |
| `late_intervention_abort` | `unsupported_by_host_model` | The selected pre-upstream ext_authz host model has no upstream response-phase point from which the authorization service can perform a late connection abort. |
| `late_intervention_status_metadata` | `unsupported_by_host_model` | The selected ext_authz integration does not observe an upstream response, so it cannot produce Phase-4 metadata that distinguishes original and visible upstream-response status or late actions. |
| `content_type_scope` | `unsupported_by_host_model` | The selected ext_authz path does not receive an upstream response Content-Type or response body to scope. |
| `header_limits` | `not_implemented` | The ext_authz header allowlist is not a connector-local canonical header-limit enforcement contract. |
| `request_body_limits` | `configured_not_exercised` | Envoy with_request_body is configured with a 4096-byte bound, but no canonical host limit case has exercised it. |
| `response_body_limits` | `unsupported_by_host_model` | HTTP ext_authz does not receive an upstream response body on which to enforce a response-body limit. |
| `no_full_response_buffering` | `unsupported_by_host_model` | The request-only ext_authz host model has no upstream response stream for this property to describe. |
| `first_byte_before_response_end` | `unsupported_by_host_model` | The request-only ext_authz service cannot observe an Envoy client first byte or upstream response end. |
| `http1_content_length` | `configured_not_exercised` | Envoy can proxy HTTP/1.1 responses, but no canonical ext_authz transport case covers Content-Length handling. |
| `http1_chunked` | `configured_not_exercised` | Envoy can proxy chunked HTTP/1.1 responses, but no canonical ext_authz transport case covers them. |
| `keep_alive` | `configured_not_exercised` | No canonical sequential-request keep-alive run is attached to the Envoy ext_authz path. |
| `parallel_requests` | `not_implemented` | The Envoy ext_authz full-lifecycle catalog has no parallel-request evidence path. |
| `http2` | `configured_not_exercised` | Envoy HTTP/2 transport behavior is not exercised by a canonical ext_authz full-lifecycle case. |
| `client_abort` | `unsupported_by_host_model` | The external authorization service cannot observe or directly control an Envoy downstream client-abort lifecycle. |
| `upstream_abort` | `unsupported_by_host_model` | The pre-upstream authorization service cannot observe or control an upstream response-abort lifecycle. |
| `response_body_decompression` | `unsupported_by_host_model` | HTTP ext_authz does not receive an upstream response body to decompress. |
| `deny` | `implemented_not_asserted` | A disruptive Common Runtime decision is returned as a non-2xx ext_authz response; a fresh canonical deny result is pending. |
| `redirect` | `not_implemented` | The Common Runtime preserves redirect status and URL, but the repository HTTP authorization response does not emit the Location header. |
| `drop` | `unsupported_by_host_model` | The HTTP authorization contract returns an authorization response and cannot directly silent-drop the downstream connection. |
| `abort_connection` | `unsupported_by_host_model` | The external authorization service cannot directly abort Envoy's downstream connection as a ModSecurity action. |
| `log_only` | `implemented_not_asserted` | A non-disruptive rule leaves the authorization response successful; explicit canonical log-only evidence is pending. |
| `transaction_id` | `implemented_not_asserted` | The configured x-request-id header is resolved by Common Runtime and included in decision events; canonical correlation evidence is pending. |
| `event_jsonl` | `implemented_not_asserted` | Common Runtime writes bounded metadata-only disruptive-decision JSONL; canonical field and payload-absence evidence is pending. |
| `config_inline_rules` | `implemented_not_asserted` | The repository HTTP authorization service configuration parser and Common Runtime support inline rules; canonical config evidence is pending. |
| `config_rules_file` | `implemented_not_asserted` | The checked-in service path loads a local rules file through Common Runtime; canonical config evidence is pending. |
| `config_remote_rules` | `implemented_not_asserted` | Common Runtime exposes remote rule key and URL configuration, but the no-CRS baseline does not exercise external networking. |

### Traefik

- Host: `traefik`
- Integration: `http-forwardauth-service`
- Metadata: `connectors/traefik/metadata.c`
- Source contract: `connectors/traefik/metadata.c`, `connectors/traefik/config/traefik-forwardauth-dynamic.yaml`, `connectors/traefik/config/traefik-forwardauth.conf`, `connectors/traefik/src/traefik_forwardauth_service_main.c`, `connectors/traefik/src/traefik_modsecurity_mapper.c`, `connectors/traefik/scripts/runtime_smoke.py`

Host-model constraints:

- The selected forwardAuth service observes the authorization request before the upstream request and cannot inspect the later upstream response headers or body.
- Traefik v3.7 supports buffered forwardAuth request bodies with forwardBody and maxBodySize, but the checked-in dynamic configuration does not enable them and the service config sets request_body_mode=none.
- Traefik documents that forwardBody buffering breaks streaming, so streaming request-body inspection is outside this host path.
- The authorization service currently sees the Traefik-to-service socket endpoints and does not map original client connection endpoints into Common connection metadata.

| Capability | State | Canonical reason (from manifest) |
|---|---|---|
| `connection_metadata` | `not_implemented` | The HTTP authorization service maps its local Traefik peer socket rather than the original client connection metadata. |
| `transport_metadata` | `not_implemented` | The pre-upstream forwardAuth service does not observe client-visible upstream-response commitment or transport outcomes. |
| `request_headers` | `implemented_not_asserted` | Configured forwardAuth request headers are mapped into Common Runtime; canonical multi-header and limit evidence is pending. |
| `request_body_buffered` | `not_implemented` | Traefik v3.7 supports forwardBody plus maxBodySize, but the checked-in middleware omits both and the connector config disables request bodies; see the versioned official reference. |
| `request_body_streaming` | `unsupported_by_host_model` | Traefik v3.7 documents that forwardBody reads and buffers the body before forwarding and therefore breaks streaming. |
| `request_body_incremental_ingest` | `unsupported_by_host_model` | The selected forwardAuth path disables request bodies, and Traefik forwardBody is buffered rather than incremental when enabled. |
| `response_headers` | `unsupported_by_host_model` | forwardAuth runs before the upstream request and does not receive the later upstream response headers. |
| `response_body_buffered` | `unsupported_by_host_model` | forwardAuth does not receive the later upstream response body. |
| `response_body_streaming` | `unsupported_by_host_model` | forwardAuth does not receive an upstream response body stream. |
| `response_body_incremental_ingest` | `unsupported_by_host_model` | The pre-upstream forwardAuth service never receives an upstream response-body stream. |
| `phase1` | `implemented_not_asserted` | The forwardAuth request headers enter the Common Runtime Phase-1 path; a fresh canonical baseline result is pending. |
| `phase2` | `not_implemented` | The checked-in host middleware does not set forwardBody and the connector config disables request-body processing. |
| `phase3` | `unsupported_by_host_model` | The pre-upstream forwardAuth call cannot inspect upstream response headers. |
| `phase4` | `unsupported_by_host_model` | The pre-upstream forwardAuth call cannot inspect upstream response bodies. |
| `phase4_rule_evaluation` | `unsupported_by_host_model` | The selected Traefik forwardAuth integration runs before upstream handling and cannot inspect the later upstream response body for Phase-4 rule evaluation. |
| `phase4_end_of_stream_evaluation` | `unsupported_by_host_model` | forwardAuth never receives the later upstream response stream or its end-of-stream event. |
| `phase4_pre_commit_deny` | `unsupported_by_host_model` | Because forwardAuth never sees the later upstream response, it has no Phase-4 response point at which to deny before the response commits. |
| `late_intervention` | `unsupported_by_host_model` | The authorization decision completes before the upstream response starts, so the chosen path has no response-phase late intervention point. |
| `late_intervention_log_only` | `unsupported_by_host_model` | The selected pre-upstream forwardAuth host model has no committed upstream response on which to apply a late log-only intervention. |
| `late_intervention_abort` | `unsupported_by_host_model` | The selected pre-upstream forwardAuth host model has no upstream response-phase point from which the authorization service can perform a late connection abort. |
| `late_intervention_status_metadata` | `unsupported_by_host_model` | The selected forwardAuth integration does not observe an upstream response, so it cannot produce Phase-4 metadata that distinguishes original and visible upstream-response status or late actions. |
| `content_type_scope` | `unsupported_by_host_model` | The selected forwardAuth path does not receive an upstream response Content-Type or response body to scope. |
| `header_limits` | `not_implemented` | Forwarded request headers have no connector-local canonical header-limit enforcement contract. |
| `request_body_limits` | `not_implemented` | The checked-in forwardAuth middleware disables request-body forwarding and defines no active request-body limit behavior. |
| `response_body_limits` | `unsupported_by_host_model` | forwardAuth does not receive an upstream response body on which to enforce a response-body limit. |
| `no_full_response_buffering` | `unsupported_by_host_model` | The request-only forwardAuth host model has no upstream response stream for this property to describe. |
| `first_byte_before_response_end` | `unsupported_by_host_model` | The request-only forwardAuth service cannot observe a Traefik client first byte or upstream response end. |
| `http1_content_length` | `configured_not_exercised` | Traefik can proxy HTTP/1.1 responses, but no canonical forwardAuth transport case covers Content-Length handling. |
| `http1_chunked` | `configured_not_exercised` | Traefik can proxy chunked HTTP/1.1 responses, but no canonical forwardAuth transport case covers them. |
| `keep_alive` | `configured_not_exercised` | No canonical sequential-request keep-alive run is attached to the Traefik forwardAuth path. |
| `parallel_requests` | `not_implemented` | The Traefik forwardAuth full-lifecycle catalog has no parallel-request evidence path. |
| `http2` | `configured_not_exercised` | Traefik HTTP/2 transport behavior is not exercised by a canonical forwardAuth full-lifecycle case. |
| `client_abort` | `unsupported_by_host_model` | The external authorization service cannot observe or directly control a Traefik client-abort lifecycle. |
| `upstream_abort` | `unsupported_by_host_model` | The pre-upstream authorization service cannot observe or control an upstream response-abort lifecycle. |
| `response_body_decompression` | `unsupported_by_host_model` | forwardAuth does not receive an upstream response body to decompress. |
| `deny` | `implemented_not_asserted` | A disruptive Common Runtime decision is returned as a non-2xx forwardAuth response; a fresh canonical deny result is pending. |
| `redirect` | `not_implemented` | The Common Runtime preserves redirect status and URL, but the repository HTTP authorization response does not emit the Location header for Traefik to propagate. |
| `drop` | `unsupported_by_host_model` | The external HTTP authorization contract returns a response and cannot directly silent-drop Traefik's client connection. |
| `abort_connection` | `unsupported_by_host_model` | The external authorization service cannot directly abort Traefik's client connection as a ModSecurity action. |
| `log_only` | `implemented_not_asserted` | A non-disruptive rule leaves the forwardAuth response successful; explicit canonical log-only evidence is pending. |
| `transaction_id` | `implemented_not_asserted` | The configured x-request-id header is resolved by Common Runtime and included in decision events; canonical correlation evidence is pending. |
| `event_jsonl` | `implemented_not_asserted` | Common Runtime writes bounded metadata-only disruptive-decision JSONL; canonical field and payload-absence evidence is pending. |
| `config_inline_rules` | `implemented_not_asserted` | The repository authorization-service config parser and Common Runtime support inline rules; canonical config evidence is pending. |
| `config_rules_file` | `implemented_not_asserted` | The checked-in service path loads a local rules file through Common Runtime; canonical positive and negative evidence is pending. |
| `config_remote_rules` | `implemented_not_asserted` | Common Runtime exposes remote rule key and URL configuration, but the no-CRS baseline does not exercise external networking. |

### lighttpd

- Host: `lighttpd`
- Integration: `native-lighttpd-plugin`
- Metadata: `connectors/lighttpd/metadata.c`
- Source contract: `connectors/lighttpd/metadata.c`, `connectors/lighttpd/config/lighttpd-native.conf`, `connectors/lighttpd/module/mod_msconnector.c`, `connectors/lighttpd/src/lighttpd_modsecurity_mapper.c`, `connectors/lighttpd/harness/runtime_lighttpd_smoke.sh`

Host-model constraints:

- The native plugin deliberately rejects non-none request and response body modes until safe lighttpd body hooks, limits, buffering, and intervention timing are implemented.
- The response-header mapper is called from handle_response_start, but source wiring alone is not Phase-3 behavioral verification.
- The legacy bridge and starter self-tests are separate from native mod_msconnector.so host-runtime evidence.

| Capability | State | Canonical reason (from manifest) |
|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | The native mapper reads lighttpd client and server socket endpoints into Common Runtime; canonical evidence is pending. |
| `transport_metadata` | `implemented_not_asserted` | The native mapper supplies host endpoint and response-status metadata, but a canonical transport run is pending. |
| `request_headers` | `implemented_not_asserted` | The native URI-clean hook maps lighttpd request headers into Common Runtime; canonical header evidence is pending. |
| `request_body_buffered` | `not_implemented` | The native module requires request_body_mode=none and supplies no request body to the mapper. |
| `request_body_streaming` | `not_implemented` | No native lighttpd request-body hook or streaming transaction contract is implemented. |
| `request_body_incremental_ingest` | `not_implemented` | The native module explicitly disables request-body modes until a safe lighttpd request-body hook exists. |
| `response_headers` | `implemented_not_asserted` | handle_response_start maps response headers into Common Runtime, but a real Phase-3 rule result has not yet been attached. |
| `response_body_buffered` | `not_implemented` | The native module requires response_body_mode=none and supplies no response body to the mapper. |
| `response_body_streaming` | `not_implemented` | No native lighttpd response-body hook or streaming transaction contract is implemented. |
| `response_body_incremental_ingest` | `not_implemented` | The native module explicitly disables response-body modes until a safe lighttpd output hook exists. |
| `phase1` | `implemented_not_asserted` | The URI-clean hook starts the transaction and processes request headers; a fresh canonical Phase-1 result is pending. |
| `phase2` | `not_implemented` | Request bodies are explicitly disabled in the native plugin, so a real Phase-2 body rule cannot run. |
| `phase3` | `implemented_not_asserted` | The response-start hook invokes Common Runtime response processing with mapped headers; real Phase-3 behavioral evidence is pending. |
| `phase4` | `not_implemented` | Response bodies are explicitly disabled in the native plugin, so a real Phase-4 body rule cannot run. |
| `phase4_rule_evaluation` | `not_implemented` | The current native module does not supply response-body data to ModSecurity, so it cannot yet evaluate Phase-4 rule 1100301. |
| `phase4_end_of_stream_evaluation` | `not_implemented` | Without a native response-body hook there is no Phase-4 end-of-stream evaluation path. |
| `phase4_pre_commit_deny` | `not_implemented` | The current native module has no response-body hook or Phase-4 intervention timing implementation from which to deny before response commitment. |
| `late_intervention` | `not_implemented` | The module has no response-body or post-commit intervention policy; the response-start hook is not late-intervention evidence. |
| `late_intervention_log_only` | `not_implemented` | The current native module implements no post-commit response-body intervention policy or log-only late-intervention action. |
| `late_intervention_abort` | `not_implemented` | The current native module implements no response-body late-intervention path that can abort a committed connection. |
| `late_intervention_status_metadata` | `not_implemented` | Without a native response-body Phase-4 path, the module does not yet emit late-intervention metadata separating requested WAF status, original host status, visible client status, requested action, and actual action. |
| `content_type_scope` | `not_implemented` | Content-Type scoping for response-body inspection cannot run while the native response-body path is disabled. |
| `header_limits` | `implemented_not_asserted` | The native request and response mappers apply configured header count and total-size limits, but real-host limit evidence is pending. |
| `request_body_limits` | `not_implemented` | Request bodies are disabled in the native module, so no request-body limit outcome can be enforced. |
| `response_body_limits` | `not_implemented` | Response bodies are disabled in the native module, so no response-body limit outcome can be enforced. |
| `no_full_response_buffering` | `not_implemented` | The module has no response-body path; it must not claim a streaming no-buffer proof before an output hook exists. |
| `first_byte_before_response_end` | `not_implemented` | No native response-body pass-through path exists from which to demonstrate first-byte delivery before end of stream. |
| `http1_content_length` | `configured_not_exercised` | The native plugin can load in a lighttpd HTTP/1.1 host, but the canonical Content-Length transport case has not run. |
| `http1_chunked` | `configured_not_exercised` | The native plugin can load in a lighttpd HTTP/1.1 host, but no canonical chunked transport evidence is attached. |
| `keep_alive` | `configured_not_exercised` | No canonical sequential-request keep-alive run is attached to the native plugin. |
| `parallel_requests` | `not_implemented` | The canonical parallel full-lifecycle isolation evidence path is not implemented for lighttpd. |
| `http2` | `unsupported_by_host_model` | The pinned native lighttpd integration has no asserted HTTP/2 full-lifecycle transport path. |
| `client_abort` | `not_implemented` | No native client-abort cleanup case records canonical transport metadata. |
| `upstream_abort` | `not_implemented` | No native upstream-abort cleanup case records canonical transport metadata. |
| `response_body_decompression` | `not_implemented` | The native plugin has no response-body decompression contract. |
| `deny` | `implemented_not_asserted` | A disruptive Common Runtime decision is mapped to a lighttpd error status in request and response-start hooks; canonical evidence is pending. |
| `redirect` | `not_implemented` | The native decision mapper accepts only error statuses and normalizes redirect statuses to a denial without a Location header. |
| `drop` | `not_implemented` | The native lighttpd decision mapper has no distinct drop action. |
| `abort_connection` | `not_implemented` | The native lighttpd decision mapper has no connection-abort action. |
| `log_only` | `implemented_not_asserted` | Non-disruptive rules leave the lighttpd request or response allowed; explicit canonical log-only evidence is pending. |
| `transaction_id` | `implemented_not_asserted` | The module supplies a host request ID and Common Runtime resolves configured header or fallback transaction IDs; canonical correlation evidence is pending. |
| `event_jsonl` | `implemented_not_asserted` | Common Runtime writes bounded metadata-only disruptive-decision JSONL from the native path; canonical event evidence is pending. |
| `config_inline_rules` | `implemented_not_asserted` | The native plugin uses the Common Runtime config parser, which supports inline rules; canonical config evidence is pending. |
| `config_rules_file` | `implemented_not_asserted` | The native plugin uses the Common Runtime local rules-file path; canonical positive and negative evidence is pending. |
| `config_remote_rules` | `implemented_not_asserted` | The native plugin uses Common Runtime remote rule configuration, but the no-CRS baseline does not exercise external networking. |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `connectors/apache/capabilities.json` | `2ed68f9d9d5b35ac2f1068d53c4e27bb86b3e195e0a4d4aceff68a123c0c12ce` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/nginx/capabilities.json` | `83060ff43bd255140d56f9cc82e617c7baa8d5791bb97208edc099cae2e919b9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/haproxy/capabilities.json` | `bdf6e91e01324d6cb0798fd4c291192896ab2bfc3f998d9c4ca2a2f04f9c6a1f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/envoy/capabilities.json` | `86933a4afae465af6c6318886e314a2dbc67e142063258e58780bbc3cf9eaaed` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/traefik/capabilities.json` | `093a3af50e32603bc4b5c38f55bfbf5e7b9a63169e8ee1fb03ad487be16b9bae` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/lighttpd/capabilities.json` | `c87452f2d0e6cea75b5fbc646212e821a1d47690253ba4049cb3fe3139b40b4f` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `connectors/apache/capabilities.json` | present | input file available |
| `connectors/nginx/capabilities.json` | present | input file available |
| `connectors/haproxy/capabilities.json` | present | input file available |
| `connectors/envoy/capabilities.json` | present | input file available |
| `connectors/traefik/capabilities.json` | present | input file available |
| `connectors/lighttpd/capabilities.json` | present | input file available |
