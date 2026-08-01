# FND-FRAMEWORK-0009 — NGINX HTTP/2 route lacks protocol-correlated case execution

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0009` |
| Title / Titel | `NGINX HTTP/2 route lacks protocol-correlated case execution` |
| Category / Kategorie | `protocol_gap` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `validated` |
| Status | `blocked` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `false` |

## Summary / Zusammenfassung

A separate NGINX H1/H2 TLS-ALPN route exists, but no protocol-correlated case execution is wired; H1 results cannot promote it.

## Observed behavior / Beobachtetes Verhalten

A separate NGINX H1/H2 TLS-ALPN route exists, but no protocol-correlated case execution is wired; H1 results cannot promote it.

## Expected behavior / Erwartetes Verhalten

Current evidence must be rerun against a known revision before this finding can advance beyond blocked.

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

- `sed -n '561,570p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:561-570`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '561,570p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

The retained evidence identifies the condition but does not establish a product-code root cause.

## Proposed remediation / Vorgeschlagene Remediation

Wire an isolated H2 case runner with protocol correlation and allow/block controls.

## Acceptance criteria / Akzeptanzkriterien

- NGINX H2 has a retained protocol-correlated allow and block result.
- H1 evidence is not substituted for H2 evidence.

## Validation plan / Validierungsplan

- Run the H2 TLS-ALPN case with protocol diagnostics.
- Run an H1 control separately to demonstrate non-substitution.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-HOST-0004`
- `FND-CROSS-0004`

## Residual risk / Restrisiko

The condition remains open; no risk has been accepted by the current user.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
