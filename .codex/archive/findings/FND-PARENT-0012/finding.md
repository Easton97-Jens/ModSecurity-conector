# FND-PARENT-0012 — C++ evaluator had easily-swappable string-parameter hardening gaps

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0012` |
| Title / Titel | `C++ evaluator had easily-swappable string-parameter hardening gaps` |
| Category / Kategorie | `compiler_hardening_gap` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `validated` |
| Status | `closed` (archived) |
| Feasibility status / Machbarkeitsstatus | `feasible_after_local_setup` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

The prior real Clang-Tidy baseline reported two
`bugprone-easily-swappable-parameters` diagnostics for internal C++ evaluator
string parameters. Current calls were correct, but the signatures made future
call-order mistakes unnecessarily easy.

## Observed behavior / Beobachtetes Verhalten

`bracket_value` accepted two canonical string parameters, and the sole
`append_decision_log` call supplied a long run of same-type arguments.

## Expected behavior / Erwartetes Verhalten

Internal evaluator interfaces distinguish a field key from the intervention
log and use named decision-record fields without changing emitted records or
evaluator outcomes.

## Impact / Auswirkung

This was a bounded hardening gap, not a validated request-security bypass or
current functional defect.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `common/scripts/modsecurity_targeted_eval.cc`
- `tests/test_c_cpp_diagnostics.py`

### Symbols / Symbole

- `bracket_value`
- `DecisionLogInput`
- `append_decision_log`

## Preconditions / Voraussetzungen

- A task-owned C++17 build, compilation database, and analysis output are available.
- The validated external libmodsecurity headers and library remain available.

## Reproduction / Reproduktion

- Run focused real Clang analysis with `CLANG_TIDY_CHECKS='-*,bugprone-easily-swappable-parameters'` against the fresh C++17 compilation database.

## Evidence / Evidence

- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/029-cpp17-targeted-evaluator-cpp17.log`; type: `cxx17_compile_log`; SHA-256: `083b7d535465fcb2f09d9ee5b7e14385f749d3f8d490acee43047ec5a712ec74`
  - Command: `CXX=/usr/bin/clang++ ... make check-targeted-evaluator-cpp17`; working directory: `/root/git/ModSecurity-conector`; exit code: `0`; observed: `2026-07-17T12:54:50Z`; retention: `retained_task_log`
- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/031-cpp17-clang-tidy-swappable-parameters.log`; type: `clang_tidy_analysis_log`; SHA-256: `aaa6deb035c9170dc2170a687db32a801f0513e589f8a86d20103529a7d2d746`
  - Command: `CLANG_TIDY_CHECKS='-*,bugprone-easily-swappable-parameters' make clang-analysis-baseline`; working directory: `/root/git/ModSecurity-conector`; exit code: `0`; observed: `2026-07-17T12:55:26Z`; retention: `retained_task_log`
- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/034-cpp17-evaluator-allow-block-controls.log`; type: `direct_evaluator_control_log`; SHA-256: `141216acc6602f06f25f210bd809b0c25bd4a2d9cc42ff97757a3d6c389d3827`
  - Command: direct evaluator Allow/Block controls; working directory: `/root/git/ModSecurity-conector`; exit code: `0`; observed: `2026-07-17T12:56:52Z`; retention: `retained_task_log`

## Root-cause analysis / Grundursachenanalyse

Two internal functions had adjacent canonical `std::string` parameter types.
The original calls were correct, but the interface did not encode their
distinct meanings.

## Proposed remediation / Vorgeschlagene Remediation

Use `std::string_view` for the immutable bracket field key and a value-owning
`DecisionLogInput` record at the sole decision-log call site.

## Acceptance criteria / Akzeptanzkriterien

- The evaluator compiles with C++17 `-Wall -Wextra -Werror`.
- Focused swappable-parameter Clang analysis has zero normalized findings.
- Allow remains status `200`; blocking remains status `403` with rule ID `1000001`.
- No public C or C++ API/ABI changes are introduced.

## Validation plan / Validierungsplan

- Compile the production evaluator and capture a real compilation database.
- Run focused and normal Clang analysis profiles.
- Run diagnostics contract tests and direct Allow/Block evaluator controls.

## Regression tests / Regressionstests

- `tests/test_c_cpp_diagnostics.py`
- Focused real Clang-Tidy swappable-parameter analysis.

## Legitimate control tests / Legitime Kontrolltests

- Direct evaluator Allow control: status `200`.
- Direct evaluator blocking control: status `403` and rule ID `1000001`.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-PARENT-0008`

## Residual risk / Restrisiko

Static analysis and direct evaluator controls do not substitute for every
connector runtime. No current parameter-order defect or request-security
bypass was found.

## History / Historie

- `2026-07-17T13:10:00Z`: `phase_b_preflight_and_remediation_verified` — distinct Parent-only hardening was compiled, analyzed, and verified through direct Allow/Block controls.
- `2026-07-26T14:09:02Z`: `closed_by_current_user_after_current_master_validation` — the current user authorized closure and archival; `tests.test_c_cpp_diagnostics` passed on Parent master `6ca7e1536ce7e93da68099db9c586b88852ff13e` as part of the 144-test control suite.
