# FND-CROSS-0006 — Framework authoritative Phase-4 checker does not bind promoted events to selected workload identity

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | FND-CROSS-0006 |
| Title / Titel | Framework authoritative Phase-4 checker does not bind promoted events to selected workload identity |
| Category / Kategorie | security_validated |
| Repository / Repository | parent_and_framework |
| Ownership / Ownership | framework |
| Priority / Priorität | P1 |
| Severity / Schweregrad | high |
| Confidence / Konfidenz | verified |
| Status | verified |
| Feasibility status / Machbarkeitsstatus | already_fixed |
| Release blocker / Release-Blocker | false |
| Security relevance / Security-Relevanz | true |

## Summary / Zusammenfassung

Framework PR #34 binds the authoritative strict Phase-4 promotion to selected
result, manifest, PASS-record, and event workload identity. The original
foreign or missing identity reproducer now fails closed on Framework master.

## Observed behavior / Beobachtetes Verhalten

At Framework revision cdc91a398d6c156eaff927d742b23018a3817fb6, the strict
checker accepts a phase-4 rule-1100301 event based on phase, rule, and
first-byte metadata without selected run, connector, integration-mode, or
transaction identity. Its positive fixture has no run_id and uses
integration_mode=unit-test-host-model.

## Expected behavior / Erwartetes Verhalten

Every authoritative promoted event must match its selected canonical result and
manifest by connector, run ID, selected native host/profile or integration
mode, transaction, rule, and phase. Missing or mismatched fields fail closed.

## Impact / Auswirkung

A copied or pre-positioned event can remain acceptable to the Framework
component of a strict gate even when it is not evidence of the selected
workload. Parent consumer wiring does not repair this Framework boundary.

## Affected files and symbols / Betroffene Dateien und Symbole

- modules/ModSecurity-test-Framework/ci/checks/evidence/check_full_lifecycle_evidence.py
- modules/ModSecurity-test-Framework/tests/no_crs/test_no_crs_baseline.py
- Makefile
- _matching_first_byte_event
- _strict_first_byte_errors
- first_byte_errors
- no_full_response_buffering_errors
- promotion_errors
- RUN_STRICT_FULL_LIFECYCLE_EVIDENCE_CHECK
- Framework source commit: 428dfb2741785adabad7a6280882ea5251e00324

## Preconditions / Voraussetzungen

- The Framework checker is called as an authoritative strict Phase-4 gate.
- A syntactically valid event contains expected rule and causal fields but a
  foreign or absent workload identity.

## Reproduction / Reproduktion

1. Inspect the retained security review and the Framework checker at the
   recorded Framework revision.
2. Run Framework foreign-run, connector, profile/integration, transaction, and
   missing-identity fixtures before a Framework fix.
3. Verify the identity-consistent selected native-host control after the fix.

## Evidence / Evidence

- Run ID: 20260718T075200Z-parent-evidence-integrity-ade378cf
  - Focused security review:
    /var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/06_delivery/security_diff_review.md
  - Type: focused_security_diff_review; SHA-256:
    3d5014e36faebffd46bcd83ed7ee59f8582d1ea9ec6e1b3dfe16e98444c6836e
  - Separate Framework task request:
    /var/tmp/codex/ModSecurity-conector/runs/20260718T075200Z-parent-evidence-integrity-ade378cf/evidence/codex-security-scan-c8ca0d9-20260718T075200Z/artifacts/05_findings/CAND-CROSS-007-framework-phase4-authoritative-gate/framework_task_request.md
  - Type: framework_task_request; SHA-256:
    ea1ff30c2a35514350b143f3b11b2befce60078886cdc468099d587ca11a63ef
- Run ID: 20260720T042405Z-framework-pr-34-master-integration-31a1528d
  - Post-merge receipt:
    /var/tmp/codex/ModSecurity-conector/runs/20260720T042405Z-framework-pr-34-master-integration-31a1528d/evidence/master-postmerge-verification.md
  - Type: post_merge_framework_security_remediation_verification; SHA-256:
    7471054c232a5e2ad26c3327894535ff9d2245e3ec0f37ec60e077a57caea19a
  - Exact PR #34 head `4fc22651ab2da652cbcaa7026258506d79b9af9c` was merged
    normally as Framework master
    `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f`. The PR checks and its
    SonarQube Cloud Quality Gate passed, and the four focused Phase-4
    foreign/missing identity plus legitimate-control tests passed again on
    resulting master.

## Root-cause analysis / Grundursachenanalyse

The Framework predicate does not receive or derive selected result identity,
and its positive test uses a unit-test-host-model event without a run ID.

## Proposed remediation / Vorgeschlagene Remediation

Completed by Framework PR #34: derive selected identity from result and
manifest, require matching live PASS-record identity and supplied transaction
identity per promoted claim, then require the event to match before evaluating
first-byte fields. The PR was normally merged without Parent or MRTS changes.

## Acceptance criteria / Akzeptanzkriterien

- Foreign/missing run, connector, profile/integration-mode, and transaction
  identity fail in the Framework authoritative checker.
- Result, event, and manifest identity are all bound without filename/PASS-only
  logic.
- A selected native-host control passes.
- Framework runtime, review, CodeQL, SonarQube Cloud, and exact-head evidence
  are retained.

## Validation plan / Validierungsplan

- Completed: exact PR #34 head passed focused/full Framework validation,
  CodeQL, GitHub checks, review inspection, and SonarQube Cloud PR Quality
  Gate.
- Completed: resulting Framework master
  `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` contains the reviewed head and
  reran the foreign/missing identity controls and legitimate control
  successfully.
- The independent default-branch SonarQube Cloud backlog remains
  `FND-SONAR-0002`; it is not evidence that this finding remains reproducible.

## Regression tests / Regressionstests

- Framework full-lifecycle evidence checker identity fixtures.
- Framework No-CRS baseline native-host control.

## Legitimate control tests / Legitime Kontrolltests

- Selected event, result, manifest, connector, run, integration mode, and
  transaction agree.
- Native-host evidence cannot be replaced by unit-test-host-model metadata.

## Dependencies / Abhängigkeiten

- FND-PARENT-0027

## Blockers / Blocker

None for FND-CROSS-0006. The separate Framework master SonarQube Cloud
backlog remains tracked as FND-SONAR-0002.

## Related findings / Verwandte Findings

- FND-PARENT-0027
- FND-CROSS-0001
- FND-CROSS-0005
- FND-SONAR-0002

## Residual risk / Restrisiko

No observed FND-CROSS-0006 bypass remains on Framework master. The failed
default-branch SonarQube Cloud gate is the independent FND-SONAR-0002
multi-file backlog; it is neither attributed to this remediation nor silently
risk-accepted for PR #34.

## History / Historie

- 2026-07-18T10:47:59Z: validated_framework_authoritative_gate_boundary —
  independent review identified the unbound Framework authoritative predicate;
  a Parent consumer wiring remediation and separate Framework task request
  were created.
- 2026-07-20T04:52:04Z: verified_after_framework_pr_34_master_merge —
  Framework PR #34 head `4fc22651ab2da652cbcaa7026258506d79b9af9c` merged
  normally as master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f`. Exact PR
  checks and SonarQube Cloud passed; the four focused foreign/missing identity
  and legitimate-control tests reran successfully on master. The separate
  master-only FND-SONAR-0002 gate failure remains unwaived for this PR and is
  not attributed to this finding.
