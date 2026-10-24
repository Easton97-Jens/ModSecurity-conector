## I12 Traefik evidence — continuation of 18 October 2026

**Language:** English | [Deutsch](i12-traefik-evidence-20261015.de.md)

## Current review status — 18 October 2026

Status remains **I12_PARTIAL**: **6 historical lifecycle PASS, 1 historical qualified FAIL and 273 unqualified required IDs**. No new host lifecycle has been promoted by Root. Independent source review now resolves **56 of the original 124 expectations;68 remain open**. A source-resolved expectation establishes an oracle, not a host execution or lifecycle PASS.

| Route | Required IDs | Historical lifecycle PASS | Historical qualified FAIL | Unqualified IDs | Original oracles resolved | Original oracles open |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `traefik-native-uds` | 118 | 2 | 0 | 116 | 30 of 55 | 25 |
| `traefik-forwardauth-request` | 93 | 2 | 0 | 91 | 15 of 39 | 24 |
| `traefik-forwardauth-response-companion` | 69 | 2 | 1 | 66 | 11 of 30 | 19 |
| Total | 280 | 6 | 1 | 273 | 56 of 124 | 68 |

The same 273 lifecycle-unqualified IDs are listed in the historical appendix preserved below. The current per-ID reconciliation is retained under `R18/root-source52-reconciliation-20261018/summary.json` and `ledger.json`, where `R18` is `/var/tmp/codex/ModSecurity-conector/runs/i12-traefik-acceptance-20261015`. These are local retained artifacts; a durable published evidence package is still outstanding.

## Current source and oracle boundaries

The telemetry and original-method product corrections were integrated from #382 through #410 (`f8ce4c1342e29a20070029738663f86716488ccf` integration) into the published #413 revision `782f31ed78353b59a0dcd63978638ae5b107f8cf`. Corrected host telemetry has been observed, but the historical qualified FAIL remains unchanged until a separately reviewed lifecycle retest is qualified. The statements about unchanged product source and the old 4-resolved/120-open count in the 15 October report describe that historical snapshot.

`R18/root-sdk-review-20261018-v3` supersedes only ten unsupported native P2 `backend_request_count=0` expectations from v2. Pinned Go transport source permits backend headers before native request-body inspection completes; the actual independent early-header backend count remains mandatory. No replacement count is inferred from the host result. Named forwardAuth backend-exclusion obligations are unchanged. The v2 records and original contracts remain immutable; source review never manufactures missing client bytes, native EOS, Finish/Free or cleanup evidence.

## Retained continuation runs

| Capture | Actual retained extent | Qualification boundary |
| --- | --- | --- |
| Native v4 | 118 original attempt rows completed | Older sealed product source and explicit staged instrumentation; Root 35-field packet review pending |
| Auth v12 request / companion | 93 +69 original IDs;179 physical directories including controls | Two companion producer client timeouts; canonical fixture-variant and File/API gaps remain |
| Native v5 | Selected41 IDs,54 executions; controller exit0, timeoutfalse | Root's 12 pre-host SDK controls pass and sink expectations match physical evidence; full Root review pending |
| Native v7 kernel transport | Two IDs; two producer failures | First before-neighbor receives404 during startup, first target times out after30seconds, second before-neighbor times out; zero observed short-write/EAGAIN/resume proofs |

Native v7 has **no qualified PASS and no product-failure claim**. Its retained physical review is `R18/native-current/v7-physical-review-v1/review.json`; controller completion does not repair failed client production. Every v4/v5/v7 result stays bound to its actual older sealed source revision, staged delta, executable/configuration and run. None is relabeled as a capture of `782f31ed78353b59a0dcd63978638ae5b107f8cf`.

The export manifests bind Native v4/v5/v7 to `770dd71b76bad4cf8ce9e98880e3028b76945892` and Auth v12 to `a29019558678222b88913be0e202db3c9d14323a`, each with its retained explicit instrumentation delta.

The independent Auth v12 audit is under `R18/auth-v12-root-audit-20261018`. All 179 pending packets contain 35 observation fields and retain their original expectations, but are still `pending_root`. In both routes, `finish_failure_propagation` has zero actual client bytes/no HTTP status despite writer200/body33 and Common visible200/committed telemetry. Writer/Common commit state is not a TCP delivery proof. Native API returns, injected returns, native EOS, once-only logging/Free and actual client framing require separate reconciliation. All 179 MIME-gate observations remain null; absence is not zero or an inspection PASS.

