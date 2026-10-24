# Change Record: CR-20261018-haproxy-original-oracle-sources

**Sprache:** [English](CR-20261018-haproxy-original-oracle-sources.md) | Deutsch

Reine Quellenoracle-Lieferung; keine Hostabnahme wird behauptet.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-original-oracle-sources |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `fc7e0d25c6ed3240d6e257e92f25475e63f150c8` |

## Motivation und Problemstellung

Die ursprüngliche HAProxy-Oracle-Teilmenge enthält 124 Erwartungen über drei getrennte Routen. 34 hatten historische Quellenauflösungen; 90 waren offen. Root prüfte 31 zusätzliche exakte Quellenerwartungen unabhängig über die bestehende Reconciliation-API. Diese Quellenfreigaben machen die verbleibenden 59 sichtbar, ohne Host-Lifecycle-Evidence zu erzeugen.

## Akzeptanzkriterien

Das exakt von Root freigegebene Artefakt mit 124 Datensätzen übernehmen; alle ursprünglichen IDs, Werte, ausgewählten Vertragshashes, Revisionen und 34 historischen Datensätze erhalten. Die 31 freigegebenen Quellenreviews mit der eingefrorenen bestehenden API reproduzieren, physische Quellenhashes prüfen und getrennte Routenzahlen erhalten. Kein neuer Hostcredit, Retest, Verzicht auf Runtime-Abwesenheitsnachweise oder Lifecycle-PASS.

## Implementierungsentscheidung und Begründung

Nur die HAProxy-eigene Fixture-JSON wird durch das exakte freigegebene Artefakt mit SHA256 d3a917eec9ac60d5dd23a2d61f6acefc1efd6f52d9c66127a6a93cc05fa90f3e ersetzt. Die ursprünglichen v1-Bytes bleiben extern als source-proposals-v1.json erhalten (SHA256 2e1358250894569b2cb25a0c8409bea95606d4fd48bd1bcc0026bd2847fef05a). SDK 3.0.14, offizielle HAProxy 3.2.25-Dokumentation und der versionierte normative Phasenvertrag sind unabhängige Quellen; Framework-Regeln, deklarierte Eingaben und Fixture-Implementierung bleiben getrennt ausgewiesen. Die freigegebene Fixture-Historie bindet native v7, SPOP v4 und companion v5; spätere Fixture-Änderungen brauchen eine separate Bindung. Der übernommene Candidate-Schema-Identifier bleibt bytegenau erhalten; eingebettete Root-Freigaben legen den tatsächlichen Quellenreviewstatus fest.

## Geänderte Dateien

connectors/haproxy/harness/fixtures/i12-oracles-20261015.json und dieses englisch/deutsche Change-Record-Paar. Zentrale Matrix, gemeinsame Capture-Objekte, Generatoren, andere Connectoren, Common-Implementierung und Produktdateien gehören nicht zu dieser Lieferung.

## Ausgeführte Befehle

Alle Befehle verwendeten RTK. Der aufgabeneigene Python 3.14.7-Verifier approved-source-delivery-20261018/verify.py bestand: Identität der ursprünglichen 1484 Verträge, 124 ursprüngliche Oracle-Datensätze, 34 unveränderte historische Datensätze, 31 reproduzierte Root-Quellenfreigaben und 138 physische Quellenreferenzen mit Hash-/Längenbindung. Die regulären Prüfungen für zweisprachige Dokumentation, Dokumentationslinks und Change-Record-Struktur bestanden. Exakte argv/cwd/Exits und Rohhashes liegen unter /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/oracles/approved-source-delivery-20261018/. Die Strukturprüfung prüft nur Struktur; beide Sprachfassungen wurden auf übereinstimmende Fakten gelesen.

## Security-Auswirkung

Begrenzte defensive Evidence-Pflege im vom Nutzer autorisierten Umfang. Validierung, Quellenunabhängigkeit, ursprüngliche Verträge, Isolation und Hostqualifikation bleiben erhalten. Weder ein tiefer Security-Scan noch eine Exploit-Untersuchung wurden durchgeführt.

## Runtime-Evidence

Keine neue Runtime-Beobachtung wird behauptet. Quellenaufgelöst sind 65/124 bei 59 offenen Fällen: native HTX 31/48 mit 17 offen; SPOP Request 21/44 mit 23 offen; Response-Companion 13/32 mit 19 offen. Diese Zahlen betreffen ursprüngliche Oracle-Erwartungen, nicht die 112/94/72 Routenpflichten oder unabhängige Hostausführungen. Neuer Hostcredit ist 0; vollständige Lifecycle-Qualifikation wurde nicht durchgeführt. Ein SPOP-ACK qualifiziert nicht den unabhängigen Response-Companion.

## Bekannte Einschränkungen

Die 31 Quellenfreigaben enthalten keinen Retestbeleg oder Lifecycle-PASS. Native P3 Redirect behält die geforderten 302 und den historischen v7-Fixture-Konflikt 503; keine Korrektur auf Grün. Connection-Reuse verlangt die vordefinierte Allow/Deny/Allow-Folge mit HTTP [200,403,200], Phasen [2,1,2], EOS [1,0,1], drei Allokationen/Frees und zwei Backendrequests. SPOP ist ein begrenzter Authorization-Pfad für vollständige Samples; kein unbegrenzter Stream oder nicht unterstütztes HTTP/2-Mapping wird als vollständig inspiziert erklärt. Die historischen 34 Datensätze bleiben erhalten und werden nicht neu qualifiziert.

## Verbleibende Risiken

Die 59 exakten Quellenoracle-Lücken benötigen weiterhin ihre eigene ausgewählte Fixture-/Fault-/Scope-Auflösung. Aktuelle Produktfixes und spätere Fixtures ändern freigegebene Quellenhistorie nicht rückwirkend. Physische native Events, erste Ursache, Response-Commit, echter Client-/Backendtransport, EOS und einmaliges Cleanup benötigen getrennte Hostevidence mit aktuellem Build. Feste 500-Vertragskonflikte bleiben unverändert.

## Nicht ausgeführte Prüfungen mit Begründung

Es wurden keine Hostläufe, Paketinstallationen, Produkt- oder Common-Änderungen, Matrixgenerierung, Git-Commits/Pushes/Merges oder breiten Security-Scans durchgeführt. Eine reine Quellen-JSON-Lieferung belegt die damit prüfbaren Runtime-Ebenen nicht; der Koordinator verantwortet spätere Hostabnahme und Lieferung.

## Finaler Diff- und Review-Status

Die freigegebene JSON ist bytegleich mit Roots current-source-inventory124.json, alle Prüfungen auf ursprüngliche und historische Erhaltung bestanden, und beide Sprachfassungen enthalten dieselben Zahlen, Hashes, Umfänge und Einschränkungen. Root hat die 31 Quellenerwartungen bereits über die bestehende API freigegeben. Dieser Change Record dokumentiert nur Quellenlieferung; er erteilt keine Host- oder Mergefreigabe.
