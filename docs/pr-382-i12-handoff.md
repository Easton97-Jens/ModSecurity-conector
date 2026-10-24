# PR #382: I12 handoff after review remediation

**Language:** English | [Deutsch](pr-382-i12-handoff.de.md)

## Reduced I12 closeout, 2026-10-24

The current decision replaces the historical full-matrix campaign and its
retest/action items. The [concise closeout](pr-410-i12-closeout-20261024.md)
freezes [21 existing-evidence cases](../reports/testing/i12-closeout-20261024/frozen-selection.json)
across all 13 required profiles, below the 100-case ceiling. All 21 are
historical PASS evidence; applicability to current heads remains
`not_verified` because no new I12 campaign was run.

The [archive disposition](../reports/testing/i12-closeout-20261024/archive-disposition.json)
preserves the other 1463 original cases (37 configuration-only PASS and 1426
unqualified) and all 575 unresolved historical oracles without scheduling
follow-up work. The 100-case rule is a selection ceiling; automated global
inventory and enforcement remain `not_verified`. The policy base is
`42fd5a8e895aca3a36b09eb09fe5c7cf9c3399e3`, PR #382 remains at
`1eda4e99d1c60e79c5d3aff2caa7eabc83e61041`, and the PR #410 integration
checkpoint before these closeout files is
`73feabd05a10bb94d887530dd2e62cca7152ca0b`. The published head and automatic
gate state belong to PR #410. The later 2026-10-14 sections are retained as
historical evidence and no longer initiate work.

## Historical I12 lifecycle consolidation, 2026-10-14

State: **I12_PARTIAL** and independently **RELEASE_BLOCKED_SECRET_HISTORY**.
Both PRs remain Draft. The [current host report](pr-382-i12-host-evidence-20261014.md)
and [complete original index](pr-382-i12-missing-case-index-20261014.md)
bind physical packets, original contracts and hashes. Earlier sections below
describe only their historical checkpoints.

The unchanged selection contains 1484 original IDs: 1406 required and 78
diagnostic. There are 21 full required-case lifecycle PASS and 0 FAIL, with at
least one full case on each of 13/13 required route parts. Actual execution is
recorded for 151 original IDs. The 37 historical configuration PASS include 36
required cases; total qualified required PASS is 57, required FAIL is 0, and
1426 original IDs remain unqualified. Of the original 596 unresolved oracles,
21 are independently source-confirmed and actually retaken; 575 remain unresolved.
Original membership, null oracles, raw records and earlier failures are preserved.

The 21 full cases do not qualify all 1406 required IDs. Applicable host/native
EOS, MIME, finish/free, client/backend, handle and cleanup evidence is physically
measured for these packets; justified nonapplicability remains explicit.
Zero-byte append and client EOF do not replace native EOS evidence. Stock-native
control remains diagnostic, including its 23 originally unresolved oracles;
it was not broadly relabelled unsupported. Other required IDs, missing fixtures,
further limits, late/commit, sink failures, cancellation/reset and neighbor
cases remain open. I12/V08–V10 remain open overall.

[Private capture sources](../ci/runtime/lifecycle/i12/README.md) retain nine explicit variants. Each packet
binds actual source, loaded images, SDKs and configuration. Earlier a9/0275
builds remain distinct from current product/delivery revisions; source success
does not replace host execution.

Published #382 product head is `9980eb049dde0643da6a4f04e3b6712801b670b3`;
the normal #410 integration is `eca03db3`. The test-only follow-up replaces the
stale mapper400 assertion with typed dispatch/default500 and the separately
bounded headercount400 contract; all 38 requested contract tests and five
compiled mapper tests pass. New #382 CI is pending. The e47 Sonar SUCCESS
(check `116148729241`, Gate OK, Security A, new/accepted issues 0, hotspots 0,
duplication 0) remains historical evidence for e47 only, with no transfer to
9980 or #410. Remote #410 remains `02754040bced960cfc1857416cd7101bb3116ef4`
at this pre-push checkpoint; #410 source CI awaits Root push and fresh readback.
Historical Gitleaks remains a separate release blocker. No all-CI PASS, master
merge or release is asserted.


The extension includes four additional HAProxy body/header cases, two native
HAProxy request-limit cases at 16 bytes (`Reject` and `ProcessPartial`), and two
genuine lighttpd empty-body cases. Separate confirmed expectations and retakes
do not qualify siblings. Patched lighttpd records an actual null EOS argument
on its genuine empty-body branch and native P2 finalization without request append.

