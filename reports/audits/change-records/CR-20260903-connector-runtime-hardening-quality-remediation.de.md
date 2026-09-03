# Change Record CR-20260903-connector-runtime-hardening-quality-remediation

**Sprache:** [English](CR-20260903-connector-runtime-hardening-quality-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260903-connector-runtime-hardening-quality-remediation |
| Datum (UTC) | 2026-09-03 |
| Basis-Revision | 95bc04203455bc74a9cd18fafc6fb5848af2bbb2 (`origin/master`) |
| Auslieferungsstatus | In Arbeit auf `codex/connector-runtime-hardening-20260824`; Draft PR [#346](https://github.com/Easton97-Jens/ModSecurity-conector/pull/346). Kein Remediation-Commit, Push-Ergebnis, Exact-Head-Hosted-Ergebnis oder Merge wird behauptet. |

## Motivation und Problemstellung

Diese Parent-only-Remediation bearbeitet die aktuellen Codex-Review-Findings,
SonarQube-Cloud-Quality-Gate-Fehler und roten Connector-Workflow-Nachweise für
Runtime-Fehler-, Timeout-, Cancel-, Protokoll- und Cleanup-Pfade. Der
anfängliche Hosted-Stand enthielt einen Apache-Runtime-Fehler, einen
Heading-Fehler der zweisprachigen Dokumentation und einen SonarQube-Cloud-Gate-
Fehler (`new_security_rating=3` und `new_duplicated_lines_density=4.5`).

## Akzeptanzkriterien

- Die erkannten Connector-Runtime- und Cleanup-Fehler werden behoben, ohne
  Fail-Closed-Kontrollen zu schwächen oder CI-/Governance-Inputs zu ändern.
- Legitime Allow-/Block-Verhalten bleiben erhalten und jede geänderte Grenze
  erhält Trigger- und Kontrollregressionen.
- Die erkannten Sonar-New-Code-Sicherheits- und Duplikationsursachen werden
  ohne Suppressions, Exclusions oder Quality-Gate-Änderungen entfernt.
- Englische/deutsche leserorientierte Dokumentation und Change-Record-Paar
  bleiben materiell gleichwertig.
- Nach einem normalen Push werden frische Exact-Head-GitHub-Actions- und
  SonarQube-Cloud-Nachweise erhoben; bis dahin bleibt die Auslieferung offen.

## Implementierungsentscheidung und Begründung

Die Remediation korrigiert Apache-Listener-Inode-Parsing und private
Artefaktbehandlung; Common-Event-Double-Escaping von Protocol-Werten sowie
verlustfreie JSONL- und Integritätskettenbehandlung; Traefik-Cleanup über
stabile Worker-Slots; Lighttpd-Helper-Artefakt-, Endpoint-, Executable- und
Zombie-Session-Behandlung; Envoy-ext_proc-absolute Stream-Lifetime, Cancel und
begrenzte Post-Send-Evidence nach einer bestätigten Antwort an der
Lifetime-Grenze; sowie die zwei bilingualen Heading-Hierarchien.

Für HAProxy SPOE/SPOP verwendet die Remediation geprüfte `MSG_NOSIGNAL`-
Full-Write-Pfade, terminale Peer-lokale Fehlerbehandlung und ratengelimitierte
Fehler-Evidence, abgetrennte begrenzte Peer-Worker, sofortiges Schließen bei
ausgeschöpfter Peer-Zulassung, strikte Worker-/Transaktionsgrenzen und
fail-closed Protokoll-Outcomes. Ein Response-NOTIFY bei deaktivierter
Response-Verarbeitung erzeugt das dokumentierte 503-Ergebnis vor der
Transaktionsverarbeitung; fehlerhaftes NOTIFY und fehlende
Response-Korrelation bleiben auch in `mode=detect-only` disruptiv. Gültige
Engine-Allow-/Block-Entscheidungen behalten ihre konfigurierte Mode-Semantik.
Der quellenbasierte Konfigurationsrenderer dokumentiert nun, dass
`response-body-timeout` nur bei `response-companion=none` null sein muss.

Der Umfang ist auf Parent-Source, Tests, Connector-Dokumentation,
Beispielkonfiguration und diesen Record begrenzt. Er enthält keine Änderung an
CI-Workflows, Berechtigungen, Branch-Protection, Rulesets, Required Checks,
Framework, MRTS, Gitlinks, direktem `master` oder Merge. Der aktuelle
`master` bleibt die maßgebliche Basis.

## Security-Auswirkung

Betroffene Sicherheitsgrenzen sind untrusted Netzwerk-Peers,
Request-/Response-Streams, Subprocess- und Artefaktpfade, Unix-/TCP-
Endpunkte, Protokollparser und nebenläufiger Transaktionszustand. Die
Implementierung ergänzt begrenzte Pfad- und Endpoint-Prüfungen, stabile
Cleanup-Ownership, Cancel-Propagation, absolute Stream-Lifetime und
einmaliges Event-Encoding; bestehende Autorisierungsentscheidungen bleiben
erhalten. Ein unabhängiges Post-Fix-Review fand einen Apache-`/proc/net/tcp`-
Tokenindexfehler; Parser und tatsächliches Layout-Regression-Fixture wurden
korrigiert und fokussiert verifiziert. Das finale unabhängige Review fand dann
drei aktive Envoy-Service-Konfigurationen ohne die neue verpflichtende
Stream-Lifetime; alle wurden korrigiert. Ein späteres unabhängiges HAProxy-
Boundary-Review fand die oben behobenen Lücken bei Response-Phase,
Detect-only-Protokollfehlern und gesättigter Zulassung. Das nachfolgende
frische kombinierte Diff-Review fand keine konkrete Sicherheits- oder
Integritätslücke mittlerer oder hoher Schwere; es prüfte insbesondere die
Envoy-Post-Send-Evidence-Grenze sowie die Common-verlustfreien
Serialisierungs-/Integritätskettenpfade.

## Geänderte Dateien

- `connectors/apache/harness/apache_process_guard.py` und
  `tests/test_apache_process_guard.py`
- Common-Event-Header, Runtime, JSON-/JSONL-/Integritätsimplementierung sowie
  `tests/event_json_utf8_smoke.c` und
  `tests/transaction_phase_runtime_companion_test.c`
- `connectors/traefik/src/traefik_engine_service.c` und
  `tests/test_traefik_engine_service_shutdown_contract.py`
- Lighttpd-Backend-Close- und Stock-Lifecycle-Harness-Source, Tests und
  englische Dokumentation
- Envoy-ext_proc-Processor-/Config-Source, Tests, englische/deutsche READMEs
  sowie aktive und Beispiel-Service-Konfigurationen
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`, HAProxy-
  Beispielkonfigurationen und englische/deutsche Konfigurationsreferenzen sowie
  `reports/connector-configuration-inventory.json`
- HAProxy-Response-Timeout-, Transaction-Cache-, Peer-Isolation-,
  Resource-Limit-, SIGPIPE/Peer-Isolation- und Sonar-Reliability-Verträge
- `ci/checks/documentation/connector_config_reference.py` und
  `tests/test_connector_config_reference.py`
- `connectors/traefik/native_middleware/README.de.md`
- dieses englische/deutsche Change-Record-Paar und beide Archivindizes

## Ausgeführte Befehle

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
  tests.test_apache_process_guard
  connectors.lighttpd.tests.test_backend_close_harness_contract
  connectors.lighttpd.tests.test_stock_lifecycle_harness_contract
  tests.test_traefik_engine_service_shutdown_contract` — bestanden, 81 Tests.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
  tests.test_haproxy_spop_response_timeout_contract
  tests.test_haproxy_spop_transaction_cache_contract
  tests.test_haproxy_spop_peer_isolation_contract
  tests.test_haproxy_spop_resource_limits_contract
  tests.test_haproxy_spop_sigpipe_peer_isolation_contract
  tests.test_sonar_reliability_contract` — bestanden, 34 Tests.
- `rtk proxy make -C connectors/haproxy self-test-spoa-runtime` — bestanden;
  den ausgewählten libModSecurity-Headern fehlt die optionale Rule-ID-API, und
  wie vorgesehen wurde der unterstützte Baseline-Probe gewählt.
- In `connectors/envoy/ext_proc`, `rtk proxy go test -count=5
  ./internal/processor`, `rtk proxy go test -race -count=1
  ./internal/processor`, `rtk proxy go test -count=1 ./...` und `rtk proxy go
  vet ./...` — bestanden; deterministische Kontrollen decken erfolgreiche
  Response-CONTINUE- und Immediate-Response-Sends an der tatsächlichen
  Stream-Deadline, Evidence-Fehler, Terminal-Cleanup und abgelehnte Folgezulassung
  ab.
- `rtk proxy cc -std=c17 -Wall -Wextra -Werror -Icommon/include
  tests/event_json_utf8_smoke.c common/src/*.c`, dann Smoke-Binärdatei und
  `jq`-Decoded-Value-Assertion — bestanden. Strikte C17- und ASAN/UBSAN-Builds
  dieses Smokes und des echten Common-Runtime/libmodsecurity-Companion-Tests —
  einschließlich Ablehnung von fehlerhaftem UTF-8 ohne Event-/Kettenfortschritt
  und einer legitimen Folgeanfrage — bestanden; task-eigene Binärdateien werden
  vor der Auslieferung entfernt.
- `rtk proxy jq -e .` für die drei aktiven und vier Beispiel-Envoy-Service-
  JSON-Dateien — bestanden.
- `rtk proxy cc -std=c17 -Wall -Wextra -Werror -fsyntax-only
  -Icommon/include -Iconnectors/haproxy/src
  connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — bestanden.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
  tests.test_connector_config_reference` und
  `rtk proxy python3 ci/checks/documentation/check-connector-config-reference.py
  --repo-root .` — bestanden, 4 Tests und aktuelle generierte Referenzen.
- `rtk proxy git diff --check` — am finalen lokalen Validierungspunkt
  bestanden.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
  tests.test_bilingual_docs tests.test_connector_config_reference` — bestanden,
  26 Tests. Das kombinierte fokussierte Connector-Set bestand 119 Tests.

## Runtime-Evidence

Es wird kein vollständiger lokaler Real-Host-Matrixlauf behauptet. Der
gehostete Apache-Runtime-Fehler wurde auf Listener-Inode-Parsing zurückgeführt
und lokal korrigiert; Exact-Head-Hosted-Workflow-Evidence ist weiterhin nötig.
Die echte Common-Runtime-Regression beweist, dass ein verlustbehaftetes Event
weder geschrieben noch verkettet wird und dass eine legitime Folgeanfrage
gelingt. Der native HAProxy-Selbsttest beweist die gerahmten
Protokollkontrollen des Connectors, aber keine vollständige HAProxy-
Host-Integration oder ein Betriebssystem-FD-Leak-Audit.

## Nicht ausgeführte Prüfungen mit Begründung

Kein vollständiger lokaler Real-Host-Matrixlauf wurde ausgeführt. Der
vollständige bilinguale Dokumentationscheck wurde ausgeführt, ist aber
`blocked_environment` ausschließlich wegen fehlender Framework-Gitlink-Ziele
in diesem Task-Checkout; eine Framework-Initialisierung oder -Änderung ist
nicht autorisiert. PR-bezogene SonarQube-Cloud-Analyse und GitHub Actions sind
für den Remediation-Head noch nicht gelaufen. Kein Merge und kein direkter
`master`-Update sind autorisiert.

## Bekannte Einschränkungen

Die zehn Connectorlösungen benötigen weiterhin vollständige Runtime-Layer-
Failure-Vector-, Parallelitäts-, Shutdown- und Cleanup-Evidence, sobald ihre
echten Host-Abhängigkeiten verfügbar sind.

## Verbleibende Risiken

Jeder verbleibende Sonar- oder Hosted-Fehler muss anhand seines Exact-Heads
ohne Abschwächung von Kontrollen bearbeitet werden.

## Finaler Diff- und Review-Status

Der finale lokale Diff hat sein erforderliches frisches unabhängiges
kombiniertes Security-/Bypass-Review ohne konkrete Lücke mittlerer oder hoher
Schwere abgeschlossen. Ein normaler Remediation-Commit und Push sowie danach
Exact-Head-Codex-, GitHub-Actions- und SonarQube-Cloud-Ergebnisse stehen noch
aus. Dieser Record behauptet absichtlich keinen finalen Commit, Push,
Quality-Gate-Pass, Workflow-Pass oder Merge; diese Fakten werden erst nach
ihrem Eintreten abgeglichen.
