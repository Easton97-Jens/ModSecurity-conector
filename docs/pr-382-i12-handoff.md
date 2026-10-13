# PR #382: I12 handoff after review remediation

**Language:** English | [Deutsch](pr-382-i12-handoff.de.md)

Date: 2026-10-13. State: **BLOCKED_FOR_I12**. PR #382 remains Draft;
PR #410 is neither merged nor rerun by this task.

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
