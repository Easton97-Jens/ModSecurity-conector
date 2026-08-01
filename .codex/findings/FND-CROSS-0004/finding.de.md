# FND-CROSS-0004 — Ausgewählte CRS-Profilrouten bleiben für mehrere Connectoren nicht verfügbar

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-CROSS-0004` |
| Title / Titel | `Ausgewählte CRS-Profilrouten bleiben für mehrere Connectoren nicht verfügbar` |
| Category / Kategorie | `crs_gap` |
| Repository / Repository | `parent_and_framework` |
| Ownership / Ownership | `cross_repository` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `validated` |
| Status | `blocked` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `false` |

## Summary / Zusammenfassung

Aktuelle Profilevidence hält blockierte CRS-Routen für HAProxy, Envoy, Traefik und lighttpd fest.

## Observed behavior / Beobachtetes Verhalten

Aktuelle Profilevidence hält blockierte CRS-Routen für HAProxy, Envoy, Traefik und lighttpd fest.

## Expected behavior / Erwartetes Verhalten

Die aktuelle Evidence muss gegen eine bekannte Revision erneut ausgeführt werden, bevor dieses Finding über blocked hinaus fortschreiten kann.

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

- `sed -n '520,549p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:520-549`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '520,549p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.

## Proposed remediation / Vorgeschlagene Remediation

Connector-spezifische, isolierte CRS-Profilrunner bereitstellen, ohne MRTS- oder Runtime-Sicherheitsgrenzen zu schwächen.

## Acceptance criteria / Akzeptanzkriterien

- Each listed connector/profile has a retained allow and block control or an evidence-backed unsupported disposition.
- No original MRTS checkout is modified during profile execution.

## Validation plan / Validierungsplan

- Run the required no-CRS and with-CRS profile cases in task-owned paths.
- Retain result records, process manifests, and control HTTP statuses.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-MRTS-0001`
- `FND-FRAMEWORK-0008`
- `FND-HOST-0003`

## Residual risk / Restrisiko

Der Zustand bleibt offen; der aktuelle Benutzer hat kein Risiko akzeptiert.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
