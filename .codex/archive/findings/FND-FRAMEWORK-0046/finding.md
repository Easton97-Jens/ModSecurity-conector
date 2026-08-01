# FND-FRAMEWORK-0046 — Framework PR #42 OSV trusted-base interpreter and lock ABI mismatch during CPython 3.14 transition

## Identity

| Field | Value |
| --- | --- |
| Category | ci_failure |
| Repository / ownership | framework / framework |
| Priority / severity / confidence | P1 / not_applicable / confirmed |
| Status / feasibility | verified / already_fixed |
| Release blocker / security relevant | false / true |
| Historical failed head | e0564d219980d62bc37162ac6c11641f289f1b71 |
| Exact fixed head | 2930e04e1558b5b10bdeb87a76abb077a2085566 |
| Exact merged PR head | dc6cf411e78b3f37f1e4be52edef59894560b1ae |
| Resulting Framework master / merge commit | 935cf14c676a24672be5c336e92cd13457cc35c8 |
| Trusted base | f73f8842f45318e2df8aff1d31855eeb7c20a22f |

## Summary

The historical Framework PR #42 OSV pull-request-head job failed before its
dependency comparison. Exact head
e0564d219980d62bc37162ac6c11641f289f1b71 selects CPython 3.14.6 from
bounded PR-head data, then installs the checked-out trusted base
f73f8842f45318e2df8aff1d31855eeb7c20a22f requirements-ci.lock. That lock
has a CP313-only PyYAML hash, so pip correctly rejects the downloaded CP314
wheel. The failure is an interpreter/lock ABI mismatch across the
trusted-base bootstrap boundary; it does not show that the reviewed CP314 lock
tuple is invalid.

This finding historically tracked the absent trusted-base .python-version
case. The exact-SHA-bound trusted-base CPython 3.13.14 bridge is now committed
and included in exact head 2930e04e1558b5b10bdeb87a76abb077a2085566. Its
current OSV pull-request-head check passes alongside the remaining current PR
checks, SonarQube Cloud passes, and no review or inline comment exists. The
retained verification receipt is framework-pr42-2930e04-hosted-verification.md,
SHA-256 4f7de2c315aa3f262b7a237b7228d5e682529065b28c8ce1046f2519752418b0.
PR #42 was then normally merged at `2026-07-23T07:41:13Z` with exact merge
commit and resulting Framework master
935cf14c676a24672be5c336e92cd13457cc35c8. Its parents are the trusted base
f73f8842f45318e2df8aff1d31855eeb7c20a22f and exact merged PR head
dc6cf411e78b3f37f1e4be52edef59894560b1ae; the resulting tree equals the
reviewed PR-head tree. The retained resulting-master receipt,
framework-pr42-20260723-postmerge-verification.md, SHA-256
0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1,
records eight exact-master GitHub Actions workflow successes. The PR-only
`pull-request-head` job is expected to be skipped for the push event, rather
than failed. Together with the earlier exact PR-head OSV pass, this verifies
the repair. The finding is `verified`, not `closed`.

## Observed and expected behavior

Historical GitHub Actions OSV run 29956021487, job 89045175516, selected CPython 3.14.6
and attempted the trusted-base lock installation. The lock expected CP313
digest 0f29edc409a6392443abf94b9cf89ce99889a1dd5376d94316ae5145dfedd5d6;
pip downloaded a CP314 wheel with digest
c458b6d084f9b935061bc36216e8a69a7e293a2f1e68bf956dcd9e6cbcd143f5 and
correctly rejected it under hash enforcement.

The OSV job must pair each trusted base with its reviewed ABI-compatible
interpreter/lock pair while retaining trusted-base checkout, base/head SHA
validation, read-only permissions, bounded manifest reads, and no execution
or checkout of untrusted PR content. For exact trusted base
f73f8842f45318e2df8aff1d31855eeb7c20a22f, the bridge must select only the
reviewed CPython 3.13.14 pair only when its selector is missing; all other
base/selector states—including a present selector for that base or a missing
selector at any other base—must fail closed rather than inherit a generic
fallback.

## Root cause and proposed remediation

