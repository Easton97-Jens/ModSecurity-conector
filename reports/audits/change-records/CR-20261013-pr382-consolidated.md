# Change Record: PR #382 consolidated history and review remediation

**Language:** English | [Deutsch](CR-20261013-pr382-consolidated.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261013-pr382-consolidated` |
| Date (UTC) | `2026-10-13` |
| Base revision | `4639f982a8125f4150394e4d4f2e8af4e690f494` |
| Pull request | [#382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

## Motivation and problem statement

The user requested one compact account of PR #382 instead of 244 added Change
Record files (122 EN/DE pairs; 1,480,067 bytes). This pair preserves their
identities and immutable originals; all 176 master-owned record files remain
unchanged. It also records current review remediation and the Go security
update without creating further Change Records.

## Acceptance criteria

Preserve every historical identity, base and result; repair the three reviewed
product paths and eight Sonar source findings without weakening I09/I10/I11,
engine-owned body limits, tests or gates. Validate the four Go modules and
bounded updater with Go 1.27.2. Final delivery requires exact-head CI, strict
Sonar gates and fresh reviews. The independent historical secret-scan failure
still prevents full acceptance and READY_FOR_I12.

## Implementation decision and rationale

The original texts remain at `4639f982a8125f4150394e4d4f2e8af4e690f494`. Each
numbered index link retains an original language file and Change ID. Bases are
copied literally, including historical short/invalid values; neither bases nor
R16/R17 results are rebound to this remediation.

Historical work covers native result/error/event ownership, fourteen adapter
legs and physical sinks, NGINX evidence and integration/quality. Their detailed
failures, skips, timeouts, baselines and subsequent fixes remain in the originals.
I09/I10/I11 implementation acceptance is distinct from I12 live-host proof.
Native engine inspection limits remain effective; connector resource failures
remain technical errors, rather than fabricated rule/BODY_LIMIT events.

Current changes address these concrete triggers:

- Stock lighttpd profiles now select explicit private spool paths. A launcher
  selects only a shipped profile and executes the fixed installed native
  component through a validated descriptor, without arbitrary binary/argv-file
  inputs. It validates/provisions service-owned 0700 directories. Admission uses a shared
  256 MiB spool budget and 64 MiB filesystem free reserve, full allocation and
  checked arithmetic; exhaustion returns technical 503 before upstream contact.
  Reservations last until the unlinked 0600 descriptor closes. One directory
  cannot host two sidecars that bypass the shared budget.
- Traefik records actual response commitment and the first write error before
  fallible acknowledgment. A failed acknowledgment cannot cause a second
  response or overwrite the first cause.
- Named private C field groups and bounded diagnostic-buffer parameters repair
  the eight Sonar source findings while preserving checked opaque layouts,
  offsets and ownership. The unused runtime-smoke helper parameter is removed.
- Envoy socket startup binds beneath the pinned private directory descriptor,
  pins its own socket and publishes without replacing an existing pathname.
  Once-only cleanup preserves replacement files/sockets/symlinks. Deterministic
  replacement, descriptor/error and repeated race tests protect this boundary.
  Capacity-test synchronization and Traefik's fake-observer shutdown join
  remove test races while retaining failure assertions.
- The central Go version is 1.27.2; all four module minima are 1.26.9. Envoy uses
  `golang.org/x/net` 0.61.0, `golang.org/x/sys` 0.49.0 and
  `golang.org/x/text` 0.43.0. `google.golang.org/grpc` 1.83.2 and
  `google.golang.org/protobuf` 1.36.11 remain unchanged. The updater can repair
  approved security requirements without a grpc bump, verifies checksums and
  bounded file deltas, and preserves trusted master-only publication. A separate
  read-only PR candidate workflow validates all four modules.

## Changed files

The 244 indexed PR-only record files are replaced by this pair; archive README
and current documentation links are reconciled. Product changes are confined
to `connectors/lighttpd`, `connectors/traefik`, `connectors/envoy`, `common`,
`connectors/haproxy` and `connectors/nginx`, with their focused tests/fixtures.
Go changes cover the central lock, `.go-version`, four `go.mod` files, Envoy
`go.sum`, updater and candidate workflows/tests. Configuration references and
compiler guides are regenerated through their source generators; corresponding
EN/DE connector, build and PR documents are updated. Framework/MRTS source and
both gitlinks remain unchanged.

## Commands executed

Evidence below binds to starting Parent
`4639f982a8125f4150394e4d4f2e8af4e690f494` plus the task working-tree changes.
It is local evidence, not an attestation of an as-yet-unread final remote SHA.
Exact wrapped commands, environments, logs and exits are retained under
`/var/tmp/codex/ModSecurity-conector/runs/pr382-review-20261013`.

`rtk proxy python3 ci/tools/new-change-record.py create --name pr382-consolidated --base-revision 4639f982a8125f4150394e4d4f2e8af4e690f494 --date 2026-10-13` exited 0.

### Current review-remediation evidence

| Check / evidence | Observed result and boundary |
| --- | --- |
| Four modules: `rtk proxy go mod tidy -diff`; `go mod verify`; `go test -mod=readonly -count=1 ./...`; `go test -race -mod=readonly -count=1 ./...`; `go vet -mod=readonly ./...`; `go build -mod=readonly ./...`; `govulncheck ./...` (each through `rtk proxy`) | All 28 checks exit 0 with Go 1.27.2; `go-final/*.json` retains module-specific commands. |
| Updater/version/workflow unit suite; actionlint on both Go workflows | 71 tests pass; both workflow checks exit 0; `go-updater/validation-summary.json`. |
| `rtk proxy make quick-check`; native Traefik targets; native events/body suite | Exit 0; `root-validation/{quick-check,traefik-native,native-events-body}.json`. |
| `rtk proxy make check-i09-native-routes check-i10-adapter-errors check-apache-event-sink check-haproxy-spop-event-sink check-apache-native-response-limit check-common-helpers-c17 check-http-authorization-service-timeout`; `rtk proxy make -C connectors/envoy test-envoy-ext-proc` | Both final runs exit 0; Parent Python and external build/cache/short socket paths are recorded in the runner. |
| Stock sidecar suite | Closed-launcher follow-up: 44 PASS, one real nonroot startup BLOCKED by UID namespace mapping `0 0 1`; no nonroot runtime PASS is inferred. |
| Config-reference/all-example tests and generated-reference check; compiler-guide contracts | Exit 0; 22 compiler-guide tests pass; generator output is current. |
| Compiled C/route/mutation checks and private layout comparison | Focused acceptance passes; opaque size/alignment/offsets unchanged, including NGINX sanity configurations; `sonar/` evidence. Final native aggregate/Envoy reruns pass: `root-validation/{native-i09-i10-sinks,envoy-native}.json`, exit 0 (234.759 / 14.283 seconds). |
| Independent Gitleaks 8.30.1 PR-range scan | Exit 1, two historical prose false positives; current docs-directory scan exits 0. No suppression or narrowed PR scan. |
| Official OSV graph comparison | Old head: 25 module/advisory pairs; current: three pairs, 22 removed, zero new. Remaining pairs cover unused OpenTelemetry SDK exporter and `x/crypto/openpgp` paths; all four govulncheck runs report no reachable vulnerabilities. This is not an OSV zero-findings claim. |

Earlier aggregate failures and their subsequent fixes remain separate run
attempts; they are not relabeled PASS. Final pushed-head CI, Sonar zero/duplication
readback and Codex/security review are pending at this checkpoint.

The first delivery at `34b396875876d2d52e09bf44722e55d13bd9ab28` closed the original
eight Sonar findings but introduced twelve findings in new tests, launcher and
reference text. This follow-up removes arbitrary launcher inputs, extracts
coherent test/path helpers and preserves every original assertion. Its CI
registration repair adds only the new Go candidate workflow to the existing
exact publisher/copy/staging inventory. Action pins and permission boundaries remain
unchanged. Current source validation precedes a fresh normal delivery; remote
results from the first delivery cannot attest the follow-up.

The follow-up at `f96714c5470f9148dd6971871cff688b81cc36a9` incorrectly changed an
existing self-repository workflow reference after running an older actionlint
directly. Its independent zizmor check exposed that error. The original `$/`
reference and exact assertion are restored; the existing native compatibility
wrapper normalizes only validated references in memory for the older tool,
while security audits continue to inspect original sources.

At `8a36baac97b7a0eb177a2fb31e7b6f9f6288c338`, Sonar and both strict gates passed
with zero findings/annotations/duplication. Native Envoy CI then exposed a test
fixture's umask assumption: creation with 0640 becomes 0600 under umask 077.
The fixture now explicitly establishes 0640 before invoking the listener;
the unchanged assertion still requires preservation of that foreign file mode.
The failure reproduces under 077; focused repetitions/race and module checks
are repeated with that mask. This corrects test setup without relaxing cleanup.

## Security impact

Spool admission fails closed and preserves resource reservations through actual
cleanup. Service administrators must provision trustworthy private parent paths;
regular-file allocation is not cancellable by socket deadlines, and unrelated
filesystem writers require a dedicated filesystem/quota for isolation. Envoy
requires Linux procfs and atomic publication support; its private UID boundary
assumes trusted same-UID writers. Linux has no conditional inode unlink, so no
absolute guarantee against an adversarial same-UID racing writer is claimed.

Gitleaks still flags `generic-api-key` prose in published commits
`492663334d89428dce084792145ef94e91579788` (`docs/pr-382-i09-route-audit.de.md:55`)
and `91f07e124fe09056dc46dc59d65693f406b4b1a1` (`docs/pr-382-event-contract.md:138`).
Current wording is corrected; append-only commits cannot remove historical
matches. No credential values are reproduced. History rewrite and scanner
exceptions are prohibited in this task; a separate decision is required.
No validation, authentication, action pin, redaction, warning or gate is weakened.

## Runtime evidence

Local native/CGo, socket, spool-admission and physical-sink tests establish their
observed layers. R16/R17 remain historical selected NGINX-H1 runs, not evidence
for this head, all ten profiles or fourteen route legs. The real service-UID
startup test is blocked locally; injected ownership/read-only controls and root
profile readiness are separate evidence.

## Known limitations

Overall state: **BLOCKED_FOR_I12**. Full exact-head delivery acceptance remains
open because the historical PR-range secret check cannot pass under the current
constraints. Strict final Sonar and fresh reviews still require remote readback.
Known OSV graph-only baseline advisories are retained, rather than hidden.

## Remaining risks

The [I12 handoff](../../../docs/pr-382-i12-handoff.md) describes host prerequisites,
#410 conflicts, route-specific client/reset/neighbor/log evidence and historical
failure retests. I09/I10/I11 completion does not close I12/V08–V10. Post-return
budgets do not cancel a hanging engine; late abort cannot retract delivered bytes.

## Checks not run and rationale

The full I12 matrix, #410 integration, master merge and deployment are NOT RUN
and outside this task. The repaired master Go updater is **NOT_EXECUTED** after
integration: failed run `38370968157` remains historical evidence. Local/PR
candidate validation cannot establish **MASTER_WORKFLOW_VERIFIED**; that requires
a later authorized trusted master execution. `GO_UPDATER_FIXED_IN_PR` is not
asserted at this checkpoint; it requires the pending final PR verification.

## Final diff and review status

All 122 identities and original bases remain in the immutable index. The final
normal commit IDs, full local/remote/PR-head SHA binding and observed remote checks
belong in the [current PR description](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382)
and external delivery ledger. Historical green CI/Sonar is not promoted to the
current revision. This record authorizes no merge.

### I12 native regression follow-up, 2026-10-13

Starting product `8c574cdf86f10af976297c31d31485b042eba73b` remains the source
of these component observations. The old Companion assertion classified one
reversibly escaped byte as lossy and failed with SIGABRT/exit134. The repaired
fixture checks lossless escaping separately from real escaped-field overflow,
retaining physical no-write/hash-chain/first-cause assertions and explicit
native request/response policies. Product serializer/runtime code is unchanged.

`make check-native-engine-body-inspection` now runs the genuine Companion C
regression inside the native suite and existing Envoy runtime-components CI
step. External SDK include/library selections are honored; invalid selections
fail closed. Fourteen native methods pass with both system and explicitly
selected external libraries, without skips; the prefix-selected Companion
passes separately. Nineteen protocol/sink tests pass.

Stock's current RST control already passes. Strengthened tests correlate the
productive P2 decision and technical write failure, then prove denied418 with
backend0 and allowed200 with backend1 after reset. Six native component controls
pass; their UID0 scope does not establish Nonroot or stock-host acceptance.
An opt-in real Traefik UDS regression covers Reject/ProcessPartial, separate or
combined EOS, both directions, checked Finish/Destroy acknowledgments and
connection closure:18 native subcases pass
with race detection and the EOS-loss mutation fails as expected. No productive
append bug is reproduced; actual Traefik-host protocol-error classification
remains open. These checks do not independently count physical native cleanup.
The opt-in test requires the private real C service; ordinary
Go unit runs explicitly skip that additional integration control.

Local receipts remain under
`/var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/{common-lossy,stock-rst,traefik-repair,native-wiring}`.
They are retained local artifacts, not uploaded download links. `tests/README.md`
and its German companion document the new native target. Framework/MRTS source
and gitlinks, dependencies, gates and runtime guards remain unchanged. Full
live-host I12, exact final-head CI/Sonar/reviews and the independent historical
secret gate are not established by these component results.

The broad check also reproduced a separate optional-prerequisite test-fixture
defect: inherited GNU Make command-line assignments override the child fixture's
deliberately missing Framework and private build paths. The five synthetic
nested-Make invocations now clear only `MAKEFLAGS`, `MAKEOVERRIDES`, `MFLAGS`
and `GNUMAKEFLAGS`. Production Make/scripts, compiler flags and all failure
assertions remain unchanged. The original missing-Framework case fails with
inherited assignments; the corrected complete20-test module passes through
the normal outer Make target with explicit Python/Framework assignments.
Receipts: the same local run's `optional-fixture/` directory. Broad verification
and exact final-head delivery evidence remain separate.

### Historical I12 evidence adopted from PR #410

The ordinary merge of Parent `8c574cdf86f10af976297c31d31485b042eba73b` into the
existing #410 branch preserves its old head
`511c4ac4515f0e515f68b3bbc38274c5a230d903` in history.
The additional historical Change ID `CR-20261011-pr382-i12-host-evidence`
is consolidated here; its [immutable original](https://github.com/Easton97-Jens/ModSecurity-conector/blob/511c4ac4515f0e515f68b3bbc38274c5a230d903/reports/audits/change-records/CR-20261011-pr382-i12-host-evidence.md)
remains accessible. The [historical I12 report](../../../docs/pr-382-i12-host-evidence-20261011.md)
retains all observations; only its historical Change Record link now resolves
to the immutable original revision instead of the removed file.
Run `20261011T063350Z-0df51024008f-i12` tested Parent
`0df51024008fc84f0a6820f3b011055b69c3a3e2`, Framework
`99a7985c1be92a2297b1b59208f64df6768f2cbf`, MRTS
`8a6bb546c4c81d8ffc7be801dceac60c6925685f`: 79 selected records,
9 PASS, 6 FAIL, 53 BLOCKED, 11 NOT_EXECUTED; thirteen required legs with
0 complete PASS, 2 FAIL, 11 BLOCKED. Advisory Stock-native control separately
NOT_EXECUTED. These counts are not a complete required-case matrix or new
Parent results. I12/V08–V10 remain open. Original raw artifacts/checksums stay
unchanged; new runs receive their own source/config/host bindings. No removed
redundant record is restored; I09/I10/I11 and the original122 index entries remain.

### Stock real-backend evidence producer correction, 2026-10-13

The historical Stock06 physical log remains byte-identical. Its canonical
engine decision legitimately has empty `actual_action` before host observation;
the old validator rejected it. The corrected validator permits that contract
only for unobserved engine/error events and requires a separate observed,
same-transaction native deny451. Wrong correlation or missing host proof fails
closed; no engine action is invented.

The seven-case real-backend harness retains every attempt, physical stderr,
launch/exit/cleanup receipts, direct waited client headers/body/hash/framing and
independent backend failure/final counts. Failed cases continue after successful
cleanup; a cleanup failure stops further launches. Verified receipts publish
only after cleanup. Eighteen focused harness tests pass, including incomplete
framing despite client exit0, missing host evidence, wrong correlation and
launch/cleanup failures. Root's real current Stock host reexecution remains
required. Local receipts:
`/var/tmp/codex/ModSecurity-conector/runs/e2e/20261013T125816Z-8c574cdf-i12-completion/stock-harness/resumed-01`.
This modifies only the host-specific harness and its tests; product sources,
Framework/MRTS gitlinks, scanners and native runtime guards are unchanged.

### Native test quality-gate follow-up, 2026-10-13

The exact `b982c6f35abc47eccddcfded2bfd920f92516d90` Sonar check has zero
new/accepted issues and hotspots, but the strict duplication check reports
13 new duplicated lines in `tests/transaction_phase_runtime_companion_test.c`.
A shared event-file reader now retains the same open/read/error/close and
termination assertions at four call sites. The focused genuine libModSecurity
Companion regression passes with C17, `-Wall -Wextra -Werror`; `git diff --check`
passes. The preceding Traefik body-policy test refactor retains all cases and
passes module tests with race detection and vet. Both edits affect test code
only. Remote Sonar/CI must be read back on the delivered follow-up revision;
the historical secret-range gate remains independently failed.

### HAProxy native companion outcome repair, 2026-10-13

Actual combined host attempt `1791917296154368188` returned the expected
P3-deny403 and P4-Safe200, but physical logs showed failed outcome
acknowledgement/terminal cleanup and protocol errors. The binding rejected
every terminal Common state, including successful native blocking decisions.
It now permits the observed host outcome after a valid terminal decision;
technical failures and completed/cleaned states remain rejected. Native
body-limit Reject is policy, so its outcome and finish must preserve BODY_LIMIT
without treating successful enforcement as a technical protocol failure.
Native logging failures still fail finish. Claim, phase, correlation,
duplicate, bounds and first-cause handling remain enforced. The host outcome
does not overwrite the engine decision.

The genuine a30 rebuild/retest (`1791918602525320691`) then exposes a second
cause: after successful P3 OUTCOME the HTX caller invokes a typed connector-error
CANCEL because normal MRC1 RELEASE previously required P4 EOS. The existing
RELEASE opcode now also accepts an acknowledged, matching disruptive P3
outcome before commitment. Client and server share the matching predicate;
CLAIM-only, Allow/log-only, missing outcome and mismatched status remain
ineligible. HTX uses OUTCOME -> RELEASE -> close on success; explicit technical
CANCEL remains intact. No artificial EOS, new opcode or error suppression is
introduced. The client structure changes, so consumers require a genuine
rebuild; old host inputs retain their original revision identity.

Genuine libModSecurity/client/server tests and standalone client tests pass.
Four copied original-guard/outcome-validation controls compile successfully
and fail at the intended assertions. Receipts:
`haproxy-precommit-native-validation.json`, SHA256
`73ccabd26af1514570e9f7327812e71c825be858067aed5ce9a47599bf6d2454`,
in the task run. The real transport regression is wired into the existing
native body suite; the overlay build copies its new private helper header.
Focused host/build and response-handle contracts pass; the stale test cleanup
signature is aligned with the actual integer return without weakening checks.

Focused P3/P4/native-limit cases fail against the original guard and pass
after correction. Existing full binding/Common caller, native-result, phase,
technical-error/reentry and mutation regressions are rerun: eight final caller
tests and 18 native/phase contracts pass; all 26 existing zero-argument
transaction-contract checks pass through explicit direct invocation because
the selected interpreter has no pytest. Logging-failure and original-guard
mutations are detected. The native API
seam controls interventions and cleanup counts; these component tests are
not live-host evidence. The task's external
`hosts-haproxy-postfix-01/` retains genuine rebuilt binaries and fresh host
retests when completed; no old binary is relabeled. Exact final validation
and delivery results remain in the current report/PR delivery ledger.

### SPOP phase metadata and caller quality follow-up, 2026-10-13

Genuine rebuilt6175 HAProxy attempt `1791920706986259057` passes8directHTX
controls but fails normal combinedP3deny cleanup. Productive SPOP conversion
uses Common decision constructors, resetting phase to CONNECTION and losing
the original nativeP3/P4 phase. Guarded RELEASE correctly requires P3; it is
not relaxed. The bridge now explicitly maps native1–5 to named Common phases
after both Allow and disruptive constructors. Productive Ccaller regressions
exercise P3/P4 Allow/Deny/Redirect, original-omission and numeric-cast controls.
Original failure/logs remain retained in `hosts-haproxy-postfix-01/retry-02`.
Shared Common/Envoy sources are unchanged by this follow-up.

Exact6175 hosted Sonar reports one new Ctest cognitive-complexity finding
28>25 at `check_precommit`. The unchanged release/close error assertions move
into a coherent `check_precommit_cleanup_failure` helper. The real caller
Off/Safe/Strict matrix and its15 mutation controls pass, exit0,18.816seconds.
No assertion, compiler warning, scanner rule or gate is suppressed.

The next exact-head Sonar check rejects a nested status ternary in the new
SPOP regression fixture. A three-value status table preserves the exact
Allow/Deny/Redirect200/403/302 test inputs without nesting. No production
source changes; genuine e2445 host/build identities remain unchanged.

### Current I12 campaign disposition, 2026-10-13

The [current paired host report](../../../docs/pr-382-i12-host-evidence-20261013.md)
supersedes earlier delivery/checkpoint claims in this record. Outcome is
**I12_PARTIAL**, with all 13 required legs and the separate Stock-native
diagnostic assessed. The final Parent is `a9d48bb58aa948aea7d79e20cdf09d3f239b7808`.
The existing #410 normally merges the Parent and retains old #410 head
`511c4ac4515f0e515f68b3bbc38274c5a230d903` in ancestry. No master integration,
history rewrite, new PR or Framework/MRTS gitlink change occurred.

The complete selection remains 1,406 required IDs plus78 diagnostic IDs;
the [generated missing-case index](../../../docs/pr-382-i12-missing-case-index-20261013.md)
preserves every missing obligation and its reason. No smoke/driver exit0
is promoted to full I12/V08–V10 PASS. Historical79records, failed attempts,
physical raw logs and original source/build identities remain intact;
all85,108 historical manifest entries were rehashed unchanged.

Actual Apache sink/recovery probes, HAProxy direct/combined probes, Envoy
request/response probes and lighttpd Stock/patched/control observations are
retained in run-specific packets. Two reproduced HAProxy terminal-cleanup
defects and phase metadata are repaired in the Parent, with native negative/mutation checks;
SPOP/HTX binaries from e2445 and Envoy binaries from 6175 are genuinely rebuilt
and retested; scoped input comparisons bind unchanged product inputs to
final a9 without relabelling actual build/run identities.
Remaining NGINX/Traefik/patched launcher prerequisites and physical lifecycle/
transport/correlation producer gaps are reported explicitly. Absent fields
remain null. Harness fixes preserve native403 policy outcomes, valid empty
unobserved actions and cleanup receipts; normal-case physical HAProxy errors
now reject publication of PASS.

The user's later security-scope instruction is applied: advisory authorization
was checked, with no further deep scan/review trigger. The already established
historical Gitleaks range failure remains an independent release gate.
Final changed-path/local and exact-head hosted results are recorded in the
current report and delivery ledger. Both PRs remain Draft.

### Focused PR410 Sonar repair, 2026-10-14

The current request explicitly authorizes analysis and repair of the actual
PR410 findings. Authenticated readback through the canonical Sonar wrapper
finds ten open issues at starting head
`1a40c9109f7aef3373ec24019000eb9ebe4dc27b`: three HIGH security impacts and
seven maintainability issues. Exact-head GitHub check `115518660334` fails
only `new_security_rating`, C rather than A. The failed decoration omits
finding counters, so both strict scaffold checks correctly fail closed.
No parser change or missing-counter-to-zero fallback was introduced.

The two `pythonsecurity:S8707` paths were reproduced using synthetic bytes
and a private loopback listener: the internal client CLI could read an
arbitrary file and create an output outside its case directory. Its sole
normal caller now opens fixed artifact names exclusively through the existing
descriptor-backed `PrivateRuntimeRoot` and passes only owned regular-file
descriptors to the child. Checks retain exact 0600 mode, one link, distinct
identities, correct access modes and fresh output. Binary/partial response
bytes, timeouts, the existing response bound and exit77 remain intact.

The `pythonsecurity:S8705` Git call uses fixed argv and no shell; an option
injection was not demonstrated. The actual unchecked foreign-checkout input
is closed by binding the helper to its own canonical source root. Git receives
fixed arguments and that trusted cwd. Both artifact probes have ten-second
deadlines; hashes, version and source-equivalence validation remain mandatory.
S108, two S3776, S9154 and three S5778 are corrected without suppressions.

An independent bounded pre-patch investigation and candidate review found
no concrete remaining bypass or compatibility defect. Root reran 79 focused
tests, including both harnesses, native spool contracts and strict Sonar
parser controls, with the selected SDK: exit0, no skips. Whitespace passes.
Exact wrapped argv, source hashes, exits and original logs are retained in
`/var/tmp/codex/ModSecurity-conector/runs/e2e/20261014T034122Z-pr410-completion/verification/focused/`;
the original synthetic reproduction is under `sonar-stock/` in that run.
At repair head `4f59d1632322a78676e224ef40c0ab7c8e96286c`, cloud readback
confirms Security Rating A and Quality Gate OK. Seven newly reported
maintainability issues remain separate from those resolved security findings:
S1192 for the repeated request-artifact name and six S5778 exception tests.
The follow-up uses one filename constant and computes descriptor values
before the exception assertion, preserving every negative case. Root reran
the same 79 tests with the selected SDK: exit0, no skips; the second receipt
is `verification/focused-02/`. Full quick-check plus bilingual/link/variable
checks exit0 in 197.163 seconds. The new exact-head strict zero-issue and
scaffold readback remains pending; no parser or gate was weakened.

At exact follow-up `71ba09f0a695c333c2c10d3a0db46d2dc956ec40`, Sonar check
`115688597895` succeeds with zero new/accepted issues, hotspots and annotations.
Authenticated cloud readback confirms Rating A/Gate OK and zero duplicated
lines, blocks and density. Scaffold-lint job `115687673149` succeeds without
a parser change. These facts belong to that head; later delivery requires
fresh readback again.

### NGINX restricted ownership handoff, 2026-10-14

The original harness reproduces chmod EPERM after worker chown under mask
`0xc1`. The repair creates and sets exact0700 modes for the complete subtree
before transferring children, then parents. A repeated handoff verifies all
eight existing paths under the resolved worker identity without changing
inode/ctime. Symlink, UID/GID and mode drift remain rejected. The wrong-owner
phase4 negative fixture also sets0600 before chown; its rejection contract
is retained. Only the NGINX harness and its ownership tests change.

Seven actual root/nobody tests, including the real Framework materializer,
pass in 2.487 seconds. The initial attempt in the command sandbox had only
UID0 mapped and could neither drop the bounding set nor chown65534; that
environment failure is retained. The authorized outside rerun uses genuine
identity mapping, and the five capability regressions explicitly drop to
`0xc1`. Receipts are under `nginx-handoff/` in the 2026-10-14 task run.

Fresh offline NGINX1.31.6/module builds compile 33 current Parent inputs from
`a9d48bb58aa948aea7d79e20cdf09d3f239b7808`, using C17/GCC15.2.0 and real
libModSecurity3.0.14. Build/version/linkage exit0 is not host acceptance.
The private namespace-only0711 worker alias retains host attempt/data0700.
Two harmless actual admissions reproduce missing runuser PAM and restricted
master EACCES on worker-private logs. Private locked fixture accounts with
PAM root/Unix checks repair the former; the latter needs separately explicit
DAC admission and native host validation. No HTTP request or I12 PASS is
claimed by these setup probes. Original controller/source/specs and outside
cleanup receipts remain immutable in their individual attempts.

### Physical lifecycle observer and private Traefik staging, 2026-10-14

The test-only GNU linker observer preserves the actual API arguments, returns
and errno while recording paired calls, separate host/canonical IDs and public
Common state at each edge. Repeated successful terminal finish calls remain
attempts rather than invented transitions. Fourteen wrappers cover external link
references; internal calls within one object may bypass them. Private inherited
append output, a fork-shared byte budget, invalidation controls and final receipts
bound observation. Missing receipts or live mappings prevent qualification;
native MIME selection and actual host EOS remain null. Release artifacts remain
uninstrumented.

Actual selected-SDK controls and the additive NGINX module relink pass. Baseline
module and objects remain unchanged. The new explicit Make target blocks missing
output/SDK configuration. These component/link results establish no host PASS.
Receipts remain in the current external run's `native-observer-root/`,
`native-observer/`, `nginx-observed-build/` and `verification/harness-02/`.

The first real isolated Traefik attempts retain compiler failures and refused
private-copy cleanup. A wrong fixture GCC_EXEC_PREFIX relocated the existing
compiler's library search; removing it is independently reproduced as fail/pass.
The native harness now normalizes only its freshly copied plugin workspace to
0700 directories/0600 files, preserving sealed source and cleanup identity.
A regression proves read-only source preservation, private copy and safe removal
while retaining logs. The stale inventory test now checks eight active controls
and both rejected decoder tombstones separately; documented UDS chunk bounds
remain 32768, with no connector-owned total inspection limit restored.

Exact e5c02189 hosted checks are terminal:22 success/two conditional skips;
SonarGateOK/RatingA, zero new/accepted/hotspots/annotations and zero new duplicated
blocks/lines/density; scaffold-lint passes without changing the strict parser.
These results attest e5 only. Later commits require their own readback. Genuine
host retakes and all1484-case qualification remain pending at this checkpoint.

The exact3a1 delivery introduced five observer maintainability findings:
two excessive parameter lists, two combined declarations and a mutable lookup
reader. Typed observation context, separate declarations and a const reader
correct those actual findings. Native append wrappers now record size/input kind
without inventing EOS;15 selected-SDK tests pass. Public native/Common append
APIs expose no EOS argument. Their success or an empty append therefore leaves
host EOS unknown. Strict remote readback for this follow-up remains required.

### SDK-bound native identity observation, 2026-10-14

The actual9a Sonar finding S3776 reports event complexity27>25. Coherent bounded
identity serialization and descriptor-validation helpers remove that complexity
without suppressions or changing observation admission. The optional test-only
C++17 helper checks runtime version before using the selected SDK's public m_id;
real named and anonymous constructors, rejected version/bounds, native errno and
fake-ABI fallback are covered. Input IDs and Common canonical IDs remain separate.
Root's verification/harness-04 passes56 tests and whitespace with explicitSDK;
no hosted lifecycle or exact next-head Sonar result is inferred.

The authentic aba76c1b provider reports four new findings: two nested conditional
operators, an implicit weak function address and strlen on a compile-time SDK
version. Separate identity branches, an explicit weak-symbol address and
compile-time array lengths correct those findings. All56 focused observer/
Traefik harness tests pass again in verification/harness-05. The new provider
result remains required; no finding was accepted, excluded or counted as zero.

### Patched lighttpd Phase-2 harness admission, 2026-10-14

The actual hosted configuration check rejected `/proc/self/fd/5/events.jsonl`
with `ENOTDIR`: Common deliberately opens every parent with `O_NOFOLLOW`, so
`/proc/self` is unsuitable for the event sink. The subsequent adapter retake
passed that boundary and exposed the missing native
`msconnector.request-body-gate = "pre-upstream"` setting. Both failures preceded
requests; neither establishes a Phase-2 decision failure.

`run_phase2_pre_upstream_gate.py` now selects that required gate and uses the
named `event_sink_path` only for events. The method checks the canonical
directory against its held descriptor, private ownership, and the admitted
task root's original device/inode. Other paths, all descriptor-relative writes,
Common's no-follow checks, and native streaming guards remain intact. Root
replacement or escape is rejected; a renamed child inside the same root follows
the held inode.

The Parent contract suite passes 21 tests, including six new tests using the
actual compiled Common secure event opener and directory/descriptor negative
controls. The additional connector suite passes six tests after replacing its
stale removed-body-limit assertion with current no-connector-limit and required
native-gate checks. All 27 focused tests pass. Validation used RTK, the
selected Parent Python3.14.7 environment, and external temporary storage.
Actual current-source hosted execution, final CI/Sonar, and full I12
qualification remain pending. This harness change introduces no product limit,
dependency, Framework/MRTS edit, merge, or deployment.

### NGINX worker mapping and parser receipts, 2026-10-14

The 24 native fault/sequence probes originally stopped before traffic because
Root cannot read the non-dumpable Nobody worker's `/proc/PID/maps`. An optional
test-only preload captures that same worker's own maps immediately after its
successful UID change, through a fresh private append descriptor. The parent
checks the actual PID generation, UID/GID, complete bounded record and mapped
module/fault libraries before traffic. The strict direct-read default remains;
no `CAP_SYS_PTRACE`, host service or product body-limit change was introduced.

Independent review reproduced two descriptor leaks on sync and parser/output
errors. Cleanup now closes both map/fault descriptors while preserving the
original exception. Five regressions use real descriptors and verify `EBADF`.
All 21 Root/Nobody tests passed. Fresh isolated attempt
`1791967087014954093` ran the same 24 native probes with every driver exit 0,
then reaped its owned processes and removed namespace mounts. Earlier attempts
remain unchanged; driver results are not complete I12 lifecycle qualification.

NGINX config producers additionally retain the actual native parser argv, cwd,
PID, normal exit or signal and raw stream hashes. Nine rejection probes in
`1791965822160608456` and valid-rule startup in `1791965824941496409` passed
with these receipts. Configuration-only qualification follows its three-field
contract; missing request/response lifecycle fields are not inferred from it.
The affected parser/sequence suite passed 79 tests before this cleanup repair;
the final affected checks and exact delivery-head CI are recorded separately.

### NGINX strict quality follow-up, 2026-10-14

The actual `10102fcf` analysis reported eight new maintainability findings:
two S5754 cleanup catches, two S3776 functions, two S1192 startup filename
literals, and C S5350/S886 on stat-field traversal. There were no new security
issues or duplicate lines. Cleanup catches now use the actual `OSError` type;
bounded stream capture and startup completion have coherent helpers; startup
filenames are constants; field traversal uses a constant iteration count and
an explicit null guard. Primary causes, private FDs, capture bounds and all
parser results remain intact. The affected Root/Nobody suite passed all 116
tests (exit 0) after these changes. Fresh physical retakes and exact new-head
Sonar/CI remain separate required evidence.

### Traefik native client completion, 2026-10-14

The normal fixture closed TCP as soon as the declared response body arrived,
while the plugin still performed EOS and deferred engine finalization. The
client now requests connection close, retains a private duplicate socket and
requires bounded physical peer EOF after exact HTTP framing. Unbuffered reads
keep extra tail bytes visible; complete-read handling preserves fragmented
Content-Length and chunked framing. Timeout, TCP reset and extra bytes fail;
every duplicate descriptor closes on errors. Cancellation fixtures remain
separate and plugin/engine production sources are unchanged.

The affected suite passed 46 tests; the combined native-client/SDK-observer
suite passed 63 tests (exit 0). Initial isolated attempt
`1791969629249293459` stopped with exit 77 before traffic because the new
read-only snapshot lost executable bits; its original remains intact. A fresh
snapshot preserves all 121 trusted executable files. Retake
`1791969989698580089` passed six native profiles, HTTP 200/54-byte allow and
200/55-byte Safe, with clean owned process/mount cleanup. The former allow-side
`client_cancel` record disappears; successful native EOS/Finish/free remains
unmeasured. Historic `protocol_error` is not claimed fixed. Complete I12
qualification still requires each selected contract's independent observations.

### Traefik framed completion follow-up, 2026-10-14

Fresh independent review reproduced clean peer EOF after only three of ten
declared bytes on the actual `response.read(4096)` branch. Normal completion
now uses the existing bounded body reader and rejects a remaining declared
length; timeout/truncation close both client sockets. Real TCP tests exercise
this exact branch and fragmented Content-Length/chunked bodies. The combined
suite passed 65 tests; fresh native retake `1791970798770219279` passed all six
profiles with unchanged 54/55-byte allow/Safe results and no client-cancel
event. Native EOS/finish/free remain independently unqualified.

The actual `bdaca57d` provider reported S3776 complexity 16 and S5778 for a
port lookup inside an exception assertion. The coherent body helper reduces
the request function's complexity; port lookups now precede exception checks.
Strict gates, status/body oracles and every physical failure control remain.

### Traefik retained-exception response cleanup, 2026-10-14

The bounded second review reproduced an open response file after body timeout:
`HTTPConnection` had detached it for Connection-Close, while the retained cause
kept its descriptor alive. Explicit response ownership now closes that file,
connection and duplicate before returning; close errors do not replace an
active body failure. A real regression retains the exception and response,
checks the file is closed and observes `EBADF` before any GC. All 66 combined
tests passed; native retake `1791971306363843767` passed with clean namespace
cleanup. Successful native EOS and once-only engine API counts remain unknown.

### Traefik cleanup quality follow-up, 2026-10-14

The actual `dd61b70d` analysis found S5754 on the cleanup catch and two S8714
exception-test patterns. Cleanup now catches the actual owned-close `OSError`.
The real descriptor regression retains `Future.exception()` with its traceback,
response and file, so assertions never clear the cause before the `EBADF`
measurement. The mock cause check uses `assertRaises` and verifies identity.
All 66 combined tests and native retake `1791972087966404513` passed (exit 0).
No findings, exclusions, tests or quality requirements were waived.

### Final I12 reconciliation, 2026-10-14

All 1,484 original IDs remain: 1,406 required across 13 independent route parts and 78 diagnostics. Exactly 37 original configuration-parser contracts are Root-qualified PASS (36 required and one diagnostic). The other 1,447 remain unqualified: 1,370 required and 77 diagnostic. Actual selected execution is separately recorded as 108/1,406 required plus 8/78 diagnostic, 116/1,484 total. Three sibling request-parser probes do not establish their selected companion parser. The 596 unresolved original oracle entries, original 79 raw records and earlier failed attempts remain preserved.

Bounded readiness evidence covers all 13 required route parts: Apache 27 controls, 81 client exchanges and 27 native cleanup pairs; NGINX root-master/nobody-worker controls, 42 selected native operations, 14 exact canonical YAML host/client cases and both historical 60-fixture retakes (each 57 PASS, two pretraffic configuration failures and one posttraffic obsolete-log-oracle mismatch); HAProxy HTX eight and six shared SPOP/HTX companion controls counted once; three separate Envoy attempts; Traefik native UDS six, forwardAuth request two and companion four profiles; Stock sidecar seven controls with verified offline provenance; patched-native six P2 gate controls. These observations do not qualify 1,406 complete hosted lifecycle contracts.

Final native UDS v5 attempt `1791972087966404513` records allow HTTP 200/54 bytes, P1 deny 403/alternative 429, P2 deny 403, P3 deny 403 and P4 Safe HTTP 200/55 bytes. Current physical logs contain zero client_cancel and protocol_error records; 185 plugin/engine product inputs remain identical. The original allow with client_cancel=1/EOS=false and failed executable-mode snapshot remain preserved. Successful native EOS, finish/free and MIME remain unknown; TCP EOF and synthetic metadata do not establish native EOS. Product parent a9, genuine older build identities, hosted source 3a with exact harness deltas and current code `6b472cab6c18dfb5d6034461e1df5609e4ec3606` remain separate.

Result: `I12_PARTIAL` and independent `RELEASE_BLOCKED_SECRET_HISTORY`; both PRs remain Draft. Exact code 6b has authenticated Sonar Gate OK, Security A, explicit zero new/accepted issues, hotspots and duplication, and strict scaffold success. Its 24 successful, two skipped and two running checks are a captured checkpoint. The later documentation head receives separate fresh terminal GitHub/Sonar evidence externally and in both PR bodies. Current paired reports: [host evidence](../../../docs/pr-382-i12-host-evidence-20261014.md) and [missing-case index](../../../docs/pr-382-i12-missing-case-index-20261014.md). The generator, original contracts, Root approvals, partial packets and raw SHA references remain in the new run's final-reconciliation directory.

### Immutable original index

Each numbered link identifies one original Change ID through its filename.
The corresponding row in the language companion links its original counterpart.

| Original | Original base revision |
| --- | --- |
| [001](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260904-protected-base-exact-head-nginx.md) | `b779167ff979aa73cdd9321a829f9c693d943760` |
| [002](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260921-pr382-native-results-events.md) | `5170d24801243cdcd7bf1bca6123bf8cb2c72386` |
| [003](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-chain-link.md) | `3730eaa03b2f76ccac3baebfc862d8a8417c99ef` |
| [004](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-context-accounting.md) | `96c41eb287778e807daeba5b28f97bd5d86fbc0a` |
| [005](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-decision-errors.md) | `1301a4e30f04cb82dd0546607bfaab1461671b7b` |
| [006](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-envoy-bridge.md) | `57d42c575372edca0149465038d8a683a11d494d` |
| [007](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-native-intervention.md) | `7a52a55cfa4eb4c4c85ed44396e7137ef013f5aa` |
| [008](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-native-logging.md) | `1ce569e1afce55e17c767e1e06b0266874fe8c3e` |
| [009](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-nginx-result-tail.md) | `81e53a943fb149a92eb4214091f81a217c567f8b` |
| [010](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-nonrule-observation.md) | `7fe606c56a423f05454fe200f07a1c03d007ea3f` |
| [011](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-profile-errors.md) | `97d3ea10d526f8ab306bc1cc24fa63f573f36bc9` |
| [012](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-route-completion.md) | `68f78e079d88c80f82d1297c651f0e38e9624308` |
| [013](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-runtime-sink-errors.md) | `0532b5eb6dac5840b482dbc936ae1cf7a7ccbeb9` |
| [014](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260922-pr382-sonar-counts.md) | `e8d5e5081f166e8a9b01bbb84ce4baf6530109d9` |
| [015](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260923-pr382-apache-adoption.md) | `cac867da7292f6ca82fc76fee3b974382881c5b1` |
| [016](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260923-pr382-apache-native-lifecycle.md) | `ad22918e92849a10483439d72ac9a50154ec00be` |
| [017](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260923-pr382-envoy-native-verification.md) | `ee33afc5bbb961f2d0d612c5ff591eb073fd02ce` |
| [018](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260923-pr382-envoy-test-boundaries.md) | `3c29004b060b461649383cdb0db9996feab51b05` |
| [019](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260927-nginx-first-byte-safe.md) | `1bf1dcd46d25ba5b22f8a7d5915b5f72b4daa4da` |
| [020](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260927-nginx-lifecycle-output-root.md) | `57b0ed6a72ff7c7235037a59f008164be673e7a5` |
| [021](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260927-nginx-projection-invocations.md) | `9fbaa70227b17d71c11005bc45984a11b9dd5dce` |
| [022](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260930-nginx-no-crs-native-event-sink.md) | `3de8043c2482b52debc6f6e2d9ca609adf257eab` |
| [023](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260930-nginx-port-cleanup.md) | `91fce858acea9273d649e0bca1a5c2faadd28f9a` |
| [024](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20260930-nginx-redirect-location.md) | `0fe4c7b8cf4b021663985d895064e56cd2c63410` |
| [025](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261001-nginx-audit-result-pointer.md) | `2634d821acd80ad208a8e1cd3e4f49fd7e80c628` |
| [026](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261001-nginx-configtest-collection.md) | `794d16d7d387512213bc2e8d8b2f3199e5dbc6ce` |
| [027](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261001-nginx-configtest-receipt.md) | `794d16d7d387512213bc2e8d8b2f3199e5dbc6ce` |
| [028](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261001-nginx-empty-header-driver.md) | `e9d022ed16d9df469baa9b12070786468706ced7` |
| [029](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261001-nginx-h1-request-binding.md) | `75e2a24bcdc3ee97dab0d6f5a0e52e76b0b542c4` |
| [030](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261003-framework-sonar-gitlink.md) | `209e6f003282695e62876332a4b916eb3e170969` |
| [031](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261003-nginx-configtest-path-authority.md) | `acefed5c81a56f636610601edcc447a257b9e947` |
| [032](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261003-nginx-size-configtest.md) | `b1dd58a1289a84f15903fa0bb46474cf776e67db` |
| [033](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261003-pr355-pr396-integration.md) | `ac4c746f6a4c07006f25b078f660e31b16341479` |
| [034](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261007-pr396-ci-fixture-contracts.md) | `1f68c3742bd29b23a6938b36816adff4524944c7` |
| [035](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261007-protected-nginx-1316.md) | `60034d48dcee4ae5225bfaff012c48413cc0acd8` |
| [036](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-common-mapper-body-pointer-invariant.md) | `85397f4d621c568316566faccac6c217fc5315d8` |
| [037](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-harness-explicit-content-type-omission.md) | `5788ba5ced597106911785a5407b2024c68bbaf2` |
| [038](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-hostruntime-binary-artifact-hash.md) | `810a9b5621b04c79d58b1429c3182f1668e672c9` |
| [039](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-native-baseline-shell-environment.md) | `461bcd62a3cb2159ec9750db6ad64f0ab6053cc3` |
| [040](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-native-first-byte-shell-environment.md) | `8c19e31a21f0388b7b1417f0d25bb6530f496fae` |
| [041](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-native-unit-fixture-boundaries.md) | `06df37a5fc8963bdc8c9c5577d602b9861e4bb4d` |
| [042](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-native-uri-budget-cleanup-20261008.md) | `7c169f5bbe946650431f8e0cdbe2ddc63d3e85c1` |
| [043](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-admitted-native-begin-ledger.md) | `20478534e305a35c7f92fd80e8303a92121a5a3a` |
| [044](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-adoption-timing-dependency-boundaries.md) | `2ee41e347b8d6c7ac3eabc91aa3aa05f1690b279` |
| [045](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-bounded-native-uri.md) | `68bf814e0d850f68f20bd26da59ed7a351e3633d` |
| [046](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-cleanup-observation.md) | `201c6194a0061efe49e854a02f8626170ddee3b1` |
| [047](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-common-input-fault-driver.md) | `48243d5f77a6ae52b52729b6d6a2447229f6fab6` |
| [048](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-config-three-native-contracts.md) | `45754c0a0f0ae3dbd04f63a028d342bdac61220a` |
| [049](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-event-boundary-driver.md) | `bc9587f086b1e4ff558a870f2d5020aa22f72b64` |
| [050](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-event-boundary-serialized-callback.md) | `1940c1dbda6b371248a37f257c19df9b60fd836d` |
| [051](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-lifecycle-sequence-driver.md) | `b7403e30111688da00d8e7ce376ea91ced1c6145` |
| [052](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-merge-c17-unused-context.md) | `fe43865c03e89c0e8b0e1ae7dfbd5a9e11a7b602` |
| [053](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-missing-rules-filename-quality.md) | `8004340da887d143bc5e850822ac122eb5ce8b59` |
| [054](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-authority-baseline.md) | `6b069af4c2c87cdbddd7efc8867f642b1dd03098` |
| [055](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-authority-mrts-root.md) | `603e84493dcb51ab72eadb5a7102c4977cab631c` |
| [056](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-authority-producer.md) | `9ecd63fce94d424526fe6a70da1021c8f0d02681` |
| [057](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-cleanup-and-technical-faults.md) | `f0aa2fe099837d44d760012d28bd247729c73120` |
| [058](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-dispatch-overrides.md) | `9dcd35c7e380c1fc46d12bfd1fa53cfacb999775` |
| [059](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-fixture-followup-framework-pin.md) | `ca8ac4b0598da65b178f670652047052cda7a531` |
| [060](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-mime-driver.md) | `70bfce7f6e776f49ae3f8160b18fed6b8fe4779a` |
| [061](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-operation-collection.md) | `63d2f9a38c506e5122ace9ba36927add7f47e377` |
| [062](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-required-framework-pin.md) | `767de5bf4e901f256dffbca76547af4ee6b54757` |
| [063](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-native-response-limit-classification.md) | `8b575c094140f3a92bb030a83f27b4c44b00127e` |
| [064](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-p3-technical-source.md) | `ec632b50d439385859113f9667fcbddb29cde357` |
| [065](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-phase4-bounded-host.md) | `b7403e30111688da00d8e7ce376ea91ced1c6145` |
| [066](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-phase4-completion-observation.md) | `0981e437968a3d0df5cd6200f4d55b0128e4874e` |
| [067](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-phase4-native-body-observations.md) | `764402f47b7d2db941e5002485b205b4d4563cbd` |
| [068](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-pointer-protocol-cleanup-selection.md) | `bcb02b6b20c2e0697be3c0cd8013ce9b28aa1afa` |
| [069](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-post-return-engine-budget.md) | `49e2011b21893d1d30fdeedbe177deb48af0e4ce` |
| [070](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-projected-jsonl-source-guard.md) | `8004340da887d143bc5e850822ac122eb5ce8b59` |
| [071](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-protocol-fixture-executor-contract.md) | `708e15aa4623b2b039d333e8f654753a027a554d` |
| [072](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-raw-h1-native-invocation.md) | `883693506efa4ce64a016e2a440ac20ace367efd` |
| [073](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-response-limit-signature.md) | `91625ef984dcff914ea3a631dc738645d78abf45` |
| [074](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-selected-native-host-wiring.md) | `b7f3bb22a8ee5ebfe78a0f3b4fb3b32238200f91` |
| [075](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-seven-contract-hostoperations.md) | `a44d276b37f4ba1ce2c57af2f016d4cf96af43b6` |
| [076](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-source-p1-completion.md) | `9cfae553e7e69b1db8211f1a4ce0afc986b88604` |
| [077](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-standard-h1-forwarding.md) | `e3fcd1c7d5a9ce09abde7c9593a15690d7ed08f0` |
| [078](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-nginx-startup-quality-refactor.md) | `54877d2824c402a3912c71755bac7fcc884da5f4` |
| [079](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-response-fixture-content-type-omission.md) | `b7403e30111688da00d8e7ce376ea91ced1c6145` |
| [080](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-scheduler-lock-reuse-fixture-control.md) | `5e22a9f0cc9b688ddc271012467b053bca8d1bfb` |
| [081](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-scheduler-refill-causal-barrier.md) | `d76cb01c84350dbaeb380929bcc80a9c7719789e` |
| [082](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-selected-nginx-native-operations.md) | `4a28d86fa0d052397e74f0843ca6931e3dd17cae` |
| [083](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261008-sonar-s5778-release-test.md) | `3ddeb8f6bfab3c619e6db50c2b0621dc0a504c19` |
| [084](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-native-input-ledger-fd.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [085](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-native-python-quality-sink.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [086](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-body-buffer-event-scope.md) | `dcbefad1144b38f1545399a9f72967fbb1b3d424` |
| [087](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-ci-terminal-fixture-seams.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [088](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-cleanup-pool-lifetime.md) | `240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee` |
| [089](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-driver-contract-construction.md) | `240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee` |
| [090](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-driver-quality-boundaries.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [091](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-early-mapper-event-selection.md) | `407b647ce007daae5340cb87d2ead57f7ab4a730` |
| [092](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-exception-test-isolation.md) | `240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee` |
| [093](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-fresh-raw-run-mode.md) | `dcbefad1144b38f1545399a9f72967fbb1b3d424` |
| [094](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-input-fault-inherited-fd-20261009.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [095](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-native-collection-authority.md) | `cf95e1e2519909d498a4a6fdb0e21db16b2ae3c4` |
| [096](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-native-readers-pin.md) | `e319c932db7da011feca54fcb1fc5d2ab5d6018f` |
| [097](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-native-receipt-single-write.md) | `e5e8569eaf0f0ce1cdc8b56e3181d872d03eb9a8` |
| [098](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-phase4-path-input-adapter-20261009.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [099](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-phase4-reject-header-flush.md) | `75686a47ba971d33c46f4f40a844bbe53d7465f1` |
| [100](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-projection-case-identity-20261009.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [101](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-ruleid-adoption-delegation.md) | `c09480ff9b5b83b52883f5cf116266f1da5ca4d1` |
| [102](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-sequence-driver-quality-phases.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [103](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-sequence-prefix-publication-barrier.md) | `fabc2b7b436cf1fe276a4fc681e8edc1221145b7` |
| [104](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-sequence-static-probe-cleanup.md) | `b884c6653a72dc490c4ae472dd3cbf5a1ee646b8` |
| [105](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-sonar-c-quality-20261009.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [106](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-nginx-upstream-header-reader.md) | `c57e6b0a930161e83cb59bf5905a6db00311dc91` |
| [107](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261009-selected-native-projection-parent-authority.md) | `f63996290925f4b0c04d286506171825de9dc2ff` |
| [108](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-apache-adoption-check-batching.md) | `ff162ecb11217320a81829169a72ca4a5a4081f9` |
| [109](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-nginx-ab-cognitive-followup.md) | `2686b07aaf64b0541d743b53970008bd86caa91f` |
| [110](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-nginx-first-byte-snapshot-binding.md) | `b0d75ef6bbc33228423aef65d8ea3409387ab30f` |
| [111](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-nginx-intervention-outcome-projection.md) | `dca17fd5690c2ec2b8806024d1061744db8c3ad8` |
| [112](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-pr382-nginx-system-reference.md) | `2a5704f82fdae4ba75902eb3f4244225838e1747` |
| [113](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-r17-pr382-nginx-system-evidence.md) | `b2622a5d6ca746485c08f4789208299a111f47c7` |
| [114](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-r17-strict-client-full97.md) | `2f02370b07149265841411894f1a2cf7f1e978ff` |
| [115](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261010-remove-phase4-body-limit.md) | `b4044d10682cb2881c218fe84cebe41e61b235c2` |
| [116](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-i09-native-route-reconciliation.md) | `498653c2a193d34b7b25b2903b1e4db1c45e7f73` |
| [117](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-pr382-b09-secret-scan-followup.md) | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |
| [118](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-pr382-i10-adapter-errors.md) | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |
| [119](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-pr382-i11-physical-sink-parity.md) | `0df51024008fc84f0a6820f3b011055b69c3a3e2` |
| [120](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-pr406-i09-i11-conflict-resolution.md) | `6a79efe7d571d9fc980f970a08073d6334c36a7a` |
| [121](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261011-response-limit-policy-removal.md) | `2619b20b9d2e70fa07cbe71f664b48ff3c105380` |
| [122](https://github.com/Easton97-Jens/ModSecurity-conector/blob/4639f982a8125f4150394e4d4f2e8af4e690f494/reports/audits/change-records/CR-20261012-pr409-base-refresh.md) | `1e7f7c8405ddcc7fc4a5ff117ef45c5bf0686707` |
