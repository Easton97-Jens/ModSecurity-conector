# Change Record: Parent NGINX MRTS HTTP-500 report unused-parameter cleanup for SonarQube Cloud S1172

**Language:** English | [Deutsch](CR-20260727-sonar-nginx-mrts-http500-unused-parameter.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-nginx-mrts-http500-unused-parameter |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S1172` Code Smell AZ7PU4lam6NRVhQ0A9r_ (inventory line 408). |
| Boundary | Parent report-generator and Parent test source, this English/German Change Record pair, and their indexes. Framework/MRTS repository content and Gitlinks, report semantics, validation controls, scanner configuration, Quality Gates, suppressions, external Sonar issue state, GitHub state, and delivery remain unchanged. |

## Motivation and problem statement

`build_payload(...)` accepts `framework_root`, but never reads it. SonarQube
Cloud rule `python:S1172` reports that dead helper parameter. Keeping it can
mislead a caller into assuming that the payload itself consumes Framework
content, when the command-line value is actually needed only later for report
metadata.

## Acceptance criteria

- Remove only the unused `framework_root` helper parameter.
- Update every Parent call site of the helper.
- Preserve the command-line `--framework-root` path and its report-metadata
  use.
- Preserve invalid verified-run-ID rejection before any report/runtime path
  join.
- Pass the focused control before and after the edit, plus no-write syntax,
  signature/call, documentation-pair, and diff-hygiene validation.

## Implementation decision and rationale

The `build_payload(...)` body does not read `framework_root`; the generator's
`main()` still resolves it and passes it to `build_metadata(...)`. This change
therefore removes it only from the helper signature and its two Parent callers:
the generator's local call and the focused invalid-run-ID test. The CLI option,
metadata identity, input selection, run-ID validation, and report fields are
unchanged. The file is Parent-owned although it describes MRTS evidence; no
Framework or MRTS source is modified.

## Changed files

- `ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py`
- `tests/test_runtime_path_security.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- Before the edit, the focused invalid-run-ID control passed: 1 test in
  0.281s.
- Before the edit, no-write in-memory compilation and AST inspection confirmed
  the four-parameter signature and no body read of `framework_root`.
- After the edit, the same focused invalid-run-ID control passed: 1 test in
  0.292s.
- After the edit, no-write in-memory compilation and AST inspection confirmed
  the three-parameter signature and no body reference to `framework_root`.
- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1
  PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v
  tests.test_bilingual_docs`, the direct Change Record-pair validator, and
  `rtk proxy git diff --check` are run after this pair is added. No CI,
  runtime, review, or delivery result is asserted here.

## Security impact

`not_applicable` to the product diff: the removed helper parameter did not
carry a filesystem, subprocess, network, or publication operation. The same
focused security control still rejects traversal and absolute verified-run IDs
before `build_payload(...)` can join a report/runtime path. No path-validation,
ownership, symlink, or publication control changed.

## Runtime evidence

No NGINX, CRS, MRTS, connector, report-generation, or host runtime was
executed. The focused test uses an invalid run ID and intentionally fails
before consuming a Framework path or report input; it is Parent test-contract
evidence only.

## Known limitations

No source-adjacent `py_compile` check is used in this mounted worktree because
the prior same-module batch observed it trying to create a read-only
`__pycache__`; the recorded in-memory `compile(...)` validates syntax without
writing outside the task-owned temporary root. This batch covers one current
Sonar Code Smell. The public project endpoint still reports 1,125 `OPEN`
issues, and this uncommitted candidate changes no external Sonar state.

## Remaining risks

An unobserved external caller could still use the old helper signature. The
repository-wide source reference check found only the two updated Parent call
sites, while the focused invalid-run-ID control exercises the retained security
boundary. An exact delivered-head Sonar analysis remains necessary before the
listed key can be treated as resolved externally.

## Checks not run and rationale

- Full report generation, NGINX/CRS/MRTS matrices, connector builds, and
  Framework/MRTS checks are not run because this is a signature-only Parent
  cleanup and they would consume unrelated runtime inputs.
- No GitHub CI, SonarQube Cloud PR analysis, review, pull request, merge, or
  default-branch update has occurred.

## Final diff and review status

The B14 candidate is local, uncommitted, and unpushed. It has no delivery,
Framework, or MRTS action.
