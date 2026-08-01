# FND-FRAMEWORK-0002 — Framework-ShellCheck-Diagnosen erfordern eine abgegrenzte Triage

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0002` |
| Title / Titel | `Framework-ShellCheck-Diagnosen erfordern eine abgegrenzte Triage` |
| Category / Kategorie | `maintainability` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priority / Priorität | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `closed` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `false` |

## Summary / Zusammenfassung

Die Bestandsaufnahme hielt 261 Framework-ShellCheck-Findings fest, einschließlich eines Shell-Declaration-Errors in ci/lib/mrts-common.sh.

## Observed behavior / Beobachtetes Verhalten

Die Bestandsaufnahme hielt 261 Framework-ShellCheck-Findings fest, einschließlich eines Shell-Declaration-Errors in ci/lib/mrts-common.sh.

## Expected behavior / Erwartetes Verhalten

Die aktuelle Evidence muss gegen eine bekannte Revision erneut ausgeführt werden, bevor dieses Finding über triaged hinaus fortschreiten kann.

## Impact / Auswirkung

Release- und Assurance-Aussagen bleiben durch die dokumentierte Evidence begrenzt.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- `ci/lib/mrts-common.sh`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '83,86p;217,219p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:83-86,217-219`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '83,86p;217,219p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.

## Proposed remediation / Vorgeschlagene Remediation

Diagnosen nach Severity und erlaubtem Scope triagieren; nur eng begründete Exclusions korrigieren oder dokumentieren.

## Acceptance criteria / Akzeptanzkriterien

- Each retained diagnostic has an owner and disposition.
- The scoped Framework ShellCheck run reports the agreed baseline.

## Validation plan / Validierungsplan

- Run Framework ShellCheck excluding original MRTS.
- Run a legitimate Framework shell control after behavior-affecting fixes.

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

Die ursprüngliche abgegrenzte ShellCheck-Bedingung reproduziert auf dem resultierenden Framework-Master nicht mehr. Spätere Änderungen benötigen ihre eigene abgegrenzte Lint-Validierung.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-26T16:13:56Z`: `remediation_fixed` und `resulting_master_verified_and_closed` — Framework-PR #50 korrigierte die abgegrenzte Shell-Deklaration. Exakter Framework-Master `de705a5efb872f95f010346fe2e6143c88876ad4` bestand direkte `shellcheck -s sh ci/lib/mrts-common.sh` und Master-Lint. Receipt: `.codex/runs/20260726T160903Z-framework-pr50-pr51-master-verification/finding-closure-evidence.md` (SHA-256 `519b89ef349a2d1a66b8cf78a5f0056f2df1909df2f386e5e67b7742bf277a2d`).
