# I12 Envoy: host measurements and remaining acceptance

**Language:** English | [Deutsch](i12-envoy-host-evidence-20261015.de.md)

Status: **PARTIAL**. Full acceptance of all 284 original cases has not been achieved.

Native/host evidence source revision: `f27eb59b53beff6f65384fc2e5037881a3052c01`.

The companion JSON preserves all 284 exact original IDs and their baseline results. New synthetic host probes have their own identities; only separately validated, individually approved full packets qualify original cases.

[i12-envoy-host-evidence-20261015.json](i12-envoy-host-evidence-20261015.json)

## Three separate route results

| Route | Original IDs | Lifecycle PASS | Config PASS | Without lifecycle | Original oracles | Open |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| envoy-ext-proc | 117 | 5 | 0 | 112 | 51 | 46 |
| envoy-ext-authz-request | 94 | 1 | 8 | 93 | 40 | 39 |
| envoy-ext-authz-response-companion | 73 | 1 | 0 | 72 | 34 | 33 |

Exact qualified IDs:

- `I12::envoy-ext-proc::NEED-request-eos-once`
- `I12::envoy-ext-proc::NEED-request-streaming`
- `I12::envoy-ext-proc::NEED-response-streaming`
- `I12::envoy-ext-proc::NEED-client-response-bytes`
- `I12::envoy-ext-proc::NEED-client-exit-signal`
- `I12::envoy-ext-authz-request::NEED-request-eos-once`
- `I12::envoy-ext-authz-response-companion::NEED-lease-claim`

The retained baseline contained 281 IDs without full host acceptance: 8 configuration-only PASS and 273 unqualified cases. Of the original 125 open oracles, 3 were resolved and 122 open. The retained baseline and its physical sources were revalidated with the current central validators. This Envoy task modified no shared validator. New qualifications are recorded separately with full receipts in the current state above.

## New physical host measurements

Each row is a measured probe, not a lifecycle verdict. HTTP/framing, transport closure, native phases and cleanup remain separate. Earlier failed attempts and retakes remain visible. Envoy ext_proc can begin an incomplete backend request before a P2 deny.

