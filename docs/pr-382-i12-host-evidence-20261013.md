# PR #382 / #410: current I12 host evidence, 2026-10-13

**Language:** English | [Deutsch](pr-382-i12-host-evidence-20261013.de.md)

**I12_PARTIAL.** Actual isolated hosts were executed again; no required route
has complete I12/V08–V10 acceptance. The current host observations, failed
attempts and missing requirements are retained independently of the
[historical report](pr-382-i12-host-evidence-20261011.md). I12 and V08–V10
remain unchecked; both existing PRs remain Draft.

## Source and evidence identity

The task run is
`/var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion`
(abbreviated `RUN` below). These are retained local files, not public download
links. The old run `20261011T063350Z-0df51024008f-i12` was rehashed: all
85,108 entries match its original manifest
`6672a248716967976992b1d972207c2ad26f51cf2e471f9ccfcacb1e0ed8d124`.
Its 79 selected records remain 9 PASS, 6 FAIL, 53 BLOCKED and 11 NOT_EXECUTED.
Those historical statuses are unchanged.

| Identity | Actual scope |
| --- | --- |
| Starting Parent | `8c574cdf86f10af976297c31d31485b042eba73b` |
| Final published Parent | `a9d48bb58aa948aea7d79e20cdf09d3f239b7808`; actual HAProxy e2445 and Envoy6175 run identities plus scoped source equality below |
| Earlier campaign host inputs | Genuine `5939dce7a4cb3572b0244c159e4f98d0b1c28040` snapshot; patched/control inputs are genuine `b982c6f35abc47eccddcfded2bfd920f92516d90` |
| Original native/bridge build producer | `8c574cdf86f10af976297c31d31485b042eba73b`; preserved in each artifact manifest |
| Framework | `99a7985c1be92a2297b1b59208f64df6768f2cbf`; source and gitlink unchanged |
| MRTS | `8a6bb546c4c81d8ffc7be801dceac60c6925685f`; pinned, not executed or modified |
| Starting/current master | `6aae115fff8531eb1e08a4b10745d7ae93550124`; no integration performed |
| libModSecurity | 3.0.14, SHA256 `32257230b8f378987ba1204049dcc1e23927fd44c8778e09d41805ad705c3407`; library source commit unavailable |
| Hosts | Apache 2.4.66; NGINX 1.31.6; HAProxy 3.2.25; Envoy 1.39.1; Traefik 3.7.13; lighttpd 1.4.85 |
| Toolchain | GCC/G++ 15.2.0; Make 4.4.1; Go 1.27.2; task Python 3.14.7 / PyYAML 6.0.3 |

`parent-final-product-equivalence.json`, SHA256
`3adab3818e1b4f5051e4f9ead4cdf3f1061a6473f7963cfe2d2dd9eb7c0c365c`,
verifies 531 selected product/runtime Git objects between the original 5939
runtime and dffac. Only tests and documentation differ. This receipt preserves
the original run identity; it does not relabel a run or prove host behavior.
The later Common/HAProxy runtime corrections invalidate this receipt for an
overall final-source equivalence claim. All older runs keep their actual
source/build identities. HAProxy and Envoy were genuinely rebuilt from e2445
and 6175 respectively; scoped input comparisons to final a9 are recorded below.
blocked host setups and other bounded observations retain their original
revision, without promotion to final-head acceptance.

## Required matrix and counting rules

Before host launches, capabilities, checked-in Framework fixtures, native
operations and explicit historical/user obligations were selected for H1.
`case-catalog/selected-01/selection.json` retains **1,406 required obligations**
and **78 diagnostic obligations**, with all exclusions and their reasons.
These are requirement IDs, not a count of HTTP requests. A runner probe,
readiness request, component test or retry is not automatically a qualified
canonical case. `final-reconciliation/` preserves every selected ID and the
actual runner observations separately. Missing native counters, backend
ledgers, causal mapping or transport observations remain `null` with reasons.

