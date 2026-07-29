# Change Record: Parent-Envoy-Runtime-Artefaktbegrenzung und Loopback-TLS

**Sprache:** [English](CR-20260729-sonar-envoy-runtime-artifact-tls-containment.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-envoy-runtime-artifact-tls-containment |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | `964630d34d0b87e9066d03131e445eeb3677956d` |
| Tracking | Fünfzehn aktuelle SonarQube-Cloud-Kandidaten in `connectors/envoy/harness/envoy_smoke_helper.py`: `pythonsecurity:S8703` ×3, `pythonsecurity:S8707` ×6, `python:S5332` ×1 und fünf Cognitive-Complexity-Zeilen. |
| Grenze | Parent-Envoy-Harness, Konfigurationsmaterializer/-template, Connector-Test, erforderliche leserorientierte Dokumentation und gepaarte Change-Record-Indizes. Keine Framework-, MRTS-, Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder `master`-Änderung. |

## Motivation und Problemstellung

Der Envoy-ext_proc-Smoke-Helper akzeptierte CLI-gesteuerte URLs, Host/Port-
Paare und Evidence-Pfade an Netzwerk- und Dateisystem-Sinks. Sein Runner
stellte den Downstream-Listener über Klartext-HTTP bereit. Lexikalische
Absolute-Pfad-Prüfungen beweisen keine Begrenzung auf private Runtime-Roots,
und ein nur auf Loopback beschränkter HTTP-Endpunkt bietet weiterhin weder
Vertraulichkeit noch Integrität des Transports.

## Akzeptanzkriterien

- Jedes vom Helper erzeugte oder gelesene Runtime-Artefakt ist ein absoluter,
  nicht-symlinkender Nachfahre eines verifizierten privaten Runtime-Roots und
  wird durch descriptor-sichere Read-/Write-Operationen verarbeitet.
- Envoy-Smoke-Client-Endpunkte sind credential-freies HTTPS auf exakt
  `127.0.0.1`, verwenden einen zertifikatverifizierenden Client-Kontext und
  verlangen TLS 1.2 oder neuer.
- Der erzeugte Envoy-Listener nutzt das private Zertifikat und den Key des
  jeweiligen Runs; gewöhnliche Phase-, Probe- und Client-Cancel-Evidence bleibt
  payload-frei.
- Bestehende legitime Loopback-Probes, das Phase-4-Barrier-Verhalten und das
  optionale Client-Cancel-Verhalten funktionieren weiterhin in fokussierten
  temporären TLS-Tests.
- Die erzeugte Envoy-1.38-Konfiguration verwendet die aktuellen getypten
  Upstream-HTTP/2- und Admin/FileAccessLog-APIs statt veralteter Felder, ohne
  den Listener zu erweitern oder einen Admin-Access-Log zu persistieren.
- Startup-Readiness-Requests verwenden eine von der an das legitime P1-
  Control gebundenen Transaktionsidentität getrennte ID, sodass Retries keine
  mehrdeutige Completion-Evidence für dieses Control erzeugen können.
- Konfigurationsmaterialisierung, Tests, englische/deutsche Dokumentation und
  die Hosted-Analyse des exakten aktuellen PR-Heads müssen vor einer
  Integration null New-Code-Issues und Duplikatzeilen bewahren.

## Implementierungsentscheidung und Begründung

Der Helper verwendet die Parent-`runtime_path_utils`-Policy für private Roots
wieder und ergänzt No-Follow-Descriptor-Helper für JSON- und JSONL-Artefakte.
Die Pfade `probe`, `client-cancel` und der Phase-4-Client weisen Nicht-
Loopback-, Klartext-, Credential-haltige, fragmentierte und ungültige
Port-Ziele vor einem Netzwerk-Sink ab. Der Runner erzeugt ein eintägiges,
self-signed SAN-Zertifikat ausschließlich unter seinem verifizierten privaten
Root, übergibt es an Envoys Downstream-TLS-Transport-Socket und verwendet das
passende Zertifikat als Python-Client-Trust-Anchor.

Der Standardbibliotheks-Python-Upstream bleibt eine interne Loopback-Fixture
hinter Envoy. Diese Änderung behauptet nicht, dass er eine Produktions-
Upstream-TLS-Topologie modelliert. Die optionale Full-Lifecycle-Evidence-
Übergabe bleibt nur über einen separat verifizierten privaten Output-Root
außerhalb des Checkouts unterstützt; sie akzeptiert niemals einen beliebigen
Output-Pfad.

Die native Envoy-1.38-Validierung zeigte veraltete
`Cluster.http2_protocol_options`, `Admin.access_log_path` und den alten
FileAccessLog-Formatpfad in der gerenderten Konfiguration. Das Template nutzt
jetzt die dokumentierte getypte `HttpProtocolOptions`-Extension für den
ext_proc-gRPC-Upstream sowie ein `FileAccessLog` mit einem leeren aktuellen
Formatfeld nach `/dev/null`. Damit bleiben explizites Upstream-HTTP/2 und das
bisherige Verhalten ohne persistierten Admin-Log erhalten.

Der erste Exact-Head-Rerun zeigte außerdem, dass eine erneut versuchte
Readiness-Probe die P1-Allow-Transaktions-ID wiederverwenden konnte. Der
Evidence-Binder lehnte zwei ansonsten gültige Completions mit derselben ID
korrekt ab. Der Runner nutzt jetzt eine eigene Readiness-ID und -Receipt und
führt danach genau eine dedizierte P1-Allow-Probe für die kausale Bindung aus.

## Geänderte Dateien

- `connectors/envoy/harness/envoy_smoke_helper.py` — Root-begrenzte
  Artefakt-Helper, verifizierte Loopback-TLS-Client-Pfade und kleinere
  Command-/Evidence-Funktionen.
- `connectors/envoy/harness/run_envoy_ext_proc_runtime.sh` — private
  Zertifikatserzeugung, TLS-Listener-Wiring, Root-Argumente für jeden
  Artefakt-tragenden Helper-Aufruf und getrennte Readiness-/P1-Control-
  Identitäten.
- `connectors/envoy/config/envoy-ext-proc-streaming.yaml.in` und
  `connectors/envoy/config/prepare_envoy_ext_proc_config.sh` — erforderliche
  Zertifikat-/Key-Platzhalter, Downstream-TLS-Transport-Socket und aktuelle
  Envoy-1.38-Upstream-/Admin-Logging-Felder.
- `connectors/envoy/Makefile` und `connectors/envoy/build/test_ext_proc.sh` —
  temporäres Zertifikat-/Key-Konfigurations-Wiring und Assertions für die
  erzeugte Konfiguration.
- `tests/test_envoy_transport_hardening_contract.py` — echte temporäre TLS-
  Legitimate-Controls sowie Negativ-Controls für Klartext, Remote-Host,
  Credentials, Outside-Root und Symlink-Nachfahren; zudem fixiert er die
  nicht veraltete Envoy-Template-Form sowie die getrennten Readiness-/P1-
  Transaktionsidentitäten.
- `scripts/generate_compiler_guides.py`, erzeugte englische/deutsche Envoy-
  Compiler-Guides, `examples/envoy/README.md` und
  `examples/envoy/README.de.md` — gültige private TLS-
  Materialisierungsbeispiele.
- Dieses englisch/deutsche Change-Record-Paar und seine gepaarten Indizes.

## Ausgeführte Befehle

| Ausgeführte Kontrolle | Beobachtetes Ergebnis |
| --- | --- |
| Isoliertes `python -m unittest -v` für Envoy-Transport-, Compiler-Guide- und bilinguale Dokumentations-Contracts | bestanden; 54 Tests, darunter zwölf fokussierte Tests für echte temporäre TLS-Probe-, Client-Cancel- und Phase-4-Pfade, negative Endpunkt-/Pfad-Controls, die aktuellen Envoy-1.38-Template-Felder sowie eindeutige Readiness-/P1-Identitäten. |
| `sh -n` auf ext_proc-Runner, Template-Materializer und ext_proc-Testskript | bestanden. |
| Isoliertes `make -C connectors/envoy build-envoy-ext-proc` mit Go 1.26.5 sowie den verifizierten Host-libmodsecurity-Headern/-Library | bestanden; Modulverifikation und die Go-Processor-Pakettests bestanden. |
| Isoliertes `make -C connectors/envoy runtime-smoke-envoy-ext-proc` mit Envoy 1.38.2, der am Parent-Gitlink gepinnten No-CRS-Regeldatei und Loopback-TLS | bestanden; Envoy akzeptierte die erzeugte Konfiguration ohne Deprecation-Diagnostik und die vollständige begrenzte Smoke-Zusammenfassung ist `PASS` / nicht promotet. |
| `make check-envoy-common-adoption` | bestanden. |
| `git diff --check` | bestanden. |

## Security-Auswirkung

Diese Änderung liegt an einer Network-Client-, Local-Listener-,
Filesystem-Artefakt- und Runtime-Evidence-Grenze. Sie entfernt den Klartext-
Client-zu-Envoy-Transport, weist Remote-/Credential-haltige Endpunkte ab und
begrenzt dynamische Artefakte auf private No-Symlink-Roots. TLS-Verifikation
ist explizit (`ssl.PROTOCOL_TLS_CLIENT`, Zertifikatsverifikation, privater
Trust-Anchor und mindestens TLS 1.2). Keine Validierungs-, Logging-, Evidence-,
Quality-Gate- oder CI-Kontrolle wird gelockert.

## Runtime-Evidence

Fokussierte Python-Controls starteten echte lokale TLS-Server mit einem
temporären SAN-Zertifikat und beobachteten die vorgesehenen Client-Pfade.
Zusätzlich wurde der exakte Kandidat mit Go 1.26.5 gegen die verifizierte
Host-libmodsecurity-Installation gebaut und mit dem offiziellen Envoy-1.38.2-
Binary über Loopback-TLS ausgeführt. Die read-only No-CRS-Fixture stammt aus
der am Parent gepinnten Framework-Revision. Envoy akzeptierte die
materialisierte Konfiguration ohne Warning-, Deprecation-, Error- oder Fatal-
Diagnostik. Die begrenzte Runtime beobachtete den legitimen P1-`200`,
gestreamtes `200`, P1/P2/P3-Denials `403`, P3-Redirect `302`, alle Phase-4-
Safe-/Barrier-Controls `200`, Request- und Response-Streaming sowie
`processes_stopped=yes`. Die dedizierte P1-Transaktion hat genau eine normale
Completion. Der Lauf bleibt `common_libmodsecurity_nonpromoted` mit
`capability_promotion=not_permitted`; er behauptet keine Production-Readiness.

## Bekannte Einschränkungen

- Der Smoke ist ein isolierter Loopback-HTTP/1.1-Downstream-Nachweis. Er deckt
  weder Produktionsnetzwerktopologie noch HTTP/2-/HTTP/3-Downstream-Traffic
  oder die vollständige Connector-Matrix ab.
- Die optionale Cancellation-Diagnostik wurde absichtlich nicht ausgeführt und
  weder promotet noch zur Ableitung einer Client-/Upstream-Reset-Ursache
  verwendet.
- Der Framework-Input wird nur lesend an der Parent-gepinnten Revision
  verwendet; diese Änderung modifiziert weder Framework/MRTS noch ersetzt sie
  die Regel-Fixture durch eine lokal erfundene Alternative.

## Verbleibende Risiken

- Vor der Integration muss der neue exakte PR-Head unabhängig bestätigen, dass
  die ausgewählten SonarQube-Cloud-Kandidaten ohne neue Issues oder Duplikate
  entfernt bleiben; der gehostete PR-Status und nicht dieser lokale Record ist
  die Evidence für dieses Gate.
- Zukünftige Envoy-Konfigurationskonsumenten müssen weiterhin Zertifikat- und
  Private-Key-Pfade übergeben; der Materializer weist ihr Fehlen jetzt ab.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Produktionsdeployment, keine vollständige Connector-Matrix, kein
Downstream-HTTP/2-/HTTP/3-Exercise und keine aktivierte Cancellation-
Diagnostik wurden ausgeführt. Jeder dieser Punkte liegt außerhalb dieses
begrenzten Loopback-Nachweises und darf nicht daraus abgeleitet werden. Hosted
Actions, SonarQube-Cloud-Analyse, Review-/Thread-Status und der Merge-Vorgang
bleiben Delivery-Evidence, die unmittelbar vor einer Integration am exakten
aktuellen PR-Head gelesen wird. Dieser Record behauptet kein Ergebnis für
einen künftigen Head und dokumentiert keinen `master`-Merge.

## Hosted-Feedback-Follow-up

Der initiale exakte PR-Head `b4401deec9bce94a806dd56f1cc0215431881f93` erhielt
ein `OK`-SonarQube-Cloud-Quality-Gate mit 0,0 % New-Code-Duplizierung, aber
fünf task-eigene neue Code Smells: zwei duplizierte Literale und drei
Exception-Testformen. Sein push-ausgelöster `scaffold-lint`-Lauf schlug zudem
fehl, weil der erzeugte Envoy-Compiler-Guide die neu verwendeten Platzhalter
`TLS_CERTIFICATE` und `TLS_PRIVATE_KEY` nicht aufführte; die OpenSSL-Tokens
`CN` und `subjectAltName` sind feste Optionsnamen, keine Platzhalter. Der
fokussierte Follow-up extrahiert die Literale, berechnet Exception-Test-
Argumente vorab, dokumentiert die zwei Variablen in beiden erzeugten Guides
und lässt den Placeholder-Test feste OpenSSL-Optionsnamen unterscheiden. Die
52 fokussierten Envoy-Transport-, Compiler-Guide- und Bilingual-Tests bestehen
lokal. Follow-up-Commit `1b6cc0372f6d5b9ba175fc9e22b61e3ba84bd0c5`
absolvierte seinen Exact-Head-Hosted-Zyklus erfolgreich; kein Fehler wurde
erlassen oder als akzeptiert markiert.

## Finaler Diff- und Review-Status

Der Kandidat ist auf den Parent-Envoy-Connector, seine direkten Tests und die
erforderliche bilinguale Traceability/Dokumentation begrenzt. Er enthält keine
Framework-/MRTS-/Gitlink-, Workflow-, Sonar-Konfigurations-, Suppression- oder
`master`-Änderung. Dieser Record erfasst den versionierten Source-/
Dokumentationsumfang, die nicht veraltete Envoy-Konfiguration, lokale
Kontrollen und Runtime-Einschränkungen. Delivery-Evidence wird absichtlich
unmittelbar vor jeder Integration vom exakten aktuellen PR-Head bezogen; sie
wird nicht für spätere Dokumentations- oder Lifecycle-Commits selbst behauptet.
Dieser Change Record dokumentiert keinen `master`-Merge.
