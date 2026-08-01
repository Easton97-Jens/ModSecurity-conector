# Änderungsnachweis: Parent-Envoy-Transaction-Opener-Interfacebenennung

**Sprache:** [English](CR-20260801-sonar-envoy-transaction-opener.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-sonar-envoy-transaction-opener` |
| Datum (UTC) | 2026-08-01 |
| Basis-Revision | `6b4aca18d390363764b96d85cd31969b9bb114a1` |
| Tracking | Aktuelle Envoy-SonarQube-Cloud-Zeile `godre:S8196` `AZ9cRyqvHhV2CayPTP0H` bei `connectors/envoy/ext_proc/internal/processor/processor.go:128`. |
| Grenze | Nur Parent-Envoy-ext_proc-interne-Go-API und dieses deutsch/englische Change-Record-/Index-Paar. Framework, MRTS, Gitlinks, C-Quellen, Protokollkonfiguration, Abhängigkeiten und Workflows bleiben unverändert. |

## Motivation und Problemstellung

Das aktuelle Envoy-SonarQube-Cloud-Inventar enthält eine Maintainability-Zeile.
Sie beanstandet `Engine`, ein internes Ein-Methoden-Interface, dessen einzige
Operation eine Transaktion öffnet, weil sein Name nicht der Go-üblichen
`-er`-Konvention entspricht.

## Akzeptanzkriterien

- Für die getrackte `godre:S8196`-Zeile gibt es eine source-native Korrektur
  ohne Suppression, `NOSONAR`, Regelausschluss, Quality-Gate-Änderung oder
  False-Positive-Disposition.
- Methodensignatur und alle Aufrufer des Interfaces bewahren ihr bisheriges
  Verhalten beim Öffnen einer Transaktion.
- Fokussierte Go-Formatierungs-, Kompilierungs- und Static-Checks bestehen mit
  der gepinnten Modultoolchain.
- Der Draft-PR erhält frische SHA-gebundene GitHub- und SonarQube-Cloud-
  Evidenz vor jeder Merge-Entscheidung.

## Implementierungsentscheidung und Begründung

`processor.Engine` wird zu `processor.TransactionOpener` umbenannt. Der neue
Name beschreibt die bestehende Operation
`Open(context.Context, StreamMetadata)`, erfüllt die Go-Konvention für
Ein-Methoden-Interfaces und bewahrt den exakten Methodensatz. Die fünf
internen typisierten Verwendungen und das Extension-Process-Main-Paket werden
gemeinsam aktualisiert, sodass weder die `CommonRuntimeEngine`-Implementierung
noch der `PassthroughEngine`-Test-Seam einen Adapter oder eine
Verhaltensänderung benötigen.

## Geänderte Dateien

- `connectors/envoy/ext_proc/internal/processor/processor.go`
- `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go`
- `reports/audits/change-records/README.md`, `README.de.md` sowie dieses
  englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

| Befehl oder Verfahren | Ergebnis |
| --- | --- |
| `GOWORK=off GOTOOLCHAIN=go1.26.5 go test -mod=readonly ./...` in `connectors/envoy/ext_proc` mit task-eigenen Go-Caches | bestanden: Das Main-Paket kompilierte und das Processor-Paket bestand. |
| `GOWORK=off GOTOOLCHAIN=go1.26.5 go vet -mod=readonly ./...` in `connectors/envoy/ext_proc` mit denselben task-eigenen Go-Caches | bestanden. |
| `gofmt -d` für die zwei geänderten Go-Dateien | bestanden ohne Ausgabe. |
| Begrenzte Suche nach dem zurückgezogenen `processor.Engine`-Typ | bestanden: Keine verbleibende Envoy-ext_proc-Verwendung; alle sechs erwarteten `TransactionOpener`-Deklarationen und Verwendungen sind vorhanden. |

## Security-Auswirkung

Dies ist eine interne Compile-Time-Typnamen-Korrektur. Sie bewahrt Methodensatz,
CGo-Bridge-Implementierung, Transaktionslebenszyklus, Envoy-gRPC-
Streambehandlung, Request-Metadaten, Response-Commit-Grenze, Konfiguration und
alles netzwerkseitige Verhalten. Sie fügt keine Parser-, Datei-, Prozess-,
Authentifizierungs-, TLS-, Logging-, Dependency-, Scanner- oder CI-
Control-Änderung hinzu.

## Runtime-Evidence

Es wird keine Runtime-Behauptung erhoben. Der paketweite Go-Test kompiliert
Service und Extension-Process-Main-Paket und führt die bestehenden
Processor-Lifecycle-Tests aus; er ist fokussierte Source-/Behavior-Evidence,
aber kein Ersatz für eine native Envoy-Runtime-Matrix.

## Bekannte Einschränkungen

Es wurden weder ein nativer Envoy-Prozess, eine vollständige CRS/MRTS-Matrix
noch HTTP/1.1-, HTTP/2- oder HTTP/3-Runtime-Probes ausgeführt. Diese Dimensionen
werden durch die interne Go-Identifier-Umbenennung nicht beeinflusst; es wird
keine Transportkompatibilitätsbehauptung erhoben.

## Nicht ausgeführte Prüfungen mit Begründung

Der C17-Connector-Build ist nicht anwendbar, da sich weder C-Quellen,
CGo-Bridge noch Compilerkonfiguration geändert haben. Native Envoy-
Runtime-Checks benötigen ein gepinntes Envoy-Binärprogramm und
Komponenteninputs und sind nicht erforderlich, um den unveränderten Go-
Methodensatz festzustellen. Hosted GitHub Actions, Review-Status und
SonarQube-Cloud-Analyse benötigen den exakten Remote-Draft-PR-Head und stehen
noch aus. Der repository-weite Bilingual-Checker ist nur durch 20 bereits
bestehende Links in den nicht populierten Framework-Gitlink blockiert; er
meldete keinen Pair- oder Strukturfehler dieses Change Records.

## Verbleibende Risiken

Die externe SonarQube-Cloud-Zeile ist erst geschlossen, wenn der exakte
Draft-PR-Head ohne task-eigenes neues Issue oder New-Code-Duplizierung
analysiert ist. Die lokalen Paket-Checks ersetzen keine Hosted-Analyse.

## Finaler Diff- und Review-Status

Der Kandidat ist Parent-only und enthält keine Framework-/MRTS-/Gitlink-,
Dependency-, Workflow-, Scanner-Konfigurations-, Suppression- oder
`master`-Änderung. Die fokussierte Source-Validierung bestand. Finaler Diff- /
Security-Review, Commit, Push, Draft-PR und SHA-gebundene Hosted-Verifikation
stehen zum Zeitpunkt des Record-Authorings noch aus.
