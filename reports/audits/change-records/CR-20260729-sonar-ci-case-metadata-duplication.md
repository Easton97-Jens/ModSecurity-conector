# Change Record: Parent CI case-metadata parsing deduplication

**Language:** English | [Deutsch](CR-20260729-sonar-ci-case-metadata-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-case-metadata-duplication` |
| Date (UTC) | `2026-07-29` |
| Base revision | `fda62539b6f0a710865707e3003b73ed4469f20e` |
| Source revision assessed | Local task patch against the stated base revision. |
| Boundary | Parent `ci` sources listed below, direct Parent test, this EN/DE pair and indexes only. No `.github`, `scripts`, Framework, MRTS, Gitlink, scanner configuration, Quality Gate, exclusion, suppression, or default-branch action. |
| SonarQube Cloud linkage | Targets the current 17-line duplicate case-document parsing pair between the two Parent report generators; no scanner control or issue status is changed. |

## Motivation and problem statement

The two generators independently parsed already-read YAML case text, accepted only mapping results, selected `request`/`expect`/`metadata`, and split request paths from query strings. The selected 17-line pair was a current SonarQube Cloud duplicate target, but it is adjacent to evidence-path and YAML trust controls.

## Implementation decision and rationale

`parse_case_document()` owns only that pure text parsing. It accepts raw text plus the optional YAML module and performs no path resolution, file read, root registration, output, subprocess, or network action.

`parse_empty=True` preserves the remaining-failure generator's previous empty-text parser attempt. Phase 4 retains its previous no-parse-on-empty behavior. Both callers retain their own safe evidence/case-path handling, rule/phase precedence, expected intervention/body, Phase-4 classification, runtime-verification state, and pending/non-promoted fields.

## Acceptance criteria

- Valid mappings preserve request method, path/query, expectation, and metadata; malformed, scalar, absent-parser, and empty inputs retain safe defaults.
- Both generators use the helper but preserve their intended evidence-first versus YAML-first priority.
- In-root case data remains readable; outside-root paths, escaping symlinks, and outside evidence files retain default metadata before parsing.
- The exact future PR head must show zero new SonarQube Cloud issues and `0.0%` New-Code duplication without a scanner-policy change.

## Changed files

- `ci/lib/case_metadata_utils.py`
- `ci/evidence/reports/generate-phase4-hard-abort-capability.py`
- `ci/evidence/reports/generate-remaining-failure-analysis.py`
- `tests/test_case_metadata_utils.py`
- this English/German Change Record pair and its indexes

## Commands executed

| Command or control | Result |
| --- | --- |
| Focused helper, remaining-failure, and focused-analysis utility suites | passed: 19 tests, including mappings, parser fallbacks, query-only paths, caller priority, in-root, outside-root, symlink, and rejected-evidence controls. |
| Selected-file `py_compile` with task-owned bytecode cache | passed. |
| `git diff --check` | passed. |
| Independent final source and test security-diff reviews | passed: no plausible diff-induced security candidate. |
| `make check-bilingual-docs` | `blocked_external_dependency`: all new Change-Record section checks passed; existing repository links require absent Framework-submodule targets, and no changed document link was reported. |

## Security impact

Case YAML and evidence metadata are untrusted CI-report inputs. Existing callers retain `safe_existing_file()` before reads; production entry points retain safe-root setup. The helper keeps `yaml.safe_load()` and a failure-to-empty fallback. Sinks remain generated JSON/Markdown reports; no connector enforcement or runtime PASS/FAIL value changes.

## Runtime evidence

No connector runtime, networked preparation, report-generator main, or Framework/MRTS execution was run. The focused test uses a private temporary filesystem and writes no repository report. Hosted GitHub Actions, SonarQube Cloud, review, approval, merge, and master verification are not yet observed or claimed.

## Known limitations

The isolated worktree lacks the Framework submodule targets referenced by existing repository documentation, so the repository-wide documentation check may be externally blocked. This record does not claim that the broader Parent `ci/` backlog is exhausted.

## Remaining risks

The helper preserves the existing trusted-artifact-root and bounded-input assumptions. It does not establish a full connector runtime result, hosted Quality Gate result, or master-state evidence.

## Checks not run and rationale

- No connector runtime, report-generator main, or networked preparation ran because this is a pure metadata refactor and those commands would require generated evidence and unavailable Framework content.
- Hosted GitHub Actions, SonarQube Cloud, review, approval, merge, and master checks have not yet run for a PR head because no PR has been created.

## Delivery status

Before verification, the exact PR head must be reconciled with master and receive fresh hosted checks and SonarQube Cloud results. No direct master change or merge is authorized or implied.

## Final diff and review status

The local source/test diff has passed focused tests, selected compilation, whitespace validation, and independent source/test security-diff review with no plausible diff-induced candidate. The final exact PR-head hosted verification remains pending.
