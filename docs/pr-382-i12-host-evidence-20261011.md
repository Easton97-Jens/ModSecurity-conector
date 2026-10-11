# PR #382: I12 host evidence, 2026-10-11

**Language:** English | [Deutsch](pr-382-i12-host-evidence-20261011.de.md)

**I12 NOT COMPLETE.** No complete required route leg has PASS. Actual Apache
requests demonstrate useful bounded behavior and five physical-sink failures;
The historical focused Traefik Native/UDS Allow demonstrates a physical
`protocol_error`; the later full run has normal Allow records and stays BLOCKED
for missing evidence, without a global regression claim. Host startup,
HTTP 200, a successful driver, or compiled checks cannot close the required
client/backend/transport/log/cleanup matrix. This manually maintained report
describes the tested source tuple below, not a later PR head or delivery commit.

## Source and run binding

| Field | Observed value |
| --- | --- |
| Run ID | `20261011T063350Z-0df51024008f-i12` |
| Tested Parent / starting HEAD | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |
| Starting branch | `work/pr382-i12-host-evidence-20261011` |
| Starting `origin/master` / merge base | `3019722fbda40dc281b861c1cc38085be2f430a0` / `3019722fbda40dc281b861c1cc38085be2f430a0` |
| Framework gitlink / actual HEAD | `99a7985c1be92a2297b1b59208f64df6768f2cbf` / `99a7985c1be92a2297b1b59208f64df6768f2cbf` |
| MRTS gitlink / actual HEAD | `8a6bb546c4c81d8ffc7be801dceac60c6925685f` / `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |
| Starting dirty state | Task worktree, Framework and MRTS clean; unrelated main-checkout modification preserved |
| libModSecurity | Installed 3.0.14; `/usr/lib/x86_64-linux-gnu/libmodsecurity.so.3.0.14` |
| Library SHA256 | `32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407` |
| Library source commit | Unavailable; binary/package identity is recorded, no invented source SHA |
| Platform | Ubuntu 26.04.1 LTS; kernel 7.0.0-38-generic; x86_64; 8 logical CPUs |
| Toolchain | GCC/G++ 15.2.0; Make 4.4.1; Go 1.27.2; curl 8.18.0 |
| Python | Parent, Apache and native fixture wrappers 3.14.7; Envoy/Traefik native helpers explicitly use `/usr/bin/python3` 3.14.4 |
| Host prerequisites | Apache 2.4.66; NGINX 1.31.6; HAProxy 3.2.25; Envoy 1.39.1; Traefik 3.7.13; lighttpd 1.4.85 stock and patched |

Initial `metadata.json`, `pre-execution.json` and `matrix.initial.json` were
retained before host execution. Their initial absent-host inventory remains
historical; later build receipts record provisioning without rewriting it.
Per-attempt snapshots, actual config hashes, binary/module identities, direct
client completions, original physical logs and cleanup receipts bind individual
observations. Unobserved fields stay null. Framework/MRTS source and gitlinks
were not changed. Successful pinned builds are prerequisites, not I12 PASS.


PR #382 advanced later to `498653c2a193d34b7b25b2903b1e4db1c45e7f73`. The inspected
delta is documentation plus a B09 test change, with no product change. This
report keeps the original tested `0df51024008fc84f0a6820f3b011055b69c3a3e2`
binding and does not inherit PASS onto that later head.

## Isolation and historical NGINX scope

Default sandbox namespace and UID-change probes failed. Outside-sandbox
immutable probes succeeded, but custom root-master handoff remained rejected
under the installed `bwrap//&unpriv_bwrap` AppArmor boundary. No AppArmor policy,
capability boundary or validation was weakened. Admitted fixtures use actual
UID/GID 65534 with zero effective capabilities, official bwrap, private
user/network/PID namespaces, loopback/private UDS, read-only root/source/Framework/artifact mounts
and task-private writable roots. Root, source, Framework and staged artifacts are
read-only; this does not claim every host mount was read-only. Earlier attempts
retained an inaccessible root-owned mode0700 writable sysfs target limitation;
the fresh guard masks sysfs. A namespace-relative UID 0 mapping does not
prove host root identity. Current NGINX root/nobody evidence remains BLOCKED by
the required identity handoff; a compiled NGINX/module does not replace it.