The earlier remediation correctly treated the PR-head .python-version as
bounded SHA-verified data rather than checking out or executing the PR head.
At e0564d219980d62bc37162ac6c11641f289f1b71, however, its CPython 3.14.6
selection was used to install the trusted base's CP313-only lock. The workflow
coupled a trusted-base lock installation to a PR-head interpreter instead of
to an exact trusted-base interpreter/lock pair.

The implemented remediation is an exact-SHA-bound trusted-base
CPython 3.13.14 bridge. It must match only trusted base
f73f8842f45318e2df8aff1d31855eeb7c20a22f while that selector is missing,
choose its reviewed CPython 3.13.14 bootstrap pair, and fail closed for every
other base or selector state. It must preserve
trusted-base checkout, base/head SHA checks, read-only credentials, bounded
data-only PR-head reads, and the no-untrusted-code-execution boundary. It
must not install the PR-head lock, loosen hashes, add credentials, or introduce
a generic interpreter fallback.

## Evidence and reproduction

| Evidence | Value |
| --- | --- |
| Current receipt | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-e056-hosted-ci-failures.md |
| Current receipt SHA-256 | 5940246feb917a3d83a7372ef09f2f54673cf506ec24d457d5dec5dfeaa381be |
| Current receipt run / observed date | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e / 2026-07-22 |
| Historical original failure | /var/tmp/codex/ModSecurity-conector/runs/20260722T145132Z-framework-pr-39-41-master-integration-9a3c7dc7/evidence/pr39-osv-trusted-base-python-version-failure.md |
| Historical original SHA-256 | a0d6e64e4acfaabab6cda79704a28f3e9a7257897e0ebe8fc3e168152cc9bf76 |
| Historical local security validation | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/security-diff/consolidation-local-security-closure.md |
| Historical local-validation SHA-256 | 6a5f626d9f574841484055431c33fb8dcfc47bc0029d641ea48359c1a9764719 |
| Historical commit receipt | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/security-diff/consolidation-commit-receipt.md |
| Historical commit-receipt SHA-256 | c07815638b747cb80002db2f34ff18028d80d0241eb7c7248488d5c8fe6f9e1c |
| Historical hosted-pass receipt | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/delivery/pr42-exact-head-hosted-verification.md |
| Historical hosted-pass SHA-256 | 07d30f93ab9bda5fb03fb22b20b9755aba2b8567b67678a34ec3ff7927bcb853 |
| Resulting-master receipt | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-postmerge-verification.md |
| Resulting-master receipt SHA-256 | 0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1 |
| Resulting master / merged PR head | 935cf14c676a24672be5c336e92cd13457cc35c8 / dc6cf411e78b3f37f1e4be52edef59894560b1ae |
| Resulting-master observed at | 2026-07-23T07:51:09Z |

The current receipt retains the run/job facts but not the producer command or
observation time. This record therefore preserves 2026-07-22 exactly and does
not invent a more precise hosted timestamp.

Reproduce the observed condition with:

    rtk gh run view 29956021487 --repo Easton97-Jens/ModSecurity-test-Framework --log-failed
    rtk git -C <task-worktree> show f73f8842f45318e2df8aff1d31855eeb7c20a22f:requirements-ci.lock
    rtk git -C <task-worktree> show e0564d219980d62bc37162ac6c11641f289f1b71:.github/workflows/ci-security-osv.yml

## Acceptance criteria and validation plan

1. Only exact trusted base f73f8842f45318e2df8aff1d31855eeb7c20a22f with a
   missing selector selects its SHA-bound reviewed CPython 3.13.14 bridge; all
   other base/selector states, including a present selector for that base or a
   missing selector at any other base, fail closed.
2. The OSV job keeps trusted-base checkout, validates both SHAs, compares
   bounded manifests, and neither checks out nor executes PR-head code.
3. The CP313-lock/CP314-head mismatch and absent-base-version-file paths have
   focused Framework workflow/version-contract regression coverage.
4. Exact PR head 2930e04e1558b5b10bdeb87a76abb077a2085566 passes OSV
   pull-request-head and has fresh exact-head checks, Sonar, and review/thread
   evidence.
