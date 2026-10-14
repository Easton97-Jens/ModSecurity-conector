# PR #382: shared connector behavior checklist

**Language:** English | [Deutsch](pr-382-checklist.de.md)

## Current I12 execution, 2026-10-14

Outcome: **I12_PARTIAL**. The [current host report](pr-382-i12-host-evidence-20261014.md)
and [complete index](pr-382-i12-missing-case-index-20261014.md) retain all
1,484 IDs. NGINX and the three Traefik legs now execute in isolated hosts;
Apache, HAProxy, Envoy, Stock and patched-host retakes retain separate original
client/backend/log/cleanup evidence. Config-parser qualification covers only
its explicit contract. I12/V08–V10 stay unchecked while physical EOS/MIME,
Common-Finish and complete case/oracle bindings remain missing. The historical
secret-range failure separately blocks release. Exact final CI is in the PR bodies.

## Earlier I12 execution, 2026-10-13

Outcome: **I12_PARTIAL**. Parent
`a9d48bb58aa948aea7d79e20cdf09d3f239b7808` includes the reproduced HAProxy
native outcome, normal P3 completion and phase-conversion repairs. The existing #410 branch receives
this Parent through normal merges and retains its historical evidence.
The [current host report](pr-382-i12-host-evidence-20261013.md) covers all
13 required legs and the separate Stock-native control, 1,406 required and
78 diagnostic obligations, actual host attempts and remaining prerequisites.
Bounded host success and component tests leave I12/V08/V09/V10 unchecked.
The independent historical secret-range gate remains failed. Final exact
Parent/evidence delivery and CI states are in the current PR descriptions.

## Earlier review/Go checkpoint, 2026-10-13

State: **BLOCKED_FOR_I12**. Current remediation starts at
`4639f982a8125f4150394e4d4f2e8af4e690f494`. The [consolidated Change Record](../reports/audits/change-records/CR-20261013-pr382-consolidated.md)
replaces 122 historical EN/DE pairs with one pair while retaining immutable
original evidence. Private/budgeted Stock spools, Traefik commit-before-ACK,
Envoy socket ownership and eight Sonar source repairs preserve I09/I10/I11 and
engine-owned body limits. Go 1.27.2, four module minima 1.26.9 and targeted
`x/net` 0.61.0 / `x/sys` 0.49.0 / `x/text` 0.43.0 replace vulnerable versions;
grpc 1.83.2 and protobuf 1.36.11 remain unchanged.

All four local Go module validations, including race and govulncheck, pass,
as do 71 updater/workflow tests and quick-check. Focused local acceptance does
not replace final remote CI/Sonar/review readback. Two historical Gitleaks prose
matches block the independent PR secret check; append-only commits do not remove
them. No scanner exception or history rewrite is performed. The real nonroot
Stock startup is BLOCKED by local UID mapping `0 0 1`. The master updater has
not run after integration; **MASTER_WORKFLOW_VERIFIED: NOT_EXECUTED**. The
[I12 handoff](pr-382-i12-handoff.md) binds missing host evidence and final delivery facts;
That earlier task left #410 and the full I12 matrix untouched. Historical R16/R17 and the table
revisions below retain their original scope.

[Draft PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382),
branch `fix/unified-native-results-events-20260921`, base
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Updated: 2026-10-13.
Historical 2026-10-10 stack readback: the branch is synchronized through `master` `3019722fbda40dc281b861c1cc38085be2f430a0` via merge commit `b3dc0139`; `behind=0` and GitHub reports the PR mergeable. Framework PR #137 is merged and the Parent now pins its merge commit `99a7985c1be92a2297b1b59208f64df6768f2cbf`. Stacked PR #396 is merged into #382 at `da50b67c`; its later historical source-head SHA remains evidence provenance only.

**I09 is closed for the audited code/API contracts on 2026-10-11.** The [current I09 route audit](pr-382-i09-route-audit.md) covers 14 route legs across ten profiles. I10 and I11 are complete in their separately verified implementation scopes; I12 remains open. The I11 implementation closes neither live-host proof nor release CI. Completed Apache module repairs remain preserved.

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
[main Change Record](../reports/audits/change-records/CR-20261013-pr382-consolidated.md),
[Apache lifecycle](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260923-pr382-apache-native-lifecycle.md),
[Apache adoption](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260923-pr382-apache-adoption.md),
[Envoy native test repair](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260923-pr382-envoy-test-boundaries.md).


