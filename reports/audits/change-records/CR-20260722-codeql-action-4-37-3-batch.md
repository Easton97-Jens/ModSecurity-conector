# Change Record: CodeQL Action 4.37.3 batch

**Language:** English | [Deutsch](CR-20260722-codeql-action-4-37-3-batch.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260722-codeql-action-4-37-3-batch` |
| Date (UTC) | `2026-07-22` |
| Base revision | `784d79b4e399e2cb64314a3ba63dcf1633c672bd` |
| Boundary | Parent CI security and traceability only; Framework, MRTS, gitlinks, and original Dependabot PRs #82, #83, and #84 remain unchanged. |

## Motivation and problem statement

After the atomic v4.37.2 delivery, Dependabot independently advanced selected
PRs #82, #83, and #84 to separate v4.37.3 `init`, `upload-sarif`, and
`analyze` updates. Each is again an unsafe partial transaction. This
task-owned replacement applies the official v4.37.3 release coherently across
all ten existing CodeQL Action invocations and the immutable lock.

## Acceptance criteria

- Four `init`, four `analyze`, and two `upload-sarif` references resolve
  to exact official commit `e4fba868fa4b1b91e1fdab776edc8cfbe6e9fb81` with
  their v4.37.3 comments.
- `ci/tooling/security-tools.lock.yml` records the identical v4.37.3/SHA pair.
- No v4.37.2 CodeQL Action pin, mutable action tag, mixed CodeQL version,
  trigger/permission/input/action-source change, or unrelated dependency change
  remains in the scoped diff.
- Focused local contracts, complete diff-scoped security review, and exact PR
  and master evidence are recorded truthfully before delivery is complete.

## Implementation decision and rationale

The official `github/codeql-action` annotated tag `v4.37.3` has object
`c54b30b7df092240050e69945842bc67aee0f0f4` and targets commit
`e4fba868fa4b1b91e1fdab776edc8cfbe6e9fb81`; GitHub reports the tag unsigned
and the target commit PGP-verified. The official release was published on
2026-07-22. Matching workflow pins and the lock entry move atomically. The
prior v4.37.2 Change Record pair is corrected only with observed delivery facts.

## Changed files

- `.github/workflows/ci-security-codeql.yml`
- `.github/workflows/ci-security-osv.yml`
- `.github/workflows/ci-security-scorecard.yml`
- `ci/tooling/security-tools.lock.yml`
- Both v4.37.2 Change Record files, this English/German pair, and both indexes.

## Commands executed

| Command | Result |
| --- | --- |
| Official GitHub API release, annotated-tag object, and target-commit inspection for v4.37.3 | passed: official tag targets the stated immutable commit; its tag signature is unsigned and its target commit PGP-verified. |
| Exact current Dependabot PR #82/#83/#84 diff inspection | passed: the three partial diffs collectively require four `init`, four `analyze`, and two `upload-sarif` updates. |
| `make check-ci-security-contract` | passed: the focused workflow-security suite and actionlint, zizmor, and gitleaks lock-parser validations passed. |
| Scoped v4.37.3 inventory and `git diff --check` | passed: exactly ten references remain (four `init`, four `analyze`, two `upload-sarif`), the v4.37.2 SHA is absent from scoped files, and the lock matches. |
| `python -m unittest -v tests.test_bilingual_docs` | passed: all 11 focused bilingual-documentation unit tests passed. |
| `make check-bilingual-docs` | blocked_environment: only pre-existing missing Framework-gitlink link targets remain; no error names either v4.37.3 Change Record file. |
| Complete v4.37.3 Codex Security diff scan | passed: complete ten-file coverage, no reportable findings, and no deferred scan work; the generated report is retained as task-owned delivery evidence. |
| Exact replacement-PR and resulting-master hosted checks | pending; outcomes are added only after observation. |

## Security impact

This is a CI supply-chain change. Every CodeQL Action call remains full-SHA
pinned to one official release. Permissions, checkout credential behavior,
triggers, job matrices, action sources, secret handling, scanners, and Quality
Gate configuration are unchanged. No security control is weakened.

## Runtime evidence

No connector runtime behavior changes. This batch updates only CI Action
provenance and its central immutable registry.

## Known limitations

The official annotated tag is unsigned; evidence relies on the official release,
annotated-tag target, full immutable commit, and GitHub-reported target-commit
verification. The lock-wide `checked_at` remains `2026-07-16` because this
batch does not revalidate every lock entry.

## Remaining risks

The update cannot eliminate upstream Action risk; immutable official pinning
and unchanged CI controls bound it. The unrelated existing Sonar master
Quality-Gate blocker remains tracked by `FND-SONAR-0001` and is not changed.

## Checks not run and rationale

Exact replacement-PR checks, review/thread state, PR SonarQube evidence, and
resulting-master workflows are pending. The broad bilingual checker remains
environment-blocked by the intentionally unpopulated Framework gitlink and is
not represented as a pass.

## Final diff and review status

The intended final diff is limited to the ten coordinated v4.37.3 pins, the
matching lock record, accurate v4.37.2 delivery retention, this bilingual pair,
and the two indexes. The new supply-chain security scan passed with complete
coverage and no reportable finding; the protected delivery cycle remains
pending, and original Dependabot PRs remain open.
