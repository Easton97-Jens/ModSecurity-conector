# Change Record: CR-20261008-nginx-event-boundary-driver

**Sprache:** [English](CR-20261008-nginx-event-boundary-driver.md) | Deutsch

Lokale Source-Implementierung; integrierte native Validierung steht aus.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-event-boundary-driver |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `bc9587f086b1e4ff558a870f2d5020aa22f72b64` |

## Motivation und Problemstellung

Zwei Required-Event-Records benötigen echte Phase1-Regel1100402-Callbacks und feste sourcegebundene URI-/Writer-Grenzen einschließlich unabhängiger At255- und Over256-Requests.

## Akzeptanzkriterien

Geschlossene nicht sensible lange Query und exakte Grenz-Eingaben; echte Regel-/Pass-Events, HTTP200, explizite Truncation/Redaction, begrenzte payloadfreie JSONL und unabhängig versiegelte Kindartefakte. Native Ausführung bleibt beim Koordinator.

## Implementierungsentscheidung und Begründung

Ein dünner Adapter verwendet run_operation und echte Request-Header-/Callback-Auswahl-Hooks. Jedes Kind erhält neue Output-/Projection-Wurzel und Laufidentität. Das Aggregat versiegelt exakte Kind-Receipt-Bytes und Source-Identitäten. Grenzen sind feste NGX-Source-Konstanten URI256 und Writer4096, keine erfundenen konfigurierbaren Direktiven. Callback ist request_rule_match/pass, keine log_only-Intervention.

## Geänderte Dateien

ci/runtime/lifecycle/run-nginx-event-boundary-cases.py, tests/test_nginx_event_boundary_driver.py und dieses EN/DE-Paar. Gemeinsame Runtime und Root-Event-Projektion bleiben separat verantwortete Abhängigkeiten.

## Ausgeführte Befehle

Parent-Python über RTK `-m unittest discover -s tests -p 'test_nginx_event_boundary_driver.py' -v`:3 reine Tests bestanden, Exit0. Kein Listener oder nativer Prozess gestartet. Finale Record-/Diff-Prüfungen stehen im externen Koordinator-Handoff.

## Security-Auswirkung

Keine Required-Verkleinerung oder Common-Validator-Änderung. Eingaben sind nicht sensibel; Events benötigen Query-Redaction und dürfen keine Body-/Query-Payload enthalten. Canonical-Reader müssen versiegelte Receipts/Rohdaten sicher öffnen und echte Source-/Build-/Prozessidentität authentifizieren.

## Runtime-Evidence

Kein nativer Lauf oder Modul-Build für diese Fälle. Unit-Beobachtungen prüfen nur Helferinvarianten. Adapter behält NOT_EXECUTED bis Canonical-Validierung.

## Bekannte Einschränkungen

Benötigt gemeinsame C-Runtime-Hooks und Framework-Event-Boundary-Helfer vor Aufruf. Root muss Katalogwortlaut zur konfigurierten Grenze an feste Source-Konstanten anpassen; konfigurierbare Produktgrenze existiert nicht.

## Verbleibende Risiken

Tatsächlich projizierte native URI/Flags, At-/Over-Callbacks, echter Header-Trigger und neue Modul-/Artefaktidentität bleiben bis Koordinator-Slot ungeprüft.

## Nicht ausgeführte Prüfungen mit Begründung

Native Runtime/Build, integriertes Canonical97, vollständige Parent-Suite und Remote-CI/Sonar warten auf Root-Integration/serialisierte Runtime-Autorität. Vollständiges Parent-Bilingual-Target behält fehlende Framework-Submodul-Links dieses isolierten Worktrees als Einschränkung.

## Finaler Diff- und Review-Status

Nur neue delegierte Adapter-/Test-/ENDE-Dateien; lokaler Commit ohne Push/Gitlink/Merge/MRTS-Änderungen. Runtime-Ergebnis partial.
