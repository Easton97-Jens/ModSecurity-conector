# PR #382: shared connector behavior checklist

**Language:** English | [Deutsch](pr-382-checklist.de.md)

[Draft PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382),
branch `fix/unified-native-results-events-20260921`, base
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Updated: 2026-10-10.
Historical 2026-10-05 stack readback: the branch was synchronized through then-current `master` `820b6975495bdf0f90aca67eee86e27a3b7d329b` via merge commit `dfd5e5b1`, with no commits behind at that readback.

**I09 and I10 are not yet reduced to live-host proof alone.** Completed code,
executed compiled tests, pending native tests and actual host evidence remain
separate. The Apache module subset is now implemented and must not remain
listed as an untouched intervention/initialization/audit defect.

Historical published test repair (2026-10-05): `7d05e89fc12dca64c7129553d0c83157e956e0f3`.
Its Sonar analysis confirms zero findings and displayed 0.0% new duplication.
Its complete native Envoy job has now passed, including actual Common/libModSecurity
and libmodsecurity-tagged Go tests (V20/V25). The date-field and paired-checklist
repair passed bilingual validation at `b92459ba` (V26). These are revision-scoped
results, not an automatic pass for this later evidence-only update.

Evidence correction: `a6898480` was never published. Its claimed results are not
used. Historical test claims apply only to the referenced revision and test layer.
The six host-action tests were actually delivered in `5a696b7c`.

References: [contract/migration](pr-382-event-contract.md),
[main Change Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.md),
[Apache lifecycle](../reports/audits/change-records/CR-20260923-pr382-apache-native-lifecycle.md),
[Apache adoption](../reports/audits/change-records/CR-20260923-pr382-apache-adoption.md),
[Envoy native test repair](../reports/audits/change-records/CR-20260923-pr382-envoy-test-boundaries.md).


## 2026-10-10 downstream NGINX-H1 system evidence from PR #396

This is a downstream NGINX-H1 system evidence reference from PR #396, not a
runtime test of the unchanged PR #382 product revision. The documentation base
is `2a5704f82fdae4ba75902eb3f4244225838e1747`; this reference neither integrates
the tested #396 code nor changes its Gitlinks.

