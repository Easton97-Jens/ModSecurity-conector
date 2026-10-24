# Change Record: CR-20261018-haproxy-spop-client-window

**Sprache:** [English](CR-20261018-haproxy-spop-client-window.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-spop-client-window |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `f8a1bfa272dfd3ca0953ad8e7ca2dffe5864140d` |

## Motivation und Problemstellung

Ursprünglichen SPOP-Clientzeilen fehlten tatsächliche Start-/Abschlusszeitstempel; dadurch war kein unabhängiger Allocation-/Clientfenster-Abgleich möglich. Dem Elternprozess-Beleg fehlte außerdem die tatsächlich gewartete Kind-PID. Bestehende diagnostische Zeitstempel und historische Läufe müssen unverändert bleiben.

## Akzeptanzkriterien

Tatsächliche Wall-/Monotonic-Sende- und Abschlussfenster einschließlich Fehlern, echte IP-Socket-Endpunkte oder explizite Fehlgründe sowie tatsächliche Client-PID erfassen. Eltern-Popen-PID, gewarteten Exit/Signal, Timeout und Reaping ohne Ableitung erfassen. Ursprüngliche Requests/Responses/Frames, Admission und Erwartungsprädikate erhalten; sämtliche94Original-JSON/Oracles bytegleich und alle729historischen v4Dateien erhalten.

## Implementierungsentscheidung und Begründung

Nur der ursprüngliche Clientpfad erhält Messfelder. Abschluss wird in finally erfasst; nach fehlgeschlagenem Senden bleibt der Sendeabschluss null mit Grund. Endpunkte stammen aus dem echten Socket. Eine schmale Popen/wait-Grenze erhält exakte argv und40Sekunden Timeout; Timeout tötet und wartet vor Weitergabe, andere Wait-Ausnahmen ebenfalls. Keine Produkt-, gemeinsamen Capture-, Generator-, Framework- oder Oracleänderung.

## Geänderte Dateien

`connectors/haproxy/harness/i12_spop_host.py`, neu `tests/test_haproxy_i12_spop_client_window.py` sowie dieses EN/DE-Change-Record-Paar. Andere parallele Arbeit bleibt außerhalb dieser Änderung.

## Ausgeführte Befehle

Alle Shellbefehle verwendeten RTK. Vorher-Beleg spop-window-before führte den alten Client mit harmlosem echtem TCP-Peer aus und scheiterte am fehlenden started_wall_ns. `rtk proxy python3 -m unittest -v tests.test_haproxy_i12_spop_client_window tests.test_haproxy_i12_spop_wire` bestand45Tests:8Messprüfungen und37bestehende Wire-/Prädikatprüfungen. Positive/Fehler-TCP-Kontrollen beobachten tatsächliche Intervalle/Endpunkte; unabhängige Kinder prüfen0/7/SIGTERM/Timeout-Kill-Wait/Startfehler. Exakte argv/cwd/Exits/Loghashes liegen unter `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/product-spop/spop-window-*.json`. Abschließende `rtk proxy make check-bilingual-docs check-doc-links` und `rtk proxy git diff --check` bestanden. Exakter Quellvergleich bestätigt außerdem capture_response, original_rules, original_configuration, evaluate_original, prepare_host_inputs, original_client und response_measurement bytegleich gegen die Basis.

## Security-Auswirkung

Begrenzte defensive Nachweiskorrektur. Keine Validierung, Isolation, Redaktion oder Erwartung wird geschwächt. Fehlende Daten bleiben explizit abwesend; Prozess-Cleanup wird über wait beobachtet. Kein tiefer Security-Scan und kein tatsächlicher HAProxy-Hostlauf wurde ausgeführt.

## Runtime-Evidence

Harmlose echte TCP- und Kindprozess-Komponentenkontrollen belegen ausschließlich die Messgrenze. Kein HAProxy-, Native-Allocation-, Lifecycle-PASS-, Backendzustellungs- oder Original-Oracle-Nachweis wird behauptet. Historische Zeilen erhalten keine erfundenen Zeitstempel oder PID-/Exit-Nachträge.

## Bekannte Einschränkungen

Das ursprüngliche Requestfenster beginnt unmittelbar vor dem Senden auf einem bereits verbundenen Socket; der vorherige Verbindungsaufbau liegt außerhalb dieses Fensters. Fehlende Socket-Endpunkte werden explizit angegeben. Diagnostische capture_response-Zeitstempel bleiben wie zuvor implementiert.

## Verbleibende Risiken

Nur ein frischer zugelassener Hostlauf kann diese unabhängigen Clientfenster/PIDs mit physischen nativen Beobachtungen verbinden. Root verantwortet Review, v5Fixture-Versiegelung, tatsächliche Hostwiederholungen und Qualifikation.

## Nicht ausgeführte Prüfungen mit Begründung

Für diese reine Python-Messänderung ist kein Produktneubau erforderlich. Dieser Worker führte keinen HAProxy-Hostlauf, Git-Schreiben, Veröffentlichung, Merge, Paketinstallation oder tiefen Scan aus. Fixture v5 bleibt bis zum Koordinatorreview unversiegelt; altes v4 bleibt versiegelt und unverändert.

## Finaler Diff- und Review-Status

Der externe v5Vorbereitungsvergleich erhält729Dateien, ändert nur106Host-Messkopien sowie Sourcebinding-/Index-/Ledger-Metadaten und erhält106selected-JSON-Dateien einschließlich94Original-Effective-Oracles bytegleich. Quell-/Diffhashes und abschließende Bilingual-/Linkergebnisse liegen unter spop/client-window; Root kontrolliert Review, Versiegelung und Lieferung. Kein vollständiger Hostnachweis wird behauptet.