| Batch / probe | Route | Runner exit | Target HTTP | Neighbor HTTP | Backend starts | Overlap |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| host-v2/ext-proc-p1-deny | envoy-ext-proc | 77 | 403 | None | 0 | None |
| host-v2/ext-proc-streaming | envoy-ext-proc | 77 | 200 | 200 | 2 | False |
| host-v2/ext-proc-p2-deny | envoy-ext-proc | 0 | 403 | 200 | 2 | False |
| host-v2/ext-proc-p3-deny | envoy-ext-proc | 77 | 403 | 200 | 2 | False |
| host-v2/ext-proc-p4-deny-safe | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-v2/ext-proc-request-reject | envoy-ext-proc | 0 | 403 | 200 | 2 | False |
| host-v2/ext-proc-request-partial | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-v2/ext-proc-response-partial | envoy-ext-proc | 77 | 200 | None | 1 | None |
| host-v2/ext-proc-response-reject | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-v2/ext-proc-mime-out | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-v2/ext-authz-request-streaming | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-v2/ext-authz-request-p1-deny | envoy-ext-authz-request | 0 | 403 | 200 | 1 | False |
| host-v2/ext-authz-request-p2-deny | envoy-ext-authz-request | 77 | None | None | None | None |
| host-v2/ext-authz-request-host-reject | envoy-ext-authz-request | 77 | 413 | None | 0 | None |
| host-v2/ext-authz-request-host-partial | envoy-ext-authz-request | 77 | 503 | None | 0 | None |
| host-v2/ext-authz-request-request-reject | envoy-ext-authz-request | 0 | 403 | 200 | 1 | False |
| host-v2/ext-authz-request-request-partial | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-v2/ext-authz-response-companion-streaming | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-v2/ext-authz-response-companion-p3-deny | envoy-ext-authz-response-companion | 77 | 403 | 200 | 2 | False |
| host-v2/ext-authz-response-companion-p4-deny-safe | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-v2/ext-authz-response-companion-response-partial | envoy-ext-authz-response-companion | 77 | 200 | None | 1 | None |
| host-v2/ext-authz-response-companion-mime-out | envoy-ext-authz-response-companion | 77 | 200 | 200 | 2 | False |
| host-v2/ext-authz-response-companion-response-reject | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-v3/ext-authz-request-concurrent | envoy-ext-authz-request | 0 | 200 | 200 | 2 | True |
| host-v3/ext-proc-concurrent | envoy-ext-proc | 0 | 200 | 200 | 2 | True |
| host-v3/ext-authz-response-companion-concurrent | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | True |
| host-v3/ext-proc-streaming | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-v3/ext-proc-p1-deny | envoy-ext-proc | 0 | 403 | 200 | 1 | False |
| host-v3/ext-proc-p3-deny | envoy-ext-proc | 77 | 403 | 200 | 2 | False |
| host-v3/ext-proc-response-partial | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-faults-v2/ext-authz-response-companion-cancel | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | True |
| host-faults-v2/ext-proc-cancel | envoy-ext-proc | 0 | 200 | 200 | 2 | True |
| host-faults-v2/ext-proc-grpc-unavailable | envoy-ext-proc | 77 | 500 | 500 | 0 | False |
| host-faults-v2/ext-authz-response-companion-missing-lease | envoy-ext-authz-response-companion | 0 | 503 | 503 | 2 | False |
| host-faults-v2/ext-authz-response-companion-expired-lease | envoy-ext-authz-response-companion | 0 | 503 | 200 | 2 | False |
| host-faults-v2/ext-authz-request-grpc-unavailable | envoy-ext-authz-request | 77 | 500 | 500 | 0 | False |
| host-final/ext-authz-request-grpc-unavailable | envoy-ext-authz-request | 77 | 500 | 500 | 0 | False |
| host-final/ext-proc-grpc-unavailable | envoy-ext-proc | 0 | 500 | 500 | 0 | False |
| host-final/ext-proc-incomplete-response | envoy-ext-proc | 77 | 502 | 200 | 2 | False |
| host-final/ext-authz-response-companion-incomplete-response | envoy-ext-authz-response-companion | 77 | 502 | 200 | 2 | False |
| host-final/ext-proc-p3-deny | envoy-ext-proc | 0 | 403 | 200 | 2 | False |
| host-final/ext-authz-request-p2-deny | envoy-ext-authz-request | 0 | 403 | 200 | 1 | False |
| host-final/ext-authz-request-host-reject | envoy-ext-authz-request | 0 | 413 | 200 | 1 | False |
| host-final/ext-authz-response-companion-p3-deny | envoy-ext-authz-response-companion | 0 | 403 | 200 | 2 | False |
| host-final/ext-authz-request-host-partial | envoy-ext-authz-request | 77 | 503 | 200 | 1 | False |
| host-postcommit/ext-authz-response-companion-incomplete-response | envoy-ext-authz-response-companion | 77 | 200 | 200 | 2 | False |
| host-postcommit/ext-authz-request-grpc-unavailable | envoy-ext-authz-request | 0 | 500 | 500 | 0 | False |
| host-postcommit/ext-proc-incomplete-response | envoy-ext-proc | 77 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-request-streaming-0 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-request-content-type-present-1 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-request-charset-present-2 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-request-process-partial-3 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-response-streaming-4 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-response-content-type-present-5 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-response-charset-present-6 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-response-mime-scope-in-7 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-response-mime-scope-out-8 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-client-response-bytes-10 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-response-process-partial-9 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-client-exit-signal-11 | envoy-ext-proc | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-proc-need-neighbor-connection-stream-12 | envoy-ext-proc | 0 | 200 | 200 | 2 | True |
| host-originals/original-envoy-ext-proc-need-independent-neighbor-stream-13 | envoy-ext-proc | 0 | 200 | 200 | 2 | True |
| host-originals/original-envoy-ext-authz-request-need-request-multiple-chunks-14 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-request-need-request-content-type-present-15 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-request-need-request-charset-present-16 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-request-need-client-response-bytes-17 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-request-need-neighbor-connection-stream-18 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | True |
| host-originals/original-envoy-ext-authz-request-need-host-413-before-engine-20 | envoy-ext-authz-request | 0 | 413 | 200 | 1 | False |
| host-originals/original-envoy-ext-authz-request-need-complete-sample-19 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-request-need-native-engine-403-21 | envoy-ext-authz-request | 0 | 403 | 200 | 1 | False |
| host-originals/original-envoy-ext-authz-request-need-native-body-limit-22 | envoy-ext-authz-request | 0 | 403 | 200 | 1 | False |
| host-originals/original-envoy-ext-authz-request-need-native-body-limit-23 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-request-need-host-buffer-not-engine-limit-24 | envoy-ext-authz-request | 0 | 413 | 200 | 1 | False |
| host-originals/original-envoy-ext-authz-request-need-host-buffer-not-engine-limit-25 | envoy-ext-authz-request | 0 | 403 | 200 | 1 | False |
| host-originals/original-envoy-ext-authz-request-need-host-buffer-not-engine-limit-26 | envoy-ext-authz-request | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-allow-27 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-response-streaming-28 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-cancel-29 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | True |
| host-originals/original-envoy-ext-authz-response-companion-need-incomplete-framing-31 | envoy-ext-authz-response-companion | 77 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-client-response-bytes-30 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-backend-count-exclusion-32 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-neighbor-connection-stream-33 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | True |
| host-originals/original-envoy-ext-authz-response-companion-need-missing-correlation-34 | envoy-ext-authz-response-companion | 0 | 503 | 503 | 2 | False |
| host-originals/original-envoy-ext-authz-response-companion-need-lease-expiry-35 | envoy-ext-authz-response-companion | 0 | 503 | 200 | 2 | False |
| companion-retake-original-v1/original-envoy-ext-authz-response-companion-need-allow-0 | envoy-ext-authz-response-companion | 0 | 200 | 200 | 2 | False |
| fault-host-v1/ext-proc-drop-response-eos | envoy-ext-proc | 77 | 200 | 200 | 2 | False |

