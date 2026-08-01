# FND-PARENT-0027 — Phase-4 evidence matching omits selected run and workload identity

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | FND-PARENT-0027 |
| Title / Titel | Phase-4 evidence matching omits selected run and workload identity |
| Category / Kategorie | security_validated |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priority / Priorität | P1 |
| Severity / Schweregrad | high |
| Confidence / Konfidenz | confirmed |
| Status | closed (archived) |
| Feasibility status / Machbarkeitsstatus | feasible_now |
| Release blocker / Release-Blocker | false |
| Security relevance / Security-Relevanz | true |

## Summary / Zusammenfassung

The Phase-4 lifecycle checker accepted event records based only on rule ID and
phase. Copied events carrying a foreign run ID, connector, or profile passed
the same first-byte and no-full-buffer checks as a legitimate Apache event.

## Observed behavior / Beobachtetes Verhalten

`ci/checks/evidence/check-full-lifecycle-evidence.py:154-155` uses an event
predicate that does not bind run ID, connector, host profile, integration mode,
or transaction identity. Three temporary foreign-identity variants and one
legitimate control all returned PASS for the first-byte and no-full-buffer
checks.

## Expected behavior / Erwartetes Verhalten

Each promoted Phase-4 event must bind selected run ID, connector, host profile,
integration mode, and transaction identity via the canonical event/result
schema. Missing or mismatched identity fails closed.

## Impact / Auswirkung

Evidence copied from another run, connector, or profile can be promoted as
proof for a selected workload, breaking run identity and integration-mode
integrity.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `ci/checks/evidence/check-full-lifecycle-evidence.py`
- `ci/checks/evidence/check-six-connector-core-completion.py`
- `Makefile`
- `tests/test_full_lifecycle_evidence.py`
- `tests/test_full_lifecycle_gate_wiring.py`

### Symbols / Symbole

- `matching_events`
- `check_first_byte`
- `check_no_full_buffer`
- identity matcher
- `RUN_PARENT_FULL_LIFECYCLE_EVIDENCE_CHECK`
- `RUN_STRICT_FULL_LIFECYCLE_EVIDENCE_CHECK`

### Provenance / Herkunft

- Source commit: `6bfdc66329fc68531b3f358cab25ef91b3d9a2a9`
- Parent remediation commits: `8b7b13b294fe4043fb4002c1cb96ba3de72986f8` and
  `0124b0d685c69129d4aeace8eff75ccc288e7a8e`
- Exact PR #57 head: `5f8949b1d98a98127b933e9f1d626b30e3291b59`
- Resulting Parent master: `fde2e02a1cf2226f8e9106e663e05e9b2941357e`
- Flow: selected result → phase/rule-only event predicate → first-byte or
  no-full-buffer PASS → promoted Phase-4 evidence.

## Preconditions / Voraussetzungen

- A selected evidence directory contains a syntactically valid Phase-4 event
  with the expected rule and phase.
- The event originates from a foreign run, connector, profile, or integration
  mode.

## Reproduction / Reproduktion

1. Build temporary evidence roots containing an Apache selected-run result and
   a foreign-run, foreign-connector, or foreign-profile event.
2. Run `check-full-lifecycle-evidence.py` with `--run-id selected-run` and
   `--connectors apache` for `first-byte` and `no-full-buffer`.
3. Observe PASS for every foreign variant and for the legitimate control.

## Evidence / Evidence

- Run ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/CAND-PARENT-004-phase4-identity/validation_report.md`
  - Type: `codex_security_validation_report`; SHA-256:
    `70d07710bb9cab22be7cc64657e030302905ec99a4cfdfd1702a5ab8b930a645`
  - Command:
    `rtk env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python ci/checks/evidence/check-full-lifecycle-evidence.py --connector-root /root/git/ModSecurity-conector --evidence-root <temporary-root> --run-id selected-run --check <first-byte|no-full-buffer> --connectors apache`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`;
    observed `2026-07-18T09:22:02Z`; retention:
    `retained_task_evidence`.
- Run ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/pr_delivery_status.json`
  - Type: `draft_pr_delivery_status`; SHA-256:
    `70aa1c1c9048027f02da2bad4f097165d267e70befeb965eec735b512dc1c366`
  - Command:
    `rtk gh pr checks 57 --repo Easton97-Jens/ModSecurity-conector`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`;
    observed `2026-07-18T11:13:55Z`; retention:
    `retained_task_evidence`.
