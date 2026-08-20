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
| Delivery status | Task branch implementation in progress; no commit, push, PR, merge, or hosted result asserted |

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
The Parent Go-version contract checker is also aligned with the current
CodeQL `awk` guard, preserving the exact stable `1.26.x` grammar instead of
requiring the superseded Bash-only spelling.

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
- `ci/checks/common/check-go-version-contract.py`
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh`
- `connectors/traefik/scripts/runtime_native_smoke.py`
- `connectors/lighttpd/harness/run_patched_full_lifecycle.sh`
- `.github/workflows/test-connectors-no-crs-with-mrts.yml`
- focused `tests/test_no_crs_with_mrts_*.py` contracts
- `tests/test_go_version_contract.py`
- `docs/testing-and-evidence.md` and `docs/testing-and-evidence.de.md`
- this paired Change Record and its archive index entry

Framework and MRTS source files are not changed.

## Commands executed

The following repository inspection commands were executed while preparing the
record: `rtk proxy find`, `rtk proxy sed`, `rtk proxy rg`, and
`rtk proxy git status --short`. They confirmed the current-master base,
existing documentation convention, and task-owned implementation paths. The
documentation contract checks passed: `rtk proxy make check-bilingual-docs` (`bilingual docs ok`), `rtk proxy make check-doc-links` (`repository path references: PASS`; `doc links ok`), and `rtk proxy git diff --check` (exit 0).
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
connector-specific issues. The documentation records the intended closed
route and current evidence boundary; it does not establish `verified_pr`.

## Remaining risks

The final host adapters may reveal capability, readiness, or cleanup defects.
The final workflow may expose environment or required-check failures. Until
those exact results are observed, the three target cells remain
`PENDING` for delivery classification.

## Final diff and review status

`PARTIAL — documentation updated; implementation and runtime/delivery evidence
pending.` No commit, push, PR creation, merge, auto-merge, or default-branch
write is recorded.