The same audit separates host request 4097 rejection401 with no target authorization/native/backend request from the delivered4096-byte sample. A delivered sample does not prove inspection beyond the native body policy. Authorization response 32768 reaches client200/backend1;32769 yields host401/backend0 despite authorizer200. The companion application separately delivers40019 bytes. `maxResponseBodySize=32768` remains exclusively authorization-response capacity.

The original four File obligations across the three routes remain mandatory gaps. Supported native File calls and missing native/MRC1 contracts cannot be replaced with an unsupported or not-applicable disposition. Original canonical fixture variants, strict admission, error-phase boundaries and complete per-allocation EOS/Finish/Free/cleanup still need the exact required proof.

## Verified-TLS baseline and delivery still pending

The corrected TLS source at `782f31ed78353b59a0dcd63978638ae5b107f8cf` passed 31 TLS/Auth controls and 42 documentation checks. Actual host attempt `R18/relay-tls-host-current/isolation/attempt-1792321692553561516` now completed with controller exit0, timeoutfalse, no namespace survivors/mount leaks and all five processes exiting0. Its real effective configuration uses HTTPS, the fresh private CA/IP-SAN leaf, `insecureSkipVerify: false`, `preserveRequestMethod: true` and the unchanged 32768 capacity. All15 delivered authorization sample hashes/lengths match their physical receipts.

| Existing TLS baseline cases | Actual client status/entity bytes | Backend requests |
| --- | --- | ---: |
| allow | 200/26 | 1 |
| p1-deny, p2-deny, engine-limit, limit-boundary | 403/15 each | 0 each |
| host-limit | 401/0 | 0 |
| p3-deny | 403/0 | 1 |
| p4-safe | 200/19 | 1 |
| large-response | 200/40019 | 1 |
| observer-abort | No HTTP status/0; client command exit1 | 1 |
| observer-no-handle, observer-invalid-handle | 503/34 each | 0 each |
| mrc1-error | 503/30 | 0 |
| auth-cap-boundary | 200/38 | 1 |
| auth-cap-overlimit | 401/0 | 0 |
| neighbor | 200/29 | 1 |

This exercises actual Traefik HTTPS authorization and physical failure paths; it is **not16 client PASS**. Fifteen client commands exit0, while observer-abort retains EOF/zero client bytes and its parsing error/exit1. Native allocation/logging/Free are15 each, request EOS14 and response EOS5; final pending/live mappings are0. The abort has response EOS0. The companion socket is removed and the socket directory is empty. The actual P4 event now has `late_intervention=true`, `late_intervention_mode=safe`, requested deny and actual log_only, without promoting the historical FAIL. Actual public CA/leaf/receipt hashes match the three public build-manifest entries; separate public-certificate chain/IP-SAN/server-purpose verification passes. Only private-key presence/mode metadata was inspected: leaf0600 under0700. Key bytes/hashes remain excluded from public artifacts/manifests.

At the exact 782f head, Sonar Quality Gate is OK with security rating A, but the stricter zero-findings requirement still has **five S1192 findings** for duplicated TLS filename literals. Accepted findings, hotspots and duplication are0. The local source correction passes31 existing TLS/Auth controls; hosted resolution on the next published head remains pending. The retained hosted readback contains28 checks: Sonar success1, skipped2, pending25. These time/head-bound observations establish no all-green, complete I12 acceptance, `verified_pr` or durable artifact publication. This continuation documents functional tests and evidence review; no additional deep security assessment is included.

## Historical report and appendix — 15 October 2026, preserved verbatim


# I12 Traefik evidence — 15 October 2026

**Language:** English | [Deutsch](i12-traefik-evidence-20261015.de.md)

Status: **I12_PARTIAL**. The reviewed result is **6 lifecycle PASS, 1 lifecycle FAIL and 273 unqualified required IDs**. Three new PASS and one FAIL concern three freshly executed transactions; two different companion oracles evaluate the same P4 transaction. Three existing PASS remain separate. Of the original124 open expectations,121 remained after the existing3 resolutions. Exactly one further original expectation is independently resolved: **120 remain open**.

