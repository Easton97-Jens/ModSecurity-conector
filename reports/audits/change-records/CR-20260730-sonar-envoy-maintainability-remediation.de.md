# Änderungsnachweis: Parent-Envoy-Maintainability-Bereinigung

**Sprache:** [English](CR-20260730-sonar-envoy-maintainability-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260730-sonar-envoy-maintainability-remediation` |
| Datum (UTC) | 2026-07-30 |
| Basis-Revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Tracking | 16 aktuelle SonarQube-Cloud-Maintainability-Zeilen unter `connectors/envoy/`: `shelldre:S1192` ×2, `go:S3776` ×5, `c:S107` ×1, `godre:S8193` ×3, `godre:S8196` ×1, `go:S1186` ×1 und `godre:S8242` ×1. |
| Grenze | Nur Parent-Envoy-ext_proc-Service, C-Bridge, Testcode, Runtime-Harness und dieses deutsch/englische Change-Record-/Index-Paar. |

## Motivation und Problemstellung

Die aktuelle Envoy-Komponente meldet sechzehn Maintainability-Befunde. Es
handelt sich um wiederholte feste Harness-Literale, Lifecycle-Methoden mit zu
hoher Komplexität, einen C-Bridge-Body-Aufruf mit zu vielen unabhängigen
Argumenten sowie kleine Go-API- und Testcode-Hygiene-Befunde. Die öffentliche
Komponentenansicht enthält außerdem eine `python:S5332`-Security-Zeile für den
Standardbibliotheks-Fixture-Server.

## Akzeptanzkriterien

- Für alle sechzehn genannten Maintainability-Zeilen gibt es fokussierte
  Source-Änderungen ohne Scanner-Suppression oder Quality-Gate-Änderung.
- gRPC-Receive, Abbruch, EOF, Sendefehler, Response-Commit und Host-Action
  bleiben durch die Processor-Tests abgedeckt.
- Die geänderte native Bridge baut als C17 mit `-Wall -Wextra -Werror` gegen
  die installierten libmodsecurity-Header und -Bibliothek.
- Die vorhandenen Security-Kontrollen für festes Loopback-TLS und private
  Runtime-Roots bestehen weiter ihre legitimen und negativen Contracts.
- Der ausgelieferte PR erhält frische SHA-gebundene GitHub- und SonarQube-Cloud-
  Evidenz vor jeder Merge-Entscheidung.

## Implementierungsentscheidung und Begründung

Der Service delegiert Stream-Receive/-Send-Lifecycle, Header, Body-Limits und
Header-Decoding an kleine, zweckgebundene Hilfen. Damit liegt jede
Zustandsänderung weiter beim bestehenden `streamState`-Owner; Timeout,
Close-Reason und Response-Commit-Grenzen bleiben unverändert. Ein Sendefehler
bei einem abgebrochenen Stream beendet die Verarbeitung weiter ohne
Host-Action-Evidenz zu schreiben.

Die Common-Runtime-Bridge erhält einen typisierten C-Body-Deskriptor statt vier
unabhängiger Body-/Richtungsargumente. Dieser bewahrt Pointer-, Längen-,
Richtungs- und End-of-Stream-Validierung und wird als C17 kompiliert.
Common-Lifecycle-Testfälle sind benannte Hilfen; der Test-gRPC-Stream liefert
sein gefordertes `Context()` über einen Provider statt ein `context.Context`-
Feld zu speichern.

Die zwei festen Shell-Literale haben je einen readonly-Owner. Das optionale
Response-Commit-Interface hat einen verbgerechten Namen, und das leere
`Close` der source-only Transaction beschreibt, warum es keine Ressourcen
besitzt.

Die `python:S5332`-Zeile wird erneut validiert, aber bewusst nicht geändert.
Ihr `ThreadingHTTPServer` ist ein Same-Process-Upstream-Fixture mit fester
Bindung an `127.0.0.1`, nicht der Downstream-Client-Sink. Die vorhandenen
Downstream-Probes akzeptieren nur credential-freies `https://127.0.0.1`,
nutzen einen zertifikatprüfenden TLS-Kontext und erzwingen TLS 1.2 oder neuer.
Der kanonische `FND-SONAR-0001` verbietet eine externe False-Positive-
Disposition ohne aktuelle explizite Nutzerentscheidung. Es gibt keine
Suppression und keinen künstlichen Topologie-Umbau.

## Geänderte Dateien

- `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.h`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_engine.go`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_engine_test.go`
- `connectors/envoy/ext_proc/internal/processor/config.go`
- `connectors/envoy/ext_proc/internal/processor/processor.go`
- `connectors/envoy/ext_proc/internal/processor/processor_test.go`
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh`
- `reports/audits/change-records/README.md`, das deutsche Gegenstück und
  dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `GOWORK=off go test -mod=readonly ./...` in `connectors/envoy/ext_proc` | bestanden. |
| `ENVOY_EXT_PROC_COMMON_TEST=1 sh connectors/envoy/build/build_ext_proc.sh` mit task-eigenem Cache/Build-Root, `/usr/include` und installierter libmodsecurity-`.so` | bestanden; Modulprüfung, C17-Kompilierung, Go-Common-Tests und Binärbuild bestanden. |
| Gebautes Binärprogramm mit `--config connectors/envoy/config/envoy-ext-proc-service.json --check-config` | bestanden. |
| `shellcheck -S error -x connectors/envoy/harness/run_envoy_ext_proc_runtime.sh` | bestanden. |
| `python3 -m unittest tests.test_envoy_transport_hardening_contract` | bestanden: 16 Tests. |
| `git diff --check` | vor dem Record bestanden; wird vor Auslieferung erneut ausgeführt. |

## Security-Auswirkung

Der Refactor bewahrt Request-Isolation, Context-Abbruch, begrenzte Header-/
Body-Prüfungen, native Transaction-Lebensdauer, Response-Commit und
Loopback-TLS-Kontrollen. Es ändern sich keine Pfadannahme, Netzwerkfreigabe,
TLS-Policy, Artifact-Root-Containment, Event-Payload-Policy, Scanner-Regel,
Suppression oder Quality-Gate-Konfiguration. Die fokussierte Source-/Diff-
Prüfung fand keinen neuen Source-to-Sink-Sicherheitskandidaten.

## Runtime-Evidence

Der native Build verwendete die real installierten libmodsecurity-Header und
die Shared Library, kompilierte die Bridge mit strikten C17-Diagnosen und
führte die libmodsecurity-getaggten Common-Runtime-Go-Tests aus. Der
Transport-Contract startete nur temporäre Loopback-Testserver und prüfte
normales TLS-Verhalten zusammen mit privaten Root- und Unsafe-Endpoint-
Negativkontrollen.

## Bekannte Einschränkungen

Es wurden weder die vollständige Envoy-Binär-/Runtime-Matrix noch ein
Produktiv-Deployment, HTTP/2-/HTTP/3-Downstream oder Framework-/MRTS-Tests
ausgeführt. Diese liegen außerhalb dieser fokussierten Parent-Envoy-
Maintainability-Änderung.

## Nicht ausgeführte Prüfungen mit Begründung

Die vollständige Connector-Matrix und ein realer Envoy-Prozess-Smoke wurden
nicht ausgeführt, weil die lokale Umgebung das gepinnte Envoy-Binärprogramm
nicht bereitstellt. Hosted Actions, Review-Status und SonarQube-Cloud-Analyse
sind erst nach Erstellung dieses Draft-PRs am exakten Remote-Head möglich. Der
erste Sandbox-Lauf des Python-Transport-Contracts konnte seine absichtlichen
`127.0.0.1`-Testsockets nicht binden; derselbe unveränderte Test bestand
außerhalb der Sandbox.

## Verbleibende Risiken

Die sechzehn anwendbaren Source-Zeilen sind extern erst geschlossen, wenn die
SonarQube Cloud am aktuellen Head ihre Abwesenheit mit null neuen Issues und
null New-Code-Duplikation bestätigt. Die erneut geprüfte `python:S5332`-
Fixture-Server-Zeile bleibt in SonarQube Cloud offen, bis eine getrennt
autorisierte externe Disposition erfolgt; sie ist kein Source-Defekt dieser
Änderung.

## Finaler Diff- und Review-Status

Der Kandidat bleibt an der Parent-Envoy-Grenze und enthält keine Framework-/
MRTS-/Gitlink-, Workflow-, Dependency-, Scanner-Konfigurations-, Suppression-
oder `master`-Änderung. Zum Zeitpunkt dieses Records bestanden die lokalen
Prüfungen; Auslieferung und SHA-gebundene Hosted-Verifikation sind noch offen,
und es wird kein Merge behauptet.
