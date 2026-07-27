# Change Record: Parent focused report-utility duplication reduction for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260727-sonar-focused-report-utility-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-focused-report-utility-duplication |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent duplication baseline: 2,013 duplicated lines and 0.4 percent density. Candidate: the exact shared 78-line utility prefix in the Nolog and response-header focused report generators, including nine byte/behavior-equivalent functions. |
| Boundary | Two Parent report generators, new Parent utility/test, and this English/German Change Record pair. Workflows, report refreshes, generated reports, runtime matrices, Framework/MRTS source, Gitlinks, Sonar configuration, suppressions, external issue state, and master remain unchanged. |

## Motivation and problem statement

The focused Nolog and response-header report generators duplicated their small utility layer. Maintaining it twice makes safe read/write wrappers, path redaction, dynamic import behavior, and JSON formatting harder to review consistently. This candidate centralizes only the equivalent nine-function block; it intentionally leaves generator-specific behavior such as Nolog's `action_value` local.

## Acceptance criteria

- The nine extracted utility functions retain their previous return values, exceptions, JSON formatting, and dynamic import behavior.
- `report_path_safety` remains the sole safe-root/file containment control for reads and writes.
- Outside paths remain redacted as `<runtime-artifact>/<leaf>`; valid in-root files retain relative connector/framework labels.
- Both generators retain their local CLI parsing, safe-root setup, payload/schema assembly, output calls, and generator-specific functions.
- No report refresh, runtime-all, workflow, Framework/MRTS, Gitlink, suppression, or master change occurs.
- A new exact-head SonarQube Cloud analysis, not the local diff, determines the actual global duplication change.

## Implementation decision and rationale

The new `ci/lib/focused_analysis_utils.py` owns only `utc_now`, safe JSON/text wrappers, list coercion, queue totals, dynamic import, path sanitization, and quoted-comma action parsing. Each generator retains `add_safe_roots`, `add_report_roots`, `resolve_output_dir`, CLI handling, schema/payload construction, and output orchestration. The helper delegates file operations to the unchanged `report_path_safety` wrappers and does not configure or mutate `SAFE_ROOTS`.

## Changed files

- ci/evidence/reports/generate-nolog-audit-evidence-analysis.py
- ci/evidence/reports/generate-response-header-hook-analysis.py
- ci/lib/focused_analysis_utils.py
- tests/test_focused_analysis_utils.py
- reports/audits/change-records/CR-20260727-sonar-focused-report-utility-duplication.md
- reports/audits/change-records/CR-20260727-sonar-focused-report-utility-duplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Commands executed

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_focused_analysis_utils tests.test_generated_report_evidence_integrity tests.test_report_presentation_literals
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B ci/evidence/reports/generate-nolog-audit-evidence-analysis.py --help
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B ci/evidence/reports/generate-response-header-hook-analysis.py --help
rtk proxy git diff --check
```

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused utility contract | passed: 7 tests for shared bindings, parsing, totals, in-root read/write, outside-root redaction/refusal, safe-root preservation, and module registration. |
| Evidence/presentation regression modules | passed: 84 tests total; their generated-report-layout check reported `PASS`. |
| Both generator `--help` entrypoints | passed without generating or refreshing report artifacts. |
| Independent security/path review | passed: no security blocker or changed safe-root/evidence-integrity control. |
| `git diff --check` | passed: no whitespace errors. |

## Security impact

This is a security-relevant refactor because it touches report path and evidence utilities. The helper delegates reads to `read_json_file`/`read_text_file`, writes to `write_json_file`, and path classification to `safe_existing_file`; those existing functions enforce configured safe roots and regular-file checks. The helper neither clears nor expands safe roots. Dynamic imports retain the prior fixed caller-controlled paths and `sys.modules` registration-before-execution behavior. No new security finding was identified.

## Documentation status

This complete English/German Change Record pair documents scope, actual local validation, the no-refresh boundary, and the fact that an external SonarQube Cloud measure is still required. Both change-record indexes are updated.

## Runtime evidence

No report refresh, connector runtime, protocol test, or production behavior was run or claimed. The two `--help` invocations demonstrate only direct-script import/argument initialization; the test modules provide helper/evidence-contract checks.

## Known limitations

No base-versus-candidate full-report byte comparison was run because report refresh/generation is deliberately outside this task. Helper-level outside-root behavior is directly tested, while traversal/symlink cases continue to be enforced by the unchanged `report_path_safety` implementation and existing integrity suite. SonarQube Cloud has not analyzed the candidate, so no observed global reduction is claimed.

## Remaining risks

The shared dynamic-import utility still executes trusted configured script paths; that was an existing trust boundary, not broadened by this extraction. A future integration fixture may execute each generator end to end against a dedicated non-generated output root. This candidate makes no conclusion about other duplicate blocks or the broader 1,022-item backlog.

## Checks not run and rationale

- No `refresh-all-reports`, runtime-all, 12-cell matrix, generated-report update, or workflow change was run because each is explicitly out of scope.
- Connector builds and MRTS tests are not applicable because no connector or cross-repository source changed.
- Hosted GitHub checks and exact-head SonarQube Cloud analysis have not yet occurred; this record gives neither a global duplication result nor master-merge authority.

## Final diff and review status

The candidate is limited to the two parent report generators, a small Parent helper and direct test, plus required bilingual traceability material. An independent security/path review found no blocker. Commit, push, PR, hosted-check, Sonar-analysis, and merge facts will be recorded only after they are observed.
