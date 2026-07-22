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
- Focused local contracts and exact PR checks pass before delivery; master
  outcomes are retained without conflating an unrelated baseline failure.

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
| `make check-ci-security-contract` | passed: the focused workflow-security suite and the actionlint, zizmor, and gitleaks lock-parser validations passed. |
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

## Delivery and final review outcome

The current prompt selected Parent PRs #55, #73, #74, #77, #79, #80, #82,
#83, and #84 for `master` integration. Task-owned replacement PR
[#85](https://github.com/Easton97-Jens/ModSecurity-conector/pull/85) used
`agent/codeql-action-v4372-batch`; its local, remote, and PR heads matched
`35914dccb6e5406fb753d7fbb184b12dfbfe45d5` before protected squash merge.
Required `actions`, `bounded-c-cpp`, `envoy-go`, `traefik-go`, `actionlint`,
and `zizmor` passed, as did PR CodeQL, OSV, and the SonarQube Cloud Quality
Gate with zero new issues/hotspots. GitHub reported zero reviews and threads.

GitHub merged #85 at `2026-07-22T16:57:14Z` as master
`784d79b4e399e2cb64314a3ba63dcf1633c672bd`. GitHub Actions, CodeQL, OSV,
Scorecard, connector, governance, and three Dependabot update checks passed.
The external master Sonar Quality Gate failed only for three pre-existing
`TO_REVIEW` `python:S5332` hotspots tracked by `FND-SONAR-0001`, none in this
eight-file batch diff. No hotspot review, suppression, Quality-Gate change, or
source change occurred. Parent-root restoration was not attempted because the
unrelated gate remains failed; original #82/#83/#84 were not changed or closed
and later advanced independently to v4.37.3.

## Checks not run and rationale

The full-tree bilingual check is environment-blocked by the intentionally
unpopulated Framework gitlink, not marked as a pass. All observed #85 PR and
resulting-master outcomes are recorded above.

## Final diff and review status

The delivered v4.37.2 diff was limited to ten coordinated CodeQL pins, the
matching immutable lock record, this bilingual pair, and its indexes. Focused
security-diff analysis and local validation passed. Its master Sonar failure is
a separately tracked pre-existing baseline condition, not successful full
master verification.
