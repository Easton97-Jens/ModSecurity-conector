# Change Record: CR-20261027-sonar25-maintainability

**Language:** English | [Deutsch](CR-20261027-sonar25-maintainability.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261027-sonar25-maintainability |
| Date (UTC) | 2026-10-27 |
| Base revision | `0867713cca9401a80831f116efdacce4727d4e13` |

## Motivation and problem statement

The user explicitly requested correction of the 25 remaining Sonar findings in PR #382. A complete authenticated CLI readback confirmed 11 cognitive-complexity findings, eight duplicated literals, two generator constructors, two verbose regex classes, one nested conditional expression and one ambiguous exception test. Scope is six existing native-analysis helpers and one existing test.

## Acceptance criteria

Fix these 25 issues through source changes, preserve behavior and security checks, introduce no new finding in the changed sources, and verify the new published head with required CI and the existing Sonar analyses. Keep 100 expanded automatic cases / 80 executions, 1893 on-demand cases / 839 executions and E2E 26. No new feature, test catalog, I12 campaign, analysis project, Framework/MRTS work, merge, release or deployment.

## Implementation decision and rationale

Extract ordered SDK/archive, capture, producer, source-mapping and graph-validation steps into small helpers; retain existing public signatures, actual commands, explicit errors, check order and manifest formats. Name duplicated literals with constants and use dictionary comprehensions. Regex shortcuts preserve ASCII digit semantics. Build the exception fixture before entering assertRaisesRegex so only the intended call may satisfy the expected failure.

## Changed files

`ci/checks/analysis/prepare-sonar-native-ci.py`; `ci/checks/analysis/sonar-native-security/{build-target,capture,go_provenance,source_mapping,validate}.py`; `tests/test_sonar_native_ci.py`; source digests in `config/testing/active-cases.json`; the generator-produced archive; this EN/DE record and the compact PR status pair. Test selectors, expanded cases, workflows, gates and source scope are unchanged.

## Commands executed

RTK wrapped rule/API readback, source/diff review and AST/syntax checks. All 11 baseline complexity scores matched the read-only estimator; the changed functions estimate at most 15. The seven original validator functions are AST-identical after helper/state normalization and scoped ASCII regex normalization. Independent review found no concrete regression. Canonical inventory admission `972866207512972dda9bc4b4d7be387fcbf35f8d5b13753b684dc2f40a177adb` preceded explicit on-demand execution: 29 existing executors / 38 expanded cases PASS, zero skips. The archive was regenerated with `ci/tools/update-test-archive.py`. Evidence is retained under the external task root `runs/pr382-sonar25-20261027`, including `targeted-admission.json` and `active-tests-_i43xiv4/summary.json`.

## Security impact

The refactor retains ownership/permissions, canonical ancestry, source/header/hash closure, actual compiler/linker provenance, archive boundaries, private outputs, SDK identity, exact revision and scanner/gate controls. No suppression, exclusion, accepted-risk disposition, dependency change or control weakening was introduced.

## Runtime evidence

Focused tests use existing offline fixtures, including the real validator export seam; no application, connector host, historical matrix or Oracle campaign was launched locally. The previous SDK/native analysis results belong to base 0867713. Current-head automatic CI and server results are maintained on the PR.

## Known limitations

AST and local tests prove their own layers. The complexity estimator is calibrated static guidance, not an authoritative Sonar result. Implicit Python diagnostics for malformed pin lines remain ValueError rejection; no new pin syntax is admitted. Fresh Hosted analysis is required to confirm issue closure and actual builds.

## Remaining risks

Helper extraction touches provenance and traversal paths; targeted negatives and static ordering checks passed. The final published-head Sonar/CI result remains the delivery criterion, with actual terminal status recorded on PR #382. Existing unrelated advisory baseline findings stay outside this focused request.

## Checks not run and rationale

No full offline catalog, new tests, extra native campaign, dependency installation or local scanner campaign. Existing automatic workflows run after the necessary normal push; repeated checks require a concrete correction or infrastructure cause. Coverage remains outside acceptance under the earlier user decision.

## Final diff and review status

Scoped source review and focused tests passed. Normal commit/push is limited to the existing task branch. Final head identity, actual CI/Sonar issue resolution, review feedback, Ready state and stopped monitors are recorded on [PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) and the [compact closure record](../../../docs/pr-382-merge-readiness.md). No master merge is authorized.