| Required leg | Obligations | New real host scope | Full acceptance |
| --- | ---: | --- | --- |
| `apache-native` | 155 | 27 bounded transactions; corrected recovery rerun | PARTIAL; lifecycle/MIME/EOS proof and 128 further obligations missing |
| `nginx-native` | 140 | Two preserved 60-case batches stop before host/client execution | BLOCKED_ENVIRONMENT; ownership/traversal prerequisite |
| `haproxy-native-htx` | 112 | Eight freshly rebuilt e2445 direct HTX probes pass | PARTIAL; full independent lifecycle/framing/physical-sink matrix missing |
| `haproxy-spop-request` | 94 | 51 incomplete request-fixture cases; six combined probes | PARTIAL; incomplete fixture separated from real companion evidence |
| `haproxy-spop-htx-response-companion` | 72 | Six freshly rebuilt e2445 combined probes pass; earlier errors preserved | PARTIAL; bounded result does not fill full lifecycle/transport proof |
| `envoy-ext-proc` | 117 | Ten distinct functional probes and two transport diagnostics | PARTIAL; full backend/native cleanup counters missing |
| `envoy-ext-authz-request` | 94 | Two real allow/deny probes | PARTIAL; full hostbuffer/native-limit/ledger matrix missing |
| `envoy-ext-authz-response-companion` | 73 | Two separate P3/P4 companion probes | PARTIAL; Strict/reentry/lease and full lifecycle proof missing |
| `traefik-native-uds` | 118 | No current host started | BLOCKED_ENVIRONMENT; compiler subprocess and writable plugin staging |
| `traefik-forwardauth-request` | 93 | No current host started | BLOCKED_ENVIRONMENT; checked-in observer setup requires Go |
| `traefik-forwardauth-response-companion` | 69 | No current host started | BLOCKED_ENVIRONMENT; checked-in observer setup requires Go |
| `lighttpd-stock-sidecar` | 153 | Seven final real-host cases, eight extra profile controls, 17 separate component checks | PARTIAL; full producer provenance and physical lifecycle counters missing |
| `lighttpd-patched-native` | 116 | Two real P1 compatibility controls | PARTIAL; full namespace launcher/P2 configuration blocked |
| Diagnostic `lighttpd-stock-native-control` | 78 | Two real P1 controls using a genuine Stock-compatible module | Separate PARTIAL diagnostic; no native body-hook capability claim |

No required leg is fully PASS. The complete missing-ID/reason inventory is in
the [generated missing-case index](pr-382-i12-missing-case-index-20261013.md)
and `final-reconciliation/requirements.json`.
Raw runner exits and their narrower PASS counts are reported below; they do
not change the requirement denominator or fill absent observations.

The sealed reconciliation retains 123 distinct runner fixture IDs, excluding
retries, readiness, follow-ups and shared request/response identities. Semantic
uniqueness remains null because effective fixture equivalence is unproven;
the exact fully mapped canonical execution count is also unknown. Qualified
canonical PASS/FAIL counts are 0/0; missing qualification statuses are
420 BLOCKED_ENVIRONMENT and 1,064 NOT_EXECUTED_UNQUALIFIED. These counts do not
mean no actual traffic. The index pair preserves all 1,484 missing IDs once each.
`final-reconciliation/summary.json` SHA256 is
`78e6985a83ba70d4f1dc83dfbcfbba2e459eb192a7b61d69c05bbb016f8ddac6`;
35 original source hashes were independently checked. `final=true` seals the
reconciliation and does not mean I12 acceptance.

## Apache and NGINX

Apache attempt `1791916326230218540` has 27 actual native transactions,
controller/candidate exit 0, no surviving process or mount, and one observed
`msc_transaction_cleanup` enter/return pair per transaction. Allow is 200;
P1/P2 deny are 403/backend 0; P3 deny is 403/backend 1; redirect is 302;
Safe late is 200/curl 0; Strict and technical postcommit errors retain 200
with curl 18. Physical closed-FD and `/dev/full` errors are visible in the
original Apache error log. All five mandatory sink failures return technical
500/backend 0. The diagnostic writer fails before the later disruptive rule;
the old 403 oracle was incorrect. No product change was needed.