## PR #409 base refresh, 2026-10-12

PR #409 combines verified I10 head `caafe7ecec1a91669cbb82cea18b2b97309cde44` with newer PR #382 base `d94a7a38b90bc56b828d70f7df8794e12fd21e10`, including I09/I11 closure and engine-owned body limits. Completed checkboxes preserve their separately verified earlier implementation acceptance; they do not claim freshly executed tests or CI on the combined head. Fresh integration/delivery checks are recorded separately in the [refresh Change Record](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261012-pr409-base-refresh.md); they are pending at this documentation reconciliation. I12/V08–V10 live evidence remains open; R16/R17 are not rebound.

## Current 2026-10-11 I11 sink reconciliation

Integration readback: published I11 head `6a79efe7` and PR #382 base `492663334d89428dce084792145ef94e91579788` (I09 / PR #408) are combined in PR #406. Fresh local integration checks and conflict-resolution decisions are in the [integration change record](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-pr406-i09-i11-conflict-resolution.md). The I09 and I11 evidence below belongs to their separate earlier revisions; it is not current-head CI or live-host proof. Pushed-head delivery checks are tracked separately in PR #406.

The isolated branch `fix/i11-event-sink-parity-20261011` starts at `0df51024008fc84f0a6820f3b011055b69c3a3e2` from PR #382. Code changes and current compiled tests satisfy I11 implementation acceptance; I11 is `[x]`, with live-host I12/V10 evidence still open. The [Change Record](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-pr382-i11-physical-sink-parity.md) and [remaining-work matrix](pr-382-i09-i12-rest-matrix.md) separate current patch evidence from historical R16/R17 and open I12/V10 evidence. The historical description of unchecked Apache/SPOP sinks below applies to its original checkpoint, not the current patch.

Pre-integration I11 evidence (published head `6a79efe7`): physical sink tests 50, Common/event regressions 60, fully instrumented C ASan/UBSan tests 46, Apache native/C17 45 and adoption 28, Envoy native/tagged 218 tests/324 cases/8 packages and race 105/164/3 pass. All 110 NGINX adoption methods pass in four disjoint shards of 28+28+27+27 tests. Bilingual/path/link, workflow, format and Change Record checks pass. Broad Apache suite: current patch 215 tests, 7 failures/7 errors; unchanged base 195 tests, 8 failures/7 errors. No new failure/error sets; the earlier precommit_rate_limit fixture failure now passes. Three UID/chown environment errors occur on both revisions. HAProxy suite: 203 tests, five failures reproduced on base, twelve skips. Neither broad suite is claimed fully green.

## Historical PR #382 host-evidence run, 2026-10-11

The [historical host-evidence report](pr-382-i12-host-evidence-20261011.md) keeps
route-specific observations and remaining cases separate from historical R17.
Run `20261011T063350Z-0df51024008f-i12` binds tested Parent
`0df51024008fc84f0a6820f3b011055b69c3a3e2`, Framework
`99a7985c1be92a2297b1b59208f64df6768f2cbf` and MRTS
`8a6bb546c4c81d8ffc7be801dceac60c6925685f`. This product tuple does not identify
the later documentation or delivery commit.

Build/version checks and isolated admission probes prove prerequisites only.
An Apache allow observation alone does not close its required host, transport,
physical-sink and cleanup matrix. Request and response companion legs require
separate evidence. I12c–l and broad I12 remain unchecked; the report records
actual case outcomes without transferring R17 PASS to this tuple. Local raw
bundles are retained evidence, not downloadable GitHub artifacts.

## Historical R16: 2026-10-10 downstream NGINX-H1 system evidence from PR #396

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

**At the R16 checkpoint, local acceptance remained BLOCKED by a measurement gap:** the generic H1
Strict curl process's exact numeric exit was not persisted. Its failure is
known to be nonzero, but the diagnostic number `52` is not proof of exit 52.
This is distinct from the native Strict driver and its expected incomplete-read
evidence. Canonical PASS and measured writer exits do not close that missing
direct client-status requirement. PR #396 therefore remained Draft at that checkpoint; no overall
local E2E acceptance PASS or Ready transition is claimed here.

