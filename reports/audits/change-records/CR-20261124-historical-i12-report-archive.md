# Change Record: CR-20261124-historical-i12-report-archive

**Language:** English | [Deutsch](CR-20261124-historical-i12-report-archive.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261124-historical-i12-report-archive |
| Date (UTC) | 2026-11-24 |
| Base revision | `48c4672dc07458411288570515bb8357f1e9e581` |

## Motivation and problem statement

Six I12 artifacts from 2026-10-15 occupy 970,967 bytes in the reports tree. They document completed Apache and lighttpd investigations.

## Acceptance criteria

Reduce the tracked report payload by at least 900,000 bytes, verify byte-for-byte recovery of all six archived files, and pass documentation and report governance. Compare the full layout diagnostics against the base revision.

## Implementation decision and rationale

Keep the originals at the base revision and link to each file from the [reports index](../../README.md#historical-i12-evidence). GitHub's tree API and local `git ls-tree -rl` returned matching blob IDs and sizes for all six files. The pinned Framework's active inventory requires the Apache ledger, Apache review script, and lighttpd stock-sidecar cases. Those three inputs are present with their original bytes.

## Changed files

The English and German reports indexes link to the archived Apache rule-equivalence probe and five lighttpd case or oracle snapshots. The six files are retired from the current checkout. This Change Record is also available in both languages.

## Commands executed

The reference review covered 542 tracked Parent documents, 407 active Parent source, configuration and workflow files, and the pinned Framework's report tooling and active inventory.

| Check | Observed result |
| --- | --- |
| `git ls-tree -rl` and `gh api` | Matching blob IDs and sizes for all six archived paths at the base revision. |
| `make check-bilingual-docs`, `make check-doc-links` | Passed with the pinned Framework and Python 3.15.2. |
| `make report-governance` | Passed with the pinned Framework after restoring the three required inventory inputs identified by the first run. |
| `make check-generated-report-layout` | Exit 2 on both base and task checkout, with 207 identical diagnostics covering historical inputs and metadata. |
| `python -P ci/tools/new-change-record.py check`, `git diff --cached --check` | Passed. |

## Security impact

The change concerns historical artifact retention and navigation. Existing security and runtime checks continue to use their original inputs.

## Runtime evidence

Existing I12 evidence is available at the base revision. This change makes no new runtime claim.

## Known limitations

A shallow clone needs to obtain the archived revision before `git show` can retrieve a file.

## Remaining risks

Private tooling with hard-coded paths to the six historical files must retrieve them from the pinned revision.

## Checks not run and rationale

Connector builds, runtime suites, and report regeneration are outside this historical archive change. The report governance check includes its runtime-path policy fixtures.

## Final diff and review status

The change was prepared in a dedicated Parent worktree. Publication and GitHub check status are tracked on the pull request.
