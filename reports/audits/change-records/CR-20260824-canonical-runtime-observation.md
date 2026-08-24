# Change Record CR-20260824: Canonical runtime observation contract

**Language:** English | [Deutsch](CR-20260824-canonical-runtime-observation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260824-canonical-runtime-observation` |
| Date (UTC) | `2026-08-24` |
| Base revision | `232b020cac23d5edc0e18adaf502468bb3012237` |
| Source implementation revision | `ebb1aa565c0fd1e88efef454a5807640daf6adcd` |
| Scope | Parent-only versioned runtime-observation contract, strict validator/CLI, contract fixtures/tests, Envoy/Lighttpd/Traefik normalizer integration, secure raw-evidence reader hardening, and paired traceability. No Framework/MRTS source or Gitlink, workflow, permission, NGINX broker, HAProxy artifact-upload, root-runtime, or dependency change. |

## Motivation and problem statement

Connector-specific runtime evidence previously had no common, versioned
contract that could make one strict decision without treating a successful CI
step or synthetic input as live runtime proof. This change introduces a
canonical observation schema and validator with one explicit evidence and
provenance model. It keeps missing Apache and HAProxy live producers
fail-closed, while preserving NGINX's separate protected boundary.

## Acceptance criteria

- Versioned schema, public `validate_runtime_observation()` API, and strict
  CLI accept only complete, identity-bound observations.
- One profile requirement matrix governs all four CRS/MRTS profiles and never
  promotes a missing `live_executed` fact to PASS.
- Envoy, Lighttpd, and Traefik structured evidence is adapted through the
  common validator; Apache and HAProxy remain fixture/interface-only.
- All 32 requested contract cases are covered, including identity, expected
  versus observed behavior, cleanup, profile, provenance, JSON, and safe-file
  negative controls.
- Evidence processing rejects symlinks, unsafe hardlinks and permissions,
  unsafe owners, non-regular objects, unsafe component directories, oversized
  files, duplicate JSON keys, and replacement races.
- No live six-connector-by-four-profile PASS is claimed without host evidence.

## Implementation decision and rationale

- `ci/runtime/contracts/runtime-observation.schema.json` is the versioned
  contract; `runtime_observation.py` exposes the shared API and strict policy
  result vocabulary; `validate-runtime-observation.py` is the CLI.
- Every profile carries full `parent_commit`, `framework_commit`, and
  `mrts_commit` identity. No-MRTS isolation facts stay false while the selected
  MRTS revision remains provenance.
- The strict policy recomputes digest-bound relative evidence under a private
  evidence root. `fixture` evidence is explicitly separate and cannot be
  smuggled into a strict live claim.
- `runtime_observation_adapters.py` contains only Envoy, Lighttpd, and Traefik
  live adapters. Apache and HAProxy have canonical fixtures but no lite live
  adapter; NGINX is represented as `protected-separate` without a broker change.
- The existing no-MRTS normalizer keeps connector-specific correlation, then
  emits and validates the canonical observation. Its raw reader now uses
  descriptor-relative no-follow traversal, owner/mode/link-count checks,
  `O_NONBLOCK`, bounded reads, and before/after state checks.

## Security impact

The change processes connector-produced JSON and filesystem evidence, so it
adds no-follow, regular-file, owner, writable-mode, link-count, size, duplicate
key, non-finite JSON, and exchange-race defenses. `FND-PARENT-0228` records a
validated pre-fix raw-reader gap and its focused local remediation. The strict
validator does not treat a test fixture, a command success, a raw log, or
self-consistent synthetic data as live runtime PASS evidence.

The focused workflow-security equality control fails closed for two existing
trusted workflows that are outside this task's workflow scope; this is retained
as `FND-PARENT-0111`, not remediated or suppressed here.

## Changed files

- `ci/runtime/contracts/__init__.py`
- `ci/runtime/contracts/runtime-observation.schema.json`
- `ci/runtime/contracts/runtime_observation.py`
- `ci/runtime/contracts/runtime_observation_adapters.py`
- `ci/runtime/contracts/validate-runtime-observation.py`
- `ci/runtime/contracts/README.md` and `ci/runtime/contracts/README.de.md`
- `ci/runtime/lifecycle/normalize-with-crs-no-mrts.py`
- `ci/README.md` and `ci/README.de.md`
- `tests/test_runtime_observation_contract.py`
- `tests/test_with_crs_no_mrts_runtime.py`
- `tests/fixtures/runtime-observation/apache-no-crs-no-mrts.json`
- `tests/fixtures/runtime-observation/haproxy-no-crs-no-mrts.json`
- This Change Record, its German companion, and both change-record indexes.

## Commands executed

The commands below use the configured project Python interpreter through RTK;
their observed outcomes are retained rather than inferred from a CI step.

## Tests and actual results

| Check | Actual result |
| --- | --- |
| `tests.test_runtime_observation_contract` + `tests.test_with_crs_no_mrts_runtime` | Passed: `107 tests in 35.534s`. |
| Focused raw-reader hardlink/owner/mode/FIFO/nonblocking and replacement controls | Passed: `7 tests`. |
| `tests.test_with_crs_no_mrts_runtime` legitimate-control suite | Passed: `54 tests in 27.829s`. |
| `py_compile` for all seven changed Python files | Passed: exit `0`. |
| `tests.test_runtime_path_security` | Passed: `21 tests in 2.230s`. |
| `tests.test_evidence_output_security` | Passed: `9 tests in 0.237s`. |
| `tests.test_bilingual_docs` | Passed: `22 tests in 0.288s`. |
| Existing CI-security baseline | Passed: `1 test in 70.580s`. |
| Workflow-security exact equality control | Failed closed on two pre-existing omitted workflow paths; tracked as `FND-PARENT-0111`, no workflow source changed. |
| `git diff --check` for the working change | Passed. |
| `make check-bilingual-docs` and `make check-doc-links` | Task-owned Change Record validation passed; each target remains blocked only by existing links into the intentionally uninitialized Framework submodule. |

## Runtime evidence

The recorded tests validate schema, API, adapters, provenance, and safe file
processing. They are not live host-runtime evidence. No full six-connector by
four-profile matrix was run, and this record makes no such PASS claim. Envoy,
Lighttpd, and Traefik normalizer tests use structured host-shaped evidence;
Apache and HAProxy retain only canonical fixtures until real producers exist.

## Checks not run and rationale

- A live six-connector by four-profile host matrix was not run; required
  connector hosts, provenance, and legitimate runtime evidence are not present
  in this local contract task.
- `make check-bilingual-docs` and `make check-doc-links` ran but cannot pass in
  this task worktree because existing repository documents link to the
  intentionally uninitialized Framework submodule. Framework initialization or
  modification is outside this task's authority, and no link or source control
  was weakened.
- The terminal Security-Diff report remains pending at record creation.

## Known limitations

The common validator can verify a private, digest-bound evidence contract but
cannot cryptographically attest a process that already has the same local UID
and private evidence-root authority. It therefore preserves the existing
trusted-runner boundary rather than claiming an unattainable proof of producer
identity. Apache and HAProxy live producers remain explicitly absent and
fail-closed.

## Remaining risks

`FND-PARENT-0111` remains a P1 workflow-governance blocker outside authorized
scope. Its two exact workflow paths require a separate, narrowly authorized
repair that preserves the finite allowlist and fail-closed negative control.
The current implementation adds no workaround, path exclusion, permission
change, or weakened security control.

## Final diff and review status

The source implementation and raw-reader remediation have focused regression,
full changed-Python compilation, task-owned bilingual-record, CI-security, and
working-diff evidence. The final delivery review must still seal the terminal
Security-Diff workflow and perform exact Draft-PR delivery preflight. No hosted
result or merge is asserted in advance.

## Delivery status

The user authorizes one independent Draft PR from
`codex/canonical-runtime-observation` against `master` after final validation.
No ready-for-review transition, merge, auto-merge, rebase, force-push, default-
branch push, Framework/MRTS change, or Gitlink update is authorized by this
record.
