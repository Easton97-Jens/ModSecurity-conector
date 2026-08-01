# FND-MRTS-0001 — MRTS-related assurance remains limited to controlled external-copy evidence

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-MRTS-0001` |
| Title / Titel | `MRTS-related assurance remains limited to controlled external-copy evidence` |
| Category / Kategorie | `mrts_gap` |
| Repository / Repository | `mrts` |
| Ownership / Ownership | `mrts_external_read_only` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `validated` |
| Status | `blocked` |
| Feasibility status / Machbarkeitsstatus | `blocked_missing_evidence` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

The original MRTS checkout stayed read-only; current conclusions rely on task-owned external-copy controls and do not establish unrestricted original-checkout runtime assurance.

## Observed behavior / Beobachtetes Verhalten

The original MRTS checkout stayed read-only; current conclusions rely on task-owned external-copy controls and do not establish unrestricted original-checkout runtime assurance.

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

- `sed -n '496,517p;620,629p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:496-517,620-629`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '496,517p;620,629p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

The retained evidence identifies the condition but does not establish a product-code root cause.

## Proposed remediation / Vorgeschlagene Remediation

Define an authorized read-only assurance protocol that preserves original MRTS integrity and records exact pre/post boundary controls.

## Acceptance criteria / Akzeptanzkriterien

- MRTS-related runtime claims identify external-copy versus original-checkout evidence precisely.
- The original MRTS SHA, status, and Gitlink controls pass before and after authorized work.

## Validation plan / Validierungsplan

- Run only an authorized external-copy harness.
- Retain Parent/Framework/MRTS boundary checks and distinguish assurance limitations from product defects.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-CROSS-0004`
- `FND-FRAMEWORK-0010`

## Residual risk / Restrisiko

The condition remains open; no risk has been accepted by the current user.

## Current task update / Aktueller Task-Stand

Read-only structural inspection found `DetectionOnly` declarations, but no
current runtime evidence proves external overlay ordering or separates the
requested DetectionOnly detection/audit behavior from Blocking Allow/Block
behavior. The original MRTS checkout, its generated output, dependencies, Git
state, and gitlink were not changed.

- Feasibility: `blocked_missing_evidence`
- Next action: a Framework-owned external overlay must retain DetectionOnly
  Allow/detection and Blocking Allow/block controls plus original-MRTS
  integrity evidence.
- Evidence: run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/039-phase-b-blocker-source-preflight.log`, SHA-256
  `bd04a04698986fd23669aef44c81eff94d1e7c1da2df367858c72257e1d17329`, exit `0`.

## Test-only MRTS relevance assessment / MRTS-Relevanzbewertung nur für Tests

The static source trace was recorded at `2026-07-24T04:20:19Z` against
Framework `f98a8739cb13b583f23d646784b144e596b61441` and read-only MRTS
`13aa91291adea12d5c607fdd165d010fcfb1da78`. A final delta refresh at
`2026-07-24T04:28:24Z` found current Framework
`4c9753291d26d92f2d7e51ae425dedb79666fd5e`; its delta from the static
source revision changes no MRTS generation/import/runner path or the
Framework gitlink, which remains
`160000 13aa91291adea12d5c607fdd165d010fcfb1da78`.

- **Classification:** conditionally relevant only when the Framework opt-in
  `with-mrts` path executes. Merely retaining or reading MRTS as a test corpus
  is not evidence of a production MRTS vulnerability or connector runtime
  defect; it only bounds test-evidence provenance and assurance claims.
- **Test-only path:** the Framework invokes the MRTS generator into an
  external build root, imports generated rules/cases into a private Framework
  runtime root, and can reach a local connector smoke runtime only if an
  imported case is active and selected. The normal `test` target does not use
  MRTS; `test-with-mrts` is opt-in.
- **Current limitation:** the static coverage summary records `399` imported
  cases, `0` active/runtime-executable cases, and `399` pending/unclassified
  cases. No evidence therefore supports a claim that this corpus currently
  exercises a live connector runtime.
- **Boundary result:** no command in this task changed Parent, Framework, or
  original MRTS. A recorded out-of-task Framework fast-forward was followed
  by the delta check above; current Framework and MRTS are clean and their
  gitlink still matches. No generator, importer, test, build, or write-capable
  MRTS command was run. The finding remains `blocked` /
  `blocked_missing_evidence` because no fresh authorized external-copy runtime
  evidence was produced.
- **Retained evidence:** run
  `20260724T042019Z-open-pr-triage-mrts-test-only-relevance-9786d0b7`,
  `evidence/mrts-test-only-relevance-assessment.md`, SHA-256
  `f06f7a8fb6bf8aa9ed18916f7dcc964b83f6b94ae74f0fda6683a27ad75ed75f`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: phase_b_preflight_blocked — structural evidence alone did not authorize a profile assertion or any MRTS mutation.
- `2026-07-17T14:06:23Z`: phase_b_evidence_synchronized — Added the retained active-run source-preflight log to canonical evidence; `blocked_missing_evidence` and the MRTS read-only boundary are unchanged.
- `2026-07-24T04:21:50Z`: test_only_relevance_assessed — Classified the finding as conditionally relevant to opt-in MRTS test execution only, not as a demonstrated production exposure. The blocked disposition and original-MRTS read-only boundary are unchanged.
- `2026-07-24T04:28:24Z`: framework_delta_refreshed — A recorded out-of-task Framework fast-forward was checked from `f98a8739cb13b583f23d646784b144e596b61441` to `4c9753291d26d92f2d7e51ae425dedb79666fd5e`; no MRTS generation/import/runner path or gitlink changed, so the test-only classification remains valid.