## Directed response-EOS fault probe

The directed real `envoy-ext-proc` probe removes only the target stream’s empty response EOS and then performs the actual gRPC half-close. The engine returns API status 14. Envoy’s own trace binds the received status-14 trailer, remote close and error callback to the same HTTP stream through the target nonce, connection ID and stream ID; a reset follows after HTTP 200 headers were already sent. The proxy still observes no wire status and does not turn that absence into success. The target client receives the exact 96-byte prefix in 64+32 chunks but no terminal zero chunk, then exits with an error. Native P1–P3 run; P4 and response EOS are absent, `runtime_finish` is attempted once and returns 0, while logging, free and cleanup are each observed once. The neighbor stream completes P1–P4 with a successful finish. Runner exit 77, controller exit 1, client exit 1 and `new_lifecycle_pass=0` are retained.


`None` denotes a missing measurement. A lower-bound backend count remains explicitly marked `request_count_is_lower_bound` in JSON. Runner exit 0 is not oracle acceptance; exit 77 remains non-PASS.

## Native identity and evidence chain

- Native/host evidence source revision: `f27eb59b53beff6f65384fc2e5037881a3052c01`.
- Envoy: `b579d07d3ad7ee11d32b105e91a5a39ad24718d7/1.39.1/Clean/RELEASE/BoringSSL`.
- Envoy image SHA256: `002c6e1c69ed0fa0ea381887247cadadfaec9481375fa8d8d2b1731eeabf40b8`.
- SDK: `ModSecurity v3.0.14 (Linux)`; SHA256 `32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407`.
- Go: `go1.27.2`; `go.mod`: `go 1.26.9`; `golang.org/x/net v0.61.0`.

The fresh C17/C++17/CGo build uses the same Envoy capture variant and common observer. Source copy, eight overlays, loaded images, effective configuration, separate real clients/backend, native scopes, actual EOS arguments, P1–P4, logging/free, Finish calls and physical event logs are hash-bound. A normal transaction needs one native logging/free and one logical Finish transition; two idempotent Common Finish calls are not two transitions.

A complete HTTP entity can be followed by a TCP reset. An observed local HTTP/2 reset does not prove remote `grpc-status`. With that status absent, successful gRPC completion remains false/unknown. Authorization success requires explicit trailers and the associated stream close.

## Request sample and response companion