The response-limit Reject recovery controls originally sent ten bytes against
an eight-byte native limit. Their legitimate 403 results were fixture errors.
Fresh attempt `1791916546816730611` uses three-byte controls: main 403/backend 1,
follow-up and neighbor 200/backend 1, complete framing and clean shutdown.
The final 27 bounded mechanical controls match; all 27 remain BLOCKED for full
lifecycle acceptance because Common finish, physical EOS and MIME observations
are missing. `apache-current-host-v2/summary.json` SHA256 is
`fcaf4dda8482b6d7378de78632d42da12ac71a425ca69fb99c0dee5352ada791`.
The unchanged Apache module SHA256 is
`908c9e7a7062ada3e36499a69e2c41e17791a36021d5872d0981bfc5864bb5d0`.

NGINX's current binary/module provenance is established, but current local
host acceptance is blocked. Attempt `1791916064021781516` marks all 60 planned
operations NOT_EXECUTABLE because the spec placed the harness outside
`BUILD_ROOT`. Corrected attempt `1791916436174006544` reaches the harness but
fails its worker-directory preparation before HTTP/configtest: it performs
`chown nobody` followed by `chmod`, under the admitted CHOWN/SETUID/SETGID mask
`0xc1`. The latter operation returns EPERM; private ancestor traversal is also
unavailable. These are setup failures, not observed product FAILs. Both
attempts retain clean outside cleanup. The required root/nobody environment
must support the checked-in ownership/traversal contract; no extra capability
was granted. Historical R16/R17 and hosted CI remain separate evidence scopes.
NGINX binary SHA256 is
`b39012fa2158408c55d8506ac1b1254fc712dd471a6137e64264fa42a0504384`;
module SHA256 is
`8c807a5ff55d93af63542050928e0158f2c8ec965bb46dba8ec232935f552efe`.

## HAProxy

Direct HTX attempt `1791916380864162400` observes eight expected functional
results, including empty request/response EOS controls and synchronized P4
Safe/log-only. Full physical API/destructor/framing and required-case evidence
is absent. The original SPOP-only fixture executes 51 rows: 42 driver exits 0,
nine exits 1; the nine expected-Allow controls receive 503 because their
mandatory response companion is absent. Those results are preserved as an
incomplete fixture, not silently promoted or attributed to a product bug.

The combined runner now accepts an explicit pair of prepared binaries only
with actual binary/library hashes, version and current production-source
object proof. The original build route remains available. Seventeen focused
tests, shell syntax and diff checks pass. Attempt `1791917296154368188` executes
six combined probes/seven HTTP requests, controller and driver 0, clean
shutdown. The old runner's HTTP-only PASS missed actual errors: P3-deny403
then fails outcome acknowledgement; P4-Safe200 and connection reuse fail
terminal cleanup, with physical connector/protocol error records. These
original observations remain immutable. Diagnosis, fix and newly built host
retest are recorded in the final revision/evidence section below.
`hosts-haproxy-prepared-01/SHA256SUMS` SHA256 is
`f593c9ee648eee9e2f9bb27aeeeddacc00156fe9da0f8cd15a1750a428af36e2`;
all 2,045 entries were checked.

Native terminal-outcome, P3 completion and SPOP phase-conversion defects were
reproduced and corrected. Commit `a30fd5e414b35b990355e04fda148dfae7514c21`
allows actual Host OUTCOME after valid native terminal policy decisions, while
preserving technical/logging errors. Its genuine rebuilt retest
`1791918602525320691` passes eight direct HTX controls, then stops at a residual
P3 SPOP `connector_error`; the failed attempt is retained. Successful P3 cleanup
called typed CANCEL because normal RELEASE required P4 EOS.
Common completion commit `6175a30d94de66f349c11eb8164b28942e040457` permits existing MRC1
RELEASE after an acknowledged matching disruptive precommit P3 OUTCOME; HTX
now performs OUTCOME→RELEASE→close. EOS is not fabricated. Allow/log-only,
mismatched outcomes and technical cancellation remain guarded. Genuine native
client/server tests and four mutation controls, three caller checks, six build
contracts and 18 response-handle checks pass. The compiler-prefix path also
passes with `CC='env cc'`. The native validation receipt SHA256 is
`73ccabd26af1514570e9f7327812e71c825be858067aed5ce9a47599bf6d2454`.