| Route | Required IDs | Lifecycle PASS, baseline + new | Lifecycle FAIL | Unqualified | Original oracles unresolved |
| --- | ---: | ---: | ---: | ---: | ---: |
| `traefik-native-uds` | 118 | 1 + 1 | 0 | 116 | 53 of55 |
| `traefik-forwardauth-request` | 93 | 1 + 1 | 0 | 91 | 38 of39 |
| `traefik-forwardauth-response-companion` | 69 | 1 + 1 | 1 | 66 | 29 of30 |
| Total | 280 | 3 + 3 | 1 | 273 | 120 of124 |

The nine historical configuration-only PASS (native1/request8) remain without lifecycle qualification. The appendix lists all273 still-unqualified IDs. The qualified FAIL remains explicit; it is neither an unqualified case nor a PASS.

## Provenance and qualification

The isolated worktree starts from PR #410 remote head `f27eb59b53beff6f65384fc2e5037881a3052c01`. The existing central [capture infrastructure](../ci/runtime/lifecycle/i12/README.md) supplies distinct `traefik-native` and `traefik-forwardauth` variants. Only Traefik-specific fixtures, producers, tests and this report are added; product/Common source, central matrix/shared generators and Framework/MRTS remain unchanged. The UDS regression harness correction preserves the product deadline and worker limit.

External evidence root `R` is `/var/tmp/codex/ModSecurity-conector/runs/i12-traefik-20261015`. Exact paths, hashes, effective configuration, loaded executable/library maps, raw client/backend bytes and controller admission/cleanup receipts remain there. The host is Traefik3.7.13 (binary built with Go1.26.8); the separate execution/build toolchain is Go1.27.2 and SDK3.0.14. Private nonroot controllers retain isolation and resource checks; observation overlays are source/hash-bound test copies. Source export, successful compilation, client EOF or a driver exit alone cannot qualify a lifecycle.

The immutable [original inventory](../connectors/traefik/harness/fixtures/i12_original_inventory.json) retains all 280 selected contracts and original dispositions. `R/root-reviewed/traefik-ledger-final-v2.json`, `oracle-reviews.json` and `packets-all.json` record the separately reviewed Traefik result. The new exact ID is `I12::traefik-native-uds::NEED-request-streaming`; the existing qualified IDs remain native/request `NEED-request-eos-once` and companion `NEED-observer-response-eos`.

## Native UDS

Corrected captures: functional attempt `1792072946603518992`, fault attempt `1792072950400546981`, MIME attempt `1792072953883553989`, under `R/native/isolation/attempt-<ID>`. Summaries are `initial-host-v2-review.json`, `faults-host-v2-review.json` and `mime-host-v2-review.json`. Each corrected controller returns0 with no surviving namespace processes or outside mount leaks and final native pending calls/mappings0.

The new streaming PASS binds a connector-free native oracle to the exact 32 request bytes/hash and three 7/12/13-byte appends, followed by exactly one native request-body finalization. Its independently established result is allow/200/phase2. `R/independent-request-oracle` and the independent streaming build/run receipts retain the comparison. `R/root-reviewed/native-request-streaming.json` contains the 35-field reviewed lifecycle packet; `native-request-streaming-retest.json` binds the exact ID and oracle digest.

The actual host has 48 matching callback rows, three request and three response native appends, host EOS opcodes 3/6 and nested native request/response finalization once. Client200/33B matches the independent backend; one statusline, complete Content-Length and actual TCP EOF are observed. RuntimeFinish1, nativeLogging1 and nativeFree1 are distinct from Commonfinish2 idempotent calls. The completed-state transition may occur in final phase completion before finish. TCP EOF is not substituted for native EOS.

| Functional probe | Actual client status/body | Independent backend requests |
| --- | --- | ---: |
| Allow chunks | 200/33B | 1 |
| P1 deny | 403/17B | 0 |
| P2 deny | 403/17B | 0 |
| P3 deny | 403/17B | 1 |
| Late P4 Safe | 200/33B | 1 |
| MIME excluded / neighbor | 200/29B each | 1 each |

The MIME/charset matrix additionally measures absent Content-Type, absent charset, ISO8859-1 and UTF8 arguments on the appropriate request/response paths. All 8 actual exchanges have exact200 bodies. Native debug explicitly rejects response inspection for `application/octet-stream` and names `text/plain` as the selected allowlist; MIME-in produces an actual phase4 body-rule match. Wrapper append calls and200 alone do not prove inspection. ASCII fixture bodies do not establish non-ASCII recoding correctness.

