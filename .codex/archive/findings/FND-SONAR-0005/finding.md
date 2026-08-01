# FND-SONAR-0005 — Framework PR #29 SonarQube Quality Gate failed on workflow-checker path containment and complexity findings

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-SONAR-0005` |
| Category | `sonarqube_finding` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity | `P1` / `not_applicable` |
| Confidence / status | `validated` / `verified` |
| Feasibility | `feasible_now` |
| Release blocker | `false` |
| Security relevant | `true` |

## Summary and observed behavior

Exact Framework PR #29 head
`191b7e3d1999c7ffb39ad16bfaff7821bfc09825` failed SonarCloud Check Run
`88075927543` on `2026-07-18T11:33:49Z`. The Quality Gate reported Security
Rating C on New Code where A is required and emitted eleven annotations in
`ci/checks/security/check-github-actions-workflows.py`. Failure-level
annotations were at lines 122, 126, 284, and 313; the remaining warnings were
at lines 32, 38, 48, 51, and 198, with two distinct annotations at lines 38
and 48.

The normal current-master reconciliation and focused remediation first passed
SonarCloud at exact PR head `fdb400b85bfd2779e95cc3ab8fb29a3e2e3793bf` without
suppression. The final synchronized PR head
`5fa814d19b86f5c0a406b95914d6121af83ffe07` then passed all ten fresh PR checks,
including SonarCloud Code Analysis, CodeQL Actions/C++/Python, scaffold-lint,
and common-structure. It had no reviews or review threads. It squash-merged as
Framework master `7a12073c28e62a67492dd501b6513b9914fe5df8` at
`2026-07-19T15:12:26Z`; the final PR and master tree are both
`25dae479a3f23e12a69db0ef9e034edae218f6d9`. The resulting master reran the
original workflow-security and legitimate-control matrix successfully, so this
record is `verified`, not `closed`.

## Expected behavior, impact, and scope

The canonical workflow-security checker must recursively scan nested
`.yml`/`.yaml` files and resolve every supplied root, discovered candidate, and
read target beneath the invocation repository root. It must reject outside
roots and symlink escapes while retaining strict YAML parsing and every
workflow trust-boundary control.

The Quality Gate failure was a required external integration blocker. The
affected validator is security-relevant, but the evidence does not establish a
separately exploitable product vulnerability; security severity is therefore
`not_applicable`. The exact fresh PR-head and resulting-master evidence prove
that this specific gate failure no longer reproduces. This remains
Framework-only scope: it does not authorize a Parent product/gitlink change or
any MRTS action. `FND-SONAR-0002` is a separate accepted-risk default-branch
backlog and explicitly did not waive the fresh PR-head gate.

## Evidence, root cause, and remediation

The retained receipt
`/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/pr29-fdb400b-sonar-remediation.md`
has SHA-256
`65ce440af9e7ee53221ef36980581bad5f66e9e3273bf611135ceabcf8c9a8ee`. It
records the historical failure, all annotation locations, the source-level
remediation, and the exact-head success. It was collected with the GitHub
Checks API commands for old check `88075927543`, its annotations, and commit
`fdb400b…`, all from the Parent root with exit code 0.

The root cause was a missing single resolved repository-root containment
boundary across every requested, discovered, and read workflow path, plus
tightly coupled scanning helpers that produced constructed-path and cognitive-
complexity scanner findings. The remediation resolves the repository root and
workflow paths strictly, confines candidates beneath the workflow root,
recursively discovers YAML files, rejects explicit outside roots and escaping
symlinks, revalidates before reading, and decomposes `source_uses` and
`validate_permissions`. It adds nested-workflow, outside-root, and symlink-
escape regressions without scanner suppression, exclusion, Quality Gate
modification, workflow disablement, or security-control weakening.

The immutable post-merge receipt
`/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/fnd-sonar-0005-pr29-master-verification.md`
has SHA-256
`ad53a13fb5d9c8364da23433c0caabe9dd5a980e007413505d84bb1eb7944171`. It was
observed at `2026-07-19T15:16:31Z`, retained as task evidence, and records the
final exact PR head, merge/master/tree identities, tree equality, and the
native master validation in
`/var/tmp/codex/worktrees/framework-workflow-hardening` (exit code 0). The
native full lint passed all seven workflow-security contract tests—including
nested discovery, explicit outside-root rejection, and symlink-escape
rejection—plus twenty-one Action-pin tests, ten CRS provenance tests, and the
remaining repository-native controls.

## Acceptance criteria and validation

- Retain the historical exact-head failure and its eleven annotations with a
  hash-addressed receipt.
- Prove nested discovery, outside-root rejection, and symlink-escape rejection
  with the focused workflow-security regression suite, while retaining existing
  YAML, permissions, token, checkout, pull-request-target, and Action-pin
  controls.
- Observe all ten passing fresh checks at final exact PR head `5fa814d…`,
  including SonarCloud, without changing scanner policy or suppressing a rule,
  and confirm the absence of reviews and review threads.
- On Framework master `7a12073c…`, establish final-PR/master tree equality and
  rerun the original reproduction and legitimate controls successfully.
- Observe successful master CodeQL C++/Actions/Python, scaffold-lint, and
  common-structure checks. Master SonarCloud check `88207281607` failed with
  Security E and Reliability D and zero annotations only under separately
  accepted `FND-SONAR-0002`; this is not a fresh PR-head waiver.

## Residual risk and history

The historical PR #29 Sonar gate condition is verified remediated on Framework
master. The separate master-only SonarCloud check `88207281607` remains
accepted-risk `FND-SONAR-0002` with Security E, Reliability D, and zero
annotations; it neither waives nor reopens this finding. `FND-SONAR-0005` is
verified on master but not closed: the original failure/remediation evidence
remains retained, and a future lifecycle closure requires separate
authorization. `2026-07-18T11:33:49Z`: historical exact-head failure
validated. `2026-07-19T14:18:07Z`: non-suppressive remediation passed the
first exact PR-head gate. `2026-07-19T15:12:26Z`: final head `5fa814d…`
merged as `7a12073c…`. `2026-07-19T15:16:31Z`: tree-equality and native master
controls completed successfully; status advanced to `verified`.
