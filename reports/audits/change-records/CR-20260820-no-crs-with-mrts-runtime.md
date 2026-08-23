# CR-20260820 — Closed no-CRS/with-MRTS runtime route

**Language:** English | [Deutsch](CR-20260820-no-crs-with-mrts-runtime.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260820-no-crs-with-mrts-runtime |
| Date (UTC) | 2026-08-20 |
| Base revision | `7c403fada21de4547259fef1dc4a1b079cb0cb25` |
| Parent boundary | Parent only; current Framework and MRTS gitlinks consumed read-only |
| Framework gitlink | `c40e924ec5c341032908e0082feba1d37ed1dfda` |
| MRTS gitlink | `615b13bacbd008562c17408246c41ab27dca3104` |
| Delivery status | Task branch is rebased on the observed current master; Draft delivery may proceed without claiming host-runtime, hosted-check, or Sonar success; no merge, auto-merge, or default-branch write is authorized |

## Motivation and problem statement

The current `master` state needs a closed, mode-specific route for real
`no-crs/with-mrts` execution through Envoy, Traefik, and lighttpd. The stale
PR #279 state is not used as the implementation base. The route must keep the
three `with-crs/with-mrts` targets unsupported and must not broaden unrelated
connector behavior.

## Acceptance criteria

- Only Envoy, Traefik, and lighttpd are admitted to the new target route.
- The exact Parent/Framework/MRTS gitlink chain is recorded and checked.
- The Framework-generated MRTS inventory and load file are used by a real
  host executor, with a control, detection, and benign bypass case.
- Runtime results correlate request, transaction, case, and observed events;
  result output is bounded and atomically written in a private run root.
- CRS paths and CRS includes are rejected; OWASP CRS is not acquired, loaded,
  cached, or reused by this profile.
- Real host, cleanup, exact-head CI, Required Checks, and Sonar evidence is
  recorded only when actually observed.
- `with-crs/with-mrts` for the three targets and NGINX remain unchanged.
- No Framework or MRTS source change is required.

## 2026-08-23 branch reconciliation and job isolation

The task branch was normally rebased onto the fresh
`origin/master` `7c403fada21de4547259fef1dc4a1b079cb0cb25`; it is neither based
on nor delivered through PR #279. The Parent records Framework
`c40e924ec5c341032908e0082feba1d37ed1dfda`, whose published MRTS gitlink is
`615b13bacbd008562c17408246c41ab27dca3104`. The local nested Framework
checkout is not used to rewrite that gitlink.

The no-CRS/with-MRTS workflow now derives preparation and execution from a
closed per-connector branch. Apache receives only the Apache component and
runtime path; HAProxy receives only the HAProxy component and runtime path;
Envoy, Traefik, and lighttpd use their own literal sealed-target invocation.
NGINX is absent. No matrix-provided component target or command reaches
`make`, a shell, a path, or a runner.

Every job writes a safe GitHub Step Summary after evidence upload, including
fixed stage outcomes, counts, the first non-passing stage, and a
`PASS`/`FAIL`/`MISSING`/`CANCELLED` runtime-bundle state. It does not read raw
evidence or promote a missing, skipped, or failed runtime to success.

The repository and hosted workflow retain `.go-version` `1.26.7`. The local
binary is `go1.26.6`; under the current user direction that difference is a
recorded local-validation limitation, not a download, upgrade, contract
change, or exact-hosted proof.

## Implementation decision and rationale

Parent owns the host adapters and the closed dispatch boundary. The new
`ci/runtime/lifecycle/run-no-crs-with-mrts-target.py` materializes the exact
Framework MRTS runtime, selects the portable phase-1 GET ARGS cases, adds
explicit control and bypass cases, and invokes the existing real host stage.
`execute-no-crs-mrts-cases.py` sends live requests and validates DetectionOnly
HTTP 200 plus event correlation before writing a fresh receipt. Host-specific
adapters remain Envoy ext-proc, Traefik native middleware, and lighttpd's
patched native path.

The route is opt-in through `MSCONNECTOR_MRTS_RUNTIME=1` and uses private,
symlink-checked runtime paths. It rejects plan/result reuse, duplicate JSON
keys, traversal, CRS references, and connector names outside the closed set.
The plan is sealed by the SHA-256 digest of its exact bytes and that digest is
required at every host-adapter and executor boundary. Selected case hashes and
the selected inventory hash are reconstructed from the exact Framework
checkout and must match the sealed plan. Rule-match evidence uses a typed
native `RuleMessage` observer, disabled by default and enabled only for the
sealed MRTS profile; it emits bounded metadata-only JSONL records and validates
native integrity and contiguous chaining. The Parent Go-version contract
checker is aligned with the current CodeQL `awk` guard, preserving the exact
stable `1.26.x` grammar. Local Go validation used `/usr/local/go/bin/go`
`go1.26.6` with `GOTOOLCHAIN=local`.

The lifecycle follow-up generates `NO_CRS_RUN_ID` inside the closed target
runner as `mrts-<32 lowercase hexadecimal characters>`. It rejects an ambient
value, forwards the generated value through the `env -i` boundary, and
reasserts the readonly snapshot value before either native host starts. The
workflow therefore does not pre-seed a GitHub-provided identity. This supplies
the same bounded lifecycle identity to Traefik and lighttpd without accepting
a caller-controlled value.

Traefik's native engine needs a short AF_UNIX socket parent while the sealed
runtime root can exceed the platform socket-path limit. Only for that host the
target runner allocates one unique `/var/tmp/msct-*` child, checks every path
component for symlinks, forces exact owner mode `0700`, and bounds the complete
native socket candidate to 100 bytes. The native host must remove its own
child first; the Parent removes only the now-empty exact parent and fails
closed on any unexpected artifact. Plans, logs, results, and retained evidence
remain below the private run root. The sealed MRTS `env -i` boundary forwards
only this calculated parent for Traefik; a missing value still makes the native
runner fail closed.

The current implementation commits include the sealed run-identity and socket
parent follow-up (`602d88e3`) and its closed Traefik `env -i` forwarding fix
(`14f453d7`). Neither commit changes the Framework or MRTS gitlink.

The first fresh Traefik `r2` target attempt then stopped fail-closed before
host creation: its auxiliary load-file check used a broad textual CRS match and
classified `mrts-no-crs-*` in the legitimate private root as CRS material. The
generated load file itself had only the 15 pinned `MRTS_*.conf` includes, and
the central sealed validator still requires canonical include syntax, the
private generated-rule directory, the complete canonical include set, and
byte-for-byte hashes. The narrow local guard now detects only actual CRS path
components; focused controls reject `crs` and `owasp-crs` components and accept
a `no-crs` parent. `FND-PARENT-0201` preserves the diagnostic and keeps release
promotion blocked until two fresh exact-head Traefik receipts.

Fresh Traefik `r3` on Parent `27b7e5a5` passed that guard, built the pinned
Traefik runtime, and reached the real native host. Its first legitimate MRTS
GET control then received HTTP 501 from the local upstream fixture: the sealed
executor intentionally sends GET cases, while that fixture implemented only
`do_POST`. This is a task-owned fixture capability gap, not CRS, rule, or host
middleware evidence. No MRTS receipt was written, and host cleanup still
completed. The fixture now routes body-free GET and existing POST requests
through the same bounded response path, and rejects GET body framing;
a direct GET control contract prevents a repeat of the 501. It still requires
two fresh receipts on the new candidate head before promotion.

## Security impact

The relevant boundaries are untrusted connector/case selection, generated
MRTS configuration, subprocess and host lifecycle, HTTP request correlation,
and private evidence files. Validation is fail-closed for path traversal,
symlink components, mutable or mismatched gitlinks, CRS references, stale
results, duplicate JSON keys, and unsupported connector names. This record
also records diagnosed `FND-PARENT-0194`: the approved venv's final symlink
must be preserved, symlinked parent directories must be rejected, and shell
dispatch must carry the same approved interpreter through its closed boundary.
The Framework generator uses explicit `PYTHON` selection; this record does not
claim that the product rewrites the caller's `PATH`. The remediation is present
in the current source and focused contracts, but the finding remains
release-blocking until fresh runtime validation. This record does not claim a
completed hosted security scan; any remaining security result is pending the
implementation and validation run.

## Changed files

The task implementation currently includes these Parent paths, subject to
final diff review:

- `ci/runtime/lifecycle/run-no-crs-with-mrts-target.py`
- `ci/runtime/lifecycle/execute-no-crs-mrts-cases.py`
- `ci/runtime/lifecycle/run-connector-stage.sh`
- `ci/runtime/lifecycle/run-remaining-connector-target.sh`
- `ci/checks/common/check-go-version-contract.py` and focused common security,
  adapter, and remaining-connector wiring checks
- `common/include/msconnector/config.h`
- `common/include/msconnector/event.h`
- `common/runtime/msconnector_runtime.c`
- `common/runtime/msconnector_rule_match_observer.cc`
- `common/runtime/msconnector_rule_match_observer.h`
- `common/src/config.c`
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh`
- Envoy build/configuration/harness scripts and ext-proc Go source/tests
- `connectors/traefik/scripts/runtime_native_smoke.py`
- Traefik build scripts, MRTS input tests, and
  `tests/test_traefik_transport_hardening_contract.py`
- `connectors/lighttpd/harness/run_patched_full_lifecycle.sh`
- `connectors/lighttpd/harness/run_patched_lifecycle_smoke.sh`
- Lighttpd build/configuration and host-contract tests
- `.github/workflows/test-connectors-no-crs-with-mrts.yml`
- `ci/runtime/lifecycle/summarize-no-crs-with-mrts-workflow.py`
- focused `tests/test_no_crs_with_mrts_*.py`, including workflow-isolation and
  safe-summary contracts, Envoy transport, and selected-runner contracts
- `tests/test_go_version_contract.py`
- `docs/testing-and-evidence.md` and `docs/testing-and-evidence.de.md`
- this paired Change Record and its archive index entry

Framework and MRTS source files are not changed.

## Commands executed

The following repository inspection commands were executed while preparing the
record: `rtk proxy find`, `rtk proxy sed`, `rtk proxy rg`, and
`rtk proxy git status --short`. The observed local validation passed: 97
focused Python contract tests; shell syntax checks for changed runners;
Python compilation; `check-common-security-contract.py`;
`check-adapter-contracts.py`; `check-remaining-connectors-build-wiring.py`;
`git diff --check`; C17 remaining-connector checks; and C/C++ syntax checks.
The current Traefik GET-upstream correction passed 106 focused selected-runner,
sealed-target, dispatch, workflow, Traefik input/plugin, and transport-contract
tests with `TMPDIR=/var/tmp` and bytecode writing disabled.
Envoy and Traefik Go checks used `/usr/local/go/bin/go` `go1.26.6` with
`GOTOOLCHAIN=local`: `gofmt`, `go mod verify`, `go list -deps ./...`,
`go test ./...`, `go vet ./...`, and `govulncheck ./...` passed. The Traefik
module was run from `connectors/traefik/native_middleware`; its first longer
temporary socket path was replaced by a private short test root. The scanner
kept the original C/H baseline and explicitly added only
`common/runtime/msconnector_rule_match_observer.cc`; four pre-existing
ShellCheck SC1007 warnings remain in the Envoy configuration helper. The
documentation contract checks passed: `rtk proxy make check-bilingual-docs`
(`bilingual docs ok`), `rtk proxy make check-doc-links` (`repository path
references: PASS`; `doc links ok`), and `rtk proxy git diff --check` (exit 0).
After the diagnostic Envoy `r10` header mismatch, the focused Envoy/Lighttpd
contract pair passed 50 tests and `sh -n` passed for
`connectors/envoy/harness/run_envoy_ext_proc_runtime.sh` and
`connectors/lighttpd/harness/run_patched_lifecycle_smoke.sh`. These checks
validate the narrow source dispatch changes only.
The focused target-runner suite for the r11 phase-ordering correction passed
28 tests, and its security review found no concrete blocker. This is still
source-level validation only.
The current socket-parent and run-identity follow-up passed shell syntax,
ShellCheck, `git diff --check`, 107 focused Python contracts, and the broader
160-test Parent suite. That broader suite used the short AF_UNIX-capable
`TMPDIR=/var/tmp`: an earlier long private temporary path made the test helper
reject its own socket candidate, and the unchanged Envoy phase-4 barrier test
timed out once under suite contention. Both tests then passed in isolation and
the complete rerun passed; this is recorded as an environment/test-path limit,
not a product success shortcut. A focused security-diff scan of the six
follow-up files reported no concrete finding. It is source-level review only
and does not replace fresh host receipts or exact-head hosted checks.
The focused post-forwarding suite passed 94 tests, including selected runner,
sealed target, dispatch, workflow, Traefik MRTS-input, and Traefik native
plugin contracts. The three real-host final-candidate repetitions, the full
five-connector hosted workflow, exact-head Required Checks, and SonarQube
Cloud analysis are currently `NOT EXECUTED`. No static contract or inventory
result is promoted to runtime `PASS`.
The narrow Traefik load-guard correction passed 56 focused target and Traefik
input contracts plus `git diff --check`; it has not yet been used in a host
run. Its focused independent security review found no concrete bypass, and it
does not weaken the central sealed no-CRS corpus validation.

The 2026-08-23 connector-isolation update passed 188 selected Parent tests
(four expected skips due to the locally checked-out nested Framework not being
the Parent-recorded gitlink), 125 focused CI-security tests (five expected
skips), `check-common-security-contract`, `check-common-memory-safety`,
`check-common-flow-integrity`, `check-adapter-contracts`, checksum-verified
actionlint, and offline zizmor. These are source, workflow, and security
contract results only. No local Go version was acquired or changed: the
available `go1.26.6` is documented as non-equivalent to the repository's
required `1.26.7` hosted contract.

## Runtime evidence

One retained pre-documentation Envoy receipt is now claimed as diagnostic
runtime evidence only: `r15` on Parent `14f453d7` used the exact recorded
Framework and MRTS gitlinks, passed real Envoy ext-proc startup/readiness,
executed ten live DetectionOnly MRTS cases with HTTP 200, emitted correlated
native rule-match evidence, and reported cleanup passed. It establishes the
current host path but is not final-candidate evidence because this record's
reconciliation commit follows it. Final promotion still requires two fresh,
independent receipts for every target connector on the candidate head.

Two later independent Envoy receipts, `r16` and `r17`, completed on Parent
`e7316caa` with real ext-proc host start/readiness, ten HTTP-200
DetectionOnly cases, correlated metadata-only rule-match evidence, and cleanup
passed. They remain behavioral evidence only because the current Traefik guard
repair follows that head; every target connector must be repeated from fresh
roots on the final candidate head.

Traefik `r2` is diagnostic-only: it stopped at the auxiliary load-file guard
before native host creation, readiness, request processing, case execution,
or a runtime receipt. Its failure is not evidence of CRS loading and cannot be
used as a runtime result.

Traefik `r3` is also diagnostic-only: it passed the repaired no-CRS guard and
started the real host, but its first MRTS GET control received HTTP 501 from
the POST-only local upstream before a case result, event correlation, or
receipt could be produced. It confirmed clean host teardown but cannot be used
as a runtime result.

Evidence must remain in the private run root and include the plan/result/event
paths, exact Parent/Framework/MRTS identities, case and request correlation,
no-CRS result, evidence hashes, and cleanup status. Raw payloads, secrets,
private keys, and local absolute paths must not be copied into this record.

The complete sealed `mrts.load` can legitimately yield more than one native
DetectionOnly match for a selected request. The Parent executor therefore
uses the canonical Apache/HAProxy subset oracle: every case-declared expected
ID must be present in the fully validated, exact-transaction and exact-phase
evidence, and additional same-phase IDs remain in the receipt only when they
belong to the revalidated pinned rule-ID inventory. They do not replace an
expected ID; an expected ID at another phase fails closed; and
any correlated match still fails a control or bypass case.

Envoy `r10` is retained only as diagnostic evidence: it reached real-host
start and readiness, then failed with HTTP 500 before MRTS case execution
because sealed evidence mode requires `x-mrts-transaction-id` while the
readiness probe sent `X-Request-Id`. No case result, sealed MRTS receipt, or
runtime success is claimed. The current local correction selects the closed
MRTS readiness header only in MRTS mode and retains `x-request-id` in normal
mode. Independently, the Lighttpd MRTS dispatcher now selects the sealed full
lifecycle executor instead of falling through to legacy compatibility smoke.
Both corrections still require fresh host validation.

Commit `6e63fb52` records the readiness-header and Lighttpd dispatcher
corrections. Fresh Envoy `r11` reached real Envoy/ext-proc start and corrected
readiness but stopped before MRTS case receipts: valid unrelated readiness
events were phase-checked before transaction/URI correlation. The valid
transaction `envoy-ext-proc-readiness-1` includes `request_body`,
`response_headers`, and `response_body`. This is diagnostic-only real-host
evidence, not a runtime result. `FND-PARENT-0198` tracks the Parent executor
ordering defect. The narrow correction retains duplicate-safe parsing, exact
schema, native-hash, and global-chain validation for every event line; it uses
a finite native phase mapping, ignores only fully valid unrelated
transaction/URI records after validation, and keeps a relevant wrong phase
fail-closed.

Fresh Envoy `r12c` then reached the pinned build, real ext-proc host start,
readiness, and a DetectionOnly request but failed before any valid MRTS receipt.
The relevant request transaction contained the selected request-body rule and
valid same-transaction `response_headers`/`response_body` records. Treating
those nonexpected response-phase records as invalid is a second executor
classification defect. They must remain integrity-validated and then be
outside the selected request-body acceptance profile. An expected rule ID at a
wrong phase, and all control/bypass expectations, remain fail-closed. `r12c`
is diagnostic-only and cannot promote the cell.

## Checks not run and rationale

- Final-candidate Envoy, Traefik, and lighttpd real host execution:
  `NOT EXECUTED`; Envoy `r15` is a successful pre-documentation diagnostic
  receipt and does not replace the required fresh repetitions.
- Hosted GitHub Actions and exact final PR-head checks: `NOT EXECUTED` at this
  record update; a Draft PR may be opened, but no success is inferred before
  exact-head evidence is observed.
- SonarQube Cloud analysis and Quality Gate for this task head: `NOT EXECUTED`;
  no exact task PR-head analysis is observed.
- Framework/MRTS source tests: `NOT APPLICABLE`; neither source repository is
  changed by this Parent task.

## Known limitations

The task branch is based on current `master`, not PR #279. The implementation
and its local contracts may still change after host execution exposes
connector-specific issues. The local evidence includes one real Envoy receipt
but does not establish the three-connector final-candidate host matrix. The
documentation records the intended closed route and current evidence boundary;
it does not establish `verified_pr`.

## Remaining risks

The final host adapters may reveal capability, readiness, or cleanup defects.
`FND-PARENT-0194` is not closed by local interpreter-contract tests alone;
fresh private-root host attempts must confirm that MRTS generation uses the
approved venv and produces no false runtime receipt on dependency failure.
Envoy `r15`, `r16`, and `r17` demonstrate the current host route but all
precede the Traefik guard repair and cannot be final-candidate evidence. Two
fresh final-candidate receipts per target connector must prove MRTS cases,
no-CRS evidence, and cleanup. Neither a legacy Lighttpd smoke result nor a
static contract can serve as runtime evidence.
The final workflow may expose environment or required-check failures. Until
those exact results are observed, the three target cells remain
`PENDING` for delivery classification.

## Final diff and review status

`PARTIAL — the task branch is rebased on current master and adds narrow
connector-isolation and GitHub Summary contracts, while fresh candidate-head
runtime, exact-head CI, Required Check, and Sonar evidence remain pending.` A
normal Draft PR may be created; no merge, auto-merge, or default-branch write
is authorized or claimed.