The real-engine fault relay records exact physical opcodes. Corrupt MSE1 begin reply produces500/56B; internal error 5 after actual request EOS produces500/41B. `AcknowledgeApplied` uses opcode 10: its injected error produces zero client bytes and EOF, nativeFree1, no second response and no runtimeFinish. This technical failure is distinct from the earlier native P1 deny.

For an actual post-commit error, the client receives200 and8192 of the advertised16384 bytes before internal error 5 on the second response chunk. The host's header/body writes and first client receive precede the error. The connection ends with incomplete framing, no second response, no response EOS and nativeFree1. The generic full-body probe oracle remains false; this is not silently promoted to a complete-response PASS or a proven product defect.

Active client RST during the delayed16KiB response yields requestEOS1/responseEOS0, runtimeFinish0/nativeFree1; the independent neighbor succeeds. Successful allow now has complete native EOS; the historical allow/client-cancel/EOS discrepancy remains preserved. Earlier small-body cancellation occurred after completion and is retained separately.

Strict is rejected before traffic at `transaction_profile`: the current native profile has no strict post-commit capability and the runtime enforces that admission check. No supported Strict lifecycle is claimed. Its initial controller recorded two surviving processes; `R/native/strict-cleanup-audit.json` later proves both absent without sending an unverified signal. Initial cleanup remains a recorded failure.

## ForwardAuth request

`R/auth/request-v6-observed.json` binds14 actual host exchanges,13 targets plus neighbor, to separate attempt `1792073095947554957`. Controller0, no survivors/mount leaks, socket removed; native allocation/logging/free13 each and final pending/mappings0. The new complete PASS `I12::traefik-forwardauth-request::allow_without_marker` is in `R/root-reviewed/request-allow_without_marker.json`: identical15sample/backend bytes, authorization200, client200/26complete bytes, native P1/P2/EOS once, once native finalization/free and independent neighbor.

| Probe | Authorization sample/status | Client status/entity bytes | Backend requests |
| --- | --- | --- | ---: |
| Allow | 15B/200 | 200/26B | 1 |
| P1 deny | 15B/403 | 403/15B | 0 |
| P2 deny | 17B/403 | 403/15B | 0 |
| Native engine limit | 1500B/403 | 403/15B | 0 |
| Host sample boundary | 4096B/403 | 403/15B | 0 |
| Host limit exceeded | No authorization request/native scope | 401/0B | 0 |

Host buffering errors, native1024-byte Reject and technical observer/transport failures remain separate. The sample EOS callback proves actual Content-Length, buffered bytes and remaining0. Native events record GET while the original client sends POST; original-method inspection is not claimed. Inspection beyond the delivered sample or native body policy is not demonstrated.

The separate capacity run `1792073637547502847`/`R/auth/capacity-v7-observed.json` measures the authorization-response bound. The real engine authorizes both cases with200/16B; an explicit test relay subsequently changes only the synthetic authorization response:

| Relay authorization response | Actual client | Backend requests |
| --- | --- | ---: |
| 32768B | 200/38B, complete framing | 1 |
| 32769B | 401/0B, complete framing | 0 |
| Independent neighbor | 200/29B | 1 |

This is measured host capacity rejection, not native403 denial. Controller0, no survivors/mount leaks, pending/mappings0; the over-capacity case's unclaimed native handoff is logged/freed at service shutdown.

## Response companion

`R/auth/companion-v6-observed.json` comes from independent companion attempt `1792073375816854728`; its `attempt` field records the exact path. It contains14 actual exchanges, native allocation/logging/free13 each, controller0 and final pending/mappings0. No request execution is transferred into companion execution.

The new complete PASS `I12::traefik-forwardauth-response-companion::phase4_rule_observed` is in `R/root-reviewed/companion-phase4_rule_observed.json`: observed handle registration/claim association, native P3/P4, two response appends, host/native response EOS, companion finish/release and native logging/free once; client200/19complete bytes. Commonfinish2 are idempotent calls, not two native finalizations. One extra FD is the lazily-created companion listener, verified by kernel inode/path/accept flag; no connected UDS session survives aftercase.

P3 denial gives403/0B after one backend request. Missing or syntactically invalid handles give503/34B and backend0; an unknown correctly64hex-formatted handle was not tested. The explicit same-UID MRC1 fault peer receives a real12-byte MRC1 header and returns `BAD!`; the host gives503/30B with backend0. This is a technical parser/transport error, not a native engine decision.

