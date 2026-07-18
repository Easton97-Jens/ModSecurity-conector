# Change Record: CodeQL Action 4.37.1 batch

**Language:** English | [Deutsch](CR-20260717-codeql-action-4-37-1-batch.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260717-codeql-action-4-37-1-batch` |
| Date (UTC) | `2026-07-17` |
| Base revision | `02f9f98cdbbdd70bbc530ac1399974e53884f4e9` |
| Boundary | Parent CI security and traceability only; Framework, MRTS, gitlinks, and PR #51 unchanged. |

## Motivation and problem statement

Dependabot PRs #48, #49, and #50 independently updated one part of
`github/codeql-action` from v4.37.0 to v4.37.1. The immutable-action registry
correctly rejected each partial update, and updating only `init` or `analyze`
also produced a CodeQL configuration-version mismatch. This change applies the
verified release as one consistent batch.

## Acceptance criteria

- Every `github/codeql-action/init`, `github/codeql-action/analyze`, and
  `github/codeql-action/upload-sarif` reference resolves to full commit
  `7188fc363630916deb702c7fdcf4e481b751f97a` with its v4.37.1 comment.
- `ci/tooling/security-tools.lock.yml` records the same v4.37.1 commit.
- No v4.37.0 CodeQL Action reference, mutable action tag, mixed CodeQL Action
  version, unexpected action source, permission change, trigger change, or
  matrix change remains in the scoped workflows.
- Focused local contracts and the resulting exact PR and `master` checks pass
  before this record is finalized for delivery.

## Implementation decision and rationale

The release source is official `github/codeql-action` annotated tag `v4.37.1`.
Its tag object `bb16b9baa2ec4010b29f5c606d57d01190139edd` targets official
commit `7188fc363630916deb702c7fdcf4e481b751f97a`. The ten existing immutable
workflow references and one matching registry entry move atomically. The
independent Dependabot PRs are superseded only after the replacement pull
request is created and linked.

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
| `make print-python` | passed: selected repository interpreter is `/root/git/ModSecurity-conector/.venv/bin/python`. |
| `make check-framework` | passed: the configured Framework root exists; no Framework content was changed. |
| `PYTHONDONTWRITEBYTECODE=1 make check-ci-security-contract` | passed: all five focused tests and the Actionlint, Zizmor, and Gitleaks lock-record validations passed. |
| Checksum-verified Actionlint with `/usr/bin/shellcheck` over every workflow | passed. |
| Checksum-verified `zizmor --offline .github/workflows` | passed: no findings; 77 configured suppressions were reported. |
| Zizmor safe and deliberately insecure fixtures | passed: safe fixture accepted; insecure fixture rejected as expected (exit 14, dangerous trigger/template-injection findings). |
| Exact ten-reference scoped-diff invariant and `git diff --check` | passed: no stale/mixed CodeQL pin; workflow diff changes only the ten intended `uses` lines. |
| Direct Change Record schema and EN/DE structural-parity control | passed. |
| Initial `PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` | failed because this new record lacked required headings and identity fields; corrected before the final control. |
| Final `PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` | blocked by the unpopulated Framework gitlink in the isolated worktree; only pre-existing Framework link targets were missing, and no Change Record schema/parity error remained. |
| `PYTHONDONTWRITEBYTECODE=1 make check-doc-links` | blocked by the same unpopulated gitlink; its repository-path checker reported only existing Framework link targets. |

The isolated task worktree has the Framework only as an unpopulated gitlink,
so the initial documentation scan also reported pre-existing Framework link
targets as unavailable there. No scoped documentation link was changed. The
final documentation evidence will distinguish a successful schema check from
an environment-limited full-tree link check.

## Security impact

This is a supply-chain and CI-security change. Every CodeQL Action invocation
remains an official full immutable release commit and the registry, `init`,
and `analyze` agree on one release. Existing minimal permissions, action
sources, CodeQL scope, triggers, secret handling, and security checks are
preserved. No scanner, Quality Gate, or protection is weakened.

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

## Remaining risks

The batch cannot eliminate upstream Action risk. Pinning the official full
release commit, retaining the registry evidence, and preserving the existing
CI security controls bound that dependency risk. No risk is accepted.

## Checks not run and rationale

Exact replacement-PR checks, review/thread state, SonarQube evidence, and
final `master` workflows remain pending. Full-tree bilingual/documentation
link targets cannot be verified in this isolated worktree because its
Framework gitlink is intentionally unpopulated; the targeted Change Record
schema/parity control passed. No check is represented as passed until it has
run on the relevant exact head.

## Final diff and review status

Focused security validation, scoped-diff review, and targeted Change Record
schema/parity control passed. The former Change Record schema failure is
corrected. The only local limitation is unavailable Framework content for the
full-tree link checks. Exact replacement-PR evidence, authorized squash merge,
final `master` workflows, and safe Parent-workspace restoration remain
pending.