Its genuine rebuilt attempt `1791920706986259057` again passes eight direct
controls but fails combined P3 cleanup: the productive SPOP conversion resets
the native decision phase to Common CONNECTION. The RELEASE guard correctly
rejects a decision lacking P3 metadata. Final commit
`e2445c781eded55e006f114e981ef841872eb74e` explicitly maps native phases to
named Common phases after Allow/Deny/Redirect constructors. The guard is
unchanged. The productive caller's six P3/P4 decision variants and all nine
binding tests pass; omission and numeric-cast mutations compile then fail the
phase assertion. Genuine C17/`-Werror` SPOP build passes. Receipt SHA256:
`2e197b9168aacb8e164771b3eae7e0954ffa1cd53f8f908f7c4e91b25813c6f3`.
The failed 6175 run's 12,080 artifact hashes verify, manifest
`7ac95c5fc3208b4becc301d0c7814eec530a4e84e08c355d319bcc884920d5ab`.

Final genuine e2445 SPOP/HTX builds both exit 0. Regular attempt
`1791921462735406083` passes eight direct HTX and six combined probes; separate
explicit ResponseBodyLimit10/Reject attempt `1791921552453068894` passes six
combined variant probes. Normal physical connector/protocol errors are absent
after service reaping; the missing-correlation negative is retained. Both
controllers confirm no surviving process or outside mount. P4 in the native
limit variant observes requested deny/actual log_only, client200/full 23 bytes;
raw native-limit/API return and causal rule ID remain null. These six configured
variants are separate observations, not six additional qualified requirements.
HTX binary SHA256 is
`e04d068da23906adf68b9f52019db7be4e8051d6cf10ca9e2ecd080fea17cc20`;
SPOP binary SHA256 is
`030f667437964be54655637c7f35751342911efe8cdc2c2da167432e665a30f1`.
All 12,247 artifact hashes verify against manifest
`86073b3fd2ab27d23d75c0c99d756b52e260d147d5995e8c5f8c5ec4fa224e53`.
Packets are under `hosts-haproxy-postfix-01/retry-03/`; native physical API/EOS/
destructor counters and independent numeric per-client exit receipts still
prevent full I12 acceptance.

## Envoy and Traefik

Envoy ext_proc's original body-limit oracle expected 413. The actual native
engine decision and real host return 403 for the explicit Reject fixture;
the native CGo regression independently agrees. Only the oracle was corrected.
Fresh attempt `1791916687448257248` passes ten functional probes: streamed
allow, P1/P2/native-limit deny, P3 deny/redirect, P4-only and synchronized Safe
late response with recovery. Two cancellation/recovery diagnostics remain
narrowly scoped; cancellation attribution is `grpc_context_canceled_unattributed`,
not an independently established downstream Strict abort.

Request-only ext_authz attempt `1791916573908703091` observes allow200/deny403.
Combined attempt `1791916466421772127` independently observes P3deny403 and
P4Safe200/log_only. The request native event's empty actual action is retained;
the client separately sees 403. Missing native counters/full backend ledgers
and Strict/reentry/lease cases keep all three legs partial.
`hosts-envoy-traefik-01/SHA256SUMS` SHA256 is
`d79696f7df3916d375659668b6722ee2f3d1d39ef065cb84e422ccdd2df28aa6`;
all 2,010 entries were checked.

All three Envoy legs were genuinely rebuilt from
`6175a30d94de66f349c11eb8164b28942e040457` and actually rerun: request
`1791920841266999968`, companion `1791920756422928567`, ext_proc
`1791920898020674821`. All bounded runner/controller results are exit 0 with
UID/GID 65534, capabilities 0 and independently clean outside cleanup.
Fourteen distinct functional probes plus two diagnostics pass; repeated
request/readiness controls are excluded from that count. Both builds actually
compile all 63 shared Common C units, including the changed MRC1 files.
New binary hashes are ext_authz
`67a93560bf30f9e0197fb25addc956bbcc282d71b9ebb6da15a8eb0463b5a9b2`,
response observer `e21535607f739a8346d513541c05146bb769680332d600d3bb3fa000c583936d`
and ext_proc `67f0f832f76fb68abb1489c9e27ecf9770841b0f3911e767a3a441fc42675b13`.
All 4,005 acceptance-artifact hashes verify; manifest
`53d5b3d458007f01a2ac2105dc2c78e946210bf14cf88da65f052adac0eedef7`.
The later e2445 correction changes only HAProxy product source. The scoped
172-input Envoy Git-object comparison is equal, receipt SHA256
`da0fd519cc921568b1bc04cc02746a246b4c0f0f09bed1b67506fabafed7b4dc`.
Actual build/run identities remain 6175; no full Parent equivalence or missing
lifecycle/Strict evidence is inferred.

