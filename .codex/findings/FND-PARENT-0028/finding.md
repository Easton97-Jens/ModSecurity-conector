# FND-PARENT-0028 — SHA-pinned Parent scanner actions retain mutable Docker image dependencies

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0028 |
| Title | SHA-pinned Parent scanner actions retain mutable Docker image dependencies |
| Category | security_hardening |
| Repository | parent |
| Ownership | parent |
| Priority | P2 |
| Severity | medium |
| Confidence | confirmed |
| Status | triaged |
| Feasibility status | requires_user_decision |
| Security assessment | validated |
| Release blocker | false |
| Security relevance | true |
| Protocol/profile | GitHub Actions CI / OSV and OpenSSF Scorecard scanner workflows |

## Summary

The Parent pins the outer OSV and OpenSSF Scorecard Git Action repositories to
full commit SHAs, but the action metadata at those exact revisions executes
Docker images selected by mutable version tags. The outer Git SHA therefore
does not bind the final executable container payload.

## Observed behavior

At Parent `origin/master`
`c8ca0d92b630c18232b881855c4f5d1482568ea6`:

- `.github/workflows/ci-security-osv.yml` invokes
  `google/osv-scanner-action/osv-scanner-action` and
  `google/osv-scanner-action/osv-reporter-action` at
  `9a498708959aeaef5ef730655706c5a1df1edbc2`.
- The metadata at that exact Git revision declares `runs.using: docker` and
  `docker://ghcr.io/google/osv-scanner-action:v2.3.8` for both the scanner
  and reporter actions.
- `.github/workflows/ci-security-scorecard.yml` invokes
  `ossf/scorecard-action` at `4eaacf0543bb3f2c246792bd56e8cdeffafb205a`.
  Its exact `action.yaml` declares `runs.using: docker` and
  `docker://ghcr.io/ossf/scorecard-action:v2.4.3`.
- The OSV pull-request job and Scorecard default-branch job grant
  `security-events: write`.
- `ci/tooling/security-tools.lock.yml` records the outer Git SHAs, but no
  immutable identity for those nested images.

## Expected behavior

Every executable scanner payload must be bound to an immutable, independently
verifiable artifact identity. A full outer Git Action SHA alone is insufficient
when action metadata delegates execution to a mutable container tag. Job
permissions must remain minimal for the selected reporting mechanism.

## Impact

A later tag retargeting, compromised registry publisher, or registry supply-
chain incident can change the code executed by these jobs without changing the
Parent workflow or its outer action SHA. The affected jobs process repository
content and, in the noted contexts, can write security events. This record does
not claim that a retagging or compromise occurred.

## Affected files and symbols

### Files

- `.github/workflows/ci-security-osv.yml`
- `.github/workflows/ci-security-scorecard.yml`
- `ci/tooling/security-tools.lock.yml`

### Symbols and action metadata

- `google/osv-scanner-action/osv-scanner-action`
- `google/osv-scanner-action/osv-reporter-action`
- `ossf/scorecard-action`
- `runs.using: docker`
- `runs.image`

### Provenance

- Parent source commit: `c8ca0d92b630c18232b881855c4f5d1482568ea6`
- OSV action revision: `9a498708959aeaef5ef730655706c5a1df1edbc2`
- Scorecard action revision: `4eaacf0543bb3f2c246792bd56e8cdeffafb205a`

## Preconditions

- A Parent OSV or Scorecard workflow runs the named SHA-pinned outer action.
- GitHub Actions resolves the Docker image declared by that action metadata.
- The referenced image tag is retargeted, or its publisher/registry trust
  boundary is compromised, after the action Git revision was pinned.

## Reproduction

1. Run `rtk git show origin/master:.github/workflows/ci-security-osv.yml` and
   `rtk git show origin/master:.github/workflows/ci-security-scorecard.yml`.
2. Observe the full outer action SHAs and the OSV pull-request or Scorecard
   default-branch `security-events: write` permission.
3. Retrieve the action metadata at exactly
   `9a498708959aeaef5ef730655706c5a1df1edbc2` and
   `4eaacf0543bb3f2c246792bd56e8cdeffafb205a`; observe `runs.using: docker`
   and image values ending in `:v2.3.8` or `:v2.4.3`, not an image digest.
4. Compare the outer Git pin with the nested tag-resolution boundary: the
   workflow contains no immutable digest for the executed image.

## Evidence

