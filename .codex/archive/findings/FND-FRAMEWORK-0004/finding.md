# FND-FRAMEWORK-0004 — Mutable Git source references can reach Framework provisioning consumption

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0004` |
| Category | `security_validated` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity / confidence | `P2` / `medium` / `validated` |
| Status | `verified` |
| Release blocker / security relevance | `false` / `true` |
| Final disposition | `verified_on_framework_master_not_closed` |

## Summary

Framework provisioning now binds CRS consumption to the centrally approved literal
HTTPS origin and reviewed lower-case 40-character commit. Mutable caller selectors
cannot select CRS content, and fetch, resolution, and checkout identities are
verified before consumption.

## Observed and expected behavior

Before remediation, `CRS_GIT_REF=main` could reach a Git source-ref selector.
The current master tree rejects divergent `CRS_REPO_URL` and `CRS_GIT_REF` values
before Git; a fresh repository fetches only the approved full commit and verifies
`FETCH_HEAD`, resolved object, and final `HEAD`.

CRS provisioning may consume only the centrally approved literal HTTPS origin and
lower-case 40-character immutable commit. The release label is metadata, never a
Git content selector. Existing source paths, origin mismatch, identity mismatch,
and `.gitmodules` declarations fail closed.

## Impact

The verified boundary prevents caller-controlled selectors, mutable tags or
branches, and ref-namespace spellings from selecting the CRS source tree consumed
by Framework provisioning and rule preparation.

## Affected files and symbols

- `modules/ModSecurity-test-Framework/ci/lib/common.sh`
- `modules/ModSecurity-test-Framework/ci/provisioning/fetch-crs.sh`
- `modules/ModSecurity-test-Framework/tests/security_regression/test_crs_git_ref_provenance.py`
- `modules/ModSecurity-test-Framework/docs/reference/variables.md`
- `modules/ModSecurity-test-Framework/docs/reference/variables.de.md`
- `modules/ModSecurity-test-Framework/docs/testing-and-evidence.md`
- `modules/ModSecurity-test-Framework/docs/testing-and-evidence.de.md`
- `modules/ModSecurity-test-Framework/reports/audits/change-records/20260718-01-fix-framework-crs-ref-provenance.md`
- `modules/ModSecurity-test-Framework/reports/audits/change-records/20260718-01-fix-framework-crs-ref-provenance.de.md`

Symbols: `F-DISC-01-02`, `CRS_APPROVED_REPO_URL`, `CRS_APPROVED_COMMIT`,
`CRS_RELEASE_TAG`, `ci_require_full_git_commit`,
`require_approved_crs_provenance`, `crs_git`, and `provision_fresh_crs`.

## Preconditions and reproduction

- Retained assessment, local revalidation, and PR #26 master-verification
  evidence remain available.
- Final PR #26 head: `465766c01e2bb0a9a003cfcefa8afca5fceeafe0`; current
  Framework master: `36cac3029c735dddf9f717b3ce077b9285567a6a`.
- Post-merge validation worktree:
  `/var/tmp/codex/ModSecurity-test-Framework/worktrees/fw-crs-ref-provenance`.
- Parent gitlink and MRTS remain outside this Framework-only delivery.

The original retained assessment is at
`.codex/reports/repository-full-assessment.md:221-227,238-244`. The current
negative reproduction runs `CRS_GIT_REF=main` through the process-boundary
fake-Git fixture and returns `77` before Git use. The focused master check was:

```text
rtk env BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/tmp/pr26-master-lint-build PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/tmp/pr26-master-lint-build/pycache python3 -m unittest discover -s tests/security_regression -p test_crs_git_ref_provenance.py -v
```

## Evidence

1. `20260716T193351Z-repository-full-assessment-0cb855ad` —
   `.codex/reports/repository-full-assessment.md:221-227,238-244`; type
   `bilingual_assessment_report`; SHA-256
   `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`;
   `sed -n '221,227p;238,244p' .codex/reports/repository-full-assessment.md`;
   `/root/git/ModSecurity-conector`; exit `0`; observed
   `2026-07-16T22:46:50Z`; `retained_local_report`.
2. `20260718T092708Z-fnd-framework-0004-crs-ref-provenance-05f04893` —
   `/var/tmp/codex/ModSecurity-conector/runs/20260718T092708Z-fnd-framework-0004-crs-ref-provenance-05f04893/evidence/fnd-framework-0004-local-validation.md`;
   type `framework_security_revalidation_and_delivery_evidence`; SHA-256
   `cc8e2a5292c47b416482acaaf8e6c1e5336b90ba6aa9e2e7d791c2fd3ab20757`;
   focused provenance regression, exact-head Draft-PR CI, SonarCloud, and
   security revalidation; worktree above; exit `0`; observed
   `2026-07-18T10:41:10Z`; `retained_local_evidence`.
3. `20260719T081017Z-framework-pr-resolution-20260719-840082e0` —
   `/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/fnd-framework-0004-pr26-master-verification.md`;
   type `framework_pr26_master_verification_receipt`; SHA-256
   `d64b00219a95d4cbdb550d4af2abc5c9b248cb493796c3cd84301674f6f76f9a`;
   exact-head/master verification, tree/diff/MRTS comparison, focused CRS
   checks, documentation check, and lint; worktree above; exit `0`; observed
   `2026-07-19T15:00:59Z`; `retained_local_evidence`.

## Root cause and remediation

The CRS provisioning path accepted the mutable `CRS_GIT_REF` release tag as a
Git source selector and detached `FETCH_HEAD` without binding consumption to a
reviewed immutable commit identity.

The remediation centralizes approved origin, release metadata, and full-commit
constants; rejects divergent selectors before Git; validates the full commit;
uses an isolated Git invocation and a fresh source path; fetches only the literal
commit; compares `FETCH_HEAD`, resolved object, and `HEAD`; and fails closed for
`.gitmodules`.

## Acceptance criteria and validation

- Provisioning uses only the literal approved HTTPS origin and lower-case
  40-character full commit.
- Tags, branches, ref namespaces, abbreviated hashes, divergent environment
  selectors, inherited Git controls, existing source paths, and `.gitmodules`
  declarations fail closed before CRS content is consumed.
- The fresh approved-origin control verifies `FETCH_HEAD`, resolved object,
  detached checkout, and final `HEAD` without a submodule command.
- Final PR #26 passed all fresh-head checks: CodeQL Actions/C++/Python, two
  `scaffold-lint` jobs, two `common-structure` jobs, and SonarCloud Code
  Analysis; there were no blocking reviews or review threads.
- PR #26 merged at `2026-07-19T14:29:48Z`; final head
  `465766c01e2bb0a9a003cfcefa8afca5fceeafe0` and resulting master
  `36cac3029c735dddf9f717b3ce077b9285567a6a` have tree
  `75d90508ca6576ae3595010c52f2fd32cfa662c3`.
- Current-master `git diff --quiet`, `git diff --check`, and MRTS comparison
  passed. The focused provenance suite passed `10` tests, including the original
  `main` rejection and fresh approved-origin/full-commit control.
- `rtk make -s check-documentation` passed. `rtk make -s lint` passed with its
  bytecode cache redirected to task-owned external storage; the unredirected
  retained-worktree attempt only encountered its read-only `__pycache__` path.

Framework master SonarCloud run `88203518811` failed separately under
`FND-SONAR-0002` accepted risk. It does not waive, replace, or reinterpret the
successful fresh PR-head SonarCloud result for this finding.

## Regression and legitimate control tests

`tests/security_regression/test_crs_git_ref_provenance.py` passed `10` focused
mocked Git/provenance tests on the current master tree. The process-boundary
fake-Git fixture accepts only the approved literal origin and
`55b09f5acfd16413e7b31041100711ceb7adc89c`, then observes exact fetch,
resolution, detached checkout, and final-HEAD verification.

## Dependencies, blockers, related findings, and residual risk

- Dependencies: none.
- Blockers: none.
- Related finding: `FND-FRAMEWORK-0003`.
- Residual risk: the approved commit is not independently verified through a
  signed release-attestation chain; the control relies on the centrally reviewed
  literal and HTTPS/TLS Git transport. It also assumes trusted Framework code,
  `CI_ROOT`, Git binary/`PATH`, TLS trust store, and exclusive source-root
  ownership.

## History

- `2026-07-17T10:43:59Z`: `bootstrap_created` — retained evidence created the
  finding; no remediation, verification, closure, or risk acceptance occurred.
- `2026-07-18T08:09:21Z`: `root_cause_triaged` — static evidence at
  `cdc91a398d6c156eaff927d742b23018a3817fb6` confirmed the separate CRS
  mutable-ref provenance gap.
- `2026-07-18T10:41:10Z`: `local_fix_revalidated` — the Framework worktree
  passed focused mocked regression, shell/documentation, direct pinning, lint,
  exact-head CI, SonarCloud, and security revalidation before the final
  documentation correction.
- `2026-07-19T15:00:59Z`: `verified_on_master` — PR #26 merged as current
  Framework master; the original negative reproduction and legitimate control
  reran successfully. The finding is verified, not closed.
