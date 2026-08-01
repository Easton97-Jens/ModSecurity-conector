# FND-PARENT-0024 — Verified-report workflow accepts governance-only validation without the strict runtime-evidence gate

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | FND-PARENT-0024 |
| Title / Titel | Verified-report workflow accepts governance-only validation without the strict runtime-evidence gate |
| Category / Kategorie | security_validated |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priority / Priorität | P1 |
| Severity / Schweregrad | high |
| Confidence / Konfidenz | reproduced |
| Status | fixed |
| Feasibility status / Machbarkeitsstatus | feasible_now |
| Release blocker / Release-Blocker | true |
| Security relevance / Security-Relevanz | true |

## Summary / Zusammenfassung

The verified-report workflow invoked only a governance-only report-layout
target. It could therefore succeed while the strict runtime-evidence gate
failed, allowing governance to be confused with verified runtime evidence.

## Observed behavior / Beobachtetes Verhalten

At Parent revision `c8ca0d92b630c18232b881855c4f5d1482568ea6`,
`.github/workflows/verified-report-governance.yml:41-44` invoked
`make report-governance`. `Makefile:388-390` delegates that target to
`check-generated-report-layout.py --governance-only`; it does not invoke the
strict `verified-report-evidence-gate` at `Makefile:392-393`. The governance
target succeeded while the strict checker rejected stale or missing runtime
evidence inputs.

## Expected behavior / Erwartetes Verhalten

A workflow that represents verified report evidence must execute the existing
strict runtime-evidence gate after governance. Governance-only validation may
remain available, but it cannot mint a runtime-evidence claim.

## Impact / Auswirkung

A stale, incomplete, or absent runtime-manifest set could be obscured by a
successful governance-only result, undermining release evidence and report
integrity.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.github/workflows/verified-report-governance.yml`
- `Makefile`
- `ci/checks/documentation/check-generated-report-layout.py`

### Symbols / Symbole

- `report-governance`
- `verified-report-evidence-gate`
- `check_generated_report_layout`

### Provenance / Herkunft

- Source commit: `dd6e0455c4838949ce86cff81ce89dccd4e524f8`
- Flow: workflow → `make report-governance` → `--governance-only` checker;
  strict gate existed but was unwired.

## Preconditions / Voraussetzungen

- The workflow is run against reports with a valid governance layout.
- Strict runtime evidence is stale, incomplete, or rejected for another
  evidence-integrity reason.

## Reproduction / Reproduktion

1. Run `make report-governance` with the documented external task roots and
   observe success.
2. Run the strict report-evidence checker against the same checkout and observe
   its rejection of stale or missing runtime evidence.
3. Before the remediation, run the focused workflow-contract test requiring
   `make verified-report-evidence-gate` and observe failure.

## Evidence / Evidence

- Run ID: `20260718T075200Z-parent-evidence-integrity-ade378cf`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/CAND-PARENT-001-governance-gate/validation_report.md`
  - Type: `codex_security_validation_report`; SHA-256:
    `b8f6e7b7ba71fccef38a2119938491748475498b62560ceb7b883b303eaebfba`
  - Command: `rtk make report-governance`; the strict checker command and
    outcome are retained in the validation report.
  - Working directory: `/root/git/ModSecurity-conector`; observed
    `2026-07-18T09:22:02Z`; retention: `retained_task_evidence`.

## Root-cause analysis / Grundursachenanalyse

The workflow wired a governance-only target but omitted the existing strict
runtime-evidence target. These targets enforce different trust boundaries.

## Proposed remediation / Vorgeschlagene Remediation

Add the existing strict target to the verified workflow, retain governance as a
companion check, and cover order and both target names with a focused test. Do
not regenerate reports or weaken the strict checker.

## Acceptance criteria / Akzeptanzkriterien

- The workflow invokes `make verified-report-evidence-gate` after
  `make report-governance`.
- A report without accepted runtime manifests cannot produce a successful
  verified-evidence workflow result.
- A complete, checksum-consistent runtime-evidence run remains eligible for
  verification.
- No report is hand-edited to make the strict gate pass.

## Validation plan / Validierungsplan

- Retain the pre-fix workflow-contract failure and rerun the same test after
  the source change.
- Run workflow/YAML validation when available.
- Keep separate results for report governance and the strict evidence gate.
- Obtain PR CI, CodeQL, SonarQube Cloud, and exact-head evidence before status
  can advance to `verified`.

## Regression tests / Regressionstests

- `tests/test_ci_security_workflows.py`
- Focused strict-gate tests for absent runtime manifests and inconsistent
  checksums.

## Legitimate control tests / Legitime Kontrolltests

- A complete current run with consistent manifests and checksums passes the
  strict gate.
- Governance-only layout checks remain available but do not represent runtime
  verification.

## Dependencies / Abhängigkeiten

- `FND-CROSS-0001` must be reconciled before the current stale repository can
  become release-verified.

## Blockers / Blocker

- FND-CROSS-0001 remains unresolved. PR 55 correctly fails the newly wired
  strict runtime-evidence gate on stale critical inputs, so it is not a
  verified PR.

## Related findings / Verwandte Findings

- `FND-CROSS-0001`
- `FND-CROSS-0005`

## Residual risk / Restrisiko

PR 55 head 42b31f1c84c0c915a5cb65119714613fbf3e0c40 contains the strict
gate and passed CodeQL and SonarCloud. Its expected report-governance failure
proves that FND-CROSS-0001 is unresolved. This finding is fixed, not verified
or closed, because no green current runtime-evidence run or master rerun exists.
No risk has been accepted.

## Remediation update / Remediation-Update

- Draft PR 55 wires make verified-report-evidence-gate after
  make report-governance.
- The focused workflow test passed (6 tests), YAML parse and diff check passed,
  and focused security review found no bypass.
- Delivery evidence SHA-256:
  70aa1c1c9048027f02da2bad4f097165d267e70befeb965eec735b512dc1c366.
- No merge occurred.

## History / Historie

- `2026-07-18T09:22:02Z`: `validated_and_root_cause_remediation_started` —
  governance-only success and strict runtime-evidence rejection were
  reproduced; the isolated Parent workflow remediation started after a pre-fix
  workflow-contract failure.
- 2026-07-18T11:13:55Z: fixed_strict_gate_wired_cross_evidence_blocked —
  PR 55 wired the strict gate and passed focused review, but its expected CI
  rejection preserves FND-CROSS-0001 as a release blocker.
