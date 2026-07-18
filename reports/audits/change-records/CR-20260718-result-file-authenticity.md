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

The full-matrix generator retains `job_id`, `verified_run_id`, status, hashes,
inputs, and outputs when it rewrites the raw manifest so the strict consumer
can compare source and derived records. The lifecycle producer adds the
structured result JSONL path and hash to its job receipt. The verified-run
manifest excludes its own overwritten files from its generated-output hash
list, preventing a self-referential stale hash after regeneration.
The report-refresh producer emits every aggregate input-status collection as a
typed list, so a future valid record has the same schema the strict consumer
requires.

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

| Command | Result |
| --- | --- |
| Initial fixture-first `unittest` run before the strict-chain implementation | Failed as expected: eight fixtures reached the absent strict-chain control and the critical missing-input status was not rejected. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_generated_report_evidence_integrity` after the implementation | Passed: forged `PASS` result content/checksum mismatch, missing raw manifest, incomplete receipt, foreign run ID, copied connector/profile receipt, leaf and intermediate escaped/symlinked paths, missing/invented/malformed critical input status, typed producer arrays, raw-manifest preservation, self-reference prevention, and a valid twelve-cell control are covered. |
| `rtk sh -n ci/runtime/lifecycle/run-full-matrix-parallel.sh` | Passed. |
| In-memory `compile()` validation of the three changed Python sources | Passed without attempting checkout-local bytecode writes. |
| Strict `make verified-report-evidence-gate` against retained evidence | Expected failure: it rejects critical missing input states and noncanonical/missing command receipts. Existing `FND-CROSS-0001` stale Cross evidence remains a separate fail-closed blocker. |
| Governance-only generated-report layout check against retained evidence | Passed: governance-only mode is not a runtime-evidence assertion. |
| `rtk git diff --check` | Passed. |

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
trusted producer aggregate receipt and is tracked separately as
`FND-PARENT-0031` on its own stacked Parent branch; this Change Record does
not claim to close that producer-authenticity boundary.

## Checks not run and rationale

A full connector/runtime matrix needs the separately provisioned runtime
components and authoritative Framework harness, which are unavailable in this
isolated worktree. That absence does not authorize a synthetic success or a
governance-only substitute. Full exact-head CI, CodeQL, SonarQube Cloud, and
review verification are required after the draft PR is created. No merge is
authorized.

## Final diff and review status

The source change has focused negative/control tests, shell syntax validation,
and whitespace-diff validation. It remains `remediation_required` until its
own exact draft-PR head has been pushed and independently verified. No runtime
evidence or merge claim is made.
