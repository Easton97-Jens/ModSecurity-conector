# Change Record: CR-20261030-nginx-request-error-status

**Sprache:** [English](CR-20261030-nginx-request-error-status.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261030-nginx-request-error-status |
| Datum (UTC) | 2026-10-30 |
| Basis-Revision | `8c7e8c44cf69ac4e9d7ffb9101365c552f2ca7cf` |

## Motivation und Problemstellung

Die reale H1-Injektion der beiden internen Common-Input-Faults lieferte HTTP 500
und CONNECTOR_ERROR, während das native Event den bekannten terminalen Status
nicht enthielt (`http_status=0`). Eine separate Framework-Erwartung wählte noch
`phase1_error`. Common emittiert absichtlich das kanonische Event
`connector_error` mit typisiertem `phase=request_headers`.

## Akzeptanzkriterien

Den gewählten terminalen Status von 400 bis 599 melden, ohne sichtbare Antwort,
abgeschlossenen Transport oder tatsächliche Aktion zu erfinden. Timeout 504,
späte/Kontrollwerte 0, Fail-closed-Verhalten und einmaligen Schreibversuch erhalten.
Konsumenten prüfen kanonisches Event, exakte Phase, Message-ID und Status.

## Implementierungsentscheidung und Begründung

Der Product-Produzent kopiert den bereits gewählten begrenzten Fehlerstatus in
die HTTP-Metadaten. Transport und sichtbarer Status bleiben unverändert. Dies
schließt eine Beobachtbarkeitslücke; weder Wire-Statuswahl noch Request-Lifecycle
ändern sich. Common-Kanonisierung bleibt maßgeblich; Framework-Konsumenten folgen
diesem Vertrag. Siehe den [Event-Vertrag](../../../docs/pr-382-event-contract.de.md).

## Geänderte Dateien

`connectors/nginx/src/ngx_http_modsecurity_access.c` und dieses EN/DE-Protokoll.
Produzentenregressionen, strikte Konsumenten und Negativ-Fixtures gehören in
Framework-PR #142. Die Product-Korrektur erhält einen separaten Commit gegenüber
Ownership-Migration und Framework-Pin-Änderungen.

## Ausgeführte Befehle

- Bestehende Produzentenregression: 15 Methoden; sechs erweiterte Assertions
  reproduzierten vor der Korrektur fehlende bekannte 500/400/413-Metadaten.
- Derselbe reale extrahierte Product-Produzent mit Common-Writer: danach
  15 PASS (1,631 Sekunden), einschließlich 500/400/413, Timeout 504 und später/
  Kontrollwerte 0; Assertions für sichtbaren Status, Aktion und Transport bleiben.
- Bestehender Framework-Treiber und öffentlicher Konsument: 9 und 4 Methoden PASS.
  Gemeinsamer Nachweis: 28 Methoden / 156 erweiterte Subtests, keine Skips.
- Reale H1-Baseline vor der Korrektur: PASS. Beide Faults: Wire-HTTP 500 mit
  nativem Fault-Ledger und vollständigem Cleanup, alte Event-Auswahl fehlgeschlagen.
- Whitespace-Prüfung des Product-Diffs: PASS.

## Security-Auswirkung

Nur vorhandene begrenzte Metadaten werden sichtbar. Fehlende Transportevidenz
wird weder sichtbare Antwort noch erfolgreiche Aktion. Fehlerhafte Clientdaten
bleiben Protokollfehler/HTTP 400, interne Pointer-Faults Connectorfehler/HTTP 500.
Keine Änderung an Validierung, Isolation oder Compilerwarnungen.

## Runtime-Evidence

Synthetische Quittungen liegen extern unter `nginx-canonical-event-regression`;
keine Kundendaten. Frühere Runtime-Fehler bleiben dokumentiert. Compile-/Unit-
Evidenz bleibt vom erforderlichen neuen Modul und H1-Runtime-Nachweis getrennt.

## Bekannte Einschränkungen

Ein bekannter gewählter Status beweist keine Zustellung. HTTP-Kontrollwerte
außerhalb 400..599 bleiben 0. Das vorhandene spezielle Timeout-504 bleibt erhalten.

## Verbleibende Risiken

Ein Revert der beiden Zuweisungszeilen stellt die Auslassung ohne verändertes
Wire-Verhalten wieder her; keine Konfigurations- oder Speichermigration.

## Nicht ausgeführte Prüfungen mit Begründung

Frisch gebauter H1-Lauf sowie gehostete Checks und SonarCloud am aktuellen Head
stehen an diesem Protokollstand aus. Keine vollständige historische oder
On-demand-Kampagne wurde ausgeführt.

## Finaler Diff- und Review-Status

Produzentenauslassung und kanonischer Event-Unterschied wurden unabhängig anhand
realer C-Ausführung und eingecheckter Verträge geprüft. Die bedingte Merge-Freigabe
verlangt sauberes SonarCloud am aktuellen Head, keine neuen offenen Findings und
alle Repository-Gates; dieses Protokoll behauptet deren ausstehende Ergebnisse nicht.