Raw evidence and per-record mapping are retained locally below
`/var/tmp/codex/ModSecurity-conector/analysis/nginx-full97-777a244f-20261010T181030Z`
and its separate task runtime root. Local files are not downloadable GitHub
artifacts; the public PR report is a summary, not the raw bundle. Historical R15
retains its original Canonical PASS and separate First-Byte-writer measurement
gap; this fresh run does not rewrite it.

This proves only the observed NGINX-H1 contracts on that concrete local system.
It is not H2/H3, CRS, Off, all-platform, production, cross-connector or Protected
Exact-Head acceptance. At the R16 checkpoint I10/I12 and V08-V10 remained open; later I09/I10/I11 code closures apply only to their own revisions. Framework PR #137's
review readiness is evaluated separately; neither PR is merged by this reference.
Soft-budget cases prove overrun detection after the engine returns, not hard
cancellation of a hanging engine. Transport short-write/EAGAIN observations do
not prove physical event-log sink short-write.

## R17: downstream NGINX-H1 system evidence from PR #396

**Nachgelagerter NGINX-H1-Systemnachweis aus PR #396.** The [public R17 report](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396#issuecomment-6101794434) was published before this documentation change. It records one authorized standard local Full97; it does not test the PR #382 product or this later documentation revision. Documentation base: `b2622a5d6ca746485c08f4789208299a111f47c7`. No product source or Gitlink changes.

