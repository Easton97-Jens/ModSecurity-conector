# Change Record: CR-20261008-nginx-lifecycle-sequence-driver

**Sprache:** [English](CR-20261008-nginx-lifecycle-sequence-driver.md) | Deutsch

Implementierungs-Handoff; finale integrierte Exact-Head-Coverage steht aus.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261008-nginx-lifecycle-sequence-driver |
| Datum (UTC) | 2026-10-08 |
| Basis-Revision | `b7403e30111688da00d8e7ce376ea91ced1c6145` |

## Motivation und Problemstellung

Required-Lifecycle-/Transportrecords brauchen echte Operationen statt aus HTTP abgeleitetem Erfolg oder vom Driver erzeugten Events.

## Akzeptanzkriterien

Sequenzen auf derselben Verbindung, getrennte Transaktionen, native Deny-/Late-Rules, begrenzte Faults, Root/nobody und eigenes Prozess-/Listener-Cleanup beweisen. Echtes Framing, native Access- und Syscall-Beobachtungen aufbewahren.

## Implementierungsentscheidung und Begründung

Sichere Artefakt-, Projektions- und pidfd-Startup-Helfer wiederverwenden. Ein begrenzter H1-Client verbindet niemals unbemerkt neu. Ein eigener Upstream gibt den Marker nach beobachteten Client-Headern frei. Attempt-Interposer binden Root-Launcher, nobody-Worker, genaue Transaktion oder eigenen Client-Socket. Short-Write delegiert einen tatsächlich partiellen Write; Would-Block verwendet kleine eigene Socketpuffer und verzögertes Clientlesen für tatsächliches EAGAIN/Resume. Receipts sind keine erfundenen nativen Events und kein Canonical PASS.

## Geänderte Dateien

`ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py`, `ci/runtime/lifecycle/nginx_sequence_client.py`, `ci/runtime/lifecycle/nginx_sequence_upstream.py`, `tests/fixtures/nginx_transaction_fault.c`, `tests/fixtures/nginx_write_fault.c`, `tests/test_nginx_sequence_client.py`, `tests/test_nginx_sequence_driver.py` und dieses EN/DE-Paar. Zentrale Katalog-/Dispatch-/Collection-Dateien gehören dem Koordinator.

## Ausgeführte Befehle

Parent-Python über RTK führte vier echte Loopback-Clienttests und zwei Driver-Kontrollen mit Exit 0 aus, nachdem die Unsafe-Path-Regression fehlgeschlagen und behoben war. Native Fixtures wurden mit `cc -std=c17 -Wall -Wextra -Werror -fPIC -shared`, Exit 0, kompiliert. Framework-Tests sind separate Repository-Evidenz. Negativkontroll-Flags können keine fremden Fälle beeinflussen; die Begin-Kontroll-ID unterscheidet sich garantiert von der scharfgeschalteten nativen Transaktion. Deaktivierte Writer-Kontrollen erfüllen die erforderliche native Write-Beobachtung nicht.

## Security-Auswirkung

Nur eigene isolierte Attempts, Loopback-Sockets und private begrenzte Captures. Frische direkte Projektionen, Root/nobody und pidfd-Cleanup bleiben verpflichtend. Keine Common-/Produkt-/MRTS-Änderung, globalen Faults, Secret-Dumps oder Protected-Prüfer.

## Runtime-Evidence

Task `nginx-all-required-20261008T124555Z` hält 13 echte Sequenz-/Mapping-/Allokations-/Late-Operationen mit Exit 0 unter `stream-d-r2`. `stream-d-write-r1` belegt partiellen Write und vollständig fortgesetztes Framing. `stream-d-write-r2` belegt natives EAGAIN, positive fortgesetzte Writes und eine vollständige Antwort mit 213228 Bytes. Root/nobody und Cleanup wurden beobachtet. Frühere nicht auslösende Fixtures und künstlicher EAGAIN-Timeout bleiben fehlgeschlagene Attempts.

## Bekannte Einschränkungen

Native Transport-Provenance braucht zentrale Integration. Phase-5-Finish-Failure ist nicht ehrlich als Pre-Commit-HTTP500 belegbar; Engine-Timeout braucht definierten Deadline-Vertrag. Required-Auswahl bleibt unverändert.

## Verbleibende Risiken

Freigegebene Soft-Budget-Arithmetik: Ein reiner begrenzter Zeit-Header misst abgeschlossene synchrone Aufrufe anhand vom Aufrufer gelieferter monotoner Zeitstempel. Standardwert null deaktiviert ihn; exakt am Budget bleibt zulässig, nur größere Laufzeit überschreitet es. Rückwärts laufende/ungültige Zeitstempel und Überlauf werden abgelehnt. C17-Warnings-as-Errors-Regression schlug zunächst wegen fehlendem Header fehl; danach bestanden Kompilation und Grenzwert-/Kontrollausführung. Die Hilfe ist keine harte Deadline, unterbricht keinen hängenden nativen Engine-Aufruf und belegt keinen Host-Timeout ohne Koordinator-Wiring und echte Diagnose-Evidence.

Diagnostik verwendet verifizierte b7403e-Artefakte und separat gehashte Entwicklungshilfen, keine finalen integrierten Artefakte. Operationsgültigkeit ist nicht Canonical PASS; C17-Kompilation ist keine Runtime-Promotion.

## Nicht ausgeführte Prüfungen mit Begründung

Finale integrierte Suites, Standard-Lifecycle, aktuelle CI/Sonar und Protected-Administration bleiben Koordinator-Verantwortung. Keine Gesamtabnahme.

## Finaler Diff- und Review-Status

Die Auswahl `transport_sequential_requests` sendet allow/deny/allow nun auf einem tatsächlichen Socket gemäß Katalogvertrag. Der rote dynamische Test beobachtete vor der Korrektur drei Verbindungen; zwei Transporttests bestehen jetzt, einschließlich der vorhandenen Keep-alive-allow/allow-Kontrolle. Lifecycle-Fälle mit unabhängigen Verbindungen bleiben separat ausgewählt. Native Transportereignisse und finale Canonical-Coverage bleiben beim Koordinator.

Freigegebene Post-Response-Finish-Folgearbeit:

Der versuchsgebundene Finish-Interposer bindet exakten Worker und Case-Transaktion, lehnt natives Logging einmal ab und delegiert echtes Common-Cleanup. Der Client hält den tatsächlichen Body-SHA256 fest. Exakte URI-Zuordnung und statische Fixture ohne Redirect verhindern gemeinsame scharfgeschaltete Identität für fremde Listener-Probes/Internal-Redirects. Sieben Parent-Fokustests bestehen nach rotem Identitäts-Scope-Test. `stream-d-finish-r3` belegt unveränderten HTTP-200-Status/Body, exakten Logging-Fehler, echtes Cleanup und Ablehnung der falschen Transaktion (direkte Exits 0/1). Frühere Versuche bleiben erhaltene Fehler. Weder Produkt-Cleanup-Änderung noch Validator-Lockerung waren nötig. Finale Canonical-Coverage bleibt offen.

Exklusive Source und Negativkontrollen geprüft. Keine fremden Änderungen, Payload-Kopien, Gitlink-Updates, Merges oder Historienumschreibung. Separate Commits warten auf kontrollierte Integration.
