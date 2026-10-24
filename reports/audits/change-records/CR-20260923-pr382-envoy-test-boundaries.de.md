# Change Record: Native Envoy-Testgrenzen

**Sprache:** [English](CR-20260923-pr382-envoy-test-boundaries.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260923-pr382-envoy-test-boundaries` |
| Datum (UTC) | `2026-09-23` |
| Basis-Revision | `3c29004b060b461649383cdb0db9996feab51b05` |

## Motivation und Problemstellung

Der native Envoy-Lauf 35847504839, Job 107137107263, baute Common und
libModSecurity und führte die Go-Pakete aus. Drei Tests scheiterten: Eine unsichere
Datei wurde durch umask 077 privat; eine Remove/Create-Fixture konnte dieselbe
Inode wiederverwenden; der Body-Limit-Test erwartete erfolgreiche Bestätigung
nach einer ungültigen Hostbestätigung, obwohl die Transaktion bereits terminal war.

## Akzeptanzkriterien

Gültiges HTTP 413 und Payload-Redaktion weiter prüfen. Ungültige Hostbestätigungen
bleiben dauerhaft Fehler; erste Ursache erhalten, keine doppelten Ereignisse und
keine weitere Request-/Response-Verarbeitung. Unsichere Rechte und unterschiedliche
Ersatzidentität unabhängig von Runner-Defaults herstellen. Keine Produktivprüfung,
Scannereinstellung, Warnung oder Auswahl nativer Tests abschwächen.

## Implementierungsentscheidung und Begründung

Nur den echten Body-Limit-Transaktionsaufbau zwischen getrennten Positiv- und
Negativfällen teilen. Der neue Negativfall prüft wiederholte falsche und korrigierte
Bestätigungen, gesperrte Body-/Header-Verarbeitung und bytegleiche Ereignisausgabe
nach Wiederholungen. Bisherige positive JSONL-Prüfungen bleiben erhalten. Explizites
chmod erzeugt die unsichere Testdatei ohne geänderte Prozess-umask. Rename hält die
alte Inode beim Erzeugen der Ersatzdatei am Leben; die echte Socket-Besitzkontrolle
bleibt unverändert. Keine Produktivquelle oder Abhängigkeit wird geändert.

## Geänderte Dateien

- `connectors/envoy/ext_proc/internal/processor/common_runtime_engine_test.go`
- `connectors/envoy/ext_proc/internal/processor/body_limit_host_action_test.go`
- `connectors/envoy/ext_proc/internal/processor/jsonl_test.go`
- `connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main_test.go`
- Dieser zweisprachige Change Record.

## Ausgeführte Befehle

Geänderter nativer Testhelfer und Aufrufer wurden mit gofmt formatiert.
Die Rekonstruktion des ursprünglichen Aufrufers ergab exakt den veröffentlichten
Git-Blob `540644d88ff07f02bbc8e157497751417edd56a7`; fremder Inhalt blieb erhalten.
Der bestehende Pflichtworkflow führt das Repository-Buildskript mit
`ENVOY_EXT_PROC_COMMON_TEST=1` aus und damit `go test -mod=readonly -tags libmodsecurity -count=1 ./...`.
Frische Ausführungsergebnisse stehen bei Commitvorbereitung aus.

## Security-Auswirkung

Keine akzeptierten Befunde, Ausnahmen, schwächeren Dateirechte, erweiterten
Berechtigungen oder neuen Hostfähigkeiten. Der negative Hostaktionstest wird
strenger statt Erholung nach terminalem Fehler zu erlauben. Testdaten bleiben
in temporären Fixtures.

## Runtime-Evidence

Der dokumentierte fehlgeschlagene Lauf nutzte echte Common-/CGo-/Engine-Integration.
Die neuen Fälle benötigen einen frischen erfolgreichen nativen Lauf, bevor V20
abgeschlossen wird. Sie beweisen weder Client-Bytes, echtes Envoy-Resetverhalten
noch sämtliche anderen Connector-Routen.

## Bekannte Einschränkungen

I09 und I10 bleiben für andere Adapter offen; diese Reparatur entfernt gefundene
Testblocker, nicht alle Implementierungslücken. I11 und I12 behalten getrennte
Abnahmekriterien für physische Ausgaben und Live-Hosts.

## Verbleibende Risiken

Native Integration, vorhandene Quellcodeverträge und exakte Head-Sonar-Befunde
sowie Duplikation erneut prüfen. Der unabhängige Secret-Scan bleibt ungeklärt.

## Nicht ausgeführte Prüfungen mit Begründung

Kein vollständiger nativer Build im Bearbeitungscontainer: Repository-Download
scheiterte dort an fehlender GitHub-DNS-Auflösung. GitHub-APIs bleiben nutzbar;
Remote-CI übernimmt die native Ausführung. Testpräsenz gilt nicht als Erfolg.

## Finaler Diff- und Review-Status

Begrenzte Testreparatur im bestehenden Draft-PR #382. Parallele Apache- und
native CI-Arbeit erhalten. Kein Merge, Master-/Force-Push oder Framework-/MRTS-Eingriff.
