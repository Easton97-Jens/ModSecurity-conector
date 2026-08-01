# FND-CROSS-0002 — Historische GitHub-JSON-Receipts sind kein parsebares kanonisches JSON

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-CROSS-0002` |
| Title / Titel | `Historische GitHub-JSON-Receipts sind kein parsebares kanonisches JSON` |
| Category / Kategorie | `evidence_gap` |
| Repository / Repository | `parent_and_framework` |
| Ownership / Ownership | `cross_repository` |
| Priority / Priorität | `P0` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `validated` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `false` |

## Summary / Zusammenfassung

Frühere JSON-suffigierte GitHub-Summary-Receipts enthielten ein literales trailing \\n; ein separates reconciled JSON snapshot war erforderlich.

## Observed behavior / Beobachtetes Verhalten

Frühere JSON-suffigierte GitHub-Summary-Receipts enthielten ein literales trailing \\n; ein separates reconciled JSON snapshot war erforderlich.

## Expected behavior / Erwartetes Verhalten

Die aktuelle Evidence muss gegen eine bekannte Revision erneut ausgeführt werden, bevor dieses Finding über validated hinaus fortschreiten kann.

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

- `sed -n '204,230p;311,329p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:210-212,311-329`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '204,230p;311,329p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.

## Proposed remediation / Vorgeschlagene Remediation

Den Artifact-Writer so korrigieren, dass er parsebares kanonisches JSON erzeugt, und das Raw-Original getrennt bewahren.

## Acceptance criteria / Akzeptanzkriterien

- A newly produced GitHub receipt parses as canonical JSON without reconciliation.
- The raw receipt and its reconciled derivative are traceable by SHA-256.

## Validation plan / Validierungsplan

- Run the GitHub evidence writer in a safe read-only fixture.
- Parse its emitted JSON with jq and retain the exact output.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-CROSS-0001`

## Residual risk / Restrisiko

Der Zustand bleibt offen; der aktuelle Benutzer hat kein Risiko akzeptiert.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
