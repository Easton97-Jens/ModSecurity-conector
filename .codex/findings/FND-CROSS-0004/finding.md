# FND-CROSS-0004 — Selected CRS profile routes remain unavailable for multiple connectors

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-CROSS-0004` |
| Title / Titel | `Selected CRS profile routes remain unavailable for multiple connectors` |
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

Current profile evidence retains blocked CRS routes for HAProxy, Envoy, Traefik, and lighttpd.

## Observed behavior / Beobachtetes Verhalten

Current profile evidence retains blocked CRS routes for HAProxy, Envoy, Traefik, and lighttpd.

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

- `sed -n '520,549p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:520-549`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '520,549p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

The retained evidence identifies the condition but does not establish a product-code root cause.

## Proposed remediation / Vorgeschlagene Remediation

Provide connector-specific, isolated CRS profile runners without weakening MRTS or runtime safety boundaries.

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

The condition remains open; no risk has been accepted by the current user.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
