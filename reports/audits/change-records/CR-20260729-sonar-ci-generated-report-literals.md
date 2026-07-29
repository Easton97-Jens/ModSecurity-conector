# Change Record — Parent CI generated-report literal deduplication

**Language:** English | [Deutsch](CR-20260729-sonar-ci-generated-report-literals.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-generated-report-literals` |
| Date (UTC) | `2026-07-29` |
| Base revision | `a1c8394e528bfcd7b54bc3e0aac4cdf3430d1345` |
| Source revision assessed | Current local task-working-tree diff from the base revision; no commit, push, pull request, hosted check, or merge is claimed at record authoring. |
| Boundary | Parent `ci/lib/generated_report_utils.py`, direct Parent generated-report evidence tests, this English/German Change Record pair, and paired Change-Record indexes only. No `.github`, `scripts`, Framework, MRTS, Gitlink, generated report, scanner policy, Quality Gate, exclusion, suppression, or default-branch change is included. |
| SonarQube Cloud linkage | Resolves five open `python:S1192` literal clusters in `generated_report_utils.py`: local-home display token; refresh-report generator; remaining-failure generator; Framework case-matrix generator; and Framework native-MRTS generator. |

## Motivation and problem statement

The Parent CI generated-report helper carried five independent repeated static
literal clusters reported by SonarQube Cloud. The strings are trusted,
source-authored presentation or provenance labels, so changing their contents
would risk path portability or report-registry inference. The required remedy
is narrow: one static private owner for each value, with the existing values
and all consumer-visible behavior retained exactly.

## Acceptance criteria

- Each of the five cited values has exactly one static private source owner in
  `generated_report_utils.py`; no rule, exclusion, suppression, or Quality Gate
  changes.
- `/root`, `/home/<user>`, and `/Users/<user>` retain their portable Markdown
  rendering, including descendant paths; `/home` and relative paths remain
  unchanged.
- Every affected `GeneratedReport.generator` value and its complete registry
  membership remain unchanged.
- The exact future pull-request head must report zero new SonarQube Cloud
  issues, zero new duplicated lines, and `0.0%` New-Code duplication.

## Implementation decision and rationale

- Added five private module constants directly beside existing static generated
  report constants. They are not configuration, environment, manifest, or CLI
  inputs.
- Replaced only the cited duplicate string occurrences. The code still renders
  local-home references only in Markdown presentation; raw evidence paths,
  hashing, and JSON provenance are untouched.
- Added a table-driven direct control through the actual generated-report
  layout import path. It verifies all supported home-root variants plus safe
  controls and validates exact report-generator groups rather than private
  constant names.

## Changed files

- `ci/lib/generated_report_utils.py`
- `tests/test_generated_report_evidence_integrity.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-generated-report-literals.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-generated-report-literals.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

The commands were executed from the task worktree. Task-owned host paths are
shown below as portable redactions; command identity and observed results are
unchanged.

- Passed — focused tests, `Ran 2 tests in 0.001s`, `OK`:

  ```text
  rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> <repository-venv-python> -m unittest -v tests.test_generated_report_evidence_integrity.GeneratedReportEvidenceIntegrityTests.test_generated_markdown_home_paths_remain_portable tests.test_generated_report_evidence_integrity.GeneratedReportEvidenceIntegrityTests.test_registry_generator_provenance_groups_remain_stable
  ```

- Passed — full module, `Ran 76 tests in 20.590s`, `OK`; its controlled
  `check-generated-report-layout` assertion also passed:

  ```text
  rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> TMPDIR=<task-tmp> <repository-venv-python> -m unittest -v tests.test_generated_report_evidence_integrity
  ```

- Passed — selected compilation for the changed helper/test and final
  whitespace validation, both with no output:

  ```text
  rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-pycache> <repository-venv-python> -m py_compile ci/lib/generated_report_utils.py tests/test_generated_report_evidence_integrity.py
  rtk proxy -- git -C <task-worktree> diff --check
  ```
- Blocked evidence: direct `make check-generated-report-layout` reads committed
  generated-report evidence that currently references unavailable verified
  runtime artifacts and stale report inputs. It reports those pre-existing
  evidence/freshness failures; this task changes neither reports nor evidence.
- Blocked external dependency: `make lint` completed shell syntax and Parent CI
  Python compilation, then stopped at the isolated worktree's absent Framework
  `no_crs_baseline.py`. No control was weakened.

## Security impact

This is a static-data refactor in a path-redaction and report-provenance helper.
The local-home replacement remains byte-for-byte `<local-home-root>` and is
used only at the existing Markdown presentation points. The generator values
retain the `framework:` prefix and exact paths used by report-key inference,
metadata, hash, verified-run, and Framework-gitlink controls. No untrusted
input, resolution, hash, JSON serialization, or policy surface changes.

## Runtime evidence

No connector runtime, network, protocol, build, Framework, or MRTS behavior is
changed. Runtime/matrix execution is not required to validate a static Python
literal extraction; the direct generated-report evidence suite supplies the
proportionate regression controls.

## Known limitations

The repository's committed generated-report snapshot is not fresh against its
referenced verified runtime artifacts in this isolated worktree. The standalone
layout Make target therefore cannot serve as a clean aggregate control here.
Its in-memory/direct test control passes, and no generated report is refreshed
or altered to hide the unrelated evidence gap.

## Remaining risks

- Hosted GitHub Actions and SonarQube Cloud must still validate the exact future
  pull-request head.
- The Change-Record indexes may need a routine rebase if concurrent Parent
  Change-Record work lands first; no source conflict is expected.

## Checks not run and rationale

- Full connector/runtime/matrix execution: not applicable to static helper
  literals and would require unrelated runtime evidence.
- Framework/MRTS checks: not applicable and outside this Parent-only task.
- Scanner-policy, Quality Gate, exclusion, or suppression changes: prohibited
  and not performed.

## Final diff and review status

The current diff is limited to the Parent CI helper, its direct Parent
generated-report evidence tests, and bilingual traceability. Focused security
preflight found no validated vulnerability and requires only exact-value
preservation, which the direct tests cover. A local commit, Draft PR, hosted
checks, SonarQube Cloud result, review state, and merge are not claimed at
record authoring. No default-branch action is authorized or implied.
