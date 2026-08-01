# FND-HOST-0001 — Manifest cleanup required special-file and foreign-process safeguards

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-HOST-0001` |
| Title / Titel | `Manifest cleanup required special-file and foreign-process safeguards` |
| Category / Kategorie | `storage_cleanup` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `verified` |
| Feasibility status / Machbarkeitsstatus | `feasible_now` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

The native runtime manifest is partial because cleanup correctly refused two symlinked temporary paths; no manual deletion is authorized.

## Observed behavior / Beobachtetes Verhalten

The native runtime manifest is partial because cleanup correctly refused two symlinked temporary paths; no manual deletion is authorized.

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

- `jq -c '{run_id,task_slug,goal,start_time_utc,end_time_utc,last_check_status,last_check_utc,final_size_bytes,expected_max_size_bytes,cleanup}' /var/tmp/codex/ModSecurity-conector/runs/20260717T054830Z-native-runtime-evidence-6c0853fe/manifest.json`

## Evidence / Evidence

- Run ID: `20260717T054830Z-native-runtime-evidence-6c0853fe`
  - Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260717T054830Z-native-runtime-evidence-6c0853fe/manifest.json`
  - Type: `external_storage_manifest`; SHA-256: `97bf04a08164e7abc46aa3d419761376b76684d496c34cdfe595bf3ef3ae85a7`
  - Command: `jq -c '{run_id,task_slug,goal,start_time_utc,end_time_utc,last_check_status,last_check_utc,final_size_bytes,expected_max_size_bytes,cleanup}' /var/tmp/codex/ModSecurity-conector/runs/20260717T054830Z-native-runtime-evidence-6c0853fe/manifest.json`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T08:17:36Z`; retention: `retained_external_evidence`
- Run ID: `20260717T054830Z-native-runtime-evidence-6c0853fe`
  - Artifact: `.codex/reports/repository-full-assessment.md:480-489,620-629`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '480,489p;620,629p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T08:17:36Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

The retained evidence identifies the condition but does not establish a product-code root cause.

## Proposed remediation / Vorgeschlagene Remediation

Define a safe, owner-authorized retention or cleanup procedure for symlinked task paths without following links.

## Acceptance criteria / Akzeptanzkriterien

- Each retained symlinked path has an owner, retention decision, and safe disposal procedure.
- No cleanup follows a symlink or removes data outside the task-owned run.

## Validation plan / Validierungsplan

- Inspect object types with no symlink traversal.
- Run the storage helper's safe dry-run/finalization controls only on registered paths.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None / Keine

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-CROSS-0001`

## Residual risk / Restrisiko

The condition remains open; no risk has been accepted by the current user.

## Current task update / Aktueller Task-Stand

The Parent-only helper now rejects special files, unsafe mounts, symlinks,
ownership/identity changes, missing or changed retained evidence, and foreign
process references. It rescans all candidate roots immediately before every
concrete deletion. The focused suite passed 49 tests, including an injected
foreign-process reference after the first deletion; no external runtime path
was deleted.

- Feasibility: `feasible_now`
- Security result: validated path, symlink, special-file, retained-evidence,
  and per-operation process protections.
- Strict same-UID disposition: `partial`; `FND-PARENT-0014` separately tracks
  the unproven final leaf validation-to-removal boundary. This record's covered
  special-file, evidence, and process controls remain `verified`.
- Evidence: run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/043-storage-budget-security-regression-final.log`, SHA-256
  `0b1322f17bb7c1fe5ed71f2b9f94d7eca8c4a01189982289798629a12f6e22ac`,
  exit `0`.
- Final finding status: `verified`.

## Current user-directed archive / Aktuelles nutzergerichtetes Archiv

The current user directed a lossless archive of this non-blocking verified
finding. Its lifecycle remains `verified`; this is not a new closure, release
approval, or weakening of the cleanup controls. Restore the complete triplet
and rerun its existing acceptance criteria before relying on it as current
release evidence.

Archive decision evidence: run
`20260726T180544Z-fnd-host-archive-20260726-8b20e52d`, artifact
`evidence/fnd-host-user-directed-archive-scope-disposition.md`, SHA-256
`50f77adb2bfbe8dbea9341bb4012ed67acaa4bf43a540ef3268f7ef2121c666b`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: phase_b_remediation_verified — Parent manifest cleanup hardening and all 49 focused controls passed.
- `2026-07-17T14:06:23Z`: phase_b_evidence_synchronized — Added the retained active-run cleanup-regression log to canonical evidence; the verified disposition is unchanged.
- `2026-07-17T14:36:22Z`: strict_same_uid_boundary_separated — Existing
  verified special-file/process/evidence remediation remains in scope;
  independent final review added `FND-PARENT-0014` for the distinct final leaf
  validation-to-removal boundary.
