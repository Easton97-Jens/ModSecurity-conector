# Change Record: Parent remaining-failure analysis discarded-read cleanup for SonarQube Cloud S1481

**Language:** English | [Deutsch](CR-20260727-sonar-remaining-failure-analysis-discarded-read.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-remaining-failure-analysis-discarded-read |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S1481` Code Smell AZ7HxAnC_i61V0DF6_Gg (inventory line 568). |
| Boundary | Parent remaining-failure report-generator and Parent test source, this English/German Change Record pair, and their indexes. Framework/MRTS repository content and Gitlinks, report fields, path-validation controls, scanner configuration, Quality Gates, suppressions, external Sonar state, GitHub state, and delivery remain unchanged. |

## Motivation and problem statement

`category_rollup(...)` built an `examples` list and discarded it immediately.
Its RHS invoked `case_group_summary(...)` and then `example_entry(...)`,
repeating evidence/case-file/YAML reads even though the independently built
`typical_examples` field is the only report output. The Sonar `S1481` finding
therefore needed behavior review rather than a blind dead-local deletion.

## Acceptance criteria

- Remove only the discarded `examples` assignment.
- Preserve `typical_examples`, category counts, ordering, and report fields.
- Establish a baseline showing the discarded summary-read path.
- Add focused Parent-only coverage that rejects that path but verifies output.
- Pass no-write syntax/AST, documentation-pair, and diff-hygiene checks.

## Implementation decision and rationale

The report already creates `typical_examples` through a separate
`example_entry(...)` comprehension. The deleted list was neither returned nor
read. A mocked baseline showed one redundant `case_group_summary(...)` call
for a populated category. The new focused test turns that call into an error
and verifies that the selected category still returns one typical example and
the same count. The change removes extra read/parse work, not report output.

## Changed files

- `ci/evidence/reports/generate-remaining-failure-analysis.py`
- `tests/test_remaining_failure_analysis.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -c <mocked baseline category_rollup predicate>` passed before the
  edit and confirmed the discarded summary-read invocation and retained output.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -m unittest -v tests.test_remaining_failure_analysis` passed
  after the edit: 1 test in 0.002s.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -c <post-edit syntax and discarded-read AST predicate>` passed.
- The documentation-pair validator, `tests.test_bilingual_docs`, and
  `rtk proxy git diff --check` are run after this pair is added; this record
  asserts no unobserved CI, runtime, review, or delivery result.

## Security impact

`not_applicable` to the product diff: the removed work was a discarded,
duplicate safe-reading/parsing path, not a path-validation, ownership,
symlink, publication, or access-control decision. The retained
`typical_examples` path still uses the existing report helper behavior, and
the focused test uses mocks without consuming Framework/MRTS data.

## Runtime evidence

No connector, NGINX, CRS, MRTS, native libmodsecurity, or report-generation
runtime was executed. The test checks an in-memory Parent generator contract;
it does not claim runtime evidence or output derived from real inputs.

## Known limitations

The local interpreter is Python 3.14.4 while the CI version-file contract is
Python 3.14.6, so the focused result is same-minor local evidence. The change
intentionally eliminates externally observable redundant file-read timing; it
does not preserve that irrelevant side effect. The public project endpoint
still reports 1,125 `OPEN` issues, and this uncommitted candidate changes no
external Sonar state.

## Remaining risks

An undocumented consumer could have relied on redundant read timing or a
suppressed malformed-input parse. The baseline and focused test prove the
selected output contract, but an exact delivered-head Sonar analysis is still
needed before the key can be treated as resolved externally.

## Checks not run and rationale

- Full report generation, connector builds, NGINX/CRS/MRTS matrices, and
  Framework/MRTS checks are not run because this focused Parent cleanup would
  otherwise consume unrelated runtime inputs.
- No GitHub CI, SonarQube Cloud PR analysis, review, pull request, merge, or
  default-branch update has occurred.

## Final diff and review status

The B15 candidate is local, uncommitted, and unpushed. It has no delivery,
Framework, or MRTS action.
