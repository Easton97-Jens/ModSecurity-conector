# Change Record: Parent CI marker-section and script-literal deduplication for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260728-sonar-ci-marker-script-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-ci-marker-script-deduplication |
| Date (UTC) | 2026-07-28 |
| Base revision | `8a3872e5e63f93e202bed24e0dcbad7bdf110ede` |
| Scope and boundary | Parent `ci/`, `scripts/`, directly focused Parent tests, and this English/German Change Record pair with its indexes only. `.github/`, Framework, MRTS, gitlinks, generated reports, and SonarQube configuration remain unchanged. |
| Finding linkage | The pre-PR SonarQube Cloud master analysis reported 631 open issues, 0.2% project duplication (1,260 lines), and `python:S1192` issues `AZ9cRzA4HhV2CayPTP47` and `AZ9cRzA4HhV2CayPTP46` in the repository-organization inventory. The CI clone evidence includes the 113-line nolog/response-header pair. This record does not claim historical issue closure or a master integration. |

## Motivation and problem statement

Six Parent report generators independently performed the same bounded Markdown
marker replacement, insertion-before-anchor, and append fallback. Two of
those generators also carried an identical Framework-case lookup that already
used the safe-file boundary. This duplicated code raised maintenance cost and
contributed to the measured Parent CI duplication cluster.

The repository-organization inventory separately repeated two stable literals:
the German Markdown suffix and the Parent-relative Framework path prefix. The
current Sonar issues identify those literal repetitions directly.

## Acceptance criteria

- `find_framework_case_path()` keeps the existing case-name rejection,
  searches only the existing Framework case/upstream roots, and returns only a
  `safe_existing_file` result.
- `upsert_marked_section()` has no filesystem effects and preserves the
  existing marker replacement, selected-anchor insertion, fallback append,
  blank-line, and final-newline behavior.
- All six report generators retain their existing report paths and safe
  reader/writer calls; no output destination is newly derived or broadened.
- The inventory retains English/German classification and Parent/Framework
  routing with named equivalents of the prior literals.
- Focused utility and inventory tests, report conditional-remediation tests,
  syntax compilation, and whitespace validation pass.

## Implementation decision and rationale

The shared helpers are located in the pre-existing Parent-only
`ci/lib/focused_analysis_utils.py` module. `find_framework_case_path()` is an
unchanged relocation of the two cloned implementations. The marker helper is a
pure string operation using literal `split()` boundaries rather than a broad
regular expression. Callers retain their current `read_text()` and
`write_text_file()` operations, so `report_path_safety` remains the write
enforcement boundary.

`FRAMEWORK_PATH_PREFIX` and `GERMAN_MARKDOWN_SUFFIX` name the two invariant
script values. They do not alter tracked-file enumeration, destination
selection, temporary output handling, or Framework ownership.

## Changed files

- `ci/lib/focused_analysis_utils.py`
- `ci/evidence/reports/generate-nolog-audit-evidence-analysis.py`
- `ci/evidence/reports/generate-response-header-hook-analysis.py`
- `ci/evidence/reports/generate-rule-chain-semantics-analysis.py`
- `ci/evidence/reports/generate-phase4-hard-abort-capability.py`
- `ci/evidence/reports/generate-remaining-failure-analysis.py`
- `ci/evidence/reports/generate-no-mrts-intervention-nomatch-analysis.py`
- `scripts/generate_repository_organization_inventory.py`
- `tests/test_focused_analysis_utils.py`
- `tests/test_repository_organization_inventory.py`
- this English/German Change Record pair and both indexes

## Commands executed

| Command or control | Actual result |
| --- | --- |
| Current SonarQube Cloud issue, measure, component-tree, and duplication API readback | passed: 631 open/confirmed issues; 0.2% / 1,260 duplicated lines; selected Parent-only CI and script evidence recorded above. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_focused_analysis_utils tests.test_repository_organization_inventory` | passed: 16 tests. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_report_conditional_remediation` | passed: 9 tests. |
| `env PYTHONPYCACHEPREFIX=<task-owned external cache> python3 -P -m py_compile <changed Python files>` | passed. |
| `git diff --check` | passed; no whitespace error was reported. |
| Direct `python3 -m compileall` | blocked_environment: it attempts to write `__pycache__` beneath the read-only task worktree. The equivalent selected-file `py_compile` control passed with the cache redirected to a registered task-owned external directory. |
| Direct bilingual-documentation and repository-path checks | blocked_environment: all diagnostics name missing targets below the unpopulated Framework gitlink; none names this Change Record pair or its indexes. |

## Security impact

This is a CI/reporting and path-sensitive boundary review. The Framework-case
helper preserves the existing slash/backslash rejection and `safe_existing_file`
gate unchanged. The marker helper neither reads nor writes files and accepts
only caller-provided static markers and anchors. Each caller keeps its existing
safe report-path configuration and writer.

No workflow permissions, action pins, scanner controls, suppressions, runtime
path policy, Framework/MRTS source, gitlink, or generated report changes are
included. Current security-classified Sonar rows were rechecked against the
canonical `FND-SONAR-0001` triage and are not represented as fixes in this
duplication batch.

## Runtime evidence

The passed checks are local source, import, and focused-unit evidence only.
They do not claim report generation, runtime matrix execution, a connector
runtime, Framework/MRTS execution, or hosted CI/SonarQube Cloud analysis.

## Known limitations

The change intentionally addresses a bounded subset of the 1,260 project
duplicate lines. Current SonarQube Cloud analysis of the active PR head is
external delivery evidence and must be verified at that exact head; it is not
frozen in this static source record. A future report generator with a materially
different anchor is outside this batch.

## Remaining risks

A future report generator with a materially different anchor must use the
helper deliberately and retain an exact-output control. Hosted SonarQube Cloud
analysis may identify residual clones in the broader report-generator family;
those need a separate evidence-backed selection rather than an unreviewed
large refactor.

## Checks not run and rationale

- Report generation, connector/CRS matrices, and runtime checks were not run:
  the change is a source-only deduplication and no generated artifact was
  intentionally refreshed.
- `make lint` was not run: its required `check-framework` prerequisite cannot
  use the unpopulated Parent-pinned Framework gitlink in this task worktree.
  The selected Python files instead passed direct syntax and focused behavior
  controls.
- The direct documentation checks cannot complete while the same Framework
  gitlink is unpopulated; their diagnostics did not identify this record pair
  or either index as a defect.
- Hosted CI and SonarQube Cloud are external delivery controls. Their result
  must be verified at the active PR head rather than copied into this static
  record.

## Final diff and review status

Local review found only the declared Parent source, test, and traceability
files. The task worktree is based on the fresh remote master revision above;
the original shared checkout's unrelated Framework-gitlink change was not
copied or staged. No merge or master update is authorized or claimed.
