# Change Record CR-20260903-security-remediation-open-findings

**Sprache:** [English](CR-20260903-security-remediation-open-findings.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260903-security-remediation-open-findings |
| Datum (UTC) | 2026-09-03 |
| Basis-Revision | 95bc04203455bc74a9cd18fafc6fb5848af2bbb2 |
| Branch | codex/security-remediation-open-findings-20260903 |
| Finaler HEAD_SHA | Dieser Record ist Teil des Delivery-HEAD und kann sein eigenes finales Git-Objekt daher nicht wahrheitsgemäß selbst referenzieren. Der exakte unveränderliche SHA wird nach dem Commit dieses Records in Draft-PR-Metadaten und Delivery-Evidence erfasst. |
| Delivery-Status | Draft PR [#354](https://github.com/Easton97-Jens/ModSecurity-conector/pull/354) ist offen und nicht gemergt. Lokale Remediation und fokussierte Validierung sind abgeschlossen; der Hosted-Runtime-Rerun nach der Korrektur steht noch aus. |

## Motivation und Problemstellung

Die aktuelle origin/master-Basis enthielt weiterhin fünf Parent-eigene Connector-/Runtime-Sicherheitslücken und einen unvollständigen Authorization-Response-Companion-Lebenszyklus. Der zugehörige Envoy-grpc-go-Befund war auf der Basis bereits behoben und wird hier nur verifiziert. Die Remediation ist Parent-only: Framework, MRTS, Gitlinks, CI-Berechtigungen, Dependencies und master bleiben unverändert.

| Befund | Root Cause auf der Basis | Sicherheitsinvariante und Remediation |
| --- | --- | --- |
| A — HAProxy-SPOP-Request-Target | Eine generische 1024-Byte-Kopie konnte length-delimited path/uri-Werte vor der WAF-Inspektion still kürzen. | Ein Request-Target wird bis zum expliziten 4096-Byte-Limit entweder verlustfrei kopiert oder abgewiesen, einschließlich eingebetteter NUL- und Überlimit-Eingaben. |
| B — Event-JSONL-Query-Privacy | Serializer und Integrity-Metadaten verwendeten die rohe URI und konnten Query-Werte in JSONL schreiben. | Die WAF behält die rohe URI; Serialisierung und zugehörige Integrity-Repräsentation verwenden eine query-redigierte URI und markieren die Redaktion. |
| C — NGINX-Callback-Logging | Der native libModSecurity-Callback schrieb ohne Prüfung des effektiven use_error_log in den NGINX-Error-Log-Sink. | modsecurity_use_error_log off unterdrückt diesen Host-Sink, ohne WAF-Verarbeitung oder den unabhängigen Event-JSONL-Pfad auszuschalten. |
| D/E — Traefik-UDS-Transport und Worker | Blockierendes Socket-I/O, unbeschränkte Aufnahme und unsicheres Teardown nach begrenztem Warten konnten hängen, Worker erschöpfen oder Service-State zu früh freigeben. | Eine monotone Deadline je Frame, nonblocking I/O, begrenzte Aufnahme (64 Standard; 256 harte Obergrenze), Shutdown aktiver Sockets und aufgeschobenes einmaliges Cleanup halten den Dienst begrenzt. |
| F — FND-PARENT-1013 Authorization-Companion | Die Basis nutzte unbeschränktes Worker-Warten sowie destruktives Cleanup/abort bei nicht quieszentem Companion-Fehler. | Heap-eigenes Deferred Cleanup erlaubt genau einen Release erst nach Workern und Companion-Quieszenz; konfigurierte Companions bleiben bei fehlgeschlagenem Shutdown quarantänisiert. |
| Envoy-grpc-go-Untergrenze | Auf der Basis bereits behoben. | Keine Dependency-Änderung; die Modulgraph-Verifikation bewahrt google.golang.org/grpc v1.83.1. |

## Akzeptanzkriterien

- Die betroffenen Request-, Event-, Host-Log-, UDS- und Authorization-
  Lifecycle-Pfade erzwingen die Invarianten der Baseline-Tabelle, ohne
  Framework/MRTS oder die bereits behobene Envoy-Dependency zu ändern.
- Fokussierte positive, Grenz- und Negativregressionen bestehen, soweit die
  nötige lokale Host-/Toolchain verfügbar ist.
- Erzeugte Dokumentation bleibt aktuell, englische/deutsche Records bleiben
  gepaart und alle nicht verfügbaren Host- oder Framework-Checks sind explizit
  festgehalten.
- Der resultierende Review-Branch wird ausschließlich als Draft PR geliefert;
  es erfolgt weder Merge noch Default-Branch-Write.

## Implementierungsentscheidung und Begründung

Die Implementierung portiert ausschließlich die auf der aktuellen Basis benötigten Sicherheitskontrollen. Historische breite PRs sind Referenzevidence, keine Merge-Quellen. Der Authorization-Port schließt nicht zugehörige Duplicate-Host-Validierung und SIGPIPE-Strategieänderungen aus. Die NGINX-Konfigurationsreferenz wird aus einer NGINX-spezifischen Metadata-Überschreibung erzeugt, sodass englische/deutsche Dateien und das kanonische Konfigurationsinventar quellenbasiert statt manuell divergent bleiben. Hosted-Lighttpd-Feedback zeigte anschließend, dass zwar der Host-Harness bereits die sichere serialisierte URI und `redacted=true` erwartet, der spätere Parent-Normalizer sie aber noch mit der rohen Query-URI aus dem Wire-Trace verglich. Beide Korrelationsstufen verlangen nun die sichere JSONL-Repräsentation, während rohe Curl-Wire- und korrelierte CRS-Log-Evidence erhalten bleiben.

## Geänderte Dateien

- Common-Runtime und Event-Serialisierung: common/include/msconnector/event.h, common/src/event.c, common/src/integrity_event.c und common/runtime/http_authorization_service.c.
- Connector-Implementierung: connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c, connectors/nginx/src/ngx_http_modsecurity_log.c und connectors/traefik/src/traefik_engine_service.c.
- Fokussierte Regressionen: tests/event_json_query_redaction_test.c, tests/haproxy_spop_request_target_test.c, tests/test_haproxy_spop_request_target.py, tests/http_authorization_service_detached_worker_smoke.c, tests/test_http_authorization_service_worker_contract.py, tests/test_nginx_error_log_callback_contract.py und tests/test_traefik_engine_service_contract.py.
- Lighttpd-Runtime-Redaction-Regression: connectors/lighttpd/harness/run_patched_full_lifecycle.sh, ci/runtime/lifecycle/normalize-with-crs-no-mrts.py, connectors/lighttpd/tests/test_patched_host_contract.py und tests/test_with_crs_no_mrts_runtime.py.
- Quellenbasierte Dokumentation/Inventar: ci/checks/documentation/connector_config_reference.py, examples/nginx/configuration-reference.md, examples/nginx/configuration-reference.de.md und reports/connector-configuration-inventory.json.
- Parent-NGINX-Provenance-Angleichung: ci/provisioning/components/prepare-runtime-components.py, ci/checks/evidence/check-runtime-producer-readiness.py, ci/runtime/broker/nginx_root_broker.py, ci/runtime/broker/protected_nginx_broker_caller.py, die NGINX-Hosted-/Full-Smoke-/Broker-Workflows sowie die gepaarte Compiler-Anleitung.
- Betreiber-Dokumentation: common/docs/transaction-phase-contract.md und .de.md; die README-Paare von connectors/haproxy, nginx und traefik; sowie die README-Paare von examples/traefik.
- Traceability: dieser gepaarte Change Record und die gepaarten Archivindizes.

## Ausgeführte Befehle

| Prüfung | Ergebnis |
| --- | --- |
| HAProxy-executable-Parserregression | Bestanden: 1024-/4096-Byte-path- und uri-Kontrollen, Überlimit- und Embedded-NUL-Ablehnung. |
| HAProxy C17 und ASan/UBSan | Bestanden. |
| Common-JSONL-Redaction-Linktest und ASan/UBSan | Bestanden; rohe WAF-URI bleibt von redigierter JSONL-/Integrity-Ausgabe getrennt. |
| Common-Security-Contract | Bestanden. |
| NGINX-Callback-, Phase-Runner- und Upstream-Security-Contracts | Bestanden: 23 Tests (3 übersprungen). |
| NGINX-generated-reference- und fokussierte Contract-Tests | Bestanden: 5 Tests; make check-connector-config-reference bestanden. |
| NGINX-C17-Host-Kompilierung | Blockiert: Diese Umgebung enthält keine NGINX-Header/-Quellen; keine Header-Installation und keine Host-Emulation erfolgte. |
| Authorization-Timeout, Detached-Worker-Smoke, dynamisches Response-Companion-Lifecycle-Fixture, ASan/UBSan und TSan | Bestanden. Das dynamische Fixture beweist den Hold vor Companion-Quieszenz, Quarantäne bei fehlgeschlagenem Shutdown, genau einen Release nach Drain, den Single-Winner-Release bei konkurrierendem Owner/Worker sowie den No-Companion-Deferred-Fall. |
| Envoy-Modulgraph, Go-Test und Go-vet | Bestanden; Modulgraph meldet google.golang.org/grpc v1.83.1. |
| Traefik-Contracts/native-plugin/Authorization-Worker-Contracts | Bestanden: 47 Tests. |
| Traefik-C17-Syntax und Engine-Service-Build/Selbsttest/Runtime/Negativtest | Bestanden mit GCC- und Clang-Syntaxchecks; normale, ASan/UBSan- und TSan-Engine-Service-Läufe bestanden. |
| Lighttpd-JSONL-Redaction-Host-/Normalizer-Contract | Bestanden: 62 fokussierte Tests und `bash -n`. Der Host-Harness verlangt `/?<redacted>` mit `redacted=true`; der Parent-Normalizer verwendet nun dieselbe Repräsentation und bindet den Allow-Guard an seine servergenerierte Transaktions-ID. |
| Directive Parity | Bestanden. |
| Vollständige Bilingual-/Link-Checks | Ausschließlich durch vorbestehende fehlende Framework-Submodul-Link-Targets blockiert; die Aufgabe initialisiert oder verändert das Framework nicht. |

## Security-Auswirkung

Die Änderungen reduzieren Request-Target-Ambiguität, Offenlegung von Query-Werten, Umgehungen der Logging-Konfiguration, lokale UDS-Ressourcenerschöpfung und das Risiko asynchroner Use-after-free-/Double-Release-Fehler. Event-JSONL-Redaktion gilt für neu ausgegebene Records; Betreiber müssen historische JSONL- und Audit-Logs als potenziell sensitiv behandeln und nach lokaler Policy beschränken, rotieren oder aufbewahren. Es wurde kein Produktionsdienst kontaktiert und kein echtes Credential, Cookie, Token, Passwort oder personenbezogenes Datum in Tests oder Evidence verwendet.

## Runtime-Evidence

Der lokale Traefik-Engine-Service wurde gebaut und über einen privaten
Unix-Socket für normale, fehlerhafte-Frame- und Socket-Ownership-Negativ-
Kontrollen ausgeführt. Dies ist kein Traefik-Host-Runtime-Test. Es wurde kein
Produktionsdienst kontaktiert.
Die Hosted-Lighttpd-CRS/no-MRTS-Runtime ist die maßgebliche Host-Validierung
für den aktualisierten JSONL-Korrelations-Contract. Der diagnostische Lauf auf
`fe518101` führte den unteren Host-Harness erfolgreich aus, aber der spätere
Parent-Normalizer verglich noch mit der rohen URI; sein Rerun steht für den
nächsten unveränderlichen Draft-PR-Head aus.

## Nicht ausgeführte Prüfungen mit Begründung

NGINX-C17-Host-Kompilierung/-Runtime ist durch fehlende lokale NGINX-
Header/-Quellen blockiert. Vollständige Bilingual- und Link-Checks sind nur
durch vorhandene fehlende Framework-Submodul-Targets blockiert; keine
Framework-Initialisierung oder -Änderung ist autorisiert. Vollständige
HTTP/1.1-, HTTP/2- und HTTP/3-Host-Matrizen benötigen lokale Host-Fixtures, die
nicht vorhanden sind.

## Bekannte Einschränkungen

Ein konfigurierter Authorization-Companion hat statische Lifecycle-Contract-
Abdeckung und ein dynamisches Late-Quiescence-Fixture; das lokale Fixture
bestand die vollständige Release-/Worker-Drain-Matrix, frische Exact-Head-
Hosted-Evidence steht jedoch noch aus. Der lokale Traefik-Service-Test übt
keinen Traefik-Hostprozess aus. Dies sind Evidence-Grenzen, keine Behauptung
deaktivierter Sicherheitskontrollen.

## Verbleibende Risiken

Historische JSONL- und Audit-Records können weiterhin Daten enthalten, die vor
dieser Redaktionsänderung ausgegeben wurden. Der korrigierte Exact-Head-
Lighttpd-Runtime-Rerun, weitere Hosted-CI, Review und jede Merge-Entscheidung
sind separate zukünftige Evidence. Es wird kein Merge angefragt oder
durchgeführt.

## Finaler Diff- und Review-Status

In Bearbeitung, bis der finale Diff nach der Korrektur auf dem Task-Branch
committed und aus Task-Branch und Draft PR zurückgelesen ist. Der aktuelle
Benutzer autorisiert nur einen normalen Task-Branch-Push und Draft PR; Merge,
Force-Push, Rebase veröffentlichten Works und Default-Branch-Writes bleiben
nicht autorisiert.

## Review-Remediation-Follow-up für Draft PR #354 vom 2026-09-03

Dieses Follow-up dokumentiert den angeforderten Review-Durchlauf gegen den
Ausgangs-HEAD
`c44dd04a16cb698584c023e2f81521e07f5c3fb2`. Es behauptet ausdrücklich nicht,
dass der Nachfolge-HEAD bereits gepusht wurde oder Hosted-Checks abgeschlossen
sind.

Die eingegrenzte Remediation und Evidence umfasst:

- RR1 erweitert den Common-Helper zur URI-Query-Redaktion für JSONL um eine
  explizite Truncation-Ausgabe. Der Serializer kombiniert Redaktion und
  Kürzung im sicheren Buffer nun korrekt, einschließlich teilweise gekürzter
  `<redacted>`-Marker, in JSON und JSONL. Tests decken lange Pfade mit und ohne
  Query, das Fehlen von Canary-Daten, `redacted=true`, `truncated=true`,
  unveränderte rohe WAF-URIs und konsistente Integrity-Repräsentation ab.
- RR2/RR4 machen Traefik-Slot-Invalidierung und Descriptor-Schließen zu einer
  gemeinsamen gesperrten Ownership-Operation, schützen Shutdown mit
  `socket_fd >= 0` und ergänzen einen kontrollierten Descriptor-Reuse-/Shutdown-
  Race-Test sowie dynamische `max_workers=2`-Nachweise für Aufnahme,
  Slot-Wiederverwendung, Rollback bei Create-Fehlern und langsame/nicht lesende
  Peers.
- RR3 ergänzt ausführbare HAProxy-Parser-/Mapper-Fälle exakt bei 1023 Bytes
  und setzt einen harmlosen Marker ausschließlich hinter Byte 1023. Damit wird
  die vollständige Boundary-Erreichbarkeit oder eine ausdrückliche Ablehnung
  nachgewiesen, statt nur eine statische Python-Längenschleife zu verwenden.
- RR5 ergänzt ein dynamisches Live-Response-Companion-Fixture für Quieszenz,
  fehlgeschlagenen Shutdown, exakt einmaligen Release nach Worker-Drain,
  konkurrierenden Owner-/Worker-Release sowie den weiterhin funktionierenden
  No-Companion-Deferred-Pfad. FND-PARENT-1013 bleibt bis zur frischen
  Exact-Head-Evidence `fixed, verification pending`.
- Der diagnostische Hosted-Lighttpd-Lauf zeigte nach erfolgreichem
  Host-Harness eine veraltete Roh-URI-Prüfung im Parent-Normalizer. Die
  eingegrenzte Korrektur verwendet in beiden Stufen dieselbe redigierte
  Repräsentation, bindet den Allow-Guard an seine servergenerierte
  Transaktions-ID und bewahrt rohe Wire- und CRS-Evidence.
- Lokale NGINX-Header/-Quellen sind nicht verfügbar. Deshalb ist ein klar
  benanntes `Exact-Head-Hosted`-NGINX-Gate für Kompilierung gegen unterstützte
  Header und einen isolierten `modsecurity_use_error_log`-on/off-Runtime-
  Nachweis erforderlich; ein lokales Host-Ergebnis wird nicht behauptet.

### SonarQube Cloud: zwölf PR-neue Issues einzeln triagiert

Die zwölf für PR #354 gemeldeten Issues wurden am Ausgangs-HEAD einzeln wie
folgt triagiert. Neun werden durch Wartbarkeits-Refactorings oder
Const-Korrekturen behoben; drei öffentliche Test-Stub-Befunde sind fachlich
begründete Nichtprobleme, weil ihre Signaturen zur Produktions-Header-ABI
passen müssen. Es wurden weder `NOSONAR`, Regel-Ausschlüsse,
Schwellenwertänderungen noch eine Quality-Gate-Abschwächung verwendet.

| # | Sonar-Key / Regel | Ort/Issue | Disposition |
|---:|---|---|---|
| 1 | `AaBnPLiUQISHK43ZVdjk` / c:S134 | `common/runtime/http_authorization_service.c` — verschachtelter Deferred-Worker-Ablauf | In einen fokussierten Helper refaktoriert. |
| 2 | `AaBnPLYKQISHK43ZVdjZ` / c:S995 | `tests/http_authorization_service_detached_worker_smoke.c` — Flag-Parameter | Durch Const-Pointer für das Wait-Flag behoben. |
| 3 | `AaBnPLYKQISHK43ZVdja` / c:S995 | Öffentlicher Authorization-Test-Runtime-Stub — Parameter-Constness | Nichtproblem: Produktions-Header-ABI erfordert die nicht-const Signatur. |
| 4 | `AaBnPLYKQISHK43ZVdjb` / c:S995 | Öffentlicher Authorization-Test-Runtime-Stub — Parameter-Constness | Nichtproblem: Produktions-Header-ABI erfordert die nicht-const Signatur. |
| 5 | `AaBnPLYKQISHK43ZVdjc` / c:S995 | Öffentlicher Authorization-Test-Runtime-Stub — Parameter-Constness | Nichtproblem: Produktions-Header-ABI erfordert die nicht-const Signatur. |
| 6 | `AaBnPLhlQISHK43ZVdjd` / c:S3776 | Traefik-Send-Deadline | Deadline-/Poll-Logik in begrenzte Helper refaktoriert. |
| 7 | `AaBnPLhlQISHK43ZVdje` / c:S134 | Traefik-Send-Pfad — verschachtelter Kontrollfluss | Durch den fokussierten Send-/Wait-Helper-Refactor entfernt. |
| 8 | `AaBnPLhlQISHK43ZVdjf` / c:S134 | Traefik-Send-Pfad — verschachtelter Kontrollfluss | Durch denselben fokussierten Send-/Wait-Helper-Refactor entfernt. |
| 9 | `AaBnPLhlQISHK43ZVdjg` / c:S3776 | Traefik-Receive-Schleife | In gemeinsame begrenzte Wait-/Deadline-Helper refaktoriert. |
| 10 | `AaBnPLhlQISHK43ZVdjh` / c:S995 | Traefik-Shutdown-Helper-Service-Parameter | Durch einen const Service-Parameter behoben. |
| 11 | `AaBnPLhlQISHK43ZVdji` / c:S3776 | Traefik-Serve-Orchestrierung | Lifecycle-Setup, Runtime-Konfiguration, Handler und Abschluss aufgeteilt. |
| 12 | `AaBnPLhlQISHK43ZVdjj` / c:S3776 | Traefik-CLI-Parsing | Switch-/Value-Parsing aufgeteilt und fail-closed Validierung beibehalten. |

### Sonar-Nachverfolgung für den Exact-Head-Nachfolger

Der SonarCloud-Check `100738129438` analysierte den Nachfolger
`fe518101c7c19ee29dba8be165f9356f5acfe78f` und schlug ausschließlich wegen
der New-Code-Sicherheitsbewertung `D` fehl. Die zwölf unten neu zugeordneten
Meldungen wurden einzeln geprüft. Die acht `c:S5443`-Meldungen sind keine
erreichbaren Operationen in öffentlich beschreibbaren Verzeichnissen: Dieses
reine Parser-Fixture öffnet, bindet, erzeugt oder schreibt keinen übergebenen
Pfad. Seine inerten `/tmp`-Literale werden dennoch durch nicht-dateisystemische
Sentinel-Namen ersetzt, damit der Test keine unsichere Verzeichnisnutzung
modelliert. Der `c:S108`-Retry wird erläutert. Die drei `c:S995`-Meldungen
bleiben die einzigen dokumentierten Nichtprobleme: Ihre Test-Stubs
implementieren öffentliche Runtime-ABI-Deklarationen, deren mutable
Pointer-Typen nicht ohne ABI-Änderung const werden können.

| # | Sonar-Key / Regel | Ort/Issue | Disposition |
|---:|---|---|---|
| 1 | `AaBoE29gD03N4v8H0Ojv` / c:S5443 | Traefik-CLI, gültiges Config-Literal, Zeile 214 | Inerte `/tmp`-Schreibweise durch `engine.conf` ersetzt; Parser-Coverage bleibt unverändert. |
| 2 | `AaBoE29gD03N4v8H0Ojw` / c:S5443 | Traefik-CLI, gültiges Socket-Literal, Zeile 215 | Inerte `/tmp`-Schreibweise durch `engine.sock` ersetzt; dieser Test führt keine Dateisystemoperation aus. |
| 3 | `AaBoE29gD03N4v8H0Ojx` / c:S5443 | Traefik-CLI, Config-Literal ohne Wert, Zeile 218 | Durch das nicht-dateisystemische Config-Sentinel ersetzt. |
| 4 | `AaBoE29gD03N4v8H0Ojy` / c:S5443 | Traefik-CLI, Socket-Literal ohne Wert, Zeile 219 | Durch das nicht-dateisystemische Socket-Sentinel ersetzt. |
| 5 | `AaBoE29gD03N4v8H0Ojz` / c:S5443 | Traefik-CLI, Config-Literal für null Worker, Zeile 222 | Durch das nicht-dateisystemische Config-Sentinel ersetzt. |
| 6 | `AaBoE29gD03N4v8H0Oj0` / c:S5443 | Traefik-CLI, Socket-Literal für null Worker, Zeile 223 | Durch das nicht-dateisystemische Socket-Sentinel ersetzt. |
| 7 | `AaBoE29gD03N4v8H0Oj1` / c:S5443 | Traefik-CLI, Config-Literal für Überlauf, Zeile 226 | Durch das nicht-dateisystemische Config-Sentinel ersetzt. |
| 8 | `AaBoE29gD03N4v8H0Oj2` / c:S5443 | Traefik-CLI, Socket-Literal für Überlauf, Zeile 227 | Durch das nicht-dateisystemische Socket-Sentinel ersetzt. |
| 9 | `AaBoE29gD03N4v8H0Oju` / c:S108 | Traefik-EINTR-Sleep-Retry, Zeile 41 | Kommentar zum Retry-Zweck ergänzt; Verhalten bleibt unverändert. |
| 10 | `AaBnPLYKQISHK43ZVdja` / c:S995 | Authorization-Fixture, Runtime-Setter, Zeile 99 | Nichtproblem: Signatur muss zur öffentlichen ABI mit mutable Pointer passen. |
| 11 | `AaBnPLYKQISHK43ZVdjb` / c:S995 | Authorization-Fixture, Profil-Setter, Zeile 112 | Nichtproblem: Signatur muss zur öffentlichen ABI mit mutable Pointer passen. |
| 12 | `AaBnPLYKQISHK43ZVdjc` / c:S995 | Authorization-Fixture, Transaction-Beginn, Zeile 194 | Nichtproblem: Signatur muss zur öffentlichen ABI mit mutable Pointer passen. |

Der daraus entstehende Nachfolge-Commit, GitHub-Read-back, die frische
Sonar-Analyse, der vollständige Exact-Head-Runtime-Workflow einschließlich
Hosted-NGINX-Gate sowie der abschließende Read-back von PR-Beschreibung und
Change Record stehen zum Zeitpunkt dieses Eintrags noch aus. Es wird weder ein
Merge, Force-Push, Framework-/MRTS-/Gitlink-Change noch eine Abschwächung von
Tests oder Workflows autorisiert oder behauptet.

### Wiederholung des Exact-Head-NGINX-Gates

Das erste gehostete NGINX-Gate auf dem Successor-Head erreichte den echten
Provisioning-Schritt, endete jedoch vor einem Host-Build mit dem vom Framework
verwendeten Status `77`. Sein Workflow hatte das aggregierte Default für
Runtime-Komponenten aufgerufen, das nicht benötigte Aggregateingaben verlangt.
Die begrenzte Wiederholung wählt explizit `RUNTIME_COMPONENT_TARGET=nginx` und
erteilt der vorhandenen Runtime-Vorbereitung die erforderlichen Build-/Download-
Capability-Flags; sie erweitert weder das Target noch schwächt sie einen
Control ab. Die aktualisierten statischen Gate-Contracts und `actionlint`
bestehen. Ein neuer unveränderlicher PR-Head und ein neuer Hosted-Run sind
weiterhin erforderlich, bevor NGINX-Compile- oder On/Off-Runtime-Evidenz
behauptet wird.

### Angleichung der Exact-Head-NGINX-Provenance

Die begrenzte Wiederholung erreichte anschließend die aktuelle
Framework-Provenance-Guard und endete korrekterweise mit Status `77`, bevor
ein Download oder Build erfolgen konnte: Der unveränderliche Framework-Gitlink
`86451b45ae7bb7953baf9f81f2c2dad07395a808` wählt kanonisch
`release-1.31.4`, `nginx-1.31.4.tar.gz` und
`e6f20b644a17a643f059ae6467a1971fe2811587d025e071068753a1f1e3b3c3`, während
die Parent-Consumer noch das abgelöste `1.31.3`-Tuple verlangten. Dieser
Successor gleicht ausschließlich Parent-Provenance-Consumer,
Exact-Head-/Full-Smoke-/Broker-Deklarationen, die gepaarte Betreiber-Doku und
ihre direkten Tests an dieses bereits gepinnte Framework-Tuple an. Die
strikten Tag-/Ref-/Asset-/Digest- und Runtime-Readback-Prüfungen bleiben
fail-closed; Framework, MRTS und Gitlink bleiben unverändert. Für den neuen
unveränderlichen Head sind weiterhin frische Hosted-Compile- und
On/Off-Evidence erforderlich.

### Isolation nativer NGINX-Overrides im Exact-Head-Gate

Der Hosted-Retry auf `fe518101` bestand seine Exact-Head- und
Pinned-Provenance-Prüfungen, stoppte jedoch vor dem Host-Build mit
`missing_nginx_modsecurity_module`. Der Provisioner hatte einen geerbten
nativen NGINX-Modulverzeichnis-Override erhalten, der bei erforderlicher
gepinnter Provenance verboten ist und das verwaltete Modul nicht enthielt.
Das Gate löscht nun ausschließlich geerbte native NGINX-Artefakt-Overrides
sowohl beim Provisioning als auch beim anschließenden Runtime-Wrapper, damit
der vorhandene verwaltete Cache-Plan das Parent-NGINX-Modul baut und
validiert. Dies akzeptiert weder ein fehlendes Modul noch verändert es MRTS,
Framework, Gitlink, Release-Tuple oder Runtime-Provenance-Prüfungen. Der
statische Gate-Contract prüft jeden gelöschten Override an beiden
Prozessgrenzen; frische Exact-Head-Hosted-Compile- und On/Off-Runtime-Evidence
bleibt erforderlich.

### Korrektur der Exact-Head-NGINX-Fehlerdiagnosegrenze

Der reine Diagnose-Nachfolger `c5073a9ef3466c879cb5e352fe256ddeb8e88e75`
führte einen getrennten CI-Trust-Boundary-Fehler ein: Nachdem
PR-kontrollierter Provisioning-Code gelaufen war, vertraute sein
`if: failure()`-Helper veränderbaren `GITHUB_ENV`-Wurzeln und vom Report
ausgewählten Pfaden. Er konnte eine vom Runner lesbare Datei offenlegen, einen
unbegrenzten Report/Log laden oder Terminal-/Workflow-Command-Text ausgeben.
Seine gehosteten NGINX- und Complete-Runtime-Läufe wurden abgebrochen und sind
keine Evidenz für einen späteren Head.

Die eingegrenzte Parent-only-Korrektur leitet die einzige Diagnosewurzel aus
dem unveränderlichen `${{ runner.temp }}`-Kontext ab, startet einen isolierten
Python-Helper mit leerer Environment und erlaubt nur feste Report- und
NGINX-Build-Log-Nachfahren, die über No-Follow-Descriptor-Walks geöffnet
werden. Sie verwirft Symlinks, Hardlinks, Ersetzungsrennen,
fehlerhafte/übergroße Eingaben und nicht vertrauenswürdige Log-Auswahlen;
ausgegebene Metadaten/Tail-Zeilen sind begrenzt und terminalsanitisiert. Das
bereits fehlgeschlagene Provisioning-Ergebnis bleibt maßgeblich. Zweiundvierzig
fokussierte dynamische CI-/Workflow-/Helper-Tests, Python-Kompilierung,
`actionlint` und Diff-Checks bestehen lokal. Ein neuer normaler
Successor-Head, exakter Remote-/PR-Read-back sowie frische
Successor-only-Sonar-, NGINX-On/Off- und Full-CRS/no-MRTS-Workflow-Evidenz
bleiben erforderlich; kein früherer grüner Lauf wird wiederverwendet.

### Exact-Head-NGINX-Diagnose-Kompatibilität und Sonar-Korrektur

Der Exact-Head-Hosted-Lauf `33800744562` für
`4350a8a77c61630025ba436cda12dfac6b3751e2` beließ das fehlgeschlagene
Provisioning-Ergebnis (`missing_nginx_modsecurity_module`) korrekterweise als
maßgeblich und führte den begrenzten Diagnoseschritt aus. Dieser Schritt
meldete `report_too_large`: Der normale vollständige generierte Komponenten-
Report ist ungefähr 120,601 Byte groß und überschreitet die absichtlich
beibehaltene 64-KiB-Metadaten-Grenze, sodass der separat erzeugte feste
NGINX-Build-Log-Tail nicht erreicht wurde.

Der eingegrenzte Successor-Kandidat behält diese Report-Grenze bei, parst
keinen abgeschnittenen Report und vertraut dessen `build_log`-Wert nicht. Nur
für das explizite Ergebnis `report_too_large` gibt er diesen Status aus und
liest anschließend den unabhängig festen Pfad
`build/logs/runtime-components/nginx-build.log` über denselben no-follow-,
identitätsgeprüften und begrenzten Reader. Das Regression-Fixture platziert
einen gefälschten Log-Pfad und Canaries im übergroßen Report und beweist, dass
nur der feste kanonische Tail gerendert wird. Symlink-/Hardlink-/Race-
Verwerfung, 64-KiB-Tail-Grenzen, Zeilenlimits und Terminal-/Actions-Command-
Sanitisierung bleiben erhalten.

Das aktuelle SonarQube-Cloud-PR-Ergebnis hat vier offene Records: Der neue
`python:S3776`-Komplexitätsbefund des Diagnose-Readers ist ein echtes
Wartbarkeitsproblem; der Kandidat trennt Descriptor-Traversierung, Öffnen
regulärer Dateien und begrenztes Lesen, ohne deren Sicherheitsinvarianten zu
ändern. Die drei verbleibenden `c:S995`-Authorization-Fixture-Zeilen bleiben
die oben bereits dokumentierten Nichtprobleme der öffentlichen ABI. Es werden
weder Suppression, `NOSONAR`, Quality-Gate-Änderung noch Workflow-/Test-
Abschwächung verwendet. Python-Kompilierung und die 42 fokussierten
Diagnose-/Gate-/CI-Sicherheits-Tests bestehen lokal; ein neuer normaler Head,
exakter Remote-Read-back und Successor-only-Sonar-, NGINX-On/Off- sowie Full-
CRS/no-MRTS-Evidenz bleiben erforderlich.

### Exact-Head-NGINX-Non-H3-QUIC-TLS-Übergabe

Der Exact-Head-Hosted-Lauf `33803351249` für
`79156cb550eebf76c52add7a2059379ee2d8df90` erreichte die gepinnte
NGINX-Build-Grenze, stoppte jedoch korrekterweise vor Configure mit `BLOCKED:
NGINX_QUIC_TLS_VERSION override is not permitted`. Der begrenzte
Diagnose-Fallback legte diesen primären Blocker sicher offen; das spätere
Mapping `missing_nginx_modsecurity_module` war nachgelagert, weil noch kein
Modul-Build begonnen hatte. Der Complete-CRS/no-MRTS-Lauf `33803351191` bestand
für denselben Head seine fünf Nicht-NGINX-Connector-Jobs, kann aber keinen
Nachfolge-Head validieren.

Die Parent-Source-Korrektur schwächt weder den Framework-Provenance-Guard noch
sein QUIC-TLS-Tupel ab. Für H1/H1-H2 werden profilspezifische
`not_used`-/leere Fakten nicht mehr als Environment-Pin-Overrides weitergereicht,
sodass die aus Framework `common.sh` geladenen kanonischen Werte die nächste
geschützte Source-Grenze überstehen. H3 ersetzt diese Felder weiterhin durch
sein aufgelöstes geprüftes Tupel. Ein leerer oder nicht kanonischer geerbter
Pin bleibt damit an der unveränderten Framework-Grenze fail-closed.

Fokussierte dynamische Tests beweisen nun die Bewahrung der kanonischen
H1/H1-H2-Child-Environment, den H3-Ersatz durch das geprüfte Tupel und den
tatsächlichen gemockten NGINX-Preparation-Pfad. Python-Kompilierung, 78
Parent-Komponenten-Tests (fünf bestehende Framework-Head-Skips), alle 45
NGINX-Cache-Contract-Tests, die 64 Bilingual-/NGINX-Gate-/CI-Security- /
Diagnose-Tests, `actionlint` und `git diff --check` bestehen lokal. Ein
unabhängiges Post-Patch-Security-Review bestand und fand keinen Bypass und
keine Regression. Ein neuer normaler Exact-Head-Successor bleibt erforderlich,
bevor Kompilierung gegen unterstützte Header oder
`modsecurity_use_error_log`-on/off-Runtime-Evidenz behauptet wird; exakter
Remote-Read-back und Successor-only-Sonar-, NGINX-On/Off- sowie Full-
CRS/no-MRTS-Evidenz bleiben ebenfalls erforderlich.

### Exact-Head-NGINX-Make-Log-Evidence-Handoff

Der Exact-Head-Hosted-Lauf `33807403800` für
`810b0df3c1a83af2cedc6a2b3a84a4fe60df2c5b` bestand Exact-Head- und
Pinned-Provenance-Prüfungen und erreichte den echten Schritt `make -j4`. Der
Build schlug fehl, aber die vorherige begrenzte äußere Diagnose bewahrte nur
den Fehler auf Kommandoebene und nicht die zur Klassifizierung benötigte
Compiler-/Linker-Zeile. Aus diesem Lauf werden weder ein erfolgreicher Compile
noch `modsecurity_use_error_log`-on/off-Runtime-Evidence behauptet.

Die eingegrenzte Parent-only-Nachbesserung lässt den fehlgeschlagenen Build
maßgeblich und leitet vor dem transaktionalen Staging-Cleanup ausschließlich
den festen verwalteten Pfad `build/logs/nginx/nginx-make.log` ab. Sie verlangt
den aktuellen `connector:nginx`-Marker, Cache-Key, Cache-Root und die exakte
`staging_root/build`-Identität; sie verwendet weder einen report-ausgewählten
Pfad noch eine veränderliche Environment-Root. Der feste Nachfahre wird über
No-Follow-Deskriptoren mit Directory-/File-Identitätsprüfungen geöffnet.
Path-Escape-, Symlink-, Hardlink- und Ersetzungsrennen-Eingaben werden
verworfen; übergroße Inhalte werden auf einen 64-KiB-Tail begrenzt; und die
erhaltene Repräsentation wird terminal- und Actions-Command-sanitisiert, bevor
sie an das bestehende feste äußere Log angehängt wird. Der längere Staging-
Zeilenpräfix ist im 512-Zeichen-Zeilenbudget enthalten. Framework, MRTS,
Gitlink, Provenance-, Test- und Workflow-Kontrollen bleiben unverändert. Ein
Fehler bei der Staging-Root-Auflösung ist fail-soft und kann das primäre
fehlgeschlagene Build-Ergebnis nicht ersetzen.

Die fokussierte lokale Validierung deckt Managed-Identity-Abweichung, einen
fehlenden Inner-Log, Path-Escape, Symlink-/Hardlink-Verwerfung,
Ersetzungsrennen, begrenzte Tails, das vollständige Staging-Zeilenlimit und
Terminal-/Actions-Command-Sanitisierung sowie Symlink-Schleifen-Auflösung ab.
Sie beweist außerdem, dass das
Anhängen den primären fehlgeschlagenen Build-Exit-Code, Failed-Status und das
Blocker-Mapping maßgeblich lässt. Python-Kompilierung, 81
Parent-Komponenten-Tests mit fünf bestehenden Framework-Head-Skips, 11
NGINX-Diagnose-Tests, `git diff --check` und ein unabhängiges
Post-Patch-Security-Review bestehen. Ein frischer normaler Successor-Head und
ein Exact-Head-Hosted-Rerun bleiben erforderlich, bevor Kompilierung gegen
unterstützte Header oder isolierte `modsecurity_use_error_log`-on/off-Runtime-
Evidence behauptet wird.

### NGINX-Profile-Registry-Materialisierungsbehebung

Der Exact-Head-NGINX-Lauf `33813265768` auf
`896a7dd94421bd47d1078cf4360c463be3fa1a14` verifizierte die begrenzte
Make-Log-Übergabe, indem er den frühesten Compilerfehler bewahrte. Er legte
zugleich einen getrennten fail-closed Parent-Builddefekt offen: Der
materialisierte NGINX-Tree ließ die kanonische Eingabe
`connectors/profile_registry.h` aus, und beide dynamischen/statischen
Source-Listen ließen `connectors/profile_registry.c` aus. Dieses getrennte
Problem wird als `FND-PARENT-1030` verfolgt; `FND-PARENT-1028` ist nur für
seine Diagnoseübergabe verifiziert, nicht als NGINX-Host-Build-Nachweis.

Die lokale Behebung bindet beide Registry-Dateien an den NGINX-Cache-Source-
Hash, stagt sie unter der verwalteten Build-Root, übergibt nur diese gestagte
Root an die Child-Environment und deklariert Quelle, Header und Include-Root
in beiden NGINX-Konfigurationszweigen. Das Staging verwendet descriptor-
relative `O_NOFOLLOW`-Directory-/File-Opens, reguläre Single-Link-Source-
Prüfungen vor und nach dem Öffnen, größenexaktes Kopieren,
descriptor-relative temporäre Dateien und atomaren Ersatz. Damit können eine
beliebig geerbte Registry-Root, Source-Ersetzung, Hardlink-Eingabe und
Destination-Symlink/-Ersetzung den verwalteten Build nicht unbemerkt
beeinflussen. Der Direct-Checkout-Fallback bleibt ausdrücklich dokumentiert
und gilt nicht für einen kopierten Adapter-Tree.

Frische lokale Validierung bestand mit 88 Preparation-Cases mit fünf
bestehenden Framework-Head-Skips, 45 Cache-Contract-Cases, 7 Cache-Identity-
Cases und 51 Diagnostics-/Compiler-Guide-/Bilingual-Cases. Sie enthält
deterministische Controls für Source-Ersetzung, Source-Hardlink,
Destination-Directory-Symlink/-Ersetzung und einen Destination-File-Symlink-
Canary. Der NGINX-Source-/C17-Wiring-Contract, Shell-Syntaxprüfungen,
Python-Kompilierung und Diff-Check bestanden. Ein begrenzter lokaler
`make check-nginx-c17`-Versuch lieferte korrekt den nativen Blocked-Status,
weil unterstützte NGINX-Header/-Quellen hier fehlen; dies ist kein Host-
Compile-Nachweis. Der nächste normale unveränderliche Head muss von GitHub
zurückgelesen werden und frisches Sonar, den Exact-Head-NGINX-Build plus beide
`modsecurity_use_error_log`-Zellen sowie den vollständigen CRS/no-MRTS-
Runtime-Workflow ausführen. Kein früherer Lauf wird wiederverwendet und es
erfolgen kein Merge, Force-Push, Framework-/MRTS-/Gitlink-, Workflow-, Test-
oder Quality-Gate-Änderung.