- Run ID: `20260720T080314Z-parent-pr55-57-59-framework-update-3443af13`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/evidence/pr57-5f8949b-current-head-verification.md`
  - Type: `parent_pr_current_head_delivery_verification`; SHA-256:
    `cb6ae640643dec166ab77cb364ab61f01d79ce44cfaba99c97477d4d92820178`
  - Command: exact PR #57 head check-runs, CodeQL/code-scanning, SonarCloud,
    review-thread, and scoped-diff inspection.
  - Working directory:
    `/var/tmp/codex/worktrees/parent-evidence-phase4-binding`; exit code `0`;
    observed `2026-07-20T10:41:05Z`; retention `retained_task_evidence`.
- Run ID: `20260720T080314Z-parent-pr55-57-59-framework-update-3443af13`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/evidence/pr57-master-fde2-phase4-identity-verification.md`
  - Type:
    `exact_parent_master_phase4_identity_original_reproduction_and_legitimate_control`;
    SHA-256: `8c638de640cd2fd6b49c1c26ac026ac569aa119642fd51e31dec558667d11f0f`
  - Command: RTK-proxied detached exact-master inspection, diff/gitlink
    comparison, and the focused Parent lifecycle/wiring/six-connector tests.
  - Working directory:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T080314Z-parent-pr55-57-59-framework-update-3443af13/tmp/parent-pr57-master-fde2`;
    exit code `0`; observed `2026-07-20T11:05:00Z`; retention
    `retained_task_evidence`.

## Root-cause analysis / Grundursachenanalyse

The event predicate used only rule ID and phase and was not initially invoked
by the actual Parent first-byte, no-full-buffer, and promotion Make targets.
A stronger identity matcher existed in the six-connector completion checker
but was not reused or wired into promotion.

## Proposed remediation / Vorgeschlagene Remediation

Reuse the canonical identity-matching pattern, require all selected identity
fields before promotion, and wire the Parent first-byte, no-full-buffer, and
promotion targets to their matching Parent checks. Add the named foreign-
identity fixtures, a legitimate control, and a static target-wiring contract.

## Acceptance criteria / Akzeptanzkriterien

- Foreign run-ID, connector, profile, and integration-mode events cannot
  satisfy first-byte or no-full-buffer checks.
- Missing required event identity fails closed.
- A legitimate selected-run event remains accepted.
- Result, event, manifest, and checksum identity are checked consistently,
  without a filename/PASS-only decision.
- The actual Parent first-byte, no-full-buffer, and promotion Make targets
  invoke their matching Parent identity checks.

## Validation plan / Validierungsplan

- Add the named foreign-identity and valid-control fixtures before the
  implementation change.
- Rerun the original copied-event PoCs, an alternate missing-identity case,
  and the valid control after the fix.
- Run focused lifecycle-evidence tests, a static Makefile target-wiring
  contract, and applicable runtime-harness contract tests.

## Regression tests / Regressionstests

- Focused `check-full-lifecycle-evidence` tests for run, connector, profile,
  and integration-mode mismatch.
- Existing six-connector identity matcher control tests.

## Legitimate control tests / Legitime Kontrolltests

- A selected Apache run with an identity-consistent native event passes
  first-byte and no-full-buffer checks.
- A complete manifest chain with matching event/result identity remains
  accepted.

## Dependencies / Abhängigkeiten

- None.

## Blockers / Blocker

`FND-CROSS-0006` is independently verified on Framework master. The separate
`FND-CROSS-0001` runtime-evidence gap remains tracked and is not replaced or
risk-accepted by this Parent-only remediation. Independent Parent finding
`FND-SONAR-0001` blocks aggregate master delivery; it neither reopens this
verified identity repair nor receives a risk acceptance here.

## Related findings / Verwandte Findings

- `FND-CROSS-0001`
- `FND-CROSS-0006`

## Remediation update / Remediation-Update

PR #57 exact head `5f8949b1d98a98127b933e9f1d626b30e3291b59` was squash-merged
as Parent master `fde2e02a1cf2226f8e9106e663e05e9b2941357e`. The exact
resulting master contains only the reviewed eight Parent files and preserves
Framework gitlink `efdbcbd98afeed0f39f8912ce1140aaa5742f507`. In a clean
detached worktree, all 20 focused lifecycle/wiring/six-connector tests passed:
foreign run, connector, profile, integration-mode, transaction, and missing-
identity variants fail closed through both first-byte and no-full-buffer paths,
while the selected Apache legitimate control remains accepted. The finding is
verified, not closed.

## Residual risk / Restrisiko

The exact Parent master reproduces the original and alternate copied/missing
identity cases as fail-closed and preserves the selected Apache legitimate
control. `FND-PARENT-0027` is verified, not closed. `FND-CROSS-0006` is
separately verified and `FND-CROSS-0001` remains a distinct runtime-evidence
limitation. Independent Parent Sonar release blocker `FND-SONAR-0001` prevents
aggregate `master_integration_complete` but does not reopen this verified
Phase-4 identity repair. No risk has been accepted.

## History / Historie

- `2026-07-18T09:22:02Z`: `validated_foreign_identity_promotion` — foreign
  run, connector, and profile event variants passed the selected Apache
  Phase-4 checks alongside the legitimate control.
- `2026-07-18T11:13:55Z`: `fixed_parent_gate_wiring_after_security_review` —
  independent review found the initial identity matcher was not wired into
  actual Parent promotion targets. Follow-up `0124b0d` wired first-byte,
  no-full-buffer, and promotion checks, passed 20 focused tests and 33 PR
  checks, and received a clean re-review. `FND-CROSS-0006` records the separate
  Framework-authoritative boundary.
- `2026-07-20T10:41:05Z`: `fixed_current_pr_57_head_validated` — exact head
  `5f8949b1d98a98127b933e9f1d626b30e3291b59` has current terminal checks,
  CodeQL, SonarCloud, zero open code-scanning alerts, no review thread, and a
  reviewed Parent-only diff. The finding remains fixed pending authorized
  merge and master reproduction.
- `2026-07-20T11:05:00Z`:
  `verified_on_resulting_parent_master_after_original_reproduction` — source
  head `5f8949b...` is merged as exact Parent master `fde2e02...`. A clean
  detached master worktree passed 20 focused lifecycle/wiring/six-connector
  tests: foreign run, connector, profile, integration-mode, transaction, and
  missing-identity variants fail closed on both first-byte and no-full-buffer
  paths, while selected Apache evidence remains accepted. The Framework
  gitlink remains `efdbcbd...`. The independent Parent Sonar failure
  `FND-SONAR-0001` leaves aggregate delivery partial but does not reopen this
  verified finding.

## Closure / Abschluss

The current user authorized closure and archival after `tests.test_full_lifecycle_evidence` and `tests.test_full_lifecycle_gate_wiring` passed on Parent master `6ca7e1536ce7e93da68099db9c586b88852ff13e` as part of the 144-test control suite. `FND-SONAR-0001` remains an independent active Quality-Gate blocker.
