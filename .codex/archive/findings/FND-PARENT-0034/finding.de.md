# Finding: Temporäre Report-Writer können fremde Dateien über symlinkte Wurzeln oder Report-Leaves überschreiben

**Sprache:** [English](finding.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-PARENT-0034` |
| Kategorie | `security_validated` |
| Repository / Ownership | `parent` / `parent` |
| Priorität / Schwere / Confidence | `P0` / `high` / `reproduced` |
| Status | `fixed` |
| Release-Blocker / sicherheitsrelevant | ja / ja |

## Zusammenfassung, Verhalten und Auswirkung

Vorhersehbare temporäre Report-Wurzeln und pfadbasierte Report-/Index-/Log- /
Cleanup-Writes erlaubten einem vorangelegten Symlink, die Publikation in einen
fremden Pfad umzuleiten. Vor dem Fix ließ ein echter
`TMP_ROOT/modsecurity-doc-cleanup`-Symlink
`generate-connector-roadmap.py` einen fremden Sentinel überschreiben und
Return Code 0 liefern. Ein lokaler Angreifer konnte Same-User-Dateien über
einen Temp-Root- oder Final-Leaf-Symlink korrumpieren.

Erwartet sind eine zufällige private Temp-Wurzel und deskriptorgebundene,
kanonische Schreibautorität; unsichere Children, Parent-/Final-Links,
Fremddateien und Cleanup-Substitutionen müssen abgewiesen oder nur als Leaf
entfernt werden.

## Betroffener Umfang und Voraussetzungen

- Dateien/Symbole: `ci/lib/report_path_safety.py`, Report-Generatoren,
  `refresh-connector-reports.py`, `generate-connector-roadmap.py`,
  Inventory-Erzeugung, `allocate_private_output_directory`,
  `prepare_report_directory`, `write_report_index` und `run_command`.
- Der Angreifer kann vor der Nutzung durch Generator/Publisher einen
  Verzeichnis-/Leaf-Link unter einem Report-Output-Ancestor vorbereiten.

## Reproduktion und Evidenz

1. `TMP_ROOT/modsecurity-doc-cleanup` als Directory-Link auf ein Verzeichnis
   mit Sentinel anlegen und den Roadmap-Generator ausführen.
2. Mit Parent-/Final-Links und Validation-to-Publish-Swap wiederholen.
3. Die erhaltene Exact-Head-Evidenz hat den historischen Pfad
   `.codex/runs/20260718T075146Z-harden-temp-paths-97486abe/evidence/report-temp-writer-revalidation.md`
   (nicht in diesem Reconciliation-Checkout verteilt),
   SHA-256 `c4dc1573be22442521af0e6254bff8c205068fad51feb5d68b0d3775a80d1660`.
   Der Post-Fix-Command lieferte Exit 0 mit 18 fokussierten Tests auf PR-B-Head
   `3a3e1274e62182a6cb0853d1352a40a52a9196f5`; die Legacy-Klasse liefert nun
   Return Code 1 und bewahrt den Sentinel.

## Root Cause und Remediation

Lexikalische `Path`-Objekte und ein vorhersehbares Temp-Verzeichnis wurden als
Schreibautorität behandelt. PR B trennt kanonische Read-/Write-Autoritäten,
traversiert Verzeichnis-FDs mit `lstat`/No-Follow, publiziert atomar auf
allowlistete Leaves, alloziert CSPRNG-private Wurzeln, validiert Children und
unlinkt nur bekannte Symlink-Leaves. Runtime-Logs behalten PR-A-Capability-
Binding bei vorhandenem `VERIFIED_RUN_ROOT`.

## Akzeptanz, Validierung und Kontrollen

- Legacy-, Parent-/Final-/Swap-Links und Foreign-File-Versuche bewahren
  Sentinels.
- Absolute/Traversal/leere/lange/Unicode-Children scheitern; parallele
  Allokation und normale Report-/Index-Kontrollen gelingen.
- `tests/test_report_temp_path_findings_poc.py` bestand 18/18; In-Memory-
  Kompilierung bestand für 21 geänderte Python-Dateien, und `git diff --check`
  bestand.

## Abhängigkeiten, Blocker, verwandte Findings und Restrisiko

`FND-PARENT-0033` liefert die verifizierte Runtime-Capability für Runtime-Logs.
Framework-gestützter Full Refresh/Layout bleibt `blocked_missing_evidence`.
`FND-PARENT-0035` ist getrennte Library-Regel-Autorität. Der lokale Fix ist
delivery-pending bis Exact-PR-CI-/Review-Evidenz vorliegt; kein Merge oder Risk
Acceptance ist autorisiert.

## Historie

- `2026-07-18T14:46:42Z`: realer Pre-Fix-Clobber reproduziert; Exact-PR-B-
  Head-Kontrollen bestanden; Status auf `fixed` pending verified PR gesetzt.
