# Change Record: CodeQL Action 4.37.2 batch

**Language:** English | [Deutsch](CR-20260722-codeql-action-4-37-2-batch.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260722-codeql-action-4-37-2-batch` |
| Date (UTC) | `2026-07-22` |
| Base revision | `1e5e2fefce12ef455f4fdbc9a0afb7bb09ab4e7d` |
| Boundary | Parent CI security and traceability only; Framework, MRTS, gitlinks, and Dependabot PRs #82, #83, and #84 remain unchanged. |

## Motivation and problem statement

Dependabot PRs #82, #83, and #84 independently updated one portion of
`github/codeql-action` from v4.37.1 to v4.37.2. The immutable-action registry
correctly rejected each partial update, while updating only `init` or
`analyze` also creates a CodeQL configuration-version mismatch. This
task-owned replacement applies the official release as one consistent batch.

## Acceptance criteria

- Every `github/codeql-action/init`, `github/codeql-action/analyze`, and
  `github/codeql-action/upload-sarif` reference resolves to full commit
  `e0647621c2984b5ed2f768cb892365bf2a616ad1` with its v4.37.2 comment.
- `ci/tooling/security-tools.lock.yml` records the same v4.37.2 commit.
- No v4.37.1 CodeQL Action reference, mutable action tag, mixed CodeQL Action
  version, unexpected action source, permission change, trigger change, or
  matrix change remains in the scoped workflows.
- Focused local contracts and the resulting exact PR and `master` checks pass
  before this record is finalized for delivery.

## Implementation decision and rationale

The release source is the official `github/codeql-action` annotated tag
`v4.37.2`. Its tag object `26dfab68fffc1cbc36c56970c32f0e53cf1fcc01` targets
official commit `e0647621c2984b5ed2f768cb892365bf2a616ad1`; the official
release was published on 2026-07-21. The ten existing immutable workflow
references and one matching registry entry move atomically. The independent
Dependabot PRs remain open and are only candidates for a later verified
supersedure disposition after the replacement pull request is delivered.

## Changed files

- `.github/workflows/ci-security-codeql.yml`
- `.github/workflows/ci-security-osv.yml`
- `.github/workflows/ci-security-scorecard.yml`
- `ci/tooling/security-tools.lock.yml`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- This English/German Change Record pair.

## Commands executed

| Command | Result |
| --- | --- |
| Official GitHub API release, tag-object, and target-commit inspection for `github/codeql-action` v4.37.2 | passed: the official annotated tag targets `e0647621c2984b5ed2f768cb892365bf2a616ad1`; its tag signature is unsigned. |
| Current-`master` CodeQL-reference inventory | passed: exactly ten v4.37.1 references, four `init`, four `analyze`, and two `upload-sarif`, were identified before this atomic update. |
| `make check-ci-security-contract` | passed: all 15 focused workflow-security tests and the actionlint, zizmor, and gitleaks lock-parser validations passed. |
| Scoped v4.37.2 reference inventory and `git diff --check` | passed: exactly ten replacement references remain (four `init`, four `analyze`, two `upload-sarif`), no v4.37.1 SHA remains in the scoped workflows, and the registry pair matches. |
| Codex Security diff scan | passed: all eight changed files received complete review receipts; the only candidate was suppressed with evidence and no reportable finding survived. |
| `make check-bilingual-docs` | blocked_environment: the intentionally unpopulated Framework gitlink has pre-existing missing-link targets; the checker reported no error for this new English/German Change Record pair. |

## Security impact

This is a supply-chain and CI-security change. Every CodeQL Action invocation
remains an official full immutable release commit and the registry, `init`,
`analyze`, and `upload-sarif` agree on one release. Existing minimal
permissions, action sources, CodeQL scope, triggers, secret handling, and
security checks are preserved. No scanner, Quality Gate, or protection is
weakened.

## Runtime evidence

No connector runtime behavior changes. Current Dependabot job logs showed that
partial updates fail the immutable-action registry and that partial `init` or
`analyze` updates fail CodeQL version consistency; this batch removes both
partial states by construction.

## Known limitations

The official annotated tag's GitHub signature state is `unsigned`. The
verification evidence therefore relies on the official upstream repository,
release, annotated-tag target, and full commit SHA rather than a tag-signature
claim.

The lock-wide `checked_at` remains `2026-07-16`. This batch independently
revalidated the CodeQL mapping, but did not revalidate every lock entry; moving
the global date would therefore make a false whole-lock attestation.

## Remaining risks

The batch cannot eliminate upstream Action risk. Pinning the official full
release commit, retaining the registry evidence, and preserving the existing
CI security controls bound that dependency risk. No risk is accepted.

## Checks not run and rationale

Exact replacement-PR checks, review/thread state, SonarQube evidence, and
final `master` workflows remain pending. The full-tree bilingual check was run
but is blocked by the intentionally unpopulated Framework gitlink, not marked
as a pass.

## Final diff and review status

The replacement diff is intentionally limited to the ten coordinated CodeQL
pins, matching immutable registry record, bilingual Change Record pair, and
their indexes. Focused security-diff analysis and local validation passed;
exact replacement-PR evidence, protected squash merge, final `master`
workflows, and safe Parent-workspace restoration remain pending.
