# Change Record: CR-20261015-i12-envoy-host-evidence

**Language:** English | [Deutsch](CR-20261015-i12-envoy-host-evidence.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-i12-envoy-host-evidence |
| Date (UTC) | 2026-10-15 |
| Base revision | `76672071c3f7665dfde3340bef9e64271d6f6e70` |
| Historical native/host evidence source revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |
| Latest Envoy runtime-evidence source revision | `afaf6305bd55646073c3b40632b52fc4e5edf714` |

## Motivation and problem statement

The original Envoy ledger has 284 IDs across ext_proc, request authorization and the response companion. Three existing lifecycle PASS resolve only three of 125 original open oracles. Host effects must remain distinct from unit/build results and configuration-only PASS.

## Acceptance criteria

Preserve all original IDs/oracles and patched Go/x/net inputs; execute real isolated host probes and native/Go/race/vet controls; bind physical evidence and report each route separately. Full original-case acceptance remains unmet: 118 original oracles remain open after four newly qualified ext_proc original IDs; the retained central baseline remains unchanged.

## Implementation decision and rationale

Add only Envoy-specific I12 producers/tests and own EN/DE reports. Reuse the unchanged envoy capture registry and common observer in a Git-free source copy. Verify binary/source/SDK correspondence. Count started/aborted backend requests separately; preserve TCP resets and missing gRPC status. Pin the positively identified PID namespace through cleanup in the Envoy-only controller copy, with identity checks before/after open and fail-closed fallback. Preserve original controller gates and all failed attempts.

## Changed files

New Envoy-local files under `ci/runtime/lifecycle/i12/envoy/`: native preparation, original-ledger reconciliation, host fixture preparation/runner, transport classifier, physical reviewer, report producer, tests and EN/DE README. Own report pair and exact-ID JSON: `reports/testing/i12-envoy-host-evidence-20261015.*`. Parent discovery wrapper: `tests/test_i12_envoy_evidence.py`. This EN/DE Change Record pair. In the task diff against Base, shared manifest/generators, product files, other connectors, dependencies and Gitlinks are unchanged.

## Commands executed

All shell entrypoints used RTK. The exact afaf native/CGo build, full Go tests, race and vet argv/results/log hashes are retained in `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/current-base-afaf-native-v3/native-build/receipt.json`; all 16 steps exit 0. `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_i12_envoy_evidence`: 257 PASS, 0 skips; current raw logs and all 31 Python input hashes (30 Envoy sources and the Parent discovery wrapper) are bound in `ci/final-envoy-controls-257-sonar-v3.json`. Focused fault controls have 16 PASS; separate Go test-proxy controls have 10 PASS. The current capture registry verifies 155 objects/10 profiles, and the native observer controls pass 34 tests. Host commands and nonzero exits remain in each batch runs.json; they are not normalized to PASS.

## Security impact

CI remediation closes unbounded CLI/JSON file access in the Envoy evidence readers. Approved roots are checked before filesystem access; directory descriptors, O_NOFOLLOW, owner/mode checks, byte limits and stable file identity protect the read. Outputs use private, exclusive creation; Git metadata arguments require exact SHAs and fixed scope. The current complete Envoy suite has 257 PASS and 0 skips. The new reader is hash-bound in freshly reproduced, individually approved packets; old packets and raw host runs remain retained. The first CI run for head `d91891fd0e19826d6f09a426daa289dafea9f598` completed with 21 successful checks, two skipped checks and one failed scaffold-lint check. SonarCloud's Quality Gate passed, while the separate zero-new gate reported 44 maintainability annotations. Envoy-local refactors address those annotations; the current head's terminal CI result remains tracked in Draft PR417. No rule, exclusion, disposition or Quality Gate was changed.


Synthetic unit fixtures use independently scoped temporary storage so hosted
runner paths do not require this machine's capture root. Three pre-fix controls
fail when that root is absent; all 95 original portability controls pass with absent
production roots and in the normal environment. Actual capture containment and
listener/privilege checks are unchanged. Receipts: `ci-portability-before.json`,
`ci-portability-controls.json`, `final-envoy-controls-portable.json`.

No product defaults, authentication, validation, compiler warnings, listener permissions or dependency pins are weakened. Actual candidates run as UID/GID65534, capabilities0, NoNewPrivs1 in private namespaces. The namespace FD prevents inode-reuse misattribution while retaining all ownership checks. No foreign process was signalled. Generated report metadata excludes payloads, opaque leases, private keys, caches and binaries.

All 125 original oracles have individual physically validated source reviews. The 33 new concrete fixture/expectation proposals (14/10/9) remain separate from canonical resolution and lifecycle PASS. Complete build-source inventory (2,105 files), case/route/Parent binding and the bounded outer timeout with byte-exact partial logs have additional controls.

The continuation on 18 October 2026 uses only the trusted configured storage export and refuses missing configuration. All 84 previous physical review outputs, 34 fixture outputs and the normalized inventory of all 125 original oracles remain exactly equal. A negative test reproduced a refactor defect involving duplicate binary basenames; every original receipt entry is again checked individually. Receipts: `ci/resume-final-controls.json`, `ci/review-final-physical-parity.json`, `ci/owned-refactor-parity.json`.

The new companion supplement received physical validation of all 17 references before host execution and preserves original/effective/source semantics. An initial controller 77 occurred before host start because the registered 1 GiB estimate was below the unchanged 2 GiB output limit. Official registration was corrected to 3 GiB; original registration and failed attempt are retained. The actual retry ends controller 0 / client 0, without survivors or mount leaks. Native source remains explicitly `f27eb59…`; this does not qualify the advanced Parent.

## Runtime evidence

Actual Envoy1.39.1, SDK3.0.14 and Go1.27.2 loaded/built identities, client/backend wire/body hashes, P1–P4, body chunks/EOS, native logging/free, runtime/Common Finish counts, physical events and cleanup receipts reside under `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015`. Own EN/DE report and exact-ID JSON preserve every measured batch and original case. Runner exit0 is not lifecycle qualification; exit77 and unknown observations remain explicit.

86 real host measurements include 37 retakes under 33 exact original IDs. Four individual Root approvals in `root-approved-originals-v14`, after fresh reproduction of all 35 proof categories, qualify these exact ext_proc original IDs; the three previous lifecycle PASS remain preserved:

- `I12::envoy-ext-proc::NEED-request-streaming`
- `I12::envoy-ext-proc::NEED-response-streaming`
- `I12::envoy-ext-proc::NEED-client-response-bytes`
- `I12::envoy-ext-proc::NEED-client-exit-signal`

The retained baseline PASS are `I12::envoy-ext-proc::NEED-request-eos-once`, `I12::envoy-ext-authz-request::NEED-request-eos-once` and `I12::envoy-ext-authz-response-companion::NEED-lease-claim`.

The three former request-authorization approvals (`I12::envoy-ext-authz-request::NEED-complete-sample`, `I12::envoy-ext-authz-request::NEED-request-multiple-chunks`, `I12::envoy-ext-authz-request::NEED-client-response-bytes`) and the former companion approval (`I12::envoy-ext-authz-response-companion::NEED-allow`) are revoked. Visible `grpc-status:0` trailers lack a proven Authorization stream association. The strict parser therefore records remote status unknown and successful completion false; matching HTTP/native measurements do not establish the complete route contract.

The physical request trace still identifies worker 285 / CID1 / SID6459190741822168578 and host fragments 64+31=95 followed by EOS, then Authorization Check at line 275. The engine receives one complete 95-byte native sample and one EOS; multiple client writes do not imply multiple native callbacks. Raw HTTP framing and entity bytes remain independent observations. `max_request_bytes` is a host buffer boundary, not a connector WAF inspection limit. Host 413 before engine entry, native body-limit Reject/ProcessPartial, valid rule intervention and technical gRPC/runtime failure retain separate evidence obligations.

The additional companion retake proves two early captured backend requests, target 1 / neighbor 1, request 95 / response 96 and response callbacks 64+32+0/EOS. Lease claim, P1–P4, logging, RuntimeFinish, NativeFree and cleanup are physical observations; the separate request leg gains no further PASS. Observed local HTTP2 reset 2 remains separate from unknown remote gRPC status.


The exact Base head `a62296fb57263f9be18c6ac879e36e0ab2a9935c` was merged into this branch in `dfb1a07a863530a53c0006ee204319453d66a2ad`. The retained baseline and physical sources were revalidated with the current central validators; this Envoy task modified no shared validator. Historical native and host evidence remains limited to `f27eb59…`. Fresh current-Base native and host captures are separately bound below and add no original-case qualification. The fixture from `fault_scenarios.py` and separate Go test proxy were used in the real, bounded ext_proc Response-EOS fault probe `fault-host-v1`. Its runner77/controller1/client1 remains unqualified; new PASS: 0.
The probe drops only the empty Response-EOS callback and performs an actual half-close. The engine API and unambiguously correlated Envoy target stream report gRPC status14. The target client receives HTTP200 with a prefix of 96 body bytes in 64+32 without a terminating zero chunk. P1–P3 are observed, P4=0; the `runtime_finish` attempt has result0 and is not counted as successful Finish. Logging/free/cleanup are one each. The healthy neighbor reaches P1–P4/Finish once each. No survivors or mount leaks remain. Proxy wire status is unobserved; no successful stream completion is inferred from its absence.

## Historical a622 supplemental evidence

`current-base-evidence-v1.json` separately binds source `a62296fb57263f9be18c6ac879e36e0ab2a9935c`, final `current-base-a622-native-v3/native-build/receipt.json` and `current-base-a622-host-v3/physical-review.json`. All 2,179 current build-source entries, binaries, loaded images and physical receipts are verified. The isolated engine build uses exact Go1.27.2 driver, compiler and linker with the task toolchain GOROOT; the host-installed Go1.27.3 is a separate environmental measurement. SDK3.0.14 and Envoy1.39.1 are physically identified. Native/CGo/Go/race/vet checks and 34 common native observer controls pass; 16/16 native preparation steps exit0.

Three fresh real streaming probes each finish runner/controller0, with no survivors, mount leaks or pending observer scopes. Every route observes target request/response 95/96 bytes, neighbor 6/7 bytes and two complete backend requests. Per-route observations remain distinct:

- `envoy-ext-proc`: two native transaction scopes; request callbacks 64+31+0/EOS and response callbacks 64+32+0/EOS; P1–P4, runtime Finish, logging, native cleanup/destroy and physical event/cleanup receipts are bound. Two idempotent Common Finish calls produce one completed transition per transaction. Target and neighbor have complete HTTP entities and TCP EOF. Local Process reset2 is observed; remote Process status remains unknown.
- `envoy-ext-authz-request`: the host receives multiple request fragments, while the engine receives one complete 95-byte bounded sample with EOS. Native request processing and actual client/backend effects are bound independently. Target and neighbor have complete HTTP entities and TCP EOF. Untagged Authorization trailers leave remote status unknown and successful completion false; target Process scope remains unknown, while neighbor local reset2 is observed. This streaming probe alone does not prove host Reject, native limit decisions or rule interventions.
- `envoy-ext-authz-response-companion`: correlated native lease/response events, P3/P4, response callbacks 64+32+0/EOS, Finish/free and cleanup have physical evidence. P3 completes before the Common commit, which precedes response-body callbacks and P4; this is adapter ordering, not a kernel send timestamp. The target receives the complete HTTP entity then TCP reset errno104; the neighbor reaches TCP EOF. The target Process scope and remote statuses remain unknown; neighbor local reset2 is observed. Missing/expired leases, observer/gRPC abort and first-error retention still require their own fully qualified original-case proofs. No shared HTTP receipt independently qualifies both route legs, and no P4 Strict capability is inferred.

All unscoped Authorization trailers remain unknown and successful completion false; no absent Process grpc-status is interpreted as success. These supplemental probes assign no original ID and add `new_lifecycle_pass=0`. The earlier Go1.27.3 engine build in `current-base-a622-native-v1` and its `current-base-a622-host-v2` probes remain superseded. The `current-base-a622-host-v1` admission failures retain exit77, unknown host execution and no cleanup claim. Rejected `current-base-a622-native-v2` failed before host launch with `compile: version "go1.27.3" does not match go tool version "go1.27.2"`; its mixed-toolchain receipt/stderr remain bound. The final v3 build explicitly isolates GOROOT and proves all three tool identities. Historical case counts and original-case qualifications are not advanced by these supplemental measurements.

## Current-base afaf supplemental evidence

Normal merges retain the subsequent Base heads `e4c872cde16eb73182de49c09a8ba8ee4219b417` and `afaf6305bd55646073c3b40632b52fc4e5edf714`. `current-base-e4-evidence-v2-sonar.json` preserves the passing e4 native build, initial ext_proc timeout and successful host retake. `current-base-afaf-evidence-v3-sonar.json` binds that prior supplement to fresh afaf native and host receipts; it adds no original-ID qualification or oracle progress. The afaf shared-manifest change is inherited from Base; this task edits no shared manifest or product source. The Envoy-local source adapter verifies current registry 155 objects/10 profiles and reconstructs the historical e4 registry from exact physical source anchors.

The delivery Base later advanced by normal merge to `76672071c3f7665dfde3340bef9e64271d6f6e70`. The inherited afaf-to-766 delta changes only two Parent test fixtures and their own EN/DE Change Record. It changes no Envoy, product runtime, capture, dependency or build input, so afaf remains the latest real Envoy native/host evidence source. No new host execution, lifecycle PASS or oracle progress is assigned to 766.

`current-base-afaf-native-v3/native-build/receipt.json` has 16/16 steps exit0, including native/CGo/Go, race, vet and observer controls. Driver/compiler/linker use Go1.27.2; the host probe reports installed Go1.27.3 separately. SDK3.0.14, Envoy1.39.1, loaded images, binaries and all 2,196 build-source entries are physically verified. Earlier technical build/admission failures remain recorded. All three `current-base-afaf-host-v2` runners/controller runs exit0 after the retained host-v1 admission failures. Every route records target request/response 95/96 bytes, neighbor 6/7 bytes, exactly two backend requests and physical Finish/free/cleanup with no surviving task processes or mount leaks. UID/GID65534, capabilities0, NoNewPrivs1 and namespace/listener boundaries remain intact.

- `envoy-ext-proc`: P1–P4, native request callbacks 64/31/0-EOS and response callbacks 64/32/0-EOS, distinct target/sequential-neighbor scopes and Finish/logging/free/Common-cleanup twice. Local Process reset2 remains separate from absent remote gRPC status. The observed text/plain;charset=utf-8 header does not prove independent native MIME/charset selection. This allow probe does not establish Reject/ProcessPartial, cancellation or deliberate missing/repeated callbacks.
- `envoy-ext-authz-request`: client writes 32/32/31 become one complete 95-byte native sample with EOS under host max_request_bytes4096/allow_partial_message=false. The host buffer contract is distinct from native inspection limits. No host reject, native body-limit decision, valid rule intervention or technical runtime failure is triggered. Untagged status0 trailers cannot establish Authorization completion.
- `envoy-ext-authz-response-companion`: lease issue/accepted claim/P3/P4 are allocation-bound in two separate scopes; wire token equality remains unproven. P3 precedes commit and response callbacks 64/32/0-EOS/P4 follow commit. The first client entity byte precedes P4, so P4 Strict is not claimed. Process has local reset2; attributed remote Process/Authorization status remains absent. Missing/expired leases, observer/gRPC abort and first technical error cause require their own qualified cases.

All missing or unattributed remote gRPC statuses remain unknown with successful completion false. `new_lifecycle_pass=0`; the strict 7 lifecycle PASS/118 open, 86 historical host measurements and 37 retakes for 33 IDs remain unchanged. Bounded TAC1/DrayTek Blue verification applies; no deeper security scan is inferred.

## Known limitations

Outcome PARTIAL. Required full host acceptance of all 284 original cases is not established. Current lifecycle PASS totals 7: 5/1/1 for 117/94/73 original IDs; configuration PASS 0/8/0; original open oracles 46/39/33, totaling 118. Of 277 IDs without full lifecycle acceptance, 8 are configuration-only PASS and 269 are unqualified. Direct native MIME/charset selection, fully correlated concurrent terminal gRPC status, complete acceptance of deliberate missing/repeated callbacks beyond the single Response-EOS fault probe, all physical event-sink failures, full observer stop/restart and Strict-P4 capability qualification remain incomplete.

## Remaining risks

Synthetic scenarios have separate IDs; no shared HTTP receipt transfers request acceptance to the companion. Missing remote grpc-status never means successful completion. Earlier client TLS/TCP close handling obscured otherwise complete HTTP responses; retakes preserve both layers. One old controller 77 misidentified a foreign Traefik process; namespace inode reuse is the inferred cause. Its original failure remains, with a fresh scoped namespace-pin retest.

## Checks not run and rationale

Full `rtk proxy make check-bilingual-docs PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` exited2 because this isolated worktree has22 unchanged missing links into the uninitialized Framework gitlink. All Parent bilingual non-link contracts and every new document link passed the scoped checker API; `ci/docs-sonar-v3.json` records that limited result. No Framework checkout, Gitlink or baseline documentation was changed. No master integration or master merge. Full 284-case/original-oracle acceptance and the remaining host capabilities above are not claimed. No broad Framework/MRTS matrix, other-connector run or unrelated production change was authorized. Current-head hosted CI and Quality Gate outcomes are tracked in the Draft PR; local results do not imply CI success.

## Final diff and review status

Scoped static review identified and corrected target-only P3 rule scope, obsolete source identities, build/binary binding, native fixture parsing, partial backend counts and namespace lifetime races. Physical evidence review retains failures. Delivery targets `codex/i12-envoy-410-20261015` against `work/pr382-i12-host-evidence-20261011`; no force push or master merge is authorized. Completion remains partial pending the stated original-case evidence gaps.
