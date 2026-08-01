# FND-PARENT-0007 — Traefik connector worker admission is unbounded

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0007` |
| Title / Titel | `Traefik connector worker admission is unbounded` |
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

Static validation found conditional resource pressure from unbounded connector-level worker creation under sustained UDS ingress.

## Observed behavior / Beobachtetes Verhalten

Static validation found conditional resource pressure from unbounded connector-level worker creation under sustained UDS ingress.

## Expected behavior / Erwartetes Verhalten

Current evidence must be rerun against a known revision before this finding can advance beyond validated.

## Impact / Auswirkung

Release and assurance claims remain bounded by the recorded evidence.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- `P-DISC-05-02`

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

The retained evidence identifies the condition but does not establish a product-code root cause.

## Proposed remediation / Vorgeschlagene Remediation

Reserve bounded active capacity, reject overload, and retain saturation plus normal-traffic controls.

## Acceptance criteria / Akzeptanzkriterien

- Worker admission has a documented bound and overload behavior.
- Normal UDS traffic remains available below the bound.

## Validation plan / Validierungsplan

- Run a bounded admission saturation test.
- Run normal Traefik UDS traffic as a legitimate control.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0008`

## Residual risk / Restrisiko

The condition remains open; no risk has been accepted by the current user.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
