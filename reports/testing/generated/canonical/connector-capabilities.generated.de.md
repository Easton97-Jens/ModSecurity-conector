> Generated file - do not edit manually.
>
> Generated at: `2026-07-11T08:47:58Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/connector_capabilities.py`
> Make target: `capabilities-all-connectors`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `4e004f821d0d91a3a9f63ffe9d27e541cab95d65`
> Framework SHA: `de0fc5dc0751d3b0e8cb1bd5187e4e3ff558f41f`
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
| `request_headers` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `request_body_buffered` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `configured_not_exercised` | `not_implemented` | `not_implemented` |
| `request_body_streaming` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `response_headers` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `unsupported_by_host_model` | `unsupported_by_host_model` | `implemented_not_asserted` |
| `response_body_buffered` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `response_body_streaming` | `not_implemented` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `phase1` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` |
| `phase2` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `configured_not_exercised` | `not_implemented` | `not_implemented` |
| `phase3` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `unsupported_by_host_model` | `unsupported_by_host_model` | `implemented_not_asserted` |
| `phase4` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `phase4_rule_evaluation` | `implemented_not_asserted` | `implemented_not_asserted` | `implemented_not_asserted` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `phase4_pre_commit_deny` | `implemented_not_asserted` | `not_implemented` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `late_intervention` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `late_intervention_log_only` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `late_intervention_abort` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
| `late_intervention_status_metadata` | `implemented_not_asserted` | `implemented_not_asserted` | `not_implemented` | `unsupported_by_host_model` | `unsupported_by_host_model` | `not_implemented` |
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
- Source-Contract: `connectors/apache/metadata.c`, `connectors/apache/src/mod_security3.c`, `connectors/apache/src/msc_filters.c`, `connectors/apache/src/msc_config.c`, `connectors/apache/harness/run_apache_smoke.sh`

Host-Modell-Grenzen:

- Request and response bodies are accumulated through Apache filters before the corresponding ModSecurity phase is completed; this is not streaming phase execution.
- The connector JSONL writer is currently specific to Phase-4 interventions and does not by itself prove canonical event coverage for request-phase decisions.
- A Phase-4 disruptive result can occur after response commitment and is handled by the configured late-intervention policy.

| Capability | Zustand | Kanonischer Grund (aus dem Manifest) |
|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | The native request hooks pass Apache client and server addresses and ports to libmodsecurity; no current canonical capability result is attached. |
| `request_headers` | `implemented_not_asserted` | The native module maps Apache request headers and calls the ModSecurity request-header phase; canonical baseline evidence is pending. |
| `request_body_buffered` | `implemented_not_asserted` | The Apache input filter appends request-body buckets and completes request-body processing; canonical body evidence is pending. |
| `request_body_streaming` | `not_implemented` | The connector appends body chunks but completes the ModSecurity body phase as a buffered phase rather than exposing streaming phase semantics. |
| `response_headers` | `implemented_not_asserted` | The Apache output filter maps response headers and invokes the response-header phase; canonical Phase-3 evidence is pending. |
| `response_body_buffered` | `implemented_not_asserted` | The output filter buffers bounded response data and invokes response-body processing; canonical Phase-4 evidence is pending. |
| `response_body_streaming` | `not_implemented` | Response buckets are accumulated for a bounded Phase-4 decision and are not processed as a streaming ModSecurity phase. |
| `phase1` | `implemented_not_asserted` | The early request hook processes URI and request headers before request handling; the canonical Phase-1 baseline has not been run here. |
| `phase2` | `implemented_not_asserted` | The late request hook and input filter complete request-body processing; canonical Phase-2 evidence is pending. |
| `phase3` | `implemented_not_asserted` | The output filter invokes response-header processing before body processing; canonical Phase-3 evidence is pending. |
| `phase4` | `implemented_not_asserted` | The bounded output filter invokes response-body processing and records late decisions; canonical Phase-4 evidence is pending. |
| `phase4_rule_evaluation` | `implemented_not_asserted` | The bounded native output-filter path is wired to invoke response-body processing, but no current canonical real-host run proves that Phase-4 rule 1100301 was evaluated. |
| `phase4_pre_commit_deny` | `implemented_not_asserted` | The output-filter intervention path has a denial branch, but no current canonical evidence proves a Phase-4 deny before response commitment with a changed visible client status. |
| `late_intervention` | `implemented_not_asserted` | Phase-4 minimal, safe, and strict policy branches distinguish log-only, status denial, and post-commit connection abort; behavioral evidence is pending. |
| `late_intervention_log_only` | `implemented_not_asserted` | The configured safe late-intervention branch is intended to preserve the committed response and record a log-only result, but no canonical event proves requested deny, actual log_only, and an unchanged visible status. |
| `late_intervention_abort` | `implemented_not_asserted` | The configured strict late-intervention branch has a controlled connection-abort path, but no canonical real-host event proves actual abort_connection and connection_aborted=true. |
| `late_intervention_status_metadata` | `implemented_not_asserted` | Phase-4 metadata wiring exists, but no canonical event yet proves separate requested WAF status, original host status, visible client status, requested action, and actual action. |
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

- NGINX request and response body filters feed bounded body data into a completed ModSecurity phase; they do not provide streaming phase semantics.
- The connector JSONL writer is currently specific to Phase-4 interventions and does not by itself prove canonical event coverage for request-phase decisions.
- A Phase-4 decision can be observed after NGINX has sent response headers and is then governed by the late-intervention policy.

| Capability | Zustand | Kanonischer Grund (aus dem Manifest) |
|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | The native request path maps NGINX connection endpoints into the ModSecurity transaction; canonical evidence is pending. |
| `request_headers` | `implemented_not_asserted` | The access handler maps NGINX request headers and invokes request-header processing; canonical evidence is pending. |
| `request_body_buffered` | `implemented_not_asserted` | The request-body callback appends buffered NGINX body buffers and completes Phase 2; canonical body evidence is pending. |
| `request_body_streaming` | `not_implemented` | Body buffers are accumulated for a completed request-body phase rather than exposed as streaming ModSecurity phase execution. |
| `response_headers` | `implemented_not_asserted` | The NGINX header filter invokes response-header processing; canonical Phase-3 evidence is pending. |
| `response_body_buffered` | `implemented_not_asserted` | The bounded body filter invokes response-body processing and applies the configured Phase-4 policy; canonical evidence is pending. |
| `response_body_streaming` | `not_implemented` | Response chains are inspected through bounded buffering and do not expose streaming Phase-4 semantics. |
| `phase1` | `implemented_not_asserted` | The access handler processes URI and request headers before upstream handling; canonical Phase-1 evidence is pending. |
| `phase2` | `implemented_not_asserted` | The request-body callback completes ModSecurity request-body processing; canonical Phase-2 evidence is pending. |
| `phase3` | `implemented_not_asserted` | The response header filter invokes ModSecurity Phase 3; canonical behavioral evidence is pending. |
| `phase4` | `implemented_not_asserted` | The response body filter invokes bounded ModSecurity Phase 4; canonical behavioral evidence is pending. |
| `phase4_rule_evaluation` | `implemented_not_asserted` | The bounded native response-body filter is wired to invoke Phase 4, but no current canonical real-host run proves that Phase-4 rule 1100301 was evaluated. |
| `phase4_pre_commit_deny` | `not_implemented` | The native Phase-4 decision runs in the NGINX body filter after the response-header path; this connector has no demonstrated pre-commit response-body decision point, so a visible Phase-4 HTTP 403 must not be claimed. |
| `late_intervention` | `implemented_not_asserted` | The body filter distinguishes pre-header denial from post-header log-only or connection-abort policy outcomes; canonical evidence is pending. |
| `late_intervention_log_only` | `implemented_not_asserted` | The safe post-commit policy is wired to record a log-only outcome, but no canonical event proves requested deny, actual log_only, late_intervention=true, and an unchanged visible status. |
| `late_intervention_abort` | `implemented_not_asserted` | The strict post-commit policy has an abort path, but no canonical real-host event proves actual abort_connection and connection_aborted=true. |
| `late_intervention_status_metadata` | `implemented_not_asserted` | The Phase-4 path can emit intervention metadata, but no canonical event yet proves separate requested WAF status, original host status, visible client status, requested action, and actual action. |
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
- Source-Contract: `connectors/haproxy/metadata.c`, `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`, `connectors/haproxy/src/haproxy_modsecurity_binding.c`, `connectors/haproxy/src/haproxy_modsecurity_mapper.c`, `connectors/haproxy/harness/run_haproxy_smoke.sh`

Host-Modell-Grenzen:

- HAProxy and the repository-owned SPOP agent are separate processes; host and agent liveness and logs are distinct evidence.
- Response phases run only when the HAProxy configuration sends the corresponding response notification to the agent.
- Response-body notification and inspection are bounded and experimental; a mapper or agent code path alone is not runtime verification.
- Starter and binding self-tests are not HAProxy host-runtime evidence.

| Capability | Zustand | Kanonischer Grund (aus dem Manifest) |
|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | The SPOP request message carries client and server endpoints into the libmodsecurity binding; canonical evidence is pending. |
| `request_headers` | `implemented_not_asserted` | HAProxy request headers are encoded in the SPOP message and mapped into the transaction; canonical evidence is pending. |
| `request_body_buffered` | `implemented_not_asserted` | The HAProxy configuration buffers the request and passes a bounded req.body sample to the agent; canonical Phase-2 evidence is pending. |
| `request_body_streaming` | `not_implemented` | The current SPOP message carries one bounded body sample rather than a streaming body protocol. |
| `response_headers` | `implemented_not_asserted` | An optional HAProxy response-check message maps response headers and the agent invokes Phase 3; canonical host evidence is pending. |
| `response_body_buffered` | `implemented_not_asserted` | The optional response-check message and agent implement bounded experimental response-body inspection; canonical Phase-4 evidence is pending. |
| `response_body_streaming` | `not_implemented` | The response path uses one bounded HAProxy response sample and does not implement a streaming transaction protocol. |
| `phase1` | `implemented_not_asserted` | The request-check group executes connection, URI, and request-header processing in the agent; canonical evidence is pending. |
| `phase2` | `implemented_not_asserted` | The agent appends the bounded request body and invokes request-body processing; canonical evidence is pending. |
| `phase3` | `implemented_not_asserted` | The optional response-check group invokes response-header processing; canonical host evidence is pending. |
| `phase4` | `implemented_not_asserted` | The bounded experimental response-body branch invokes response-body processing; canonical host evidence is pending. |
| `phase4_rule_evaluation` | `implemented_not_asserted` | The bounded SPOA/SPOP response-body branch is present, but no current canonical HAProxy host run proves that Phase-4 rule 1100301 was evaluated. |
| `phase4_pre_commit_deny` | `not_implemented` | The current agent emits policy-derived pre-commit fields but the HAProxy host runner does not capture a client-visible Phase-4 deny and actual commitment timing, so this semantic capability is not implemented. |
| `late_intervention` | `not_implemented` | The current SPOE/SPOP response decision path is modeled before response commitment and implements no post-commit late-intervention point. |
| `late_intervention_log_only` | `not_implemented` | The current HAProxy/SPOA path has no post-commit log-only action or host-observed unchanged-visible-status result. |
| `late_intervention_abort` | `not_implemented` | The current HAProxy/SPOA path implements no controlled post-commit abort_connection action and no host-observed connection-abort result. |
| `late_intervention_status_metadata` | `not_implemented` | Current diagnostics are policy-derived and the host runner does not capture original and visible client statuses plus actual commitment timing, so semantic late-intervention status metadata is not implemented. |
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
- Source-Contract: `connectors/envoy/metadata.c`, `connectors/envoy/config/envoy-ext-authz-smoke.yaml.in`, `connectors/envoy/config/envoy-ext-authz.conf`, `connectors/envoy/src/envoy_ext_authz_service_main.c`, `connectors/envoy/src/envoy_modsecurity_mapper.c`, `connectors/envoy/harness/run_envoy_connector_runtime.sh`

Host-Modell-Grenzen:

- The selected Envoy HTTP ext_authz service observes a pre-upstream authorization request and cannot inspect the later upstream response headers or body.
- The checked-in ext_authz configuration buffers at most 4096 request-body bytes with partial messages disabled; the existing minimal smoke sends no request body.
- Only the headers allowed by the ext_authz authorization_request configuration are forwarded to the authorization service.
- The authorization service currently sees the Envoy-to-service socket endpoints and does not map original downstream connection endpoints into Common connection metadata.

| Capability | Zustand | Kanonischer Grund (aus dem Manifest) |
|---|---|---|
| `connection_metadata` | `not_implemented` | The HTTP authorization service maps its local Envoy peer socket rather than the original downstream connection metadata. |
| `request_headers` | `implemented_not_asserted` | The ext_authz HTTP request forwards an allowlisted header set into the Common Runtime mapper; canonical header coverage is pending. |
| `request_body_buffered` | `configured_not_exercised` | Envoy with_request_body and the connector buffered body mode are both configured at 4096 bytes, but the existing host smoke sends no body. |
| `request_body_streaming` | `unsupported_by_host_model` | The selected ext_authz integration deliberately uses the with_request_body buffered authorization request, not a streaming body protocol. |
| `response_headers` | `unsupported_by_host_model` | HTTP ext_authz runs before the upstream request and does not receive the later upstream response headers. |
| `response_body_buffered` | `unsupported_by_host_model` | HTTP ext_authz does not receive the later upstream response body. |
| `response_body_streaming` | `unsupported_by_host_model` | HTTP ext_authz does not receive an upstream response body stream. |
| `phase1` | `implemented_not_asserted` | The authorization service maps request headers into the Common Runtime Phase-1 path; a canonical baseline result is pending. |
| `phase2` | `configured_not_exercised` | Buffered request-body forwarding and Common Runtime Phase 2 are configured, but no existing host smoke proves that Envoy delivered the body. |
| `phase3` | `unsupported_by_host_model` | The pre-upstream ext_authz call cannot inspect upstream response headers. |
| `phase4` | `unsupported_by_host_model` | The pre-upstream ext_authz call cannot inspect upstream response bodies. |
| `phase4_rule_evaluation` | `unsupported_by_host_model` | The selected Envoy ext_authz integration executes before the upstream response and does not expose upstream response-body data for Phase-4 rule evaluation. |
| `phase4_pre_commit_deny` | `unsupported_by_host_model` | Because ext_authz never sees the later upstream response, it has no Phase-4 response point at which to deny before the response commits. |
| `late_intervention` | `unsupported_by_host_model` | The authorization decision completes before the upstream response starts, so there is no response-phase late intervention point. |
| `late_intervention_log_only` | `unsupported_by_host_model` | The selected pre-upstream ext_authz host model has no committed upstream response on which to apply a late log-only intervention. |
| `late_intervention_abort` | `unsupported_by_host_model` | The selected pre-upstream ext_authz host model has no upstream response-phase point from which the authorization service can perform a late connection abort. |
| `late_intervention_status_metadata` | `unsupported_by_host_model` | The selected ext_authz integration does not observe an upstream response, so it cannot produce Phase-4 metadata that distinguishes original and visible upstream-response status or late actions. |
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
- Source-Contract: `connectors/traefik/metadata.c`, `connectors/traefik/config/traefik-forwardauth-dynamic.yaml`, `connectors/traefik/config/traefik-forwardauth.conf`, `connectors/traefik/src/traefik_forwardauth_service_main.c`, `connectors/traefik/src/traefik_modsecurity_mapper.c`, `connectors/traefik/scripts/runtime_smoke.py`

Host-Modell-Grenzen:

- The selected forwardAuth service observes the authorization request before the upstream request and cannot inspect the later upstream response headers or body.
- Traefik v3.7 supports buffered forwardAuth request bodies with forwardBody and maxBodySize, but the checked-in dynamic configuration does not enable them and the service config sets request_body_mode=none.
- Traefik documents that forwardBody buffering breaks streaming, so streaming request-body inspection is outside this host path.
- The authorization service currently sees the Traefik-to-service socket endpoints and does not map original client connection endpoints into Common connection metadata.

| Capability | Zustand | Kanonischer Grund (aus dem Manifest) |
|---|---|---|
| `connection_metadata` | `not_implemented` | The HTTP authorization service maps its local Traefik peer socket rather than the original client connection metadata. |
| `request_headers` | `implemented_not_asserted` | Configured forwardAuth request headers are mapped into Common Runtime; canonical multi-header and limit evidence is pending. |
| `request_body_buffered` | `not_implemented` | Traefik v3.7 supports forwardBody plus maxBodySize, but the checked-in middleware omits both and the connector config disables request bodies; see the versioned official reference. |
| `request_body_streaming` | `unsupported_by_host_model` | Traefik v3.7 documents that forwardBody reads and buffers the body before forwarding and therefore breaks streaming. |
| `response_headers` | `unsupported_by_host_model` | forwardAuth runs before the upstream request and does not receive the later upstream response headers. |
| `response_body_buffered` | `unsupported_by_host_model` | forwardAuth does not receive the later upstream response body. |
| `response_body_streaming` | `unsupported_by_host_model` | forwardAuth does not receive an upstream response body stream. |
| `phase1` | `implemented_not_asserted` | The forwardAuth request headers enter the Common Runtime Phase-1 path; a fresh canonical baseline result is pending. |
| `phase2` | `not_implemented` | The checked-in host middleware does not set forwardBody and the connector config disables request-body processing. |
| `phase3` | `unsupported_by_host_model` | The pre-upstream forwardAuth call cannot inspect upstream response headers. |
| `phase4` | `unsupported_by_host_model` | The pre-upstream forwardAuth call cannot inspect upstream response bodies. |
| `phase4_rule_evaluation` | `unsupported_by_host_model` | The selected Traefik forwardAuth integration runs before upstream handling and cannot inspect the later upstream response body for Phase-4 rule evaluation. |
| `phase4_pre_commit_deny` | `unsupported_by_host_model` | Because forwardAuth never sees the later upstream response, it has no Phase-4 response point at which to deny before the response commits. |
| `late_intervention` | `unsupported_by_host_model` | The authorization decision completes before the upstream response starts, so the chosen path has no response-phase late intervention point. |
| `late_intervention_log_only` | `unsupported_by_host_model` | The selected pre-upstream forwardAuth host model has no committed upstream response on which to apply a late log-only intervention. |
| `late_intervention_abort` | `unsupported_by_host_model` | The selected pre-upstream forwardAuth host model has no upstream response-phase point from which the authorization service can perform a late connection abort. |
| `late_intervention_status_metadata` | `unsupported_by_host_model` | The selected forwardAuth integration does not observe an upstream response, so it cannot produce Phase-4 metadata that distinguishes original and visible upstream-response status or late actions. |
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
- Source-Contract: `connectors/lighttpd/metadata.c`, `connectors/lighttpd/config/lighttpd-native.conf`, `connectors/lighttpd/module/mod_msconnector.c`, `connectors/lighttpd/src/lighttpd_modsecurity_mapper.c`, `connectors/lighttpd/harness/runtime_lighttpd_smoke.sh`

Host-Modell-Grenzen:

- The native plugin deliberately rejects non-none request and response body modes until safe lighttpd body hooks, limits, buffering, and intervention timing are implemented.
- The response-header mapper is called from handle_response_start, but source wiring alone is not Phase-3 behavioral verification.
- The legacy bridge and starter self-tests are separate from native mod_msconnector.so host-runtime evidence.

| Capability | Zustand | Kanonischer Grund (aus dem Manifest) |
|---|---|---|
| `connection_metadata` | `implemented_not_asserted` | The native mapper reads lighttpd client and server socket endpoints into Common Runtime; canonical evidence is pending. |
| `request_headers` | `implemented_not_asserted` | The native URI-clean hook maps lighttpd request headers into Common Runtime; canonical header evidence is pending. |
| `request_body_buffered` | `not_implemented` | The native module requires request_body_mode=none and supplies no request body to the mapper. |
| `request_body_streaming` | `not_implemented` | No native lighttpd request-body hook or streaming transaction contract is implemented. |
| `response_headers` | `implemented_not_asserted` | handle_response_start maps response headers into Common Runtime, but a real Phase-3 rule result has not yet been attached. |
| `response_body_buffered` | `not_implemented` | The native module requires response_body_mode=none and supplies no response body to the mapper. |
| `response_body_streaming` | `not_implemented` | No native lighttpd response-body hook or streaming transaction contract is implemented. |
| `phase1` | `implemented_not_asserted` | The URI-clean hook starts the transaction and processes request headers; a fresh canonical Phase-1 result is pending. |
| `phase2` | `not_implemented` | Request bodies are explicitly disabled in the native plugin, so a real Phase-2 body rule cannot run. |
| `phase3` | `implemented_not_asserted` | The response-start hook invokes Common Runtime response processing with mapped headers; real Phase-3 behavioral evidence is pending. |
| `phase4` | `not_implemented` | Response bodies are explicitly disabled in the native plugin, so a real Phase-4 body rule cannot run. |
| `phase4_rule_evaluation` | `not_implemented` | The current native module does not supply response-body data to ModSecurity, so it cannot yet evaluate Phase-4 rule 1100301. |
| `phase4_pre_commit_deny` | `not_implemented` | The current native module has no response-body hook or Phase-4 intervention timing implementation from which to deny before response commitment. |
| `late_intervention` | `not_implemented` | The module has no response-body or post-commit intervention policy; the response-start hook is not late-intervention evidence. |
| `late_intervention_log_only` | `not_implemented` | The current native module implements no post-commit response-body intervention policy or log-only late-intervention action. |
| `late_intervention_abort` | `not_implemented` | The current native module implements no response-body late-intervention path that can abort a committed connection. |
| `late_intervention_status_metadata` | `not_implemented` | Without a native response-body Phase-4 path, the module does not yet emit late-intervention metadata separating requested WAF status, original host status, visible client status, requested action, and actual action. |
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
| Declared input | `connectors/apache/capabilities.json` | `ce13177afa0686f9357ae4945b42fc11073e17de661fcc3196514020287a507b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/nginx/capabilities.json` | `93c20b58628a286abe7bc3810546a52509828709fef723f39b1cf8f9ea6c9698` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/haproxy/capabilities.json` | `39517a94d913562641c973c9844ff3439ffbdc4c1ff79f6c7cd64f831a5b8fa8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/envoy/capabilities.json` | `ae7f73116a211e15114ea484313a72aea99adec5a7fe318821d821d707af2a81` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/traefik/capabilities.json` | `2bdcf75907d869e6b33b41f801abe764897abaef63551e198674c972037d21bd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/lighttpd/capabilities.json` | `5e5d114428c30316fe26097ccff5e2ecfd59bf5e37d4c323d95d9e5eba012710` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `connectors/apache/capabilities.json` | present | input file available |
| `connectors/nginx/capabilities.json` | present | input file available |
| `connectors/haproxy/capabilities.json` | present | input file available |
| `connectors/envoy/capabilities.json` | present | input file available |
| `connectors/traefik/capabilities.json` | present | input file available |
| `connectors/lighttpd/capabilities.json` | present | input file available |
