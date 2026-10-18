# Change Record: CR-20261018-haproxy-spop-sequences-sonar-refactor

**Sprache:** [English](CR-20261018-haproxy-spop-sequences-sonar-refactor.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261018-haproxy-spop-sequences-sonar-refactor |
| Datum (UTC) | 2026-10-18 |
| Basis-Revision | `7ad1d7b1c6d88c7430213d408f1f184f2442314c` |

## Motivation und Problemstellung

Die 16 zugewiesenen Sonar-Befunde in den SPOP-Quellfixtures/dem Hosttreiber und im nativen Sequenztreiber/-test bearbeiten, ohne Routenprädikate, Original-Oracles, Wire-Repräsentationen oder eingefrorene Fixture-Artefakte zu ändern. Grundlage ist der aufbewahrte PR-415-Befundbericht für Revision `7ad1d7b1c6d88c7430213d408f1f184f2442314c`.

## Akzeptanzkriterien

Gemeldete Funktionskomplexität und wiederholte Literale reduzieren, ungenutzten Clientparameter und verschachtelte Bedingung entfernen sowie den einzigen auslösenden Aufruf im Exceptiontest isolieren. Parität von Auswahldefinitionen, Paketen, Konfiguration und Beobachtungen nachweisen, alle eingefrorenen Artefakte erhalten und fokussierte Prüfungen unter Python 3.14.7 bestehen. Frisches Sonar-Readback bleibt separat erforderlich.

## Implementierungsentscheidung und Begründung

Endpoint-IP-/Portprüfungen, Request-/Evaluatorprüfungen, Beobachtungsstatus, Hostvorbereitung/-start, Erfassung einzelner nativer Sequenzrequests und Allokationszuordnung extrahieren. Bestehende Fetchausdrücke, Dateinamen und Ledgersuffix als Konstanten bündeln. Vergleichsreihenfolge, Fehlergründe, Guards, Kontrollwerte, Clientrequestbytes, Socketwiederverwendung, native Allokationsintervalle und Erhaltung zusätzlicher Aufrufe bleiben erhalten. Der Exceptiontest erzeugt sein Socket vor der Exceptionassertion. Keine Unterdrückung oder Änderung eines Gates.

## Geänderte Dateien

- `connectors/haproxy/harness/i12_spop_cases.py`
- `connectors/haproxy/harness/i12_spop_host.py`
- `connectors/haproxy/harness/i12_native_sequences.py`
- `tests/test_haproxy_i12_native_sequences.py`
- `reports/audits/change-records/CR-20261018-haproxy-spop-sequences-sonar-refactor.md`
- `reports/audits/change-records/CR-20261018-haproxy-spop-sequences-sonar-refactor.de.md`

## Ausgeführte Befehle

```sh
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python -m pytest -q tests/test_haproxy_i12_spop_wire.py tests/test_haproxy_i12_native_sequences.py tests/test_haproxy_i12_spop_samples.py
rtk proxy /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/test-env/bin/python /var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/sonar-spop-sequences-20261018/verify-parity-v3.py
```

Python 3.14.7: 49 Tests und 47 Subtests bestanden. Das Paritätsskript schloss 812 gleiche Vergleiche ab: alle 94 Originaldefinitionen, 96 konstruierte NOTIFY-Pakete, rohe HTTP-Inputs, 68 Originalkonfigurationen, 16 Diagnosekonfigurationen, sieben Szenarien des tatsächlichen Evaluators, vier simulierte Sequenztransporte und native Zuordnungen. Alle 728 SPOP-v4-Ledgereinträge und 50 native Sequenzfixture-Einträge über die erhaltenen Versionen wurden fehlerfrei neu gehasht. Der abgegrenzte Lauf von `git diff --check` bestand.

## Security-Auswirkung

Bestehende Kontrollen für Typen, Framing, Korrelation, ACK-Integrität, endliche Samples, Bodylimits, Isolation und Evidence bleiben erhalten. Metadatenfehler, verwaiste/doppelte ACKs, abgeschnittenes Framing sowie fehlende/zusätzliche native Aufrufe behalten ihre tatsächlichen Ergebnisse. Simulierte Transporte starten keine Hosts. Produkt, Common, gemeinsame Captures, zentrale Matrizen, Framework und MRTS bleiben unverändert.

## Runtime-Evidence

Externes Evidenceverzeichnis: `/var/tmp/codex/ModSecurity-conector/runs/i12-haproxy-415-acceptance-20261015/sonar-spop-sequences-20261018`. `verification-final.json` enthält exakte argv, Exits, Interpreter, vorherige/nachherige Quellhashes und Diffhash; `parity-v3.json` enthält die 812 Gleichheitsprüfungen einschließlich tatsächlicher Socket-Close-Aufrufzahlen; `native-frozen-integrity-final.json` erfasst die frische erneute Prüfung nativer Fixturehashes; `native-frozen-integrity.json` enthält die einzelnen nativen Fixturehashes. Vorherige/nachherige Quellkopien, Testausgabe, `source-final.diff` und das ausführbare Paritätsverfahren bleiben erhalten. Die erste Paritätsberichtsserialisierung konnte Bytes in einem Rückgabetupel nicht serialisieren; das erste Skript bleibt erhalten, Version 2 korrigiert ausschließlich die Berichtsserialisierung und verwendet neue Ausgabeverzeichnisse. Kein Host wurde ausgeführt und keine Lifecycle-Anrechnung vergeben.

Eine abschließende Quellprüfung fand eine nicht committete Refaktorierungsregression: Das Schließen eines nicht wiederverwendeten Sockets in `drive_item` vor dem Surplus-Fehler ließ im Aufrufer die alte Referenz bestehen, sodass `finally` erneut schloss. Die erste Paritätsprüfung erfasste nur den geschlossenen Boolzustand und übersah den doppelten Aufruf. Der korrigierte Treiber übernimmt die erfasste Antwort, weist das Freigabeergebnis im Aufrufer zu und prüft danach separat auf überzählige Bytes; Ownership und bisherige Exceptionreihenfolge bleiben erhalten. Die neue Close-Aufrufregression schlägt gegen die aufbewahrte erste Refaktorierung fehl (Exit 1) und besteht mit der Korrektur. Normale unabhängige Verbindungen, Keepalive-EOF und der Surplus-Exceptionpfad prüfen genau einen Close-Aufruf. Alle 812 Paritätsvergleiche wurden mit Close-Aufrufzahlen wiederholt. Aus keinem Ergebnis folgt eine Hostqualifikation.

## Bekannte Einschränkungen

Die geänderten ausführbaren Quelldateien haben neue Quellhashes. Bestehende versiegelte Quellkopien und jede geprüfte Fixture-Datei bleiben unberührt; keine Fixture-Neugenerierung war erforderlich. Der Paritätsnachweis vergleicht erzeugte Inputs und Komponentenbeobachtungen und belegt keinen echten HAProxy- oder nativen Lifecycle-Lauf.

## Verbleibende Risiken

Root muss frische Sonar-Analyse/Readback und die üblichen Lieferprüfungen ausführen. Spätere Host-Evidence muss ihren tatsächlichen ausführbaren Snapshot und Produktstand binden; diese Komponentenresultate dürfen nicht als neue Hostläufe übertragen werden.

## Nicht ausgeführte Prüfungen mit Begründung

Dieser abgegrenzte Remediation-Worker führte keinen neuen Host, Produktbuild, Sanitizerlauf, keine Controllerzulassung, Sonarübermittlung oder vollständige CI aus. Root verantwortet diese unabhängigen Prüfungen und die Git-Lieferung.

## Finaler Diff- und Review-Status

Die vier zugewiesenen Dateien und dieses EN/DE-Paar wurden gegen die erfassten vorherigen Quellen geprüft. Fokussierte Tests und Byteparitätsprüfungen bestanden. Änderungen anderer Worker blieben erhalten. Frischer Remote-Sonarstatus und Lieferung stehen aus; es wurde keine Git-Schreiboperation ausgeführt.
