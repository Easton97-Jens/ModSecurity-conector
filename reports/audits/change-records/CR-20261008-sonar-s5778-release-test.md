# Change Record: CR-20261008-sonar-s5778-release-test

**Language:** English | [Deutsch](CR-20261008-sonar-s5778-release-test.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-sonar-s5778-release-test |
| Date (UTC) | 2026-10-08 |
| Base revision | `3ddeb8f6bfab3c619e6db50c2b0621dc0a504c19` |

## Motivation and problem statement

Current PR396 analysis is bound to 810a9b5621b04c79d58b1429c3182f1668e672c9. Sonar issue AaEX3Mmerf44IvJc6hHr, python:S5778, identifies multiple possibly-throwing calls in the release-tuple exception test at lines 501–502. Lint run 37675358566 fails zero-findings/duplication prerequisite checks on this same issue; lightweight lint is skipped, not a measured Ruff failure.

## Acceptance criteria

Only the intended `candidate_manifest()` operation remains inside the exception assertion. The same LauncherError, message and three previous/crossed version/digest negatives remain tested. No suppression or quality-contract change.

## Implementation decision and rationale

Prepare `dispatcher_payload()` before entering the assertion. The test still checks exactly the candidate manifest release rejection; setup failure can no longer satisfy the wrong assertion.

## Changed files

`tests/test_nginx_exact_head_root_launcher.py` and this EN/DE record pair. No production source, Framework/MRTS, Gitlink or release digest changes.

## Commands executed

`rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_exact_head_root_launcher` before and after the change: 47 tests PASS, 0 SKIP, exit 0. The official Sonar rule was read via authenticated API. Syntax, document checks and `git diff --check` are required before commit.

## Security impact

Release-version/digest rejection remains strict; all three invalid tuple controls retain the expected exception and regex. No issue acceptance, NOSONAR, exclusion, weakened assertion or runtime evidence change.

## Runtime evidence

No runtime claim is made by a test-structure fix. Fresh standard local lifecycle is a separate subsequent validation.

## Known limitations

The baseline quality gate is OK with one open code smell. Only a fresh analysis of the published new head can prove the issue resolved; a local unit pass is not a Sonar pass.

## Remaining risks

Other independent coverage gaps and Protected approvals remain outside this fix. Remote analysis may still be queued or running.

## Checks not run and rationale

Full native lint and fresh-head CI/Sonar follow stable publication; their statuses are not inferred from baseline results.

## Final diff and review status

Minimal three-line test diff reviewed against the current issue and official rule. Independent C commit planned after focused checks; no unrelated source or evidence included.
