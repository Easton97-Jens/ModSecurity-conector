# FND-PARENT-0006 — NGINX-Response-Handling kann einen Over-Limit-Suffix aus der Inspektion auslassen

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0006` |
| Title / Titel | `NGINX-Response-Handling kann einen Over-Limit-Suffix aus der Inspektion auslassen` |
| Category / Kategorie | `security_validated` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P3` |
| Severity / Severity | `low` |
| Confidence / Confidence | `validated` |
| Status | `validated` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

Die statische Validierung fand einen bedingten Over-Limit-Response-Pfad, dessen Suffix uninspected bleiben kann.

## Observed behavior / Beobachtetes Verhalten

Die statische Validierung fand einen bedingten Over-Limit-Response-Pfad, dessen Suffix uninspected bleiben kann.

## Expected behavior / Erwartetes Verhalten

Die aktuelle Evidence muss gegen eine bekannte Revision erneut ausgeführt werden, bevor dieses Finding über validated hinaus fortschreiten kann.

## Impact / Auswirkung

Release- und Assurance-Aussagen bleiben durch die dokumentierte Evidence begrenzt.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- `P-DISC-04-08`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '225,227p;241,244p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:225-227,241-244`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '225,227p;241,244p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.

## Proposed remediation / Vorgeschlagene Remediation

Eine explizite Truncation-Policy definieren und Tail-only-Rule-Regressionen sowie Controls ergänzen.

## Acceptance criteria / Akzeptanzkriterien

- The over-limit policy is explicit and tested for prefix and suffix behavior.
- A legitimate within-limit response remains fully inspected.

## Validation plan / Validierungsplan

- Run an over-limit tail-only regression.
- Run within-limit allow/block controls with the same NGINX profile.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- None / Keine

## Residual risk / Restrisiko

Der Zustand bleibt offen; der aktuelle Benutzer hat kein Risiko akzeptiert.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
