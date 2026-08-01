# FND-HOST-0003 — NGINX non-root worker isolation cannot be proven in the current sandbox

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-HOST-0003` |
| Title / Titel | `NGINX non-root worker isolation cannot be proven in the current sandbox` |
| Category / Kategorie | `lifecycle_defect` |
| Repository / Repository | `host_environment` |
| Ownership / Ownership | `host_environment` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `reproduced` |
| Status | `blocked` |
| Feasibility status / Machbarkeitsstatus | `blocked_missing_evidence` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

The sandbox denied runuser group setup; the renderer lacks a user directive and no post-start worker PID, effective UID, or capability set was retained.

## Observed behavior / Beobachtetes Verhalten

The sandbox denied runuser group setup; the renderer lacks a user directive and no post-start worker PID, effective UID, or capability set was retained.

## Expected behavior / Erwartetes Verhalten

Current evidence must be rerun against a known revision before this finding can advance beyond blocked.

## Impact / Auswirkung

Release and assurance claims remain bounded by the recorded evidence.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- `runuser cannot set groups`
- `worker PID/effective UID/capability set absent`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '528,533p;580,594p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:528-533,580-594`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '528,533p;580,594p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

The retained evidence identifies the condition but does not establish a product-code root cause.

## Proposed remediation / Vorgeschlagene Remediation

Use a separately authorized harness/configuration that can prove non-root worker ownership, readability, and capabilities without unsafe bypass.

## Acceptance criteria / Akzeptanzkriterien

- A non-root NGINX worker is evidenced with PID, effective UID, and capability facts.
- Root control runtime is not promoted as non-root isolation proof.

## Validation plan / Validierungsplan

- Run the authorized non-root NGINX profile.
- Run the root control separately and retain both distinct results.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- Explicit current-user authorization for an isolated NGINX runtime that can
  retain worker identity and capability evidence.

## Blockers / Blocker

- No `nginx` executable is available on the current host, and the current task
  does not authorize a service start, account change, or runtime provisioning.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0009`
- `FND-CROSS-0004`

## Residual risk / Restrisiko

The condition remains open; no risk has been accepted by the current user.

## Current task update / Aktueller Task-Stand

The current source preflight found an access-only `runuser` probe, but no
rendered NGINX `user` directive or current worker PID/effective UID/GID/
capability evidence. No user, namespace, file permission, NGINX source, or
host configuration was changed.

- Feasibility: `blocked_missing_evidence`
- Next action: retain an authorized non-root runtime with rendered config and
  distinct control-runtime and worker identity facts.
- Evidence: run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/039-phase-b-blocker-source-preflight.log`, SHA-256
  `bd04a04698986fd23669aef44c81eff94d1e7c1da2df367858c72257e1d17329`, exit `0`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: phase_b_preflight_blocked — current evidence remains insufficient; no speculative privilege change was made.
- `2026-07-17T14:06:23Z`: phase_b_evidence_synchronized — Added the retained active-run source-preflight log to canonical evidence; `blocked_missing_evidence` is unchanged.

## Current non-root-worker revalidation — 2026-07-26

The Parent harness still uses `NGINX_WORKER_USER` only as an access-preflight
hint; its generated NGINX template has no `user <name> [group];` directive.
The current host has no `nginx` executable, so no post-start worker PID,
effective UID/GID, or capability facts can be retained. The current evidence is
run `20260726T173136Z-fnd-host-remediation-20260726-7837c9e2`, artifact
`evidence/fnd-host-0002-0003-0004-0006-current-revalidation.md`, SHA-256
`81fdeceb0f34806cd781ee3adf0c8d57d6619d78549fef7e37313e90a4d545bf`.

No privilege, service, product, Framework, or MRTS action occurred. The P1
finding remains `blocked_missing_evidence`; an explicitly authorized isolated
non-root runtime must retain rendered configuration, worker identity/capability
facts, and a distinct root-control observation.
