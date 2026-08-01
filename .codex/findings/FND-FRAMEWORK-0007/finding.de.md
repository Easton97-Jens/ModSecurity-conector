# FND-FRAMEWORK-0007 — Apache-kanonischer Full-Lifecycle-Finalizer beendet sich nach Live-Traffic mit 77

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0007` |
| Title / Titel | `Apache-kanonischer Full-Lifecycle-Finalizer beendet sich nach Live-Traffic mit 77` |
| Category / Kategorie | `lifecycle_defect` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `validated` |
| Status | `blocked` |
| Feasibility status / Machbarkeitsstatus | `blocked_missing_evidence` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `false` |

## Summary / Zusammenfassung

Der Apache-Retry hatte Live-First-Byte/H1-Traffic, aber sein zurückgehaltener kanonischer Full-Lifecycle-Finalizer gab Exit 77 zurück; der Bericht klassifiziert dies als Harness-Fehler, nicht als Produktfehler.

## Observed behavior / Beobachtetes Verhalten

Der Apache-Retry hatte Live-First-Byte/H1-Traffic, aber sein zurückgehaltener kanonischer Full-Lifecycle-Finalizer gab Exit 77 zurück; der Bericht klassifiziert dies als Harness-Fehler, nicht als Produktfehler.

## Expected behavior / Erwartetes Verhalten

Die aktuelle Evidence muss gegen eine bekannte Revision erneut ausgeführt werden, bevor dieses Finding über validated hinaus fortschreiten kann.

## Impact / Auswirkung

Release- und Assurance-Aussagen bleiben durch die dokumentierte Evidence begrenzt.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- `exit 77`
- `finalizer symptom assertion_failed`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '399,403p;580,594p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:399-403,580-594`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '399,403p;580,594p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.

## Proposed remediation / Vorgeschlagene Remediation

Die Framework-Finalizer-Assertion diagnostizieren und korrigieren; anschließend einen Full-Lifecycle-Rerun mit Prozess-/Port-Cleanup-Controls aufbewahren.

## Acceptance criteria / Akzeptanzkriterien

- Apache full lifecycle completes without exit 77 after real traffic.
- First-byte, allow, block, process, and port-release controls all pass.

## Validation plan / Validierungsplan

- Rerun the canonical Apache full lifecycle in task-owned storage.
- Verify the same legitimate allow and expected block controls before and after finalization.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-CROSS-0003`

## Residual risk / Restrisiko

Der Zustand bleibt offen; der aktuelle Benutzer hat kein Risiko akzeptiert.

## Current task update / Aktueller Task-Stand

Historische Evidence hält einen Apache-Full-Lifecycle-Exit `77` nach Traffic
fest, aber diese Aufgabe besitzt kein rohes aktuelles Finalizer-Artefakt und
keine kontrollierte Reproduktion, um Assertion-, Precondition-, Cleanup- oder
Environment-Pfad zu unterscheiden. Keine Framework-Datei wurde geändert.

- Feasibility: `blocked_missing_evidence`
- Next action: den kanonischen Framework-Lifecycle mit Finalizer-, Prozess-,
  Listener-, Allow-, Block-, Shutdown- und Cleanup-Artefakten reproduzieren.
- Evidence: Run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/039-phase-b-blocker-source-preflight.log`, SHA-256
  `bd04a04698986fd23669aef44c81eff94d1e7c1da2df367858c72257e1d17329`, Exit `0`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: phase_b_preflight_blocked — retained historical validation autorisiert ohne aktuelle rohe Reproduktion keinen Framework-Patch.
- `2026-07-17T14:06:23Z`: phase_b_evidence_synchronized — Das aufbewahrte aktive Source-Preflight-Log wurde in die kanonische Evidence aufgenommen; `blocked_missing_evidence` bleibt unverändert.