Observer abort: actual header/body writer calls and commit ACK, but zero client bytes/EOF; no native P4, one session-fail, logging and free. A writer call alone does not establish delivery to the client. Unclaimed handle-error handoffs are retired at shutdown; immediate per-request release is not inferred.

`maxResponseBodySize=32768` remains unchanged and protects only authorization-response capacity. The application delivers40019complete Content-Length bytes with matching backend/client SHA256 `1eb178f60b2dec89f5af85451fc49fb1dee17f685d1ff92f8dffe1c789070a70`. In the independent companion run, first client bytes at52020203548419ns precede native P4 at52020205146517ns and host outcome at52020206377362ns. Native response policy1024/Reject and its late Safe log-only outcome remain separate. The Common `body_bytes_inspected` counter describes bytes delivered to the engine according to the product source comment; it does not prove full native inspection.

## Confirmed product defect and handoff to #382

`I12::traefik-forwardauth-response-companion::phase4_deny_after_commit_log_only_safe` is a **fully qualified FAIL**. Both separate realhost runs physically write a complete `MSCONN_EVENT_PHASE4_LATE_INTERVENTION` event for rule1100301 with `response_committed=true`, `headers_sent=true`, requested deny403, actual `log_only` and visible200, but `late_intervention=false`; required `late_intervention_mode` is absent. The narrower rule-observation PASS does not conceal this metadata defect; both oracles use the same companion P4 transaction.