- Run ID: `20260718T110742Z-fnd-parent-0028-mutable-action-images`
  - Artifact:
    `.codex/runs/20260718T110742Z-fnd-parent-0028-mutable-action-images/validation.md`
  - Type: `parent_ci_supply_chain_validation_receipt`
  - SHA-256:
    `2f1016917d0a0e1dc46bdd8901a4e4f6860d48ba5cdc25d0d0b698c7f16db732`
  - Command: `rtk git rev-parse origin/master`; RTK-mediated `git show` of
    the Parent OSV, Scorecard, and action-lock files; RTK-mediated retrieval
    of exact upstream action metadata at the pinned commits.
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`;
    observed `2026-07-18T11:07:42Z`; retention:
    `retained_local_evidence`.
- Source inventory:
  `.codex/runs/20260718T110742Z-fnd-parent-0028-mutable-action-images/source-inventory.json`
  (SHA-256
  `32714b3b8dab1eda6cbeadf365e2bdbdc969877221d6d166e684763833bac781`).
- Complete command record:
  `.codex/runs/20260718T110742Z-fnd-parent-0028-mutable-action-images/command-record.md`
  (SHA-256
  `c100a6e4fea8b27f48ab24d487a6b16996eac24fd775cc022b4e6732af0a5b2c`).

## Root-cause analysis

The Parent immutable-action policy and lock model record the outer Git
repository commit but do not model or verify the Docker image identity declared
inside Docker-backed action metadata. A Git SHA pin therefore stops at the
action-repository boundary, while the container runtime resolves a mutable tag
later.

## Proposed remediation

Create a separate Parent-owned remediation task. Prefer a checksum-verified
standalone OSV Scanner and Scorecard CLI from explicitly locked official
release assets, with task-specific no-token local output. If a Docker action
remains necessary, record and enforce an immutable image digest together with
provenance and renewal validation. Remove `security-events: write` where local
JSON/advisory reporting does not require SARIF upload; preserve only
permissions required by the selected behavior.

## Acceptance criteria

- The Parent OSV and Scorecard execution paths no longer resolve a mutable
  container tag at job runtime.
- Every executed scanner artifact has an exact immutable identity with retained
  provenance and verification evidence.
- The Parent lock/contract detects a future mutable nested Docker image
  dependency or documents the verified immutable replacement mechanism.
- Job permissions are limited to the selected reporting path;
  `security-events: write` exists only when a verified SARIF-upload path
  requires it.
- Focused contract tests, actionlint/ShellCheck, Zizmor, scanner control cases,
  exact-head CI, CodeQL, security checks, Scorecard, SonarQube Cloud, reviews,
  and review-thread checks pass on the Parent remediation PR.

## Validation plan

- Before any Parent source change, revalidate the exact Parent master workflow
  source and nested action metadata/image identity.
- Add a focused Parent CI-security contract test that fails for a Docker-backed
  scanner action with a mutable tag and passes for the chosen immutable
  replacement.
- Run Parent CI-security contract checks, actionlint/ShellCheck, offline
  Zizmor, Gitleaks/OSV/Scorecard legitimate controls, and documentation/change-
  record checks.
- For the Parent remediation PR, verify local SHA = remote SHA = PR head, then
  inspect exact-head CI, CodeQL, security checks, Scorecard, SonarQube Cloud,
  reviews, and unresolved review threads.

## Regression tests

- A Parent CI-security contract test rejects mutable nested Docker image tags
  for OSV and Scorecard execution paths.
- The Parent immutable-action registry/contract test covers the replacement
  artifact identity.
- A negative fixture proves an outer Git SHA does not falsely satisfy the
  nested-image invariant.

## Legitimate control tests

- The selected OSV scan still analyzes the intended dependency scope and
  reports its documented result.
- The selected Scorecard check still produces the documented local or SARIF
  result under only the permissions it needs.
- A known-safe workflow fixture with immutable scanner artifact identity passes
  the focused contract.

## Dependencies

- A separately authorized Parent-owned CI remediation task and delivery
  lifecycle.

## Blockers

- The active Framework CI-security task expressly excludes Parent product and
  workflow changes.

## Related findings and deduplication

- `FND-PARENT-0018`
- `FND-GITHUB-0001`
- This is not a duplicate of `FND-PARENT-0018`: that record concerns outer
  CodeQL action-version and registry consistency, while this record concerns
  mutable executable Docker image resolution inside separately SHA-pinned OSV
  and Scorecard action metadata.

## Residual risk

The current Parent workflows retain the nested mutable image-tag boundary until
a separately authorized Parent remediation is verified. The full outer Git SHAs
remain a partial control but do not bind the executed image. No risk has been
accepted.

## History

- `2026-07-18T11:07:42Z`:
  `validated_nested_mutable_docker_image_dependency` — current Parent OSV
  scanner/reporter and Scorecard workflows were inspected at
  `c8ca0d92b630c18232b881855c4f5d1482568ea6`. Exact upstream action metadata
  at their outer Git SHAs resolves v2.3.8 and v2.4.3 Docker image tags rather
  than immutable digests. No product, Git, Framework, or MRTS change was made.
