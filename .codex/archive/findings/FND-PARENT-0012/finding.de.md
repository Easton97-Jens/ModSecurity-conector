# FND-PARENT-0012 — C++-Evaluator hatte Hardening-Lücken durch leicht vertauschbare String-Parameter

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0012` |
| Title / Titel | `C++-Evaluator hatte Hardening-Lücken durch leicht vertauschbare String-Parameter` |
| Category / Kategorie | `compiler_hardening_gap` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `validated` |
| Status | `closed` (archiviert) |
| Feasibility status / Machbarkeitsstatus | `feasible_after_local_setup` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Die frühere reale Clang-Tidy-Baseline meldete zwei
`bugprone-easily-swappable-parameters`-Diagnosen für interne C++-Evaluator-
String-Parameter. Die aktuellen Aufrufe waren korrekt, aber die Signaturen
machten künftige Verwechslungen der Aufrufreihenfolge unnötig leicht.

## Observed behavior / Beobachtetes Verhalten

`bracket_value` akzeptierte zwei kanonische String-Parameter und der einzige
`append_decision_log`-Aufruf übergab eine lange Folge gleich typisierter
Argumente.

## Expected behavior / Erwartetes Verhalten

Interne Evaluator-Schnittstellen unterscheiden einen Field-Key vom
Intervention-Log und verwenden benannte Decision-Record-Felder, ohne
ausgegebene Records oder Evaluator-Ergebnisse zu ändern.

## Impact / Auswirkung

Dies war eine begrenzte Hardening-Lücke, kein validierter Request-Security-
Bypass und kein aktueller funktionaler Defekt.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `common/scripts/modsecurity_targeted_eval.cc`
- `tests/test_c_cpp_diagnostics.py`

### Symbols / Symbole

- `bracket_value`
- `DecisionLogInput`
- `append_decision_log`

## Preconditions / Voraussetzungen

- Ein task-owned C++17-Build, eine Compilation Database und Analyseausgabe sind verfügbar.
- Die validierten externen libmodsecurity-Header und -Library bleiben verfügbar.

## Reproduction / Reproduktion

- Fokussierte reale Clang-Analyse mit `CLANG_TIDY_CHECKS='-*,bugprone-easily-swappable-parameters'` gegen die frische C++17-Compilation-Database ausführen.

## Evidence / Evidence

- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/029-cpp17-targeted-evaluator-cpp17.log`; type: `cxx17_compile_log`; SHA-256: `083b7d535465fcb2f09d9ee5b7e14385f749d3f8d490acee43047ec5a712ec74`
  - Command: `CXX=/usr/bin/clang++ ... make check-targeted-evaluator-cpp17`; working directory: `/root/git/ModSecurity-conector`; exit code: `0`; observed: `2026-07-17T12:54:50Z`; retention: `retained_task_log`
- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/031-cpp17-clang-tidy-swappable-parameters.log`; type: `clang_tidy_analysis_log`; SHA-256: `aaa6deb035c9170dc2170a687db32a801f0513e589f8a86d20103529a7d2d746`
  - Command: `CLANG_TIDY_CHECKS='-*,bugprone-easily-swappable-parameters' make clang-analysis-baseline`; working directory: `/root/git/ModSecurity-conector`; exit code: `0`; observed: `2026-07-17T12:55:26Z`; retention: `retained_task_log`
- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/034-cpp17-evaluator-allow-block-controls.log`; type: `direct_evaluator_control_log`; SHA-256: `141216acc6602f06f25f210bd809b0c25bd4a2d9cc42ff97757a3d6c389d3827`
  - Command: direkte Evaluator-Allow/Block-Controls; working directory: `/root/git/ModSecurity-conector`; exit code: `0`; observed: `2026-07-17T12:56:52Z`; retention: `retained_task_log`

## Root-cause analysis / Grundursachenanalyse

Zwei interne Funktionen hatten benachbarte kanonische `std::string`-
Parametertypen. Die ursprünglichen Aufrufe waren korrekt, aber die Schnittstelle
kodierte ihre unterschiedlichen Bedeutungen nicht.

## Proposed remediation / Vorgeschlagene Remediation

`std::string_view` für den unveränderlichen Bracket-Field-Key und einen
value-owning `DecisionLogInput`-Record an der einzigen Decision-Log-Call-Site
verwenden.

## Acceptance criteria / Akzeptanzkriterien

- Der Evaluator kompiliert mit C++17 `-Wall -Wextra -Werror`.
- Die fokussierte Swappable-Parameter-Clang-Analyse hat null normalisierte Findings.
- Allow bleibt Status `200`; Blocking bleibt Status `403` mit Regel-ID `1000001`.
- Es werden keine öffentlichen C- oder C++-API-/ABI-Änderungen eingeführt.

## Validation plan / Validierungsplan

- Production-Evaluator kompilieren und eine reale Compilation Database erfassen.
- Fokussierte und normale Clang-Analyseprofile ausführen.
- Diagnostics-Contract-Tests und direkte Evaluator-Allow/Block-Controls ausführen.

## Regression tests / Regressionstests

- `tests/test_c_cpp_diagnostics.py`
- Fokussierte reale Clang-Tidy-Swappable-Parameter-Analyse.

## Legitimate control tests / Legitime Kontrolltests

- Direkter Evaluator-Allow-Control: Status `200`.
- Direkter Evaluator-Blocking-Control: Status `403` und Regel-ID `1000001`.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-PARENT-0008`

## Residual risk / Restrisiko

Statische Analyse und direkte Evaluator-Controls ersetzen nicht jede
Connector-Runtime. Es wurde kein aktueller Parameterreihenfolge-Defekt und
kein Request-Security-Bypass gefunden.

## History / Historie

- `2026-07-17T13:10:00Z`: `phase_b_preflight_and_remediation_verified` — das getrennte Parent-only-Hardening wurde kompiliert, analysiert und durch direkte Allow/Block-Controls verifiziert.
- `2026-07-26T14:09:02Z`: `closed_by_current_user_after_current_master_validation` — der aktuelle Nutzer autorisierte Abschluss und Archivierung; `tests.test_c_cpp_diagnostics` bestand auf Parent-Master `6ca7e1536ce7e93da68099db9c586b88852ff13e` als Teil der 144-Test-Control-Suite.
