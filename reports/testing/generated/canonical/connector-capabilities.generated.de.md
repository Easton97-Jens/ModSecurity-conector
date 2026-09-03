> Generated file - do not edit manually.
>
> Generated at: `2026-09-03T03:00:24Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/evidence/collectors/connector_capabilities.py`
> Make target: `capabilities-all-connectors`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `d50fad793a8af1fa4cf0dc83a951c041dcd940e9`
> Framework SHA: `unknown`
> Framework gitlink SHA: `86451b45ae7bb7953baf9f81f2c2dad07395a808`
> Framework checkout: `not_checked_out`
> Framework gitlink status: `not_checked_out`
> Input status: `complete`

> Generierte Datei – nicht manuell bearbeiten.

# Kanonische Connector-Capabilities

**Sprache:** [English](connector-capabilities.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Statusnamen, Pfade und Tabellen bleiben absichtlich unverändert.

Diese Datei wird deterministisch aus den sechs connector-lokalen Manifesten erzeugt. Sie beschreibt Host-Grenzen und Implementierungszustände; sie befördert keine Capability ohne kanonische Lauf-Evidence zu `verified`.

## Capability-Matrix

| Capability | Apache | NGINX | HAProxy | Envoy | Traefik | lighttpd |
|---|---|---|---|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `implemented_not_asserted` |
| `transport_metadata` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `not_implemented` | `implemented_not_asserted` |
| `request_headers` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `request_body_buffered` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `configured_not_exercised` | `configured_not_exercised` | `not_implemented` |
| `request_body_streaming` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `request_body_incremental_ingest` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `response_headers` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `unsupported_by_host_model` | `unsupported_by_host_model` | `implemented_not_asserted` |
| `response_body_buffered` | `not_implemented` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `response_body_streaming` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `response_body_incremental_ingest` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `phase1` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `phase2` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `configured_not_exercised` | `configured_not_exercised` | `not_implemented` |
| `phase3` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `unsupported_by_host_model` | `unsupported_by_host_model` | `implemented_not_asserted` |
| `phase4` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `phase4_rule_evaluation` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `phase4_end_of_stream_evaluation` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `phase4_pre_commit_deny` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `late_intervention` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `late_intervention_log_only` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `late_intervention_abort` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `late_intervention_status_metadata` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `content_type_scope` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `header_limits` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `implemented_not_asserted` |
| `request_body_limits` | `not_implemented` | `not_implemented` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `not_implemented` |
| `response_body_limits` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `no_full_response_buffering` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `first_byte_before_response_end` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `http1_content_length` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` |
| `http1_chunked` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` |
| `keep_alive` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` |
| `parallel_requests` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http2` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `configured_not_exercised` | `unsupported_by_host_model` |
| `http2_downstream` | `not_implemented` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http2_upstream` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http2_tls_alpn` | `not_implemented` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http2_cleartext_h2c` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http2_multiplexing` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http2_stream_reset` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http3_downstream` | `not_implemented` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http3_upstream` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http3_quic` | `not_implemented` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http3_alt_svc` | `not_implemented` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http3_multiplexing` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `http3_stream_reset` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `protocol_transaction_isolation` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `protocol_first_byte_before_response_end` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `protocol_no_full_response_buffering` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` | `not_implemented` |
| `client_abort` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `upstream_abort` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `response_body_decompression` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `deny` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `redirect` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` |
| `drop` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `abort_connection` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `log_only` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `transaction_id` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `event_jsonl` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `config_inline_rules` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `config_rules_file` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `config_remote_rules` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |

## Evidence-Stufen

| Stufe | Apache | NGINX | HAProxy | Envoy | Traefik | lighttpd |
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

## Connector-Details

### Apache

- Host: `apache`
- Integration: `native-httpd-module`
- Metadata: `connectors/apache/metadata.c`
- Source-Contract: `connectors/apache/metadata.c`, `connectors/apache/src/mod_security3.c`, `connectors/apache/src/msc_filters.c`, `connectors/apache/src/msc_config.c`, `connectors/apache/harness/run_apache_smoke.sh`, `ci/runtime/lifecycle/run-apache-phase4-response-regression.sh`

Host-Modell-Grenzen:

- Apache incrementally appends each response-data bucket, preserves pre-EOS FLUSH and metadata, and immediately passes the normalized pre-EOS prefix to the next filter. Only the terminal EOS fragment remains until msc_process_response_body and late-action resolution complete; no full response brigade is retained across filter calls.
- libModSecurity's C API does not expose its effective SecResponseBodyMimeType selection, so Apache gates every response MIME type. The legacy modsecurity_phase4_content_types_file parser is deprecated and cannot narrow that gate; the configurable default 1048576-byte bound is checked before each later append without creating a full-response buffer.
- Normal r->prev and pre-output ErrorDocument redirects fail closed because the connector cannot safely rebind a source transaction to a target URI/ruleset. During terminal output EMITTING, exactly one Apache-core-marked local ErrorDocument hop is allowed with no_local_copy plus matching immediate predecessor status and REDIRECT_STATUS.
- The connector JSONL writer is currently specific to Phase-4 interventions and does not by itself prove canonical event coverage for request-phase decisions.
- Phase-4 rule evaluation remains EOS-only. After a pre-EOS prefix reaches the next filter, Safe records log_only and Strict uses abort_connection rather than attempting to rewrite bytes that may already be visible.

| Capability | Zustand | Kanonischer Grund (aus dem Manifest) |
|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | The native request hooks pass Apache client and server addresses and ports to libmodsecurity; no current canonical capability result is attached. |
| `transport_metadata` | `implemented_not_asserted` | The native filters retain status and commit metadata, but canonical transport evidence is pending. |
| `request_headers` | `implemented_not_asserted` | The native module maps Apache request headers and calls the ModSecurity request-header phase; canonical baseline evidence is pending. |
| `request_body_buffered` | `implemented_not_asserted` | The Apache input filter borrows each current request bucket and completes request-body processing at EOS; canonical body evidence is pending. |
| `request_body_streaming` | `not_implemented` | The connector appends body chunks but completes the ModSecurity body phase as a buffered phase rather than exposing streaming phase semantics. |
| `request_body_incremental_ingest` | `implemented_not_asserted` | The input filter borrows and appends each Apache bucket and finalizes Phase 2 only at EOS; a real-host capability run is pending. |
| `response_headers` | `implemented_not_asserted` | The Apache output filter maps response headers and invokes the response-header phase; canonical Phase-3 evidence is pending. |
| `response_body_buffered` | `not_implemented` | The output filter has no active cross-callback full-response brigade; it uses bounded current buckets plus a terminal EOS fragment. |
| `response_body_streaming` | `implemented_not_asserted` | Each pre-EOS response-data bucket is appended once and its normalized prefix is passed to the next filter immediately; a real-host progressive-output result is pending. |
| `response_body_incremental_ingest` | `implemented_not_asserted` | The output filter appends each data bucket incrementally and passes the normalized pre-EOS prefix to the next filter; runtime evidence is pending. |
| `phase1` | `implemented_not_asserted` | The early request hook processes URI and request headers before request handling; the canonical Phase-1 baseline has not been run here. |
| `phase2` | `implemented_not_asserted` | The late request hook and input filter complete request-body processing; canonical Phase-2 evidence is pending. |
| `phase3` | `implemented_not_asserted` | The output filter invokes response-header processing before body processing; canonical Phase-3 evidence is pending. |
| `phase4` | `implemented_not_asserted` | The output filter incrementally ingests body buckets, forwards the pre-EOS prefix, and invokes response-body processing exactly once on the terminal EOS fragment; canonical real-host evidence is pending. |
| `phase4_rule_evaluation` | `implemented_not_asserted` | The native output-filter path is wired for incremental ingestion and one terminal EOS evaluation, but no current canonical real-host run proves that Phase-4 rule 1100301 was evaluated. |
| `phase4_end_of_stream_evaluation` | `implemented_not_asserted` | The output filter invokes response-body processing exactly once on the terminal EOS fragment after all pre-EOS prefixes have been forwarded; canonical Phase-4 evidence is pending. |
| `phase4_pre_commit_deny` | `not_implemented` | Because the progressive output filter can pass a pre-EOS prefix before the EOS-only P4 decision, it does not claim a reliable pre-commit P4 deny or redirect. |
| `late_intervention` | `implemented_not_asserted` | The output filter resolves disruptive EOS decisions through the shared post-commit policy once a prefix may have reached the next filter; behavioral evidence is pending. |
| `late_intervention_log_only` | `implemented_not_asserted` | The configured safe late-intervention branch preserves a progressively forwarded prefix and records a log-only result; canonical event evidence is pending. |
| `late_intervention_abort` | `implemented_not_asserted` | The configured strict late-intervention branch has a controlled connection-abort path for independently committed output, but no canonical real-host event proves actual abort_connection and connection_aborted=true. |
| `late_intervention_status_metadata` | `implemented_not_asserted` | Phase-4 metadata wiring exists, but no canonical event yet proves separate requested WAF status, original host status, visible client status, requested action, and actual action. |
| `content_type_scope` | `implemented_not_asserted` | SecResponseBodyMimeType selects libModSecurity inspection, but the connector gates every response because the C API cannot expose the effective MIME decision; the deprecated legacy MIME file cannot narrow the gate. Evidence is pending. |
| `header_limits` | `not_implemented` | No canonical Apache host-header-limit enforcement case is implemented in the full-lifecycle catalog. |
| `request_body_limits` | `not_implemented` | No connector-local configurable request-body limit action is implemented for the Apache streaming filter. |
| `response_body_limits` | `implemented_not_asserted` | The configurable default 1048576-byte Phase-4 limit is checked before each later append and does not require a retained full response; canonical limit evidence is pending. |
| `no_full_response_buffering` | `implemented_not_asserted` | The progressive path does not retain a full response brigade across filter calls; only the terminal EOS fragment is held for finalization. |
| `first_byte_before_response_end` | `implemented_not_asserted` | The source passes a normalized pre-EOS prefix to the next filter, but no canonical client-visible first-byte-before-EOS run is attached. |
| `http1_content_length` | `configured_not_exercised` | Apache can serve HTTP/1.1 responses through the progressive Phase-4 source path; the focused H1 run has not yet produced canonical run-scoped evidence. |
| `http1_chunked` | `configured_not_exercised` | Apache filter wiring can receive chunked output, but no canonical transport result is attached. |
| `keep_alive` | `configured_not_exercised` | No canonical sequential-request keep-alive run is attached. |
| `parallel_requests` | `not_implemented` | The full-lifecycle parallel-request evidence path is not implemented. |
| `http2` | `configured_not_exercised` | No Apache HTTP/2 full-lifecycle result is attached; ci/runtime/lifecycle/run-apache-phase4-response-regression.sh is the task-local H1/H2 evidence placeholder, not a pass claim. |
| `http2_downstream` | `not_implemented` | The pinned Apache native-host profile does not yet build and exercise mod_http2 on the connector path. |
| `http2_upstream` | `not_implemented` | No Apache native connector upstream HTTP/2 profile is implemented. |
| `http2_tls_alpn` | `not_implemented` | The pinned Apache harness has no TLS/ALPN h2 listener. |
| `http2_cleartext_h2c` | `not_implemented` | The pinned Apache harness has no h2c prior-knowledge listener. |
| `http2_multiplexing` | `not_implemented` | No native Apache HTTP/2 multiplexing isolation evidence path is implemented. |
| `http2_stream_reset` | `not_implemented` | The Apache strict path only models a connection abort; no request-local HTTP/2 stream-reset API is implemented. |
| `http3_downstream` | `not_implemented` | The pinned Apache native host has no audited HTTP/3 module, QUIC listener, or H3 stream path. |
| `http3_upstream` | `not_implemented` | No Apache native connector upstream HTTP/3 profile is implemented. |
| `http3_quic` | `not_implemented` | The pinned Apache native host has no QUIC runtime path. |
| `http3_alt_svc` | `not_implemented` | No native Apache HTTP/3 Alt-Svc profile is configured. |
| `http3_multiplexing` | `not_implemented` | No native Apache HTTP/3 stream-isolation evidence path is implemented. |
| `http3_stream_reset` | `not_implemented` | No Apache H3 stream-reset API has been audited or wired. |
| `protocol_transaction_isolation` | `not_implemented` | Protocol-specific multiplexed transaction-isolation evidence is not implemented. |
| `protocol_first_byte_before_response_end` | `implemented_not_asserted` | The source passes a pre-EOS prefix to the next filter, but no protocol-scoped client-visible first-byte result is attached. |
| `protocol_no_full_response_buffering` | `implemented_not_asserted` | The source does not retain a full normalized response brigade, but no protocol-scoped runtime result is attached. |
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
- Source-Contract: `connectors/nginx/metadata.c`, `connectors/nginx/src/ngx_http_modsecurity_access.c`, `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`, `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`, `connectors/nginx/src/ngx_http_modsecurity_module.c`, `connectors/nginx/harness/run_nginx_smoke.sh`

Host-Modell-Grenzen:

- NGINX receives the request body after host preparation, but its response body filter incrementally feeds each current chain buffer to the active P4 phase and forwards the chain without retaining a cross-callback response body.
- The connector JSONL writer is currently specific to Phase-4 interventions and does not by itself prove canonical event coverage for request-phase decisions.
- A Phase-4 decision can be observed after NGINX has sent response headers and is then governed by the late-intervention policy.

| Capability | Zustand | Kanonischer Grund (aus dem Manifest) |
|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | The native request path maps NGINX connection endpoints into the ModSecurity transaction; canonical evidence is pending. |
| `transport_metadata` | `implemented_not_asserted` | The native filters retain response status and commitment state, but no canonical transport run has recorded it. |
| `request_headers` | `implemented_not_asserted` | The access handler maps NGINX request headers and invokes request-header processing; canonical evidence is pending. |
| `request_body_buffered` | `implemented_not_asserted` | The request-body callback appends buffered NGINX body buffers and completes Phase 2; canonical body evidence is pending. |
| `request_body_streaming` | `not_implemented` | Body buffers are accumulated for a completed request-body phase rather than exposed as streaming ModSecurity phase execution. |
| `request_body_incremental_ingest` | `not_implemented` | The native request-body callback begins after NGINX has collected the host request body; it is not a real incremental host-ingestion path. |
| `response_headers` | `implemented_not_asserted` | The NGINX header filter invokes response-header processing; canonical Phase-3 evidence is pending. |
| `response_body_buffered` | `implemented_not_asserted` | The bounded body filter invokes response-body processing and applies the configured Phase-4 policy; canonical evidence is pending. |
| `response_body_streaming` | `implemented_not_asserted` | The response body filter appends NGINX's memory-authoritative current range or file-only ranges through a reusable bounded scratch buffer to the active P4 phase and forwards the current chain without retaining a connector-owned full response; current native-host evidence is pending. |
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
| `content_type_scope` | `implemented_not_asserted` | The Phase-4 filter checks its configured response Content-Type scope before appending body bytes; out-of-scope response bodies are not appended to libmodsecurity. Real-host coverage is pending. |
| `header_limits` | `not_implemented` | No canonical NGINX connector path asserts the shared header-limit behavior in the full-lifecycle catalog. |
| `request_body_limits` | `not_implemented` | The current request-body path is host-buffered and has no connector-level incremental limit outcome contract. |
| `response_body_limits` | `implemented_not_asserted` | The response filter applies the Common reject body-limit plan before forwarding each in-scope memory or file buffer, but native-host limit-mode evidence is pending. |
| `no_full_response_buffering` | `implemented_not_asserted` | The response filter processes and forwards current chain buffers rather than accumulating a connector-owned full response; file-only ranges use one reusable bounded scratch buffer and synchronized proof is pending. |
| `first_byte_before_response_end` | `implemented_not_asserted` | The pass-through filter wiring permits downstream delivery before end of stream, but the synchronized first-byte test has not run. |
| `http1_content_length` | `configured_not_exercised` | The native NGINX module can run behind HTTP/1.1 Content-Length responses, but the canonical transport case has not run. |
| `http1_chunked` | `configured_not_exercised` | The body-filter path can receive HTTP/1.1 chunked response buffers, but no canonical transport result is attached. |
| `keep_alive` | `configured_not_exercised` | No canonical sequential-request keep-alive run is attached to the native module. |
| `parallel_requests` | `not_implemented` | The canonical parallel full-lifecycle isolation evidence path is not implemented for this connector. |
| `http2` | `configured_not_exercised` | The module can be built into an HTTP/2-capable NGINX host, but the currently pinned canonical host was configured without --with-http_v2_module. No applicable HTTP/2 lifecycle case is attached. |
| `http2_downstream` | `implemented_not_asserted` | The managed NGINX protocol build profile can enable the native HTTP/2 module, but no forced negotiated connector run is attached. |
| `http2_upstream` | `not_implemented` | No native NGINX connector upstream HTTP/2 matrix is implemented. |
| `http2_tls_alpn` | `implemented_not_asserted` | The managed protocol profile can configure TLS and h2 ALPN, but no negotiated client evidence is attached. |
| `http2_cleartext_h2c` | `not_implemented` | No h2c prior-knowledge listener profile is implemented for the native NGINX harness. |
| `http2_multiplexing` | `not_implemented` | No HTTP/2 parallel-stream transaction-isolation runner is implemented. |
| `http2_stream_reset` | `not_implemented` | The current strict filter marks a connection error; it does not prove a stream-local HTTP/2 reset. |
| `http3_downstream` | `implemented_not_asserted` | The managed NGINX protocol profile has an explicit HTTP/3/QUIC build path, but no forced H3 client evidence is attached. |
| `http3_upstream` | `not_implemented` | No native NGINX connector upstream HTTP/3 matrix is implemented. |
| `http3_quic` | `implemented_not_asserted` | The managed profile records a QUIC-capable TLS build input, but it is not runtime QUIC evidence. |
| `http3_alt_svc` | `implemented_not_asserted` | The managed H3 listener template can advertise Alt-Svc, but no forced H3 observation is attached. |
| `http3_multiplexing` | `not_implemented` | No HTTP/3 parallel-stream transaction-isolation runner is implemented. |
| `http3_stream_reset` | `not_implemented` | The current strict path has no proven QUIC stream-reset action. |
| `protocol_transaction_isolation` | `not_implemented` | No negotiated HTTP/2 or HTTP/3 transaction-isolation evidence is implemented. |
| `protocol_first_byte_before_response_end` | `not_implemented` | The existing synchronized first-byte proof is HTTP/1.1-only. |
| `protocol_no_full_response_buffering` | `not_implemented` | No negotiated HTTP/2 or HTTP/3 no-full-buffer proof is implemented. |
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
- Source-Contract: `connectors/haproxy/metadata.c`, `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`, `connectors/haproxy/src/haproxy_modsecurity_binding.c`, `connectors/haproxy/src/haproxy_modsecurity_mapper.c`, `connectors/haproxy/harness/run_haproxy_smoke.sh`, `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`, `connectors/haproxy/htx-overlay/haproxy-makefile.patch`, `connectors/haproxy/harness/run_haproxy_htx_runtime.sh`

Host-Modell-Grenzen:

- HAProxy and the repository-owned SPOP agent are separate processes; host and agent liveness and logs are distinct evidence.
- Response phases run only when the HAProxy configuration sends the corresponding response notification to the agent.
- The selected SPOE/SPOP configuration sends response headers only; the prior wait-for-body response sample is deliberately disabled because it is not a low-latency response stream.
- Starter and binding self-tests are not HAProxy host-runtime evidence.
- The full-lifecycle profile separately selects native-htx-filter through full-lifecycle-haproxy-htx: a patched Framework-synchronized HAProxy non-promoted path with real P1/P2/P3 response outcomes and P4 safe log_only evidence. Its one-block P2 probe returns 403 and records zero or one observed upstream requests without proving their ordering; that does not prove incremental request forwarding or a general host-buffering property. P4 Strict has no client-visible abort evidence and remains NOT EXECUTED.

| Capability | Zustand | Kanonischer Grund (aus dem Manifest) |
|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | The SPOP request message carries client and server endpoints into the libmodsecurity binding; canonical evidence is pending. |
| `transport_metadata` | `not_implemented` | SPOP decision messages do not expose client-visible response commitment, stream lifecycle, or transport-outcome metadata. |
| `request_headers` | `implemented_not_asserted` | HAProxy request headers are encoded in the SPOP message and mapped into the transaction; canonical evidence is pending. |
| `request_body_buffered` | `implemented_not_asserted` | The HAProxy configuration buffers the request and passes a bounded req.body sample to the agent; canonical Phase-2 evidence is pending. |
| `request_body_streaming` | `not_implemented` | The current SPOP message carries one bounded body sample rather than a streaming body protocol. |
| `request_body_incremental_ingest` | `not_implemented` | The current SPOP request message carries one bounded req.body sample rather than incrementally ingested request chunks. |
| `response_headers` | `implemented_not_asserted` | An optional HAProxy response-check message maps response headers and the agent invokes Phase 3; canonical host evidence is pending. |
| `response_body_buffered` | `not_implemented` | The selected SPOE/SPOP host configuration deliberately does not send response bodies; the former wait-for-body sample was disabled because it violates the low-latency contract. |
| `response_body_streaming` | `not_implemented` | The selected SPOE/SPOP configuration has no wired native response-chunk callback or streaming transaction protocol. A separate HTX observer is selected only by the non-promoted full-lifecycle profile and does not change this SPOP capability state. |
| `response_body_incremental_ingest` | `not_implemented` | No native HAProxy response-chunk callback is wired into the selected SPOP path. The separate full-lifecycle HTX observer handles borrowed body chunks/EOS in observer mode, but does not change this SPOP capability state. |
| `phase1` | `implemented_not_asserted` | The request-check group executes connection, URI, and request-header processing in the agent; canonical evidence is pending. |
| `phase2` | `implemented_not_asserted` | The agent appends the bounded request body and invokes request-body processing; canonical evidence is pending. |
| `phase3` | `implemented_not_asserted` | The optional response-check group invokes response-header processing; canonical host evidence is pending. |
| `phase4` | `not_implemented` | No native HAProxy response-body callback is wired into the selected SPOE/SPOP host configuration. The separate HTX observer is selected only by the non-promoted full-lifecycle profile and does not promote this SPOP capability. |
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
| `http2_downstream` | `not_implemented` | The pinned native HTX harness has no TLS/ALPN HTTP/2 frontend profile. |
| `http2_upstream` | `not_implemented` | No HAProxy native HTX upstream HTTP/2 profile is implemented. |
| `http2_tls_alpn` | `not_implemented` | The pinned HAProxy build and harness do not configure an h2 ALPN listener. |
| `http2_cleartext_h2c` | `not_implemented` | No HAProxy h2c native connector profile is implemented. |
| `http2_multiplexing` | `not_implemented` | No HAProxy HTTP/2 stream-isolation evidence path is implemented. |
| `http2_stream_reset` | `not_implemented` | The HTX filter has no proven HTTP/2 stream-reset action. |
| `http3_downstream` | `not_implemented` | The pinned HAProxy native HTX build has no configured QUIC/HTTP/3 frontend. |
| `http3_upstream` | `not_implemented` | No HAProxy native HTX upstream HTTP/3 profile is implemented. |
| `http3_quic` | `not_implemented` | No pinned HAProxy QUIC runtime build is provisioned. |
| `http3_alt_svc` | `not_implemented` | No HAProxy HTTP/3 Alt-Svc profile is configured. |
| `http3_multiplexing` | `not_implemented` | No HAProxy HTTP/3 stream-isolation evidence path is implemented. |
| `http3_stream_reset` | `not_implemented` | The HTX filter has no proven QUIC stream-reset action. |
| `protocol_transaction_isolation` | `not_implemented` | No multiplexed protocol transaction-isolation case is implemented. |
| `protocol_first_byte_before_response_end` | `not_implemented` | No protocol-specific first-byte barrier is implemented. |
| `protocol_no_full_response_buffering` | `not_implemented` | No protocol-specific no-full-buffer proof is implemented. |
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
- Source-Contract: `connectors/envoy/metadata.c`, `connectors/envoy/config/envoy-ext-authz-smoke.yaml.in`, `connectors/envoy/config/envoy-ext-authz.conf`, `connectors/envoy/src/envoy_ext_authz_service_main.c`, `connectors/envoy/src/envoy_ext_authz_response_companion.c`, `connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main.go`, `connectors/envoy/ext_proc/internal/responseobserver/service.go`, `connectors/envoy/src/envoy_modsecurity_mapper.c`, `connectors/envoy/harness/run_envoy_connector_runtime.sh`

Host-Modell-Grenzen:

- The HTTP ext_authz service alone observes a pre-upstream authorization request; the mandatory following private-UDS ext_proc response observer receives the corresponding upstream response headers and streaming body.
- The checked-in ext_authz configuration buffers at most 4096 request-body bytes with partial messages disabled; the existing minimal smoke sends no request body.
- Only the headers allowed by the ext_authz authorization_request configuration are forwarded to the authorization service.
- The authorization service currently sees the Envoy-to-service socket endpoints and does not map original downstream connection endpoints into Common connection metadata.
- The opaque response handle is propagated only from ext_authz to the following local ext_proc observer and is removed before routing upstream; missing observer or correlation is fail-closed.

| Capability | Zustand | Kanonischer Grund (aus dem Manifest) |
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
| `http2_downstream` | `not_implemented` | The selected native ext_proc harness has no TLS/ALPN HTTP/2 listener profile. |
| `http2_upstream` | `not_implemented` | No ext_proc upstream HTTP/2 evidence profile is implemented. |
| `http2_tls_alpn` | `not_implemented` | No pinned ext_proc TLS/ALPN listener is configured. |
| `http2_cleartext_h2c` | `not_implemented` | No ext_proc h2c listener is configured. |
| `http2_multiplexing` | `not_implemented` | No ext_proc HTTP/2 stream-isolation runner is implemented. |
| `http2_stream_reset` | `not_implemented` | Closing an ext_proc gRPC stream is not a client-visible HTTP/2 reset and no native reset hook is wired. |
| `http3_downstream` | `not_implemented` | The selected native ext_proc harness has no QUIC/HTTP/3 downstream listener. |
| `http3_upstream` | `not_implemented` | No ext_proc upstream HTTP/3 evidence profile is implemented. |
| `http3_quic` | `not_implemented` | No Envoy QUIC listener is configured in the pinned native harness. |
| `http3_alt_svc` | `not_implemented` | No Envoy H3 Alt-Svc profile is configured. |
| `http3_multiplexing` | `not_implemented` | No Envoy H3 stream-isolation runner is implemented. |
| `http3_stream_reset` | `not_implemented` | No client-visible QUIC stream-reset hook is implemented for ext_proc. |
| `protocol_transaction_isolation` | `not_implemented` | No multiplexed downstream protocol transaction-isolation evidence is implemented. |
| `protocol_first_byte_before_response_end` | `not_implemented` | No negotiated-protocol first-byte barrier is implemented. |
| `protocol_no_full_response_buffering` | `not_implemented` | No negotiated-protocol no-full-buffer proof is implemented. |
| `client_abort` | `unsupported_by_host_model` | The external authorization service cannot observe or directly control an Envoy downstream client-abort lifecycle. |
| `upstream_abort` | `unsupported_by_host_model` | The pre-upstream authorization service cannot observe or control an upstream response-abort lifecycle. |
| `response_body_decompression` | `unsupported_by_host_model` | HTTP ext_authz does not receive an upstream response body to decompress. |
| `deny` | `implemented_not_asserted` | A disruptive Common Runtime decision is returned as a non-2xx ext_authz response; a fresh canonical deny result is pending. |
| `redirect` | `implemented_not_asserted` | The shared authorization service emits one bounded, validated Location header for a redirect decision; the focused Common service regression covers the Envoy ext_authz profile, while fresh canonical Envoy runtime evidence remains pending. |
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
- Source-Contract: `connectors/traefik/metadata.c`, `connectors/traefik/config/traefik-forwardauth-dynamic.yaml`, `connectors/traefik/config/traefik-forwardauth.conf`, `connectors/traefik/src/traefik_forwardauth_service_main.c`, `connectors/traefik/src/traefik_forwardauth_response_companion.c`, `connectors/traefik/response_observer/observer.go`, `connectors/traefik/config/traefik-response-observer-static.yaml`, `connectors/traefik/config/traefik-response-observer-dynamic.yaml`, `connectors/traefik/src/traefik_modsecurity_mapper.c`, `connectors/traefik/scripts/runtime_smoke.py`, `connectors/traefik/native_middleware/middleware.go`, `connectors/traefik/native_middleware/.traefik.yml`, `connectors/traefik/config/traefik-native-middleware-dynamic.yaml`, `connectors/traefik/config/traefik-native-middleware-static.yaml`, `connectors/traefik/scripts/runtime-native-middleware.sh`, `connectors/traefik/scripts/runtime_native_smoke.py`

Host-Modell-Grenzen:

- The forwardAuth service alone observes the authorization request before upstream handling; the mandatory following response-observer plugin receives the corresponding response headers and streaming body.
- Traefik v3.7 supports buffered forwardAuth request bodies with forwardBody and maxBodySize; the checked-in dynamic configuration enables both with a 4096-byte cap and the service config requires request_body_mode=buffered.
- Traefik documents that forwardBody buffering breaks streaming, so streaming request-body inspection is outside this host path.
- The authorization service currently sees the Traefik-to-service socket endpoints and does not map original client connection endpoints into Common connection metadata.
- The full-lifecycle profile separately selects native-middleware through full-lifecycle-traefik-native in a pinned Traefik local-plugin host probe. Its selected UDS engine service performs Common/libmodsecurity evaluation, while this forwardAuth compatibility declaration remains separate and unpromoted.
- In the checked-in profile, forwardAuth propagates the opaque response handle only to the following local response observer, which removes it before the upstream handler. The static source contract requires that chain; an operator who omits or reorders the observer is outside this profile and must validate P3/P4 separately.

| Capability | Zustand | Kanonischer Grund (aus dem Manifest) |
|---|---|---|
| `connection_metadata` | `not_implemented` | The HTTP authorization service maps its local Traefik peer socket rather than the original client connection metadata. |
| `transport_metadata` | `not_implemented` | The pre-upstream forwardAuth service does not observe client-visible upstream-response commitment or transport outcomes. |
| `request_headers` | `implemented_not_asserted` | Configured forwardAuth request headers are mapped into Common Runtime; canonical multi-header and limit evidence is pending. |
| `request_body_buffered` | `configured_not_exercised` | The checked-in middleware explicitly sets forwardBody=true and maxBodySize=4096, and the service requires request_body_mode=buffered; a fresh real-host P2 result is still required for runtime promotion. |
| `request_body_streaming` | `unsupported_by_host_model` | Traefik v3.7 documents that forwardBody reads and buffers the body before forwarding and therefore breaks streaming. |
| `request_body_incremental_ingest` | `unsupported_by_host_model` | Traefik forwardBody buffers the bounded body before authorization and does not provide incremental request-body callbacks. |
| `response_headers` | `unsupported_by_host_model` | forwardAuth runs before the upstream request and does not receive the later upstream response headers. |
| `response_body_buffered` | `unsupported_by_host_model` | forwardAuth does not receive the later upstream response body. |
| `response_body_streaming` | `unsupported_by_host_model` | forwardAuth does not receive an upstream response body stream. |
| `response_body_incremental_ingest` | `unsupported_by_host_model` | The pre-upstream forwardAuth service never receives an upstream response-body stream. |
| `phase1` | `implemented_not_asserted` | The forwardAuth request headers enter the Common Runtime Phase-1 path; a fresh canonical baseline result is pending. |
| `phase2` | `configured_not_exercised` | The checked-in forwardAuth path buffers and bounds P2 at 4096 bytes, and the start harness rejects templates that omit either setting; a fresh real-host P2 result is still required. |
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
| `request_body_limits` | `configured_not_exercised` | Traefik maxBodySize=4096 and the Common request_body_limit=4096 are explicitly configured; a fresh real-host over-limit result is still required. |
| `response_body_limits` | `unsupported_by_host_model` | forwardAuth does not receive an upstream response body on which to enforce a response-body limit. |
| `no_full_response_buffering` | `unsupported_by_host_model` | The request-only forwardAuth host model has no upstream response stream for this property to describe. |
| `first_byte_before_response_end` | `unsupported_by_host_model` | The request-only forwardAuth service cannot observe a Traefik client first byte or upstream response end. |
| `http1_content_length` | `configured_not_exercised` | Traefik can proxy HTTP/1.1 responses, but no canonical forwardAuth transport case covers Content-Length handling. |
| `http1_chunked` | `configured_not_exercised` | Traefik can proxy chunked HTTP/1.1 responses, but no canonical forwardAuth transport case covers them. |
| `keep_alive` | `configured_not_exercised` | No canonical sequential-request keep-alive run is attached to the Traefik forwardAuth path. |
| `parallel_requests` | `not_implemented` | The Traefik forwardAuth full-lifecycle catalog has no parallel-request evidence path. |
| `http2` | `configured_not_exercised` | Traefik HTTP/2 transport behavior is not exercised by a canonical forwardAuth full-lifecycle case. |
| `http2_downstream` | `not_implemented` | The repository-owned native-middleware harness renders only a cleartext web entry point; it has no TLS HTTP/2 listener or forced H2 client path. |
| `http2_upstream` | `not_implemented` | No Traefik native middleware upstream HTTP/2 matrix is implemented. |
| `http2_tls_alpn` | `not_implemented` | The repository-owned native-middleware configuration has no certificate, TLS entry point, or h2 ALPN configuration. |
| `http2_cleartext_h2c` | `not_implemented` | No native middleware h2c profile is configured. |
| `http2_multiplexing` | `not_implemented` | No native middleware HTTP/2 stream-isolation runner is implemented. |
| `http2_stream_reset` | `not_implemented` | HTTP/1 hijack behavior is not HTTP/2 reset evidence and no stream-reset API is wired. |
| `http3_downstream` | `not_implemented` | The repository-owned native-middleware harness has no HTTP/3 entry point, UDP/QUIC listener, or forced H3 client path. |
| `http3_upstream` | `not_implemented` | No Traefik native middleware upstream HTTP/3 matrix is implemented. |
| `http3_quic` | `not_implemented` | No repository-owned Traefik QUIC listener or QUIC traffic observation is configured for the native middleware. |
| `http3_alt_svc` | `not_implemented` | No repository-owned native-middleware Traefik configuration advertises an HTTP/3 Alt-Svc endpoint. |
| `http3_multiplexing` | `not_implemented` | No native middleware H3 stream-isolation runner is implemented. |
| `http3_stream_reset` | `not_implemented` | No client-visible QUIC stream-reset API is wired for the middleware. |
| `protocol_transaction_isolation` | `not_implemented` | No multiplexed protocol transaction-isolation evidence is implemented. |
| `protocol_first_byte_before_response_end` | `not_implemented` | No negotiated-protocol first-byte barrier is implemented. |
| `protocol_no_full_response_buffering` | `not_implemented` | No negotiated-protocol no-full-buffer proof is implemented. |
| `client_abort` | `unsupported_by_host_model` | The external authorization service cannot observe or directly control a Traefik client-abort lifecycle. |
| `upstream_abort` | `unsupported_by_host_model` | The pre-upstream authorization service cannot observe or control an upstream response-abort lifecycle. |
| `response_body_decompression` | `unsupported_by_host_model` | forwardAuth does not receive an upstream response body to decompress. |
| `deny` | `implemented_not_asserted` | A disruptive Common Runtime decision is returned as a non-2xx forwardAuth response; a fresh canonical deny result is pending. |
| `redirect` | `implemented_not_asserted` | The shared authorization service emits one bounded, validated Location header for a redirect decision; the focused Common service regression covers the Traefik forwardAuth profile, while fresh canonical Traefik runtime evidence remains pending. |
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
- Source-Contract: `connectors/lighttpd/metadata.c`, `connectors/lighttpd/config/lighttpd-native.conf`, `connectors/lighttpd/module/mod_msconnector.c`, `connectors/lighttpd/src/lighttpd_modsecurity_mapper.c`, `connectors/lighttpd/harness/runtime_lighttpd_smoke.sh`, `connectors/lighttpd/patches/0001-lighttpd-msconnector-stream-hooks.patch`, `connectors/lighttpd/build/build_patched_host.sh`, `connectors/lighttpd/harness/run_patched_lifecycle_smoke.sh`, `connectors/lighttpd/stock_sidecar/stock_sidecar.c`, `connectors/lighttpd/stock_sidecar/README.md`, `connectors/lighttpd/build/build_stock_sidecar.sh`, `connectors/lighttpd/tests/test_stock_sidecar_contract.py`

Host-Modell-Grenzen:

- The stock native plugin requires both body modes to be none. The matched patched Framework-synchronized core/module pair accepts streaming request ranges and HTTP/1.1 identity response-entity ranges before transfer framing; this source/build contract has no canonical runtime promotion.
- The response-header mapper is called from handle_response_start, but source wiring alone is not Phase-3 behavioral verification.
- The legacy bridge and starter self-tests are separate from native mod_msconnector.so host-runtime evidence.
- The canonical logical Stock profile lighttpd-stock selects stock-lighttpd-sidecar and owns P1--P4 within its bounded HTTP/1.1 component. The current host-family full-lifecycle target separately selects patched-native through full-lifecycle-lighttpd-patched: its checked-in host smoke uses both body modes as none and does not prove Stock-sidecar or native-Stock host behavior. Identity streaming configuration is available for contract checks, while gzip/br, HTTP/2, strict abort, first-byte, and no-full-buffer client evidence remain NOT EXECUTED.

| Capability | Zustand | Kanonischer Grund (aus dem Manifest) |
|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | The native mapper reads lighttpd client and server socket endpoints into Common Runtime; canonical evidence is pending. |
| `transport_metadata` | `implemented_not_asserted` | The native mapper supplies host endpoint and response-status metadata, but a canonical transport run is pending. |
| `request_headers` | `implemented_not_asserted` | The native URI-clean hook maps lighttpd request headers into Common Runtime; canonical header evidence is pending. |
| `request_body_buffered` | `not_implemented` | The native module requires request_body_mode=none and supplies no request body to the mapper. |
| `request_body_streaming` | `not_implemented` | The checked-in selected evidence profile has no promoted request-stream case. The patched Framework-synchronized ABI has a borrowed request-range source contract, but it remains non-promoted until its host artifacts are selected and validated. |
| `request_body_incremental_ingest` | `not_implemented` | The patched Framework-synchronized request callback supplies monotonic borrowed ranges, but the selected capability profile remains unpromoted without a matching canonical host result. |
| `response_headers` | `implemented_not_asserted` | handle_response_start maps response headers into Common Runtime, but a real Phase-3 rule result has not yet been attached. |
| `response_body_buffered` | `not_implemented` | The native module requires response_body_mode=none and supplies no response body to the mapper. |
| `response_body_streaming` | `not_implemented` | The checked-in selected evidence profile has no promoted response-stream case. The patched Framework-synchronized ABI has a borrowed HTTP/1.1 identity entity-body callback before transfer framing, but no canonical streaming host run validates it. |
| `response_body_incremental_ingest` | `not_implemented` | The patched HTTP/1.1 identity entity callback supplies borrowed ranges before transfer framing and marks EOS once; its source/build contract lacks a canonical streaming host result. |
| `phase1` | `implemented_not_asserted` | The URI-clean hook starts the transaction and processes request headers; a fresh canonical Phase-1 result is pending. |
| `phase2` | `not_implemented` | The stock module disables request bodies, and the selected capability profile has no promoted Phase-2 body result. The patched request-range source path is deliberately kept separate pending matching host evidence. |
| `phase3` | `implemented_not_asserted` | The response-start hook invokes Common Runtime response processing with mapped headers; real Phase-3 behavioral evidence is pending. |
| `phase4` | `not_implemented` | The selected capability profile has no canonical Phase-4 host result. The patched identity entity-body source path is not promoted by its current body-disabled smoke. |
| `phase4_rule_evaluation` | `not_implemented` | The patched identity entity callback can incrementally ingest bytes and finish at EOS, but no real host run has observed rule 1100301 through that path; per-chunk evaluation is not claimed. |
| `phase4_end_of_stream_evaluation` | `not_implemented` | The patched entity callback invokes the Common finish API once at EOS, but no real host run verifies that Phase-4 result; per-chunk rule evaluation is not claimed. |
| `phase4_pre_commit_deny` | `not_implemented` | The patched callback has no client-validated precommit disposition. It deliberately does not fabricate a late HTTP status from an EOS decision. |
| `late_intervention` | `not_implemented` | The patched callback resolves the shared late-intervention policy in source, but no real host run proves a post-commit outcome; the response-start hook is not late-intervention evidence. |
| `late_intervention_log_only` | `not_implemented` | The patched source records disruptive safe/minimal Phase-4 decisions as actual log_only while preserving the response, but no client-visible canonical evidence has been produced. |
| `late_intervention_abort` | `not_implemented` | Strict deliberately remains NOT EXECUTED: the patched entity hook has no client-validated lighttpd connection-abort primitive or follow-up-health proof. |
| `late_intervention_status_metadata` | `not_implemented` | The patched source can record a safe log_only host action, but no canonical client artifact proves original, requested, visible, and actual values at a post-commit point. |
| `content_type_scope` | `not_implemented` | No canonical response-stream run proves Content-Type behavior for the patched identity-only entity path. |
| `header_limits` | `implemented_not_asserted` | The native request and response mappers apply configured header count and total-size limits, but real-host limit evidence is pending. |
| `request_body_limits` | `not_implemented` | No canonical request-stream run exercises body limits on the patched request-range path. |
| `response_body_limits` | `not_implemented` | No canonical response-stream run exercises body limits on the patched identity entity path. |
| `no_full_response_buffering` | `not_implemented` | The patched callback receives only the current borrowed identity entity range and retains no queue copy, but no real first-byte-before-EOS client run proves the no-full-buffer property. |
| `first_byte_before_response_end` | `not_implemented` | No synchronized real-client run demonstrates a first body byte before upstream EOS on the patched identity entity path. |
| `http1_content_length` | `configured_not_exercised` | The native plugin can load in a lighttpd HTTP/1.1 host, but the canonical Content-Length transport case has not run. |
| `http1_chunked` | `configured_not_exercised` | The native plugin can load in a lighttpd HTTP/1.1 host, but no canonical chunked transport evidence is attached. |
| `keep_alive` | `configured_not_exercised` | No canonical sequential-request keep-alive run is attached to the native plugin. |
| `parallel_requests` | `not_implemented` | The canonical parallel full-lifecycle isolation evidence path is not implemented for lighttpd. |
| `http2` | `unsupported_by_host_model` | The pinned native lighttpd integration has no asserted HTTP/2 full-lifecycle transport path. |
| `http2_downstream` | `not_implemented` | The pinned patched lighttpd module rejects HTTP/2 requests; a decoded H2 stream hook is not implemented. |
| `http2_upstream` | `not_implemented` | No patched lighttpd upstream HTTP/2 profile is implemented. |
| `http2_tls_alpn` | `not_implemented` | The managed lighttpd build currently disables TLS backends and has no h2 ALPN listener. |
| `http2_cleartext_h2c` | `not_implemented` | No patched lighttpd h2c integration profile is implemented. |
| `http2_multiplexing` | `not_implemented` | The patched module has no H2 stream lifecycle or multiplexing contract. |
| `http2_stream_reset` | `not_implemented` | No lighttpd HTTP/2 stream-reset hook is implemented. |
| `http3_downstream` | `not_implemented` | The Framework-synchronized lighttpd host has no audited native HTTP/3 listener or codec path. |
| `http3_upstream` | `not_implemented` | No patched lighttpd upstream HTTP/3 profile is implemented. |
| `http3_quic` | `not_implemented` | The pinned lighttpd host has no QUIC runtime path. |
| `http3_alt_svc` | `not_implemented` | No native lighttpd HTTP/3 Alt-Svc profile is configured. |
| `http3_multiplexing` | `not_implemented` | No native lighttpd H3 stream-isolation path is implemented. |
| `http3_stream_reset` | `not_implemented` | No lighttpd H3 stream-reset API exists in the pinned host profile. |
| `protocol_transaction_isolation` | `not_implemented` | No multiplexed protocol transaction-isolation evidence is implemented. |
| `protocol_first_byte_before_response_end` | `not_implemented` | No decoded modern-protocol response-body hook exists for a first-byte barrier. |
| `protocol_no_full_response_buffering` | `not_implemented` | No decoded modern-protocol response-body hook exists for a no-full-buffer proof. |
| `client_abort` | `not_implemented` | No native client-abort cleanup case records canonical transport metadata. |
| `upstream_abort` | `not_implemented` | No native upstream-abort cleanup case records canonical transport metadata. |
| `response_body_decompression` | `not_implemented` | The patched response contract is identity only. gzip/br remain NOT EXECUTED until filter order and decompression have real host evidence. |
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
| Declared input | `connectors/apache/capabilities.json` | `44d36c9ac944e89e472368decf1f23b61296b55c4ac0a4e599fcfa6a8e17b1ff` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/nginx/capabilities.json` | `2c0474e075187b692aa4ba12467b0839a895c33a9ceca4771638eab219c3a3b3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/haproxy/capabilities.json` | `83528048ed6d012042bf5f0ca245a07d0a4457b72d7e89925d2745d70b4bc82a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/envoy/capabilities.json` | `5e3848e27db6133eed8a7a7c4c579f722745a17e61490c2b2bad67654bf92ab4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/traefik/capabilities.json` | `f96775fa85d85bb66f739743ae154feb66d61c710ad6f9dde0be2977fef86b88` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/lighttpd/capabilities.json` | `95c68aeba2340c6ed996c976188d6fae0c5ff1c91f1995a2cc245a33bbd47665` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `connectors/apache/capabilities.json` | present | input file available |
| `connectors/nginx/capabilities.json` | present | input file available |
| `connectors/haproxy/capabilities.json` | present | input file available |
| `connectors/envoy/capabilities.json` | present | input file available |
| `connectors/traefik/capabilities.json` | present | input file available |
| `connectors/lighttpd/capabilities.json` | present | input file available |