Apache preserves the original duplicate-header FAIL and original rule. A separate
hash/version-bound override follows actual Apache/APR merging into one header
value `one, two`, without product comma splitting. The 14 canonical host cases,
12 real APR/SDK regressions and full Root-reviewed Apache packet are separate
evidence. NGINX repair `12756aa957f54d3efce6bd97ec0dbac07fa576cc` propagates
internal mapper faults as HTTP500; actual HTTP500/client-HTTP400 retakes and
full case09 are separately bound. The earlier body-P2 versus injected-P1 scope
conflict remains preserved as a historical disposition.

Exactly three generators produce oracle reconciliation, the lifecycle ledger
and current EN/DE report with index. They preserve originals, the 596-member
subset and nulls. The native test observer records 38 wrappers plus an explicit
snapshot, typed handle associations and actual returns. The renderer binds the
37 historical configuration PASS to their unchanged physical original source
and rejects unsubstantiated PASS/scope/execution labels. Private hooks are
excluded from release artifacts.

Actually passed: 62 native/oracle/ledger/Apache tests, 13 renderer tests, 115
NGINX mutation tests, 77 guards, five compiled mapper tests, Root Quick06,
native contracts and Docs10. Capture checks passed nine variants, 45 patch
applications, 15 negative guards and five capture groups. The source-copy
receipt-overwrite correction rejects an existing receipt before any write and
creates it exclusively; three added controls preserve file/hardlink/directory
targets. The 150-object registry verifies; observer C/H and manifests are unchanged.
This is a functional source-copy guard, not a security scan. Root validates
the final combined documentation/source snapshot again after this handoff.

No deep security scan, gate weakening or guard weakening occurred. Framework/
MRTS gitlinks and original raw evidence remain unchanged. All earlier CR sections
and the immutable original index are preserved.

Root additionally approved 20 `HARNESS_DEFECT_CONFIRMED` supplemental
dispositions outside the original 596-member subset. Original generic catalog
exit 1 remains unchanged and is not treated as a direct-native or wrapper-driver
contract: actual waited native exits are 255 x 8, 78 x 9, 2 x 1 and 77 x 2.
These are process exits, not HTTP statuses; nine operations are parser-only and
eleven are service-startup failures. Nine physically empty sidecar stderr
first-causes remain NULL; source/config cause is separate. Scope-file cases
reject the Common Runtime unknown `phase4_content_types_file` key and do not
prove MIME/wildcard parser execution. Formal resolved expectation and retest
remain null; this produces no additional configuration or lifecycle PASS.
The different 29 historical original596 gaps and 23 Stock-native diagnostic
oracles remain unresolved; no new unsupported approval is inferred.

Disposition source: `catalog-conflicts/final-supplemental20/disposition-summary.json`,
SHA256 `d68c2535d5ece0990670b3e01f173df9d98ad26684fef1f7bf39ca37cc436021`.
Root-approved records15, oracle13 and ledger08 retain 21 resolved/575 unresolved,
21 full PASS, 13 routes, 151 executed, 37 configuration PASS, 57 required
qualified PASS and 1426 unqualified IDs. Actual Quick06 and Docs10 passed;
Root90 tests and SourceRoot05 passed with 150 source objects, nine variants,
45 patch applications and 15 guards. These remain distinct from pending hosted CI.

## Historical review checkpoint, 2026-10-13

The previous review task was **BLOCKED_FOR_I12** and did not rerun #410.
Its revision-specific observations follow; they are preserved as history.

