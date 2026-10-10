# Change Record: CR-20261008-nginx-pointer-protocol-cleanup-selection

**Sprache:** [English](CR-20261008-nginx-pointer-protocol-cleanup-selection.md) | Deutsch

Begrenzte Eventprojektion; originale Rohdaten bleiben erhalten.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-pointer-protocol-cleanup-selection |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `bcb02b6b20c2e0697be3c0cd8013ce9b28aa1afa` |

## Motivation und Problemstellung

Neue native Cleanup-Evidenz nach Rückkehr teilt den P1-JSONL-Sink. Alle Zeilen an den strikten Ein-Protokollfehler-Helper zu geben schließt Cleanup fälschlich ein.

## Akzeptanzkriterien

Nur tatsächlich quellgebundenen eigenen P1-protocol_error auswählen; originale JSONL und Hashes einschließlich Cleanup erhalten; strikte Wrong-TX-/Phase-/URI- und Duplikat-Negative erhalten. Kein nativer Lauf/Build.

## Implementierungsentscheidung und Begründung

select_protocol_events(rows,transaction,path) verlangt exakt nativen nginx-Connector/Modus, protocol_error/MSCONN_EVENT_PROTOCOL_ERROR, request_headers, gleiche Transaktion, POST und exakte URI. Es filtert ohne Records zu bearbeiten; keine/mehrere oder fehlerhafte ausgewählte Errors werden vom unveränderten strikten Framework-Helper weiter abgelehnt. Vollständiger Rohhash/Capture von phase1-events.jsonl bleibt unverändert.

## Geänderte Dateien

Nur Parent ci/runtime/lifecycle/run-nginx-common-input-fault.py, tests/test_nginx_common_input_fault_driver.py und dieser gepaarte Record. Root-Modul/Framework-Helper nur gelesen.

## Ausgeführte Befehle

RTK-gewrapter fokussierter Parent-Unittest mit explizitem FRAMEWORK_ROOT: zuerst Exit1 wegen fehlendem Selektor, final Exit0/drei Tests ohne Skips. Bytes und SHA der reinen gemischten JSONL-Datei bleiben identisch. Der Strict-Framework-Helper nutzt nur die Standardbibliothek und wird an der expliziten Grenze readonly geladen. Portabler Befehl: `rtk proxy env FRAMEWORK_ROOT="${FRAMEWORK_ROOT}" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 "${PARENT_PYTHON}" -m unittest discover -s tests -p test_nginx_common_input_fault_driver.py`. Natives Record-Scaffold erstellt Exit0; finale Checks im Handoff.

## Security-Auswirkung

Keine erfundenen Events oder Rohdaten-Rewrites. Selektor begrenzt auf tatsächliche eigene Request-Identität, ohne nachgelagerte Status-/Action-/Rule-/Errorprüfungen zu schwächen. Wrong-TX-/Phase-/URI-/Method-/Connector-/Mode- und doppelte gültige Zeilen scheitern am Strict-Helper.

## Runtime-Evidence

Kein Lauf/Build ausgeführt. Aktuelle Root-Cleanup-Source ruft readonly geprüft Common-Cleanup, dann natives void-Cleanup auf und emittiert danach ihr Logging-Event; reine Tests modellieren nur Koexistenz, keinen nativen Cleanup-PASS.

## Bekannte Einschränkungen

Reine Tests sind keine Live-Pointer-Injection-Evidenz. Fehlt der Framework-Helper, überspringt der zusätzliche Helper-Integrationstest ausdrücklich; der tatsächliche Task-Befehl setzte FRAMEWORK_ROOT und hatte null Skips.

## Verbleibende Risiken

Root muss aktualisierte Treiber-/Source-Hashes integrieren und exakte native Runtime-Validierung durchführen. Bestehender Readerguide-Satz zu MIME-Scope/content_type_not_in_scope ist gegenüber quellseitiger Late-Intervention-Resolution veraltet; Root gemeldet, nicht bearbeitet.

## Nicht ausgeführte Prüfungen mit Begründung

Kein nativer Lauf/Build, keine Framework-Mutation/-Tests, MRTS, Scanner, Push oder Main-Integration. Nur begrenzte reine Parent-Prüfungen; breitere integrierte Checks bleiben bei Root.

## Finaler Diff- und Review-Status

Begrenzter Review bestätigt vollständige originale Rohhash-Schleife und nur geänderte beobachtete Eventprojektion. Commit und finale Validierung separat geliefert; keine Runtime-Promotion behauptet.
