# Change Record: Parent full-runtime-matrix UTC offset for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260727-sonar-full-runtime-matrix-utc-offset.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-full-runtime-matrix-utc-offset |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S1192` Code Smell AZ7POyMJBW70q7L2nMI1 (line 164). |
| Boundary | Parent full-runtime-matrix report timestamp formatting and its Parent in-memory parsing test, this English/German Change Record pair, and their indexes. Manifest parsing, UTC `Z` representation, report generation, runtime-matrix execution, evidence, output paths, status semantics, scanner configuration, Quality Gates, suppressions, external Sonar state, GitHub state, Framework/MRTS content, and delivery remain unchanged. |

## Motivation and problem statement

The full-runtime-matrix report used the same ISO-8601 UTC numeric offset
literal three times: once when accepting a `Z` manifest timestamp and twice
when emitting a `Z` timestamp. Sonar rule `python:S1192` reports that
duplication. A private constant makes the numeric-offset representation
explicit while keeping the user-visible `Z` contract unchanged.

## Acceptance criteria

- Define one module-private numeric UTC-offset constant.
- Replace only the three `"+00:00"` literals.
- Preserve parsing of `Z` input, UTC-aware duration arithmetic, and emitted
  `Z` designator behavior.
- Import the module only through the established dynamic-import pattern; do
  not execute its `main()`, a runtime matrix, or report output.
- Maintain the English/German Change Record pair and indexes, then run
  documentation-pair and diff-hygiene validation.

## Implementation decision and rationale

`_UTC_OFFSET = "+00:00"` replaces exactly the parser normalization operand
and the two generated-at normalization operands. The three `"Z"` literals
stay inline because they are the one-character serialized representation, not
the Sonar finding. The focused test imports the module with the same
`sys.modules` registration required by its `@dataclass`, asserts
`Z` parsing to a UTC-aware datetime, and checks a 60-second duration.

## Changed files

- `ci/evidence/reports/generate-full-runtime-matrix.py`
- `tests/test_report_presentation_literals.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- `rtk proxy env TMPDIR=<task-owned evidence root> PYTHONDONTWRITEBYTECODE=1
  PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest
  tests.test_report_presentation_literals` passed after the edit: 3 tests in
  0.001s.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -c <AST offset-ownership predicate>` passed, confirming one
  `"+00:00"` literal and three `_UTC_OFFSET` loads.
- The documentation-pair validator and `rtk proxy git diff --check` are run
  after this pair is added; this record asserts no unobserved CI, runtime,
  review, or delivery result.

## Security impact

`not_applicable` to the product diff: this is a static timestamp-format
literal extraction. It changes no path/root validation, manifest source,
evidence authenticity, subprocess, network, request/rule/status handling, or
output-writing behavior.

## Runtime evidence

No runtime-matrix producer, report-generator `main()`, output writer,
connector, Framework, MRTS, or host runtime was executed. The test imported
the module and called only the pure timestamp parsing and duration helpers.

## Known limitations

The local interpreter is Python 3.14.4 while the CI version-file contract is
Python 3.14.6, so the result is same-minor local evidence. This batch covers
one current Code Smell; the public project endpoint still reports 1,125
`OPEN` issues and this uncommitted candidate changes no external Sonar state.

## Remaining risks

Generated reports are audit artifacts whose UTC spelling is externally
consumed. The `Z` token remains byte-for-byte unchanged, input parsing is
covered directly, and an exact delivered-head Sonar analysis is still required
before the listed key can be treated as resolved externally.

## Checks not run and rationale

- Full runtime-matrix generation is intentionally excluded: it reads manifest
  evidence and writes reports, outside this literal-only batch.
- Full documentation/link checks remain outside this small batch; previous
  full runs are blocked by the intentionally uninitialized Framework Gitlink,
  not this timestamp formatting.
- No GitHub CI, SonarQube Cloud PR analysis, review, pull request, merge, or
  default-branch update has occurred.

## Final diff and review status

The B19 candidate is local, uncommitted, and unpushed. It has no delivery,
Framework, or MRTS action.