`max_request_bytes` is the host buffer boundary. Native limit probes use a complete sample below the larger host capacity. Host 413 before the engine, rejected partial metadata with a technical gRPC error, native 403 intervention and actual backend effects are recorded separately. Multiple client writes are not multiple engine body callbacks for Authorization/Check.

The companion has its own runs for P3/P4, streaming, native response limits, missing/expired leases and cancellation. One shared HTTP receipt does not automatically qualify request and response together. Client timing overlap proves only the observed concurrency; ambiguous gRPC correlation remains unknown.

## Cleanup and isolation

UID/GID 65534, zero capabilities, NoNewPrivs 1, private network/PID/mount namespaces and listener boundaries are preserved. An old v5 run misclassified a foreign Traefik process as a survivor; its identity and namespace inode support inferred namespace-ID reuse after the Envoy run ended. It was not signalled; original exit 77 is retained. The Envoy-specific controller copy now holds a namespace FD positively bound to its own init through cleanup, revalidates identity before/after open and treats unprovable ownership as an error.

## Verification and limits

Native/CGo Go `./...`, race `./...` and vet `./...`: PASS. The historical f27 evidence contains 32 common native observer controls; the current afaf native-v3 run contains 34 PASS. The current complete Envoy evidence suite has 257 PASS with no skips. New controls cover unchanged IDs/oracles, physical hashes, absent gRPC trailers, ordered stream forwarding, sealed fault fixtures, substituted source/binaries, backend framing and namespace ownership races. Exact commands, outcomes and log hashes are in the referenced receipts.

Still open: complete independent oracle/original-ID acceptance, direct native MIME/charset selection, fully correlated concurrent gRPC terminal status, deliberate missing/repeated host callbacks, all physical event-sink failures and the complete observer stop/restart contract. P4 Strict is not claimed supported or accepted. Unit, native and race success do not replace these host proofs.

## Independent oracle review and original-ID retakes

All 125 original oracles were individually reviewed against source, SDK and host semantics. The three Envoy-owned review files preserve original oracles unchanged. Concrete new fixture/expectation proposals remain separate from canonical resolution and host acceptance:

| Route | Reviewed original oracles | New source proposals | Retaken original IDs |
| --- | ---: | ---: | ---: |
| envoy-ext-proc | 51 | 14 | 14 |
| envoy-ext-authz-request | 40 | 10 | 10 |
| envoy-ext-authz-response-companion | 34 | 9 | 9 |

New individually reviewed lifecycle PASS:

- `I12::envoy-ext-proc::NEED-request-streaming` — `7964c0c6075770e516a455c79fad486ceef0bc8f132398777402b06179cf5e6f`.
- `I12::envoy-ext-proc::NEED-response-streaming` — `3cad230cbc39d7ace8536725d2962e42ae795b21188d70197567d4b910dcdfca`.
- `I12::envoy-ext-proc::NEED-client-response-bytes` — `dc4f1e67fb9a4ee82929812f6497963146008bf7bb39d3bc3351ddef490b50b5`.
- `I12::envoy-ext-proc::NEED-client-exit-signal` — `4de6cf4389348e62bd5cafbb24cebedd127bf4b2bd7895f229bcb13030332488`.

Not reapproved because the visible Authorization trailers are not stream-bound and the remote gRPC status remains unknown:

- `I12::envoy-ext-authz-request::NEED-complete-sample`.
- `I12::envoy-ext-authz-request::NEED-request-multiple-chunks`.
- `I12::envoy-ext-authz-request::NEED-client-response-bytes`.
- `I12::envoy-ext-authz-response-companion::NEED-allow`.

This task’s current acceptance state has 7 resolved and 118 open original oracles. The central baseline inventory remains unchanged.

Every new proposal has an explicit original-ID/fixture binding and physical source references. Associated retakes remain unqualified until every case-specific proof is reviewed; even a matching HTTP result does not automatically resolve an original oracle.

Postcommit probes synchronize deliberate backend EOF with an actual client receipt of the first entity byte. ext_proc and companion each deliver HTTP 200/32 body bytes before incomplete chunk framing. The client exits with an error; the first physical Common error remains protocol_error with original/visible status 200 and commitment set. Free/cleanup are observed; successful runtime_finish is not invented.

