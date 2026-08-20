# CR-20260820 — Closed no-CRS/with-MRTS runtime route

**Language:** English | [Deutsch](CR-20260820-no-crs-with-mrts-runtime.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260820-no-crs-with-mrts-runtime |
| Date (UTC) | 2026-08-20 |
| Base revision | `b42907ca410da69843c80d0c4376193b6ab3801b` |
| Parent boundary | Parent only; current Framework and MRTS gitlinks consumed read-only |
| Framework gitlink | `bd69ee96e0e7082317d4afe1232bee625665eb9a` |
| MRTS gitlink | `615b13bacbd008562c17408246c41ab27dca3104` |
| Delivery status | Task branch implementation in progress; current source changes uncommitted; no push, PR, merge, or hosted result asserted |

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

## Security impact

The relevant boundaries are untrusted connector/case selection, generated
MRTS configuration, subprocess and host lifecycle, HTTP request correlation,
and private evidence files. Validation is fail-closed for path traversal,
symlink components, mutable or mismatched gitlinks, CRS references, stale
results, duplicate JSON keys, and unsupported connector names. This record
does not claim a completed hosted security scan; any remaining security result
is pending the implementation and validation run.

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
- Traefik build scripts and MRTS input tests
- `connectors/lighttpd/harness/run_patched_full_lifecycle.sh`
- Lighttpd build/configuration and host-contract tests
- `.github/workflows/test-connectors-no-crs-with-mrts.yml`
- focused `tests/test_no_crs_with_mrts_*.py`, Envoy transport, and selected-runner contracts
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
The three real host runs, the full five-connector hosted workflow, exact-head
Required Checks, and SonarQube Cloud analysis are currently `NOT EXECUTED`.
No static contract or inventory result is promoted to runtime `PASS`.

## Runtime evidence

No retained three-connector runtime receipt is claimed by this record yet.
When available, evidence must remain in the private run root and include the
plan/result/event paths, exact Parent/Framework/MRTS identities, case and
request correlation, no-CRS result, evidence hashes, and cleanup status. Raw
payloads, secrets, private keys, and local absolute paths must not be copied
into this record.

## Checks not run and rationale

- Envoy, Traefik, and lighttpd real host execution: `NOT EXECUTED` at record
  creation; requires the completed adapters and their runtime prerequisites.
- Hosted GitHub Actions and exact final PR-head checks: `NOT EXECUTED`; no PR
  exists yet.
- SonarQube Cloud analysis and Quality Gate for this task head: `NOT EXECUTED`;
  no task PR head exists yet.
- Framework/MRTS source tests: `NOT APPLICABLE`; neither source repository is
  changed by this Parent task.

## Known limitations

The task branch is based on current `master`, not PR #279. The implementation
and its local contracts may still change after host execution exposes
connector-specific issues. The local evidence covers static, language, and
contract checks only; it does not establish host-runtime behavior. The
documentation records the intended closed route and current evidence boundary;
it does not establish `verified_pr`.

## Remaining risks

The final host adapters may reveal capability, readiness, or cleanup defects.
The final workflow may expose environment or required-check failures. Until
those exact results are observed, the three target cells remain
`PENDING` for delivery classification.

## Final diff and review status

`PARTIAL — documentation updated; implementation and runtime/delivery evidence
pending.` No commit, push, PR creation, merge, auto-merge, or default-branch
write is recorded.