| Binding | Observed value |
| --- | --- |
| Tested Parent | `777a244f0689c320475b030b9e7adbb3192febbe` |
| Tested Framework | `9f41f80db7bf53b57429457bce0dda675d2ec5d7` (PR #137) |
| Tested MRTS | `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |
| Run / date (UTC) | `nginx_full97_777a_20261010_r16` / 2026-10-10 |
| Standard target | `make full-lifecycle-nginx` through the isolated RTK-wrapped supervisor |
| Concrete local test system | Ubuntu 26.04.1 LTS; kernel 7.0.0-38-generic; x86_64; KVM (actual host readback); GCC 15.2.0; Python 3.14.7; NGINX 1.31.6 |
| Isolation / identities | Private mount/PID/network namespaces; loopback; actual Root master UID 0 / nobody worker UID 65534 |
| Original Canonical / schema | `PASS`; 97/97 selected Required-PASS; both schema error lists empty |
| Remaining inventory | 34 unselected `NOT_EXECUTED`, 35 `NOT_APPLICABLE`; no selected non-PASS record |
| Direct measured completions | 13 completions for nine exact scripts, all exit 0, no signals |
| First-Byte writer | `write-first-byte-source-results.py`: exactly one direct Child wait, exit 0; invocation `1d65c03b1453430eaeede8c1271dd487` |
| Make / supervisor / collector / validator | 0 / 0 / 0 / 0 |
| Actual HTTP operations | 79 non-readiness requests: 75 primary/fault requests plus four parser controls; 17 readiness probes counted separately |
| Other actual operations | 61 server lifecycles / 61 cleanup observations; 17 reloads; 10 config operations (nine specific rejections exit 1, one accepted startup exit 0) |
| Binding observations | 57 fresh root-owned direct projection children; 43 native invocation receipts for 42 native Required records; 24 worker Engine/module mappings |
| Runtime checksum ledger SHA256 | `2c35f93c059dd80bbe84bb158f52bff3bfbe97b81d44379e53ecb3e2bce0e246` |
| Source / ledger verification | 3552 source-file hashes unchanged; runtime ledger 2514 entries, independent checksum check exit 0 |

Public summaries: [PR #396 R16 result](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396#issuecomment-6100868299)
and [Framework PR #137 scope](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/137#issuecomment-6100868488).

**Local acceptance remains BLOCKED by a measurement gap:** the generic H1
Strict curl process's exact numeric exit was not persisted. Its failure is
known to be nonzero, but the diagnostic number `52` is not proof of exit 52.
This is distinct from the native Strict driver and its expected incomplete-read
evidence. Canonical PASS and measured writer exits do not close that missing
direct client-status requirement. PR #396 therefore remains Draft; no overall
local E2E acceptance PASS or Ready transition is claimed here.

Raw evidence and per-record mapping are retained locally below
`/var/tmp/codex/ModSecurity-conector/analysis/nginx-full97-777a244f-20261010T181030Z`
and its separate task runtime root. Local files are not downloadable GitHub
artifacts; the public PR report is a summary, not the raw bundle. Historical R15
retains its original Canonical PASS and separate First-Byte-writer measurement
gap; this fresh run does not rewrite it.

This proves only the observed NGINX-H1 contracts on that concrete local system.
It is not H2/H3, CRS, Off, all-platform, production, cross-connector or Protected
Exact-Head acceptance. Broad I09-I12 and V08-V10 remain open. Framework PR #137's
review readiness is evaluated separately; neither PR is merged by this reference.
Soft-budget cases prove overrun detection after the engine returns, not hard
cancellation of a hanging engine. Transport short-write/EAGAIN observations do
not prove physical event-log sink short-write.

### Historical 2026-10-05 stack and conflict reconciliation

- [x] `master` was merged into PR #382 without force-push. Twelve overlapping files were reconciled semantically: current master CI/security changes were retained together with PR #382 native-result, first-error, Apache lifecycle, NGINX terminal-error and Envoy native-bridge contracts.
- [x] The resulting PR #382 head `dfd5e5b1` was read back as `mergeable=true`, `behind=0`; PR #382 remains Draft and unmerged.
- [x] Two merge-follow-up defects exposed by fresh CI were corrected in `29af9abe`: duplicate `permissions` in `.github/workflows/lint.yml` and the B09 NGINX C regression fixture missing the newer transaction-contract stub. Fresh verification of that follow-up is required; the failed merge-run checks are not relabelled as passes.
- [x] Stacked PR #396 was inspected and refreshed on the updated #382 base. Its NGINX Exact-Head work remains a separate Draft acceptance layer; it does not by itself close I09-I12 or establish a canonical full E2E PASS.
- [x] Framework PR #135 is merged. Its merge commit `dc41bd22c335156cae02d9049098b92af65b7c57` is the Framework gitlink on current `master`/#382. The historical PR #396 pointer `dd4af7d...` is therefore not used as the current Parent gitlink.

## 1. Implementation

- [x] I01: Native byte append accepts 0/1, phase success only 1. APR, NGINX, HTTP, Common and file-loading contracts remain distinct.
- [x] I02: Shared predicates in affected Apache, HAProxy, Common Runtime and NGINX body paths.
- [x] I03: Common/HAProxy intervention validation, cleanup and failure propagation.
- [x] I04: HAProxy response-header binding errors survive disruptive decisions.
- [x] I05: Common JSONL/hash view preserves input validation, redaction, counters and actual observations.
- [x] I06: Technical Apache/Common errors remain distinct from rule blocks; handwritten Apache JSON fallbacks removed.
- [x] I07: Typed NGINX response errors; no successful EOS inferred before evaluation.
- [x] I08: Native engine failure maps to invalid-engine-response; other classes stay distinct.
- [ ] I09: Complete the remaining route-by-route native/API and typed-error audit and resolve any resulting implementation gaps; obtain combined native verification.
- [x] I09a: NGINX byte/file separation, cumulative bounds, success-only completion and terminal failed re-entry (`fcbaca03`; V13).
- [x] I09b: Typed NGINX request errors, exact intervention collection, first cause/status and one event attempt; empty bodies remain valid (`7fe606c5`; V17).
- [x] I09c: Checked, once-only NGINX native audit completion with retained failure (`47714de0`; V17).
- [x] I09d: Envoy ext_proc retains the first Common error, seals failed header/body/EOS callbacks, clears pending rule state and bounds canonical failure reporting (`31200e8c`; V22).
- [x] I09e: Shared NGINX connection/URI result helper retains strict success, PCRE/phase brackets and host statuses without duplicate implementation (`bced5ce7`; V23).
- [x] I09f: Apache module now checks exact intervention results, releases buffers on every post-call outcome, checks retained copies, separates native/host error causes, checks initialization and binds engine cleanup to its configuration generation. Present and tested at `3c29004b`; V24.
- [ ] I10: Complete actual cross-route off/safe/strict error handling and its native integration verification, not merely shared policy tests.
- [x] I10a: NGINX late technical errors precede Safe/Strict rule policy (`52445b18`; V14).
- [x] I10b: Actual Common policy tests cover five error classes, ten profiles, two contract modes and both commitment states; technical failure never becomes Safe log-only. Not host-I/O proof.
- [x] I10c: Real NGINX collector/dispatcher/P4 chain tests retain late rules, Off behavior and cleanup (`1ce569e1`; V17).
- [x] I10d: Envoy commitment failure stops before append; empty EOS does not invent body-started state. Checked C ABI propagates errors through Go while retaining the compatibility ABI (`31200e8c`, `81e53a94`). Native verification passed at `7d05e89f` (V20).
- [x] I10e: Apache's checked collector cannot mutate committed Location headers or reuse stale rule metadata on a technical failure. Audit claims its attempt before callbacks and never dispatches an actionable logging-phase intervention. Present at `3c29004b`; V24 is compiled APR/native-boundary evidence, not live httpd.
- [ ] I11: Complete producer/physical-sink parity, identifiers/causes, observed actions, duplicate terminal events and open/write/short-write/serialization failures.
- [x] I11a: Missing transport observations do not prove rule/error enforcement; custom records and actual evidence remain preserved.
- [x] I11b: Mandatory NGINX Phase-4 log failures remain terminal; invalid sinks and repeated terminal writes are bounded.
- [x] I11c: Missing-observation handling covers body limits, unsupported capabilities, cancellation and upstream disconnect (`3730eaa0`; V18).
- [x] I11d: Runtime retains original event errors with NULL output, prevents failed-write retry and completion/snapshot masking, and preserves hash advancement rules (`68f78e07`; V21).
- [ ] I12: Verify each direct, companion, middleware and sidecar route separately, including actual host/transport/log results.
- [x] I12a: Ten separate ext_proc C-bridge failure/re-entry/empty-response scenarios pass (V22); not ext_authz/companion or live gRPC completion.
- [x] I12b: Downstream R16 from PR #396 executed the standard native NGINX-H1 route with actual Root/nobody separation and fresh projections. This closes only that execution-reference subset, not PR #382 product testing or the measurement-blocked overall local acceptance.
- [x] I13: Bounded HAProxy Rule-ID decoder and ordered cleanup extracted without changing phase/ownership semantics.
- [x] I14: All 96 original NGINX adoption cases plus four regressions retained.
- [x] I15: HAProxy helper/callsite adoption checks and eight isolated regressions retained.

### What remains before "only host proof is missing"

| Item | Remaining requirement |
| --- | --- |
| I09 | Review filter/API exits outside the completed Apache module and the remaining HAProxy, direct, companion and middleware producers. Trace each error through the actual caller and cleanup path; shared predicates or diagnostics alone do not prove completion. The Apache collector/init/audit fixes above are no longer open implementation items. |
| I10 | Verify each remaining adapter's error-to-host-control path, including failures after commitment. Native Envoy verification is now complete at V20, not an outstanding prerequisite. Do not infer missing behavior solely from a helper lacking a guard when the Common state machine may already prevent it. |
| I11 | Apache's void event writer/callers still need complete physical failure propagation; HAProxy SPOP still needs its Common-event fputs result handled. Original Runtime I/O-error retention is fixed. These are implementation work, not just missing live evidence. |
| I12 | Run route-specific host, client-byte/reset, neighbor-stream, cleanup and physical-log cases. Request-only routes require their actual response companion. |

## 2. Verification

- [x] V01: Generated C return types repaired without disabling warnings/assertions.
- [x] V02: Original native/event step passed at `4f94f33d`, [run 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389).
- [x] V03: Compiled native error-classifier regressions and required CI wiring.
- [x] V04: Terminal-error, no-second-response and failed-append accounting assertions retained.
- [x] V05: Historical focused suites passed at `092dfd1c`; evidence retained below.
- [ ] V06: Complete all adoption/mutation checks on the final release head.
- [x] V06a: Historical Apache helper checks and 16 negative mutations passed at `1709e1de`; the current 25-case update is V24.
- [x] V06b: All 100 NGINX adoption/mutation cases passed at `f7aa2f2c`, `092dfd1c` and `bced5ce7`.
- [ ] V07: All final-release checks and review; overall release CI is not claimed green.
- [ ] V07a: Resolve independent secret scanning without an unsupported exception. The fresh exact-range Secret scanning run `37281536909` / job `111670517150` still fails on the synchronized stack. No secret contents are inferred or reproduced from that status.
- [ ] V08: Real-host ProcessPartial/Reject, MIME/CSV, empty/multiple-chunk/EOS, budgets and native errors.
- [x] V08a: R16 supplies actual NGINX-H1 required operation mappings and 97/97 original Required-PASS, including native/config/fault operations; 31 explicit derivations are records, not additional requests. Other hosts/profiles and broader V08 coverage remain open.
- [ ] V09: Late Safe/Strict, pre/post-commit failures, client bytes, reset scope, neighboring streams and cleanup.
- [x] V09a: R16 preserves genuine native Safe/Strict decision, abort/incomplete-read and cleanup evidence. The generic Strict curl process's exact numeric exit remains NOT SEPARATELY MEASURED; this is not complete client-exit acceptance or closure of V09.
- [ ] V10: Actual route logs, invalid/oversized metadata, missing observations and failed physical sinks.
- [x] V10a: R16 has schema-valid Canonical evidence and 13 direct-child completion receipts for nine required programs, including exactly one First-Byte source writer exit 0. This does not close every physical sink/log contract in V10.
- [x] V11: Actual Common JSONL/hash tests retain evidence/redaction; family labels are not host runs.
- [x] V12: Eight compiled HAProxy helper cases and binding compile/link checks passed at `039b7f12`.
- [x] V13: Nine NGINX request/file cases with controlled boundaries, not full file-reader integration.
- [x] V14: Nine NGINX late-error/re-entry cases, not a full HTTP matrix.
- [x] V15: Eight HAProxy Rule-ID adoption cases.
- [x] V16: Historical bilingual/template validation passed at `bced5ce7` and `b91b6826`; the newer Apache report schema repair is V26, not silently inherited.
- [x] V17: 43 NGINX request/native cases, including ten collector-chain and eight audit tests, passed at `b91b6826`.
- [x] V18: 55 Common/native/event/profile cases passed at `b91b6826`.
- [x] V19: Helper-aware source/security repair passed at `b91b6826` without removing other negative paths.
- [x] V20: [Native Envoy job 107300314663](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35896111748/job/107300314663) passed for exactly `7d05e89f`, including the actual Common/libModSecurity build and `go test -mod=readonly -tags libmodsecurity -count=1 ./...`. Both checked-commitment cases are included; this is not just the source/preflight check.
- [x] V21: Eight runtime sink/error-replay plus six host-action cases passed at `b91b6826` (14 total).
- [x] V22: Ten complete ext_proc C-bridge cases passed at `b91b6826`; controlled Common/native boundaries, not live transport evidence.
- [x] V23: Six compiled connection/URI caller/helper cases passed at `b91b6826`.
- [x] V24: At `3c29004b`, [Apache native job 107137107158](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35847504774/job/107137107158) passed the 20 compiled lifecycle cases and bootstrap. [Structure job 107137106792](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35847504774/job/107137106792) passed 25 adoption/mutation cases, then failed the separate missing report-date check.
- [x] V25a: `7d05e89f` contains the native test repair: independent valid-413 and terminal-invalid-acknowledgement cases, explicit unsafe file permissions and retained original inode. Production guards and existing positive controls remain unchanged.
- [x] V25: The native Go suite in V20 passed the V25a fixes, including first-error retention and unchanged event bytes after failed retries. The first failing run is retained as the regression baseline.
- [x] V27: `dfd5e5b1` integrates current `master` `820b6975` into #382 without force-push; the branch read back at `behind=0` and `mergeable=true` before the follow-up fix.
- [x] V28a: `29af9abe` repairs the two deterministic merge-follow-up defects identified by actionlint and the bounded NGINX B09 regression build. This marks the fixes delivered, not their fresh CI rerun.
- [ ] V28: Require fresh CI for `29af9abe` and the later documentation head; do not inherit the failed `dfd5e5b1` actionlint/B09 results or older green results.
- [x] V29: PR #396 stack reconciliation reviewed the six overlapping text paths plus the Framework gitlink. The merged Framework PR #135 result `dc41bd22` is authoritative for the Parent gitlink; PR #396 remains Draft and requires its own post-refresh checks.
- [x] V26: [Lint job 107304638636](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35897399419/job/107304638636) passed the unchanged bilingual validator for `b92459ba`, confirming both added date fields and the paired checklist. Its overall status was still running at this readback.

## 3. Sonar zero findings and zero duplication

- [x] S01: Read-only exact-head/provider gate rejects missing, stale, unfinished and ambiguous evidence.
- [x] S02: Negative tests, bounded diagnostics and scoped read permissions retained; no exclusions, accepted findings or weaker rules.
- [x] S03: Historical zero counts remain revision-specific: `039b7f12`, `91f07e12`, `47714de0`.
- [x] S03a: Exact-head gate passed at `f7aa2f2c`.
- [x] S03b: `91f07e12`, [check 106651947571](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106651947571): zero new/accepted issues, hotspots and annotations.
- [x] S03c: `47714de0`, [check 106837589312](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106837589312): same four zero counts.
- [x] S03d: `bced5ce7`, [check 106898325037](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106898325037): same zero counts and displayed 0.0% duplication.
- [x] S03e: Exact `7d05e89f`, [check 107300845580](https://github.com/Easton97-Jens/ModSecurity-conector/runs/107300845580): zero new/accepted issues, hotspots and annotations; displayed new-code duplication 0.0%.
- [ ] S04: Confirm final-release-head quality after the last delivery; earlier analysis cannot prove a later documentation SHA.
- [x] S05: Required duplication gate demands exact zero new duplicated lines, blocks and density, not a rounded percentage alone.
- [x] S06: Exact duplication gate passed at `bced5ce7`, [job 106897813154](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35772630849/job/106897813154), and at `b91b6826` in the full lint run below.

These are PR new-code metrics, not claims about all historical repository debt.
Coverage and secret scanning are independent requirements.

## 4. Route-specific state

| Route | Completed subset | Remaining |
| --- | --- | --- |
| NGINX native | Typed errors, predicates, audit latch, caller and adoption tests | Final combined and live transport/log matrix |
| Apache native | Exact collector, copied storage, first errors, checked audit/init/generation cleanup; 20 compiled and 25 adoption cases | Other filter/API exits, physical sink propagation and live host matrix |
| HAProxy HTX | Binding predicates and helper/adoption tests | Caller-level failure/cleanup and host/reset/log verification |
| HAProxy SPOE/SPOP + companion | Native/Common result contracts | SPOP write propagation and distinct companion/control proof |
| Envoy ext_proc | Checked commitment, sticky errors, ten C-bridge cases and real native Go suite passed | Live gRPC/host/log cases and final combined verification |
| Envoy ext_authz + companion | Shared Runtime fixes | Separate companion lifecycle and physical output proof |
| Traefik middleware/UDS | Shared Runtime fixes | Adapter-level errors, physical sinks and live host evidence |
| Traefik forwardAuth + companion | Shared Runtime fixes | Separate companion control/log evidence |
| lighttpd sidecar | Shared Runtime fixes | Adapter failure and actual socket/log evidence |
| lighttpd native/patched | Shared contracts on Runtime routes | Separate hooks, strict admission and native host proof |

Unsupported strict profiles remain unsupported. Equal semantics neither require
identical host integers nor grant new reset/abort capabilities.

## 5. Documentation and delivery

- [x] D01: Existing Draft PR only; no merge/master/force push.
- [x] D02: EN/DE checklist distinguishes implemented code from verification.
- [ ] D03: Complete connector guides/examples and compatibility review.
- [x] D03a: Paired contract and consumer/hash migration warnings retained.
- [x] D04: Reconcile actual Apache/Envoy work, the 2026-10-05 master conflict resolution, PR #396 stack status and the merged Framework #135 gitlink; obsolete pre-sync claims are removed.
- [ ] D05: Final-release document/link/diff/CI and PR/branch reconciliation.

## Revision-scoped evidence

The full [lint job 106900742683](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35773496921/job/106900742683)
passed for `b91b6826`, including both Sonar gates. That is historical evidence,
not an automatic pass for new Apache source or Envoy tests.
The `3c29004b` Apache structure job reached its final bilingual check before
failing for two missing date fields. Its native/APR job passed independently.
The first real Envoy run [35847504839](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35847504839)
failed three fixture/expectation cases; the repaired full native run passed at
`7d05e89f` (V20/V25), without changing production protections. The unchanged
bilingual check passed after the date-field fix at `b92459ba` (V26).

On 2026-10-05, #382 was synchronized with current master in `dfd5e5b1`. Fresh CI on that merge confirmed several connector workflows but exposed two deterministic merge-follow-up defects: duplicated job permissions in lint and an outdated B09 compiled fixture. Both are repaired in `29af9abe`; fresh post-fix checks remain required. Secret scanning remains independently open. PR #396 was also inspected as a stacked Draft; its NGINX Exact-Head chain is useful downstream evidence but its historical canonical run was not a full E2E PASS.

Earlier evidence remains in [the checklist at ad22918e](https://github.com/Easton97-Jens/ModSecurity-conector/blob/ad22918e92849a10483439d72ac9a50154ec00be/docs/pr-382-checklist.md)
and linked Change Records. The user clarified RTK scope for this continuation;
GitHub API edits do not require a local execution wrapper. Local Go formatting
was performed for the new native fixture and its consumer; full native execution
uses GitHub CI because GitHub DNS/download was unavailable in the editing container.
