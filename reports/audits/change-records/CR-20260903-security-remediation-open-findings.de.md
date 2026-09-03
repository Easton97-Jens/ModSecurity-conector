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

Die Implementierung portiert ausschließlich die auf der aktuellen Basis benötigten Sicherheitskontrollen. Historische breite PRs sind Referenzevidence, keine Merge-Quellen. Der Authorization-Port schließt nicht zugehörige Duplicate-Host-Validierung und SIGPIPE-Strategieänderungen aus. Die NGINX-Konfigurationsreferenz wird aus einer NGINX-spezifischen Metadata-Überschreibung erzeugt, sodass englische/deutsche Dateien und das kanonische Konfigurationsinventar quellenbasiert statt manuell divergent bleiben. Hosted-Lighttpd-Feedback zeigte anschließend, dass sein Runtime-Harness noch eine rohe Query-URI im JSONL erwartete; der Harness erwartet nun die sichere serialisierte URI und `redacted=true`, während rohe Curl-Wire- und korrelierte CRS-Log-Evidence erhalten bleiben.

## Geänderte Dateien

- Common-Runtime und Event-Serialisierung: common/include/msconnector/event.h, common/src/event.c, common/src/integrity_event.c und common/runtime/http_authorization_service.c.
- Connector-Implementierung: connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c, connectors/nginx/src/ngx_http_modsecurity_log.c und connectors/traefik/src/traefik_engine_service.c.
- Fokussierte Regressionen: tests/event_json_query_redaction_test.c, tests/haproxy_spop_request_target_test.c, tests/test_haproxy_spop_request_target.py, tests/http_authorization_service_detached_worker_smoke.c, tests/test_http_authorization_service_worker_contract.py, tests/test_nginx_error_log_callback_contract.py und tests/test_traefik_engine_service_contract.py.
- Lighttpd-Runtime-Redaction-Regression: connectors/lighttpd/harness/run_patched_full_lifecycle.sh und connectors/lighttpd/tests/test_patched_host_contract.py.
- Quellenbasierte Dokumentation/Inventar: ci/checks/documentation/connector_config_reference.py, examples/nginx/configuration-reference.md, examples/nginx/configuration-reference.de.md und reports/connector-configuration-inventory.json.
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
| Authorization-Timeout, Detached-Worker-Smoke, ASan/UBSan und TSan | Bestanden. Der konfigurierte Late-Quiescence-Companion-Zweig ist statisch abgedeckt; ein dynamisches Host-Companion-Fixture existiert nicht. |
| Envoy-Modulgraph, Go-Test und Go-vet | Bestanden; Modulgraph meldet google.golang.org/grpc v1.83.1. |
| Traefik-Contracts/native-plugin/Authorization-Worker-Contracts | Bestanden: 47 Tests. |
| Traefik-C17-Syntax und Engine-Service-Build/Selbsttest/Runtime/Negativtest | Bestanden mit GCC- und Clang-Syntaxchecks; normale, ASan/UBSan- und TSan-Engine-Service-Läufe bestanden. |
| Lighttpd-JSONL-Redaction-Harness-Contract | Bestanden: 37 Tests (2 übersprungen) und `bash -n`. Ein erster Hosted-Lighttpd-Runtime-Lauf deckte seine veraltete rohe-URI-JSONL-Erwartung auf; die eingegrenzte Harness-Korrektur bewahrt die rohe Wire-/CRS-Korrelation und verlangt `/?<redacted>` mit `redacted=true`. |
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
für den aktualisierten JSONL-Harness-Contract; ihr Rerun steht auf dem
aktuellen Draft-PR-Head noch aus.

## Nicht ausgeführte Prüfungen mit Begründung

NGINX-C17-Host-Kompilierung/-Runtime ist durch fehlende lokale NGINX-
Header/-Quellen blockiert. Vollständige Bilingual- und Link-Checks sind nur
durch vorhandene fehlende Framework-Submodul-Targets blockiert; keine
Framework-Initialisierung oder -Änderung ist autorisiert. Vollständige
HTTP/1.1-, HTTP/2- und HTTP/3-Host-Matrizen benötigen lokale Host-Fixtures, die
nicht vorhanden sind.

## Bekannte Einschränkungen

Ein konfigurierter Authorization-Companion hat statische Lifecycle-Contract-
Abdeckung, aber kein dynamisches Late-Quiescence-Fixture. Der lokale Traefik-
Service-Test übt keinen Traefik-Hostprozess aus. Dies sind Evidence-Grenzen,
keine Behauptung deaktivierter Sicherheitskontrollen.

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
- Der erste Hosted-Lighttpd-Lauf zeigte eine veraltete Harness-Erwartung für
  JSONL mit Query in der rohen URI. Die eingegrenzte Korrektur korreliert das
  sichere redigierte Event über die Response-Transaction-ID und bewahrt rohe
  Wire- und CRS-Evidence.
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

Der Nachfolge-Commit, GitHub-Read-back, die frische Sonar-Analyse, der
vollständige Exact-Head-Runtime-Workflow einschließlich Hosted-NGINX-Gate
sowie der abschließende Read-back von PR-Beschreibung und Change Record stehen
zum Zeitpunkt dieses Eintrags noch aus. Es wird weder ein Merge, Force-Push,
Framework-/MRTS-/Gitlink-Change noch eine Abschwächung von Tests oder
Workflows autorisiert oder behauptet.
