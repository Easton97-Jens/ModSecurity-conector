# Change Record: CR-20261018-haproxy-route-observation-extractor

**Sprache:** [English](CR-20261018-haproxy-route-observation-extractor.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-route-observation-extractor |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `7ad1d7b1c6d88c7430213d408f1f184f2442314c` |

## Motivation und Problemstellung

Die aufbewahrten SPOP- und Response-Companion-Captures benötigen eine quellgebundene Beobachtungsstruktur zur unabhängigen Root-Prüfung. Ein Request-ACK kann keine Response-Verarbeitung qualifizieren; Quellvorhersagen ersetzen keine physischen Client- und Native-Messungen.

## Akzeptanzkriterien

Alle 35 Felder der bestehenden `reviewed_packet`-API bleiben erhalten. Attempt, Falldaten-Root, Spec, Build-Beleg, Fixture, Route und ursprüngliche Fallidentität müssen explizit vorliegen. Fehlende oder mehrdeutige Beobachtungen bleiben mit Begründung null. Alle Ergebnis- und Freigabefelder bleiben offen. Historische Rohartefakte und Fixtures bleiben unverändert.

## Implementierungsentscheidung und Begründung

Der Extraktor verwendet die Deskriptorzulassung des aktuellen Captures, den nativen Transition-Helfer, den begrenzten SPOP-Decoder, MRC1-Framing und das bestehende Schema der Messrollen. Controller-, Spec- und Admission-Hashes binden die Ausführung. Versiegelte Root-Binding-Ledger lösen Namespace-Images in physischen externen Storage auf; kein Namespace-Pfad wird lokal geöffnet. Build-Provenienz und physische Image-Hashes müssen übereinstimmen. Batch-Queue-Hashes und tatsächliche Member-Belege binden jeden Fall an sein eigenes Datenverzeichnis.

## Geänderte Dateien

Die v4-Korrektur dekodiert physische SPOP-Backendzeilen mit `header_hex` und `body_hex` und bewahrt deren ursprüngliche Felder `neighbor`, `wall_ns` und den Rohdatensatz. Der aufgezeichnete Header enthält den CRLFCRLF-Trenner nicht; eingebettete Trenner, ungültige Request-/Headersyntax, mehrdeutige Längen, Transfer-Coding, abweichende Bodylängen und übergroße Hexdaten werden abgelehnt. Unbekannte oder beschädigte Zeilen lassen die exakte Backendanzahl und Korrelation unbekannt. Eine gemessene Null erfordert zusätzlich Backend-Readiness, einen gejointen Producer und genau einen unabhängig erfassten gesunden Nachbarn. Bestehende Companion-Backendformate bleiben unterstützt. Pfadanzahlen allein belegen keine Zuordnung zu einzelnen Clients.

Aktuelle Host-Input-Provenienz kann das geprüfte Abschluss-Siegel der drei Binärdateien direkt binden. Der Observer verlangt das exakte Direct-/Agent-/Companion-Inventar, die exakte Quellrevision, alle vier unveränderlichen Image-Hashes einschließlich der separat fixierten nativen Engine sowie das vom Controller geprüfte Artefakt-Ledger. Das frühere Build-Receipt-Format bleibt für aufbewahrte Läufe unterstützt.

Der native Direct-Observer verlangt zusätzlich den vom Controller gehashten Spec und den Admission-Beleg. Er löst Direct-Binärdatei, SDK, Quellprovenienz, Fixture-Vertrag und Launch-Einstieg aus dem Namespace über die exakten Artefakt- und Fixture-Ledger auf und vergleicht anschließend alle Provenienz-Images mit Quelle, versiegelter Kopie und Abschluss-Siegel. Namespace- und physischer Pfad bleiben getrennt; ein ausgetauschter Spec, ein anderes Fixture, Binary, SDK, Ledger oder Provenienzfile wird abgelehnt.

- `connectors/haproxy/harness/i12_native_cases.py`
- `connectors/haproxy/harness/i12_native_observe.py`
- `connectors/haproxy/harness/i12_route_observe.py`
- `tests/test_haproxy_i12_native_cases.py`
- `tests/test_haproxy_i12_route_observe.py`
- `reports/audits/change-records/CR-20261018-haproxy-route-observation-extractor.md`
- `reports/audits/change-records/CR-20261018-haproxy-route-observation-extractor.de.md`

## Ausgeführte Befehle

```sh
rtk proxy env PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_haproxy_i12_route_observe
```

Neunzehn gezielte Tests prüfen gespeicherte Schemata, unvollständige oder beschädigte Evidence, Nachbarfälle, Client-Payload-/UUID-/Endpunkt-/Zeitkonflikte, versiegelte Images, Batch-Roots, tatsächliche Prozessbelege und Request-Authorization-Finish. Die gespeicherten Extraktionsbelege enthalten exakte Argumente, Exits und Rohhashes unter `R2/route-observer-20261018`.

Für v4 wurde die deklarierte Python-3.14.7-Umgebung verwendet:

```sh
rtk proxy env PYTHONNOUSERSITE=1 /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -B -m pytest -q tests/test_haproxy_i12_route_observe.py
```

Alle 24 Tests und 20 Subtests bestanden, einschließlich wörtlich übernommener aufbewahrter Pilot-Backendzeilen, gültiger Bodies, beschädigter Grenzen/Header/Längen/Metadaten, unbekannter Zeilen, fehlender Positivkontrollen und unvollständigem JSONL. Die v4-Belege für gespeicherte Extraktionen und Validierung liegen unter `R2/route-observer-20261018/v4`; diese Korrektur ergänzt weder Hostläufe noch Qualifikation.

Der aktuelle Follow-up führte beide betroffenen Module gemeinsam und anschließend die gesamte HAProxy-I12-Harnessgruppe aus. Das gezielte Ergebnis lautet 48 Tests und 29 Subtests bestanden; das breitere Ergebnis lautet 194 Tests und 106 Subtests bestanden. Die neuen Kontrollen lehnen eine inhaltsgleiche Direct-Binärdatei an einem anderen Pfad, ein geändertes SDK, einen falschen Namespace, ein geändertes Siegel-/Provenienz-Image und ein unvollständiges Image-Inventar ab. Der Redirect-Headervergleich akzeptiert HTTP-OWS, lehnt aber weiterhin fehlende, falsche oder doppelte `Location`-Felder ab.

## Security-Auswirkung

Dies ist ein begrenztes defensives Abnahmewerkzeug. Es liest zugelassene physische Dateien und schreibt eine neue exklusive Ausgabe. Es ergänzt weder Hostverkehr noch einen breiten Scan, eine Autorisierungsänderung, Ausnahme oder Unterdrückung. Ein geändertes Quellsiegel oder widersprüchliches Namespace-Binding wird abgelehnt.

## Runtime-Evidence

Sieben Pakete wurden aus aufbewahrten Fallausführungen in sechs Isolation-Attempts extrahiert: Safe, Strict, drei frühere SPOP-Fälle und zwei frische SPOP-Pilot-Member unter einem gemeinsamen Controller. Die Extraktion startet keinen Host. Jedes Paket bewahrt alle 35 Felder, die ausstehende Root-Prüfung sowie null für Oracle-Auswertung und Ergebnis. Den bestehenden Safe-/Strict-Captures fehlen Client-Startzeiten; den ursprünglichen SPOP-Clientzeilen fehlen beide Intervallgrenzen. Diese fehlenden Zeitstempel bleiben unbekannt.

## Bekannte Einschränkungen

UUID-/PID-/Scope-/Pfad-/Payload-Verknüpfungen bleiben bei fehlenden Clientintervallen nur Teilzuordnungen. MRC1-Capability-Hashes verbinden tatsächliche Claims, Handoffs und Host-Callbacks separat. Global nicht zugeordnete native Zeilen, Host-Callbacks und physische Sinkzeilen bleiben sichtbar. Tatsächlicher endlicher P2-Abschluss und Request-Finalisierung bleiben bekannte Rohfakten; ihr Streaming-EOS-Argument bleibt ausdrücklich null. Ein abgeschlossener SPOP-Sample erzeugt weder Streaming-EOS noch Response-Phasen. Common-Cleanup zählt nicht als zweite native Freigabe.

## Verbleibende Risiken

Die Klassifikation der ersten Ursache, terminale Eventsemantik, exakte Transport-/Schreibzuordnung und ursprüngliche Oracle-Auswertung bleiben unabhängige Root-Arbeit. Native Auditdaten ersetzen nie physische Common-Events. Unbekannte Framework-/MRTS-Identitäten bleiben null. Künftige Zeitstempelfelder werden nur bei neuer Messung unterstützt; ältere Pakete werden nicht durch Schlussfolgerungen repariert.

## Nicht ausgeführte Prüfungen mit Begründung

Dieser Harness-Follow-up startete weder einen neuen Host, Produktbuild noch Scannerlauf. Er wurde auf einen separat aufbewahrten aktuellen Host-Attempt angewandt; dieser Attempt und seine unabhängige Root-Qualifikation stehen in der aktuellen Abnahme-Evidence und gelten nicht als Eigenschaft des Extraktors.

## Finaler Diff- und Review-Status

Geändert werden ausschließlich HAProxy-Fixture-/Observation-Harnesses, ihre Tests und dieser zweisprachige Change Record. Die sechs zuvor eingefrorenen Sonar-Dateien bleiben unberührt. Lieferung und Veröffentlichung sind getrennte Schritte.