5. Completed: PR #42 was normally merged as
   935cf14c676a24672be5c336e92cd13457cc35c8, and the resulting-master receipt
   records successful exact-master GitHub Actions workflows. The PR-only
   `pull-request-head` job is correctly skipped on a push event.

The exact bridge diff, focused workflow/version-contract tests, and new hosted
OSV run are recorded for the fixed PR head. Legitimate controls remain
preserved: base/head manifest reads are bounded and SHA-verified, hash
enforcement remains intact, no PR-head lock is installed, and no write-capable
credentials were added.

## Dependencies, delivery limitations, and residual risk

There is no outstanding remediation dependency or blocker for this verified
OSV repair. The normal PR #42 merge and resulting-master evidence satisfy the
lifecycle proof for this finding. Related findings include
FND-FRAMEWORK-0044, FND-FRAMEWORK-0049, FND-FRAMEWORK-0051,
FND-SONAR-0009, FND-SONAR-0002, and FND-GITHUB-0007.

No risk is accepted for this OSV defect. The resulting-master Sonar condition
(`FND-SONAR-0002`) and queued Cloudflare suite (`FND-GITHUB-0007`) are
separate, user-bounded PR #42 delivery limitations. Their global findings
remain tracked independently; neither condition reproduces or blocks this
verified OSV repair. No Parent gitlink or MRTS action occurred. The finding is
verified and deliberately not closed.

## History

- 2026-07-23T07:51:09Z — verified_after_pr42_normal_merge_and_resulting_master:
  PR #42 was normally merged at 2026-07-23T07:41:13Z as Framework master
  935cf14c676a24672be5c336e92cd13457cc35c8 from predecessor
  f73f8842f45318e2df8aff1d31855eeb7c20a22f and merged head
  dc6cf411e78b3f37f1e4be52edef59894560b1ae. The retained postmerge receipt
  SHA-256 0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1
  records eight successful exact-master GitHub Actions workflows; the
  PR-only pull-request-head job is correctly skipped on the push event. With
  the prior exact PR-head OSV pass, the finding transitions from fixed to
  verified, not closed. FND-SONAR-0002 and FND-GITHUB-0007 remain separate
  bounded delivery limitations, not blockers of this repair.
- 2026-07-22T22:35:46Z — framework_pr42_2930_exact_head_osv_fixed:
  exact head 2930e04e1558b5b10bdeb87a76abb077a2085566 passed the repaired OSV
  pull-request-head control and all current PR checks. The retained verification
  receipt SHA-256 is
  4f7de2c315aa3f262b7a237b7228d5e682529065b28c8ce1046f2519752418b0.
  The trusted-base, read-only, no-untrusted-code-execution boundary remains
  intact. Status is fixed only; no master merge, resulting-master evidence,
  Parent gitlink action, or MRTS action occurred.
- 2026-07-22T15:07:13Z — historical
  exact_head_ci_failure_reproduced_and_tracked: the original PR #39
  trusted-base .python-version absence was recorded.
- 2026-07-22T17:04:03Z — historical
  consolidation_remediation_locally_fixed: the data-only PR-head bootstrap
  path passed focused local controls.
- 2026-07-22T17:24:06Z — historical
  consolidation_remediation_committed: that local path was bound to
  22747d460a9f7be02760edf05c311be376492457.
- 2026-07-22T17:42:25Z — historical
  exact_pr_head_hosted_controls_passed: head
  1fd3b362e0fed9766c6920e3c7bd1939535850f2 passed hosted OSV; this is not
  current verification.
- 2026-07-22T21:23:05Z —
  current_e056_trusted_base_interpreter_lock_mismatch_confirmed: the retained
  receipt records the current e0564d219980d62bc37162ac6c11641f289f1b71
  failure in run 29956021487, job 89045175516.
- 2026-07-22T21:23:05Z —
  sha_bound_cp313_bridge_recorded_as_uncommitted_follow_up: the reported
  CPython 3.13.14 bridge is allowed only for exact base
  f73f8842f45318e2df8aff1d31855eeb7c20a22f with its missing selector; every
  other base or selector state fails closed. No fixed, hosted-verification,
  merge, or resulting-master claim is made.
