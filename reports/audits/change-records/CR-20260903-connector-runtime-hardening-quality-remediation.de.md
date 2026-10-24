# Change Record CR-20260903-connector-runtime-hardening-quality-remediation

**Sprache:** [English](CR-20260903-connector-runtime-hardening-quality-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260903-connector-runtime-hardening-quality-remediation |
| Datum (UTC) | 2026-09-03 |
| Basis-Revision | 08fab232d77e300be15cb010e2adbcd590955727 (`origin/master`; current-master integration) |
| Auslieferungsstatus | Draft PR [#346](https://github.com/Easton97-Jens/ModSecurity-conector/pull/346) ist die alleinige Delivery-Authority. Die Integration des aktuellen `master` und lokale Kandidatenevidence sind unten dokumentiert; Exact-Head-Hosted-Evidence und Merge-Status müssen aus dem PR gelesen werden. Dieser Record behauptet selbst keinen Merge. |

Die anfänglichen Befehls-, Runtime-, Einschränkungs- und Reviewabschnitte unten
bleiben historische Momentaufnahmen früherer Kandidaten. Für den Kandidaten auf
aktuellem `master` werden sie durch die datierten Follow-up-Abschnitte ersetzt;
keine dieser Momentaufnahmen ersetzt Hosted-Evidence des Exact-Heads.

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
frühere kombinierte Diff-Review bleibt als historische Evidenz erhalten. Ein
späteres zweistufiges Apache/lighttpd-Boundary-Review fand und verifizierte
anschließend die Korrektur von FIFO-vor-Typprüfung, Verzeichnis-Erstellungs-
und Artefakt-Eltern-TOCTOU, begrenztem Cleanup-Baum und Ressourcenlimits für
JSON-Receipts. Sein finales Re-Review fand keinen konkreten verbleibenden
Bypass in der korrigierten Grenze.

## Geänderte Dateien

- `connectors/apache/harness/apache_process_guard.py`,
  `connectors/apache/harness/run_apache_smoke.sh` und ihre fokussierten sowie
  echten Prozesstests für launchgebundene Supervision, Parent-Death,
  pidfd-Fehler, typisierten Zustand, Exact-Inode-Publikation, Retirement und
  Cleanup
- Common-Event-Header, Runtime, JSON-/JSONL-/Integritätsimplementierung sowie
  `tests/event_json_utf8_smoke.c` und
  `tests/transaction_phase_runtime_companion_test.c`
- `connectors/traefik/src/traefik_engine_service.c`, Request-Body-Watchdog,
  Konfiguration und Tests der Native-UDS-Middleware sowie alle synchronisierten
  Native-UDS-Beispiele und generierten englischen/deutschen Referenzen
- Lighttpd-Backend-Close- und Stock-Lifecycle-Harness-Source und Tests
  einschließlich Parent-Death vor Registrierung, Prozessidentität und Cleanup
- `ci/checks/common/check-common-helpers.sh`
- Envoy-ext_proc-Processor-/Config- und Composite-Integrations-Source und
  -Tests einschließlich getrennter Stream-Idle-/Lifetime-Ursachen,
  Cancellation, begrenztem nativen Cleanup/Destruction, Duration-Grenzen,
  englischen/deutschen READMEs sowie aktiven und Beispiel-Service-
  Konfigurationen
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`, sein Cache-Miss-
  Harness und Cleanup-/Ownership-Tests, HAProxy-Beispielkonfigurationen und
  englische/deutsche Konfigurationsreferenzen sowie
  `reports/connector-configuration-inventory.json`
- HAProxy-Response-Timeout-, Transaction-Cache-, Peer-Isolation-,
  Resource-Limit-, SIGPIPE/Peer-Isolation- und Sonar-Reliability-Verträge
- `ci/checks/documentation/connector_config_reference.py` und
  `tests/test_connector_config_reference.py`
- Traefik-Native-UDS-`.traefik.yml`, Middleware-Source/-Tests, EN/DE-READMEs,
  dynamische Profilbeispiele und Operatorflächen für
  `requestBodyIdleTimeoutMillis`
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
  26 Tests. Zum damaligen historischen Validierungszeitpunkt bestand das
  kombinierte fokussierte Connector-Set 119 Tests.

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

Ein früheres lokales kombiniertes Review bleibt als historische Evidenz
erhalten. Das frische unabhängige Apache/lighttpd-Bypass-Review wurde in zwei
Korrekturrunden abgeschlossen: Es fand zunächst FIFO- und Erstellungsraces,
dann Pfade nach Validierung und schließlich einen unbegrenzten
`write-json --field`-Sink. Das finale enge Re-Review fand nach den
descriptor-relativen und größenbegrenzten Korrekturen keinen konkreten
verbleibenden Bypass. Ein normaler Remediation-Commit und Push sowie danach
Exact-Head-Codex-, GitHub-Actions- und SonarQube-Cloud-Ergebnisse stehen noch
aus. Dieser Record behauptet absichtlich keinen finalen Commit, Push,
Quality-Gate-Pass, Workflow-Pass oder Merge; diese Fakten werden erst nach
ihrem Eintreten abgeglichen.

## Nachfolgende Trust-Boundary-Korrektur

Der Apache-Smoke-Runner bereitet generierte Runtime-, Log-, Audit-, Modul-,
Konfigurations-, Document-Root- und Case-Output-Verzeichnisse nun über einen
descriptor-relativen `mkdirat`/`O_DIRECTORY|O_NOFOLLOW`-Walk vor. Er verwirft
einen verschachtelten Symlink-Pfad, ohne ein Ziel außerhalb des Runtime-
Bereichs anzulegen, verlangt vertrauenswürdige Ancestor-Ownership und erhält
sowohl private `0700`- als auch legitime nicht-private Output-Root-Kontrollen.
Apache-Evidence wird descriptor-relativ unterhalb des privaten Artefakt-Roots
geöffnet, akzeptiert nur reguläre Dateien und ist auf `1048576` Bytes
begrenzt; FIFO- und übergroße Evidence schlagen fail-closed ohne Blockierung
fehl.

Der lighttpd-Linux-Guard öffnet Trusted Root, Artefakt-Eltern und Cleanup-
Tree-Descendants nun über verifizierte Directory-Descriptoren. Er öffnet
Kandidatenartefakte mit `O_NONBLOCK|O_NOFOLLOW`, verlangt vor dem Parsen eine
private reguläre Datei, erhält retrybares Polling für fehlende Logs und
begrenzt den Cleanup-Baum nach Entry-Anzahl und Tiefe. JSON-Receipts erlauben
höchstens 32 Felder, 4096 Bytes pro Feld und 65536 serialisierte Bytes; ein
übergroßes Receipt erzeugt kein Artefakt, während die Fixed-Provenance-
Kontrolle weiter akzeptiert wird.

Die enge Common-Helper-Testkorrektur behält den verlustfreien Event-Vertrag:
Wenn die Serialisierung kein verlustfreies Event erzeugen kann, bleibt der
Output-Puffer leer statt einen synthetischen `"truncated":true`-Record zu
erzeugen. Dies ändert weder Workflow noch Ruleset, Required Check, Quality
Gate oder Produktions-Fail-Mode.

Das neueste fokussierte Aggregat war:

```text
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.test_apache_process_guard tests.test_apache_smoke_case_output_root \
  connectors.lighttpd.tests.test_backend_close_harness_contract \
  connectors.lighttpd.tests.test_stock_lifecycle_harness_contract \
  tests.test_haproxy_spop_peer_isolation_contract \
  tests.test_haproxy_spop_sigpipe_peer_isolation_contract
```

Es bestand `114` Tests. `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m
py_compile` für die betroffenen Apache/lighttpd-Python-Guards und Probes,
`rtk proxy sh -n` für die betroffenen Apache/lighttpd-Runner,
`rtk proxy make check-common-helpers-c17` und `rtk proxy git diff --check`
bestanden ebenfalls. `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m
unittest -v tests.test_bilingual_docs tests.test_connector_config_reference`
bestand ebenfalls mit `26` Tests. Die HAProxy-Revalidierung bestätigt, dass ein gesättigtes
Gate den neuen Peer schließt und die Accept-Schleife fortsetzt; alle Slots
können bis zu ihren begrenzten Peer-Deadlines weiterhin belegt sein, ein
dokumentiertes deployment-abhängiges Restrisiko, das vor einer weiteren
Klassifikation einen Real-Agent-Sättigungslauf benötigt.

## Exact-Head-Sonar-Authority-Boundary-Follow-up — 2026-09-04

Dieser Abschnitt ersetzt die früheren Aussagen zum noch ausstehenden
Hosted-Status; diese früheren Aussagen bleiben historische Momentaufnahmen und
sind kein aktueller Auslieferungsstatus. Für den exakten PR-Head
`d4f5674e8438d398696b1e92965d6e246618306f` bestanden alle zurückgemeldeten
GitHub-Actions-Prüfungen, einschließlich `bounded-c-cpp` und der fünf
Connector-Runtime-Matrixzellen. Ausschließlich SonarQube Cloud schlug am
Quality Gate mit `new_security_rating=3` (erforderlich `<=1`) und fünf offenen
Vulnerabilities fehl: vier `pythonsecurity:S8707`-Findings im Apache-
Process-Guard und ein `pythonsecurity:S8705`-Finding im lighttpd-Session-Guard.
Der Duplikationswert betrug `2.3` und lag innerhalb seines konfigurierten
Schwellwerts. Es wurden keine CI-Workflows, Rulesets, Branch-Regeln oder
Required Checks geändert.

Der Apache-Guard akzeptiert von einer direkten Ausführung keine generischen
`--directory`- oder `--artifact-root`-Flags mehr. Der Smoke-Runner liefert
diese Capabilities durch verpflichtende vertrauenswürdige runner-spezifische
Konfiguration; die bestehenden descriptor-relativen, Ownership-, Mode-,
Größen- und Cleanup-Kontrollen bleiben erhalten. Der lighttpd-Guard akzeptiert
keinen `argparse.REMAINDER`-Befehl mehr. Er konstruiert nur vier typisierte
Runner-Profile: `lighttpd-config-check`, `lighttpd-server`,
`stock-lifecycle-hold` und begrenztes `sleep-duration`. Fehlende, unbekannte,
zusätzliche oder widersprüchliche Profile-Werte schlagen vor `execv` fehl; das
Stock-Profil verwendet den festen Lifecycle-Probe und seine feste Argumentform.

Der finale lokale Kandidat bestand das folgende fokussierte
Apache/lighttpd/HAProxy-Aggregat mit `116` Tests und die
bilinguale/config-reference-Suite mit `26` Tests:

```text
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.test_apache_process_guard tests.test_apache_smoke_case_output_root \
  connectors.lighttpd.tests.test_backend_close_harness_contract \
  connectors.lighttpd.tests.test_stock_lifecycle_harness_contract \
  tests.test_haproxy_spop_peer_isolation_contract \
  tests.test_haproxy_spop_sigpipe_peer_isolation_contract
```

Auch Python-Kompilierung für die betroffenen Guards/Probes, `sh -n` für alle
betroffenen Runner, `make check-common-helpers-c17` und `git diff --check`
bestanden. Zwei unabhängige Post-Patch-Reviews der Authority-Boundary fanden
weder einen direkten CLI-Bypass noch eine Runner-Contract-Regression. Die
verbleibende Vertrauensgrenze sind Runner-Prozesskonfiguration und gewählte
Host-Executables: Dies sind vertrauenswürdige Orchestrierungsinputs, kein
Authentifizierungsmechanismus gegen einen gleichberechtigten lokalen Principal.
Ein solcher Principal liegt außerhalb dieser lokalen Harness-Grenze.
`FND-SONAR-0074` bleibt `in_progress`, bis ein normaler Follow-up-Push ein
bestehendes SonarQube-Cloud-Ergebnis für seinen exakten PR-Head erzeugt.

### lighttpd-Zombie-Cleanup-Follow-up

Ein ursprüngliches Codex-Review-Finding blieb nach der früheren
Zombie-State-Korrektur reproduzierbar: `terminate_registered_session()` behielt
die rohe initiale Session-Mitgliedschaft für Audit-Zwecke und leitete danach
`unexpected_members` fälschlich aus dieser rohen Liste ab. Ein bereits
existierender Zombie ließ deshalb
`cleanup-session --reject-unexpected-members` nach erfolgreicher aktiver
Containment fehlschlagen. Der Guard behält rohe `initial_members` nun als
Evidence, leitet unerwartete Mitglieder aber nur aus aktiven initialen
Non-Leadern und verifizierten Non-Leader-TERM/KILL-Signalen ab. Nicht
inspizierbarer State bleibt fail-closed; lebende initiale und spät geforkte
Mitglieder bleiben unerwartet und erhalten die Reject-Kontrolle.

Die Regression startet eine Task-Session mit einem bereits existierenden
Zombie-Child, verlangt erfolgreiche Rückkehr von
`cleanup-session --reject-unexpected-members` und beweist, dass der Zombie in
`initial_members`, nicht aber in `unexpected_members` erhalten bleibt. Der Test
wartet auf einen vollständigen Child-PID-Record und gibt dem Leader vor jeder
Eskalation einen TERM-Reaping-Pfad. Ein Prozess, der zwischen
Membership-Scan und `/proc`-State-Read verschwindet, ist nur bei `ENOENT` oder
`ESRCH` benign; alle anderen Inspektionsfehler bleiben fail-closed. Die
bestehenden Live-Child- und Late-Fork-Kontrollen bestanden ebenfalls. Die zwei
lighttpd-Harness-Contract-Suites bestanden mit `65` Tests; Python-Kompilierung
und `git diff --check` bestanden. Es wurden keine CI-Workflows, Rulesets,
Branch-Regeln oder Required Checks geändert.

## Follow-up zur Integration des aktuellen Masters — 2026-09-07

PR #346 wurde durch einen normalen, nicht umschreibenden Merge semantisch mit
dem aktuellen `origin/master` `08fab232d77e300be15cb010e2adbcd590955727`
kombiniert. Die fünf tatsächlichen Konflikte wurden als Union der aktuellen
Kontrollen aufgelöst: helper-aware Apache-Common-Adoption-Vertrag, begrenztes
HAProxy-SPOP-Parsing und Peer-Isolation, vollständige englische/deutsche
Change-Record-Indizes sowie der kombinierte Sonar-Reliability-Harness. Die
aktuellen Master-Reparaturen der NGINX- und HAProxy-Checker bleiben erhalten.
Das ursprüngliche #346-Verhalten für lighttpd-Response-Abort und Deferred-
Finish wurde auf das aktuelle Source-Layout portiert, statt bei der Integration
verloren zu gehen. Kein `.github/**`-, Ruleset-, Branch-Protection-, Required-
Check-, Quality-Gate-, Gitlink-, Framework- oder MRTS-Pfad wurde geändert.

Ein unabhängiges Integrationsreview fand, dass ein laufender nativer SPOP-Owner
seine Caller-Deadline überleben, alle folgenden Owner-Arbeiten blockieren und
einen unbegrenzten Shutdown-Join festhalten konnte. Die Reparatur setzt diese
Queue terminal, schließt Admission und Listener, storniert ausstehende Arbeit
und erlaubt höchstens eine feste Ein-Sekunden-Shutdown-Grace-Period. Bleibt
nativer Zustand erreichbar, beendet sich der Agent mit dem dokumentierten
Restart-Status `75`, ohne diesen Zustand freizugeben oder abzubauen. Ein zweites
Review fand dieselbe Lifetime-Klasse über einen fehlgeschlagenen oder hängenden
Response-Companion-Transport-Stop. Dieser Stop ist nun unabhängig außen
begrenzt; jeder unvollständige Synchronisations-/Stop-Pfad beendet sich mit
`75`. Common entfernt ausschließlich die erfasste eigene UDS-Inode vor
potenziell blockierenden Joins oder Worker-Waits. Eine Ersatz-Inode bleibt
bewusst erhalten. Das finale unabhängige Re-Review fand in diesen Pfaden keinen
verbleibenden UAF-, Double-Free-, Listener-FD-Reuse- oder Lock-Order-Bypass.

Die Exact-Head-Sonar-Analyse von `f572fa1a` meldete ausschließlich zwei
`c:S5487`-Reliability-Blocker im SPOP-Owner-Lock-Lebenszyklus. Die
Folgereparatur verwendet für den legitimen Post-Restart-Selbsttest einen
getrennten Prozesszustand und erfasst die terminale Restart-Disposition vor
dem Abbau des Queue-Locks. Sie unterdrückt weder ein Issue noch verändert sie
das Quality Gate. Zwei unabhängige Envoy-Reviews bestätigten außerdem
verbleibende Watchdog-Lücken nach einem erfolgreichen Response-`Send` und in
`transaction.Close`: Ein bereits in einen nicht unterbrechbaren Abschnitt
eingetretener nativer/CGo-Aufruf konnte Stream und Admission-Slot ohne
Fatal-Signal halten. Beide Operationen sind nun außen begrenzt. Ein hängender
Evidence-Aufruf übergibt das State-Ownership atomar an genau einen Reaper; ein
hängendes Close liefert einen terminalen Cleanup-Fehler zurück. In beiden
Fällen erhält der Prozessbesitzer `FatalErrors`, Folgezulassung wird abgewiesen
und die native Transaktion wird weder ein zweites Mal geschlossen noch
freigegeben, solange sie erreichbar ist. Engine-Operation-, Stream-Idle-,
Stream-Lifetime- und Cleanup-Timeout bleiben getrennte Kontrollen.

Die aktuelle lokale Evidence umfasst:

- Common/Apache/NGINX: 146 Tests plus 80 Subtests bestanden; alle vier Common-
  Adoption-Targets und der Common-Sicherheitsvertrag bestanden.
- HAProxy: Die vollständige Python-/Contract-Auswahl führte 239 Tests aus; 227
  bestanden, 12 wurden übersprungen, zusätzlich bestanden 93 Subtests; der fokussierte ASan/UBSan-Harness
  bestand die Kontrollen für terminalen Owner, fehlgeschlagenen Transport-
  Stop, hängenden Transport-Stop und legitime frische Instanz. Der echte
  Common-Response-Companion-Transporttest bestand C17
  `-Wall -Wextra -Werror` mit ASan, UBSan und Leak-Erkennung einschließlich
  paralleler Clients, UDS-Ownership, Stop/Restart, Cancel, Cleanup und Follow-up.
- Envoy: Alle ext_proc-Pakettests, die vollständige Race-Suite, Vet und der
  Build mit `-buildvcs=false` bestanden, einschließlich deterministischer
  Fatal-/Reaper-/Folgekontrollen für blockierte Evidence und blockiertes Close.
  Traefik-Native-UDS-, Composite-Middleware- und Response-Observer-
  Tests, Race-Tests, Build, Vet, Fuzz, Contracts und Runtime-Harnesses bestanden.
- lighttpd: 154 Tests bestanden, 28 wurden übersprungen und 80 Subtests
  bestanden; die enge Stock-/Patched-/ABI-Auswahl bestand 156 Tests, 18 wurden
  übersprungen und 108 Subtests bestanden. Das Common-Adoption-Target bestand.
- Die bilinguale Dokumentation bestand 22 Tests; `git diff --check` bestand.

Vier nicht verbindliche aktuelle Master-Baselines werden nicht zu Erfolgen
umgedeutet: Der eigenständige HAProxy-SPOA-Selbsttest-Link schlägt auf
unverändertem Master identisch mit undefiniertem
`msconnector_block_status_is_allowed` fehl; der Common-SDK-Vertrag schlägt
identisch fehl, weil sein Textchecker einen Kommentar matched; und ein Envoy-
Beispieltest schlägt identisch fehl, weil er eine gofmt-instabile
Spaltenausrichtung behauptet. Der NGINX-Bounded-Soak-Vertrag schlägt auf
unverändertem Master ebenfalls identisch fehl, weil er noch die entfernte
einzelne Cleanup-Trap erwartet, während der Harness getrennte EXIT-, INT- und
TERM-Handler verwendet. Das lighttpd-Konfigurations-Target wurde innerhalb
der begrenzten lokalen Beobachtung nicht fertig; es wird kein Build-Ergebnis
behauptet. Produktions-SPOP-PID-/Ready-/Port-Metadaten werden durch das
Runtime-Root-Cleanup des Repository-Harnesses entfernt, aber vom eigenständigen
Agenten weder inodegebunden noch selbst entfernt; diese bestehende Supervisor-/
Stale-Metadata-Einschränkung bleibt ausdrückliche Folgearbeit. Exact-Head-
GitHub-Actions- und SonarQube-Cloud-Evidence stehen bis zum normalen Push des
Integrationscommits aus; dieser Abschnitt behauptet weder dieses Hosted-
Ergebnis noch einen Merge nach `master`.

## Follow-up des terminalen Cleanup-Reviews — 2026-09-07

Das Security-Review vor der Auslieferung identifizierte drei durch den PR
eingeführte Lücken; sie wurden vor Finalisierung des aktuellen Kandidaten
korrigiert. Common Runtime ruft den Shutdown-Callback des Response-Companions
nicht mehr aus dem generischen Service-Release auf: Der Serving-Pfad ist der
alleinige Owner und ruft ihn genau einmal auf, während ein Fehler beim
Listener-Setup ihn nullmal aufruft, weil kein Companion gestartet wurde. Damit
bleibt der öffentliche Callback-Vertrag auch für nicht idempotente
Implementierungen erhalten und Double-Shutdown, Double-Destroy oder ein durch
einen abgelehnten zweiten Callback verursachtes Cleanup-Leak werden vermieden.

Der Apache-Process-Guard schließt einen neu geöffneten PID-Descriptor jetzt
auch dann, wenn eine anschließende Binding-Prüfung fehlschlägt. Cleanup-
Evidence wird vollständig in eine private temporäre Datei geschrieben und
geschlossen und danach per nicht überschreibendem Hardlink veröffentlicht;
Short Writes werden vervollständigt und jede fehlgeschlagene Veröffentlichung
setzt temporäre und finale Namen zurück. Bei einem Storage-Fehler beendet der
Guard den gerade gestarteten Server über die bereits verifizierte In-Memory-
Identität und pidfd, weist einen ruhenden Listener und eine ruhende Session
nach und liefert einen eigenen Status für erfolgreiches Fehler-Cleanup. Die
Shell reapet danach dieses Kind, entfernt seine PID-Datei, prüft den freien
Port und führt nach ungültiger Evidence keinen unbegrenzten `wait` aus.
Die Ownership-Inspektion wird für ein begrenztes Intervall wiederholt. Trat
vor einem vollständigen Snapshot ein transienter `/proc`- oder Listener-
Snapshot-Fehler auf, behandelt der Guard die Beobachtung als instabil, führt
dasselbe verifizierte Cleanup aus und veröffentlicht keine möglicherweise
inkonsistente Evidence.

Traefiks neue Kontrolle `maxRequestBodyBytes` ist in den englischen und
deutschen Beispielen und Konfigurationsreferenzen, der ausgewählten sicheren
dynamischen Konfiguration und dem generierten Konfigurationsinventar
abgebildet. Ein quellenbasierter Test vergleicht alle acht JSON-Felder der
nativen Middleware mit jeder dieser Operator-Oberflächen. Default und harte
Obergrenze bleiben 1048576 Bytes.

Die fokussierten lokalen Kontrollen bestanden 56 Apache-Guard-Tests
einschließlich 21 parametrisierter/Subtest-Fälle, 15 Common-Worker-/Security-
Contract-Tests und
60 Traefik-/Dokumentationstests plus 15 Subtests. Das finale Aggregat und die
unveränderliche Exact-Head-Security-
Diff-Evidence werden erst nach dem Kandidaten-Commit festgehalten. Die
bestehenden Findings `FND-PARENT-0015` (Pathname-UDS-Impersonation durch
dieselbe Identität) und `FND-PARENT-0966` (Drain-Reihenfolge bei erzwungenem
Envoy-Shutdown) bleiben vorbestehende Follow-up-Punkte und werden durch diese
Änderung nicht geschlossen. Es wurde kein `.github/**`-, Quality-Gate-,
Ruleset-, Branch-Protection- oder Required-Check-Pfad geändert.

## Finale Validierung mit aktuellem master — 2026-09-07

Der Kandidat basiert auf dem aktuellen `origin/master`
`08fab232d77e300be15cb010e2adbcd590955727`, das über den bestehenden
nicht-umschreibenden Merge integriert wurde. Kein Pfad unter `.github/**`,
keine Ruleset-, Branch-Protection-, Required-Check-, Quality-Gate-, Gitlink-,
Framework- oder MRTS-Struktur wurde geändert.

Die lokale Validierung deckte Apache, HAProxy, Envoy, Traefik und lighttpd ab.
Apache-Prozess-/Smoke-Supervision und Cleanup-Kontrollen bestanden,
einschließlich Parent-Death, pidfd-Fehler, Evidence-Publikation, Identität,
Retirement und Folgeanfrage. HAProxy bestand die begrenzten nativen
Owner-/Transport-Cleanup-Kontrollen sowie den Common-
Response-Companion-Transporttest mit strengem C17, ASan, UBSan,
Leak-Erkennung, parallelen Clients, Cancel, Restart, Cleanup und Follow-up.
Envoy-ext_proc bestand Pakettests, Race-Tests, Vet und Build-Validierung,
einschließlich begrenzter Evidence-/Close-Watchdogs, Fatal-/Reaper-Übergabe,
Cancel und Folgezulassung. Traefik-Native-UDS-, Composite- und
Response-Observer-Tests, Race-/Build-/Vet-/Fuzz-/Contract-Checks und
Runtime-Harnesses bestanden, einschließlich der begrenzten
Request-Body-Größen- und Idle-Kontrollen. lighttpd-Stock-/Patched-/ABI-
Lifecycle-, Parent-Death-, Identitäts-, Zombie- und Cleanup-Kontrollen
bestanden.

Die unveränderten Master-Baselines bleiben ausdrücklich nicht verbindlich und
werden nicht als Erfolge umklassifiziert: Das eigenständige HAProxy-SPOA-
Linking scheitert am bestehenden undefinierten
`msconnector_block_status_is_allowed`; der Common-SDK-Vertrag matched einen
bestehenden Kommentar; der Envoy-Beispieltest behauptet eine instabile
gofmt-Spaltenausrichtung; und der NGINX-Bounded-Soak-Vertrag erwartet noch die
entfernte einzelne Cleanup-Trap. Die begrenzte lighttpd-Konfigurations-
Beobachtung lieferte kein Build-Ergebnis. Produktions-SPOP-PID-/Ready-/Port-
Metadaten bleiben als dokumentierte Supervisor-/Inode-Bindungs-Folgearbeit
offen.

`FND-PARENT-0015` (Pathname-UDS-Impersonation durch dieselbe Identität) und
`FND-PARENT-0966` (Drain-Reihenfolge bei erzwungenem Envoy-Shutdown) bleiben
als vorbestehende Folge-Findings offen. Exact-Head-GitHub-Actions- und
SonarQube-Cloud-Ergebnisse stehen bis zum normalen Push des Kandidaten aus;
ein Merge nach `master` wird hier nicht behauptet.
