# Change Record

**Sprache:** [English](CR-20260824-connector-runtime-hardening.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260824-connector-runtime-hardening |
| Datum (UTC) | 2026-08-24 |
| Basis-Revision | a6b4ced4876a19666f7c7203ed9e719674c69ec1 |
| Repository-Grenze | Nur Parent; Framework, MRTS, Gitlink, CI, Branch-Regeln, Rulesets und Required Checks unverändert |
| Evidence | `runs/20260824T120000Z-connector-runtime-hardening/evidence/runtime-hardening-validation.md`; SHA-256 `5fc2c8d6f5f2bdd36bd757fd044ab6f0f8d5f8f0e976a65ac46153ce3975ef63` |
| Delivery-Status | Durch diesen Record wurden kein Commit, Push, PR oder Merge ausgeführt |

## Motivation und Problemstellung

Die Aufgabe verlangte ein einheitliches, explizites Fehler-, Verfügbarkeits- und Cleanup-Modell für Apache, NGINX, HAProxy HTX, HAProxy SPOE/SPOP, Envoy `ext_authz`, Envoy `ext_proc`, Traefik `forwardAuth`, Traefik Native UDS, lighttpd Stock und lighttpd Patched. Ein fehlerhafter oder nicht erreichbarer Engine-, Peer-, Backend-, Client-, Stream-, Body- oder Handshake-Zustand darf keinen langlebigen Connector stillschweigend beenden, spätere Verarbeitung dauerhaft blockieren, unbegrenzt Ressourcen halten oder Prozesse, Ports, UDS-Dateien, Streams oder Transaktionszustände zurücklassen.

## Akzeptanzkriterien

- Direkte libmodsecurity-C-API-Aufrufe behandeln exakt `1` als Erfolg und schlagen bei `0` oder negativen Rückgaben in den abgedeckten Apache-, NGINX-, HAProxy- und gemeinsamen Runtime-Pfaden fail-closed fehl.
- HAProxy-SPOE/SPOP-Schreibvorgänge sind signalsicher und werden ausgewertet; Peer-Reset/EPIPE, unvollständiges oder langsames HELLO, parallele Peers, Folge-HELLO sowie Allow-/Block-Kontrollen haben begrenzte, isolierte Ergebnisse. Eine verlorene zustandsbehaftete Response-Transaktion liefert explizit geschlossen `error`/`502` mit Reason-Code `stateful_response_transaction_missing_closed`, niemals still `pass`/`200`.
- Die gemeinsame HTTP-Autorisierung für Envoy `ext_authz` und Traefik `forwardAuth` begrenzt Worker-Aufnahme, überlebt das Schließen eines fehlerhaften Peers und erlaubt nachfolgende Allow-/Block-Anfragen.
- Envoy `ext_proc` trennt Engine-Timeout und Stream-Idle-Timeout, definiert Aktivität pro vollständiger Anfrage, begrenzt parallele Streams, propagiert Cancel und gibt Zustand frei.
- Traefik Native UDS begrenzt Worker-/Socket-Tracking, behandelt Reset und Shutdown, leert innerhalb einer Frist und verwendet einen definierten kontrollierten Restart-Pfad, wenn ein nicht unterbrechbarer Engine-Worker nicht entleert werden kann.
- lighttpd Stock und Patched kompilieren und bestehen Baseline-, Block-, Event- sowie Listener-/Cleanup-Smokes.
- Keine CI-Workflow-, Branch-Regel-, Ruleset-, Required-Check-, Framework-, MRTS- oder Parent-Gitlink-Datei wird geändert.

## Implementierungsentscheidung und Begründung

- Fehlerhafter, unvollständiger, abgelaufener, zurückgesetzter oder abgebrochener Engine-/Protokollzustand wird bei unentscheidbarer Autorisierung fail-closed behandelt; eine legitime Folgeanfrage wird nach Peer-lokalem Cleanup zugelassen. Host-Aktion, Status, Event, Cleanup und Betreiberwirkung stehen in Runtime-Policy und aufbewahrter Evidence.
- Signalsicherheit gilt lokal je Socket-Schreibvorgang (`MSG_NOSIGNAL`, mit verfügbarer Plattformalternative); globales Ignorieren von SIGPIPE wird nicht verwendet.
- Admission und Shutdown sind begrenzt. Cleanup ist idempotent oder ownership-isoliert; Zustand wird nicht freigegeben, solange ein nicht unterbrechbarer Worker ihn besitzt.
- Die vom Projekt gelieferte HAProxy-SPOE-Konfiguration mit geschlossenem Default setzt `option continue-on-error` nicht: Dieses HAProxy-Opt-in ist mit `fail-mode=closed` inkompatibel, weil ein Agent-Fehler sonst als Allow enden kann. Ein Admission-Close ohne ACK ist ein geschlossener SPOP-Transportfehler; ein Failure-ACK wird auf `503` abgebildet. Der genaue native-HAProxy-Clientstatus für ein unbestätigtes Admission-Close bleibt `NOT_EXECUTED`, während die Peer-lokale Admission-/HELLO-Isolation erhalten bleibt.
- Ein Response-seitiger SPOP-Cache-Korrelationsfehler ist getrennt fail-closed, auch wenn ein Betreiber gewöhnliche Enginefehler mit `fail-mode=open` gewählt hat: begrenzte Eviction kann ein Verfügbarkeitslimit bleiben, aber ein späteres Response-NOTIFY liefert `error`/`502` mit `stateful_response_transaction_missing_closed`, statt Response-Enforcement still zu überspringen.
- `ext_proc` setzt Aktivität nur nach vollständiger Processing-Request und Response-/Engine-Arbeit zurück. Der allgemeine Engine-Timeout ist kein Stream-Idle-Timeout.
- Das aktuelle `ext_proc`-Follow-up-Fixture prüft nach Rückkehr des Idle-Handlers `pendingReceives == 0`; Mutex- und Forced-Stop-Wartezeiten sind durch Deadlines begrenzt. Ein bereits laufender, nicht unterbrechbarer nativer C-Destruktor nutzt einen kontrollierten Nonzero-Restart-Pfad, nicht eine In-Process-Cancel-Zusage.
- Native-UDS-RESULT-Writes verwenden eine `CLOCK_MONOTONIC`-Peer-Deadline mit `poll(POLLOUT)` und nicht-blockierendem `MSG_NOSIGNAL | MSG_DONTWAIT`. Ablauf schließt nur diesen Peer und gibt seinen Worker frei; das ist kein Engine-Operations- oder Receive-Timeout.
- lighttpd-Response-Start-Helfer werden außerhalb des Patched-Host-ABI-Guards kompiliert, damit beide Hostvarianten denselben Cleanup-sicheren Pfad nutzen.

## Security-Auswirkung

Die Änderungen härten Trust-Boundary-Übergänge zwischen Hosts, Clients, Peers, Engines, Sockets, Protokollstreams und Transaktionszustand. Sie reduzieren Crash-, Deadlock-, Ressourcenerschöpfungs-, Request-Blockierungs-, veraltete-Listener- und mehrdeutige-Autorisierungszustände. Allow- und Block-Kontrollen bleiben verfügbar und wurden nach fehlerhaften Peer- sowie Timeout-/Cancel-Fällen erneut geprüft. Die Evidence besteht aus lokaler Source-, Service-, Connector- und Host-Smoke-Evidence; sie beweist nicht jede Produktionshost-, HTTP/2-, HTTP/3-, Reload- oder externe Deployment-Kombination.

## Geänderte Dateien

- `common/runtime/msconnector_runtime.c` — exakte libmodsecurity-Transaktions-Erfolgsprüfungen.
- `common/runtime/http_authorization_service.c` — signalsichere Writes, begrenzte Worker-Aufnahme und begrenztes Shutdown-Ownership.
- Apache: `connectors/apache/src/mod_security3.c`, `connectors/apache/src/msc_filters.c` — fail-closed Transaktions- sowie Response-/Body-Prüfungen.
- NGINX: `connectors/nginx/src/ngx_http_modsecurity_access.c`, `ngx_http_modsecurity_body_filter.c`, `ngx_http_modsecurity_header_filter.c`, `ngx_http_modsecurity_module.c` — exakte C-API-Rückgabebehandlung.
- HAProxy: `connectors/haproxy/src/haproxy_modsecurity_binding.c`, `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`, `connectors/haproxy/harness/run_haproxy_spop_cache_miss.sh`, `examples/haproxy/compatibility-spoe/modsecurity-agent.conf` — HTX-Prüfungen, isolierte begrenzte signalsichere SPOE/SPOP-Behandlung und Harness für die malformed-NOTIFY-Regression.
- Envoy: `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go`, `connectors/envoy/ext_proc/internal/processor/config.go`, `processor.go`, `processor_test.go`, `connectors/envoy/config/envoy-ext-proc-service.json`, `examples/envoy/minimal/envoy-ext-proc-service.json`, `examples/envoy/safe/envoy-ext-proc-service.json` — Idle-/Admission-/Cancel-/Shutdown-Kontrollen und Config.
- Traefik: `connectors/traefik/src/traefik_engine_service.c`, `connectors/traefik/build/test-engine-service-runtime.sh` — begrenztes Native-UDS-Drain, kontrollierter Restart und Runtime-Regression für nicht lesende Peer-Write-Deadline.
- lighttpd: `connectors/lighttpd/module/mod_msconnector.c`, `connectors/lighttpd/tests/test_patched_host_contract.py` — Stock-/Patched-Helper-Scope und Regression.
- Regressionstests: `tests/test_apache_fail_closed.py`, `connectors/nginx/tests/test_fail_closed_contract.py`, `tests/test_native_api_fail_closed_contract.py`, `tests/test_haproxy_spop_peer_isolation_contract.py`, `tests/test_haproxy_spop_transaction_cache_contract.py`, `tests/test_http_authorization_service_worker_contract.py`, `tests/test_http_authorization_service_runtime.py`, `tests/test_traefik_engine_service_shutdown_contract.py`.
- Keine CI-, Framework-/MRTS-, Gitlink-, Dependency-, Branch-Regel-, Ruleset- oder Required-Check-Datei gehört zu diesem Record.

## Tests und tatsächliche Ergebnisse

Die vollständigen aufbewahrten Befehle und beobachteten Ergebnisse stehen in der oben genannten Evidence-Datei.

- Apache-Contracts: 4 bestanden; Apache-C17-Kompilierung bestanden.
- NGINX-Contracts: 13 bestanden, einschließlich der fail-closed-Regression Zero-Return zu 500. Native NGINX-C17 war blockiert (Exit 77), da lokale NGINX-Quellen/Header fehlten; keine Dependency wurde bereitgestellt.
- Direkte C-API-Contracts: 3 bestanden.
- HAProxy-SPOP-Source-Contracts: 5 bestanden; GCC-/Clang-Runtime-Self-Tests, Binding, Reset/EPIPE, sofortiges Schließen eines gesättigten Peers, HELLO-Deadline, parallele Peers, Folge-HELLO, Allow, Block (`403`) und Port-Cleanup bestanden.
- HAProxy-HTX-Overlay-Checks und Helper-Suite (11 Tests) bestanden; nativer HAProxy-Host war nicht verfügbar.
- Envoy-Builds/Configs bestanden. Die `ext_authz`-Runtime bestand fehlerhafte-Peer-Recovery, `200` Allow, `403` Block, begrenzten Exit und Listener-Cleanup.
- Envoy-`ext_proc`-Go-Unit- und `-race`-Suites sowie der getaggte native CGo-Test bestanden, einschließlich Timeout, Cancel, Shutdown, Admission-Freigabe, Folgekontrollen und `TestCommonRuntimeEngineCloseHonorsShutdownContext`; alle drei Config-Checks bestanden.
- Traefik-`forwardAuth`-Config/Runtime bestanden fehlerhafte-Peer-Recovery, `200` Allow, `403` Block, Exit und Port-Cleanup.
- Traefik Native UDS: `make -C connectors/traefik test-engine-service` bestand Ownership-Selbsttest, `nonreading_peer_deadline_test=pass peers=64 elapsed_seconds=31.0 followup_latency_seconds=0.0` und seinen Negativtest. Dies ist ausschließlich lokale Connector-Runtime-Evidence.
- lighttpd-Contracts bestanden (36 Tests, 2 erwartete Skips). Frische Stock-/Patched-Builds/Checks und Runtime-Smokes bestanden Baseline `200`, Block `403`, Event, Shutdown und Listener-Cleanup.
- Die Evidence wurde wie unter Identität angegeben aufbewahrt und gehasht.

## Ausgeführte Befehle

Die aufbewahrte Evidence enthält die exakten Befehle und Ergebnisse. Die
wichtigsten lokalen Prüfungen waren die Connector-Contract-Suites, die
HAProxy-SPOE/SPOP-Runtime-Self-Tests, `go test ./...` und `go test -race ./...`
für Envoy, der getaggte native Envoy-Test, GCC-/Clang-/ASan-/UBSan-Läufe für
Traefik Native UDS, frische lighttpd-Stock-/Patched-Smokes, `make
check-doc-links` und `make check-bilingual-docs`.
## Runtime-Evidence

Die aufbewahrte Evidence deckt Engine-Startverfügbarkeit, Fehler innerhalb einer Transaktion, Timeout, ungültige/unvollständige Peer-Eingaben, Client-/Peer-Reset, unvollständige HELLO- und Body-/Stream-Grenzen, soweit der lokale Harness sie bereitstellt, parallele Requests/Streams, Größen-/Admission-Grenzen, Cancel, Shutdown, Folgekontrollen und Cleanup ab. SPOP-Logs erfassen Reset `errno=104` und EPIPE `errno=32`, gefolgt von erfolgreichem Control-Traffic. Der Traefik-Native-UDS-Test hält zusätzlich Ownership-Selbsttest, 64-Peer-Nichtlese-Deadline-Ergebnis, Negativtest, Follow-up mit Null-Latenz und das Fehlen des zugewiesenen UDS-Listeners fest.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein echter NGINX- oder HAProxy-HTX-Native-Host war verfügbar.
- Kein nativer Apache-, Envoy-Proxy- oder Traefik-Proxy-Host wurde gestartet; Connector-/Agent-Binaries und gemeinsame Services wurden ausgeführt.
- Ein absichtlich hängender libmodsecurity-Engine wurde nicht unsicher simuliert; begrenzter Shutdown und kontrollierter Nonzero-Restart wurden durch Source/Tests geprüft.
- Der Default-Pfad von Traefik `check-config` versuchte das historische globale `/var/tmp/ModSecurity-conector-verified/logs` zu erstellen und wurde durch die Sandbox blockiert. Eine task-eigene Konfiguration und `event_path` bestanden; kein globaler Pfad wurde erstellt.
- Vollständige Native-Host-, HTTP/2/HTTP/3-, Reload-, Cross-Connector-Leak- und ThreadSanitizer-Matrizen wurden nicht ausgeführt. CI wurde bewusst weder ausgeführt noch geändert.

## Bekannte Einschränkungen

Native Host-Integration sowie produktionsspezifisches Reload-, TLS-, HTTP/2-, HTTP/3- und Langzeit-Scheduling-Verhalten bleiben umgebungsabhängig. Der kontrollierte Restart-Zweig ist eine explizite Verfügbarkeitsentscheidung für einen nicht unterbrechbaren Engine-Worker; er behauptet nicht, dass ein solcher Worker ohne Prozessrestart wiederhergestellt werden kann. Die aufbewahrte Evidence ist starke lokale Evidence, aber kein vollständiger Hosted-Matrix-Nachweis.

## Verbleibende Risiken

Betreiber müssen weiterhin connector-spezifische Limits, Timeouts, TLS-/UDS-Berechtigungen, Reload-Reihenfolge und Monitoring in nativen Hostversionen validieren. Nicht verfügbare Native Hosts und nicht ausgeführte Matrizen bleiben Release-Readiness-Einschränkungen, bis sie unabhängig reproduziert wurden. Keine CI- oder Governance-Schutzmaßnahme wurde abgeschwächt.

## Finaler Diff- und Review-Status

Die Implementierungs-Evidence ist aufbewahrt, auf Parent begrenzt und mit diesem bilingualen Change Record gepaart. Die Remediations für NGINX-Zero-Return, gesättigte HAProxy-SPOP-Aufnahme und Response-Cache, nicht lesende Traefik-Native-UDS-Peers sowie nativen Envoy-`ext_proc`-Shutdown sind lokal behoben; ihre Findings bleiben offen oder `fixed` statt geschlossen, wo Native-Host-/FD-Vektor-Evidence noch fehlt. Dieser Record führt keinen Commit, Push, PR, Merge oder Finding-Abschluss aus. Die finale Auslieferung und ein etwaiger Draft-PR benötigen die separate scoped Diff-Prüfung und Delivery-Policy-Checks des Parent-Agents.