Traefik native attempt `1791916290959447432` stops in the checked-in engine
rebuild because `cc1` is absent from the fixed namespace. Read-only plugin
staging also causes an explicitly failed local cleanup receipt. No Traefik
host starts; outside cleanup is independently clean. ForwardAuth request
`1791916630354113595` and response `1791916513884787401` each stop before host
start because their checked-in response-observer setup requires the Go
toolchain. These are separate environment blocks. Eighteen genuine C/UDS
component subcases with race detection and an EOS-loss mutation are separate
evidence; they do not reproduce or erase the historical real-host
`protocol_error`.

## lighttpd

Final Stock attempt `1791916820945011803` passes seven real-host cases:
full/empty allow200, P1deny451, P2deny418, native P2-limit403, P3deny422 and
P4Safe200/log_only. Actual client bytes/hash/framing, independent Stock access
counts, same-transaction physical events and reaped listener processes are
retained. The original empty `actual_action` before host observation remains
valid; a separate observed event is mandatory. The historical enum rejection,
wrong 413/native-limit event oracle, Safe event identity and accepted-request
byte snapshot were repaired in the harness, without inventing an action.
Twenty-eight harness tests pass with one explicit native-SDK skip; 17
separately executed nonroot native component regressions pass without skips.
Eight additional real-host profile/native Reject/ProcessPartial controls pass.
Strict's logical HARD_ABORT_AFTER_200 is not promoted to a physical abort: the
client received the complete 200 body and independent TCP-abort evidence is null.
The full producer still lacks the unchanged Stock-host provenance contract and
physical EOS/destructor counters. `stock-current-host-01/final-report.json`
SHA256 is `27e4657f1087d679cf7885fa35223df6b0dc8b7608796711426b33b69b1d0f80`;
`HANDOFF.json` SHA256 is
`ef8736fce9b254b29e61917bd3a96d625c367b4121964ab17c842e8751d8c7a0`.

Patched lighttpd's full unchanged namespace launcher fails with `unshare`
EPERM before host start in `1791916879454169505`. A separate P2 gate rejects
the descriptor-bound `/proc/self/fd/5/events.jsonl` path during configuration,
before requests. Compatibility attempt `1791917197697716188` nevertheless
executes real native P1 allow200/deny403 with the genuine patched module.
No native body/Strict capability is inferred. Genuine Stock diagnostic attempt
`1791917386284085054` independently passes two P1 controls using a newly built
Stock-compatible module, SHA256
`560b541c6808035cb8c137cdfec3a3d430d546eb85dfdd8b7791c7627d32c77b`.
The patched ABI was not substituted. All attempts have clean outside cleanup.
`hosts-lighttpd-patched-01/summary.json` SHA256 is
`e8d1761d1b0f21d13fba79c2a6a07bab987d071f430e98f1aa05625ec1a631e8`.

## Validation and security scope

Observed local checks include `make quick-check` (exit 0, 181.916 seconds),
I09/I10 (exit 0, 294.683 seconds), Common C17/memory/flow/adapter and physical
Apache/SPOP sink contracts (exit 0), the 14-method genuine native body suite,
native Envoy/Traefik and Go/race/vet checks, mutations, workflow lint, EN/DE,
links, Change Record and whitespace. Earlier failed prerequisite attempts
remain in `verification/`; current result receipts identify the tested tree.
Final changed-path validations are retained in
`verification/final-evidence-02/results.json`; exact-head remote readbacks are
in the PR descriptions and external delivery ledger.
Native/component checks establish their own layer only.