The final delivered Parent SHA, exact-head CI/Sonar/review results and normal
commit IDs are recorded in the current [PR #382 description](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382).
Do not substitute this document's starting revision or any historical run for
that delivery binding. The local delivery ledger is retained under
`/var/tmp/codex/ModSecurity-conector/runs/pr382-review-20261013`.

| Revision | Binding |
| --- | --- |
| Remediation starting Parent | `4639f982a8125f4150394e4d4f2e8af4e690f494` |
| Master at task start | `6aae115fff8531eb1e08a4b10745d7ae93550124` |
| Framework, unchanged gitlink | `99a7985c1be92a2297b1b59208f64df6768f2cbf` |
| MRTS, unchanged nested gitlink | `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |
| Historical #410 head | `511c4ac4515f0e515f68b3bbc38274c5a230d903` |

The [consolidated Change Record](../reports/audits/change-records/CR-20261013-pr382-consolidated.md)
retains the 122 original Change IDs and immutable detailed evidence. I09/I10/I11
and engine-owned inspection limits remain implementation contracts; they do
not replace I12 host proof.

The independent Gitleaks PR-range scan still identifies two prose false
positives in published commits: `generic-api-key` in
`docs/pr-382-event-contract.md` at `91f07e124fe09056dc46dc59d65693f406b4b1a1`
and `docs/pr-382-i09-route-audit.de.md` at
`492663334d89428dce084792145ef94e91579788`. Current prose is corrected;
an append-only commit cannot remove historical matches. There are no scanner
exceptions, narrowed scan inputs or historical rewrites. No credential value
is reproduced. A separate user decision is required before any historical
remediation; the failing independent check prevents READY_FOR_I12.

The local Go repair uses central version 1.27.2 and four module minima
1.26.9. Only necessary Envoy requirements move to `x/net` 0.61.0, `x/sys` 0.49.0
and `x/text` 0.43.0; grpc 1.83.2/protobuf 1.36.11 remain unchanged. Four module
checks including race/govulncheck, 71 updater/workflow tests and actionlint pass
locally. OSV reports zero new pairs against the starting baseline, but three
remaining graph-only baseline pairs covering two advisories in unused SDK/openpgp
paths; this does not establish zero OSV findings. `GO_UPDATER_FIXED_IN_PR`
requires final PR verification and is not asserted at this local checkpoint.
**MASTER_WORKFLOW_VERIFIED: NOT_EXECUTED**: master run `38370968157` remains the
original failing run. Following a separately authorized integration, the trusted
master updater must actually run again; read-only PR candidate validation does
not replace that execution.

Before a new I12 campaign, obtain terminal passing Parent checks on the exact
integrated SHA, strict Sonar zero/duplication gates, independent secret scan
exit 0 and fresh Codex/security reviews with no confirmed unresolved P1/P2.
Match local HEAD, remote branch and PR head; retain their complete SHAs and
all check/run URLs. Do not reuse an earlier green result after a new push.

For #410, reconcile both language versions of the checklist and remaining-work
matrix against the current I09/I10/I11 and body-policy contracts. Retain its
historical I12 report and original raw bundles unchanged. Fold its proposed
Change Record into the consolidated record instead of restoring the removed
record collection. Its old 79 records (9 PASS, 6 FAIL, 53 BLOCKED,
11 NOT_EXECUTED) describe their original tested product only. #410 is currently
merge-conflicted; resolving it and updating its tested revision is separate work.

Re-execute I12/V08–V10 on the actually integrated product, keeping ten profiles
and fourteen route legs independently bound: Apache native; NGINX native;
HAProxy HTX and SPOP/response companion; Envoy ext_proc and
ext_authz/response observer; Traefik native UDS and forwardAuth/response
observer; lighttpd Stock sidecar, diagnostic Stock native control and patched
native. Preserve unsupported modes as unsupported. The Stock native control
does not gain body hooks; patched lighttpd Strict abort remains unproven.

Each applicable leg needs fresh native rule and technical-error cases,
Off/Safe/Strict behavior, request/response body chunks, EOS and MIME selection,
pre/postcommit status and actual host action, early/late write failures,
abort/reset and neighboring/follow-up health, physical event-sink failures,
once-only finish/cleanup and original client/transport/log receipts. Recheck
native Reject/ProcessPartial and markers beyond the former body cap. Keep
bounded authorization samples and SPOP framing distinct from inspection limits.
Include Stock private spool permissions, technical admission/exhaustion and
readmission without a BODY_LIMIT event.

Actual hosts, pinned native libraries/modules, private ports and runtime paths,
matching service UIDs and writable private spool storage are prerequisites.
The local namespace maps only UID 0 (`0 0 1`): the added real nonroot startup
test is BLOCKED, while root profile readiness and injected ownership/read-only
controls are separate evidence. Regular-file allocation calls cannot be
cancelled by socket deadlines; isolate unrelated filesystem writers with a
dedicated filesystem or quotas when that guarantee is required.

Retest the historically reported Stock-RST empty-event and Common lossy-event
failures on the new exact revision; do not relabel them as current failures
or passes without execution. Historical Apache/HAProxy broad-suite failures,
UID/mount restrictions and R16/R17 source-bound results remain in the immutable
records. Preserve their raw evidence roots and checksum ledgers. The current
task performs focused remediation tests and Parent CI, **not the full I12 matrix**.
