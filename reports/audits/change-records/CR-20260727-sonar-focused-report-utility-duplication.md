# Change Record: Parent focused report-utility duplication reduction for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260727-sonar-focused-report-utility-duplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-focused-report-utility-duplication |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent duplication baseline: 2,013 duplicated lines and 0.4 percent density. The initial exact analysis for Draft PR #135, before the current local remediation, reported 1,834 duplicated lines, 22 new duplicated lines, and 9.2% new-code duplication. That head failed the ≤3% new-code-duplication gate and reported `python:S3776` and `python:S3358`. |
| Boundary | Nine Parent focused report generators, one Parent utility, one Parent-focused test, this English/German Change Record pair, and the already-existing index entries. Workflows, report refreshes, generated reports, runtime matrices, Framework/MRTS source, Gitlinks, Sonar configuration, suppressions, external issue state, and master remain unchanged. |

## Motivation and problem statement

The Nolog and response-header focused report generators originally duplicated a
small utility layer. The first extraction reduced the observed global count,
but its exact Draft PR #135 analysis still failed because the new helper
duplicated existing implementation lines and its quoted-comma parser reported
`python:S3776` and `python:S3358`. The current local remediation removes those
new-code duplication sources without scheduling report refreshes or runtime
work: it reuses existing safe primitives and shares behavior-equivalent utility
bindings across nine focused report generators. Generator-specific analysis,
payload, CLI, and output behavior remains local.

## Acceptance criteria

- The shared utility bindings retain prior return values, exceptions, JSON formatting, dynamic-import behavior, and `as_list` scalar/list behavior, including preserving a nonempty scalar whitespace string.
- `report_path_safety` remains the sole safe-root/file-containment control for reads and writes; the helper does not configure or mutate `SAFE_ROOTS`.
- Outside paths remain redacted as `<runtime-artifact>/<leaf>`; valid in-root files retain relative connector/framework labels.
- All nine generators retain their local CLI parsing, safe-root setup, payload/schema assembly, output calls, and generator-specific functions.
- `action_parts` preserves quoted commas, mixed quotes, empty segments, and unterminated quotes while avoiding the prior complexity/nested-conditional shape.
- No report refresh, runtime-all, workflow, Framework/MRTS, Gitlink, suppression, or master change occurs.
- A fresh exact-head SonarQube Cloud analysis after the uncommitted remediation is delivered, rather than a local clone comparison, determines the current Quality Gate and global duplication result.

## Implementation decision and rationale

`ci/lib/focused_analysis_utils.py` directly aliases `generated_report_utils.utc_now`, `report_path_safety.read_json_file`, `report_path_safety.read_text_file`, and `report_path_safety.write_json_file` as `utc_now`, `read_json`, `read_text`, and `write_json`. It retains only the focused list coercion, queue totals, dynamic import, path sanitization, and quoted-comma parsing that are not already provided by those primitives.

The helper keeps `as_list` compatible with the prior generators: list items with blank string representations are filtered, while a non-list nonempty scalar is returned unchanged as a single string. `action_parts` is decomposed into `_next_quote` and `_append_action_part`; the direct contract suite covers quoted, mixed-quote, empty-segment, and unterminated-quote cases. The nine generators import only behavior-equivalent bindings, retain their own `add_safe_roots`, `add_report_roots`, `resolve_output_dir`, CLI handling, schema/payload construction, and output orchestration, and do not change a report-path control.

## Changed files