At exact 6175, fresh `make quick-check` exits0 in 228.719 seconds and the combined
I09/I10/native body suite (now 15 methods) exits0 in 413.912 seconds. The earlier
a30 aggregate's Envoy Go failure was a too-long task TMPDIR for UDS; the
unchanged test passes using a short external path. The failed attempt remains.
At e2445, the changed native SPOP nine-test suite and genuine product build
pass; the unchanged Off/Safe/Strict HTX caller assertions and 15 mutation controls
pass in 18.816 seconds after the coherent complexity-helper refactor. PR410's
17 HAProxy harness checks and 28 Stock checks pass with one explicit native-SDK
setup skip; 24 Envoy receipt/verifier checks pass. Separate real native Stock
checks are unskipped. These are layer-specific validation results.
The task interpreter is 3.14.7; the separate Framework exact 3.14.8 interpreter
gate was not verified locally. No environment gate is inferred from unit success.

Final a9d48 is a test-only status-table/Change Record follow-up. Its two
productive SPOP/mutation checks pass in 16.406 seconds. The 829 selected Git
objects under Common/connectors/Makefile/ci/workflows/modules match e2445;
`parent-a9-final-input-equivalence.json` SHA256 is
`1ac6bb430bfd2a4739cad1d3f25e7b07c5dbb6a06621362c0039c26b619bccad`.
This preserves the genuine e2445/6175 run identities and proves unchanged
selected inputs only. An independent bounded final code review finds no
actionable correctness issue in the phase correction or caller extraction.
Provider reviews remain historical as stated below.

The user's later instruction limits security depth. TAC advisory was checked
as `tac1/granted`; it is not treated as blanket authorization for a deep scan.
No further deep scan or security-review trigger is used. The already required
sanitized pinned Gitleaks 8.30.1 evidence remains visible: current blobs/new
task commits pass, while the full original PR range fails on exactly two
historical prose matches. Values are not reproduced, scanner rules are not
suppressed and history is not rewritten. This release gate remains failed.
Previously submitted Codex reviews target `4639f982a8`, not the final head;
their three threads are resolved, but there is no current-head review claim.

## Reproduction, delivery and remaining decisions

Run-specific specs preserve exact argv/cwd, source/config hashes, host binaries,
UID/GID, client exits/signals, raw native logs and cleanup. The common execution
entry is:

```sh
rtk proxy /usr/local/bin/python3 RUN/isolation/private-runtime.py SPEC
```

Replace `RUN` and `SPEC` with their exact absolute values. Representative specs
are `apache-current-host-v2-retry/host-spec.json`,
`hosts-envoy-traefik-01/envoy-ext-proc-fixed-harness.json`,
`hosts-haproxy-prepared-01/spec.json` and the files named in
`hosts-lighttpd-patched-01/HANDOFF.md`. Original controller results preserve
candidate/driver statuses and independently observed outside cleanup.

Final HAProxy specs are `hosts-haproxy-postfix-01/retry-03/spec.json` and
`response-reject-variant/spec.json`; final Envoy specs are
`hosts-envoy-final-01/authz-request.json`, `authz-response.json` and
`ext-proc.json`. The generated missing-ID indexes are exact copies of
`final-reconciliation/pr-382-i12-missing-case-index-20261013.md` and `.de.md`,
SHA256 `cf707a2ec7c4d154b98de5384806c6dff1501ba564902a82bc07a350a4eb6f80`
and `7b7e0aade918b2c645dd4552aa78a44cc1376b9aa5415419d6fc9c8915e8311a`.
Regenerate through `rtk proxy python3 RUN/final-reconciliation/reconcile.py`;
generator SHA256 is `7ba941ff929afd91a84498c8eddfb92c4f70a903aea2c47a7245f95f9f86226e`.
Raw JSON, configs, builds and private TLS material remain outside source control.

The existing #410 branch retains old head
`511c4ac4515f0e515f68b3bbc38274c5a230d903` in ordinary merge ancestry.
Only scoped I12 harness/tests/evidence/docs differ from the current Parent.
The [consolidated Change Record](../reports/audits/change-records/CR-20261013-pr382-consolidated.md)
is updated without restoring redundant records. Final Parent/evidence SHAs,
remote equality and current CI/Sonar/secret/review readbacks are maintained in
the PR descriptions and external delivery ledger. PR410 remains Draft.

Full acceptance needs permitted environments satisfying the unchanged NGINX,
Traefik and patched-lighttpd launcher prerequisites, complete physical
lifecycle/correlation/transport producers and the unexecuted selected
requirements. Historical secret-range remediation needs a separate explicit
decision. I12 cannot be checked from bounded smoke success or CI alone.
