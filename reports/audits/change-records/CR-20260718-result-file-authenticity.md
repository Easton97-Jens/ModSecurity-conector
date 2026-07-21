# Change Record: Strict runtime result-file authenticity

**Language:** English | [Deutsch](CR-20260718-result-file-authenticity.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260718-result-file-authenticity` |
| Date (UTC) | `2026-07-18` |
| Base revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Finding | `FND-PARENT-0030` |
| Boundary | Parent strict report-evidence checker, full-matrix receipts, lifecycle producer, focused tests, and documentation only; Framework and MRTS are unchanged. |

## Motivation and problem statement

The strict report-evidence gate accepted critical `missing` input status and
missing-input lists. It also trusted derived report records without
independently validating the detached full-matrix command receipt, raw matrix
manifest, job identities, canonical artifact paths, or result-file hashes. A
preplaced `PASS` result file or copied job receipt could therefore contribute
to a report without a strict source-of-truth receipt check.

## Acceptance criteria

- Strict mode accepts only schema-approved critical runtime input states:
  `complete`, plus the documented self-generated exception for the refresh
  manifest; missing, empty, unknown, partial, stale, blocked, failed,
  interrupted, skipped, and invented positive-looking values are rejected.
- A verified full run has one valid run ID, one required full-matrix producer
  command, and exactly the twelve connector/CRS/MRTS job identities.
- The strict consumer accepts only the Parent runner's emitted terminal
  full-matrix states `runtime_completed` and
  `runtime_completed_with_mismatches`, never a similarly named ad-hoc state.
- Every job receipt is bound to the selected run ID, connector, CRS variant,
  MRTS variant, canonical job root, and structured completion state.
- Logs, build manifests, summaries, and result JSONL files are regular,
  canonical files with matching receipt hashes; leaf and intermediate escaped
  paths or symlinks fail closed.
- A receipt-provided summary path can select only one of the two prebuilt
  canonical summary locations; it never becomes a filesystem path used for a
  read, `stat`, or hash operation.
- Critical input receipts are canonically resolved before root containment is
  compared, so `BUILD_ROOT:../...`, `framework:../...`, and unprefixed
  `../...` cannot authenticate an external regular file even when its declared
  SHA-256 matches.
- The raw full-matrix manifest preserves receipt identity and hash fields and
  exactly matches the per-job receipts.
- A forged result file, foreign run, copied connector/profile receipt,
  missing raw manifest, incomplete job, and invalid critical report status are
  rejected; a complete valid control run remains accepted.

## Implementation decision and rationale

The strict checker now validates detached runtime receipts before accepting
derived report claims. It accepts only a positive, report-name-aware input
status schema. It anchors the command receipt at the selected runtime build
root, then verifies the run ID, profile, required full-matrix command, raw
12-cell matrix set, each canonical job location, and each structured
artifact’s SHA-256 value. Free-form receipt paths cannot redirect the checker:
they must equal the expected lexical canonical location and be regular files
without a symlink component below the evidence root.

For summary artifacts, the checker derives both allowed locations from the
enumerated connector and canonical job root before it examines receipt data.
The receipt can only select the direct or `force-all` canonical branch; it
cannot construct the path that is read, stat'ed, or hashed. This preserves the
two supported producer layouts while removing receipt-to-filesystem-path data
flow.

Critical-input receipts use the same fail-closed boundary: the checker resolves
the claimed path and trusted root before containment comparison, then still
rejects leaf and intermediate symlink components. This prevents a lexical
`..` component from retaining a trusted prefix while the filesystem operation
reaches an external file.

The full-matrix generator retains `job_id`, `verified_run_id`, status, hashes,
inputs, and outputs when it rewrites the raw manifest so the strict consumer
can compare source and derived records. The lifecycle producer adds the
structured result JSONL path and hash to its job receipt. The verified-run
manifest excludes its own overwritten files from its generated-output hash
list, preventing a self-referential stale hash after regeneration.
The report-refresh producer emits every aggregate input-status collection as a
typed list, so a future valid record has the same schema the strict consumer
requires.

The focused raw-matrix fixture updates its JSONL record from the complete
in-memory twelve-job collection it constructed; it does not reread a serialized
fixture record before rewriting the fixed fixture manifest. This keeps the
direct-summary and hash-mismatch controls intact while keeping the fixture
rewrite boundary explicit.

## Security impact

This Parent result-file-authenticity and report-consumer hardening turns report
claims into a checked chain from a canonical runtime command receipt through a
complete raw job matrix and job-local artifacts. It does not independently
establish a connector host, process, request/response traffic, CRS, MRTS, or
Framework claim. Authoritative host-lifecycle and Framework integration
bindings remain separate boundaries and are unchanged here.

## Changed files

- `ci/checks/documentation/check-generated-report-layout.py`
- `ci/evidence/reports/generate-full-matrix-job-completeness.py`
- `ci/evidence/reports/refresh-connector-reports.py`
- `ci/runtime/lifecycle/run-full-matrix-parallel.sh`
- `ci/runtime/lifecycle/run-verified-report-run.py`
- `tests/test_generated_report_evidence_integrity.py`
- this English/German Change Record pair and its README index links

## Commands executed

For the focused Python commands, `PARENT_PYTHON` denotes the explicitly
selected Parent virtual-environment interpreter at
`/absolute/path/to/ModSecurity-conector/.venv/bin/python`; the isolated PR
worktree does not create or own a second virtual environment.

| Command | Result |
| --- | --- |
| Initial fixture-first `unittest` run before the strict-chain implementation | Failed as expected: eight fixtures reached the absent strict-chain control and the critical missing-input status was not rejected. |
| Fixture-first critical-input traversal control before canonical containment | Failed as expected: `BUILD_ROOT:../...`, `framework:../...`, and unprefixed `../...` each accepted a correctly hashed external regular file without a strict-check error. |
| `rtk proxy /usr/bin/env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 "$PARENT_PYTHON" -m unittest -v tests.test_generated_report_evidence_integrity` after the implementation | Passed: 35 tests cover forged `PASS` result content/checksum mismatch, missing raw manifest, incomplete receipt, foreign run ID, copied connector/profile receipt, leaf and intermediate escaped/symlinked paths, canonicalized critical-input traversal, missing/invented/malformed critical input status, manifest and metadata input digest mismatch, direct and `force-all` summary selection plus hash rejection, summary/JSONL fallback selection, typed producer arrays, raw-manifest preservation, self-reference prevention, and a valid twelve-cell control. |
| `rtk sh -n ci/runtime/lifecycle/run-full-matrix-parallel.sh` | Passed. |
| In-memory `compile()` validation of the three changed Python sources | Passed without attempting checkout-local bytecode writes. |
| Strict `make verified-report-evidence-gate` against retained evidence | Expected failure: it rejects critical missing input states and noncanonical/missing command receipts. Existing `FND-CROSS-0001` stale Cross evidence remains a separate fail-closed blocker. |
| Governance-only generated-report layout check against retained evidence | Passed: governance-only mode is not a runtime-evidence assertion. |
| `rtk proxy /usr/bin/env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` after the post-merge factual-currency correction | Passed: the updated English/German Change Record pair remained structurally and bilingually valid. |
| `rtk git diff --check` | Passed for the original strict-chain change and again for the post-merge factual-currency correction. |

## Runtime evidence

Not established. The focused fixtures create synthetic files only to validate
consumer rejection and control semantics. No real connector host, process
lifecycle, request traffic, CRS, MRTS, or integration-mode run was started or
claimed.

## Known limitations

This isolated Parent remediation cannot close Framework-owned producer or
host-lifecycle findings. Synthetic-probe host binding and authoritative
Phase-4 integration binding remain separately tracked Framework handoffs. The
retained reports intentionally remain strict-gate failures because Cross
runtime evidence is stale.

## Remaining risks

Independent review also reproduced a paired rewrite of a result JSONL, its
mutable job receipt, and its mutable raw-matrix row. That requires a detached
trusted producer aggregate receipt and is addressed by `FND-PARENT-0031`; the
aggregate-receipt intermediate-directory follow-up is `FND-PARENT-0037`.
Both were delivered with `FND-PARENT-0030` in the user-authorized
combined/stacked, Parent-only PR #59. Their current canonical findings are
`verified`; this Change Record does not claim that P0030 alone closes either
boundary.

## Checks not run and rationale

A full connector/runtime matrix needs the separately provisioned runtime
components and authoritative Framework harness, which are unavailable in this
isolated worktree. That absence does not authorize a synthetic success or a
governance-only substitute. The observed prior exact-head validation for Draft
Parent PR #59 at `d4f88b886dac6fd5f483940015d6310bc239f814` had 33 successful
and six skipped checks, with CodeQL and the SonarQube Cloud Quality Gate
passed. That evidence applies only to
`d4f88b886dac6fd5f483940015d6310bc239f814`. PR #59's final source head
`b9b22cc36958ba506278f3aa3fbc1d383ea6a151` was merged through the protected
squash path into Parent `master` as
`5a22cbf5206dbc2b7f53a9f961d72e37d567e188` at
`2026-07-20T15:09:01Z`; PR #59 is therefore no longer a Draft and its
Parent-master integration is no longer pending. Those observed delivery facts
do not invent missing runtime evidence: no full connector/runtime matrix,
Framework or MRTS test, or task-owned Gitlink change is claimed by this Change
Record, and no check was bypassed.

`make check-doc-links` was not run for this narrow record correction because
its documented target invokes the excluded Framework documentation checker.
`make check-bilingual-docs` is the applicable Parent-only documentation check.

This candidate also contains the narrow, behavior-preserving `FND-SONAR-0006`
remediation for all eight then-current PR SonarQube Cloud maintainability code
smells: helper extraction in the strict consumer, aggregate-receipt generator
and runner, a constant for repeated run-ID diagnostics, and a more precise
tamper assertion. The fresh local 57-test receipt-integrity suite, `sh -n`,
the bilingual check, and `git diff --check` passed. No receipt, path, hash, or
TOCTOU control is changed or suppressed. The final PR source head received a
successful SonarQube Cloud PR analysis with zero new issues, zero security
hotspots, and `0.0%` duplication on new code; the current master-wide Quality
Gate state remains an independent assessment.

## Final diff and review status

Parent PR #59 was the user-authorized combined/stacked, Parent-only delivery
for `FND-PARENT-0030`, `FND-PARENT-0031`, and `FND-PARENT-0037`. Its final
source head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` was merged through the
protected squash path into Parent `master` as
`5a22cbf5206dbc2b7f53a9f961d72e37d567e188` at `2026-07-20T15:09:01Z`.
The current canonical finding records mark all three remediations `verified`.
The previously validated head `d4f88b886dac6fd5f483940015d6310bc239f814`
remains historical evidence at its own scope. No Framework, MRTS, or
task-owned Gitlink change is claimed; this factual-currency correction does
not alter the underlying remediations or their security controls.
