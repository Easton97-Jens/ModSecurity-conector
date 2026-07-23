# Change Record: GitHub Actions updater parser and complexity remediation

**Language:** English | [Deutsch](CR-20260723-sonar-actions-updater-parser.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260723-sonar-actions-updater-parser` |
| Date (UTC) | `2026-07-23` |
| Base revision | `5b8db00d44ab24f3a9f4216a00f7edee977b6898` |
| Boundary | Parent `scripts/update-github-actions-versions.py`, its Parent unit test, this English/German Change Record pair, and the paired indexes only; Framework, MRTS, and both gitlinks remain unchanged. |
| Finding linkage | `FND-SONAR-0029` (retained pending import); `AZ8hz9F2Ua5zTy8Lzy9S`, `AZ70CAr3IpeCryPNS2zf`, `AZ70CAr3IpeCryPNS2zc`, and `AZ70CAr3IpeCryPNS2zg`. |

## Motivation and problem statement

The GitHub Actions updater used an optional quote plus backreference regular
expression to parse workflow `uses:` values. SonarQube Cloud reports this as
`python:S8786` due to possible super-linear backtracking. The same updater also
has two `python:S3776` cognitive-complexity findings and one `python:S1192`
duplicated-status finding. The implementation needs a focused remediation that
keeps supported workflow syntax and existing update/write controls unchanged.

## Acceptance criteria

- The four listed SonarQube Cloud findings are removed by a fresh exact Draft
  PR analysis without a suppression, exclusion, issue disposition, rule/profile,
  or Quality-Gate change.
- Unquoted, single-quoted, and double-quoted updateable `uses:` values retain
  their comments/suffixes while their reference is updated.
- Malformed unmatched or mismatched quoted values are not parsed or rewritten.
- Existing dynamic, local, Docker, SHA-pinned, symlink-confinement, and report
  path-confinement behavior continues to pass its focused Parent tests.
- The final task branch is an unmerged Draft PR based on the recorded current
  `master`, with exact-head checks and SonarQube Cloud evidence before it is
  described as verified.

## Implementation decision and rationale

`_parse_uses_value` now scans a single workflow value from left to right and
returns the quote marker, value, and suffix only when a matching quote is
present. It replaces the optional-quote/backreference regular expression while
preserving the existing dynamic-expression fallback.

Small private helpers separate report-row construction, non-update skip
classification, semver resolution, one-file scanning, and replacement
application. This lowers the cognitive complexity of `analyze_uses` and
`scan_workflows` without changing their public interfaces or update order.
`SKIPPED_DYNAMIC` is the one shared literal used for all three dynamic-action
status sites.

## Security impact

The security boundary was assessed because workflow text reaches a possible
workflow-file write. `update-actions-versions.yml` runs only on schedule or
manual dispatch and only on the default branch; `check-actions-versions.yml`
is also schedule/manual and uses read-only contents permission. No untrusted
pull-request/event path or lower-privilege attacker precondition was shown.
The S8786 security hypothesis therefore has `fix-finding` outcome `no_change`,
not a claimed security remediation.

The deterministic parser removes the scanner-signalled backreference while
preserving existing workflow-symlink, report-path, dynamic/local/Docker/SHA,
and protected-submodule controls. No security control, token handling,
permission, Sonar rule, Quality Gate, or CI protection is weakened.

## Changed files

- `scripts/update-github-actions-versions.py`
- `tests/test_update_github_actions_versions.py`
- `reports/audits/change-records/CR-20260723-sonar-actions-updater-parser.md`
- `reports/audits/change-records/CR-20260723-sonar-actions-updater-parser.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| Focused baseline: `rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/20260723T134220Z-sonarqube-parent-backlog-remediation.xZluLr/tmp/scripts-actions-updater.2c1xcV /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_update_github_actions_versions` | passed: 19 tests before the change. |
| In-memory AST parse of the changed source and test | passed: 2 files. |
| Focused post-change unit test with the same explicit Parent interpreter and task-owned `TMPDIR` | passed: 25 tests, including parser compatibility, lookup-error, no-downgrade, protected-submodule, and read-only-write controls. |
| Differential parser comparison against base `5b8db00` across 132 quoted, unquoted, dynamic, malformed, local, Docker, and suffix combinations | passed: 132 cases, zero mismatches. |
| Bounded pre-change malformed-input control | returned `None` for a 65,547-character unmatched-quote value in 5.655 ms; this is a bounded performance observation, not a universal ReDoS claim. |
| `git diff --check` | passed. |
| Checkout artifact scan for `*.pyc` | passed: no files found. |
| `tests.test_bilingual_docs` with the explicit Parent interpreter | passed: 11 tests. |
| `make check-bilingual-docs` | blocked_environment only by 20 existing missing Framework-gitlink targets; no task Change Record diagnostic remains. |
| `make check-doc-links` | blocked_environment only by the same existing missing Framework-gitlink targets. |

## Runtime evidence

No connector or host runtime evidence was collected or claimed. The change is
limited to a repository workflow-updater parser and its unit-level temporary
workflow fixtures. The focused tests exercise the real parser-to-scan-to-write
boundary with a fake resolver and task-owned temporary roots.

## Checks not run and rationale

- No live updater run against repository workflows: it uses network-backed
  GitHub API resolution and can create a report or write workflow files, so the
  deterministic unit fixtures are the selected safe regression boundary.
- No Framework or MRTS check or modification: both are outside the Parent-only
  scope.
- Exact-head GitHub Actions, SonarQube Cloud, review, and PR evidence do not
  exist until a task-owned Draft PR is pushed and are not inferred locally.

## Known limitations

The broad SonarQube Cloud Parent backlog remains open. Full documentation
commands are expected to report the existing missing Framework-gitlink targets;
that environment condition is not worked around by this Parent-only change.

## Remaining risks

The parser compatibility comparison is a focused corpus, not a proof for every
possible YAML form; the updater continues to intentionally handle the supported
`uses:` syntax rather than act as a YAML parser. SonarQube Cloud and hosted
checks must still analyze the exact Draft-PR head before the four findings are
verified. No merge is authorized.

## Final diff and review status

The scoped diff was reviewed before staging. Local source, focused-test,
differential-parser, and bilingual validation is complete, and the private
finding record is retained. Commit `03b487f88a98ec71edf438e8ac347dd76b370f69`
was created from the stated base; normal push, Draft-PR creation, and exact-head
hosted analysis remain required and are not claimed here.