| Binding | Actual R17 result |
| --- | --- |
| Tested Parent | `2f02370b07149265841411894f1a2cf7f1e978ff` |
| Tested Framework / MRTS | `9f41f80db7bf53b57429457bce0dda675d2ec5d7` / `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |
| Run / target | `nginx_full97_2f02_20261010_r17` / `make full-lifecycle-nginx` |
| System / isolation | Ubuntu 26.04.1 LTS; kernel 7.0.0-38-generic; x86_64/KVM; GCC 15.2.0; Python 3.14.7; NGINX 1.31.6; private mount/PID/network namespaces, loopback, actual Root UID 0 / nobody UID 65534 |
| Actual lifecycle | Exit 0; 554.091 seconds; local scoped functional PASS |
| Original Canonical / selection | PASS; unchanged 97 Required = 14 YAML + 42 native + 10 config + 31 explicit derivations; zero required FAIL/BLOCKED/NOT_EXECUTED/missing; schema error lists empty |
| Other inventory / source placeholders | 34 unselected NOT_EXECUTED + 35 NOT_APPLICABLE; original source-result retains 31 PASS + 42 NOT_EXECUTED placeholders, with actual specialized native lineage instead of synthetic PASS |
| Generic Strict direct client completion | Actual normal curl exit 52, not diagnostic inference; invocation `669ba1b19fc340618d62148d715e5fc3`, child PID 10440; Rule 1100301 strict/abort; exact case/run/source/log/TX binding |
| Client observation boundary | Actual curl HTTP value 000; producer/original status 200 is a different observer. Native Strict separately received HTTP 200, 10428 bytes, chunked/incomplete_read/connection_aborted, driver exit 0 |
| First-Byte source writer | Actual normal exit 0; invocation `1515086ec928494aafd0b0a0fceab107`, child PID 12514; original barrier/EOS/identity binding retained |
| Direct completion inventory | 34 curl pairs = 16 primary + 1 First-Byte + 17 readiness; 16 program completion pairs, all normal exit 0, no signals |
| HTTP / lifecycle / cleanup | 79 non-readiness HTTP operations including four positive controls; 17 readiness separately; 61 real server lifecycles / cleanup observations; 17 reloads |
| Config / native / projections | 10 config operations (nine normal reject exits 1, one accepted startup exit 0); 43 native invocations for 42 native Required records; 57 distinct fresh root-owned nonsymlink direct projection children |
| Source / final checksum ledger | 3554 source-file hashes unchanged; 2589 final entries, independent checksum check exit 0; SHA256 `b79fbe3e2b7cf2806c8698f2a6fd7f1f1a4c4f06aed8075924311d4d1c27d97a` |

The external direct-child recorder used the existing curl injection seam without Parent/Framework/MRTS functional changes. It persisted actual `subprocess.Popen/direct-child.wait` status, preserving arguments, streams and signals; no blanket nonzero=PASS rule. The specific Strict oracle, genuine rule/transport and exact identities remain required. A genuine bounded focus preceded the single Full97. Failed pre-request focus setups and historical R15/R16 remain unchanged.

This closes the R16 measurement gap **only for the new R17 NGINX-H1 local scope**. It is not Protected Exact-Head, H2/H3, CRS, Off, production, other connectors or a runtime PASS for a later documentation SHA. Framework PR #137 was already merged with tested head `9f41f80…`; its merge commit does not change the tested Gitlink. This reference claims no Ready, merge or retarget action for #396. #382 remains Draft.

The [I09–I12 remaining-work matrix](pr-382-i09-i12-rest-matrix.md) lists 56 explicit rows across 14 separate route legs, each with contract, source/test SHA, open implementation/host proof and next action. The 2026-10-11 audit supersedes the historical I09 code inventory; I10 was open at that historical checkpoint; its later code closure is recorded separately above. I12 and V08–V10 remain open; completed I09f/I10e remain completed. The historical Apache void sink completion and unchecked SPOP `fputs` findings are closed by the separately verified I11 repairs. Transport short-write/EAGAIN does not prove physical sink failure handling; soft budgets detect overrun after return, not hard cancellation.

Local raw evidence remains under `/var/tmp/codex/ModSecurity-conector/analysis/nginx-strict-client-full97-r17-20261010T193127Z` and its separate runtime root. The public report is a summary, not a downloadable raw bundle. Checksums alone do not establish semantic PASS.

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
- [x] I09: Complete code/API audit of all 14 route legs across ten profiles, repair confirmed native/API/typed-error gaps and pass combined compiled verification; [2026-10-11 audit](pr-382-i09-route-audit.md). No live-host or release closure.
- [x] I09a: NGINX byte/file separation, cumulative bounds, success-only completion and terminal failed re-entry (`fcbaca03`; V13).
- [x] I09b: Typed NGINX request errors, exact intervention collection, first cause/status and one event attempt; empty bodies remain valid (`7fe606c5`; V17).
- [x] I09c: Checked, once-only NGINX native audit completion with retained failure (`47714de0`; V17).
- [x] I09d: Envoy ext_proc retains the first Common error, seals failed header/body/EOS callbacks, clears pending rule state and bounds canonical failure reporting (`31200e8c`; V22).
- [x] I09e: Shared NGINX connection/URI result helper retains strict success, PCRE/phase brackets and host statuses without duplicate implementation (`bced5ce7`; V23).
- [x] I09f: Apache module now checks exact intervention results, releases buffers on every post-call outcome, checks retained copies, separates native/host error causes, checks initialization and binds engine cleanup to its configuration generation. Present and tested at `3c29004b`; V24.

- [x] I09g: Common retains first cause/phase, NULL error output and missing-rule failure; terminal connection/body/EOS retry is blocked, BODY_LIMIT stays separate from technical and rule events.
- [x] I09h: Apache filters and HAProxy binding/HTX/SPOP check returns, terminal retry, typed producers and once-only cleanup through actual compiled callers.
- [x] I09i: Traefik direct/companion and lighttpd sidecar/module routes propagate commit/action failures; host latches prevent continuation and post-denial commit. Stock-native body hooks remain unsupported.
- [x] I09j: Integrated 33 compiled test methods and Common C17 smoke passed; independent follow-up found no residual I09 code gap in selected paths. External limits and open release checks remain documented below.

- [x] I10: Productive technical-error propagation across all ten registry routes and 14 separate legs is implemented and executable/native verified. I10a–I10e remain intact; live-host/client/transport evidence remains I12/V08–V10. See [Change Record](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-pr382-i10-adapter-errors.md).
- [x] I10a: NGINX late technical errors precede Safe/Strict rule policy (`52445b18`; V14).
- [x] I10b: Actual Common policy tests cover five error classes, ten profiles, two contract modes and both commitment states; technical failure never becomes Safe log-only. Not host-I/O proof.
- [x] I10c: Real NGINX collector/dispatcher/P4 chain tests retain late rules, Off behavior and cleanup (`1ce569e1`; V17).
- [x] I10d: Envoy commitment failure stops before append; empty EOS does not invent body-started state. Checked C ABI propagates errors through Go while retaining the compatibility ABI (`31200e8c`, `81e53a94`). Native verification passed at `7d05e89f` (V20).
- [x] I10e: Apache's checked collector cannot mutate committed Location headers or reuse stale rule metadata on a technical failure. Audit claims its attempt before callbacks and never dispatches an actionable logging-phase intervention. Present at `3c29004b`; V24 is compiled APR/native-boundary evidence, not live httpd.
- [x] I10f: HAProxy HTX: exact Common/nested-result returns, once-only host control, commit/EOS/reentry/cleanup; productive caller/mutation checks and full native HTX build passed.
- [x] I10g: HAProxy SPOP request and HTX response companion separately: technical ACK503, first error code/diagnostic, EOS/ack/release and terminal host output; executable caller/mutation checks passed.
- [x] I10h: Envoy ext_authz request and independent response companion plus ext_proc: technical errors, commit/EOS/reentry, checked close ABI, missing EOS and listener cleanup; complete native/CGo/Go race suites passed.
- [x] I10i: Traefik Native/UDS and forwardAuth request/observer: typed MSE1/MRC1 errors, actual host write before ACK, terminal postcommit error and once cleanup; caller/Go race/vet/mutation checks passed.
- [x] I10j: lighttpd stock sidecar and native/patched hooks separately: socket result, commit/reentry/reset/upstream errors and first cause despite later deadline; 479 executable cases/9 mutations and complete native builds passed.
- [x] I10k: Final cross-route reconciliation: no known adapter implementation gap; technical Off/Safe failures never become rule log_only; Strict follows unchanged registry; I11 was completed separately; I12 remains open.
- [x] I11: Complete producer/physical-sink parity, identifiers/causes, observed actions, duplicate terminal events and open/write/short-write/serialization failures.
- [x] I11a: Missing transport observations do not prove rule/error enforcement; custom records and actual evidence remain preserved.
- [x] I11b: Mandatory NGINX Phase-4 log failures remain terminal; invalid sinks and repeated terminal writes are bounded.
- [x] I11c: Missing-observation handling covers body limits, unsupported capabilities, cancellation and upstream disconnect (`3730eaa0`; V18).
- [x] I11d: Runtime retains original event errors with NULL output, prevents failed-write retry and completion/snapshot masking, and preserves hash advancement rules (`68f78e07`; V21).
- [x] I11e: Apache propagates typed physical sink results through request/filter callers; mandatory and diagnostic events remain distinct.
- [x] I11f: HAProxy SPOP checks serialization, fputs/ferror/fflush and owned fclose; first sink failure prevents retry and successful ACK fallback.
- [x] I11g: Common replay protection remains intact; Apache/SPOP and Envoy writers retain first cause and prevent further physical writes after sink failure.
- [x] I11h: All 14 producer/sink route legs are reconciled and compiled current tests pass; no known I11 implementation gap remains. Baseline/environment and I12/V10 limitations are separate.
- [ ] I12: Verify each direct, companion, middleware and sidecar route separately, including actual host/transport/log results.
- [x] I12a: Ten separate ext_proc C-bridge failure/re-entry/empty-response scenarios pass (V22); not ext_authz/companion or live gRPC completion.
- [x] I12b: Downstream R17 from PR #396 executed the standard NGINX-H1 route with actual Root/nobody and fresh projections, locally scoped functional PASS. This closes only the execution-reference subset, not PR #382 product testing or broad I12; R16 remains historical.
- [ ] I12c: Apache native/direct: complete current-run host, client/backend, physical-sink and cleanup evidence.
- [ ] I12d: HAProxy HTX direct: complete current-run native host/transport/log evidence.
- [ ] I12e: HAProxy SPOE/SPOP: prove request and required response-companion legs separately.
- [ ] I12f: Envoy ext_proc direct: prove actual Envoy/gRPC host, downstream action and physical logs.
- [ ] I12g: Envoy ext_authz: prove request authorization and required response companion separately.
- [ ] I12h: Traefik Native/UDS middleware: prove actual middleware/UDS host and downstream results.
- [ ] I12i: Traefik forwardAuth: prove request authorization and required response companion separately.
- [ ] I12j: lighttpd stock/sidecar: prove the traffic-owning sidecar route; keep the native diagnostic control separate.
- [ ] I12k: lighttpd patched/native: prove supported native host actions without inventing Strict abort capability.
- [ ] I12l: Reconcile all ten logical routes, required companion legs, current NGINX evidence, case outcomes, provenance and remaining work.
- [x] I13: Bounded HAProxy Rule-ID decoder and ordered cleanup extracted without changing phase/ownership semantics.
- [x] I14: All 96 original NGINX adoption cases plus four regressions retained.
- [x] I15: HAProxy helper/callsite adoption checks and eight isolated regressions retained.

The [nine-column I09–I12 matrix](pr-382-i09-i12-rest-matrix.md) makes the remaining implementation and host evidence explicit for all 14 route legs; the historical inventory closes no broad checkbox; the current I09 audit closes code/API only.

### What remains before "only host proof is missing"

| Item | Remaining requirement |
| --- | --- |
| I09 | Code/API scope closed on 2026-10-11; the current [14-leg audit](pr-382-i09-route-audit.md) supersedes the earlier open code inventory. I10 is complete in its separately verified implementation scope; I12 and host/release evidence remain open; I11 implementation is complete in its pre-integration verification scope. |
| I10 | Implementation acceptance complete; no known adapter code gap. Productive caller/native/mutation checks and lint passed. Full live-host evidence remains I12/V08–V10; I11 sink parity was completed separately. |
| I11 | Implementation complete and compiled verified; no known producer/physical-sink gap remains. Broad baseline/environment failures, unavailable HAProxy C17 headers and I12/V10 live-host evidence are recorded separately. |
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
- [x] V08a: R17 supplies actual NGINX-H1 operation mappings and original 97/97 Required-PASS (14 YAML / 42 native / 10 config / 31 explicit derivations). Derivations are records, not additional requests; other hosts/profiles and broad V08 remain open.
- [ ] V09: Late Safe/Strict, pre/post-commit failures, client bytes, reset scope, neighboring streams and cleanup.
- [x] V09a: R17 preserves genuine Safe/Strict, native incomplete-read/abort and cleanup evidence, plus actual normal generic Strict curl exit 52 bound to its case/run/rule. This closes that measurement gap only; other profiles, neighboring streams and broad V09 remain open.
- [ ] V10: Actual route logs, invalid/oversized metadata, missing observations and failed physical sinks.
- [x] V10a: R17 has schema-valid original Canonical, 16 actual program completions all normal exit 0, exactly one First-Byte source writer exit 0, and 34 genuine curl pairs. This does not close every physical sink/log contract in broad V10.
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

## 4. Historical route-specific source/test inventory

This earlier table predates the separately completed I09/I10/I11 repairs.
Its propagation/caller/adapter entries are historical scope, not current open
product defects. The current remaining work is the fully bound I12 host index
above, including the actual physical lifecycle observations each ID requires.

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

## 2026-10-11 I09 code closure

Integrated evidence covers 33 compiled methods, Common C17 smoke, contracts 74, adoption 19, HAProxy 194, Traefik 86, lighttpd 178 and Go 56/30/21. Counts identify the individual suites, not a sum of unique cases. All 219 NGINX methods are accounted for: 180 completed before the original 1800s timeout and 39 resumed with exit 0; the original aggregate command remains a timeout. The historical I09 verification had no full HTX host-header build; the historical local I09 Vortex analysis returned Sonar 403, and a validator/documentation wording failure already present on the baseline was a separate validation limit. These historical results do not describe PR #406's current-head Cloud analysis. This changes neither I09 code findings nor open V06/V07 release checks or V08–V10 live proof. R16/R17 remain historical; no release/runtime PASS is inferred.
