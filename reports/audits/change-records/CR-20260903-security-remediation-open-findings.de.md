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
| Delivery-Status | Draft PR [#354](https://github.com/Easton97-Jens/ModSecurity-conector/pull/354) ist offen, nicht gemergt und bleibt Draft. Dieser Change Record ist Teil seines eigenen Dokumentations-Successors und promotet kein Vorgängerergebnis. Nach dem Successor-Push werden seine exakte SHA und der frische Ergebnis-Readback in PR-Metadaten und aufbewahrter Delivery-Evidence festgehalten. Die Parent-Exact-Five-Workflowimplementierung existiert nun, aber es wurde noch kein frisches Exact-Successor-Five-Cell-Aggregate-Artefakt oder -Ergebnis beobachtet und zurückgelesen. FND-CROSS-0004 bleibt daher ein unabhängiger, nicht akzeptierter `P1`-Release-Blocker bis zu seinen bestehenden Framework-Abnahme- und Hosted-Evidence-Kriterien; weder Draft-Transition noch Merge sind autorisiert. |

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
- Parent-With-CRS/no-MRTS-Exact-Five-Evidence-Vertrag: ci/runtime/lifecycle/with-crs-no-mrts-profile.py, ci/runtime/lifecycle/aggregate-five-connector-with-crs-no-mrts.py, ci/runtime/lifecycle/normalize-with-crs-no-mrts.py, ci/runtime/lifecycle/prepare-with-crs-no-mrts-upload.py, ci/runtime/lifecycle/project-haproxy-runtime-evidence.py und .github/workflows/test-connectors-with-crs-no-mrts.yml.
- Apache-Profil-Evidence und fokussierte Regressionen: connectors/apache/harness/run_apache_smoke.sh, tests/test_with_crs_no_mrts_profile.py, tests/test_apache_with_crs_profile_evidence_contract.py, tests/test_haproxy_evidence_projection.py, tests/test_haproxy_evidence_workflow_contract.py, tests/test_with_crs_no_mrts_runtime.py und tests/test_ci_security_workflows.py.
- Profildokumentation: docs/reference/with-crs-no-mrts-profile-contract.md und docs/reference/with-crs-no-mrts-profile-contract.de.md.
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
| Exact-f38-NGINX-Provisioning/-Compile gegen unterstützte Quellen | Bestanden: Das gepinnte Archiv `nginx-1.31.4` wurde per SHA-256 geprüft und erzeugte das verwaltete `ngx_http_modsecurity_module.so`; die task-lokale Einstellung `--no-same-owner` vermeidet nur die nicht unterstützte Archiv-Eigentümerwiederherstellung. Dies ist kein On/Off-Runtime-Ergebnis. |
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

### NGINX-Registry-Sonar-Nachverfolgung und Hosted-Runtime-Grenze

Das Exact-Head-SonarCloud-Ergebnis für
`ac78937ace73fbc27a7c8a9b9ab0297c1d94de16` ließ das Quality Gate `OK`, doch
das PR-Inventar enthielt zwei echte neue Issues in der Registry-Staging-
Behebung: `python:S3776` für die kognitive Komplexität der Descriptor-Copy und
`python:S107` für den NGINX-Build-Environment-Helper mit vierzehn Parametern.
Die drei verbleibenden `c:S995`-Authorization-Fixture-Zeilen bleiben die
dokumentierten Nichtprobleme der öffentlichen ABI. Es werden weder ein
Issue-Übergang, `NOSONAR`, Regel-Ausschluss noch eine Quality-Gate-Änderung
verwendet.

Die Nachbesserung teilt die Descriptor-Copy in begrenzte Allokations-,
Read/Write-, Sync/Identity-, Publishing- und Cleanup-Helper auf und behält
No-Follow-Opens, Single-Link-Source-Prüfungen, größenexaktes Kopieren,
atomaren Ersatz und descriptor-relatives Cleanup bei. Sie ersetzt die große
interne Argumentliste durch eine immutable typisierte Eingabegrenze und behält
das Überschreiben einer feindlich geerbten
`MSCONNECTOR_PROFILE_REGISTRY_ROOT` bei. Ein unabhängiges Review fand während
dieser Aufteilung einen Close-Failure-Ownership-Pfad; der Descriptor bleibt
jetzt bis zum erfolgreichen Close gehalten, und eine negative Regression
prüft das Cleanup der temporären Datei bei diesem Fehler. Die fokussierte
Preparation-Suite besteht mit 89 Cases und fünf bestehenden Framework-Head-
Skips; die breitere Cache-/Diagnostics-Suite, Python-Kompilierung und
Diff-Check bestehen. Ein lokaler Single-File-Sonar-Analyzer ist wegen der CPU-
Inkompatibilität des Hosts mit seinem signierten Analyzer-Binary blockiert;
das nächste frische SonarCloud-Ergebnis ist daher die maßgebliche Verifikation.

Der Hosted-NGINX-Lauf `33818517134` auf `ac78937` provisionierte gepinntes
NGINX erfolgreich und schloss den Connector-Build-Schritt ab, aber die
isolierte On/Off-Harness brach korrekt mit ihrem beabsichtigten Status `77`
ab: Ein unprivilegierter GitHub-Runner kann die erforderliche unterschiedliche
verifizierte Worker-Identität nicht einrichten. Die Harness hat keinen sicheren
Same-Identity-Bypass, und der geschützte Root-Broker führt diese Zellen nicht
aus. Dieses Ergebnis ist daher nur Compile-Evidenz, keine
`modsecurity_use_error_log`-Runtime-Evidenz. Ein task-eigener Root-fähiger
lokaler Provision/Run bleibt die autorisierte Alternative, die nach dem
nächsten normalen Successor-Head zu prüfen ist; es erfolgen keine Workflow-
Änderung, kein Merge, Force-Push, Framework-/MRTS-/Gitlink-Change und keine
Abschwächung von Test oder Kontrolle.

### Exact-Head-f38-Validierungsnachtrag

Der Successor-Head `f38f239a8d0e73408a049583f5fcdb01d8b7be9b` wurde normal
gepusht und von GitHub zurückgelesen. Der vollständige Runtime-Workflow
`33820766693` bestand alle fünf Connector-Jobs an genau diesem Head. Der
NGINX-Workflow `33820766701` bestand außerdem Exact Checkout, gepinnte
Provenance und Runtime-Component-Provisioning.

Seine isolierten `modsecurity_use_error_log`-On/Off-Zellen endeten mit dem
beabsichtigten Status `77`, weil der unprivilegierte Hosted-Runner die
erforderliche unterschiedliche verifizierte Worker-Identität nicht einrichten
kann. Es wurde kein Same-Identity-Bypass und keine Workflow-Abschwächung
verwendet; dieser Workflow ist daher kein On/Off-Runtime-Nachweis. Ein
separater lokaler Pinned-Source-Retry bestätigte zunächst, dass das
Release-Archiv gültig ist, aber uid `502`/gid `50` in diesem
capability-restringierten Root-Namespace nicht wiederherstellen kann. Mit nur
der sicheren Host-Kompatibilitäts-Einstellung `--no-same-owner` erzeugte der
echte Provisioner das verwaltete NGINX-Connector-Modul. Die lokale Runtime kann
die geforderte Evidence dennoch nicht liefern: `runuser` kann keine Gruppen
setzen, und die bestehende Framework-Containment-Kontrolle lehnt ihre nicht
enthaltene Materialisierungsgeometrie vor dem Worker-Start korrekt ab. Keines
dieser Ergebnisse rechtfertigt eine Abschwächung der Identity- oder
Containment-Controls.

Das Exact-Head-SonarCloud-Ergebnis bestand das Quality Gate. Die zwei neu
aufgetretenen Registry-Staging-Issues (`python:S3776` und `python:S107`) wurden
in f38 behoben. Die drei verbleibenden `c:S995`-Authorization-Fixture-Befunde
sind einzeln als fachliche Nichtprobleme der öffentlichen ABI dokumentiert. Es
wurden weder `NOSONAR`, Ausschlüsse, Issue-Transitions noch eine
Quality-Gate-Abschwächung verwendet.

### 2026-09-05 Abgleich mit der aktuellen Basis

Dieser PR wurde über einen normalen Merge in den bestehenden PR-Branch mit
der exakten Vergleichsrevision von `origin/master`,
`b779167ff979aa73cdd9321a829f9c693d943760`, abgeglichen. PR #355 bleibt
ungemergt: Seine beantragte Integration am exakten Head ist durch den
unabhängigen, weiterhin offenen Befund FND-PARENT-1038 blockiert. Der externe
codex-security-Abhängigkeitsblocker FND-PARENT-1036 bleibt unverändert und
wird nicht als behoben ausgegeben.

Die fünf angeforderten Grenzbereiche wurden erhalten oder minimal an die
aktuelle Basis angepasst: verlustfreie HAProxy-path/uri-Grenzbehandlung,
Common-JSONL-Query-Redaction mit expliziten Truncation- und Integrity-Flags,
effektive `modsecurity_use_error_log`-Behandlung im nativen NGINX-Callback,
Traefik-Deadlines, Worker-Cap und FD-Ownership sowie Companion-Quieszenz und
Exactly-once-Release bei Authorization. Die fokussierte lokale Evidenz ist
für den gelinkten JSONL-Test, den ausführbaren HAProxy-Parser-Test und den
C17-Check, den nativen Authorization-Companion-Smoke-Test und sieben
Worker-Contract-Tests sowie die gezielten Traefik-Worker/FD- und
Service-Contract-Tests erfolgreich. Die vollständige Traefik-Native-Local-
Plugin-Suite mit 37 Tests lief außerdem mit einem privaten kurzen AF_UNIX-
Temporärpfad erfolgreich. Dies sind frische Ergebnisse des Arbeitsbaums und
keine Aussage über einen künftig gepushten Head.

Der lokale native NGINX-Check bleibt blockiert, weil unterstützte
NGINX-Header/-Quellen fehlen. Für die Kompilierung gegen unterstützte Quellen
und die isolierte `modsecurity_use_error_log`-On/Off-Runtime-Evidenz ist
weiterhin das benannte `NGINX-Use-Error-Log-Exact-Head-Hosted-Gate`
erforderlich; kein
Exit-77-Ergebnis wird als Erfolg gewertet und hier wird keine Host-Runtime-
Evidenz behauptet.

Der zusätzliche Control-Check `check-nginx-common-adoption` ist auf diesem
Head nur deshalb rot, weil er bereits auf der exakten Vergleichsbasis mit den
zwei bekannten FND-PARENT-1010-Assertions rot ist. Die einschlägigen NGINX-
Pfade der aktuellen Basis sind hier bis auf den nativen Log-Callback
unverändert; der separate reine Checker-Successor ist Draft-PR #357. Dieser PR
übernimmt weder diese unabhängige Reparatur noch schwächt er den Check ab; sein
frisches Hosted-Ergebnis muss den Basisfehler entsprechend ausweisen.

Auch `check-haproxy-common-adoption` reproduziert auf beiden Revisionen eine
bereits in der aktuellen Basis vorhandene Assertion (`request mapper prefers
Host header and keeps server_ip fallback`). Sie steht im Widerspruch zur
validierten Host-Zuweisung und zum separaten Server-Endpoint-Feld des aktuellen
Mappers, nicht zur Target-Parser-Änderung dieses PRs. FND-PARENT-1041 verfolgt
die reine Checker-Diskrepanz für eine separate enge Reparatur; Fallback,
Runtime-Source und Check wurden hier nicht geändert.

### 2026-09-05 Mutable-Runtime-Fixture-Remediation (vor dem Push)

Am Ausgangs-PR-Head `1208ca9b5bfbf8851ec4d9fe0772cfa3313092d8` waren die zwei
aktiven SonarCloud-`c:S995`-Records
`AaBnPLYKQISHK43ZVdja` (Event-Integration-Setter) und
`AaBnPLYKQISHK43ZVdjb` (Transaction-Profile-Setter). Produktionsdeklarationen
und -definitionen verwenden absichtlich veränderbare
`msconnector_runtime *`: der erste kopiert den Integration-Mode in
Runtime-Speicher, der zweite speichert das ausgewählte Profil. Eine Umstellung
dieser ABI auf `const` wäre fachlich falsch.

Die Detached-Worker-Fixture bildet diese beiden Wirkungen jetzt unter ihrem
bestehenden Lock in einem eigenen gültigen Runtime-Objekt ab: Sie kopiert den
akzeptierten Integration-Mode in begrenzten Fixture-Speicher und speichert den
akzeptierten Profil-Pointer. Die Fixture prüft den unkonfigurierten Zustand vor
Service-Start und den durch die echten Service-Setter konfigurierten Zustand.
Die Response-Companion-Fixture setzt dasselbe Test-Runtime-Objekt zurück statt
veralteter globaler Flags. Dies ist eine verhaltensgetreue Fixture-Korrektur,
kein Cast, Dummy-Write, Suppression oder Produktions-ABI-Change; alle Controls
für Companion-Quieszenz, Quarantäne bei fehlgeschlagenem Shutdown,
Exactly-once-Release, konkurrierenden Claim und No-Companion-Deferred-Release
bleiben erhalten.

Das C17-Timeout-/Companion-Lifecycle-Skript bestand sowohl normal als auch mit
AddressSanitizer und UndefinedBehaviorSanitizer. Die Worker- und
Security-Contract-Suiten bestanden 14 Tests mit 14 Passes, null
Failures/Errors/Skips. Eine frische SonarCloud-Analyse des normal gepushten
Successors muss weiterhin belegen, dass beide aktiven Keys fehlen; kein lokales
Ergebnis wird als SonarCloud-Evidence ausgegeben.

Der angeforderte Equal-Environment-Adoption-Vergleich wurde in sauberen
Worktrees mit `rtk 0.47.0` und `Python 3.14.7` erneut ausgeführt:

| Finding | Befehl in jedem sauberen Worktree | Basis `b779167…` | PR-Start `1208ca9…` | Ursache | PR-Regression? |
| --- | --- | --- | --- | --- | --- |
| FND-PARENT-1010 | `python3 -B ci/checks/connectors/nginx/check-nginx-common-adoption.py` | Exit 1; dieselben zwei Assertions | Exit 1; dieselben zwei Assertions | veraltete Annahmen zu nichtfatalem Mapper und explizitem Length-Sink | Nein |
| FND-PARENT-1041 | `python3 -B ci/checks/connectors/haproxy/check-haproxy-common-adoption.py` | Exit 1; dieselbe Host/server-IP-Assertion | Exit 1; dieselbe Host/server-IP-Assertion | veraltete Checker-Annahme zu Host-Priorität und Server-Endpoint | Nein |

Beide Worktrees waren vorher und nachher sauber. Diese gemeinsamen
Basis-/Checker-Fehler bleiben separate Remediation-Arbeit; dieser PR ändert
ihren Checker nicht und behauptet kein grünes Ergebnis dafür.

### 2026-09-05 Native-NGINX-Phase-4-Event-Sink-Remediation (vor dem Push)

Ausgehend vom Draft-PR-#354-Head
`bf4666883463e066aad82db6ea27716b5e9d13e7` lehnte der native Setter
`modsecurity_phase4_log` jedes konfigurierte Ziel ab, bevor er einen
Descriptor an die JSONL-Callbacks übergeben konnte. Ein gültiges sicheres Ziel
konnte daher keine native NGINX-JSONL-Evidence erzeugen.

Die eingegrenzte Behebung öffnet das konfigurierte Ziel ausschließlich über
`msconnector_open_private_event_file`, installiert genau ein NGINX-Pool-Cleanup
vor dem Ownership-Transfer des Descriptors und schreibt über diesen
connector-eigenen File-Descriptor. Der Descriptor wird bewusst nicht in
`cycle->open_files` registriert: Ein generisches NGINX-`USR1`-Reopen würde den
Pfad sonst außerhalb des Common-Vertrags für no-follow, reguläre Datei,
vertrauenswürdiges Parent/Owner und `0600` erneut öffnen. `USR1` behält daher
den validierten Descriptor; ein sicherer Konfigurations-Reload parst und
öffnet einen neuen Descriptor, während alte Worker drainen. Geerbte Locations
leihen den Parent-Descriptor ohne zweites Cleanup, explizit konfigurierte
Children besitzen ihren eigenen Descriptor, und das Cleanup invalidiert den
Descriptor vor dem Schließen.

Das zugehörige Functional-A-Gate erstellt getrennte `on`- und `off`-Zellen aus
demselben gehashten Binary-/Module-/Rule-Set. Es verlangt einen echten
root-Master und einen unterschiedlichen Non-root-Worker und prüft gültige
Ziele, nicht konfiguriertes Logging, die Reparatur bestehender Modi,
Vererbung/Override, fünf unsichere Zielformen, redigiertes JSONL,
Raw-URI-/WAF-Kontinuität, Callback-Trennung, `USR1`-Beibehaltung, Erhalt nach
fehlgeschlagenem unsicherem Reload, sicheren Reload-Overlap/Drain sowie
Shutdown-FD-/Prozess-Cleanup. Das Gate ist ein GitHub-hosted-nativer
Integrationsnachweis, keine unabhängige Attestierung gegen einen bösartigen
Kandidaten. Es führt kandidatenkontrollierten Code nur für Functional A auf
einer flüchtigen GitHub-hosted-VM aus; es ist weder source-unabhängig noch eine
adversariale Vertrauensgrenze und kann Protected B oder FND-PARENT-1038 nicht
validieren.

Die lokale Verifikation dieses Kandidaten bestand die 43 fokussierten
NGINX/Common-/Launcher-/Reference-Python-Tests, Shell-Syntaxprüfungen,
Python-Kompilierung, `actionlint`, Generated-Reference-Prüfungen,
`git diff --check` und die Supported-Source-C17/C23/C2y-Kompilierung.
`check-nginx-common-adoption` meldet weiterhin nur die zwei dokumentierten
Current-Base-FND-PARENT-1010-Assertions; weder Checker, Test, Workflow noch
Quality-Gate-Control wurden abgeschwächt. Ein lokaler Functional-A-Lauf ist in
diesem Container nicht gültig: Er ist bereits root, kann die erforderliche
sudo-/Non-root-Worker-Kette nicht herstellen, hat kein initialisiertes
Framework des Task-Worktrees und keine frischen Current-Head-Artefakte.
Exact-Head-GitHub-hosted-Build-/Runtime-Evidence, SonarCloud-Analyse und die
erforderlichen PR-Checks bleiben `not_run`, bis der normale Nachfolge-Commit
gepusht und zurückgelesen wurde. Draft PR #354 bleibt offen und ungemergt;
FND-PARENT-1036 bleibt `blocked_external_dependency`.

### 2026-09-05 Hosted-Functional-A- und Sonar-Follow-up (Successor ausstehend)

Der normale Push von `dcb499b04239f55c6faf7a3abf709b6cc9622fb6` wurde als
Head von Draft PR #354 zurückgelesen. Seine fünf frischen CRS/no-MRTS-
Runtime-Zellen bestanden, aber diese Vorgänger-Ergebnisse sind kein Nachweis
für einen Successor. Der frische hosted NGINX-Workflow schloss das
sudo-/root-gegen-Worker-Preflight und die unprivilegierte Provisionierung ab
und schlug anschließend fail-closed mit Exit `77` fehl: Sein Launcher lehnte
den generischen Libtool-Alias `libmodsecurity.so` zu Recht ab, weil dieser
Alias ein symbolischer Link ist. Dies ist ein fehlgeschlagenes Functional-A-
Runtime-Ergebnis, kein bestandenes On/Off-Ergebnis.

Der freigegebene Komponenten-Provisioner bewahrt diesen generischen Alias
absichtlich für gewöhnliche Verbraucher und publiziert daneben
`libmodsecurity.so.3` als geschütztes reguläres Runtime-Artefakt. Die enge
Successor-Behebung bindet nur Functional A an diese bereits vorhandene
reguläre Datei: Der root-Launcher validiert sie ohne Symlink-Traversal,
übergibt ihren exakten begrenzten Pfad, und das Exact-Head-Gate hasht diese
Datei vor/nach beiden On/Off-Zellen. Der generische Smoke-Harness behält
außerhalb von Functional A seinen bestehenden Default
`libmodsecurity.so`. Ein Functional-A-Aufruf weist ein fehlendes,
substituiertes oder symlinktes Runtime-Artefakt zurück, statt auf den
generischen Alias zurückzufallen. Provisioner, Framework, MRTS, Dependency,
Policy, Workflow-Berechtigung oder Attestierungsgrenze werden nicht geändert.

Der SonarCloud-Readback für den Vorgänger meldete Quality Gate `ERROR` und
sechs aktive PR-Issues: Reader-Komplexität und File-Open-Hardening, zwei
fehlende Shell-`case`-Defaults und zwei Assertion-Expression-Prüfungen. Der
Successor teilt den begrenzten Parser auf, öffnet ausschließlich die feste
`runtime_root/conf/case.env` über descriptor-relative no-follow-Operationen
und weist unsichere Directories, Substitutionen, Special Files, Hard Links,
zu große Inhalte und veränderte Datei-Identität zurück. Die Shell-Cases
schlagen jetzt fail-closed fehl und die Tests verwenden pro Exception-
Assertion genau einen ausgewerteten Ausdruck. Kein Issue wird ignoriert,
unterdrückt oder risikoakzeptiert. Fokussierte Reader-, Launcher-, Exact-Gate-
und Phase-Runner-Tests bestanden lokal; die drei Phase-Runner-Skips sind die
bestehende Bedingung eines fehlenden/nicht passenden Framework-Pins.

Der Successor benötigt weiterhin normalen Push, GitHub-Readback, frische
hosted On/Off-Runtime, frische CRS/no-MRTS-Checks sowie ein frisches
SonarCloud-Ergebnis mit null aktiven Issues und bestandenem Quality Gate.
Functional A bleibt ausschließlich ein GitHub-hosted-nativer
Integrationsnachweis, nicht Protected B oder eine Auflösung von
FND-PARENT-1038; FND-PARENT-1036 bleibt `blocked_external_dependency`.

### 2026-09-05 Zweiter Hosted-Follow-up (Successor-Kandidat ausstehend)

Für den exakten Draft-PR-#354-Head
`d2abf5dc9fc287d5e8d233ec725c23ab1f14a97a` bestand der frische hosted
NGINX-Lauf `33989150637` den Exact-Head-Checkout, das
sudo-/root-gegen-Worker-Preflight, die Initialisierung isolierter Pfade und
die unprivilegierte Komponenten-Provisionierung. Er schlug danach vor beiden
nativen On/Off-Zellen fail-closed mit Exit `77` fehl: Die absichtlich
bereinigte `/usr/bin/env -i`-Allowlist ließ sowohl
`NGINX_FUNCTIONAL_WORKER_USER` als auch `NGINX_FUNCTIONAL_WORKER_GROUP` weg,
obwohl beide zuvor geprüft worden waren. Der Root-Launcher erhielt dadurch
eine leere Worker-Identität und wies sie zurück. Dies ist eine
Workflow-Allowlist-Auslassung, keine Lockerung der Worker-Prüfung und kein
erfolgreiches Functional-A-Ergebnis.

Dieselbe Exact-Head-SonarCloud-Analyse bereinigte die vorherigen sechs Issues,
meldete aber zwei neue aktive `pythonsecurity:S8707`-Flüsse von der
pfadwertigen Reader-CLI-Option `--runtime-root` nach `os.open`; das Quality
Gate blieb daher `ERROR` (`new_security_rating=3`, Schwelle `1`). Die
Kandidatenbehebung entfernt sämtliche pfadwertigen CLI-/Environment-Eingaben
des Readers. Der Functional-A-Harness öffnet seinen bereits pfadautorisierten,
frisch privaten Runtime-Root nur als geerbten Descriptor `3`; der Reader
dupliziert und validiert diese Capability und öffnet dann ausschließlich feste
`conf/case.env`-Komponenten mit No-follow-Prüfungen. Owner-/Mode-/Typ-/Link-
Count-/Größen- und Mutation-Prüfungen bleiben erhalten. Header-, Body- und
Audit-Pfade aus dem generierten Record werden außerdem vor ihrer späteren
Nutzung durch Root-seitige Verbraucher mit den bereits konstruierten
vertrauenswürdigen Pfaden verglichen; sie können diese Pfade nicht ersetzen.

Der Kandidat reicht außerdem beide begrenzten Worker-Namen explizit durch die
bestehende bereinigte Umgebung. Der Root-Launcher validiert und mappt sie
weiter auf die NGINX-Worker-Identität; weder eine Ambient-Umgebung noch eine
breite sudo-Kette oder ein Identity-Bypass wird eingeführt. Die lokale
Kandidatenvalidierung bestand 46 fokussierte
NGINX/Common/Event/Lifecycle/Reader/Launcher/Reference-Tests, die drei
anwendbaren Phase-4-Runner-Tests (drei Framework-Pin-abhängige Tests bleiben
übersprungen), Python-Kompilierung, Shell-Syntax, `actionlint`,
C-Standard-Wiring und Whitespace-Prüfungen. Der lokale Sonar-Vortex-Precheck
ist für diese Organisation nicht verfügbar und wird nicht als
SonarCloud-Ergebnis ausgegeben. Die bestehenden zwei
FND-PARENT-1010-Basis-Assertions lassen
`check-nginx-common-adoption` weiterhin fehlschlagen; sie wurden weder
geändert noch maskiert.

Dieser Kandidat ist noch nicht gepusht. Ein normaler Successor-Push, GitHub-
Head-Readback, frische hosted On/Off-Runtime, alle fünf CRS/no-MRTS-Läufe und
ein frisches SonarCloud-Ergebnis mit null aktiven Issues/bestandenem Quality
Gate bleiben erforderlich. Functional A bleibt nur ein Integrationsnachweis,
FND-PARENT-1038 bleibt unverändert offen und FND-PARENT-1036 bleibt
`blocked_external_dependency`.

### 2026-09-05 Dritter Hosted-Follow-up (Runuser-Capability-Successor ausstehend)

Für den exakten Draft-PR-#354-Head
`1f267564b35086eda8fed80895eb0cb7f6fb35ab` meldet der frische
SonarCloud-Readback Quality Gate `OK`, null aktive `OPEN`/`CONFIRMED`-
PR-Issues und null `TO_REVIEW`-Hotspots. Auch die frische lokale
Exact-Head-C17-Kompilierung bestand. Diese Ergebnisse machen den nativen
Runtime-Nachweis für sich allein nicht erfolgreich.

Der Hosted-Workflow `33990967266` checkte genau diesen Head aus, bestand das
sudo-/root-gegen-Worker-Preflight, initialisierte den isolierten Root und
schloss die unprivilegierte gepinnte Provisionierung ab. Seine erste `on`-Zelle
schlug danach korrekterweise fail-closed mit Exit `77` fehl: Die bereinigte
Root-Umgebung verwendet absichtlich `PATH=/usr/bin:/bin`, das Preflight nutzt
bereits das verifizierte absolute `/usr/sbin/runuser`, der Harness suchte und
rief `runuser` später aber über `PATH` auf. Diese deterministische Abweichung
ist weder ein Runner-Flake noch ein erfolgreiches On/Off-Ergebnis.

Der enge Successor-Kandidat entfernt diese Pfadsuche. Seine Worker-Identity-
und Access-Prüfungen wählen ausschließlich die ausführbaren festen
System-Capabilities `/usr/sbin/runuser` oder `/usr/bin/runuser`; sie weiten
weder `PATH` aus noch akzeptieren sie einen vom Aufrufer wählbaren Helper-Pfad
oder lockern die Anforderung eines unterschiedlichen Workers. Die direkte
Path-Authority-Suite bestand 11 Tests, die relevanten NGINX-Security-,
Launcher-, Exact-Gate- und Lifecycle-Suiten bestanden 26 Tests; Shell-Syntax-
und Whitespace-Prüfungen bestanden. Der Successor ist noch nicht gepusht;
diese lokalen Ergebnisse behaupten daher keinen Hosted-Erfolg.

Die erste fünfzellige CRS/no-MRTS-Matrix für `1f267...` bestand für Apache,
Envoy, Traefik und Lighttpd. HAProxy stoppte vor der Produktausführung, weil
der GitHub-hosted Komponenten-Provisioner beim Abruf von expat `HTTP Error
403: rate limit exceeded` erhielt; Exact-Head-Checkout, Runtime-Preflight,
CRS-Vorbereitung und Cleanup bestanden. Ein normaler Retry ausschließlich des
fehlgeschlagenen Jobs auf demselben Head läuft. Unabhängig von seinem Ergebnis
ist die gesamte finale Runtime-Evidence auf dem nächsten normalen
Successor-Head erneut auszuführen.

Functional A bleibt ausschließlich ein GitHub-hosted-nativer
Integrationsnachweis, nicht Protected B und keine Auflösung von
FND-PARENT-1038. FND-PARENT-1036 bleibt `blocked_external_dependency`; PR #354
bleibt Draft, offen und ungemergt.

### 2026-09-05 Vierter Hosted-Follow-up (Contained-Materialization-Successor ausstehend)

Für den exakten Draft-PR-#354-Head
`f29fe20fd556b75b96a5fbdcef140bbeb66f5a61` meldet der frische
SonarCloud-Readback Quality Gate `OK`, null aktive `OPEN`/`CONFIRMED`-
PR-Issues, null `TO_REVIEW`-Hotspots sowie einen erfolgreichen
SonarCloud-Check für den exakten Commit.  Der frische fünfzellige
CRS/no-MRTS-Workflow `33992317099` bestand außerdem für Apache, Envoy,
HAProxy, Lighttpd und Traefik.  Diese Ergebnisse machen den separaten nativen
NGINX-Runtime-Nachweis für sich allein nicht erfolgreich.

Der Hosted-Workflow `33992317013` checkte genau diesen Head aus und schloss
das sudo-/root-gegen-Worker-Preflight, die Initialisierung isolierter Pfade und
die gepinnte unprivilegierte Provisionierung ab.  Seine erste `on`-Zelle schlug
dann vor NGINX-Konfigurationsparsing oder Worker-Start fail-closed mit Exit
`78` fehl: Das Exact-Gate setzte `BUILD_ROOT` auf das Child
`case_root/build`, während seine generierten Runtime-, Log- und Audit-Pfade
Sibling-Children des frischen privaten `case_root` waren.  Framework
`case_cli materialize` wies diese Ziele außerhalb des Output-Roots korrekt
über seinen unveränderten Containment-Guard ab.  Es gab keinen Out-of-root-
Write, die `off`-Zelle lief nicht, und es wird kein f29-Erfolg für nativen
Callback, JSONL, WAF oder die Allow-Kontrolle behauptet.

Der enge Parent-Successor-Kandidat bindet sowohl `VERIFIED_BUILD_ROOT` als
auch `BUILD_ROOT` an den bereits frischen privaten Root jeder Case, so dass
alle generierten Runtime-, Log-, Audit-, Harness- und Result-Pfade Children
desselben vertrauenswürdigen Roots bleiben.  Er ändert weder Framework-Code
noch lockert er Path-Containment, den äußeren Path-Validator, die bereinigte
Root-Umgebung oder die Anforderung eines unterschiedlichen Workers.  Eine
dynamische Regression belegt, dass der Framework-Materializer das
Common-Root-Layout akzeptiert und das frühere Sibling-Layout weiter abweist;
sie prüft auch generierte Header-/Body-/Audit-Referenzen.  Das vollständige
fokussierte Set für NGINX/Common/Event/Lifecycle/Reader/Launcher/Path-Authority/
Reference bestand 60 Tests, zusammen mit Shell-Syntax, Python-Kompilierung,
`actionlint`, C-Standard-Wiring und Whitespace-Prüfungen.  Dies sind lokale
Kandidaten-Ergebnisse, keine Behauptung eines Hosted-Erfolgs.

Der Kandidat benötigt weiterhin einen normalen Successor-Commit und -Push,
GitHub-Head-Readback, frische C17- und verfügbare Sanitizer-Bewertung, frisches
SonarCloud, erforderliche Checks, alle fünf CRS/no-MRTS-Runtimes sowie einen
neuen GitHub-hosted-nativen On/Off-/JSONL-/WAF-/Allow-Lauf auf diesem neuen
exakten Head.  Functional A bleibt ausschließlich ein GitHub-hosted-nativer
Integrationsnachweis, nicht Protected B oder eine Auflösung von FND-PARENT-1038;
FND-PARENT-1036 bleibt `blocked_external_dependency`, und PR #354 bleibt Draft,
offen und ungemergt.

### 2026-09-05 Fünfter Hosted-Follow-up (worker-traversierbarer Successor ausstehend)

Vor dem Commit des Kandidaten mit enthaltener Materialisierung identifizierte
ein unabhängiger Source-Review einen weiteren deterministischen Blocker vor
NGINX. Wenn der Provisioning-`RUN_ROOT` und jede Functional-A-Vorfahre bei
`0700` blieben, könnte der separate NGINX-Worker korrekterweise nicht zum
benötigten Docroot sowie zu Worker-State- und Server-Log-Leaves traversieren.
Den `RUN_ROOT` traversierbar zu machen wäre unsicher, weil er die
unprivilegierten Build-, Provisioning- und Evidence-Pfade enthält. Dies ist
zusätzliche aktuelle Evidence für das bestehende Lifecycle-Finding
`FND-PARENT-0078`, das `in_progress` bleibt; es ist weder ein neues Finding
noch der Abschluss eines bestehenden Findings.

Der enge Parent-Successor belässt `RUN_ROOT` bei `0700`. Der Workflow erzeugt
stattdessen unter dem GitHub-Temporary-Root einen frischen Functional-A-Parent
mit festem Namen als direkten Sibling bei exakt `0711`. Vor dem bereinigten
Root-Handoff verlangt der Launcher einen absoluten, symlinkfreien,
vorgesehenen Sibling im Eigentum des Runners, exakt nicht-auflistbaren Modus
`0711` und eine für den Worker traversierbare Vorfahrenkette. Das ausschließlich
rootseitige Exact-Gate erstellt anschließend nur die Functional-A-, Mode- und
Case-Vorfahren als neue root-eigene `0711`-Verzeichnisse. Runtime-Konfiguration,
Rules, Logs, Audit/Evidence und andere private Leaves behalten ihren bisherigen
privaten Vertrag; der Harness behält seine vorhandenen engen
worker-lesbaren Docroot-/State-/Server-Log-Kontrollen. Framework-
Materialisierung bleibt unter dem gemeinsamen Case-Root, ihr Containment-Guard
ist unverändert.

Der dedizierte Parent ist ein runner-eigener Bootstrap für den ausdrücklich
begrenzten Functional-A-GitHub-hosted-Integrationsnachweis. Er ist keine
Attestierungsgrenze gegen einen bösartigen Runner oder VM-root und wird nicht
als Protected B ausgegeben. `FND-PARENT-1038` bleibt fixed, aber unverified
und nicht geschlossen sowie durch diesen Kandidaten unverändert;
`FND-PARENT-1036` bleibt `blocked_external_dependency`. Es werden keine
Framework-, MRTS-, Gitlink-, Dependency-, Permission-Policy-, Test-, Sonar-
oder generischen Path-Authority-Kontrollen geändert.

Die lokale Kandidatenvalidierung bestand 63 fokussierte NGINX/Common/Event/
Lifecycle/Reader/Launcher/Path-Authority/Reference-Tests, einschließlich einer
dynamischen Framework-Materialization-Kontrolle gegen den read-only Checkout
am exakten Framework-Gitlink, der neuen Mode-/Layout-Regression, Shell-Syntax
für beide NGINX-Harness-Skripte, Python-Kompilierung, `actionlint`,
C-Standard-Wiring und Whitespace-Checks. Der lokale Container kann die reale
separate-Worker-`runuser`-Kontrolle nicht ausführen, weil Gruppenwechsel
abgewiesen werden; daher wird kein lokaler Worker-Runtime-Erfolg behauptet.
`check-nginx-common-adoption` bleibt nur wegen der zwei unveränderten,
getrackten FND-PARENT-1010-Basisassertions rot. Dieser Kandidat ist noch nicht
gepusht; ein normaler Successor-Push und sämtliche frische Exact-Head-Hosted-,
CRS/no-MRTS-, Required-Check- und Sonar-Evidence bleiben verpflichtend.

### 2026-09-05 Sechster Hosted-Follow-up (ShellCheck-Successor ausstehend)

Der Worker-Traversal-Commit
`25a3eea84185ebcb1d121e84d267e53610cf4118` wurde normal auf den bestehenden
Draft-PR-#354-Branch gepusht und sowohl aus Git als auch aus GitHub
zurückgelesen. Sein Exact-Head-Security-Workflow-Lint schlug danach mit Exit
`1` in `.github/workflows/test-nginx-exact-head.yml` fehl: ShellCheck `SC2015`
beanstandete korrekt die Fresh-Parent-Prüfung als `&&`/`||`-Kette. Dies ist ein
echter Workflow-Quality-Defekt, kein Grund, ShellCheck, actionlint oder die
Ablehnung belegter Pfade zu deaktivieren. Die Exact-Head-Hosted-NGINX- und
CRS/no-MRTS-Läufe waren gestartet, werden aber nicht als Erfolgsevidence
verwendet, weil der nächste normale Successor diesen Head ersetzt. Der initiale
Exact-Head-Sonar-Erfolg ist nach diesem Successor-Push ebenfalls nur
Vorgänger-Evidence.

Der enge Successor schreibt ausschließlich diese Bedingung als explizites
`if`: Ein existierender oder symlinked Functional-A-Parent schlägt weiterhin
vor jedem privilegierten Handoff fehl, während ein frischer Parent unverändert
weiterläuft. Sein Contract-Test weist eine erneute Einführung der mehrdeutigen
Kette ab. Dreizehn fokussierte Launcher-/Layout-/Gate-Tests, lokales
`actionlint` und Whitespace-Checks bestehen. Das vollständige relevante
Regressionsset, der C17-Build, Sonar, Required Checks, alle fünf CRS/no-MRTS-
Zellen und der GitHub-hosted-native On/Off-/JSONL-/WAF-/Allow-Nachweis müssen
auf dem neuen exakten Head erneut laufen.

Dieser Successor ist noch nicht gepusht. Functional A bleibt ausschließlich
ein GitHub-hosted-nativer Integrationsnachweis, nicht Protected B und keine
Attestierung gegen einen bösartigen Runner oder VM-root. FND-PARENT-1038 bleibt
fixed, aber unverified und nicht geschlossen sowie durch diesen Kandidaten
unverändert; FND-PARENT-1036 bleibt `blocked_external_dependency`; PR #354
bleibt Draft, offen und ungemergt.

### 2026-09-05 Siebter Hosted-Follow-up (Phase-4-Request-Metadata und `/tmp`-Traversal-Successor ausstehend)

Der exakte Draft-PR-#354-Predecessor
`a4666abf3b6585c80abc68f84ab9ebef10f054aa` erreichte in GitHub-hosted
Functional-A-Run `33996313979` die erfolgreiche Provisionierung und schlug
dann mit Exit `77` fail-closed fehl:
`NGINX_FUNCTIONAL_A_PARENT_ROOT has a worker-non-traversable ancestor`. Das
begrenzte Log benannte diesen Vorfahren nicht. NGINX startete nie; daher beweist
der Run weder natives Callback-Verhalten noch Phase-4-JSONL-, WAF- oder Allow-
Verhalten und darf nicht für den Successor wiederverwendet werden.

Der enge Traversal-Successor weitet `RUNNER_TEMP` nicht auf. Er verifiziert den
root-eigenen sticky-`/tmp`-Vertrag, erzeugt darunter einen atomaren
runner-eigenen Job-Root, belässt den Provisioning-`RUN_ROOT` privat bei `0700`
und macht nur den festen Functional-A-Sibling bei `0711` sichtbar. Der Launcher
bindet exakte direkte Topologie, Ownership, Modes und no-symlink-Komponenten;
der Workflow verwendet die reale konfigurierte `runuser`-Identität, um Worker-
Traversal der Job-/Functional-A-Vorfahren zu beweisen und zugleich
Nicht-Traversierbarkeit von `RUN_ROOT` zu belegen. Dies ist nur ein
GitHub-hosted-Functional-A-Integrationsnachweis, keine Attestierung gegen einen
bösartigen Runner oder VM-root und nicht Protected B.

Ein unabhängiger Source-to-Sink-Review fand außerdem einen getrennten
Phase-4-Defekt: `ngx_http_modsecurity_phase4_log_event` initialisierte sein
Event, ließ aber Request-Methode/-URI aus, sodass der Common-Serializer eine
leere URI erhielt. Die enge NGINX-C-Korrektur verwendet den bestehenden
pool-owned Helper `ngx_http_modsecurity_event_request_metadata(r)` und weist
Methode/URI vor der Common-Serialisierung zu. Common bleibt alleiniger Owner
von Query-Redaction, Truncation-Signalisierung und passender Integrity-Sicht;
die rohe `r->unparsed_uri` läuft weiter unabhängig durch den NGINX-/WAF-
Requestpfad. Es wurde kein connector-spezifischer Redactor oder Common-Runtime-
Refactor hinzugefügt.

Der Predecessor-Source-Contract wurde vor der Zuweisung als fehlschlagend
beobachtet und besteht für den aktuellen Kandidaten. Aktuelle lokale Evidence
umfasst 28 fokussierte Native-/Launcher-/Topology-/Exact-Gate-Tests, einen
C17-Compile mit Warnings als Errors, den direkten Common-Long-URI-/
Query-Redaction-/Integrity-Control, Shell-Syntax, `actionlint`, C-Standard-
Wiring und Whitespace-Checks. Dies ist nur Source-/Contract-Evidence: der
erforderliche frische Exact-Successor-Hosted-ON/OFF-/JSONL-/WAF-/Allow-Nachweis,
alle fünf CRS/no-MRTS-Zellen, Required Checks und SonarCloud müssen nach einem
normalen Successor-Push laufen. Exit `77` bleibt fehlgeschlagene Evidence.

`FND-PARENT-1046` hält die getrennt behebbare Phase-4-Request-Metadata-Grenze
fest und bleibt `in_progress`; `FND-PARENT-0078` behält die Traversal-Grenze
und bleibt ebenfalls `in_progress`. `FND-PARENT-1038` ist unverändert und
nicht geschlossen; `FND-PARENT-1036` bleibt `blocked_external_dependency`. PR
#354 bleibt Draft, offen und ungemergt.

### 2026-09-05 Achter Hosted-Follow-up (ShellCheck-Guard-Successor ausstehend)

Der normale Successor `d88b47abb598eb410ebddca7d3016ca526d06447` wurde auf
den bestehenden Draft-PR-#354-Branch gepusht und aus Git sowie GitHub
zurückgelesen. Sein Exact-Head-Security-Workflow-Lint-Run `33999439753` schlug
anschließend an den zwei neuen Functional-A-Guards für `/tmp` und den frischen
Job-Root mit ShellCheck `SC2015` fehl. Die Guards schlagen fail-closed fehl,
aber ihre Form `A && B || { ...; }` ist mehrdeutig und darf nicht in einem
grünen Workflow verbleiben.

Der begrenzte Follow-up schreibt nur diese zwei Bedingungen als explizite
`if`-Guards mit derselben Wahrheitstabelle um: ein fehlendes/nicht als
Verzeichnis vorliegendes oder symlinked `/tmp`/Job-Root wird vor jedem
privilegierten Handoff abgewiesen. Der fokussierte Contract-Test weist die
Wiedereinführung beider mehrdeutigen Formen ab, und lokales
`actionlint -shellcheck=/usr/bin/shellcheck` besteht. Keine Ownership-, Mode-,
Traversal-, Common-Serialisierungs-, Descriptor-Lifecycle- oder
Root-Command-Grenze wird abgeschwächt.

Dieser Successor ist noch nicht gepusht. Der laufende Hosted-Functional-A-Lauf
und die fünf CRS/no-MRTS-Zellen von `d88b47ab...` sowie dessen übrige Checks
und Sonar-Analyse sind nach dem nächsten normalen Push nur Vorgänger-Evidence.
Der nächste exakte Head benötigt weiterhin frische native
ON/OFF-/JSONL-/WAF-/Allow-Evidence, Worker-/Reload-/Shutdown-Lifecycle-
Evidence, relevante Checks, alle fünf Runtime-Zellen und SonarCloud.
`FND-PARENT-1046` und `FND-PARENT-0078` bleiben in progress;
`FND-PARENT-1038` ist unverändert und nicht geschlossen;
`FND-PARENT-1036` bleibt `blocked_external_dependency`. PR #354 bleibt Draft,
offen und ungemergt.

### 2026-09-06 Neunter Hosted-Follow-up (root-eigene Functional-A-Vorfahren und Fixed-Temporary-Root-Successor ausstehend)

Der normale Successor `c98dbac165d1d2dcee81fafab4a670bd90a82f53` bestand seinen
Exact-Head-Security-Workflow-Lint, aber sein GitHub-hosted-Functional-A-Workflow
`33999740011` schlug anschließend im ersten Runtime-Schritt fail-closed mit
Exit `77` fehl. Checkout, Exact-HEAD-Verifikation, das Root-/Worker-Preflight,
die Initialisierung isolierter Pfade und die unprivilegierte gepinnte
Provisionierung waren abgeschlossen. Der unveränderte Runtime-Path-Authority-
Validator wies den runner-eigenen Job-Root-Vorfahren bei der Ausführung als
Root korrekt zurück: `runtime directory has an untrusted owner below shared
temporary root /tmp`. Es liefen kein NGINX-Server und keine Assertion für
nativen On-/Off-Callback, JSONL, WAF, Allow, Reload oder Shutdown. Exit `77`
ist fehlgeschlagene Evidence, kein erfolgreicher Hosted-Nachweis.

Dieselbe exakte c98-SonarQube-Cloud-Analyse meldete ein aktives task-eigenes
`python:S5443`-Issue an der Public-Temporary-Root-Zeile des Functional-A-
Launchers und Quality Gate `ERROR`. Es wurden weder `NOSONAR`, Rule-Exclusion,
False-Positive-Status, Quality-Gate-Änderung noch Risk Acceptance verwendet.
Der eng begrenzte Successor löst das Standard-Temporary-Directory nur auf, um
fail-closed abzulehnen, wenn es nicht exakt der feste `/tmp`-Namespace ist;
danach behält er die bestehenden No-symlink-, root-owned-sticky-`01777`-,
Owner-, Mode- und Traversal-Prüfungen vor dem bereinigten `sudo`-Handoff bei.
Er akzeptiert keinen durch `TMPDIR` umgeleiteten Root.

Vor der unprivilegierten Provisionierung erzeugt der Workflow jetzt den
frischen Functional-A-Job-Root und dessen festen Functional-Parent-Sibling als
root-eigene Verzeichnisse, validiert nur den anfänglichen `0700`-Zustand des
Job-Roots und setzt anschließend beide Vorfahren auf nicht-auflistbares `0711`. Er erzeugt,
chown't und hält
nur den separaten Provisioning-`RUN_ROOT` runner-owned bei exakt `0700`. Der
Launcher verlangt deshalb root-Eigentum für beide sichtbaren Vorfahren und
Runner-Eigentum nur für diesen privaten Root. Das erhält den bestehenden
Runtime-Path-Authority-Validator, belässt die unprivilegierte Provisionierung
unprivilegiert und fügt weder ein generisches Path-Reopen hinzu noch erweitert
es die privilegierte Command-Surface.

Die Non-root-Fixture-Suite des Successors für Launcher, Exact-Gate,
Worker-Traversal, Path-Authority und Runtime-Path-Security bestand 49
fokussierte Tests; `actionlint` mit ShellCheck, Shell-Syntax,
Python-Kompilierung und Whitespace-Checks bestanden ebenfalls. Diese lokalen
Source-/Contract-Ergebnisse sind keine Behauptung eines Sonar- oder
GitHub-hosted-Runtime-Erfolgs. Nach seinem normalen Successor-Push benötigt
der neue exakte Head weiterhin eine frische C17- und verfügbare-Sanitizer-
Bewertung, SonarQube-Cloud-Quality-Gate samt Active-Issue-/Hotspot-Readback,
relevante Checks, alle fünf CRS/no-MRTS-Zellen sowie den nativen
GitHub-hosted-On-/Off-/JSONL-/WAF-/Allow-Lauf.

`FND-PARENT-0078` bleibt `in_progress`; `FND-PARENT-1046` bleibt
`in_progress`; `FND-PARENT-1038` ist unverändert und nicht geschlossen; und
`FND-PARENT-1036` bleibt `blocked_external_dependency`. Functional A bleibt
ein GitHub-hosted-nativer Integrationsnachweis, nicht Protected B oder eine
Attestierung gegen bösartigen Runner- oder VM-root-Code. PR #354 bleibt Draft,
offen und ungemergt.

### 2026-09-06 Zehnter Follow-up (enger nativer Phase-4- und Lifecycle-Kandidat, Successor-Nachweis ausstehend)

Der Predecessor `f5c16f210cd6435a7372ca8d4f8ed10aaa2d9174` ist kein Nachweis
für diesen Kandidaten. Sein Dynamic-Transaction-ID-Pfad erreichte Common mit
einem vom Evaluator hinzugefügten abschließenden NUL, weil
`ngx_conf_set_transaction_id()` `ccv.zero=1` verwendete; Common wies dieses
nicht kanonische Byte korrekt zurück. Die enge NGINX-C-Änderung setzt
`ccv.zero=0`, erhält die strikte Common-Byte-Validierung, kopiert nur die exakt
ausgewerteten Bytes und fügt erst nach dem Kopieren einen eigenen C-Terminator
hinzu. Common-Validierung, Serializer, Redaction, Integrity, WAF-URI,
Dependencies, Framework, MRTS und Gitlink wurden nicht geändert.

Der Kandidat macht außerdem zwei native Lifecycle-Assertions kausal. Bei einem
absichtlich unsicheren Phase-4-Ziel erhält er die erwartete `nginx -t`-
Ablehnung, erfasst die Identität des aktiven Master/Workers und stellt diesem
Master danach direktes HUP zu, statt einen separaten `nginx -s reload`-Parse
als Signallieferung zu behandeln. Beim sicheren Reload verwendet er den
gepinnten, read-only Framework-Synchronized-Upstream über eine dedizierte
`modsecurity off`-ungepufferte Loopback-Route wieder; Paused-Zustand und ein
Client-First-Byte gehen dem Reload voraus, ein exakter alter lebender Nicht-
Zombie-Direktkindprozess und ein anderes Replacement werden aus einem
PID/PPID/State-Snapshot beobachtet, und Release erfolgt erst nach Overlap. Der
Full-Lifecycle-Synchronized-Control-Root wird zusätzlich vor dem Öffnen von
Control- oder Evidence-Dateien durch den Helper unter dem verifizierten Run-
Root autorisiert; ein Out-of-Root-Negativcontrol wird fail-closed abgewiesen.

Frische lokale Kandidatenchecks bestanden: 208 ausführbare NGINX-Contract-
Tests, 53 Native-/Collector-Contracts, Shell-Syntax, Whitespace-Validierung und
ein C17-Compile gegen unterstützte Quellen. Der begrenzte lokale Exact-Gate
bestand beide `modsecurity_use_error_log`-On-/Off-Zellen mit Dynamic-ID-HTTP
200, Phase-4-JSONL, Redaction/Integrity, keiner Query-Canary, Failed-Reload-
Rollback, sicherem FD-Reload, Old-/New-Worker-Overlap, Drain, Descriptor-
Closure und Cleanup. Ein unabhängiger Postpatch-Review fand keinen validierten
Bypass; seine einzige unvalidierte Control-Root-Grenze wurde dem Kandidaten
hinzugefügt und ihr fokussierter Negativtest besteht. Der repositorygestützte
Live-Valgrind-Pfad ist für dieses Artefakt nicht verfügbar: Valgrind ist
installiert, aber der Harness verlangt verifiziertes NGINX `1.31.2` samt
zurückgehaltenem Archiv, während das lokale Kandidatenartefakt `1.31.4` ist;
`scan-build` fehlt. Ein Sanitizer-Erfolg wird nicht behauptet. Auch ein direkter
Full-Lifecycle-Positivversuch wird nicht behauptet: `/var/tmp` wies das
erforderliche Worker-`chown` mit `EINVAL` ab, während die Erzeugung eines
task-eigenen Roots unter `/tmp` `EROFS` lieferte.

Der Kandidat ist ungepusht. Deshalb bleiben alle früheren Hosted-Runs, Checks,
CRS/no-MRTS-Zellen und Sonar-Analysen nur Predecessor-Evidence. Nach einem
normalen Push benötigt der neue exakte Head weiterhin frische hosted NGINX-
On-/Off-/JSONL-/WAF-/Allow- und Lifecycle-Evidence, alle fünf CRS/no-MRTS-Jobs,
erforderliche Checks, SonarCloud-Quality-Gate mit null aktiven PR-Issues und
null Hotspots sowie jeden verfügbaren unterstützten Sanitizer-Pfad.
`FND-PARENT-1048`, `FND-PARENT-1049` und `FND-PARENT-1050` sind lokal `fixed`
mit ausstehender Verifikation; `FND-PARENT-1038` ist unverändert und nicht
geschlossen; `FND-PARENT-1036` bleibt `blocked_external_dependency`. PR #354
bleibt Draft, offen und ungemergt.

### 2026-09-06 Elfter Follow-up (task-eigener Sonar-Successor)

Der normale Successor-Push von
`63487793c62c3407114482f748d6e808cc303f12` erzeugte korrekt frische
Exact-Head-Checks. SonarQube Cloud bewertete sein Quality Gate als `OK`,
meldete aber ein aktives task-eigenes `shelldre:S7679`-Issue in
`connectors/nginx/harness/run_nginx_smoke.sh`: Der kleine Wrapper
`nginx_process_children()` leitete das Positionsargument `$1` direkt weiter.
Der nächste enge Successor weist diesen Wert vor der Übergabe an den bereits
validierten Snapshot-Helper der benannten POSIX-Shell-Variablen
`nginx_children_parent_pid` zu. Das ändert keine Prozess-, FD-, Pfad-,
Request- oder Logging-Semantik und besitzt eine fokussierte
Source-Contract-Regression.

Der neue Commit entwertet notwendigerweise alle noch laufenden Hosted-Ergebnisse
von `63487793` als Successor-Nachweis. Nach seinem normalen Push dürfen nur
Checks, Sonar-Analyse, CRS/no-MRTS-Zellen und NGINX-On-/Off-Runtime-Evidence,
die an seinen eigenen exakten Head gebunden sind, die verbleibenden
Akzeptanzkriterien erfüllen. PR #354 bleibt Draft, offen und ungemergt;
FND-PARENT-1036 bleibt `blocked_external_dependency` und FND-PARENT-1038
bleibt unverändert.

### 2026-09-06 Zwölfter Follow-up (eingegrenzter Pre-Merge-Gate-Kandidat)

Dieser Kandidat ergänzt eine separat gebaute, statisch gelinkte reine NGINX-Test-Fixture für die
bestehende P4-Body-Limit-Grenze. Sie gibt echte Memory-, file-only- und
gemischte `ngx_buf_t`-Zustände durch den installierten Connector-Filter aus,
deckt die Kontrollen innerhalb des Limits und Reject-before-forwarding ab und
übt Fehlerpfade für Datei-Metadaten, fehlende Quelle, Read, Short-Read und
Request-Pool-Allokation aus. Die Fixture wird nicht in das Produkt gelinkt. Es
war keine Produkt-C-Korrektur nötig: Der aktuelle Source nutzt den Common-
Reject-Plan vor dem nativen Forwarding und kehrt bei jedem getesteten Fehlerpfad
vor dem Downstream-Filter zurück. Die ausgewählte 64-Bit-Laufzeit kann den
separaten `file_length > SIZE_MAX`-Zweig nicht darstellen; der Runner zeichnet
diese Grenze auf, statt eine künstliche Overflow-Ausführung zu behaupten.

Für FND-PARENT-1047 validieren erfolgreiche Envoy-, Lighttpd- und Traefik-
Zellen jetzt ihre jeweils eigene normalisierte Evidence, bevor sie nur diese
Evidence hochladen. Eine nicht erfolgreiche generische oder Apache-Zelle
veröffentlicht ausschließlich eine begrenzte, no-follow-geschützte One-shot-
Fehlerquittung, sodass kein veraltetes oder partielles PASS-Bundle als ihr
Failure-Artefakt hochgeladen werden kann. Apache behält seinen echten Apache-
Result-Pfad; HAProxys separater Projektorpfad bleibt unverändert. Das aktuelle
Audit zu FND-PARENT-1046 führt den historischen Kandidatenlauf `ad193b...` nur
als partielle funktionale Evidence: Er behielt kein JSONL-Artefakt auf
Feldebene und ist weder Nachweis für diesen Successor noch die von
FND-GITHUB-0009 verlangte unabhängige Protected-Host-Evidence.

Der NGINX-Functional-A-Workflow des Successors bereitet jetzt vor der
begrenzten Root-Übergabe genau ein frisches, Runner-eigenes privates
Staging-Verzeichnis vor. Erst nachdem beide echten On-/Off-Zellen sowie ihre
JSONL-, Raw-WAF-, Callback-, Lifecycle-, Artifact-Identity- und Allow-Control-
Assertions bestanden haben, erzeugt ein no-follow-basierter One-shot-Writer
ein begrenztes kanonisches `result.json`. Es enthält den exakten Parent-Head,
den gepinnten NGINX-Archiv-Digest/die Version, rollenbezeichnete
Build-Identitäten und die erforderlichen Boolean-/Count-Fakten, schließt aber
Raw-Logs, Request-Targets, Canary-Daten, Nutzlasten, Transaktionskennungen,
Zeitstempel und absolute Pfade aus. Dies bleibt kandidaten-eigene
Integrations-Evidence für FND-PARENT-1046 und ist keine unabhängige
Protected-Host-Attestation für FND-GITHUB-0009.

Zum Commit-Zeitpunkt dieses Records sind die fokussierten lokalen Contracts,
der C-Fixture-Compile, Workflow-Lint und Whitespace-Checks nur aktuelle
Kandidaten-Evidence. Der neue saubere Exact-Head-Native-Lauf, normaler Push,
GitHub-hosted-Successor-Checks, Sonar-Readback, Five-Cell-CRS/no-MRTS-
Artifact-Readback sowie die getrennte Protected-Base-/Host-Owner-Entscheidung
bleiben erforderlich. Es wird kein Merge, kein Draft-Wechsel, Rebase,
Force-Push, Risk Acceptance, Framework-/MRTS-/Gitlink-/Dependency-Change und
keine Abschwächung von Tests, Sonar oder Quality Gates behauptet.

### 2026-09-06 Dreizehnter Follow-up (isolierter Runner-Root der nativen Fixture)

Der Exact-Head-NGINX-Workflow `34037807569` für
`2dba14da707216652227709e79bf73d58a6c8ba6` bestand Checkout,
Head-Verifikation, Preflight, Provisionierung und die echten Functional-A-
On-/Off-Kontrollen. Anschließend schlug sein privater `nginx -t`-Test der
nativen Body-Buffer-Fixture fail-closed mit der begrenzten Klasse
`permission_denied` und dem SHA-256 des Konfigurationsoutputs
`cf980554148465c1143c6be9dc8043b7543c4093d49d5b6518bb30d8f54d3486` fehl.
Beide Uploads wurden korrekt übersprungen; dieser Lauf liefert daher weder ein
Native-Fixture- noch ein Functional-A-Artefakt. Der gleichzeitig exakte
CRS/no-MRTS-Lauf `34037807658` bestand alle fünf Zellen einschließlich des
streng zurückgelesenen Lighttpd-Artefakts, ist nach dieser Successor-Änderung
aber Predecessor-Evidence.

Eine kontrollierte Non-root-Reproduktion zeigt keinen Produktdefekt. Common
sicherer Event-File-Parent-Walk öffnet jede Komponente mit
`O_RDONLY|O_DIRECTORY|O_NOFOLLOW`; er kann den root-eigenen, nicht
auflistbaren Functional-A-Vorfahren mit `0711` korrekt nicht lesend öffnen,
obwohl gewöhnliche Pfadtraversierung möglich ist. Derselbe Fixture-
Konfigurationstest gelingt mit einem Output-Root als direktem runner-eigenem
`0700`-Kind des verifizierten root-eigenen sticky `/tmp`. Common-No-follow-,
Owner- und Private-Leaf-Prüfungen bleiben unverändert.

Der eng begrenzte Successor erzeugt diesen Native-Fixture-Root mit einem
unprivilegierten `mktemp` direkt unter dem bereits geprüften `/tmp`, validiert
festen Namespace, Nicht-Symlink-Typ, Runner-UID:GID-Eigentum und Modus `0700`
und übergibt ihn ausschließlich an die native Fixture. `FUNCTIONAL_JOB_ROOT`,
seine root-eigene `0711`-Vorfahrenschaft, `RUN_ROOT`, der Functional-A-
Evidence-Root, Common und Produkt-C bleiben unverändert. Der Artefakt-Upload
akzeptiert weiterhin nur das vorhandene begrenzte `result.json` und schlägt bei
seinem Fehlen fehl. Dies fügt keine Runner-, Privileg-, Dependency- oder
Permission-Policy-Änderung hinzu.

Der Successor verlangt frische lokale und GitHub-hosted-Exact-Head-Evidence,
einschließlich SonarCloud-Readback, aller erforderlichen Repository-Checks,
beider NGINX-Artefakte und aller fünf CRS/no-MRTS-Zellen. PR #354 bleibt Draft,
offen und ungemergt; diese kandidaten-eigene Evidence bleibt von der für
`FND-GITHUB-0009` nötigen Protected-Host-/Collector-Entscheidung getrennt.

### 2026-09-06 Vierzehnter Follow-up (Current-Base-Refresh und begrenzte Ausnahme)

Der aktuelle Nutzer autorisierte ausdrücklich einen normalen Merge des
aktuellen `origin/master` in den bestehenden PR-#354-Arbeitsbranch, ohne
Rebase, Force-Push, direkten Default-Branch-Write,
Framework-/MRTS-/Gitlink-/Dependency-Änderung oder Abschwächung von Tests bzw.
Qualitätskontrollen. Der Merge des aktuellen Masters
`9925ef647b5fb49d21aebd658a658d4fdb649c58` war konfliktfrei. Er erhält den
Current-Master-NGINX-Common-Adoption-Checker, seine Regressionssuite und seinen
gepaarten Change Record, während die PR-#354-Remediation-Pfade erhalten
bleiben. Der resultierende Successor verlangt weiter einen normalen Push,
exaktes Remote-Readback und frische Evidence; kein Predecessor-Ergebnis wird
promotet.

Um `2026-09-06T19:30:15Z` akzeptierte der aktuelle Nutzer zudem nur das
Restrisiko aus `FND-GITHUB-0009`: Vom PR ausgewählte funktionale GitHub-CI ist
keine unabhängige Protected-Host-Attestierung. Das kanonische Finding lautet
nun ausschließlich für eine reguläre PR-#354-Integration `accepted_risk`, nicht
fixed, verified oder closed; seine technische
Base-/Environment-/Runner-/Host-Gate-Arbeit bleibt offen. Die Ausnahme bindet
erst nach frischer Validierung und Rücklesung einer finalen vollständigen
Successor-SHA unmittelbar vor einem regulären GitHub-Squash-Merge. Sie behauptet
weder unabhängigen Hostnachweis, externes Seal noch allgemeine Fehlerfreiheit
und akzeptiert kein weiteres Finding, keinen Defekt, keinen fehlgeschlagenen
Pflichtcheck, kein Sonar-Issue/Hotspot, keinen ungelösten Review, keinen
Ruleset-Fehler, keinen Bypass, keine Veröffentlichung und keinen späteren Head.

Die geltende Integrationspolicy verlangt außerdem eine 24-zeilige
Connector-Profil-Bewertung. Das unabhängig revalidierte `FND-CROSS-0004` bleibt
ein separater, nicht risikakzeptierter Release-Blocker: Das Framework besitzt
jetzt den Five-Connector-CRS-Fixture-/Katalogvertrag und der PR fünf
With-CRS/No-MRTS-Zeilen, aber der Parent-Workflow ruft weder den
Framework-Aggregate-Befehl auf noch bewahrt er ein exaktes Five-Parent-
Aggregate-Artefakt für die fünf Parent-Zellen auf. Damit bleibt sein Kriterium
für ein geschlossenes Parent-Profil unerfüllt. Diese Aufgabe ändert diese Infrastruktur nicht und
wertet ein partielles Five-Row-Ergebnis nicht als Aggregate-PASS. Der frische
Successor bewahrt die erforderlichen fünf Row-Level-Ergebnisse und eine
vollständige 24-zeilige Bewertung auf; bis der unabhängige Blocker unter
separater Autorisierung behoben ist, bleibt PR #354 Draft und darf nicht
gemergt werden.

### 2026-09-06 Fünfzehnter Follow-up (HAProxy-Sicherheitsvertragsabgleich)

Die Validierung des aktuellen Successors fand fünf veraltete lexikalische
Assertions in zwei repositoryeigenen statischen HAProxy-Checkern, keinen
Produktregressionsfehler. Der Source war bereits in `2b3d7f7f` gehärtet:
Eine Anfrage verlangt genau einen gültigen, nichtleeren empfangenen `Host`,
mappt `hostname` ausschließlich aus diesem Host und verwirft beziehungsweise
bereinigt einen fehlenden oder ungültigen Host vor der Transaktionsallokation.
Ein älterer Checker verlangte weiterhin einen überholten `server_ip`-Fallback
für `hostname`. Sein aktualisierter Vertrag verbietet nun diesen Fallback und
fordert den validierten Host-Reject- und Cleanup-Pfad. Die ausführbare
C17-Mapper-Fixture verwirft nun zusätzlich eine Anfrage ohne Header und einen
leeren `Host`, während der gültige Host-Kontrollfall erhalten bleibt.

Der HTX-Overlay-Checker behielt ebenfalls vier Schreibweisen für Felder und
Funktionsgrenzen vor dem Hardening. Er folgt nun dem Dispatcher in den echten
Request-Header-Helper und den verschachtelten Lifecycle-Feldern und bewahrt
damit die exakten Invarianten: P1 beginnt vor der Registrierung des
Request-Payloads, P2 und P4 markieren EOS vor ihrem jeweils einzigen
Binding-Finish-Aufruf, und eine P2-Native-Reply ist nur vor Response-Headern
möglich. Weder Produktions-C noch Host-Verhalten, Workflow, Gate, Framework,
MRTS, Gitlink, Dependency oder Teststrenge wurden abgeschwächt. Zwei
unabhängige Security-Reviews fanden keinen verbliebenen Bypass oder Regression
des gültigen Host-Pfads. Die fokussierte Checker-/HTX-/C17-Suite und 34 direkte
HAProxy-Contracts bestanden; der finale Successor erfordert dennoch normalen
Push, exaktes Readback und frische Hosted-Evidence, statt dieses
Vorgängerergebnis zu promoten.

### 2026-09-06 Sechzehnter Follow-up (finale Dokumentations-Head-Disposition)

Diese gepaarte Dokumentationsaktualisierung ist der nächste reguläre
PR-#354-Successor. Sie verändert weder Produktverhalten, Tests, Workflows,
Framework, MRTS, einen Gitlink, eine Dependency, eine Policy noch eine
erforderliche Kontrolle. Ihre eigene exakte SHA und der frische
GitHub-/Sonar-/Runtime-Ergebnis-Readback müssen nach ihrem normalen Push
festgehalten werden; kein Vorgänger-Run wird zu diesem Dokumentations-Head
promotet.

Die begrenzte FND-GITHUB-0009-Ausnahme bleibt `accepted_risk` nur für eine
künftige reguläre PR-#354-Integration, nachdem alle nicht ausgenommenen
Bedingungen bestehen. Sie ist weder fixed, verified oder closed noch
verbraucht: Der unabhängige FND-CROSS-0004-`P1`-Release-Blocker verhindert
zuvor jeden Merge. Die aufbewahrte 24-Zeilen-Bewertung hat fünf bestandene,
sechs blockierte und dreizehn nicht ausgeführte Zellen, und das erforderliche
Parent-Exact-Five-Aggregat-Artefakt fehlt. Daher bleibt PR #354 offen und
Draft, es wird kein GitHub-Merge versucht und es gibt keine
Resulting-Master-Checks oder Release-Aktionen zu berichten.

### 2026-09-07 Siebzehnter Follow-up (Parent-Exact-Five-With-CRS/no-MRTS-Kandidat)

Dieser Parent-only-Kandidat startet vom PR-#354-Head
`3054e43ed9082a953e718ce2341bc7e9fc43b3a7` und der geprüften Base
`9925ef647b5fb49d21aebd658a658d4fdb649c58`. Er ergänzt einen separaten
versionierten `with-crs-no-mrts`-Vertrag, statt das bestehende geschlossene
`no-crs`-Profil zu ändern oder umzubenennen. Der neue Producer bindet jede
ausgewählte Apache-, HAProxy-, Envoy-, Lighttpd- und Traefik-Zelle an
Schemaversion, exakten Parent/Base, workflow-eigene Profil- und Zellrun-IDs,
GitHub-Run/Versuch, Framework-/MRTS-/CRS-Provenance, tatsächlich ausgeführten
Fall, Originalartefaktpfade und deren Hashes. Der strikte Aggregator akzeptiert
genau eine descriptor-sichere, kanonische Zelle je erwartetem Connector und
weist fehlende, doppelte, fremde, umbenannte, identitätsgemischte,
hashveränderte, unsichere oder unvollständige Evidence ab.

`functional-facts.json` enthält jetzt `source_files_sha256`, den SHA-256-Digest
der kanonischen JSON-Darstellung der geordneten Quellartefaktliste. Das
Aggregat berechnet diesen Digest erneut und weist Receipts zurück, deren
Quellpfade oder Hashes abweichen. Damit ist die Kette Quellliste → Fakten →
Receipt → Manifest gebunden, ohne externe Quellenauthentizität zu behaupten.

Candidate-Review stellte außerdem fest, dass kanonische Syntax allein am
Aggregat-Sink keine exakten JSON-Primitivtypen verlangte: Python-Gleichheit
ließ wertgleiche `true`/`1`-, `403.0`/`403`- und `0`/`false`-Ersetzungen in
einer neu gepackten Zelle zu. Das Aggregat vergleicht Schema-, Manifest-,
Receipt-/Fakten-, Block-/Allow- und No-MRTS-Strukturen jetzt rekursiv mit
exakten Typen. Diese enge Reparatur wird als FND-PARENT-1061 verfolgt und weist
die reproduzierten Mutationen ab, ohne legitime JSON-Boolean oder -Float global
zu verbieten.

Der gleiche Abschlussreview fand eine eigene Apache-Producergrenzen-Lücke:
Summary-/JSONL- und Cleanup-Receipt-Skalare konnten `true`/`1` oder
`403`/`403.0` akzeptieren, bevor der Producer typisierte Fakten neu erzeugte.
Der Apache-lokale Vergleich exakter Skalare weist die sechs reproduzierten
Ersetzungen jetzt ab, bevor Fakten oder eine Receipt publiziert werden,
während der vollständige typisierte Quellcontrol gültig bleibt. Dies ist
FND-PARENT-1062, ein nur im Kandidaten beobachteter Quellvertrags-/Evidence-
Integrity-Befund; sein Raw-Audit bindet weiterhin getrennt Anfrage, HTTP `403`
und Regel `942270`, sodass kein Connector-Runtime-Bypass behauptet wird. Er
bleibt bis zum Exact-Successor-Hosted-Apache-/Aggregate-Readback `in_progress`.

Der Kandidat rendert eine vollständige, ehrliche aktuelle 24-Zeilen-
Disposition: Fünf ausgewählte With-CRS/no-MRTS-Zellen können nur aus den fünf
validierten Receipts `passed` sein; die sechs nicht verfügbaren
Envoy-/Lighttpd-/Traefik-MRTS-Routen bleiben `blocked`; die verbleibenden
dreizehn Zellen bleiben `not_run`. Das Aggregat trennt technische Gültigkeit,
das funktionale Five-Cell-Ergebnis, Dispositionsvollständigkeit und
verbleibende Integrationsbedingungen. Dieser Renderer und seine synthetischen
Fixtures sind kein Hosted-Ergebnis und schreiben die historischen
`3054e43...`-Zellartefakte nicht dem Successor mit diesem Record zu.

Für Apache prüft der neue Profilpfad eine rohe Serial-Transaktion, gebunden an
die ausgewählte Anfrage, HTTP `403` und CRS-Regel `942270`. Er schreibt eine
No-Follow-One-Shot-Cleanup-Receipt erst nach begrenzten Host-/Helperprozess-,
ausgewählten Listener- und PID-Datei-Prüfungen, und der Workflow liefert
`RUN_ONE_CASE=1` mit aktueller Zell-/Run-/GitHub-Identität ausdrücklich. Der
Producer prüft zudem jeden erforderlichen Apache-Summary-/JSONL-Skalar und jede
Cleanup-Receipt-Identität mit exakten JSON-Primitivtypen, bevor er Fakten
normalisieren kann. Für HAProxy liest das Profil die bestehende versiegelte
Stage über ihren strikten Verifier unter Verwendung der getrennten
Workflow-Evidence-UID/GID; es kopiert oder labelt diese Stage weder um. Sein
projizierter Quell-Receipt und das
versiegelte Paket enthalten jetzt zudem die vom Parent vergebene `cell_run_id`
mit `cell_run_id_kind: workflow_cell`. Der Workflow reicht dieselbe ID aus
`CRS_RUNTIME_RUN_ID` durch Projektion und Verifikation weiter; fehlende oder
abweichende IDs werden abgewiesen. Dies ist eine Workflow-Bindung und keine
Behauptung einer nativen HAProxy-Run-ID. Candidate-Review identifizierte die
Apache-False-Complete-Cleanup-Grenze, den fehlenden Selected-Case-Handoff und
die Quelllisten-/HAProxy-Zellbindungs-Lücke vor der Delivery. Sie werden lokal
als FND-PARENT-1058, FND-PARENT-1059 und FND-PARENT-1060 verfolgt, alle
`fixed` mit ausstehender Exact-Successor-Hosted-Verifikation; die frühere
Raw-Observation-Lücke bleibt FND-PARENT-0218 und wird nicht still geschlossen.

Frische lokale Kontrollen bestanden: 104 Profil-, Apache-, HAProxy- und
Workflow-Tests (11 Environment-Skips); 17 geschützte No-CRS-Contract-Tests;
67 aktuelle Runtime-Observation-Contract-Tests; Apache-/HAProxy-Shell-Syntax;
ausgewählte Python-Kompilierung; 22 zweisprachige Dokumentationstests; und
`git diff --check`. Der frühere breitere 141-Test-Runtime-/Observation-Lauf
liegt vor der engen Apache-Skalaränderung und wird nicht als deren direkte
Kontrolle dargestellt. Erwartete negative Fixtures drucken ihre internen
`FAIL:`-Diagnosen, während ihre Testprozesse erfolgreich enden. Vollständige
Bilingual-/Link-Make-Targets bleiben ausschließlich durch die vorhandenen
nicht verfügbaren Framework-Submodul-Targets environment-blocked und werden
nicht als bestanden berichtet. Kein Framework-, MRTS-, Gitlink-, Dependency-,
Policy-, Ruleset-, Test-, Sonar- oder Quality-Gate-Change ist Teil dieses
Kandidaten.

Bei dieser Record-Revision wurde kein neuer Head gepusht. Ein normaler
Commit/Push auf den bestehenden PR-#354-Branch, exaktes Remote-/PR-Head-
Readback, ein frischer GitHub-hosted-Five-Cell-Profillauf, Child-Receipt- und
Aggregate-Artefakt-Readback, aktuelle erforderliche Checks,
SonarCloud-Quality-Gate-/Issue-/Hotspot-Readback und Review-Disposition bleiben
erforderlich. FND-CROSS-0004 bleibt `blocked`, bis seine bestehenden
Akzeptanzkriterien tatsächlich erfüllt sind; PR #354 bleibt Draft und
ungemergt.

### 2026-09-07 Achtzehnter Follow-up (Reparatur des ersten Exact-Five-Fehlschlags)

Der erste ausgelieferte Exact-Five-Head
`8f91f70ce8f1bdf6167aa5e1aa386fe18df0fa50` wurde ausschließlich durch den
frischen GitHub-hosted-Workflow `34140286420`, gebunden an die geprüfte Base
`9925ef647b5fb49d21aebd658a658d4fdb649c58`, ausgeführt. Er schlug
fail-closed fehl und ist nur negative Evidence: Die vier Nicht-Apache-
Producer wiesen den gepinnten CRS-Source zurück, weil seine gültige
JSON-ähnliche Regelform den quoted Key `"id":942270` verwendet; Apache
fehlte die vom Evidence-Validator verlangte rohe serielle Audit-Datei; und das
Aggregat wies nicht verfügbare Upstream-Zellen korrekt zurück. Dies belegt
weder einen CRS-HTTP-Blockfehler noch wird ein Failure-Receipt zu einer
bestandenen Zelle promoviert.

FND-PARENT-1063 engt den CRS-Identity-Matcher auf die tatsächlich gepinnte
quoted Form und die etablierte unquoted Form ein, erhält aber exakte
Descriptor-, Digest- und Commit-Prüfung und weist getestete Near-Misses ab.
FND-PARENT-1064 hängt nur für das Profil Apache-Serial-/Native-
Auditdirektiven mit den Teilen `ABFHZ` nach Fallmaterialisierung und vor dem
Start an, ausschließlich für ein vollständiges ausgewähltes With-CRS-Profil.
No-CRS sowie unvollständige oder Nichtprofilpfade bleiben außerhalb dieses
Append. Framework, MRTS, Gitlink, Dependency, Workflow-Policy oder bestehende
Kontrollen wurden nicht verändert.

Ein verpflichtendes unabhängiges Review stellte anschließend fest, dass die
neue generierte `SecAuditLog`-Senke ihren abgeleiteten Pfad als Apache-
Konfigurationsdaten behandeln muss. FND-PARENT-1065 hält die payload-sichere
Quote-/Newline-Direktivensplit-Reproduktion und den getrennten Fall der
Apache-Konfigurationsvariablenexpansion fest. Der nur profilgebundene Guard
weist jetzt Quote, Backslash, Dollarzeichen und POSIX-Steuerzeichen vor Append
oder Serverstart ab. Seine echte extrahierte Shell-Regression akzeptiert einen
normalen absoluten Pfad mit Leerzeichen/normaler Interpunktion und weist
Quote-/Newline-, Backslash- und Expansionsinputs fail-closed ab. Das ist eine
enge Reparatur der neuen Senke; ein lokaler Apache-configtest oder
Runtime-Akzeptanz wird nicht behauptet.

Der Kandidat enthält zudem enge Source-Refactorings für FND-SONAR-0079 ohne
Suppression, Quality-Gate-Änderung oder semantische Abschwächung. Das frühere
SonarCloud-Ergebnis auf `8f91f70...` bleibt fehlgeschlagen (Quality Gate
`ERROR`, 44 aktive offene Issues, keine reviewbaren Hotspots), daher ist ein
frisches SonarCloud-Ergebnis für den Successor erforderlich und hier wird kein
grünes Ergebnis behauptet.

Nach der finalen Path-Guard-Änderung bestand die kombinierte betroffene
Parent-Suite `265` Tests mit `11` bestehenden Environment-Skips. Sie deckt
CI-Security, den Apache-Profilguard, HAProxy-Projection-/Workflow-/Harness-
Contracts, With-CRS-Producer-/Aggregate-/Runtime-Contracts,
Runtime-Observations und die geschützten No-CRS-Profil-/Workflow-Contracts ab.
Erwartete Negative-Fixture-Diagnosen werden innerhalb erfolgreich endender
Tests ausgegeben. Ein frischer normaler Commit/Push, exaktes
Remote-/PR-Head-Readback, Hosted-Five-Cell-/Aggregate-Artefaktvalidierung,
aktuelle erforderliche Checks und Exact-Successor-SonarCloud-Readback bleiben
verpflichtend. PR #354 bleibt Draft und ungemergt; FND-CROSS-0004 bleibt bis zu
seinen bestehenden Akzeptanzkriterien `blocked`.
