# Change Record: CR-20261008-nginx-raw-h1-native-invocation

**Sprache:** [English](CR-20261008-nginx-raw-h1-native-invocation.md) | Deutsch

Native Invocation-Producer; nur Unit-Verifikation.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-raw-h1-native-invocation |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `883693506efa4ce64a016e2a440ac20ace367efd` |

## Motivation und Problemstellung

Eine eigene native Host-Invocation für die vier geschlossenen fehlerhaften HTTP/1-Request-Verträge bereitstellen, ohne Engine-Events für Core-Parser-Ablehnungen zu erfinden.

## Akzeptanzkriterien

Exakte begrenzte Request-/Response-Bytes, einen pfadgebundenen nativen Access-Eintrag, begrenzte Parserdiagnosen, Positivkontrolle und echte Host-Rollen-/Cleanup-Receipts erfassen. canonical_status bleibt NOT_EXECUTED.

## Implementierungsentscheidung und Begründung

Eigene Host-Rollen-/Start-/Cleanup-Helper und geschlossene Framework-Raw-H1-Verträge wiederverwenden. Binary/Modul/Regeln snapshotten, Loopback-Listener binden, Root-Master/nobody-Worker nutzen und Fault-/Control-Wire-Bytes samt Receipt-Hashes erhalten. Beobachtungsgültigkeit ist kein Canonical-PASS.

## Geänderte Dateien

ci/runtime/lifecycle/run-nginx-raw-h1.py; tests/test_nginx_raw_h1_driver.py; this EN/DE pair.

## Ausgeführte Befehle

RTK-gekapselte Parent-.venv-Unittests tests.test_nginx_raw_h1_driver bestehen 3 Tests (stream-c-parent-raw.log): generierte Loopback-/Root-nobody-Konfiguration, tatsächliche begrenzte Socket-Sende-/Empfangserfassung und exakt ein Access-Eintrag mit fehlenden/fremden/doppelten Negativfällen. In-Memory-Syntax besteht beide Python-Dateien. ci/tools/new-change-record.py check, make check-bilingual-docs und make check-doc-links (expliziter aktueller Framework-Checkout) bestehen; Diff-Whitespace ist sauber.

## Security-Auswirkung

Geschlossene Wire-Verträge und begrenzte Erfassung vermeiden beliebige Eingaben oder Logspeicherung; rollenbewusstes Cleanup wird wiederverwendet. Host-Core-Ablehnung erfindet weder Engine-Regel-Event noch Canonical-Ergebnis.

## Runtime-Evidence

Keine frische native Runtime ausgeführt. Die 3 Unit-Kontrollen enthalten einen echten lokalen Testsocket, nicht NGINX. Frühere Vier-Fall-Probes mit altem Build, 400 und Diagnosen sind keine frische Abdeckung dieses Commits.

## Bekannte Einschränkungen

Das Source-Receipt bleibt NOT_EXECUTED, bis unabhängige Retained-Byte-/Source-/Build-/Host- und Canonical-Integrationsprüfungen bestehen.

## Verbleibende Risiken

Frische integrierte Build-/Runtime-Evidenz, administrative Quellautorität und Canonical-Ergebnisgenerierung bleiben Koordinator-Verantwortung.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Build, native NGINX-Runtime, E2E, Remote-CI, Sonar oder Push im Rahmen dieser begrenzten Aufgabe.

## Finaler Diff- und Review-Status

Standalone-Raw-Host-Invocation und kontrollierte Seam-Tests geprüft; separater Vier-Dateien-Commit mit generiertem Record-Paar. Andere parallele Dateien bleiben unberührt.
