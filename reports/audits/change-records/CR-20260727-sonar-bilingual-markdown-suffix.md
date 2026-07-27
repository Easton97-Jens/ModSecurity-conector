# Change Record: Parent bilingual Markdown suffix ownership for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260727-sonar-bilingual-markdown-suffix.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-bilingual-markdown-suffix |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S1192` Code Smell AZ9cRyW7HhV2CayPTPup (line 223). |
| Boundary | Parent bilingual-documentation checker and its Parent unit test, this English/German Change Record pair, and their indexes. Documentation policy, companion naming behavior, scanner configuration, Quality Gates, suppressions, external Sonar state, GitHub state, Framework/MRTS content, and delivery remain unchanged. |

## Motivation and problem statement

The bilingual-documentation checker repeated the Markdown suffix literal in the
two opposite companion constructors. Sonar rule `python:S1192` reports the
duplicate. A module-private name makes the shared formatting contract explicit
without broadening it to unrelated suffix/path handling.

## Acceptance criteria

- Add one module-private Markdown suffix constant.
- Use it only in the English/German companion constructors.
- Preserve `foo.md` to `foo.de.md` and the reverse mapping.
- Pass direct unit and no-write AST validation.
- Maintain the English/German Change Record pair and indexes, then run
  documentation-pair and diff-hygiene validation.

## Implementation decision and rationale

`MARKDOWN_SUFFIX` replaces only the two duplicate literals. The German
constructor still appends `.de` before the suffix, while the English constructor
still removes `.de` plus the suffix. A focused bidirectional test records both
paths. No documentation content, discovery, local-link resolution, or policy
decision changed.

## Changed files

- `ci/checks/documentation/check-bilingual-docs.py`
- `tests/test_bilingual_docs.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- `rtk proxy env TMPDIR=<task-owned evidence root> PYTHONDONTWRITEBYTECODE=1
  PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v
  tests.test_bilingual_docs` passed after the edit: 14 tests in 0.034s.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -c <suffix ownership, counterpart, and test syntax AST predicate>`
  passed.
- The documentation-pair validator and `rtk proxy git diff --check` are run
  after this pair is added; this record asserts no unobserved CI, runtime,
  review, or delivery result.

## Security impact

`not_applicable` to the product diff: this refactors a static documentation
suffix literal only. It changes no path containment, link escape check,
authorization, subprocess, network, or publication behavior.

## Runtime evidence

No connector, report generator, Framework, MRTS, or host runtime was executed.
The focused unit test exercises only in-memory `Path` companion construction.

## Known limitations

The local interpreter is Python 3.14.4 while the CI version-file contract is
Python 3.14.6, so the result is same-minor local evidence. This batch covers
one current Code Smell; the public project endpoint still reports 1,125 `OPEN`
issues and this uncommitted candidate changes no external Sonar state.

## Remaining risks

An unexpected caller could depend on a different suffix behavior. The two
constructors retain their exact prior transformations and the bidirectional
test executes both. An exact delivered-head Sonar analysis is still required
before the listed key can be treated as resolved externally.

## Checks not run and rationale

- Full documentation/link checks remain outside this small suffix-only batch;
  previous full runs are blocked by the intentionally uninitialized Framework
  Gitlink, not this source.
- No GitHub CI, SonarQube Cloud PR analysis, review, pull request, merge, or
  default-branch update has occurred.

## Final diff and review status

The B17 candidate is local, uncommitted, and unpushed. It has no delivery,
Framework, or MRTS action.
