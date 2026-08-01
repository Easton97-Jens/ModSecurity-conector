# FND-FRAMEWORK-0049 — Framework PR #42 Python-quality gate fails on five Pyright type diagnostics

- Category: `ci_failure`
- Repository / ownership: `framework` / `framework`
- Priority / severity / confidence: `P1` / `not_applicable` / `validated`
- Status / feasibility: `verified` / `already_fixed`
- Release blocker / security relevance: `false` / `true`

## Summary

Framework PR #42 exact head
`22747d460a9f7be02760edf05c311be376492457` fails the required
`python-ci-security-quality` check in GitHub Actions run `29942429850`.
Hosted Pyright reports five type diagnostics: repeated `dict.get()` values
typed as `Any | None` reach `re.fullmatch` in
`ci/tools/fetch-security-tool.py`, and a lock-fixture value statically typed
as `object` is indexed in `tests/ci_security/test_update_workflow_tools.py`.

Candidate commit `1fd3b362e0fed9766c6920e3c7bd1939535850f2` narrows the
dynamic values and corrects the fixture annotation. Its bounded local
validation and fresh hosted Pyright result passed: GitHub Actions run
`29943112344`, job `89001693819`, completed SUCCESS at
`2026-07-22T17:37:28Z`. All non-skipped PR checks and the PR Sonar Quality Gate
are green. PR #42 was then normally merged at `2026-07-23T07:41:13Z` as
Framework master `935cf14c676a24672be5c336e92cd13457cc35c8` from predecessor
`f73f8842f45318e2df8aff1d31855eeb7c20a22f` and merged head
`dc6cf411e78b3f37f1e4be52edef59894560b1ae`; the resulting tree equals the
reviewed PR-head tree. The SHA-256-bound postmerge receipt
`0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1`
records success for exact-master CI security Python quality workflow
`29989195066` and the other seven exact-master GitHub Actions workflows. The
source remediation is `verified`, not `closed`.

## Observed and expected behavior

The hosted `python-ci-security-quality` check fails during deterministic
Pyright analysis with five errors. The cited locations are
`ci/tools/fetch-security-tool.py:161` and `:166`, where `Any | None` reaches
`re.fullmatch`, and `tests/ci_security/test_update_workflow_tools.py:49`,
where a value typed `object` is indexed.

The required quality job must complete without a Pyright suppression or a
weakened scope. Dynamic mapping values must be narrowed before matching, and
the nested YAML-derived lock fixture must carry an accurate type contract
before indexing. Existing download-host, release-identity, action-lock,
workflow-permission, publisher, checkout, and ref-validation behavior must
remain unchanged.

## Impact, boundaries, and preconditions

The original head was a P1 release blocker because it could not satisfy a
required CI gate. Exact candidate head
`1fd3b362e0fed9766c6920e3c7bd1939535850f2` now satisfies that gate and all
non-skipped PR checks. The normal merge and successful exact-master CI-security
Python-quality workflow provide the required delivery evidence, so this is no
longer a release blocker. This is not evidence of a runtime defect or a
validated vulnerability. The affected helper participates in a security-
quality and provenance workflow, so its existing controls were preserved.

The failure requires Framework PR #42 at exact head
`22747d460a9f7be02760edf05c311be376492457`, execution of the hosted
`python-ci-security-quality` job, and its deterministic Pyright step. No
attacker-controlled source-to-sink path or broken runtime security control is
established by these type diagnostics.

## Affected files and technical cause

- `ci/tools/fetch-security-tool.py:161` — `re.fullmatch` receives a repeated
  dynamic `dict.get()` value typed `Any | None`.
- `ci/tools/fetch-security-tool.py:166` — the same typing boundary occurs at
  the second `re.fullmatch` call.
- `tests/ci_security/test_update_workflow_tools.py:49` — a nested lock-fixture
  value typed `object` is indexed.

The original source retained `Any | None` across the matching boundaries, and
the test fixture declared a flat `object` map despite being indexed as nested
dynamic YAML-derived data. This describes a static type-contract failure; it
does not allege incorrect runtime behavior.

## Evidence and reproduction

- External hosted failure: Framework PR #42, run `29942429850`, check
  `python-ci-security-quality`, exact head
  `22747d460a9f7be02760edf05c311be376492457`, exit `1`. The live GitHub log
  is not retained in this Parent-local task.
- Retained follow-up receipt:
  `evidence/ci-remediation/pr42-pyright-followup-commit-receipt.md`, SHA-256
  `5ccf2bd636101b2feea10e80c89852dbcf9c5f5e94e4b27decfbe0f5311ab790` in run
  `20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e`.
- Retained paired Framework Change Record:
  `reports/audits/change-records/20260722-01-consolidate-framework-pr-39-41.md`,
  SHA-256
  `faad4f2e542bac431c0a0f7f3b348cc3192ace933cf3c38944ee3beb7fa7ee93`.
- Retained exact-head hosted-verification receipt:
  `evidence/delivery/pr42-exact-head-hosted-verification.md`, SHA-256
  `07d30f93ab9bda5fb03fb22b20b9755aba2b8567b67678a34ec3ff7927bcb853`.