The complete bilingual check exits 2 because 22 unchanged links target this worktree’s uninitialized Framework gitlink. Parent language contracts and every new document link pass the scoped API check. This is not a global bilingual PASS. All 2,105 build sources were independently reconstructed from the archived Parent and capture overlays; case/route/Parent substitution and the outer timeout path have dedicated negative controls.


## Supplemental host probes at afaf

The v3 supplement binds base `afaf6305bd55646073c3b40632b52fc4e5edf714` to `current-base-afaf-native-v3` and `current-base-afaf-host-v2`. All 16 native preparation steps, including native/CGo/Go, race and vet, pass. The engine build uses Go 1.27.2 for driver, compiler and linker; the host probe reports Go 1.27.3 separately as an environment value. ModSecurity 3.0.14, Envoy 1.39.1, loaded images and all 2,196 build sources are physically bound. The current capture registry passes with 155 objects/10 profiles. Historical a622 and e4 supplements retain their own revisions and failed attempts. The three afaf-host-v1 admission failures retain exit 77 and unknown host execution. The delivery Base later advanced through a normal merge to `76672071c3f7665dfde3340bef9e64271d6f6e70`. Its inherited delta changes only two Parent test fixtures and their own EN/DE Change Record; Envoy, runtime, capture, dependency and build inputs remain unchanged. No new Envoy host execution, original-ID acceptance or oracle progress is assigned to that head.

All three afaf-host-v2 runners exit 0. Each route observes target request/response 95/96 bytes, neighbor request/response 6/7 bytes and exactly two backend requests. Physical native event logs prove Finish, Free and cleanup; UID/GID 65534, zero capabilities, NoNewPrivs 1 and namespace/listener boundaries remain intact. No task processes or mount leaks survive cleanup. These measurements add `new_lifecycle_pass=0`, no original ID and no oracle progress. The historical 86 host measurements, 37 retakes for 33 IDs and 7 lifecycle PASS/118 open original oracles remain unchanged.

- **`envoy-ext-proc`:** P1–P4, request callbacks `64/31/0-EOS` and response callbacks `64/32/0-EOS` are observed with real libModSecurity. Target and sequential neighbor have distinct native scopes; Finish, logging, Free and Common cleanup are each observed twice. Both Process streams end in local reset 2; their remote gRPC status remains unknown and successful completion false. The `text/plain; charset=utf-8` header does not establish independent native MIME/charset selection. This allow probe exercises neither Reject/ProcessPartial nor cancellation or deliberate missing/repeated callbacks.
- **`envoy-ext-authz-request`:** Client writes `32/32/31`; the native engine receives one complete 95-byte sample with EOS under `max_request_bytes=4096`, `allow_partial_message=false`. This is a host buffer limit. The probe triggers no host reject, native body-limit decision, rule intervention or technical runtime failure. Two visible status-0 trailers are not stream-bound; Authorization status remains unknown and successful completion false.
- **`envoy-ext-authz-response-companion`:** Two separate allocation scopes bind lease issue, accepted claim and P3/P4. Wire equality of the lease token is not proven. P3 precedes commit; response callbacks `64/32/0-EOS` and P4 follow it, and the first client entity byte precedes P4. P4 Strict is therefore not claimed supported or accepted. Process ends in local reset 2 and attributed remote gRPC statuses are absent. Missing/expired leases, observer abort and the first technical failure cause need their own qualified cases.

| Route | Client | Authorization grpc-status | Successful completion |
| --- | --- | --- | --- |
| envoy-ext-proc | target | unknown | false |
| envoy-ext-proc | neighbor | unknown | false |
| envoy-ext-authz-request | target | unknown | false |
| envoy-ext-authz-request | neighbor | unknown | false |
| envoy-ext-authz-response-companion | target | unknown | false |
| envoy-ext-authz-response-companion | neighbor | unknown | false |

## Physical references

