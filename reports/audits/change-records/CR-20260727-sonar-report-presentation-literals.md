# Change Record: Parent report-presentation literals for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260727-sonar-report-presentation-literals.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-report-presentation-literals |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S1192` Code Smells AZ7HxAmX_i61V0DF6_GJ, AZ7HxAmX_i61V0DF6_GK, and AZ7HxAoH_i61V0DF6_Gy. |
| Boundary | Parent Markdown renderers and one Parent in-memory renderer test, this English/German Change Record pair, and their indexes. Report inputs, report paths, evidence, classification, request/rule/status semantics, scanner configuration, Quality Gates, suppressions, external Sonar state, GitHub state, Framework/MRTS content, and delivery remain unchanged. |

## Motivation and problem statement

Two report renderers repeated stable Markdown presentation literals. Sonar rule
`python:S1192` reports three such current findings. Module-private constants
make the specific presentation contracts explicit without changing how either
report reads inputs, classifies evidence, or writes output.

## Acceptance criteria

- Define only the two body-processor table constants and the rule-chain empty
  row constant.
- Replace only the duplicated renderer literals.
- Preserve the exact Markdown bytes and the three relevant occurrences in
  each renderer.
- Exercise only in-memory renderer input; do not execute report-generation
  mains, file output, connector runtime, Framework, or MRTS.
- Maintain the English/German Change Record pair and indexes, then run
  documentation-pair and diff-hygiene validation.

## Implementation decision and rationale

`DISTRIBUTION_TABLE_HEADER` and `DISTRIBUTION_TABLE_SEPARATOR` retain the
two body-processor table lines in all three selected subclusters.
`NO_ROWS_MARKDOWN` retains the three rule-chain empty-list lines. The focused
test constructs zero-row report dictionaries in memory and checks the exact
constant bytes plus occurrence counts; it deliberately does not call either
generator's `main()` or path/evidence functions.

## Changed files

- `ci/evidence/reports/generate-body-processor-analysis.py`
- `ci/evidence/reports/generate-rule-chain-semantics-analysis.py`
- `tests/test_report_presentation_literals.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- `rtk proxy env TMPDIR=<task-owned evidence root> PYTHONDONTWRITEBYTECODE=1
  PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest
  tests.test_report_presentation_literals` passed after the edit: 2 tests in
  0.001s.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -c <AST exact-constant predicate>` passed.
- The first focused assertion incorrectly counted a table separator globally;
  other intentionally unchanged tables use that separator. The corrected test
  counts the exact header/separator pair. This was a test-expectation repair,
  not a product failure.
- The documentation-pair validator and `rtk proxy git diff --check` are run
  after this pair is added; this record asserts no unobserved CI, runtime,
  review, or delivery result.

## Security impact

`not_applicable` to the product diff: the change is confined to static
Markdown display literals. It changes no input reading, path containment,
evidence validation, request/rule/status semantics, subprocess, network, or
publication behavior. Existing report-path and text-sanitization controls are
not altered.

## Runtime evidence

No connector, report-generator main, output writer, Framework, MRTS, or host
runtime was executed. The focused test evaluates both renderers with in-memory
zero-row report objects only.

## Known limitations

The local interpreter is Python 3.14.4 while the CI version-file contract is
Python 3.14.6, so the result is same-minor local evidence. This batch covers
three current Code Smells; the public project endpoint still reports 1,125
`OPEN` issues and this uncommitted candidate changes no external Sonar state.

## Remaining risks

An unexpected renderer consumer could rely on byte-exact output. The constants
are tested for their exact prior strings and the focused render checks preserve
all three selected header/empty-row occurrences. An exact delivered-head Sonar
analysis is still required before the listed keys can be treated as resolved
externally.

## Checks not run and rationale

- Full report generation is intentionally excluded: it can read or write
  evidence and requires runtime/Framework inputs outside this presentation-only
  batch.
- Full documentation/link checks remain outside this small batch; previous
  full runs are blocked by the intentionally uninitialized Framework Gitlink,
  not these renderers.
- No GitHub CI, SonarQube Cloud PR analysis, review, pull request, merge, or
  default-branch update has occurred.

## Final diff and review status

The B18 candidate is local, uncommitted, and unpushed. It has no delivery,
Framework, or MRTS action.
