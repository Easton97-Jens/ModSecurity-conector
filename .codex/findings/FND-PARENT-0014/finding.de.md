# FND-PARENT-0014 — Manifest-Cleanup behält ein Same-UID-Leaf-Replacement-Löschrennen

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | `FND-PARENT-0014` |
| Titel / Title | `Manifest-Cleanup behält ein Same-UID-Leaf-Replacement-Löschrennen` |
| Kategorie / Category | `security_candidate` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priorität / Priority | `P1` |
| Schweregrad / Severity | `medium` |
| Konfidenz / Confidence | `probable` |
| Status | `blocked` |
| Machbarkeitsstatus / Feasibility status | `blocked_missing_evidence` |
| Release-Blocker / Release blocker | `true` |
| Security-Relevanz / Security relevance | `true` |

## Zusammenfassung / Summary

Der Helper validiert jedes geplante Leaf über einen gepinnten Parent-Directory-
Descriptor erneut und löscht diesen Namen danach in einer späteren
`unlinkat`/`rmdir`-Operation. Ein bösartiger Same-UID-Prozess mit Änderungsrecht
kann das Leaf im finalen Intervall ersetzen.

## Beobachtetes Verhalten / Observed behavior

`validate_planned_operations()` vergleicht Typ, Gerät, Inode, Owner, Gruppe und
Mode über den Parent-Descriptor. `remove_planned_paths_no_follow()` ruft danach
`os.rmdir()` oder `os.unlink()` mit demselben Namen und Descriptor in einer
getrennten Operation auf.

## Erwartetes Verhalten / Expected behavior

Descriptor-Anchoring muss weiterhin Ancestor-Traversal und Löschung außerhalb
des registrierten Runs verhindern. Eine strikte No-Foreign-Leaf-Deletion-
Behauptung erfordert ein atomares Expected-Object-Löschprimitiv oder eine
separat verifizierte Trust Boundary; keines ist derzeit belegt.

## Auswirkung / Impact

Der gepinnte Parent-Descriptor begrenzt die Löschung auf den registrierten Run;
dies ist kein Escape zu Parent, Framework, MRTS oder beliebigen Host-Pfaden. Es
bedeutet jedoch, dass strikte No-Foreign-Object-Deletion gegen ein feindliches
Same-UID-Leaf-Replacement nicht bewiesen ist.

## Betroffene Dateien und Symbole / Affected files and symbols

### Dateien / Files

- `.codex/bin/storage-budget`
- `.codex/tests/test_storage_budget.py`
- `.codex/context/storage-policy.md`

### Symbole / Symbols

- `validate_planned_operations`
- `remove_planned_paths_no_follow`

## Voraussetzungen / Preconditions

- Ein bösartiger Prozess teilt die effektive UID, die ein registriertes
  Task-Run-Verzeichnis besitzt.
- Er kann den geplanten Leaf-Namen im gepinnten Parent-Verzeichnis verändern.
- Er ersetzt das Leaf nach finaler Validierung und vor `os.unlink()` oder
  `os.rmdir()`.

## Reproduktion / Reproduction

- `validate_planned_operations()` liest finale No-Follow-Leaf-Metadaten über
  `operation.parent_descriptor`.
- `remove_planned_paths_no_follow()` führt `os.unlink()` oder `os.rmdir()` mit
  diesem Namen in einer späteren Operation aus.
- Die aktuelle 49-Test-Suite deckt Spezialdateien, Symlinks, Mounts, retained
  Evidence und Foreign-Process-Referenzen ab, aber kein deterministisches
  finales Leaf-Replacement.

## Evidence / Evidence

- Run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/062-same-uid-pathname-toctou-static-review.log`, Source-to-Sink-Review,
  SHA-256 `2294d4ff41b1266a34a234da0db62072cadd51199efe37db979114ebcafc2dd2`,
  Exit `0`, beobachtet `2026-07-17T14:26:58Z`.
- `logs/043-storage-budget-security-regression-final.log`, SHA-256
  `0b1322f17bb7c1fe5ed71f2b9f94d7eca8c4a01189982289798629a12f6e22ac`,
  beweist 49 fokussierte aktuelle Controls, aber keine atomare finale
  Leaf-Identity-Grenze.

## Grundursachenanalyse / Root-cause analysis

POSIX-Pfad-Entfernung trennt finale Leaf-Identity-Validierung und Entfernung.
Parent-Descriptoren verhindern Parent-Traversal, machen spätere Entfernung aber
nicht von beobachtetem Gerät/Inode abhängig.

## Vorgeschlagene Remediation / Proposed remediation

Vor einer strikten Behauptung das betroffene Objekt für manuelles
owner-autorisiertes Handling erhalten, eine separat vertrauenswürdige Cleanup-
Authority nutzen oder einen kompatiblen atomaren Expected-Object-Deletion-
Mechanismus etablieren. Descriptor-Anchoring, Spezialdatei-Refusal, Evidence-/
Process-Gates oder Dry-Run/Apply-Controls nicht abschwächen.

## Akzeptanzkriterien / Acceptance criteria

- Der Helper behauptet kein nicht verfügbares atomares `unlink-if-inode` oder
  `rmdir-if-inode`.
- Entweder verhindert eine verifizierte Grenze feindliches Same-UID-Leaf-
  Replacement, oder automatische Löschung der betroffenen Klasse scheitert
  geschlossen.
- Bestehende Anchored-Root-, Symlink-, Spezialdatei-, Mount-, Evidence-,
  Process-, Dry-Run-, Apply- und Idempotency-Controls bleiben abgedeckt.

## Validierungsplan / Validation plan

- Die gewählte Grenze mit einem deterministischen Same-UID-Replacement-Versuch
  zwischen finaler Validierung und Entfernung validieren.
- Fokussierte Storage-Budget-Controls samt normalen task-owned Regular-File-
  und Empty-Directory-Fällen erneut ausführen.
- Verifizieren, dass kein Parent-, Framework-, MRTS-, Retained-Evidence- oder
  Out-of-Run-Pfad betroffen sein kann.

## Regressionstests / Regression tests

- `.codex/tests/test_storage_budget.py`
- Ein künftiger deterministischer Final-Leaf-Replacement-Control nach Auswahl
  einer architektonischen Lösung.

## Legitime Kontrolltests / Legitimate control tests

- Die retained 49-Test-Storage-Suite besteht normales task-owned Cleanup und
  aktuell abgedeckte Sicherheits-Controls.

## Abhängigkeiten / Dependencies

- Evidence für ein kompatibles atomares Deletion-Primitiv oder ein
  user-autorisiertes separat vertrauenswürdiges Cleanup-Boundary-Design.

## Blocker / Blockers

- Kein aktuelles repository-supported atomares Expected-Object-Removal-
  Primitiv oder separat besessene Cleanup-Authority.

## Verwandte Findings / Related findings

- `FND-HOST-0001`
- `FND-PARENT-0013`

## Restrisiko / Residual risk

Der Helper ist materiell sicherer und root-begrenzt, aber nicht als Erhalt
eines fremden Same-UID-Leafs bewiesen, das nach finaler Validierung eingefügt
wird. Es liegt keine Risikoakzeptanz vor.

## Historie / History

- `2026-07-17T14:27:29Z`: `current_task_security_boundary_identified` —
  unabhängiges finales Source-Review bestätigte, dass finale Validierung und
  spätere Entfernung getrennte Leaf-Name-Operationen sind. Bestehende
  abgedeckte Controls bleiben wirksam, aber keine atomare Same-UID-Leaf-
  Identity-Grenze ist bewiesen.