- `baseline`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/baseline-envoy-reconciliation.json` — SHA256 `e5bc09638b139351aa9816df79faffcb8923117f1bd74ca59fdd7b21021ac469`.
- `native`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/native-v2/native-build/receipt.json` — SHA256 `fd429f2d49a76c71233eb581992a24fc81ac47b1ca8662fd3892be046eee16b0`.
- `validation`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/ci/final-envoy-controls-257-sonar-v3.json` — SHA256 `3edfe536ae640081fdffb6211ae00a1019aa49a5a91728a8b2e33c98f1659803`.
- `I12__envoy-ext-proc__NEED-request-streaming`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/root-approved-originals-v14/I12__envoy-ext-proc__NEED-request-streaming.json` — SHA256 `7964c0c6075770e516a455c79fad486ceef0bc8f132398777402b06179cf5e6f`.
- `I12__envoy-ext-proc__NEED-response-streaming`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/root-approved-originals-v14/I12__envoy-ext-proc__NEED-response-streaming.json` — SHA256 `3cad230cbc39d7ace8536725d2962e42ae795b21188d70197567d4b910dcdfca`.
- `I12__envoy-ext-proc__NEED-client-response-bytes`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/root-approved-originals-v14/I12__envoy-ext-proc__NEED-client-response-bytes.json` — SHA256 `dc4f1e67fb9a4ee82929812f6497963146008bf7bb39d3bc3351ddef490b50b5`.
- `I12__envoy-ext-proc__NEED-client-exit-signal`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/root-approved-originals-v14/I12__envoy-ext-proc__NEED-client-exit-signal.json` — SHA256 `4de6cf4389348e62bd5cafbb24cebedd127bf4b2bd7895f229bcb13030332488`.
- `oracles-ext-proc`: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-envoy-410-20261015/ci/runtime/lifecycle/i12/envoy/oracles-ext-proc.json` — SHA256 `a25fe9a5808df508a5182cedf343166ccafebefabaeaa7d7898a4eb6d2c61a2f`.
- `oracles-authz-request`: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-envoy-410-20261015/ci/runtime/lifecycle/i12/envoy/oracles-authz-request.json` — SHA256 `00299799b27918783dff71e44720059d23bc539570f71c4e37a4b6d91ac08ddf`.
- `oracles-companion`: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-envoy-410-20261015/ci/runtime/lifecycle/i12/envoy/oracles-companion.json` — SHA256 `fe98c20ebd63ad455a34e2a65dbced229d43cab63755d70e743a18abdaf9f1b3`.
- `oracles-companion-allow-retake`: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-envoy-410-20261015/ci/runtime/lifecycle/i12/envoy/oracles-companion-allow-retake.json` — SHA256 `6a00134155aea20f146cf7be2fe7c37b4517a378529af609e8b1fc7af9205d63`.
- `review-release-host-v2`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-v2.json` — SHA256 `c07e6c0825d15b1d80adf88519e3e4539d2378e7c0adf811ad29940771962155`.
- `review-release-host-v3`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-v3.json` — SHA256 `5379f6fd2129ac7c411f89fcfa7487bf16db826e15dbc397523144f97f657ce7`.
- `review-release-host-faults-v2`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-faults-v2.json` — SHA256 `433d338c4286a03c3f0d2b8618e3b719715685695939adc252a0eba1b5ab5406`.
- `review-release-host-final`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-final.json` — SHA256 `36f9d21db12bca52562c53b0654cedfaefc56096f8f2410b6940d442f3cc07f7`.
- `review-release-host-postcommit`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-postcommit.json` — SHA256 `6add24def432637fb8d701fe98f8b2890d473992a38939a2f27bdb21d672f27e`.
- `review-release-host-originals`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-release-host-originals.json` — SHA256 `2de58afa0962ac01258a7fd1a9fac9553eb97f54543c0e5d303668477101d7fd`.
- `review-companion-retake-v1`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-companion-retake-v1.json` — SHA256 `8e343b65be316565c222163d95c812a337b3e3de66d2544bdb8520bbffe79869`.
- `review-fault-host-v2`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/review-fault-host-v2.json` — SHA256 `862c108d07b69ccfdaa6c8dd51493a03361c8ad1f3c85b6d4a704b56c077dc3e`.
- `current_base_supplement`: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/current-base-afaf-evidence-v3-sonar.json` — SHA256 `cefcd787b5790012f1bbc03c7c99b880b9318db39e8b129c387072c6fb680a11`.

References reside in task-owned external storage; the PR contains source and sanitized metadata, not binaries, caches, private keys or raw payloads.