- Retained resulting-master verification receipt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-postmerge-verification.md`,
  SHA-256
  `0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1`.
  It binds the normal PR #42 merge to resulting master
  `935cf14c676a24672be5c336e92cd13457cc35c8` and records successful exact-
  master CI security Python quality workflow `29989195066`.

The retained receipt binds the original failure to candidate commit
`1fd3b362e0fed9766c6920e3c7bd1939535850f2` (parent
`22747d460a9f7be02760edf05c311be376492457`) and records the local result.

## Candidate remediation and local validation

The candidate stores `upstream_release` and `asset_url` once, checks and
narrows their string type before matching, and types the nested lock fixture
as nested `Any` data. It does not change the download host, release identity,
action lock, workflow permissions, publisher, checkout, or ref validation.

The retained receipt records these local results for the candidate:

- Focused Fetcher/Updater unit tests: 39 passed.
- CI-security contract: passed.
- Documentation and Change Record contracts: passed.
- Checksum-verified Ruff check and format check for both touched Python files:
  passed.
- Native `make lint`: passed.
- Clean worktree and `git diff --check` for the full base-to-head range:
  passed.

They were followed by exact-head hosted verification: run `29943112344`, job
`89001693819` passed `python-ci-security-quality`, including deterministic
Pyright, at `2026-07-22T17:37:28Z`. All non-skipped PR checks and the PR Sonar
Quality Gate passed. PR #42 is open, non-Draft, `MERGEABLE`, and `CLEAN`, with
no review or actionable thread.

## Acceptance and validation

The source-remediation criteria are satisfied at exact head
`1fd3b362e0fed9766c6920e3c7bd1939535850f2`; the normal merge and resulting-
master evidence now support `verified`, but not `closed`:

1. A reviewed candidate must retain the bounded type narrowing and fixture
   typing without relaxing the listed provenance and workflow-security
   controls.
2. The focused tests and the recorded local contract, documentation, Ruff,
   lint, clean-worktree, and whitespace checks must pass for the candidate.
3. A distinct exact PR head containing the remediation newly passed
   `python-ci-security-quality`, including Pyright: run `29943112344`, job
   `89001693819`, SUCCESS at `2026-07-22T17:37:28Z`. A result for
   `22747d460a9f7be02760edf05c311be376492457` is not replacement evidence.
4. Completed: all non-skipped hosted PR checks, the PR Sonar Quality Gate, and
   the PR review/thread controls were observed for that exact head; PR #42 was
   normally merged as `935cf14c676a24672be5c336e92cd13457cc35c8`, with
   successful exact-master CI security Python quality workflow `29989195066`.

Legitimate controls require accepted release/provenance matching and existing
updater lock-fixture behavior to remain intact, while absent or invalid dynamic
values must not bypass the existing checks.

## Dependencies, delivery limitations, and residual risk

There is no outstanding remediation dependency or blocker for this verified
source repair. The original external log is not retained here, and the type
errors alone do not prove a security exploit. The normal merge and
resulting-master evidence satisfy the required lifecycle proof.

`FND-SONAR-0002` (resulting-master Security Rating C) and
`FND-GITHUB-0007` (queued Cloudflare suite) are separately user-bounded PR #42
delivery limitations. Their global findings remain independently tracked;
neither condition reproduces, blocks, or reopens this verified Pyright repair.
No Parent gitlink or MRTS action occurred. The finding is deliberately
`verified`, not `closed`.

## Related findings

- `FND-FRAMEWORK-0020` is an earlier, distinct Pyright type-failure cause.
- `FND-FRAMEWORK-0046`, `FND-FRAMEWORK-0047`, and `FND-FRAMEWORK-0048` are
  separate Framework consolidation findings; none is changed by this record.
- `FND-SONAR-0002` and `FND-GITHUB-0007` are separate bounded delivery
  limitations, not dependencies of this repaired source defect.

## History

- 2026-07-23T07:51:09Z: `verified_after_pr42_normal_merge_and_resulting_master`
  — PR #42 was normally merged at 2026-07-23T07:41:13Z as Framework master
  `935cf14c676a24672be5c336e92cd13457cc35c8`, from predecessor
  `f73f8842f45318e2df8aff1d31855eeb7c20a22f` and merged head
  `dc6cf411e78b3f37f1e4be52edef59894560b1ae`. The retained postmerge receipt
  SHA-256 `0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1`
  records successful exact-master CI security Python quality workflow
  `29989195066` and seven other exact-master GitHub Actions workflows. With
  the prior direct Pyright success, the source repair moves from fixed to
  verified, not closed. FND-SONAR-0002 and FND-GITHUB-0007 remain separate
  bounded delivery limitations, not blockers of this repair.
- 2026-07-22T17:35:19Z: recorded hosted failure on PR #42 exact head
  `22747d460a9f7be02760edf05c311be376492457`, GitHub Actions run
  `29942429850`, check `python-ci-security-quality`.
- 2026-07-22T17:35:19Z: recorded local candidate
  `1fd3b362e0fed9766c6920e3c7bd1939535850f2` and its passed bounded local
  validation. Hosted Pyright and required checks remain unobserved.
- 2026-07-22T17:37:28Z: exact head
  `1fd3b362e0fed9766c6920e3c7bd1939535850f2` passed GitHub Actions run
  `29943112344`, job `89001693819`, including `python-ci-security-quality` /
  deterministic Pyright, all non-skipped PR checks, and the PR Sonar Quality
  Gate. PR #42 is non-Draft, `MERGEABLE`, and `CLEAN`, with no reviews or
  actionable threads. The source remediation is fixed/open; no normal master
  merge or resulting-master rerun occurred because `FND-SONAR-0002`
  independently blocks it.
