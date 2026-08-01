# Finding: Vorhersehbare Runtime-Wurzeln und unvalidierte Run-IDs verleihen Dateisystemautorität außerhalb der verifizierten Run-Wurzel

**Sprache:** [English](finding.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-PARENT-0033` |
| Kategorie | `security_validated` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Schwere / Confidence | `P0` / `high` / `reproduced` |
| Status | `fixed` |
| Release-Blocker / sicherheitsrelevant | ja / ja |

## Zusammenfassung, Verhalten und Auswirkung

Runtime-Einstiegspunkte akzeptierten vorhersehbare temporäre Wurzeln,
veränderbare Pfadfragmente und ungeprüfte `VERIFIED_RUN_ID`-Werte, bevor
nachgelagerte Writer Pfade öffneten oder bereinigten. Der erhaltene
Pre-Fix-Nachweis demonstrierte Wurzel-, Parent-/Final-Symlink-, Final-File-,
Traversal-/absolute-ID-, leere/überlange/Unicode-ID-, Foreign-File-, Parallel-
und Validation/Open-Race-Fehler. Ein lokaler Same-User-Angreifer konnte einen
Report-/Evidence-Write oder ein Delete außerhalb der vorgesehenen Runtime-
Wurzel umleiten.

Erwartet ist eine dem aktuellen Benutzer gehörende capability-gebundene
0700-Wurzel mit begrenzten allowlisteten IDs vor Joins, Descriptor-/No-Follow-/
exklusivem I/O, keiner Foreign-File-Adoption und Symlink-Leaf-only-Cleanup.

## Betroffener Umfang und Voraussetzungen

- Dateien/Symbole: `ci/lib/runtime_path_security.py`, Runtime-Lifecycle-
  Bridges, `prepare_runtime_root`, `validate_verified_run_id`,
  `relative_path_below`, und direkte Runtime-Writer einschließlich
  MRTS-native Parent-Staging.
- Ein Angreifer kann eine Komponente unter einem beschreibbaren Ancestor
  erstellen/ersetzen, und ein betroffener Einstiegspunkt konsumiert sie vor
  dem gefixten Boundary.

## Reproduktion und Evidenz

1. Eine Wurzel, Parent- oder finale Symlink auf einen fremden Sentinel anlegen
   und einen Legacy-Runtime-Writer aufrufen.
2. `..`, eine absolute, leere, überlange oder Unicode-Separator-Run-ID liefern
   oder Datei/Verzeichnis zwischen Validation und Open austauschen.
3. Die erhaltene Exact-Head-Evidenz hat den historischen Pfad
   `.codex/runs/20260718T075146Z-harden-temp-paths-97486abe/evidence/runtime-temp-path-revalidation.md`
   (nicht in diesem Reconciliation-Checkout verteilt),
   SHA-256 `db84a74c2048327ec886d03b33f04885af9b368799f45fc9959111f0b4eb1216`.
   Ihr Command lieferte Exit 0 mit 54 fokussierten Tests auf Commit
   `576c08e9fdb27bc0ec9a6507a02c28413004ac25`.

## Root Cause und Remediation

String-abgeleitete Pfade wurden über Allokation, Run-ID-Propagation, Schreiben,
Lesen und Cleanup als Autorität vertraut. PR A verwendet deskriptorrelative
`lstat`/No-Follow/exklusive Primitive, 0700-capability-gebundene Wurzeln, eine
begrenzte ASCII-Allowlist, Ownership-Records, sichere Shell-/Python-Bridges und
sicheres Cleanup in den abgebildeten Parent-Writern.

## Akzeptanz, Validierung und Kontrollen

- Alle erlaubten Artefakte bleiben unter der kanonischen verifizierten Wurzel
  mit restriktiven Modi; alle Symlink-/Traversal-/Foreign-/Race-Kontrollen
  bewahren den Sentinel.
- `tests/test_verified_runtime_path_hardening.py`,
  `test_runtime_artifact_io_hardening.py`,
  `test_mrts_native_full_path_hardening.py` und
  `test_runtime_env_snapshot_contract.py` decken Regressionen und normale
  Kontrollen ab.
- Exact-Head-`sh -n` und ShellCheck für `run-mrts-native-full.sh` bestanden.

## Abhängigkeiten, Blocker, verwandte Findings und Restrisiko

Keine Remediation-Abhängigkeit bleibt. Framework-/MRTS-End-to-End-Integration
ist `blocked_missing_evidence`, kein Pass oder Risikoakzeptanz. Verwandt sind
`FND-PARENT-0034` und `FND-PARENT-0035`, deren Report- bzw. Library-Regel-
Boundaries getrennt sind. Der Fix ist delivery-pending bis Exact-PR-CI-/Review-
Evidenz vorliegt; kein Merge oder Risk Acceptance ist autorisiert.

## Historie

- `2026-07-18T14:46:42Z`: Pre-Fix-Exploitklassen validiert; Exact-PR-A-Head-
  Kontrollen bestanden; Status auf `fixed` pending verified PR gesetzt.