- ci/evidence/reports/generate-nolog-audit-evidence-analysis.py
- ci/evidence/reports/generate-response-header-hook-analysis.py
- ci/evidence/reports/generate-body-processor-analysis.py
- ci/evidence/reports/generate-rule-chain-semantics-analysis.py
- ci/evidence/reports/generate-no-mrts-intervention-nomatch-analysis.py
- ci/evidence/reports/generate-intervention-blocking-analysis.py
- ci/evidence/reports/generate-phase4-hard-abort-capability.py
- ci/evidence/reports/generate-remaining-failure-analysis.py
- ci/evidence/reports/generate-final-consistency-audit.py
- ci/lib/focused_analysis_utils.py
- tests/test_focused_analysis_utils.py
- reports/audits/change-records/CR-20260727-sonar-focused-report-utility-duplication.md
- reports/audits/change-records/CR-20260727-sonar-focused-report-utility-duplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Commands executed

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_focused_analysis_utils tests.test_generated_report_evidence_integrity tests.test_report_presentation_literals tests.test_remaining_failure_analysis
rtk proxy bash -lc 'for task_file in ci/evidence/reports/generate-nolog-audit-evidence-analysis.py ci/evidence/reports/generate-response-header-hook-analysis.py ci/evidence/reports/generate-body-processor-analysis.py ci/evidence/reports/generate-rule-chain-semantics-analysis.py ci/evidence/reports/generate-no-mrts-intervention-nomatch-analysis.py ci/evidence/reports/generate-intervention-blocking-analysis.py ci/evidence/reports/generate-phase4-hard-abort-capability.py ci/evidence/reports/generate-remaining-failure-analysis.py ci/evidence/reports/generate-final-consistency-audit.py; do /root/git/ModSecurity-conector/.venv/bin/python -B "$task_file" --help >/dev/null || exit $?; done'
rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-doc-links
rtk proxy git diff --check
```

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused utility/evidence regression modules | passed: 86 tests across `tests.test_focused_analysis_utils`, `tests.test_generated_report_evidence_integrity`, `tests.test_report_presentation_literals`, and `tests.test_remaining_failure_analysis`. The focused utility suite includes safe-root/redaction/write rejection, shared binding, scalar/list coercion, dynamic-import, and quoted-comma parser controls. |
| Generated-report layout | passed: the focused test command reported `check-generated-report-layout: PASS`. |
| Nine generator `--help` entrypoints | passed without generating or refreshing report artifacts. |
| Focused security/path review | passed: direct aliases preserve the existing safe-root/evidence-integrity controls; no new security blocker was identified. |
| `make check-bilingual-docs` | passed: `bilingual docs ok`. |
| `make check-doc-links` | passed: `repository path references: PASS` and `doc links ok`. |
| `git diff --check` | passed: no whitespace errors. |
| Initial exact Draft PR #135 SonarQube Cloud analysis | failed: 22 new duplicated lines and 9.2% new-code duplication exceeded ≤3%; `python:S3776` and `python:S3358` were also reported. |
| Current uncommitted remediation | not run externally: it needs a new exact-head SonarQube Cloud analysis after an observed commit and push. |

## Security impact

This is a security-relevant refactor because it touches report path and evidence utilities. Reads and writes remain the existing `report_path_safety.read_json_file`, `report_path_safety.read_text_file`, and `report_path_safety.write_json_file` controls; path classification remains `safe_existing_file`. The helper neither clears nor expands `SAFE_ROOTS`. Dynamic imports retain their prior fixed caller-controlled paths and `sys.modules` registration-before-execution behavior. No new security finding was identified.

## Documentation status

This complete English/German Change Record pair now describes the expanded nine-generator candidate, the observed initial SonarQube Cloud failure, and the required fresh exact-head analysis. Both Change Record index entries already existed and need no additional change.

## Runtime evidence

No report refresh, connector runtime, protocol test, or production behavior was run or claimed. The nine `--help` calls demonstrate only direct-script import/argument initialization; the test modules provide helper and evidence-contract checks.

## Known limitations

No base-versus-candidate full-report byte comparison was run because report refresh/generation is deliberately out of scope. Helper-level outside-root behavior is directly tested; traversal/symlink cases remain enforced by the unchanged `report_path_safety` implementation and its integrity suite. The local clone comparison is not SonarQube Cloud evidence. The current remediated state is uncommitted, so it has no new exact-head result.

## Remaining risks

The shared dynamic-import utility still executes trusted configured script paths; that is an existing trust boundary and was not broadened. A future integration fixture may execute each generator end to end against a dedicated non-generated output root. This candidate makes no conclusion about other duplicate blocks or the broader 1,022-item backlog.

## Checks not run and rationale

- No `refresh-all-reports`, runtime-all, 12-cell matrix, generated-report update, or workflow change was run because each is explicitly out of scope.
- Connector builds and MRTS tests are not applicable because no connector or cross-repository source changed.
- No fresh hosted GitHub check or exact-head SonarQube Cloud analysis exists for the current uncommitted remediation. The prior exact Draft PR #135 analysis failed and cannot validate this follow-up.

## Final diff and review status

Draft PR #135's initial exact head is not ready for review or merge because its SonarQube Cloud analysis failed. The expanded remediation described here is local, uncommitted, and unpushed; it has no new remote or PR head. No Framework, MRTS, Gitlink, ready-for-review, or master action occurred. A commit/push followed by a fresh exact-head analysis is the required next delivery validation.