Independent review excludes capture interference: the transport file and complete event-emission function match product bytes. MRC1 stores the native decision and forwards it at host outcome without setting the late flag. Event formatting copies that flag and adds mode only when true, while event classification independently recognizes committed P4/log-only. Native MSE1 explicitly sets the flag. Impact: consumers filtering late flag/Safe mode can miss genuinely late interventions. No enforcement failure is demonstrated. Reproducer and [product handoff to #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382#issuecomment-6194758198) are linked from [Draft PR #413](https://github.com/Easton97-Jens/ModSecurity-conector/pull/413); no product repair is included.

## Verification and retained failures

Fresh `go test -count=1 ./...`, `go test -count=1 -race ./...` and `go vet ./...` pass for native middleware, response observer and composite middleware. Actual native service/UDS tests pass after the bounded worker-saturation harness retake, preserving the 64-worker limit, peer deadline, independent follow-up and socket replacement. The initial BrokenPipe race and overlong test socket-path failures remain retained separately from the passing retakes. Security-contract and central capture integrity/guard checks pass. Exact wrapped commands/statuses/hashes are under `R/verification`; final scoped test counts are reconciled by the delivery review.

All 23 focused Traefik I12 tests pass, including eight native no-write path/CLI controls. The three native evidence-control tests pass: TCP EOF/client success cannot synthesize native EOS, enter/return pairs are not counted twice, and runtime associations require a verified allocation join. The central observer initially admitted only two historical synthetic IDs; early matrix runs therefore remain partial. The corrected allowlist expands only to 18 explicit synthetic IDs in a separately sealed observation copy. A first acknowledgment fixture targeted opcode 7 and never exercised opcode 10; it remains excluded. The independently confirmed companion telemetry defect is preserved as the qualified FAIL and handed off to #382. Historical v4 YAML setup failures and their initial cleanup failures remain unchanged; later PID-absence receipts do not relabel initial cleanup as passed.

## Hosted quality gate and bounded triage

At initial PR head `de348eec93721741a3eca6e945009fc4a7b3e979`, SonarCloud reports **ERROR**: `new_security_rating=5` (E), required at most1 (A). Canonical `rtk proxy /usr/local/bin/sonar-with-env quality-gate status -p Easton97-Jens_ModSecurity-conector --pull-request 413 --format json` returned51; the complete condition/breakdown is retained under `R/verification/sonar-initial-head-quality-gate.*`. This is separate from the qualified companion product FAIL.

Independent read-only triage covered all15 returned signals. Ten `json:S6418` values are source-file SHA256 fingerprints, each verified against the named file at original parent `8c574cdf86f10af976297c31d31485b042eba73b`; none is a credential. Two temporary-directory signals concern fresh0700 outputs under root-owned storage with physical-path/Git guards. The YAML filename and fault-relay socket path are supplied by the sealed driver inside private `/task`; bind failure occurs before socket cleanup. The authorization relay always connects to `127.0.0.1` plus the operator's engine port; the request target does not select the destination, and the private network contains loopback only. No reachable vulnerability was validated in these15 signals under the reviewed controller. Shared-writable ancestors, hostile CLI callers or a different upstream proxy would require new validation.

These are local technical dispositions, including false-positive candidates; no Sonar issue/hotspot disposition, rule or gate was changed. The gate remains failed, so this Draft is **not verified_pr**. Current-head checks and subsequent analysis must be read from the external delivery receipts after each push; an older analysis is not a pass for a new head.

## Remaining lifecycle-unqualified IDs

All273 suffixes below come from the immutable inventory and reviewed final ledger. Each suffix takes its route prefix. Configuration-only PASS remain included; the6 lifecycle PASS and1 lifecycle FAIL are excluded.

### `I12::traefik-native-uds::` — 116

```text
allow_without_marker
deny_header_marker_403
deny_with_alternative_status
transaction_id_present
transaction_id_generated_or_fallback
deny_request_body_marker_403
deny_response_header_marker_403
phase4_rule_observed
phase4_deny_after_commit_log_only
phase4_event_contains_original_status
phase4_event_contains_late_intervention_action
multiple_headers
duplicate_header_names
empty_header_value
case_insensitive_header_name
invalid_content_length
conflicting_content_length
duplicate_transfer_encoding
content_length_overflow
body_size_nonzero_with_null_data
header_count_nonzero_with_null_headers
event_contains_connector
event_contains_transaction_id
event_contains_rule_id
event_contains_phase
event_contains_status
event_metadata_truncation
event_has_no_request_body_payload
event_has_no_response_body_payload
event_json_limit
unsafe_event_path
single_request_cleanup
multiple_sequential_requests
early_mapping_failure_cleanup
transaction_begin_failure_cleanup
finish_failure_propagation
clean_shutdown
allow
deny
log_only
phase1_allow
phase1_deny_403
phase1_alternative_status
phase1_transaction_id
phase2_request_body_rule
phase2_marker_split_across_chunks
phase2_no_payload_event
phase3_response_header_rule
phase3_deny_before_commit
phase3_original_and_visible_status
phase4_marker_split_across_chunks
phase4_end_of_stream_evaluation
phase4_deny_after_commit_log_only_minimal
phase4_deny_after_commit_log_only_safe
phase4_status_metadata
phase4_action_metadata
phase4_no_payload_event
phase4_no_full_response_buffering
phase4_first_byte_before_response_end
engine_timeout_before_commit
engine_timeout_after_commit
response_short_write_resume
response_write_would_block_resume
NEED-p3-redirect
NEED-request-empty
NEED-request-single-chunk
NEED-request-file
NEED-request-content-type-present
NEED-request-content-type-missing
NEED-request-charset-present
NEED-request-charset-missing
NEED-request-mime-scope-in
NEED-request-mime-scope-out
NEED-request-csv
NEED-request-reject
NEED-request-process-partial
NEED-request-above-former-connector-limit
NEED-request-marker-at-payload-end
NEED-response-empty
NEED-response-single-chunk
NEED-response-file
NEED-response-streaming
NEED-response-content-type-present
NEED-response-content-type-missing
NEED-response-charset-present
NEED-response-charset-missing
NEED-response-mime-scope-in
NEED-response-mime-scope-out
NEED-response-csv
NEED-response-reject
NEED-response-process-partial
NEED-response-above-former-connector-limit
NEED-response-marker-at-payload-end
NEED-invalid-native-return
NEED-missing-eos
NEED-invalid-metadata
NEED-physical-event-sink-open
NEED-physical-event-sink-write
NEED-physical-event-sink-short-write
NEED-physical-event-sink-flush
NEED-physical-event-sink-close
NEED-timeout
NEED-cancel
NEED-client-response-bytes
NEED-client-exit-signal
NEED-incomplete-framing
NEED-abort-reset-observation
NEED-neighbor-connection-stream
NEED-p1-rate-limit
NEED-redirect
NEED-uds-error
NEED-mse1-error
NEED-mrc1-error
NEED-commit-ack-applied
NEED-no-second-response
HIST-TRAEFIK-NATIVE-PROTOCOL-ERROR
```

### `I12::traefik-forwardauth-request::` — 91

```text
deny_header_marker_403
deny_with_alternative_status
transaction_id_present
transaction_id_generated_or_fallback
deny_request_body_marker_403
multiple_headers
duplicate_header_names
empty_header_value
case_insensitive_header_name
invalid_content_length
conflicting_content_length
duplicate_transfer_encoding
content_length_overflow
body_size_nonzero_with_null_data
header_count_nonzero_with_null_headers
event_contains_connector
event_contains_transaction_id
event_contains_rule_id
event_contains_phase
event_contains_status
event_metadata_truncation
event_has_no_request_body_payload
event_json_limit
valid_rules_file
missing_rules_file
invalid_rule_syntax
unknown_config_key
invalid_boolean
invalid_status
invalid_size
unsafe_event_path
single_request_cleanup
multiple_sequential_requests
early_mapping_failure_cleanup
transaction_begin_failure_cleanup
finish_failure_propagation
clean_shutdown
allow
deny
log_only
redirect_if_supported
phase1_allow
phase1_deny_403
phase1_alternative_status
phase1_redirect
phase1_transaction_id
phase2_request_body_rule
phase2_at_limit
phase2_over_limit
phase2_truncated
phase2_no_payload_event
keepalive_allow_allow
keepalive_allow_deny_allow
NEED-request-empty
NEED-request-single-chunk
NEED-request-multiple-chunks
NEED-request-file
NEED-request-content-type-present
NEED-request-content-type-missing
NEED-request-charset-present
NEED-request-charset-missing
NEED-request-mime-scope-in
NEED-request-mime-scope-out
NEED-request-csv
NEED-request-above-former-connector-limit
NEED-request-marker-at-payload-end
NEED-precommit-error
NEED-postcommit-error
NEED-invalid-native-return
NEED-missing-eos
NEED-invalid-metadata
NEED-physical-event-sink-open
NEED-physical-event-sink-write
NEED-physical-event-sink-short-write
NEED-physical-event-sink-flush
NEED-physical-event-sink-close
NEED-timeout
NEED-cancel
NEED-budget-precommit
NEED-budget-postcommit
NEED-client-response-bytes
NEED-client-exit-signal
NEED-incomplete-framing
NEED-abort-reset-observation
NEED-first-byte-before-late-error
NEED-neighbor-connection-stream
NEED-complete-sample
NEED-incomplete-sample
NEED-host-request-buffer-bound
NEED-host-auth-response-32768-bound
NEED-backend-excluded-on-deny
```

### `I12::traefik-forwardauth-response-companion::` — 66

```text
deny_response_header_marker_403
phase4_deny_after_commit_log_only
phase4_event_contains_original_status
phase4_event_contains_late_intervention_action
event_has_no_response_body_payload
unsafe_event_path
single_request_cleanup
multiple_sequential_requests
early_mapping_failure_cleanup
transaction_begin_failure_cleanup
finish_failure_propagation
clean_shutdown
phase3_response_header_rule
phase3_deny_before_commit
phase3_redirect_before_commit
phase3_original_and_visible_status
phase4_marker_split_across_chunks
phase4_end_of_stream_evaluation
phase4_deny_after_commit_log_only_minimal
phase4_status_metadata
phase4_action_metadata
phase4_no_payload_event
phase4_in_scope_content_type
phase4_content_type_with_charset
phase4_out_of_scope_content_type
phase4_missing_content_type
phase4_no_full_response_buffering
phase4_first_byte_before_response_end
phase4_body_at_limit
phase4_body_over_limit
phase4_body_process_partial
phase4_body_reject
full_lifecycle_event_metadata_bounded
engine_timeout_before_commit
engine_timeout_after_commit
response_short_write_resume
response_write_would_block_resume
NEED-allow
NEED-response-empty
NEED-response-single-chunk
NEED-response-file
NEED-response-streaming
NEED-response-charset-missing
NEED-response-csv
NEED-response-above-former-connector-limit
NEED-response-marker-at-payload-end
NEED-invalid-native-return
NEED-missing-eos
NEED-invalid-metadata
NEED-invalid-header
NEED-size-overflow
NEED-physical-event-sink-open
NEED-physical-event-sink-write
NEED-physical-event-sink-short-write
NEED-physical-event-sink-flush
NEED-physical-event-sink-close
NEED-timeout
NEED-cancel
NEED-client-response-bytes
NEED-client-exit-signal
NEED-incomplete-framing
NEED-abort-reset-observation
NEED-backend-count-exclusion
NEED-neighbor-connection-stream
NEED-host-commit
NEED-32768-auth-response-not-application-response
```
