# Änderungsnachweis: Parent-Envoy-TLS- und Maintainability-Bereinigung

**Sprache:** [English](CR-20260801-sonar-envoy-tls-maintainability.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-sonar-envoy-tls-maintainability` |
| Datum (UTC) | 2026-08-01 |
| Basis-Revision | `3ff87de53df34cecbc9c6489c858e64bdf3fd198` |
| Tracking | Fünf aktuelle SonarQube-Cloud-Zeilen unter `connectors/envoy/`: `go:S3776` `AZ9cRyqvHhV2CayPTP0G`, `godre:S8193` `AZ9cRyq6HhV2CayPTP0I` und `AZ9cRyq6HhV2CayPTP0J`, `godre:S8196` `AZ9cRyqvHhV2CayPTP0H` sowie `python:S5332` `AZ9MwivX-bUaKQ_zSGAh`. |
| Grenze | Nur Parent-Envoy-Processor, Smoke-Helper, Envoy-Fixture-Konfiguration, fokussierte Parent-Tests und dieses deutsch/englische Change-Record-/Index-Paar. Framework, MRTS und Gitlinks bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle Envoy-Komponente hat vier Maintainability-Zeilen und eine
Security-Zeile. Der Processor-Metadaten-Decoder überschreitet die
Komplexitätsgrenze, ein Ein-Methoden-Interface verwendet nicht die Go-`-er`-
Konvention und zwei testexklusive Werte sind unnötig. Der Upstream-Fixture-
Server akzeptiert noch Klartext-HTTP, obwohl die Downstream-Client-Probes
bereits zertifikatverifiziertes Loopback-HTTPS verlangen.

## Akzeptanzkriterien

- Für alle fünf genannten Zeilen gibt es repository-native Source-Änderungen
  ohne Scanner-Suppression, `NOSONAR`, Quality-Gate-Änderung,
  Regelausschluss oder externe False-Positive-Disposition.
- Request-Pseudoheader-/Attribut-Mapping, begrenzte Metadatenfehler,
  Response-Commit-Bookkeeping und Trailer-Behandlung bewahren ihre bisherige
  Semantik.
- Das Fixture akzeptiert nur TLS-1.2-oder-neuer-Verbindungen mit regulären,
  unter dem Runtime-Root liegenden Zertifikat-/Private-Key-Dateien; Envoy
  validiert dasselbe laufbezogene Zertifikat auf seinem Upstream-Hop.
- Die fokussierten Go-, C17-/Native-, Shell-, TLS-Positiv-, TLS-Klartext-
  Negativ-, Symlink-Negativ- und Dokumentations-Controls bestehen vor der
  Auslieferung.
- Der Draft-PR erhält frische SHA-gebundene GitHub- und SonarQube-Cloud-
  Evidenz vor jeder Merge-Entscheidung.

## Implementierungsentscheidung und Begründung

`requestMetadataFromEnvoy` wendet Text- und Port-Attribute nun über kleine
typisierte Helper und Assignment-Tabellen an. Das Header-Mapping bleibt bei
seinem bisherigen Owner, während die Helper fehlende Werte und dieselben
begrenzten Eingabefehler bewahren. `ResponseCommitter` bezeichnet die
Ein-Methoden-Fähigkeit in der üblichen Go-Form; der bestehende Common-Runtime-
Test prüft diese Assertion weiter. Die zwei Trailer-Assertions werten ihre
Ausdrücke direkt aus.

Der Fixture-Server verwendet nun `http.server.ThreadingHTTPSServer` statt
eines Klartext-HTTP-Servers. Er akzeptiert nur reguläre Zertifikat-/Key-Dateien
unter dem bereits validierten privaten Runtime-Root und setzt TLS 1.2 als
Mindestprotokoll. Beide Envoy-Runtime-Launcher übergeben das ephemere Paar an
das Fixture. Beide lokalen Envoy-Templates konfigurieren `UpstreamTlsContext`
mit dem laufbezogenen Zertifikat als `trusted_ca`, sodass auch der Envoy-zu-
Fixture-Hop verschlüsselt und zertifikatvalidiert ist.

## Geänderte Dateien

- `connectors/envoy/config/envoy-ext-authz-smoke.yaml.in`
- `connectors/envoy/config/envoy-ext-proc-streaming.yaml.in`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_engine_test.go`
- `connectors/envoy/ext_proc/internal/processor/processor.go`
- `connectors/envoy/ext_proc/internal/processor/processor_test.go`
- `connectors/envoy/harness/envoy_smoke_helper.py`
- `connectors/envoy/harness/run_envoy_connector_runtime.sh`
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh`
- `tests/test_envoy_transport_hardening_contract.py`
- `reports/audits/change-records/README.md`, `README.de.md` sowie dieses
  englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

| Befehl oder Verfahren | Ergebnis |
| --- | --- |
| `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_envoy_transport_hardening_contract` | bestanden: 17 Tests, einschließlich regulärem-Datei-Legitimate-Control und Symlink-Alternate-Bypass-Blockierung. |
| `GOWORK=off GOTOOLCHAIN=go1.26.5 go test -mod=readonly ./...` in `connectors/envoy/ext_proc` mit task-eigenem `GOPATH`, `GOMODCACHE` und `GOCACHE` | bestanden. |
| `GOWORK=off GOTOOLCHAIN=go1.26.5 go vet -mod=readonly ./...` in `connectors/envoy/ext_proc` mit denselben task-eigenen Pfaden | bestanden. |
| `ENVOY_EXT_PROC_COMMON_TEST=1 ... CFLAGS=-std=c17 sh connectors/envoy/build/build_ext_proc.sh` mit installierten libmodsecurity-Headern/-Bibliothek und task-eigenen Build-/Cache-Pfaden | bestanden: Modulprüfung, Processor-Tests, strikter C17-Common-Bridge-Build und ext_proc-Binärbuild. |
| `shellcheck -S error -x` und `sh -n` für die zwei geänderten Runtime-Launcher und den ext_proc-Config-Materializer | bestanden. |
| `gofmt -d` für die geänderten Go-Dateien | bestanden ohne Ausgabe. |
| Direkter task-eigener Fixture-Smoke mit `serve-upstream`, einem Ein-Tages-Loopback-Zertifikat und `probe` | bestanden: Der HTTPS-Legitimate-Control lieferte `200`; eine direkte Klartext-`http://127.0.0.1`-Anfrage wurde abgewiesen. |
| `check-bilingual-docs.py` mit dem Repository-Python | nur durch 20 bereits bestehende fehlende Links in den nicht populierten Framework-Gitlink blockiert; kein Record-Pair- oder Strukturfehler dieser Änderung wurde gemeldet. |

## Security-Auswirkung

Die relevante Grenze ist der Envoy-zu-lokales-Fixture-Upstream-Hop. Das Fixture
weist nun Zertifikat-/Key-Pfade außerhalb seines privaten Runtime-Roots oder
über einen finalen Symlink zurück, akzeptiert nur ein reguläres In-Root-Paar
und exponiert keinen Klartext-HTTP-Listener. Die Envoy-Konfiguration vertraut
diesem ephemeren Zertifikat nur für diesen Loopback-Upstream und fügt weder
einen öffentlichen Listener, Redirect, unsicheren TLS-Override,
Pfadannahme, Scanner-Suppression noch eine Quality-Gate-Änderung hinzu. Die
Downstream-HTTPS-only-Probe-Policy, begrenzte Metadatenbehandlung,
Response-Commit-Grenze und Event-Redaction-Controls bleiben erhalten.

## Runtime-Evidence

Es wird keine promotionsfähige Runtime-Evidence erhoben oder beansprucht. Der
task-eigene Loopback-Smoke erzeugte ein selbstsigniertes Zertifikat mit IP SAN
für `127.0.0.1`, startete den geänderten Helper, schloss eine
zertifikatverifizierende HTTPS-Anfrage ab und wies eine Klartext-HTTP-Anfrage
zurück; er ist als fokussierter lokaler Test statt als Ersatz für eine
Envoy-Runtime-Matrix dokumentiert. Der fokussierte Transport-Contract prüft
zudem einen Symlink-Key-Pfad als Alternate-Bypass-Klasse und bewahrt den
gültigen Regular-File-Control.

## Bekannte Einschränkungen

Es wurden weder eine vollständige Envoy-Prozess-/Runtime-Matrix noch ein
Produktiv-Deployment, HTTP/2-/HTTP/3-Downstream, Framework-Test oder MRTS-Test
ausgeführt. Dies ist eine Parent-only-Envoy-lokale Bereinigung; keine dieser
Quellen änderte sich.

## Nicht ausgeführte Prüfungen mit Begründung

Das echte gepinnte Envoy-Binärprogramm ist lokal nicht verfügbar, daher konnte
kein Envoy-Konfigurationslade-/Runtime-Run ausgeführt werden. Die vollständige
Connector-Matrix liegt außerhalb dieser connector-lokalen Source-Änderung.
Hosted GitHub Actions, Review-Status und SonarQube-Cloud-Analyse sind erst
nachdem der Draft-PR an seinem exakten Remote-Head existiert prüfbar. Der
vollständige Bilingual-Checker ist durch 20 bestehende Links in den absichtlich
nicht populierten Framework-Gitlink blockiert; daraus folgt kein Problem dieses
Parent-only-Change-Record-Paars.

## Verbleibende Risiken

Die fünf aktuellen Source-Zeilen sind extern erst geschlossen, wenn
SonarQube Cloud den exakten PR-Head analysiert und kein task-eigenes neues
Issue oder Duplikat meldet. Der lokale TLS-Smoke demonstriert die Helper-
Grenze, ersetzt aber weder die nicht verfügbare gepinnte Envoy-Runtime noch
eine vollständige Transport-Matrix.

## Finaler Diff- und Review-Status

Der Kandidat bleibt an der Parent-Envoy-Grenze. Er enthält keine Framework-/
MRTS-/Gitlink-, Dependency-, Workflow-, Scanner-Konfigurations-, Suppression-
oder `master`-Änderung. Lokale Source- und fokussierte Security-Validierung
sind abgeschlossen. Der Bilingual-Checker erreichte nur seinen bestehenden
Missing-Framework-Link-Blocker; finaler Diff-Review, Commit, Push, Draft-PR
und SHA-gebundene Hosted-Verifikation sind zum Zeitpunkt dieses Records noch
offen.
