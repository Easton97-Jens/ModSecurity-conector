# Change Record: Parent deterministic GitHub Actions `uses:` prefix parser for SonarQube Cloud S8786

**Language:** English | [Deutsch](CR-20260729-sonar-scripts-uses-prefix-parser.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-scripts-uses-prefix-parser` |
| Date (UTC) | `2026-07-29` |
| Base revision | `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc` |
| Boundary | Parent `scripts/update-github-actions-versions.py`, this English/German Change Record pair, and the paired indexes only. No `ci/` source, `.github/` workflow, test source, Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, or default-branch change is included. |
| SonarQube Cloud linkage | Current `python:S8786` issue `AZ8hz9F2Ua5zTy8Lzy9S`; the first PR analysis also reported PR-local `python:S1192` issue `AZ-sKgRKKem7UxiInyxV` for the newly repeated `uses:` mapping key. The follow-up centralizes that key. Separate content-taint signal `AZ70CAr3IpeCryPNS2zi` remains unsuppressed and is not claimed as this patch's remediation. |

## Motivation and problem statement

The Parent GitHub Actions updater used an anchored Python regular expression to
recognize workflow `uses:` prefixes. SonarQube Cloud reports it as
`python:S8786` because of possible super-linear backtracking. This narrow
remediation replaces only that prefix split with a deterministic character
scan while preserving supported line-oriented behavior and update/write
controls.

## Acceptance criteria

- Prefix recognition is deterministic and linear for long
  repository-controlled workflow lines.
- Existing supported `uses:` parsing remains equivalent for normal, quoted,
  whitespace, blank-value, malformed, and dynamic-reference edge cases.
- Existing local, Docker, dynamic, SHA-pinned, workflow-path/symlink, and
  write-enabled controls remain unchanged and pass the direct updater suite.
- The exact Draft-PR head must receive fresh SonarQube Cloud evidence of zero
  new issues and `0.0%` New-Code duplication without a rule, profile,
  exclusion, suppression, false-positive disposition, or Quality-Gate change.
- This record claims delivery facts only after observing them at the final head.

## Implementation decision and rationale

`_uses_value_rest()` now scans a physical workflow line left to right: leading
whitespace, one optional list marker, literal `uses:`, and following whitespace
are consumed before the exact prefix and non-empty remainder are returned. It
replaces the anchored prefix regular expression without adding a YAML parser,
changing `_parse_uses_value()`, or widening accepted prefixes.

`parse_uses_line()` retains the prior dynamic-reference fallback prefix.
`USES_MAPPING_KEY` expresses the same mapping key once for the scanner and
that fallback after SonarQube Cloud identified the first parser revision's
four identical literals. The patch does not alter action eligibility, semantic-version lookup, workflow path
confinement, submodule handling, report paths, network requests, or write
application. No versioned test source is changed because the current user
restricted product remediation to `ci/` and `scripts/`; the existing direct
suite and a task-owned non-writing comparison harness provide regression
evidence.

## Changed files

- `scripts/update-github-actions-versions.py`
- `reports/audits/change-records/CR-20260729-sonar-scripts-uses-prefix-parser.md`
- `reports/audits/change-records/CR-20260729-sonar-scripts-uses-prefix-parser.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| Focused existing updater suite: `python -B -m unittest discover -s tests -p test_update_github_actions_versions.py -v` | passed: 25 tests, including quoted/unquoted preservation, malformed values, dynamic/local/Docker/SHA skips, workflow-symlink rejection, and write controls. |
| Task-owned non-writing parser comparison against `origin/master` | passed: normal, long-whitespace, blank-value, and dynamic-reference cases produced identical parser results. |
| `python -P -m py_compile scripts/update-github-actions-versions.py` | passed. |
| `git diff --check origin/master -- scripts/update-github-actions-versions.py` | passed. |
| First exact-head SonarQube Cloud analysis | Quality Gate passed and New-Code duplication was zero lines / `0.0%`, but the PR correctly remained unverified because it reported one new `python:S1192` issue for the four parser copies of `uses:`. No rule, profile, exclusion, suppression, false-positive disposition, or Quality-Gate change was made. |
| Follow-up constant extraction and local rerun | passed: `USES_MAPPING_KEY` replaced only the parser's four identical mapping-key literals; the 25-test updater suite, non-writing parser comparison, `py_compile`, and `git diff --check` all passed again. |
| Complete current branch-diff Codex Security contract | passed: delegated full-file review found zero reportable candidates for `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc..99629c1e8fac38caa79e4c7d3cd352052d78feed`; sealed snapshot digest `codex-security-snapshot/v1:sha256:74e566917334508fc229bfd7002116257ffdc9b32c51c85e3084be6cef28360d`. The earlier parser scan is retained as superseded evidence only. |
| Bilingual Change Record and link validation | passed: targeted heading/table/identity/language-switch/index checks. Root checks are blocked_external_dependency: the direct bilingual checker exited `1`, `make check-bilingual-docs` exited `2`, and `make check-doc-links` exited `2` only because 20 existing Framework-gitlink targets are absent in this task worktree; none reported this pair or its indexes. |
| Draft PR creation and initial exact-head observation | passed: Draft PR [#165](https://github.com/Easton97-Jens/ModSecurity-conector/pull/165) targets `master`; local, remote, and PR head were `f5f74f203efb834edb68ff1a13fb9c46a86f1352`. CodeQL, OSV, Apache, and Lighttpd checks were in progress; the installed `gh` client lacks `pr checks --json`, so the status was observed through `gh pr view` `statusCheckRollup`. |

## Security impact

Workflow text is repository-controlled input that can ultimately reach a
maintainer-triggered workflow file write. The complete current branch-diff
review read the updater, direct tests, and repository security guidance. It found no new
source-to-sink path, weakened control, or new filesystem, network, or process
sink: malformed values still fail closed, ineligible references are still
skipped, and only confined non-symlink workflow files can be written when
write mode is explicitly enabled.

The separate content-taint signal is not a path-injection proof: fixed
discovery globs and resolved-root/non-symlink/regular-file checks bind the
writer, and the updater is a default-branch schedule/manual path. It remains
unsuppressed. This record does not claim a security vulnerability was fixed.

## Runtime evidence

No connector or host runtime evidence was collected or claimed. The change is
limited to a maintenance-script parser. The direct unit suite and non-writing
comparison harness exercise the parser and its controlled temporary workflow
write boundary without a networked GitHub Actions update.

## Known limitations

The updater remains an intentionally supported line-oriented `uses:` parser,
not a full YAML parser. Existing flow-style or block-scalar limits predate this
diff and are not a newly unsafe rewrite path. The broad Parent SonarQube Cloud
backlog is outside this isolated first batch. Full documentation/link checks
remain blocked by pre-existing absent Framework-gitlink targets in this
task-owned worktree; this patch does not restore, populate, or alter them.

## Remaining risks

The local comparison corpus is strong regression evidence but not a proof for
every YAML form. Hosted analysis and checks must evaluate the final exact PR
head before S8786 is considered resolved or delivery is considered verified.
The task makes no permission, token, workflow, scanner, or suppression change
to force that result.

## Checks not run and rationale

- Ruff and Pyright are not installed in the selected local environment; they
  were not installed merely to pass this narrow remediation.
- No live updater run against repository workflows was performed because it
  performs network-backed resolution and can write workflow files; deterministic
  tests and the non-writing harness are the safe local boundary.
- No Framework, MRTS, Gitlink, `.github/`, or unrelated Parent source check was
  run or changed because the user limited this task to `ci/` and `scripts/`.
- Exact-head GitHub Actions, SonarQube Cloud, review, and PR evidence require
  the pushed Draft PR head and are not inferred locally.

## Final diff and review status

The initial implementation and traceability commit is
`f5f74f203efb834edb68ff1a13fb9c46a86f1352` on
`agent/parent-scripts-uses-parser-20260729`. It created Draft PR #165 against
`master`; the first hosted analysis then exposed one task-owned S1192 issue,
despite a passed Quality Gate and zero New-Code duplication. Source follow-up
commit `99629c1e8fac38caa79e4c7d3cd352052d78feed` introduces only
`USES_MAPPING_KEY` and removes that repeated parser literal. The required
record pair and indexes are delivery traceability only. The current complete
branch-diff security scan is valid with no reportable finding.

This follow-up updates the record pair to retain the observed Sonar state and
the exact source-security evidence. It intentionally creates a new PR head, so
all hosted checks, SonarQube Cloud analysis, review, and merge evidence must be
refreshed for that new SHA. No current hosted pass, approval,
ready-for-review state, or merge is claimed.
