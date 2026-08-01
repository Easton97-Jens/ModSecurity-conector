# FND-PARENT-0009 — Apache-Binary-Hardening-Profil hat stale RUNPATH und unvollständigen Full-RELRO-Nachweis

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0009` |
| Title / Titel | `Apache-Binary-Hardening-Profil hat stale RUNPATH und unvollständigen Full-RELRO-Nachweis` |
| Category / Kategorie | `binary_hardening_gap` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P2` |
| Severity / Severity | `informational` |
| Confidence / Confidence | `candidate` |
| Status | `triaged` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Task-built HTTPD behielt einen temporary-build RUNPATH, während Modul und libmodsecurity kein beobachtetes BIND_NOW hatten; der Bericht validiert keinen erreichbaren Impact.

## Observed behavior / Beobachtetes Verhalten

Task-built HTTPD behielt einen temporary-build RUNPATH, während Modul und libmodsecurity kein beobachtetes BIND_NOW hatten; der Bericht validiert keinen erreichbaren Impact.

## Expected behavior / Erwartetes Verhalten

Die aktuelle Evidence muss gegen eine bekannte Revision erneut ausgeführt werden, bevor dieses Finding über triaged hinaus fortschreiten kann.

## Impact / Auswirkung

Release- und Assurance-Aussagen bleiben durch die dokumentierte Evidence begrenzt.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- None / Keine

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '605,620p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:605-620`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '605,620p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.

## Proposed remediation / Vorgeschlagene Remediation

Die beabsichtigte Linker-Hardening-Baseline festlegen, Runtime-Reachability bewerten und diesen Kandidaten ohne Evidence nicht zur Vulnerability befördern.

## Acceptance criteria / Akzeptanzkriterien

- The intended RUNPATH/RELRO policy is documented and measured on released artifacts.
- Any reachable impact is validated or the candidate has technical counter-evidence.

## Validation plan / Validierungsplan

- Inspect the rebuilt artifacts with available ELF tooling.
- Run a legitimate host startup/control after any linker configuration change.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-PARENT-0008`

## Residual risk / Restrisiko

Der Zustand bleibt offen; der aktuelle Benutzer hat kein Risiko akzeptiert.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
