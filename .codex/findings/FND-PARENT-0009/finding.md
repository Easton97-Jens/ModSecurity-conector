# FND-PARENT-0009 — Apache binary hardening profile has stale RUNPATH and incomplete full-RELRO proof

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0009` |
| Title / Titel | `Apache binary hardening profile has stale RUNPATH and incomplete full-RELRO proof` |
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

Task-built HTTPD retained a temporary-build RUNPATH, while the module and libmodsecurity lacked observed BIND_NOW; the report does not validate reachable impact.

## Observed behavior / Beobachtetes Verhalten

Task-built HTTPD retained a temporary-build RUNPATH, while the module and libmodsecurity lacked observed BIND_NOW; the report does not validate reachable impact.

## Expected behavior / Erwartetes Verhalten

Current evidence must be rerun against a known revision before this finding can advance beyond triaged.

## Impact / Auswirkung

Release and assurance claims remain bounded by the recorded evidence.

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

The retained evidence identifies the condition but does not establish a product-code root cause.

## Proposed remediation / Vorgeschlagene Remediation

Establish the intended linker-hardening baseline, assess runtime reachability, and avoid promoting this candidate to a vulnerability without evidence.

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

The condition remains open; no risk has been accepted by the current user.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
