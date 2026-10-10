# Change Record: CR-20261008-nginx-native-mime-driver

**Sprache:** [English](CR-20261008-nginx-native-mime-driver.md) | Deutsch

Lokale Adapter-Implementierung; finale integrierte native Validierung steht aus.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-native-mime-driver |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `70bfce7f6e776f49ae3f8160b18fed6b8fe4779a` |

## Motivation und Problemstellung

Vier Required-MIME-Records benötigen echte native Requests und finale Wire-Header einschließlich tatsächlich fehlendem Content-Type. Vorhandene HTTP200/Leeres-Log-Beobachtungen beweisen keine native Completion.

## Akzeptanzkriterien

Geschlossene GET-/Body-/MIME-Eingaben, eigenständige Safe-Konfiguration, tatsächliche Backend-Omission, begrenzte eigene Runtime und echte aufbewahrte Wire-/Native-Artefakte. Neue Modul-/Runtime-Akzeptanz bleibt beim Koordinator.

## Implementierungsentscheidung und Begründung

Ein dünner MIME-Adapter delegiert Host-Aufruf, Rollen, PIDFD-Cleanup und Curl-Captures an die run_operation-Schnittstelle der Phase4-Runtime. Vorhandenes deklaratives Response-Header-Backend liefert den echten Missing-Header-Vertrag. Ein Loopback-Thread für einen Request hat begrenzte Accept-/Verbindungs-Timeouts und endet vor Rückkehr. Keine Fixture erzeugt native Events.

## Geänderte Dateien

ci/runtime/lifecycle/run-nginx-mime-cases.py, tests/test_nginx_mime_driver.py und dieses EN/DE-Paar. Abhängigkeit run-nginx-phase4-cases.py und Framework-MIME-Helfer gehören separaten Arbeitsanteilen.

## Ausgeführte Befehle

Parent-Python über RTK: `-m unittest discover -s tests -p 'test_nginx_mime_driver.py' -v` bestand3 Tests, Exit0; `-m unittest discover -s tests -p 'test_nginx_common_input_fault_driver.py' -v` bestand2 Tests, Exit0. Reine Konfigurations-/Delegationskontrollen ohne nativen Prozess oder Listener. Python-Syntax2 und Change-Record-Archivstruktur bestanden. `make check-bilingual-docs` scheiterte an bestehenden Links in das nicht ausgecheckte Framework-Submodul dieses isolierten Worktrees; kein Submodul oder Gitlink wurde verändert, um diese Einschränkung zu kaschieren.

## Security-Auswirkung

Geschlossene Identitäten, exakter Marker-Body, Safe-Modus, begrenztes Loopback-Backend und vorhandene Header-Omission-Prüfung bleiben erhalten. Receipt bewahrt tatsächliche Backend-/Omission-Source-Hashes, Adapter-Hash und zugrunde liegenden Runtime-Hash; Canonical-Validierung muss Artefakte und native Fakten unabhängig authentifizieren.

## Runtime-Evidence

Keine native Runtime für diesen Adapter ausgeführt. Alte In-/Charset-Diagnose-Events und alte unvollständige Out-/Missing-Beobachtungen bleiben Diagnose-Evidence, keine Akzeptanz dieser Source.

## Bekannte Einschränkungen

Benötigt separate gemeinsame Phase4-Runtime-Schnittstelle und Framework-MIME-Helfer vor Aufruf. Root besitzt Dispatch, Receipt-Registrierung und sourcegebundenen finalen Modul-Build. Source-result bleibt NOT_EXECUTED bis unabhängige Canonical-Validierung erfolgt.

## Verbleibende Risiken

Final fehlender Wire-Content-Type, native Append-/Completion-Retention und tatsächliches Prozess-Cleanup benötigen autorisierten Lauf mit neuem Modul. Native Regel1100301 muss für In/Charset auftreten und darf für Out/Missing nicht erfunden werden.

## Nicht ausgeführte Prüfungen mit Begründung

Native Build/Runtime, integrierter E2E, vollständige Parent-Suite und Remote-CI/Sonar nicht ausgeführt; Koordinator reserviert serialisierten Runtime-Slot und besitzt integrierte Lieferung.

## Finaler Diff- und Review-Status

Nur zugewiesene MIME-Source/Tests/ENDE-Nachweis; lokaler Commit ohne Push, Merge, Gitlink- oder MRTS-Änderungen. Runtime-Ergebnis bleibt partial.
