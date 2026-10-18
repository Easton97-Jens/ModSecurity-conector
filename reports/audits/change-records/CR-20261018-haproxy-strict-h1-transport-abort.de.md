# Change Record: CR-20261018-haproxy-strict-h1-transport-abort

**Sprache:** [English](CR-20261018-haproxy-strict-h1-transport-abort.md) | Deutsch

Produkttransport-Follow-up im bestehenden #382; unabhängige Hostabnahme in #415.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-strict-h1-transport-abort |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `ebbb35e19694b6446ecf653934f1b542b94f4cc8` |

## Motivation und Problemstellung

Ein frischer isolierter HAProxy3.2.25-Strict-Hostlauf mit 33 Bytes unterdrückte den wartenden Body, doch der H1-Mux sendete weiterhin TLS close_notify. Die vorab definierte Transportabbruch-Beobachtung blieb trotz Content-Length-Unterlauf falsch.

## Akzeptanzkriterien

Unterstützten harten Transport-Shutdown verwenden, bevor H1 einen sauberen TLS-Shutdown ausführen kann; streamlokalen H2-Shutdown, Unterdrückung wartender Bytes, Safe-Verhalten, bereits gelieferte Bytes und unabhängigen Nachbarzustand erhalten. Wirklichen Transport in einem frischen integrierten Hostwiederholungslauf prüfen.

## Implementierungsentscheidung und Begründung

Nach channel_htx_erase nur die Frontend-Connection über abgesichertes öffentliches sc_conn ermitteln. Bei einer bereiten Connection mit tatsächlichem Muxnamen H1 conn_xprt_shutw_hard vor stream_abort/sc_abort/sc_shutdown/stream_shutdown aufrufen. Der öffentliche Hard-Helfer ruft den Transport mit clean=0 auf, sodass TLS close_notify unterdrücken kann. H2 und unbekannte/nichtverbindungsbezogene Endpunkte behalten ihren bestehenden Stream-Shutdown. Kein Deskriptor-Close/Free oder Backendtransportzugriff wird ergänzt.

## Geänderte Dateien

HAProxy-HTX-Filter und bestehende native I10-Host-Caller-Regressionsfixtures. Dokumentation: connectors/haproxy/README.md und README.de.md sowie dieses Change-Record-Paar. Common, SPOP, MRC1 und eingefrorenes Physical-Sink-Verhalten bleiben unverändert.

## Ausgeführte Befehle

RTK-verpackte Callbackmatrix mit tatsächlichen Upstream-Inline-APIs: drei Tests und 25 Mutationen bestanden; finale ASan/UBSan-Kontrolle bestand. C17-/Overlayprüfungen und ein frischer vollständiger HAProxy3.2.25-Build bestanden. Exakte Compiler-argv, Exits, rohe C-Fixtures und Hashes sind im externen Lauf i12-haproxy-415-acceptance-20261015/product-spop/strict-tls/review.json indiziert; 56 rohe C-/JSON-Dateien umfassen 28 Proben. Der alte ebbb35-Filter verletzt vor dem Fix die Hard-/Clean-Reihenfolge-Assertion mit echten APIs.

## Security-Auswirkung

Nur der betroffene bereite H1-Frontendtransport erhält harten Shutdown. H2 behält den bestehenden Muxpfad pro Stream, sodass diese Korrektur seinen gemeinsamen Transport nicht explizit schließt. Null-Stream/Frontend/sedesc/Connection, nicht bereiter Transport und nichtverbindungsbezogene Endpunkte sind abgesichert. Keine Abschwächung von Loader, Isolation, Validierung, Compilerwarnungen, Gates oder Abhängigkeiten.

## Runtime-Evidence

Historische und frische Vorher-Rohbelege bleiben erhalten: Der initiale ea62-Strict-Client erhielt 200-Header mit deklarierten 33 Bytes, null Bodybytes und sauberem TLS close_notify; Safe erhielt die vollständigen unabhängig erwarteten 33 Bytes. Die getrennten Proben hatten jeweils einen gesunden 12-Byte-Nachbarn. Diese Läufe bestätigen Unterdrückung und verbleibende Clean-Close-Lücke; sie qualifizieren die neue Transportkorrektur nicht.

## Bekannte Einschränkungen

Harter Shutdown kann gelieferte Bytes nicht zurückholen. Tatsächliches H1-Wire-Verhalten und Auswirkungen auf parallele H2-Streams benötigen unabhängige Hostmessung. Eine H2-Nachbarkontrolle auf Komponentenebene ist kein H2-Hostruntime-Beleg. TCP-Reset wird nicht aus Trunkierung oder TLS-Fehlern abgeleitet.

## Verbleibende Risiken

Frische integrierte Capture-Builds und Safe-/Strict-Fälle für leere, gepufferte, große, mehrteilige, streamende, abgebrochene und parallele Requests bleiben erforderlich. Ursprüngliche Abbrucherwartungen bleiben unverändert; kein HTTP-only-Ergebnis wird ein vollständiger Lifecycle-PASS.

## Nicht ausgeführte Prüfungen mit Begründung

Frische Hostausführung und Final-Head-CI/Sonar folgen normaler Integration #382→#410→#415 und Neubau. Kein automatischer Merge. Der unabhängige historische #382-Gitleaks-Release-Blocker bleibt bestehen.

## Finaler Diff- und Review-Status

Getrennter Produktdelta, eingefrorene Drei-Dateien-Identität und EN/DE-Handoff bleiben unter product-spop/strict-tls erhalten. Root prüfte den H1-begrenzten öffentlichen API-Guard und die Shutdown-Reihenfolge; unabhängiger Review und integrierte Hostqualifikation werden getrennt verfolgt.
