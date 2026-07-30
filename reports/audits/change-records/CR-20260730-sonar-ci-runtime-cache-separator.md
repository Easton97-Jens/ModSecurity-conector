# Change Record: Parent CI runtime-cache four-column Markdown separator for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260730-sonar-ci-runtime-cache-separator.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260730-sonar-ci-runtime-cache-separator` |
| Date (UTC) | `2026-07-30` |
| Base revision | `e3ab3e7819c5ff3c7df6df427077d5c0dfe1545f` |
| Boundary | Parent `ci/evidence/reports/update-runtime-reports.py`, its direct Parent presentation test, this English/German Change Record pair, and paired indexes only. No `.github/`, `scripts/`, Framework, MRTS, Gitlink, product source, scanner configuration, Quality Gate, exclusion, suppression, or default-branch change is included. |
| SonarQube Cloud linkage | Current OPEN `python:S1192` issue `AZ7b3darcO69wzd-_jHY` for four identical `"|---|---|---|---|"` literals at lines 183, 207, 211, and 214. |

## Motivation and problem statement

The runtime-cache report renderer emits the same four-column Markdown table
separator for the component-cache table and each of the three cache-index
tables. SonarQube Cloud reports that repeated immutable literal as
`python:S1192`.

## Acceptance criteria

- The four semantically identical four-column table separators share one
  private module constant.
- The component-cache report retains its existing header, one structural
  separator line, row layout, and payload rendering.
- The cache-index report retains its manifest, component, and important-file
  headers, three structural separator lines, row layouts, and field ordering.
- The exact PR head must later receive zero new SonarQube Cloud issues, zero
  new duplicated lines, and `0.0%` New-Code duplication without weakening any
  control.

## Implementation decision and rationale

`FOUR_COLUMN_TABLE_SEPARATOR = "|---|---|---|---|"` now supplies the four
unchanged renderer positions. The direct presentation regression loads the
module without executing cache reads or report writes, exercises populated
component/cache-index payloads, and checks the literal structural lines and
representative rendered rows. Existing cache selection, JSON reading,
provenance metadata, report-root checks, output paths, and rendering order are
unchanged.

## Changed files

- `ci/evidence/reports/update-runtime-reports.py`
- `tests/test_report_presentation_literals.py`
- `reports/audits/change-records/CR-20260730-sonar-ci-runtime-cache-separator.md`
- `reports/audits/change-records/CR-20260730-sonar-ci-runtime-cache-separator.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| Direct SonarQube Cloud `api/issues/search` readback for `AZ7b3darcO69wzd-_jHY` | passed: one OPEN `python:S1192` issue identifies the four literal locations. |
| `python -B -m unittest tests.test_report_presentation_literals` | passed: 4 tests, including the populated component-cache and cache-index layout regression. |
| Python AST parse of the changed renderer and test | passed. |
| `git diff --check` | passed. |
| Focused source/control/sink security preflight | passed: full Codex Security workflow is `not_applicable`; no plausible diff-induced finding. |
| `make check-bilingual-docs` and `make check-doc-links` | `blocked_external_dependency`: their only diagnostics are pre-existing links to the absent worktree Framework Gitlink; the direct Change Record validator and 21 bilingual-checker unit tests passed. |
| `env VERIFIED_RUN_ROOT=<task-owned external root> make lint` | `blocked_external_dependency`: CI shell syntax and all `ci/*.py` compilation passed before a broad test imports the absent worktree Framework checker. |

## Security impact

The existing renderer consumes cache-derived values and reaches a
safe-root-constrained generated-report write path. This change introduces only
a private static separator outside the payload-derived flow; it changes no
cache root, environment input, path control, JSON parsing, output destination,
subprocess, privilege, or provenance behavior. The presentation regression
asserts structural separator lines, so a payload substring cannot satisfy the
table-boundary control. No security finding is claimed, suppressed, or closed.

## Runtime evidence

No component preparation, connector runtime, networked matrix, cache read, or
report write is claimed. The direct in-process renderer regression is the
legitimate behavior control for this byte-preserving presentation refactor.

## Known limitations

The focused test uses representative populated in-memory payloads; it does not
exercise every cache artifact or the existing report-write workflow. That is
intentional for a static-literal change and does not establish authenticity of
the pre-existing cache JSON inputs. The broad Make documentation and lint
targets cannot finish in this isolated worktree because its Framework Gitlink
is intentionally absent; neither reports a changed task-file defect.

## Remaining risks

The exact hosted PR head must still demonstrate removal of the selected S1192
receipt with a passing SonarQube Cloud Quality Gate, zero new issues, zero new
duplicated lines, and `0.0%` New-Code duplication. Local checks cannot replace
that hosted evidence.

## Checks not run and rationale

- No component build, package download, connector runtime, or network matrix
  was run: the change is a byte-preserving pure-renderer literal extraction.
- No Framework, MRTS, Gitlink, `.github/`, `scripts/`, or unrelated Parent
  source was changed. Broad checks that require Framework source are recorded
  as blocked rather than bypassed because the user restricted this campaign to
  the Parent CI scope.
- Hosted GitHub Actions, SonarQube Cloud PR analysis, review, and merge
  evidence are not inferred locally and require the eventual exact PR head.

## Final diff and review status

The local scoped diff contains one private constant, four reference
substitutions, one direct presentation regression, and this traceability pair.
The focused final source/test diff review is `already_safe`: no payload,
path, command, parser, privilege, or report-write control changed. No commit,
push, pull request, hosted check, review, or merge is claimed by this record;
those facts are recorded only after observation.
