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
| Delivery-Status | Lokale Remediation und fokussierte Validierung sind abgeschlossen. Dieser Record behauptet keinen Commit, Push, Draft-PR, Hosted-Check oder Merge. |

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

Die Implementierung portiert ausschließlich die auf der aktuellen Basis benötigten Sicherheitskontrollen. Historische breite PRs sind Referenzevidence, keine Merge-Quellen. Der Authorization-Port schließt nicht zugehörige Duplicate-Host-Validierung und SIGPIPE-Strategieänderungen aus. Die NGINX-Konfigurationsreferenz wird aus einer NGINX-spezifischen Metadata-Überschreibung erzeugt, sodass englische/deutsche Dateien und das kanonische Konfigurationsinventar quellenbasiert statt manuell divergent bleiben.

## Geänderte Dateien

- Common-Runtime und Event-Serialisierung: common/include/msconnector/event.h, common/src/event.c, common/src/integrity_event.c und common/runtime/http_authorization_service.c.
- Connector-Implementierung: connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c, connectors/nginx/src/ngx_http_modsecurity_log.c und connectors/traefik/src/traefik_engine_service.c.
- Fokussierte Regressionen: tests/event_json_query_redaction_test.c, tests/haproxy_spop_request_target_test.c, tests/test_haproxy_spop_request_target.py, tests/http_authorization_service_detached_worker_smoke.c, tests/test_http_authorization_service_worker_contract.py, tests/test_nginx_error_log_callback_contract.py und tests/test_traefik_engine_service_contract.py.
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
| Directive Parity | Bestanden. |
| Vollständige Bilingual-/Link-Checks | Ausschließlich durch vorbestehende fehlende Framework-Submodul-Link-Targets blockiert; die Aufgabe initialisiert oder verändert das Framework nicht. |

## Security-Auswirkung

Die Änderungen reduzieren Request-Target-Ambiguität, Offenlegung von Query-Werten, Umgehungen der Logging-Konfiguration, lokale UDS-Ressourcenerschöpfung und das Risiko asynchroner Use-after-free-/Double-Release-Fehler. Event-JSONL-Redaktion gilt für neu ausgegebene Records; Betreiber müssen historische JSONL- und Audit-Logs als potenziell sensitiv behandeln und nach lokaler Policy beschränken, rotieren oder aufbewahren. Es wurde kein Produktionsdienst kontaktiert und kein echtes Credential, Cookie, Token, Passwort oder personenbezogenes Datum in Tests oder Evidence verwendet.

## Runtime-Evidence

Der lokale Traefik-Engine-Service wurde gebaut und über einen privaten
Unix-Socket für normale, fehlerhafte-Frame- und Socket-Ownership-Negativ-
Kontrollen ausgeführt. Dies ist kein Traefik-Host-Runtime-Test. Es wurde kein
Produktionsdienst kontaktiert.

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
dieser Redaktionsänderung ausgegeben wurden. Exact-Head-Hosted-CI, SonarCloud,
Review und jede Merge-Entscheidung sind separate zukünftige Evidence. Es wird
kein Merge angefragt oder durchgeführt.

## Finaler Diff- und Review-Status

In Bearbeitung, bis der dokumentierte finale Diff auf dem Task-Branch committed
und aus Task-Branch und Draft PR zurückgelesen ist. Der aktuelle Benutzer
autorisiert nur einen normalen Task-Branch-Push und Draft PR; Merge, Force-
Push, Rebase veröffentlichten Works und Default-Branch-Writes bleiben nicht
autorisiert.