Historical [R17](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396#issuecomment-6101794434)
had 97/97 selected Required-PASS for Parent
`2f02370b07149265841411894f1a2cf7f1e978ff`, Framework
`9f41f80db7bf53b57429457bce0dda675d2ec5d7` and the same MRTS. Its exact generic
Strict curl exit 52 remains historical. The inspected delta contains no native
NGINX/Common product, build or lifecycle change; CRS pins and Framework
maintenance differ. This comparison does not transfer runtime PASS to the
tested tuple here. H2/H3, CRS, Off, production and Protected Exact-Head are not
proved by the historical H1 result.

## Required route legs

Ten logical routes expand to thirteen required legs because SPOP, ext_authz and
forwardAuth each require separate request and response-companion evidence.
The fourteenth lighttpd Stock-native diagnostic control is advisory and cannot
replace the traffic-owning Stock sidecar. Complete-leg PASS count: **0**.
The selected broader-run receipts have been reconciled; their driver exits
do not close missing required observations or change these acceptance statuses.

| Logical route | Required leg | Acceptance state / remaining evidence |
| --- | --- | --- |
| Apache native/direct | `apache-native` | FAIL: five physical-sink cases; seven full MIME/EOS contracts not executed; further required cases remain |
| NGINX native/direct | `nginx-native` | BLOCKED: current root-master/nobody-worker admission; R17 retained separately |
| HAProxy HTX direct | `haproxy-native-htx` | BLOCKED: eight real cases; native stderr distinct from helper JSONL; direct client/native-sink/cleanup gaps |
| HAProxy SPOE/SPOP + companion | `haproxy-spop-request` | BLOCKED: separate request evidence and complete physical-sink/required-case coverage |
| HAProxy SPOE/SPOP + companion | `haproxy-spop-htx-response-companion` | BLOCKED: separate companion correlation, retained transaction and host action evidence |
| Envoy ext_proc direct | `envoy-ext-proc` | BLOCKED: real HTTP/gRPC observations exist; independent backend, transport, cleanup and required-case proof incomplete |
| Envoy ext_authz + companion | `envoy-ext-authz-request` | BLOCKED: real Allow/Block observations exist; exact request/backend and full required-case proof incomplete |
| Envoy ext_authz + companion | `envoy-ext-authz-response-companion` | BLOCKED: companion events do not by themselves prove downstream action, cleanup or physical-sink fault handling |
| Traefik Native/UDS | `traefik-native-uds` | FAIL: historical focused physical protocol_error remains selected; latest full run alone is BLOCKED with normal Allow/P1/P2/P3/P4 records |
| Traefik forwardAuth + companion | `traefik-forwardauth-request` | BLOCKED: real focused Allow exists; direct client completion and complete required-case evidence incomplete |
| Traefik forwardAuth + companion | `traefik-forwardauth-response-companion` | BLOCKED: response companion requires independent action/log/cleanup and required-case proof |
| lighttpd stock/sidecar | `lighttpd-stock-sidecar` | BLOCKED: full06 raw retained; exact empty engine actual_action enum mismatch before native deny451; direct deny client proof absent; four later cases NOT_EXECUTED |
| lighttpd patched/native | `lighttpd-patched-native` | BLOCKED: scoped staticfile Allow only; full03 trusted-directory reject77; Strict abort unsupported |
| Advisory stock control | `lighttpd-stock-native-control` | NOT_EXECUTED: not a substitute for required Stock sidecar or native body hooks |


## Representative E2E receipt matrix

One retained representative observation per leg is shown below; this is not full case coverage. `null` means unobserved or not yet reconciled. Client means actual HTTP / waited exit / measured bytes. Driver exits and projected diagnostics are not substituted. Historical focused faults remain separately scoped.

| Test-ID | Route leg | Host | Mode | Case / attempt | Client HTTP/exit/bytes | Backend requests | Transport | Physical log | Cleanup | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `E2E-APACHE-INVALID-EVENT-PATH` | `apache-native` | `Apache 2.4.66` | `native-httpd-module` | `invalid-event-path` | `200/0/10` | `1` | `http_completed` | `main physical event absent; sink warning` | `PASS` | `FAIL` |
| null | `nginx-native` | `NGINX 1.31.6` | `root/nobody H1` | `identity admission` | null | null | null | null | null | `BLOCKED` |
| null | `haproxy-native-htx` | `HAProxy 3.2.25` | `native HTX` | `phase1_403; full02` | `403/null/93` | `0` | null | `actual native stderr deny; canonical JSONL is helper projection` | `namespace reaped; transaction null` | `BLOCKED` |
| null | `haproxy-spop-request` | `HAProxy 3.2.25` | `SPOE/SPOP request` | `p4-safe; full03` | `200/null/23` | null | null | `native request decision retained` | `namespace reaped; transaction null` | `BLOCKED` |
| null | `haproxy-spop-htx-response-companion` | `HAProxy 3.2.25` | `HTX response companion` | `missing-correlation; full03` | `503/null/107` | null | null | `actual native fail-closed response claim503` | `namespace reaped; transaction null` | `BLOCKED` |
| `E2E-envoy-ext-proc-direct-envoy-ext-proc-allow-1` | `envoy-ext-proc` | `Envoy 1.39.1` | `common_libmodsecurity_nonpromoted` | `Allow; envoy-ext-proc/unpriv-runtime-04` | `200/0/28` | `1` | null | `matching native records present` | null | `BLOCKED` |
| `E2E-envoy-ext-authz-request-envoy-allow-1` | `envoy-ext-authz-request` | `Envoy 1.39.1` | `ext_authz` | `Allow; envoy-ext-authz/unpriv-runtime-02` | `200/0/28` | null | null | `physical sink empty` | null | `BLOCKED` |
| `E2E-envoy-ext-authz-response-companion-envoy-allow-1` | `envoy-ext-authz-response-companion` | `Envoy 1.39.1` | `response companion` | `Allow; envoy-ext-authz/unpriv-runtime-02` | `200/0/28` | null | null | `physical sink empty` | null | `BLOCKED` |
| `E2E-traefik-native-uds-direct-traefik-native-p1-allow` | `traefik-native-uds` | `Traefik 3.7.13` | `Native/UDS` | `Allow; traefik-native-uds/unpriv-runtime-02` | `200/null/54` | null | null | `matching native records present` | null | `BLOCKED` |
| `E2E-traefik-forwardauth-request-traefik-forwardauth-allow` | `traefik-forwardauth-request` | `Traefik 3.7.13` | `forwardAuth` | `Allow; traefik-forwardauth/unpriv-runtime-02` | `200/null/null` | null | null | `physical sink empty` | null | `BLOCKED` |
| `E2E-traefik-forwardauth-response-companion-traefik-forwardauth-allow` | `traefik-forwardauth-response-companion` | `Traefik 3.7.13` | `response companion` | `Allow; traefik-forwardauth/unpriv-runtime-02` | `200/null/null` | null | null | `physical sink empty` | null | `BLOCKED` |
| null | `lighttpd-stock-sidecar` | `lighttpd 1.4.85` | `stock traffic-owning sidecar` | `p1_deny; full06` | `null/null/null` | `0 for /p1-block in actual access log` | null | `native engine actual_action empty then same-TX request_blocked deny451/rule9821001` | `namespace reaped; direct transaction null` | `BLOCKED` |
| null | `lighttpd-patched-native` | `lighttpd 1.4.85` | `patched borrowed hooks` | `staticfile Allow; focus02` | `200/0/32` | null | null | `native host startup log; events empty` | `namespace reaped; transaction null` | `BLOCKED` |
| null | `lighttpd-stock-native-control` | `lighttpd 1.4.85` | `advisory diagnostic control` | `not selected` | null | null | null | null | null | `NOT_EXECUTED` |

## Latest Envoy and Traefik raw review

The latest closed raw inventory contains 27 cases: ext_proc attempt04 has 10,
ext_authz attempt02 has 5, Native/UDS attempt02 has 7 and forwardAuth attempt02
has 5. Strict evidence counts are **0 PASS, 0 FAIL, 27 BLOCKED**. The physical
Allow `protocol_error` from the earlier Native/UDS focus remains a separate
historical FAIL; latest Native/UDS Allow has normal events. Neither erases the
other or establishes a global product regression.

ext_proc attempt03 had a fixture rule/marker mismatch; matching
`common/rules/modsecurity_p1_p4_vectors.conf` in attempt04 completed driver exit
0 under `common_libmodsecurity_nonpromoted`, with actual HTTP 200/403/413/302.
Envoy has direct waited client exit 0; many actual byte counts, explicit client
transport outcomes and independent per-case cleanup remain missing. Native/UDS
records actual 200/403/429, Safe P4 55 bytes/`completed`, and follow-up 200, but
direct client exits/backend request counts/cleanup are still null. forwardAuth
has real request Block and response P3/Safe P4 events with the same independent
proof gaps. Request and response halves are not duplicated as separate PASS.

## Latest HAProxy and lighttpd native review

The retained `native-runtime-fixtures/reviews/final-native-routes-review.json`
contains 262 raw-file hash references. Its strict route statuses remain BLOCKED;
scoped host behavior and generated harness PASS do not become full I12 PASS.

HAProxy HTX full02 exercises eight actual cases: Allow, P1 403/429, empty P2 EOS,
P2 deny, P3 deny, empty P4 EOS and synchronized Safe P4. Native deny stderr and
Safe `log_only` coexist with real client 200/403/429 and measured bodies. The
first client read is 1 byte, upstream first chunk 17 bytes; the barrier supports
ordering without actual first-byte/EOS timestamps. The Safe barrier's backend
count is null, because a helper literal1 is not the raw request count. The
canonical JSONL is a helper projection, not the native physical canonical sink.
Direct client exits, full headers/hashes/timestamps and native transaction
cleanup remain missing.

SPOP full03 exercises six actual cases with separate request decisions and
response-companion evidence: P3 deny gives 403/93 bytes, Safe P4 200/23 bytes,
missing correlation 503/107 bytes, plus client cancel, TTL expiry and connection
reuse. The response native log actually records P4 `log_only`, correlation
fail-closed503 and postcommit TTL failure. Per-case waited exits/EOS timestamps,
correlated backend counts and native companion P3/EOS/cleanup sinks are absent.
The global backend log has seven arrivals but cannot assign repeated route names
to individual transactions. Namespace driver/owned children are reaped; this
is not per-transaction native cleanup. Companion assessment remains separate.

Patched lighttpd focus02 corrects the earlier fixture's missing staticfile module:
actual curl0/HTTP200/32 bytes establishes scoped staticfile Allow startup, with
empty native events. Full03 exits77 before host traffic because the mandatory
nested namespace trusted-directory guard rejects `/`. Its failing ownership/mode
tuple was not retained, so the report does not invent one. Strict client abort
capability remains unsupported.

Stock lighttpd full06 preserves 16 raw files with verified SHA256 ledger, no
skipped files and no snapshot error. Actual backend access logs retain only the
two Allow GETs (200/20 bytes and 200/0); no `/p1-block` request reaches that
backend. The retained P1 `engine_decision` row has `actual_action=""` before host
action is observed. The harness's enum validator excludes this empty value and
exits77. Row2 for the same transaction is genuine `request_blocked`,
`actual_action=deny`, HTTP451, `transport_result=http_status`, Rule9821001, with
correlated sequence/hash chain. This precise native-event/validator contract
mismatch does not prove a product regression or independent client enforcement
failure: actual deny client headers/body/exit/EOS remain null. P2 deny, P2 body
limit, P3 deny and Safe P4 rate limit remain NOT_EXECUTED. Producer snapshots
and namespace cleanup are distinct from missing direct client/transaction proof.
Historical full05 raw-file loss is retained separately; full06 resolves that
retention gap without relaxing validation or rewriting attestations.

## Apache observed cases and physical-sink failures

The full fixture has 19 cases: 16 bounded observations PASS and three physical
sink FAIL. Seven bounded MIME/EOS observations lack the full required contract
and remain NOT_EXECUTED for acceptance. Two additional genuine physical sink faults
are FAIL. The closed Apache inventory of 21 distinct cases therefore contains
**9 PASS, 5 FAIL, 7 NOT_EXECUTED** under the full-contract oracle. This is not a
complete all-route or even complete Apache required-case inventory.

| Case | Client HTTP / exit / bytes | Backend requests | Full-contract status |
| --- | --- | --- | --- |
| `E2E-APACHE-ALLOW` | 200 / 0 / 10 | 1 | PASS |
| `E2E-APACHE-P1-DENY` | 403 / 0 / 239 | 0 | PASS |
| `E2E-APACHE-P2-DENY` | 403 / 0 / 239 | 0 | PASS |
| `E2E-APACHE-P3-DENY` | 403 / 0 / 239 | 1 | PASS |
| `E2E-APACHE-P3-REDIRECT` | 302 / 0 / 256 | 1 | PASS |
| `E2E-APACHE-P4-SAFE-LATE` | 200 / 0 / 33 | 1 | PASS |
| `E2E-APACHE-P4-STRICT-LATE` | 200 / 18 / 33 | 1 | PASS |
| `E2E-APACHE-TECHNICAL-PRECOMMIT` | 500 / 0 / 571 | 0 | PASS |
| `E2E-APACHE-TECHNICAL-POSTCOMMIT` | 200 / 18 / 10 | 1 | PASS |
| `E2E-APACHE-MIME-SCOPEOUT` | 200 / 0 / 33 | 1 | NOT_EXECUTED |
| `E2E-APACHE-MISSING-CONTENT-TYPE` | 200 / 0 / 10 | 1 | NOT_EXECUTED |
| `E2E-APACHE-MISSING-CHARSET` | 200 / 0 / 10 | 1 | NOT_EXECUTED |
| `E2E-APACHE-WITH-CHARSET` | 200 / 0 / 10 | 1 | NOT_EXECUTED |
| `E2E-APACHE-EMPTY-EOS` | 200 / 0 / 0 | 1 | NOT_EXECUTED |
| `E2E-APACHE-ONE-EOS` | 200 / 0 / 10 | 1 | NOT_EXECUTED |
| `E2E-APACHE-MULTI-EOS` | 200 / 0 / 30 | 1 | NOT_EXECUTED |
| `E2E-APACHE-INVALID-EVENT-PATH` | 200 / 0 / 10 | 1 | FAIL |
| `E2E-APACHE-UNSAFE-DEVFULL` | 200 / 0 / 10 | 1 | FAIL |
| `E2E-APACHE-UNWRITABLE-EVENT-SINK` | 200 / 0 / 10 | 1 | FAIL |
| `E2E-APACHE-SINK-CLOSED-DESCRIPTOR` | 200 / 0 / 10 | 1 | FAIL |
| `E2E-APACHE-SINK-PHYSICAL-ENOSPC` | 200 / 0 / 10 | 1 | FAIL |

Actual traces bind first bytes before backend EOS. Safe P4 returns all 33 bytes
and native `log_only`. Strict P4 receives 33 bytes then curl exit 18 for incomplete
framing with native committed abort; no blanket nonzero=PASS rule is used.
Technical postcommit receives the first 10 bytes before the second upstream
chunk, then curl 18 and `invalid_engine_response`. Precommit returns 500 without
backend access. Follow-up requests recover. Worker UID65534/CapEff0, closed
host listeners, absent host PIDs, backend listener closure/stopped thread and
private-runner reaping are independently observed rather than inferred from
driver exit. Native empty timestamps and zero sequence/hash fields are retained
without synthetic replacements.

Unsafe target rejection does not provide checked host propagation: invalid
path, `/dev/full` and unwritable sink still return 200 and reach the backend.
Additional scoped faults actually reach APR: closed descriptor returns APR 9
(and close failure); a validated event FD redirected to `/dev/full` returns APR
28. Each main physical log is empty, UID65534, mode0600, while the client gets
200 and the backend receives one request. Recovery produces three genuine
physical records, reuses keepalive and cleans up. These two injections prove
the observed EBADF/ENOSPC paths, not natural filesystem exhaustion or every
concurrent descriptor-reuse schedule. There is no APR flush claim because the
writer is unbuffered; missing main physical `host_action` stays null.


## Apache PASS identity ledger

The following nine PASS receipts retain exact `result_record_sha256`, effective config SHA256 and original physical log references. Paths are relative to the private run root; they are not public downloads. Physical artifact hashes are retained in `apache/full-review.json`.

| Test-ID | `result_record_sha256` | Config SHA256 | Original physical event log |
| --- | --- | --- | --- |
| `E2E-APACHE-ALLOW` | `fa77c550e02ac22c8ceca3e4bca738963718cb664bb6d6e893ada8621852f11d` | `ec365b3a8e52fd41c1a82d46e85624d87d571408bdfeafec2ee377697afd5e9a` | `apache/unpriv-runtime-03/results/allow/events.jsonl` |
| `E2E-APACHE-P1-DENY` | `f1e8ee62340d7c43ac2b3e8654160d95826c469b54124077aa51a157b5802020` | `b5505fac254fc66fa525b6e3c855a1123785466c3166a36f80ffa9526e651e27` | `apache/unpriv-runtime-03/results/p1-deny/events.jsonl` |
| `E2E-APACHE-P2-DENY` | `f146eaf8aabd4dffe1d75bf5d8b13feb9e5555b3434eb691aa82ba38115b6bb8` | `8f6e0cb987dc50f1e847655d11376f92a5c0c19b1d5d5d060225a141c68fc10f` | `apache/unpriv-runtime-03/results/p2-deny/events.jsonl` |
| `E2E-APACHE-P3-DENY` | `32dbcfc2bb4fc1ecee91000fea9462b0dc53d7e369e51c6ad84952b42fbf8745` | `93cf68afd5e045925be96c65bbcf68f05bde6e83bcd846236b28ca087f6ccfbb` | `apache/unpriv-runtime-03/results/p3-deny/events.jsonl` |
| `E2E-APACHE-P3-REDIRECT` | `bf74dc9d19c4593cb1de752ead80cb6b3a775080bb0b6b41165e427d65d787ce` | `ce6e76e2b5e4f13eeeefc1e255c3e4ce1ae77fe63abc284235e88f52ccfd38fe` | `apache/unpriv-runtime-03/results/p3-redirect/events.jsonl` |
| `E2E-APACHE-P4-SAFE-LATE` | `31c8c3a5d4e6c1b0db19ccb499ba2baedb971036f7625bdbecbaaacce833c7fe` | `dbe7ab23a41fdce90cfccbf825aea7b0f7e13b0b81ec5e5d318ef2fbbb0e5b8a` | `apache/unpriv-runtime-03/results/p4-safe-late/events.jsonl` |
| `E2E-APACHE-P4-STRICT-LATE` | `5f60821b3ae4b7d30d99d23471b04a82d909ff5725b662eda1bbc8c332ce0a58` | `07a187dba67dd9b2d0e36b41d223cdc861f17497d961aeec425e033f52f866aa` | `apache/unpriv-runtime-03/results/p4-strict-late/events.jsonl` |
| `E2E-APACHE-TECHNICAL-PRECOMMIT` | `5c7e9392ca0d753e34a9fa2acb235ce04c9e0da8c0f75b2e195e87b7b6bb16e5` | `26bcd6fa5d15b5521fb1676ca8095ba0d87167559de1dfa1fa1be68dd9fba9b6` | `apache/unpriv-runtime-03/results/technical-precommit/events.jsonl` |
| `E2E-APACHE-TECHNICAL-POSTCOMMIT` | `73e9226091da1293e4f05bffc4d4e95476e1bd07c51663ab0f8ed7af52ed05c0` | `7e9108a117bc1da1d9218a055c22a28a46e8121d59c0427ac944d9b7450e6c19` | `apache/unpriv-runtime-03/results/technical-postcommit/events.jsonl` |

## Required remaining cases

I12 remains unchecked in the [checklist](pr-382-checklist.md) and current-run
observations remain separate from the historical source inventory in the
[remaining-work matrix](pr-382-i09-i12-rest-matrix.md). Apache's void physical
writer and SPOP's unchecked `fputs`/`fflush` propagation remain separate I11
implementation gaps. This task supplies evidence and does not fix product code.

| Area | Required remaining proof |
| --- | --- |
| Start / Allow / Block | Exact host/module/engine/config identity; deterministic rule IDs; actual client completion and backend exclusion where required; independent companion halves |
| Technical pre/postcommit | Real engine/adapter fault, first typed cause, actual precommit response or supported postcommit transport action; no successful EOS invented |
| Body / EOS / MIME | ProcessPartial/Reject and cumulative limits; declared versus actually measured bytes; scope-in/out, missing Content-Type, charset/CSV; empty/single/multiple chunks and exactly-once EOS |
| Physical sink | Original file/FD ownership, mode, IDs, action/cause, ordering and actual hashes; serialization/open/write/short-write/close failures and bounded duplicate behavior |
| Follow-up / neighbor | Genuine same-connection reuse where supported, neighboring stream health and scoped failure; a new connection alone cannot prove reuse |
| Cleanup | Listener/socket closure, absent owned host/backend/service PIDs, waited child statuses and private namespace reaping; retain failed setups |

Transport short-write/EAGAIN, UDS/gRPC failures and successful diagnostic
projections do not prove physical sink failure handling. Soft budget detection
after engine return does not prove hard cancellation of a hung engine.

## Executed Parent verification

The retained `verification/results.json` contains exact argv, cwd, durations,
exits and logs; `workflow-inputs.json` binds all 32 current workflow inputs.
Commands use RTK and explicitly installed `/usr/local/bin/python3` 3.14.7.
No packages, toolchains or dependency files were installed or changed.

| Check | Actual outcome / limit |
| --- | --- |
| Python interpreter contract | Exit 1: required `python` alias absent despite matching `python3` 3.14.7 |
| `make check-ci-security-contract` | Exit 2: 177 tests, three import errors due missing PyYAML, six skips; subsequent lock checks not reached |
| `make test-hostruntime-preflight` | Exit 0; 27 unit tests; no host-I/O proof |
| Native event/sink/lifecycle unittest batch | Exit 1; 74 tests, 15 assertion/subtest failures, two errors; 69 explicit successful methods coexist with failure |
| `make check-bounded-smoke-runtime-contract` | Exit 2; 119 tests, four assertion/subtest failures, 12 errors |
| `make check-common-helpers-c17` | Exit 0; compiled Common checks only |
| actionlint 1.7.12 | Exit 0 on all 32 workflows plus two permission fixtures; local source-built binary provenance retained |
| zizmor 1.29.0 `--offline` | Exit 0 on workflows; unsafe controls each exit 14 as expected; safe controls exit 0 |
| RTK verification | `rtk gain` exit 0 |
| Preliminary documentation checks | Failed on the absent worktree Framework and subsequently unavailable relative Git metadata; the original failed attempts remain retained. |
| Final documentation / Change Record / link checks | `make check-bilingual-docs`, `make check-doc-links`, native Change Record check and `git diff --check`: exit 0 in `document-mount-checks-02/results.json`. The private static-check mount namespace exposes the actual Framework/Git metadata read-only, with private read-only Git-path aliases; original repositories and validators are unchanged. |

Failed native seams include obsolete direct-return regex expectations, a NGINX
extracted Off branch that omits the preceding technical-failure path, and an
Envoy substring assertion that omits its called NULL guard. These are identified
test-contract drift, not independent proof of a live bypass. Broader checks
also encounter hardcoded empty worktree Framework paths, missing PyYAML and
default-sandbox UID limitations. No trust guard was weakened or unsuccessful
execution relabelled. Local scanners do not establish hosted CI, Sonar,
Protected acceptance or release readiness.

## Final selected-inventory counts

`matrix.final.json` reconciles **79 selected records: 9 PASS, 6 FAIL, 53 BLOCKED,
11 NOT_EXECUTED**. This bounded selected inventory is not the complete required
all-route case matrix. The extra advisory Stock-native diagnostic control is
NOT_EXECUTED and excluded from 79. Separate companion records may share HTTP
observations without proving the other leg. Required whole-leg counts across
13 legs are **0 PASS, 2 FAIL, 11 BLOCKED**: Apache and retained historical focused
Native/UDS failure remain FAIL; the later Native/UDS full cases remain BLOCKED.

The normalized per-leg ledger under `normalized/` retains `metadata.json`,
`client.json`, `backend.json`, `host.json`, `cleanup.json` and `result.json` for
all thirteen required legs. Original observations remain intact and no synthetic
`events.jsonl` substitutes a physical sink. Independent artifact verification
matches **791 references: 529 Apache + 262 native**. Identity verification does
not convert missing or failed behavior into PASS.

## Retention, documentation diff and delivery

Raw evidence is retained locally under
`/var/tmp/codex/ModSecurity-conector/runs/e2e/20261011T063350Z-0df51024008f-i12`.
This path is not a downloadable GitHub artifact. Useful relative receipts are
`metadata.json`, `pre-execution.json`, `matrix.initial.json`, `matrix.final.json`, `normalized/`, Apache
`full-review.json`/`sink-review.json`, `prerequisites/open-hosts/final-review.json`,
`native-runtime-fixtures/reviews/final-native-routes-review.json`,
per-route isolation/runtime roots and `verification/results.json`/`logs/`.
Receipts contain actual artifact/config hashes; a checksum proves identity,
not semantic PASS. Failed setups and historical runs are preserved.
`SHA256SUMS` and `checksum-verification.json` bind retained regular artifacts;
non-regular exclusions are explicit in `manifest-exclusions.json`. Publication
receipts under `delivery/` are kept separately from that artifact manifest.

The checklist diff adds exact current-run binding and unchecked I12c–l;
historical I12b/R17 and all 56 source-matrix rows remain unchanged. The proposed
partition is one atomic documentation commit containing the checklist pair,
remaining-work matrix pair, this report pair and the
[Change Record pair](../reports/audits/change-records/CR-20261011-pr382-i12-host-evidence.md)
(eight files). Raw fixtures/builds/evidence and local plans stay outside it.
The user authorized a stacked Draft PR on `fix/unified-native-results-events-20260921`;
delivery/review results are recorded only after actual readback. No merge,
deployment, product correction, green CI or I12 completion is claimed.

**I12 NOT COMPLETE – remaining required host evidence:** physical-sink propagation, complete body/EOS/MIME contracts, independent companion, neighbor and cleanup receipts, and current NGINX identity admission remain open.
