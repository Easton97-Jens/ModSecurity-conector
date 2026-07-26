# Change Record: OpenSSF Scorecard Action v2.4.4 immutable-lock synchronization

**Language:** English | [Deutsch](CR-20260726-scorecard-action-v2-4-4-lock.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260726-scorecard-action-v2-4-4-lock |
| Date (UTC) | 2026-07-26 |
| Base revision | 53f0937b377e2e2b2e33e58c87d4034f78587608 |
| Boundary | Parent CI workflow, reviewed action lock, and this English/German Change Record pair/index only. Framework, MRTS, gitlinks, connector source, workflow permissions, triggers, and existing findings remain unchanged. |
| Finding linkage | FND-PARENT-0028 remains open and is not remediated by this outer Git Action pin update. |

## Motivation and problem statement

Dependabot PR #121 updated both `ossf/scorecard-action` uses to the official
v2.4.4 commit but left `ci/tooling/security-tools.lock.yml` at v2.4.3. The
repository's immutable-action contract correctly failed closed because the new
workflow SHA was not present in the reviewed action lock. The original
Dependabot branch is not maintainer-modifiable, so this Parent-owned
replacement candidate carries the intended pin and matching lock entry
atomically.

## Acceptance criteria

- Both Scorecard workflow references use the official full v2.4.4 commit
  `2d1146689b8cda280b9bc96326124645441f03bc` with the matching version comment.
- `ci/tooling/security-tools.lock.yml` records v2.4.4 and the same commit SHA.
- The existing immutable-action test accepts the reviewed SHA without relaxing
  the membership control, permissions, triggers, action sources, or job scope.
- The candidate's focused local contracts and future exact-head hosted checks
  pass before any protected integration.
- No Framework, MRTS, gitlink, connector-runtime, or security finding closure
  is claimed or performed.

## Implementation decision and rationale

The official `ossf/scorecard-action` signed annotated tag `v2.4.4` resolves to
the verified commit `2d1146689b8cda280b9bc96326124645441f03bc`; the official
release and commit metadata identify it as the v2.4.4 release. Keeping the
workflow SHA and reviewed lock entry identical preserves the existing
fail-closed contract. A lock-only merge was rejected because it would not
carry the requested action upgrade; modifying the Dependabot branch was
rejected because it is not maintainer-modifiable.

## Changed files

- `.github/workflows/ci-security-scorecard.yml`: the two existing Scorecard
  Action pins move from v2.4.3 to v2.4.4.
- `ci/tooling/security-tools.lock.yml`: reviewed Scorecard Action version,
  SHA, and check date match the workflow.
- `reports/audits/change-records/README.md` and `README.de.md`.
- This English/German Change Record pair.

## Commands executed

| Command or evidence | Result |
| --- | --- |
| Official GitHub tag, tag-object, release, and commit API readback for `ossf/scorecard-action` v2.4.4 | passed: signed tag `v2.4.4` resolves to verified commit `2d1146689b8cda280b9bc96326124645441f03bc`. |
| Exact PR #121 review at head `1dd0077b6297416222ad8d130dc6997956d74757` | failed as expected: the required `actionlint` job reported the immutable-lock membership failure. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_ci_security_workflows` on the uncorrected PR #121 source | failed as expected: the new Scorecard SHA was absent from the lock. |
| `git diff --check` for the replacement candidate | passed. |
| `make PYTHON=python3 check-ci-security-contract` | passed: all 18 CI-security workflow tests and all three security-tool lock validators passed under Python 3.14.4. |
| Checksum-verified actionlint over all workflows and permission fixtures | passed. |
| Checksum-verified `zizmor --offline .github/workflows` | passed: no findings; 80 existing suppressions reported. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs` | passed: 11 tests. |
| Full `check-bilingual-docs.py` | blocked_environment: exactly 20 existing missing targets below the intentionally unpopulated Framework gitlink; no changed Change Record or index diagnostic was reported. |

Exact-head hosted validation remains pending and is not represented as passed.

## Security impact

This is a CI supply-chain integrity correction. The external action remains
pinned to an official full commit SHA, and the reviewed lock retains the
enforced relationship between workflow action SHAs and their provenance. No
permissions, secrets exposure, trigger, upload behavior, scanner
configuration, quality gate, or branch protection is weakened. FND-PARENT-0028
documents the separate inherited mutable nested-container-image boundary; this
change neither closes nor worsens that finding.

## Runtime evidence

Not applicable. This change affects only Parent CI configuration and lock
provenance; it does not start a connector, service, HTTP listener, protocol
test, Framework test, or MRTS test.

## Known limitations

The isolated Parent worktree deliberately does not initialize or inspect the
Framework gitlink or MRTS. Full documentation checks may report pre-existing
links below that unpopulated boundary. Hosted results must be re-read for the
replacement PR's exact head after it is published.

## Remaining risks

An immutable outer Git Action commit does not bind the Docker image tag that
the upstream Scorecard action metadata resolves. That inherited medium-priority
hardening gap is already tracked as FND-PARENT-0028 and needs a separately
authorized remediation; no risk is accepted here.

## Checks not run and rationale

- Exact replacement-PR checks, SonarQube Cloud, CodeQL/OSV/secret-scanning,
  review, thread, and protected-merge evidence require a published candidate
  and a fresh exact-head verification round.
- Connector runtime, protocol, Framework, and MRTS tests are not applicable to
  this Parent workflow-pin and lock-only scope.
- No nested-image hardening is attempted because FND-PARENT-0028 requires a
  separately authorized remediation decision.

## Final diff and review status

This replacement candidate has passed focused local workflow, lock, actionlint,
zizmor, whitespace, and bilingual-record validation. It still needs an
independent review and fresh hosted exact-head evidence before a protected
merge is eligible. The original Dependabot PR #121 remains open and unmodified.
