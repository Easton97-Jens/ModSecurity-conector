# FND-PARENT-0008 — Clang Werror lehnt fehlenden Field-Initializer in Apache msc_config.c ab

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0008` |
| Title / Titel | `Clang Werror lehnt fehlenden Field-Initializer in Apache msc_config.c ab` |
| Category / Kategorie | `compiler_warning` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `validated` |
| Status | `fixed` |
| Feasibility status / Machbarkeitsstatus | `feasible_now` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Historische Apache-C17-Evidence zeichnete einen Clang-Werror-missing-field-
initializer-Fehler am `module_directives`-Terminator auf. Der exakte lokale
Commit `313cae2550bf7c8ff8eadc71065dbd617762c8cc` ändert `{NULL}` zu
`{ .name = NULL }`; der Parent-Task meldet, dass GCC-/Clang-Compiler-,
Structural-, frische-DSO- und Apache-Legitimate-Controls bestehen. Er ist nur
auf dem exakten lokalen Head von Draft PR #183 fixed, nicht verified oder closed.

## Observed behavior / Beobachtetes Verhalten

Der historische positionale `{NULL}`-Terminator initialisierte nur das erste
`command_rec`-Feld. Der exakte committete Kandidat besitzt den designierten
`{ .name = NULL }`-Terminator und bestand die gemeldeten GCC-/Clang-RulesSet-
Cleanup-Harnesses, Lint, Apache/Common-Structural- und C-Standard-Wiring,
frischen materialisierten DSO-make, HTTP/1.1-phase-2-403 und SIGUSR1-Readiness.

## Expected behavior / Erwartetes Verhalten

Der designierte Terminator muss die GCC- und Clang-C17-Warning-Policy erfüllen
und normales Apache-Konfigurations- und Request-Lifecycle-Verhalten bewahren.
Exact-Head-Hosted-Validierung von Draft PR #183 und resulting-master-
Reproduktion stehen noch aus.

## Impact / Auswirkung

Die lokale exakte Korrektur entfernt den aufgezeichneten Warning-Policy-Fehler
ohne request-facing Verhaltensänderung. Hosted-Validierung, Review, Merge und
resulting-master-Reproduktion wurden noch nicht beobachtet.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `connectors/apache/src/msc_config.c`

### Symbols / Symbole

- `module_directives-Terminator`

## Preconditions / Voraussetzungen

- Die genehmigte Apache/APXS/APR/libModSecurity-Compiler-Umgebung ist verfügbar.
- Der exakte Draft-PR-#183-Head `313cae2550bf7c8ff8eadc71065dbd617762c8cc` ist der aktuell veröffentlichte Head.

## Reproduction / Reproduktion

- Den historischen `{NULL}`-Terminator und den exakten Kandidaten-
  `{ .name = NULL }`-Terminator untersuchen.
- GCC-/Clang-`make check-apache-ruleset-cleanup` und die fokussierten Controls
  auf Draft PR #183 und resultierendem Master wiederholen.

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:594-613`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '594,613p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

Der positionale `{NULL}`-Terminator verletzt die konfigurierte Clang-missing-
field-initializer-Werror-Policy. Der designierte Initializer des exakten
Kandidaten drückt die beabsichtigte Terminator-Semantik explizit aus.

## Proposed remediation / Vorgeschlagene Remediation

Die exakte Initializer-Korrektur in Draft PR #183 beibehalten, Exact-Head-
Hosted-Checks und Review erfassen und danach den ursprünglichen Compiler-Zustand
auf dem resultierenden Master vor verified oder closed reproduzieren.

## Acceptance criteria / Akzeptanzkriterien

- Beide GCC- und Clang-C17-Builds bestehen mit der erforderlichen Warning-Policy
  auf dem exakten committeten PR-Head.
- Structural-, materialisierte-DSO- und Apache-Legitimate-Controls decken die
  betroffene Initialisierungssemantik ab.
- Hosted-Exact-Head- und resulting-master-Reproduktions-Evidence liegt vor,
  bevor verified oder closed gesetzt wird.

## Validation plan / Validierungsplan

- GCC- und Clang-Kompilierung auf dem exakten Head von Draft PR #183 wiederholen.
- Betroffene Controls und den ursprünglichen Compiler-Zustand auf dem
  resultierenden Master wiederholen.

## Regression tests / Regressionstests

- `tests/test_apache_rules_set_cleanup.py` und der GCC-/Clang-RulesSet-Harness.

## Legitimate control tests / Legitime Kontrolltests

- Frisches materialisiertes DSO, HTTP/1.1-phase-2-403 und SIGUSR1-Readiness-
  Controls.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- None / Keine

## Residual risk / Restrisiko

Der Zustand bleibt offen; der aktuelle Benutzer hat kein Risiko akzeptiert.

## Current task update / Aktueller Task-Stand

Der aktuellen Umgebung fehlen ein nutzbares Apache-APXS-Tool und
Apache-Development-Header. Das exakte Strukturfeld und die
Initialisierungssemantik bei `msc_config.c:110` können daher nicht sicher
erneut validiert werden; kein Initializer, keine Warning-Policy und kein
Apache-Source wurden geändert.

- Feasibility: `blocked_environment`
- Next action: ein reproduzierbares Apache/APXS-Target für reale GCC-/Clang-
  C17-, betroffene Control- und erforderliche Sanitizer-Evidence verwenden.
- Evidence: Run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/039-phase-b-blocker-source-preflight.log`, SHA-256
  `bd04a04698986fd23669aef44c81eff94d1e7c1da2df367858c72257e1d17329`, Exit `0`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: phase_b_preflight_blocked — Apache-C17-Environment-Prerequisites fehlen; kein spekulativer Initializer-Patch wurde erstellt.
- `2026-07-17T14:06:23Z`: phase_b_evidence_synchronized — Das aufbewahrte aktive Source-Preflight-Log wurde in die kanonische Evidence aufgenommen; `blocked_environment` bleibt unverändert.
