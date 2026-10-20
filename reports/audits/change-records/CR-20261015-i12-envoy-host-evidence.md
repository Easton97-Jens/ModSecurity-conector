# Change Record: CR-20261015-i12-envoy-host-evidence

**Language:** English | [Deutsch](CR-20261015-i12-envoy-host-evidence.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-i12-envoy-host-evidence |
| Date (UTC) | 2026-10-15 |
| Base revision | `a62296fb57263f9be18c6ac879e36e0ab2a9935c` |
| Native/host evidence source revision | `f27eb59b53beff6f65384fc2e5037881a3052c01` |

## Motivation and problem statement

The original Envoy ledger has 284 IDs across ext_proc, request authorization and the response companion. Three existing lifecycle PASS resolve only three of 125 original open oracles. Host effects must remain distinct from unit/build results and configuration-only PASS.

## Acceptance criteria

Preserve all original IDs/oracles and patched Go/x/net inputs; execute real isolated host probes and native/Go/race/vet controls; bind physical evidence and report each route separately. Full original-case acceptance remains unmet: 114 original oracles remain open after eight newly qualified original IDs; the retained central baseline remains unchanged.

## Implementation decision and rationale

Add only Envoy-specific I12 producers/tests and own EN/DE reports. Reuse the unchanged envoy capture registry and common observer in a Git-free source copy. Verify binary/source/SDK correspondence. Count started/aborted backend requests separately; preserve TCP resets and missing gRPC status. Pin the positively identified PID namespace through cleanup in the Envoy-only controller copy, with identity checks before/after open and fail-closed fallback. Preserve original controller gates and all failed attempts.

## Changed files

New Envoy-local files under `ci/runtime/lifecycle/i12/envoy/`: native preparation, original-ledger reconciliation, host fixture preparation/runner, transport classifier, physical reviewer, report producer, tests and EN/DE README. Own report pair and exact-ID JSON: `reports/testing/i12-envoy-host-evidence-20261015.*`. Parent discovery wrapper: `tests/test_i12_envoy_evidence.py`. This EN/DE Change Record pair. In the task diff against Base, shared manifest/generators, product files, other connectors, dependencies and Gitlinks are unchanged.

## Commands executed

All shell entrypoints used RTK. Actual native/CGo build, full Go tests, race and vet argv/results/log hashes: `/var/tmp/codex/ModSecurity-conector/runs/i12-envoy-410-20261015/native-v2/native-build/receipt.json`. `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_i12_envoy_evidence`: 188 PASS, 0 skips; current raw logs and all 26 Envoy Python source hashes are bound in `ci/final-envoy-controls-188-base-a622-v2.json`. Focused fault controls have 16 PASS; separate Go test-proxy controls have 10 PASS. Existing affected Python contracts: 79 PASS with one observer setup skip; the separately configured native observer has 32 PASS. `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -B ci/runtime/lifecycle/i12/capture_sources.py verify`: PASS (150 objects/9 profiles). Existing capture-source controls: 15 PASS. `go mod verify` through RTK with the task-owned offline module cache: PASS. Host commands and nonzero exits remain in each batch runs.json; they are not normalized to PASS.

## Security impact

CI remediation closes unbounded CLI/JSON file access in the Envoy evidence readers. Approved roots are checked before filesystem access; directory descriptors, O_NOFOLLOW, owner/mode checks, byte limits and stable file identity protect the read. Outputs use private, exclusive creation; Git metadata arguments require exact SHAs and fixed scope. The current complete Envoy suite has 188 PASS and 0 skips. The new reader is hash-bound in freshly reproduced, individually approved packets; old packets and raw host runs remain retained. The previously analyzed Sonar head was `edc09b689d38d62ae33c3c1170eedbc4300b8399`, with Quality Gate OK, zero bugs, zero vulnerabilities and 24 maintainability code smells. Bounded read-only triage found no functional, security or evidence-PASS defect in those findings; current exact-head status remains tracked in Draft PR417. No rule, exclusion, disposition or Quality Gate was changed.


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

86 real host measurements include 37 retakes under 33 exact original IDs. Eight individual Root approvals after fresh reproduction of all 35 proof categories qualify these exact original IDs; the three previous lifecycle PASS remain preserved:

- `I12::envoy-ext-proc::NEED-request-streaming`
- `I12::envoy-ext-proc::NEED-response-streaming`
- `I12::envoy-ext-proc::NEED-client-response-bytes`
- `I12::envoy-ext-proc::NEED-client-exit-signal`
- `I12::envoy-ext-authz-request::NEED-complete-sample`
- `I12::envoy-ext-authz-request::NEED-request-multiple-chunks`
- `I12::envoy-ext-authz-request::NEED-client-response-bytes`
- `I12::envoy-ext-authz-response-companion::NEED-allow`

The two additional request-authorization qualifications independently bind the host and client contracts. The physical Envoy trace identifies worker 285 / CID1 / SID6459190741822168578 and host fragments 64+31=95 followed by EOS, then the Authorization Check at line 275. The engine receives one complete 95-byte native sample and one EOS; multiple client writes do not imply multiple native callbacks. The response-byte qualification independently checks raw HTTP framing and client entity bytes. Process remote gRPC status remains unknown and is not counted as success.

The additional companion retake proves two early captured backend requests, target 1 / neighbor 1, request 95 / response 96 and response callbacks 64+32+0/EOS. Lease claim, P1–P4, logging, RuntimeFinish, NativeFree and cleanup are physical observations; the separate request leg gains no further PASS. Observed local HTTP2 reset 2 remains separate from unknown remote gRPC status.


The exact Base head `a62296fb57263f9be18c6ac879e36e0ab2a9935c` was merged into this branch in `dfb1a07a863530a53c0006ee204319453d66a2ad`. The retained baseline and physical sources were revalidated with the current central validators; this Envoy task modified no shared validator. Existing native and host evidence remains limited to `f27eb59…` and does not qualify the merged Base product state; a fresh current-Base capture remains required. The fixture from `fault_scenarios.py` and separate Go test proxy were used in the real, bounded ext_proc Response-EOS fault probe `fault-host-v1`. Its runner77/controller1/client1 remains unqualified; new PASS: 0.
The probe drops only the empty Response-EOS callback and performs an actual half-close. The engine API and unambiguously correlated Envoy target stream report gRPC status14. The target client receives HTTP200 with a prefix of 96 body bytes in 64+32 without a terminating zero chunk. P1–P3 are observed, P4=0; the `runtime_finish` attempt has result0 and is not counted as successful Finish. Logging/free/cleanup are one each. The healthy neighbor reaches P1–P4/Finish once each. No survivors or mount leaks remain. Proxy wire status is unobserved; no successful stream completion is inferred from its absence.


## Known limitations

Outcome PARTIAL. Required full host acceptance of all 284 original cases is not established. Current lifecycle PASS totals 11: 5/4/2 for 117/94/73 original IDs; configuration PASS 0/8/0; original open oracles 46/36/32, totaling 114. Of 273 IDs without full lifecycle acceptance, 8 are configuration-only PASS and 265 are unqualified. Direct native MIME/charset selection, fully correlated concurrent terminal gRPC status, complete acceptance of deliberate missing/repeated callbacks beyond the single Response-EOS fault probe, all physical event-sink failures, full observer stop/restart and Strict-P4 capability qualification remain incomplete.

## Remaining risks

Synthetic scenarios have separate IDs; no shared HTTP receipt transfers request acceptance to the companion. Missing remote grpc-status never means successful completion. Earlier client TLS/TCP close handling obscured otherwise complete HTTP responses; retakes preserve both layers. One old controller 77 misidentified a foreign Traefik process; namespace inode reuse is the inferred cause. Its original failure remains, with a fresh scoped namespace-pin retest.

## Checks not run and rationale

Full `rtk proxy make check-bilingual-docs PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` exited2 because this isolated worktree has22 unchanged missing links into the uninitialized Framework gitlink. All Parent bilingual non-link contracts and every new document link passed the scoped checker API; `ci/docs-postmerge-a622-v2.json` records that limited result. No Framework checkout, Gitlink or baseline documentation was changed. No master integration or master merge. Full 284-case/original-oracle acceptance and the remaining host capabilities above are not claimed. No broad Framework/MRTS matrix, other-connector run or unrelated production change was authorized. Current-head hosted CI and Quality Gate outcomes are tracked in the Draft PR; local results do not imply CI success.

## Final diff and review status

Scoped static review identified and corrected target-only P3 rule scope, obsolete source identities, build/binary binding, native fixture parsing, partial backend counts and namespace lifetime races. Physical evidence review retains failures. Delivery targets `codex/i12-envoy-410-20261015` against `work/pr382-i12-host-evidence-20261011`; no force push or master merge is authorized. Completion remains partial pending the stated original-case evidence gaps.
