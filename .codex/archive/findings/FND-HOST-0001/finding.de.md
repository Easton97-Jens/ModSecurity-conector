# FND-HOST-0001 — Manifest-Cleanup erforderte Schutzvorkehrungen für Spezialdateien und fremde Prozesse

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-HOST-0001` |
| Title / Titel | `Manifest-Cleanup erforderte Schutzvorkehrungen für Spezialdateien und fremde Prozesse` |
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

Das Native-Runtime-Manifest ist partial, weil Cleanup zwei symlinked Temporary-Pfade korrekt verweigerte; manuelle Löschung ist nicht autorisiert.

## Observed behavior / Beobachtetes Verhalten

Das Native-Runtime-Manifest ist partial, weil Cleanup zwei symlinked Temporary-Pfade korrekt verweigerte; manuelle Löschung ist nicht autorisiert.

## Expected behavior / Erwartetes Verhalten

Die aktuelle Evidence muss gegen eine bekannte Revision erneut ausgeführt werden, bevor dieses Finding über blocked hinaus fortschreiten kann.

## Impact / Auswirkung

Release- und Assurance-Aussagen bleiben durch die dokumentierte Evidence begrenzt.

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

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.

## Proposed remediation / Vorgeschlagene Remediation

Eine sichere, owner-autorisierte Retention- oder Cleanup-Prozedur für symlinked Task-Pfade definieren, ohne Links zu folgen.

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

Der Zustand bleibt offen; der aktuelle Benutzer hat kein Risiko akzeptiert.

## Current task update / Aktueller Task-Stand

Der Parent-only-Helper lehnt jetzt Spezialdateien, unsichere Mounts, Symlinks,
Ownership-/Identity-Änderungen, fehlende oder geänderte retained Evidence und
fremde Prozessreferenzen ab. Er prüft alle Candidate-Roots unmittelbar vor
jeder konkreten Löschung erneut. Die fokussierte Suite bestand 49 Tests,
einschließlich einer nach der ersten Löschung injizierten fremden
Prozessreferenz; kein externer Runtime-Pfad wurde gelöscht.

- Feasibility: `feasible_now`
- Security-Ergebnis: validierte Path-, Symlink-, Spezialdatei-,
  Retained-Evidence- und Per-Operation-Process-Protections.
- Strict-Same-UID-Disposition: `partial`; `FND-PARENT-0014` verfolgt getrennt
  die nicht bewiesene finale Leaf-Validierungs-zu-Entfernungs-Grenze. Die
  abgedeckten Spezialdatei-, Evidence- und Process-Controls dieses Records
  bleiben `verified`.
- Evidence: Run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/043-storage-budget-security-regression-final.log`, SHA-256
  `0b1322f17bb7c1fe5ed71f2b9f94d7eca8c4a01189982289798629a12f6e22ac`,
  Exit `0`.
- Final finding status: `verified`.

## Aktuelles nutzergerichtetes Archiv / Current user-directed archive

Der aktuelle Nutzer ordnete das verlustfreie Archiv dieses nicht blockierenden
verified Findings an. Sein Lifecycle bleibt `verified`; dies ist weder ein
neuer Abschluss noch eine Release-Freigabe oder Lockerung der Cleanup-Controls.
Vor einer Nutzung als aktuelle Release-Evidence das vollständige Tripel
wiederherstellen und seine bestehenden Akzeptanzkriterien erneut ausführen.

Archiventscheidungs-Evidence: Run
`20260726T180544Z-fnd-host-archive-20260726-8b20e52d`, Artifact
`evidence/fnd-host-user-directed-archive-scope-disposition.md`, SHA-256
`50f77adb2bfbe8dbea9341bb4012ed67acaa4bf43a540ef3268f7ef2121c666b`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: phase_b_remediation_verified — Parent-Manifest-Cleanup-Hardening und alle 49 fokussierten Controls bestanden.
- `2026-07-17T14:06:23Z`: phase_b_evidence_synchronized — Das aufbewahrte aktive Cleanup-Regressionslog wurde in die kanonische Evidence aufgenommen; die Disposition `verified` bleibt unverändert.
- `2026-07-17T14:36:22Z`: strict_same_uid_boundary_separated — bestehende
  verified Spezialdatei-/Process-/Evidence-Remediation bleibt im Scope;
  unabhängiges finales Review fügte `FND-PARENT-0014` für die getrennte finale
  Leaf-Validierungs-zu-Entfernungs-Grenze hinzu.
