# FND-FRAMEWORK-0007 — Apache canonical full-lifecycle finalizer exits 77 after live traffic

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0007` |
| Title / Titel | `Apache canonical full-lifecycle finalizer exits 77 after live traffic` |
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

The Apache retry had live first-byte/H1 traffic but its retained canonical full-lifecycle finalizer returned exit 77; the report classifies it as a harness failure, not a product failure.

## Observed behavior / Beobachtetes Verhalten

The Apache retry had live first-byte/H1 traffic but its retained canonical full-lifecycle finalizer returned exit 77; the report classifies it as a harness failure, not a product failure.

## Expected behavior / Erwartetes Verhalten

Current evidence must be rerun against a known revision before this finding can advance beyond validated.

## Impact / Auswirkung

Release and assurance claims remain bounded by the recorded evidence.

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

The retained evidence identifies the condition but does not establish a product-code root cause.

## Proposed remediation / Vorgeschlagene Remediation

Diagnose and correct the Framework finalizer assertion, then retain a full lifecycle rerun with process/port cleanup controls.

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

The condition remains open; no risk has been accepted by the current user.

## Current task update / Aktueller Task-Stand

Historical evidence retains an Apache full-lifecycle exit `77` after traffic,
but this task has no raw current finalizer artifact or controlled reproduction
to distinguish an assertion, precondition, cleanup, or environment path. No
Framework file was changed.

- Feasibility: `blocked_missing_evidence`
- Next action: reproduce the canonical Framework lifecycle with finalizer,
  process, listener, Allow, Block, shutdown, and cleanup artifacts.
- Evidence: run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/039-phase-b-blocker-source-preflight.log`, SHA-256
  `bd04a04698986fd23669aef44c81eff94d1e7c1da2df367858c72257e1d17329`, exit `0`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: phase_b_preflight_blocked — retained historical validation does not authorize a Framework patch without current raw reproduction.
- `2026-07-17T14:06:23Z`: phase_b_evidence_synchronized — Added the retained active-run source-preflight log to canonical evidence; `blocked_missing_evidence` is unchanged.
