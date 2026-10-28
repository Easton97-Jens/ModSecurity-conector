# Change Record: CR-20261028-sonar-directory-followup

**Language:** English | [Deutsch](CR-20261028-sonar-directory-followup.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261028-sonar-directory-followup |
| Date (UTC) | 2026-10-28 |
| Base revision | `c5993ed9a7b59fc0bd58f105595ec79f596c88d6` |

## Motivation and problem statement

The current main Sonar analysis at this base reports 15 issues in `ci/` and 35 in `connectors/`: 13 security reports and 37 pointer-to-const suggestions. The user excluded the six `tests/` findings. These are remaining candidates after merged PR #430. Fresh function/flow review found no new proven exploit or actionable private const parameter. The master gate is ERROR because `new_security_rating=5`, above the required maximum `1`; its new-code period begins on `2026-05-14T18:30:31+0000`.

The case-report writer validates a runtime path, then publishes JSON directly. A failed publication does not provide the existing shared writer's atomic replacement guarantee. This change adopts that established writer and documents the remaining candidates without altering Sonar status.

## Acceptance criteria

Preserve exact successful JSON bytes, schema, filenames and valid destination paths. Failed atomic publication must preserve the previous report and remove temporary output. Use the existing private, descriptor-bound no-follow writer. Preserve host ABI, supported operator path choices, validation, rules/gates and the unchanged active selection. Leave `tests/` findings outside remediation scope and all Sonar server statuses unchanged. Deliver a new Draft PR; Cloud must independently establish the scanner effect.

## Implementation decision and rationale

`write_json()` delegates to `write_runtime_artifact_text_atomic()` with the same sorted, two-space-indented JSON plus trailing newline and the existing output label. That helper validates the runtime path, rejects unsafe objects through descriptor-bound checks, writes a private `0600` temporary regular file, flushes/fsyncs, and atomically replaces the target. The wrapper's duplicate path lookup is removed; other callers retain their existing import/use.

This is a real artifact-publication improvement, not a claimed exploit fix. It targets the two ambiguous `pythonsecurity:S2083` / `pythonsecurity:S8707` reports at baseline line85. The other 48 candidates are documentation only: 37 required API/stub parameter signatures and 11 reviewed CLI/path/content-flow reports. Adding pointee const would break host/native callback declarations; arbitrary restrictions on explicitly selected operator paths would change supported behavior. Git `-C` to `cwd` was not changed because it would not address the reported validated revision flow.

## Changed files

`ci/runtime/lifecycle/run-verified-case.py`, `config/testing/active-cases.json`, `reports/testing/test-selection-archive.generated.json`, `reports/audits/sonar-directory-followup-20261028.json`; this record and its German companion. The JSON records all 50 baseline positions with individual source counterevidence; it is review data, not server-closure evidence. One reviewed source digest changes; executions and archived selectors remain identical. The archive is regenerated through `ci/tools/update-test-archive.py`.

## Commands executed

- PASS: authenticated read-only main analysis/issues/hotspots/directory measures/gate through RTK and `/usr/local/bin/sonar-with-env`; complete 59-issue inventory, 50 selected positions, zero hotspots, exact base revision.
- PASS: fresh native signature/registration review and Python source/flow review. A dynamic revision control rejected 12 invalid values before lock/Git I/O and preserved a valid 40-hex value.
- Expected baseline FAIL / changed PASS: external atomic-publication probe. Both preserve exact normal JSON bytes; the new writer propagates injected publication failure, retains the old report, cleans temporary output and uses `0600` rather than baseline `0644`.
- PASS: `rtk bypass python3.15 ci/tools/run-active-tests.py --check`; 100 active cases / 80 executions, 1,893 on-demand cases separate, unchanged selection.
- PASS: existing `runtime-path.python-allowed` and `runtime-path.python-blocked` via the active runner with explicit Python3.15 and external `RUNNER_TEMP` / private output root. The first absent-output-root invocation was rejected before execution; corrected setup passed both cases.
- PASS: `rtk bypass python3.15 ci/tools/update-test-archive.py` and `--check`; only the reviewed source binding and derived archive digests change.
- PASS: `rtk make check-bilingual-docs PYTHON=/usr/local/bin/python3.15`, `rtk make check-doc-links PYTHON=/usr/local/bin/python3.15 FRAMEWORK_ROOT=<task-worktree>/modules/ModSecurity-test-Framework`, `rtk bypass python3.15 ci/tools/new-change-record.py check`, source syntax, staged `git diff --check` and default Gitleaks8.30.1 staged scan with `--redact=100`. The initial German language-switch formatting was rejected and corrected; both documentation checks then passed. Current-head CI/Cloud still requires terminal readback.

## Security impact

Preserves the runtime containment boundary and adds the shared writer's publication/descriptor safeguards. All 13 initial security reports were rechecked against actual inputs, guards and sinks; no newly exploitable flow was proven. Review is bounded to these positions. No Sonar status/rule/gate/analysis-scope changes, suppression, accepted risk, dependency update or ABI change.

## Runtime evidence

The controlled file-publication probe and two existing runtime-path cases are local evidence for this boundary. They do not qualify hosted connectors or an I12 runtime matrix.

## Known limitations

Local Python is 3.15.2; CI pins 3.15.1. No toolchain installation. Only fresh Cloud analysis can show whether the two direct-write reports disappear; the remaining 48 documented candidates are not claimed fixed or closed. The original master gate's failure is not translated into a pass.

## Remaining risks

The user chose to leave false-positive candidates documented and server-open. `tests/` findings are excluded from this task, with no analysis configuration exclusion. A green changed-code PR gate does not prove a clean master inventory or resolve unchanged baseline candidates. Failed publication behavior is checked by controlled injection, not a full crash/power-loss campaign.

## Checks not run and rationale

No full default suite, additional historical/I12 campaign, all-connector runtime matrix, deployment or merge. Only the affected file boundary and existing active cases were selected. No native code changed, so no new local native rebuild was required. Framework is materialized at the existing exact gitlink only for Parent documentation validation; no Framework/MRTS source or delivery change.

## Final diff and review status

The focused source change is reviewed and frozen. Independent native/Python triage and code/documentation review completed without a concrete regression. Local atomic writer probe, two active cases, admission/archive, documentation/link, syntax, staged whitespace and secret checks passed. New exact-head CI/Cloud results must be read in the PR; old-head results are not reused. No merge is authorized.
