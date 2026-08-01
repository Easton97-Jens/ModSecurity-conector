# Finding: Strict runtime evidence lacks a detached producer receipt for full-matrix artifacts

**Language:** English | [Deutsch](finding.de.md)

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-PARENT-0031` |
| Status | `closed` (archived) |
| Priority / severity | `P1 / high` |
| Owner | Parent |
| Root-control boundary | producer authenticity; result-file authenticity; run identity |
| Release blocker | no |

## Summary

The strict consumer recomputes a leaf result hash but trusts the mutable
`job.json` and raw-matrix row that declare the same hash. A forged `PASS`
result with synchronized mutable receipt fields therefore passes the current
strict chain.

## Evidence and reproduction

In a complete temporary twelve-cell Parent fixture, a result JSONL was replaced
with forged `PASS` content and its hash was updated in the matching
`job.json` and raw-matrix row. The strict artifact-chain verifier returned no
errors. The retained reproduction target is recorded in `finding.json`; it
will be sealed before delivery.

## Root cause

`verified-commands.json` proves that the full-matrix command completed but
does not bind the raw matrix, every job receipt, or each required leaf artifact.
The strict checker compares mutable documents that can be rewritten together.

## Delivered remediation and current PR evidence

PR #59 exact head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` now contains the
canonical per-run aggregate receipt under
`verified-runs/<run-id>/`, binds it into the verified run manifest, and
validates it before accepting raw/job/leaf records. It covers paired and
alternate rewrites, foreign generator run IDs, a legitimate resumed run, and a
valid twelve-cell control. `FND-PARENT-0037` separately hardens the helper's
intermediate-path race in the same user-authorized combined PR. Current
non-skipped CI, CodeQL, Sonar Quality Gate, and zero review/thread gates passed
before a protected squash merge to Parent master
`5a22cbf5206dbc2b7f53a9f961d72e37d567e188`. The exact resulting-master
reproduction passed 57/57 evidence-integrity controls, 11/11 bilingual
controls, shell syntax, and diff hygiene. This finding is verified, not
closed.

## Acceptance criteria

- A paired result/job/raw receipt forgery is rejected.
- The detached aggregate receipt is regular, schema-valid, and bound to the
  current run; descriptor-relative path confinement is tracked by
  `FND-PARENT-0037`.
- A valid complete twelve-cell control run is accepted.
- The user-authorized combined Parent Draft PR retains distinct finding
  traceability; no Framework/MRTS change or merge occurs.

## Scope and dependency

This is Parent-owned and is not a duplicate of `FND-PARENT-0030`: that finding
establishes strict consumer path/status/hash checks, while this one establishes
the separate producer-authenticity anchor. The current user explicitly permits
one combined/stacked #59 delivery candidate, but `FND-PARENT-0030`,
`FND-PARENT-0031`, and `FND-PARENT-0037` remain independently tracked,
verified, and not closed.

## Residual risk

The receipt chain is not a signature, ACL, process-identity, UID-isolation, or
external-attestation boundary. Mode `0400` limits group/other access only; an
actor with arbitrary same-UID write access to the Parent evidence namespace is
outside this local filesystem trust model. No risk is accepted. The exact
source-head gate and resulting-master original reproduction are verified. Real
current runtime evidence remains separately blocked by `FND-CROSS-0001`.
`FND-SONAR-0001` separately fails the global master Quality Gate; it is neither
accepted nor attributed to this finding.

## Current retained post-merge evidence

`pr59-5a22cbf-postmerge-validation.json` in run
`20260720T141403Z-pr55-pr59-master-integration-8a0b8640`, SHA-256
`7749e6c6fd1ab198b54eb9704221d30aa150954db6130bec0317801a8afddc51`, records
the exact source head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151`, protected
squash master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`, current gates, and
the post-merge original-reproduction and legitimate-control results.

## History

- `2026-07-20T09:57:03Z` — fixed_on_current_pr_head: #59 head
  `d4f88b886dac6fd5f483940015d6310bc239f814` contains the detached receipt and
  the related descriptor-relative fix. It is still Draft/behind current master,
  so the finding remains release-blocking pending normal synchronization,
  exact-head revalidation, authorized merge, and post-merge reproduction.
- `2026-07-20T15:13:08+00:00` — verified_on_resulting_parent_master: current
  source-head gates passed and #59 was protected-squash-merged from
  `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` to
  `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`. The retained 57/57
  original-reproduction/legitimate-control suite includes paired mutable
  result/job/raw and alternate rewrite rejections; 11/11 bilingual,
  shell-syntax, and diff controls also passed. `FND-SONAR-0001` remains
  independent and unaccepted; this finding is closed by the current user after current-master validation.

- `2026-07-26T14:09:02Z`: `closed_by_current_user_after_current_master_unchanged_path_validation` — affected paths are unchanged from verified master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` through `6ca7e1536ce7e93da68099db9c586b88852ff13e`; `tests.test_generated_report_evidence_integrity` passed in the 144-test control suite.
