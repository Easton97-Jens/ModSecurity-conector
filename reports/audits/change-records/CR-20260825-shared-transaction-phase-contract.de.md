# Change Record CR-20260825: gemeinsamer Transaktions-Phasenvertrag

**Sprache:** [English](CR-20260825-shared-transaction-phase-contract.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260825-shared-transaction-phase-contract` |
| Datum (UTC) | `2026-08-25` |
| Basis-Revision | `a6b4ced4876a19666f7c7203ed9e719674c69ec1` |
| Abgeglichene Delivery-Basis | `5d71be74369123257851eb5ec612d7523a6b061d` (`origin/master` vor dem ersten Task-Branch-Push) |
| PR-#344-Remediation-Basis | `c1653fb84201bc6a29c47723fa74e12270deb164` (`origin/master` lokal normal als `b1b6e72294a654c96dc44c9db69d25a704084c8f` gemergt; Auslieferung weiterhin ausstehend) |
| Scope | Nur Parent-Repository: gemeinsamer P1--P4-Transaktionsvertrag, zehn Connector-Zuordnungen, begrenzte Response-Companions, Stock-lighttpd-Sidecar, Tests, englische/deutsche Dokumentation und dieser gepaarte Change Record. Keine Framework-, MRTS-, Gitlink-, Workflow-, Ruleset-, Branch-Protection- oder Required-Check-Änderung. |

## Motivation und Problemstellung

Die Connector-Implementierungen stellten zuvor unterschiedliche Lifecycle- und
Decision-Formen bereit. Diese Änderung vereinheitlicht ihre fachliche
Bedeutung: P1 sind Request-Header vor dem Request-Commit, P2 ist der begrenzte
Request-Body mit genau einem End-of-Stream, P3 sind Response-Header vor dem
Response-Commit und P4 ist der begrenzte Response-Body mit genau einem
End-of-Stream. Die Bedeutungen werden aus den vorhandenen Common-, Adapter-,
Test- und Dokumentationsgrenzen abgeleitet; es wird keine neue
Phasenbedeutung erfunden.

## Akzeptanzkriterien

- Apache, NGINX, HAProxy HTX, HAProxy SPOE/SPOP, Envoy ext_authz, Envoy
  ext_proc, Traefik forwardAuth, Traefik Native UDS, lighttpd Stock und
  lighttpd Patched an denselben begrenzten Transaktions-/Decision-Vertrag oder
  eine dokumentierte minimale Hostübersetzung binden.
- Doppelte, übersprungene, verspätete, post-terminale, Cancel-, Timeout- und
  vorzeitige Cleanup-Phasenübergänge deterministisch ablehnen.
- Begrenzte Header, Request-/Response-Bodies, Events, opake Korrelation,
  private Defaults, metadata-only JSONL und keinen stillen
  Versions-/Capability-Fallback erhalten.
- Response-fähige Companions für Envoy ext_authz und Traefik forwardAuth
  beibehalten, statt P3/P4 als not applicable zu behandeln.
- Fokussierte Valid-/Invalid-Order-, Limit-, Timeout-, Cancel-, Cleanup-,
  Paralleltransaktions- und Connection-/Stream-Reuse-Coverage ergänzen.
- Nur einen wahrheitsgemäßen Draft-PR erstellen; kein Merge- oder
  `verified_pr`-Claim.

## Implementierungsentscheidung und Begründung

- `transaction_contract.h` und die Common Runtime besitzen kanonische
  Transaktionsidentität, Connector-/Host-Metadaten, Phasenstatus, begrenzte
  Request-/Response-Metadaten, Decisions, Regelkorrelation, Modus,
  Fehlerklasse, Zeitinformationen und Cleanupstatus. Sie besitzen außerdem
  die expliziten Zustandsautomatenprüfungen und normalisierten
  Hostaktionsaufzeichnungen.
- Direkte Adapter verwenden diesen Vertrag an ihren nativen P1--P4-Hooks.
  HAProxy SPOE/SPOP verwendet einen Owner-Queue-/MRC1-Responsepfad; Envoy
  ext_authz und Traefik forwardAuth übergeben dieselbe Transaktion an einen
  Single-Claim-Response-Observer über opake Handles und private UDS. Das
  Handle hat feste Kapazität und eine absolute TTL; es ist keine vom Client
  gelieferte Transaktionsidentität.
- Die kanonische Stock-lighttpd-Lösung ist ein traffic-owning HTTP/1.1-
  Sidecar auf literal `127.0.0.1` mit direktem P1--P4. Der native
  `stock-lighttpd`-Pfad bleibt eine exakte nichtkanonische P1/P3-
  Kompatibilitätsübersetzung und fällt niemals still auf das Sidecar zurück.
- Failure-Decisions bleiben typisiert und erhalten die ursprüngliche
  Regelkorrelation. Body-Limits emittieren ein begrenztes Terminal-Event ohne
  Body-Payload. Kein Connector verhandelt eine ältere MRC1-Version oder
  erfindet einen Capability-Fallback.

## Kompatibilitätsauswirkung

Connector-Protokolle und Hostmechaniken bleiben adapterspezifisch, aber
Decision-Bedeutung, Fehlerklassifikation, Cleanup und Limits sind gemeinsam.
Deployments mit der Stock-Lösung müssen das dokumentierte private
Literal-Loopback-Sidecar und einen expliziten externen Build-Root verwenden.
Envoy ext_authz und Traefik forwardAuth benötigen für P3/P4 ihren gepaarten
privaten Response-Observer.

## Security-Auswirkung

Die Änderung berührt nicht vertrauenswürdiges HTTP-Framing, begrenzte
Body-Verarbeitung, UDS-Korrelation, State-Ownership und Failure-Handling. Sie
erhält fail-closed Strict-Pre-Commit-Verhalten, begrenzte Eventserialisierung
ohne Body-Payload, opake Single-Claim-Korrelation, private Listener-Bindung,
explizite Phasenvalidierung und deterministische Zerstörung.

`FND-PARENT-0949` ist lokal fixed und seine direkten Komponentenregressionen
bestehen, benötigt aber Exact-delivered-Revision- und reale
Stock-Backend-Evidenz, bevor es verified werden kann. `FND-PARENT-0221`
bleibt P0/high, `in_progress`/`blocked_missing_evidence`; P4-Strict-
Real-Host-Proof und weitere benannte Host-Evidenz werden nicht promoted.
`FND-PARENT-0947` erfasst den out-of-scope-CI-Capability-Konflikt: sein
Collector erwartet für Traefik forwardAuth P2 `not_implemented`, während das
Produktmanifest wahrheitsgemäß `configured_not_exercised` sagt. Keine CI-Datei
wurde geändert und kein Risk Acceptance wird behauptet.

## Geänderte Dateien

- Common-Vertrag und Runtime: `common/include/msconnector/transaction_contract.h`,
  `common/src/transaction_state.c`, `common/runtime/msconnector_runtime.*`,
  `common/runtime/response_companion_{transport,client}.*`, Decision-/Error-/
  Event-Interfaces sowie die englische/deutsche Vertrags- und
  Design-Dokumentation.
- Adapter: Apache-, NGINX-, HAProxy-HTX/SPOE-SPOP-, Envoy-ext_authz/ext_proc-,
  Traefik-forwardAuth/Native-UDS- sowie lighttpd-Stock/Patched-Quellen,
  Manifeste, Harnesses und englische/deutsche Connector-Dokumente.
- Neue fokussierte Tests: Common-C-Vertrags-/Runtime-/Transport-/Client-Tests;
  HAProxy-Binding-/Overlay-/Harness-Tests; Envoy-/Traefik-Observer-Tests;
  Stock-Sidecar-/lighttpd-Gate-Tests; Apache-/NGINX-/Traefik-Contract-Tests.
- Nachvollziehbarkeit: dieser englische/deutsche Record und die gepaarten
  Archivindex-Einträge.

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Check | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte Apache/NGINX/lighttpd/Traefik-`python3 -m unittest`-Suite | Bestanden: 92 Tests, 4 erwartete Skips. |
| Stock-Sidecar-strikter-C17-Build plus direkter Loopback-`python3 connectors/lighttpd/tests/test_stock_sidecar_contract.py` | Bestanden: 11 Tests in 20,514 Sekunden für das finale Prebuilt-Sidecar-Artefakt. |
| `transaction_phase_contract_test` mit `-std=c17 -Wall -Wextra -Werror` | Bestanden. |
| `transaction_phase_runtime_companion_test`, `response_companion_transport_test` und `response_companion_client_test` mit demselben strikten C17-Modus | Bestanden. |
| `make -C connectors/haproxy check-htx-overlay` | Bestanden: 28 Quellchecks. |
| HAProxy-Binding-/Overlay-/Combined-Harness-`python3 -m unittest`-Suite | Bestanden: 12 Tests. |
| `go test -buildvcs=false -count=1 ./...` in Envoy ext_proc, Traefik Response Observer und Traefik Native-UDS-Middleware | Bestanden. |
| `python3 -m unittest tests.test_bilingual_docs` | Bestanden: 22 Tests. |
| `git diff --check` und der gescopte `.github`/`ci`-Diff-Check | Bestanden; keine CI-/Governance-Datei ist im Task-Diff. |
| `make check-bilingual-docs` und `make check-doc-links` | Nur fehlgeschlagen, weil nicht zugeordnete Dokumente auf im Task-Worktree nicht verfügbare `modules/ModSecurity-test-Framework`-Pfade verweisen. Die task-eigene English-/German-Paar-/Switch-Prüfung bestand; kein Link- oder CI-Workaround wurde ergänzt. |
| Kombinierte Capability-/Dokumentations-/Adapter-`python3 -m unittest`-Suite | Erwartet fehlgeschlagen bei 95 Tests/einem Fehler: unveränderter CI-Collector widerspricht dem wahrheitsgemäßen Traefik-forwardAuth-P2-Manifest; als `FND-PARENT-0947` festgehalten, nicht unterdrückt. |

## Runtime-Evidence

Der Stock-Sidecar-Test ist ein echter privater Loopback-Komponentenexchange
durch die Common Runtime. Er deckt P1--P4-Allow/Block, Limits, unsicheres
Framing, Body-lose Responses, Timeout, Cancel, Cleanup, Kapazität,
Connection-Reuse, nicht lesende Worker und terminale Zustell-/Reset-
Korrelation ab. Er ist kein Lauf durch eine unveränderte
Stock-lighttpd-Backend-Topologie.

Die Envoy- und Traefik-Tests sind Source-/Komponenten-Evidenz für die Observer
und ihren privaten Transport. Dieser Record promoted keine nicht ausgeführten
Host-, H2-, H3- oder client-sichtbaren Late-Action-Claims.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine unveränderte reale Stock-lighttpd-Backend-Topologie, keine vollständige
  native Hostmatrix, kein H2- oder H3-Lauf waren in diesem Task verfügbar;
  Komponenten-Evidenz wird in ihrem tatsächlichen Scope erfasst.
- Keine CI-Workflow-, Ruleset-, Required-Check- oder CI-Collector-Änderung
  wurde vorgenommen, weil der Benutzer CI ausdrücklich aus dem
  Implementierungsscope ausgeschlossen hat.
- Die repository-weiten Documentation-Make-Targets wurden ausgeführt und
  scheiterten nur an nicht verfügbaren Framework-/MRTS-Linkzielen außerhalb
  der in diesem Task geänderten Dateien. Der fokussierte bilinguale
  Dokumenttest bestand; der Task änderte keine externen Links, um ein grünes
  Ergebnis zu erzwingen.
- Hosted-PR-Checks, SonarCloud-, Review- und Merge-Evidenz existieren beim
  Commit dieses Records nicht. Sie müssen an den exakten Draft-PR-Head
  gebunden werden.

## Bekannte Einschränkungen

Der Task-Commit wurde vor seinem ersten Push gegen `origin/master`
(`5d71be74369123257851eb5ec612d7523a6b061d`) abgeglichen. Ein bestehender
Draft-PR #341 umfasst verwandte Envoy-/Traefik-Composite-Response-Arbeit; er
wird hier nicht verändert und seine Beziehung muss im Review sichtbar bleiben.

## Verbleibende Risiken

Real-Host-Coverage-Gaps und die aufgeführten Findings verhindern einen
`verified_pr`-Claim. Host-spezifisches Late-Action-Verhalten wird als
begrenzte Adapterübersetzung berichtet und nicht still zu einer erzwingbaren
Aktion promoted.

## Finaler Diff- und Review-Status

Der aktuelle Benutzer hat ausdrücklich einen PR verlangt. Dieser gepaarte
Record ist daher die erforderliche Nachvollziehbarkeit für einen Parent-
Draft-PR. Er autorisiert keinen Merge, keinen direkten `master`-Push, keine
CI-Scope-Erweiterung, keine Framework-/MRTS-Änderung, kein Gitlink-Update,
keinen Check-Bypass und keinen Risk Acceptance.

## Auslieferungsstatus

Ein abgeglichener task-eigener Commit ist für einen Draft-PR gegen `master`
vorbereitet. Zum Schreibzeitpunkt werden keine Remote-Branch-SHA, PR-Nummer,
Hosted-Check-Ergebnis oder Merge-Ergebnis behauptet.

## PR-#344-Remediation-Nachtrag vom 2026-08-26

Der Benutzer hat verlangt, dass der bestehende Draft-PR #344 auf den aktuellen
`master` gebracht und task-eigene SonarQube-Cloud-/Codex-Ursachen ohne
Abschwächung von Workflows oder Qualitätskontrollen behoben werden. Der
isolierte Follow-up-Branch hat die abgerufene `origin/master`-Revision
`c1653fb84201bc6a29c47723fa74e12270deb164` normal als
`b1b6e72294a654c96dc44c9db69d25a704084c8f` gemergt; er wurde weder rebased
noch force-gepusht oder nach `master` gemergt.

Die Remediation belässt die gemeinsame Profilregistrierung im
Connector-Eigentum, entfernt breite Kompatibilitätsmakros, schließt den
Apache-C17-/APXS-Buildpfad der Profilregistrierung und erhält die bestehenden
Contract-Checks nach Helper-Extraktion semantisch: Der Apache-Cleanup-Harness
linkt die reale Transaction-State-Implementierung und der HAProxy-HTX-Check
folgt Payload-Callbacks bis zu den Borrowed-Slice-Append-Helpern. Keine
`.github/workflows`-Datei, kein Ruleset, keine Branch-Regel, kein Required
Check, keine Sonar-Unterdrückung und kein Qualitätsschwellenwert wurde
geändert.

| Continuation-Check | Tatsächliches lokales Ergebnis |
| --- | --- |
| `make check-common-helpers-c17 check-common-sdk-contract check-common-security-contract check-common-memory-safety check-common-flow-integrity check-http-authorization-service-timeout` | Bestanden. |
| Fokussierte Connector-Adoption-/Wiring-Checks für HAProxy, Envoy, Traefik, lighttpd, NGINX und Apache; zusätzlich `make check-haproxy-htx-overlay` | Bestanden. |
| Apache-Request-Transaction-Cleanup-Python-/realer-APR-Harness sowie Apache-C17-Kompilierung mit task-eigenem Output-Root | Bestanden. |
| Direkte C17-Binärdateien für `transaction_phase_contract_test`, `transaction_phase_runtime_companion_test`, `response_companion_client_test` und `response_companion_transport_test` mit ihren realen Common-Source-Closures | Bestanden. |
| Fokussierte HAProxy-/Sonar-/Workflow-Python-Suite | Bestanden: 54 Tests. |
| `go test ./...` in Envoy ext_proc und Traefik Response Observer mit registriertem task-eigenem Go-Build-Cache | Bestanden. |
| `git diff --check` | Bestanden. |
| HAProxy-C17-Native-Header-Target | Vor der Kompilierung durch das Framework-eigene `nginx_pinned_provenance_ref_mismatch` blockiert; kein Bypass und keine Framework-Änderung. |

SonarQube-Cloud- und Hosted-Workflow-Evidenz für den exakten ausgelieferten
Head ist weiterhin ausstehend. Dieser Nachtrag behauptet daher keine
Null-Issue-Zahl, keine bestandene Quality Gate, keinen ready-for-review-Status
und keinen Merge, bevor diese Exact-Head-Ergebnisse beobachtet wurden.

## Progressiver-P4-Abschluss-Nachtrag vom 2026-08-26

Der Follow-up korrigiert einen beim Validieren des Response-Pfads gefundenen
Streaming-Lifecycle-Fehler: Wiederholte begrenzte Request- oder Response-Body-
Chunks müssen ihre bereits aktive P2-/P4-Phase fortsetzen; nur das explizite
finale EOS darf sie abschließen. Die Common Runtime erzwingt diese Regel nun.
Apaches Output-Filter leitet jedes normalisierte Pre-EOS-Brigade-Fragment
sofort weiter, erhält FLUSH- und Metadaten-Buckets, behält keine vollständige
Response-Brigade und committed den kanonischen Response-Status an der ersten
weitergeleiteten Body- oder FLUSH-Grenze oder bei terminalem leerem EOS. Der Stock-lighttpd-
Sidecar sendet nun feste 2-KiB-Response-Chunks durch die Common Runtime und
sofort an den Client, mit genau einem finalen P4-EOS.

Der englische/deutsche gemeinsame Vertrag, Apache- und Stock-lighttpd-Guides,
Capabilities und Matrix beschreiben nun dieselbe Semantik. Die Matrix behält
alle zehn logischen Connectorlösungen: rohe response-blinde Protokollpfade
sind ausdrücklich unsupported, während ihre dokumentierten begrenzten
Begleitkomponenten die erforderliche P3-/P4-Abbildung liefern. Keine
Workflow-, Ruleset-, Required-Check-, Scanner-Konfigurations-, Suppression-,
Allow-List- oder Qualitätsschwellenwert-Änderung wurde vorgenommen.

| Follow-up-Check | Tatsächliches lokales Ergebnis |
| --- | --- |
| `make check-common-helpers-c17` | Bestanden. |
| `python3 -B -m unittest -v tests.test_apache_phase4_response_regression_wiring tests.test_nginx_phase4_runner_wiring tests.test_bilingual_docs` | Bestanden: 39 Tests, 3 erwartete Framework-Gitlink-Skips. |
| Stock-Sidecar-Contract-Test mit GCC und danach mit `CC=clang` | In beiden Läufen bestanden: jeweils 11 Tests. |
| `CC=clang MSCONNECTOR_C_STD=c17 MSCONNECTOR_CFLAGS='-std=c17 -Wall -Wextra -Werror' make check-common-helpers` | Bestanden. |
| `make check-common-sdk-contract check-common-security-contract check-common-memory-safety check-common-flow-integrity` mit task-eigenem Build-Root | Bestanden. |
| Apache-Strict-C17-Check mit Clang und task-eigenem Output-Root | Bestanden. |
| Fokussierter Codex-Security-Diff-Scan des lokalen P4-Patches | Mit null reportable Findings abgeschlossen; aufbewahrter Report: `/var/tmp/codex/ModSecurity-conector/pr344-quality-gate-remediation-20260826/security-diff-p4-final-20260826/report.md`. |

Das Apache-Ergebnis ist Source-, Wiring- und Strict-C17-Kompilierungs-Evidenz;
ein echter Apache-Traffic-Lauf ist in dieser Umgebung weiterhin nicht
verfügbar. NGINX und Patched-lighttpd behalten ihre dokumentierten
host-spezifischen Runtime-Evidence-Lücken. Zu diesem Zeitpunkt wird keine
Behauptung zu SonarQube Cloud oder GitHub Actions für einen neuen ausgelieferten
Head gemacht: Diese Ergebnisse müssen nach dem normalen Abgleich gegen
aktuelles `origin/master` und dem Push beobachtet werden.

### Follow-up-Validierungsgrenzen

`make check-apache-request-transaction-cleanup` bestand seine 11 Python-Tests
und den realen APR-Lifecycle-Harness, und `make check-adapter-contracts`
bestand. Die Repository-Dokumentations-Make-Targets stoppten erneut nur an
unveränderten fehlenden Framework-/MRTS-Linkzielen.
`make check-apache-common-adoption` scheiterte an einer statischen Assertion,
die weiterhin das überholte `ap_save_brigade()`-Full-Response-through-EOS-
Design verlangt. Sie durch die Wiederherstellung dieses Bufferings zu erfüllen,
wäre ein Verstoß gegen den progressiven P4-Vertrag dieses Records; kein
CI-Check, Workflow und keine Suppression wurde geändert. Der Konflikt ist als
`FND-PARENT-0958` festgehalten und blockiert eine saubere Apache-Structure-
Workflow-Behauptung, bis ein separat autorisiertes, nicht abschwächendes
Control-Update vorliegt.

### Korrektur der Ownership partieller Response-Header

Der finale Source-Review identifizierte einen separaten Protocol-Integrity-
Defekt im Stock-lighttpd-Sidecar: Ein nichtblockierender Downstream-
Response-Header-Write konnte einige Byte emittieren, fehlschlagen und dennoch
dem generischen Error Handling eine zweite Fallback-Response erlauben. Der
Writer beobachtet jetzt Statuszeilen-, Feld- und Terminator-Byte kumulativ.
Jedes Nichtnull-Ergebnis beansprucht Client-Response-Ownership und unterdrückt
eine zweite HTTP-Response; der Common-Runtime-Response-Commit bleibt bewusst
erst nach einem vollständigen Header-Block.

`FND-PARENT-0959` ist lokal behoben und wartet auf Verifikation am exakten
ausgelieferten PR-Head. Die Stock-Sidecar-Komponentensuite einschließlich einer
begrenzten 64-KiB-Partial-Header-Socketpair-Regression bestand 12 Tests mit
GCC und erneut mit Clang. Ein unabhängiger Bypass-Review fand keinen
verbleibenden direkten Zweitresponse-Pfad. Dies ist Komponenten- und
Source-Path-Evidenz: Ein externer Stock-lighttpd-Host-Capture des
Close-after-partial-header-Pfads war nicht verfügbar. Keine Workflow-,
Quality-Gate-, Scanner- oder Suppression-Einstellung wurde geändert.

## Codex-Befundremediation-Nachtrag vom 2026-08-26

Vier aktuelle Produktbefunde wurden behoben, ohne Workflow, Quality Gate,
Scanner-Konfiguration, Suppression, Ruleset, Branch-Regel oder Required Check
zu ändern.

- Apache zeichnet die gemäß Common begrenzte Regel-ID und die terminale kanonische
  Entscheidung für eine disruptive P3-Response-Header-Intervention vor dem
  nativen Apache-Sink auf. Redirect-, Rate-Limit- und Block-Ergebnisse werden
  den gemeinsamen Entscheidungsarten zugeordnet; eine nicht korrelierbare
  Intervention schlägt vor dem Response-Commit fail-closed fehl.
- Der Stock-lighttpd-Sidecar wendet sein Response-Body-Limit nur an, wenn
  semantisch ein Body vorhanden ist, erkennt nur die exakte Methode `HEAD` als
  bodylos und liefert für jedes nicht unterstützte `Expect`-Feld 417, bevor
  ein Body gelesen oder Upstream freigegeben wird.
- Patched lighttpd markiert sowohl deklarierte Längen- als auch Streaming-
  Body-Limit-P2-Rejections als host-rejected. Dadurch wird das vorgesehene
  Incomplete-Body-Cleanup gewählt, statt einen ungültigen P3-Übergang zu
  synthetisieren.

| Lokaler Check | Tatsächliches Ergebnis |
| --- | --- |
| Direkte C17-Binärdatei `transaction_phase_contract_test`, einschließlich der maximalen Common-Regel-ID-Länge | Bestanden. |
| Fokussierte Apache-/Patched-lighttpd-Python-Suite | Bestanden: 28 Tests. |
| `make check-apache-intervention-cleanup` und Apache-C17-Kompilierung | Bestanden: 7 Tests und strikte C17-Kompilierung. |
| Stock-Sidecar-Loopback-Contract mit GCC und Clang | In beiden Läufen bestanden: jeweils 13 Tests. |
| Common-Helper-C17, Common-Security-/Flow-Integrity, Adapter-Contracts und lighttpd-Common-Adoption | Bestanden. |
| `git diff --check` | Bestanden. |

Dies sind ausschließlich lokale Source-, Komponenten- und
Kompilierungsergebnisse. Exakt-Head-SonarQube-Cloud- und Hosted-Workflow-
Ergebnisse müssen nach dem normalen Merge gegen aktuelles `origin/master` und
dem normalen Push des PR-Branches beobachtet werden.

Zwei unabhängige read-only Post-Patch-Reviews fanden keinen konkreten
erreichbaren Sicherheitsbypass. Ein Review identifizierte, dass anfängliche
lokale Apache-Regel-ID-Puffer kleiner als das Common-Maximum waren; beide
wurden auf
`MSCONNECTOR_MAX_RULE_ID_LENGTH` angeglichen und die strikte C17- sowie die
Maximum-Length-Contract-Prüfung wurden erneut erfolgreich ausgeführt.

## Codex-Thread-Remediation-Nachtrag vom 2026-08-27

Fünf offene Codex-Review-Threads am PR-#344-Head
`053ed5c827d28cd06fcb82709496b45baebf0a6e` wurden als task-eigene begrenzte
Protokoll- oder Lifecycle-Defekte erneut validiert und behoben, ohne Workflow,
Scanner, Quality Gate, Ruleset, Branch-Regel, Required Check oder Suppression
zu ändern. Das aktuell abgerufene `origin/master` bleibt
`6ccfd8de555855ac540fc4d3d9e330f82d5e8cff`; der Branch liegt bei `0 behind /
14 ahead`, daher ist weder Rebase noch History Rewrite erforderlich.

- Kanonische Request-/Response-`Content-Type`-Metadaten haben nun die
  akzeptierte Common-Header-Value-Grenze plus den erforderlichen Terminator.
- Eine absolute Deadline deckt nun den vollständigen MRC1-Request-Frame- und
  Result-Exchange ab, statt jeder Hälfte einen eigenen Timeout zu geben.
- Der Stock-lighttpd-Sidecar erlaubt gültige 304-Representation-Length-
  Metadaten, erhält ein Request-Target bis zur kanonischen URI-Grenze und
  lehnt eine abgeschnittene Upstream-Request-Line vor I/O ab.
- NGINX zeichnet die korrelierte kanonische BLOCK-, REDIRECT- oder RATE_LIMIT-
  Entscheidung vor seinem nativen Redirect-/Status-Sink auf; eine ungültige
  Entscheidung schlägt fail-closed fehl.

| Follow-up-Check | Tatsächliches lokales Ergebnis |
| --- | --- |
| Direkte C17-`transaction_phase_contract_test`- und `response_companion_client_test`-Binärdateien | Bestanden, einschließlich maximaler Content-Type-Metadaten- und kombinierter MRC1-Deadline-Regression. |
| `python3 -B -m unittest -v tests.test_nginx_upstream_security_contract` | Bestanden: 12 Tests. |
| `python3 -B -m unittest -v connectors.lighttpd.tests.test_stock_sidecar_contract.StockSidecarSourceContractTest` | Bestanden: 4 Source-Contract-Tests. |
| Stock-Sidecar-strikte-C17-Syntax, Common-Security-/Flow-/Adapter-/Memory-/Header-Fuzz-Checks sowie NGINX-Adoption-/Wiring-Checks | Bestanden. |
| Native-NGINX-C17- sowie dynamische Stock-Sidecar-/HAProxy-Komponentenläufe | Durch fehlende NGINX-Headers/Source und die ungelöste `libxml2.so.2`-Abhängigkeit des verfügbaren libModSecurity-Artefakts blockiert; keiner wird als bestanden berichtet. |

Ein unabhängiger Post-Patch-Sicherheitsreview fand in den fünf Korrekturen
keinen validierten reportable Finding. Die Auslieferung bleibt ausstehend: Der
Follow-up-Commit muss normal gepusht werden; anschließend sind
PR-Head-Gleichheit, Codex-Threads, SonarQube Cloud und Hosted Workflows für
diesen exakten neuen Head auszuwerten.

## P4-Limit- und Sonar-Remediation-Nachtrag vom 2026-08-27

Der Working-Tree-Nachtrag refaktoriert die zwei bestehenden SonarQube-Cloud-
New-Code-Stellen ohne Suppression, Exclusion, Quality-Gate-Änderung oder
Workflow-Änderung. Der Envoy-Response-Observer trennt terminale und
gestreamte Response-Body-Behandlung und behält die vollständige
Callback-Aggregatvalidierung vor der begrenzten MRC1-Chunk-Ausgabe bei. Der
NGINX-P4-Filter trennt Vorbereitung, Inspektion je Buffer, Prefix-Forwarding
und terminale Behandlung; sein lokaler Body-Limit-Pfad ruft nun den Common-
`REJECT`-Planner vor jedem nativen Forwarding auf. Damit schlägt ein aktueller
Over-Limit-Memory-, File- oder Mixed-Buffer fail-closed fehl, statt einen
uninspektierten Suffix weiterzuleiten.

Apache-Beispiele, Source-Kommentare, die generierte Konfigurationsreferenz
und der gemeinsame englische/deutsche Vertrag beschreiben konsistent das
progressive P4-Forwarding vor EOS. Keine `.github/workflows`-Datei,
Branch-Regel, kein Ruleset, Required Check, Scanner-Konfiguration oder
Qualitätsschwellenwert wurde geändert.

| Follow-up-Check | Tatsächliches lokales Ergebnis |
| --- | --- |
| `go test ./... -count=1` in `connectors/envoy/ext_proc` | Bestanden. |
| `go test -race ./internal/responseobserver -count=1` | Bestanden. |
| Fokussierte NGINX-Phase-/Runtime-Python-Suite | Bestanden: 29 Tests, 3 explizite Framework-Gitlink-Skips. |
| Fokussierte Apache-/Beispiel-Python-Suite | Bestanden: 25 Tests. |
| `make check-connector-config-reference` und `make check-common-helpers` | Bestanden. |
| `git diff --check` | Bestanden. |
| `make check-nginx-c17-lint` | Vor der Kompilierung blockiert/übersprungen, weil kompatible NGINX-Headers/Source fehlen. |

Das versiegelte, begrenzte Sicherheitsartefakt
`security-scan-20260827T043109Z-nginx-file-buffer` verzeichnet für diesen
Working-Tree-Review null reportable Findings und deferiert ausdrücklich die
native NGINX-Filter-Chain-Ausführung für File-, Mixed-Buffer-,
Downstream-Forwarding- und Connection-Reuse-Fälle. Es ist kein Native-Host-
Pass.

Das abgerufene `origin/master` ist
`6ccfd8de555855ac540fc4d3d9e330f82d5e8cff`; vor dem Follow-up-Commit liegt
der Task-Branch null Commits dahinter. Normaler PR-Push und die Beobachtung
der Hosted Workflows/SonarQube Cloud für den exakten Head stehen noch aus.
Der lokale Sonar-Client fehlt und sein Integrationsworkflow verlangt eine
explizite Freigabe vor jeder Tool-Installation oder Konfiguration; dieser
Nachtrag behauptet daher weder einen gehosteten Zero-Issue-Count noch ein
bestandenes Quality Gate.

## 2026-08-28-Nachtrag zu Stock/Common-Validierung und Auslieferungsstatus

Die Änderungen am Stock-lighttpd-Sidecar und an der Common-
Transaktionsintegrität wurden als ein begrenzter logischer Slice erneut
validiert. Der echte Stock-lighttpd-Backend-Lauf umfasste sieben H1-Fälle:
Allow mit Body, Allow ohne Body, P1-Deny, P2-Deny, P2-Body-Limit-Ablehnung,
P3-Deny und P4-Safe-Rate-Limit. Jeder Fall erzeugte, soweit anwendbar, die
kanonische P1--P4-Evidenz, begrenzte Events ohne Body-Payloads oder opaque
Handles sowie deterministisches Cleanup. P4 Strict bleibt unbeansprucht, da
kein gültiger Client-Abbruchnachweis vorliegt.

Die Common-Integrity-Event-Kette authentifiziert nun Entscheidungsmetadaten,
angeforderte und tatsächliche Aktionen, HTTP-Reason-/Default-Werte sowie
Redaktions-/Kürzungsflags. Der Stock-Verifier weist fehlerhafte, doppelte,
vertauschte oder nicht korrelierbare Engine-/Host-Entscheidungen zurück und
validiert das exakt begrenzte Event-Schema. Resolver-Artefakte werden
unmittelbar vor dem Prozessstart erneut gehasht und atomar mit restriktiven
Berechtigungen veröffentlicht.

| Follow-up-Check | Tatsächliches Ergebnis |
| --- | --- |
| Stock-Sidecar-Contract-Suite mit task-eigenen `MODSECURITY_INCLUDE_DIR` und `MODSECURITY_LIB_DIR` | Bestanden: 31 Tests. |
| Echter Stock-lighttpd-Backend-H1-Lauf | Bestanden: 7 Fälle. |

Es wurden keine Workflows, Scanner-Konfigurationen, Suppressions, Quality
Gates, Rulesets, Required Checks oder Branch-Regeln geändert.

Am zuvor ausgelieferten PR-Head
`7223b13650a5e999c062adb5993766b33b060eea` war `origin/master`
`6ccfd8de555855ac540fc4d3d9e330f82d5e8cff`; der Branch lag 18 Commits davor
und 0 dahinter. SonarCloud meldete Erfolg mit null neuen Issues, null
akzeptierten Issues, null Security Hotspots und null Sonar-Annotationen. Die
gehosteten Apache- und HAProxy-Runtime-Jobs schlugen weiterhin fehl, und der
Pull-Request-Range-Gitleaks-Check meldete weiterhin einen historischen
Finding. Diese Hosted-Ergebnisse müssen nach dem nächsten Push für den neuen
Head erneut ausgewertet werden.

NGINX bleibt in dieser Umgebung wegen der erforderlichen
Worker-Isolationsoperation `chown` blockiert. Patched lighttpd bleibt
unpromoted, weil das exakte Framework-Gitlink- und die Nicht-root-
Runtime-Voraussetzungen nicht verfügbar sind. Für Connectoren ohne
verifizierten Client-Abbruch-Capture bleibt strikte P4-Evidenz unbeansprucht.

## 2026-08-28-Nachtrag zur Apache/HAProxy-Hosted-Build-Remediation

Der Parent-eigene Build-Abschluss trennt einen fehlenden Connector-
Profile-Registry-Header von einer tatsächlich fehlenden libModSecurity-
Linkerabhängigkeit. Der generierte Apache-APXS-Build erhält nun den expliziten
Parent-Root-Include-Pfad für `connectors/profile_registry.h`; der strikte
Apache-Source-Check verwendet denselben Repository-Root-Include-Pfad. Die
Extraktion des Apache-Source-Archivs verwendet `--no-same-owner`, damit ein
task-eigener id-mapped- oder User-Namespace-Build-Root nicht beim
Wiederherstellen irrelevanter Archiv-Ownership-Metadaten scheitert.

Das disposable HAProxy-HTX-Overlay staged nun den Connector-eigenen
Profile-Registry-C-Source und Header, fügt nur dessen generierten
Worktree-Include-Pfad hinzu, linkt sein Objekt explizit, protokolliert seine
Hashes und hält Framework-Build-Logs unter dem task-eigenen HAProxy-Runtime-
Root. Der exakte Overlay-Patch und der Parent-Caller behalten die bestehenden
Source-Tree-/Output-Root-Checks. Dies ist ausschließlich eine Build-/Provenance-
Remediation; sie promotet keine HAProxy-Runtime-Evidenz.

| Follow-up-Check | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte Runtime-Component- und HAProxy-Overlay-Suite | Bestanden: 55 Tests, mit 5 erwarteten Framework-HEAD-Skips. |
| `make check-haproxy-htx-overlay` | Bestanden. |
| `APACHE_C_STANDARDS_OUT=<task-owned> make check-apache-c17` | Bestanden. |
| Standard-Output-Root von `make check-apache-c17` | Durch einen schreibgeschützten Standard-Output-Root blockiert; der oben genannte Rerun mit task-eigenem Output-Root bestand. |

Es wurden keine Workflows, Scanner-Konfigurationen, Suppressions, Quality
Gates, Rulesets, Required Checks oder Branch-Regeln geändert. Die
Exact-Head-Apache- und -HAProxy-Hosted-Runtime-Checks bleiben nach der nächsten
normalen PR-Head-Auslieferung ausstehend; ihre historischen Fehler und der
historische Gitleaks-Finding werden nicht allein aufgrund dieser lokalen
Evidenz als behoben behauptet.

## 2026-08-28-Nachtrag zu Clean-History und Exact-Head-Validierung

Der PR-Produktbaum wurde von `origin/master`
`6ccfd8de555855ac540fc4d3d9e330f82d5e8cff` als lokaler Ersatz-Commit
`47eefcd3432608361d093919ae117049034b86ea` neu aufgebaut. Vor diesem
Evidenznachtrag war dieser Ersatzbaum bytegenau gleich dem vorherigen
PR-Produktbaum bei `66155ac03681214c59bc9fc661145227980be130`. Der frühere
Head bleibt lokal unter einer dedizierten Backup-Referenz erhalten. Der
historische redigierte Gitleaks-Match liegt nicht in der Ersatz-Ancestry; der
Scan wird weder umgangen noch unterdrückt.

Die projektgepinnte Gitleaks-Binärdatei hat einen redigierten Scan von
`origin/master..47eefcd3432608361d093919ae117049034b86ea` ohne Findings
abgeschlossen. Der Scanner-Workflow sowie alle Workflow-, Scanner-, Quality-
Gate-, Ruleset-, Required-Check- und Branch-Rule-Dateien sind bytegenau gleich
dem vorherigen PR-Baum. Nach diesem Dokumentations-Commit sind noch ein
abschließender redigierter Scan und eine exakte `--force-with-lease`-
Auslieferung erforderlich; danach müssen Hosted Checks und SonarCloud für den
neuen Remote-Head beobachtet werden.

| Lokale Validierung | Tatsächliches Ergebnis |
| --- | --- |
| Common-SDK-/Security-/Flow- und Adapter-Contract-Checks; Common-C17-Helper; HAProxy-HTX-Overlay | Bestanden. |
| C-Transaktions-FSM-, Runtime-Companion-, Response-Companion-Client-, HAProxy-SPOE-Response-Companion-Backend- und UDS-Transporttests | Bestanden. |
| Fokussierte Common-/Apache-/NGINX-/Envoy-/Traefik-/lighttpd-Python-Contract-Tests | Bestanden: 115 Tests; 3 Framework-Gitlink-Mismatch-Skips. |
| Sonar-Wrapper-Authentifizierung | Über `/usr/local/bin/sonar-with-env` verbunden; keine Credential-Werte gelesen oder persistiert. |

Der UDS-Transporttest verwendet einen privaten kurzen Taskpfad, weil die
Länge von Unix-Domain-Socket-Pfaden begrenzt ist. Das Sandbox-Standard-`/tmp`
ist schreibgeschützt, und ein langer Evidenzroot überschreitet `sun_path`; der
Rerun mit kurzem Pfad bestand und begründet keinen Produktdefekt. Der
Framework-Checkout ist nicht initialisiert und erforderliche Host-Binärdateien
fehlen. Deshalb bleiben echte Host-/Client-H1-Evidenz—einschließlich des nur
aggregierten gehosteten HAProxy-Runtime-Fehlers—und Patched-lighttpd-Evidenz
unverifiziert. Diese Lücken sind nicht bestanden und weder Kompatibilitäts-
noch Safe-Mode-Fallbacks. Der PR bleibt Draft, bis Exact-Head-Hosted- und
Host-Runtime-Evidenz die genannten Akzeptanzkriterien erfüllt.

## 2026-08-28-Nachtrag zur finalen Review-Thread-Remediation

### Motivation und Akzeptanzkriterien

Am damaligen Draft-PR-#344-Head
`efcaa86d5afd225aa7402cec424b3c7e785b212d` identifizierten sechs ungelöste
Final-Head-Review-Threads Begrenzungs-, Lifecycle- und Protokolldefekte in den
Response-Companion-Pfaden von Envoy, Stock-lighttpd und HAProxy. Die lokalen
Akzeptanzkriterien sind, dass ein gültiger ein-MiB-Envoy-Response-Callback
innerhalb einer endlichen Receive-Grenze bleibt, dass ein Projection-Rollback
keinen Same-UID-Pfadnamenersatz entfernen kann, dass Stock lighttpd begrenzte
Nicht-Upgrade-Informationsresponses weiterleitet, während nur die finale
Response P3 erreicht, und dass gequeuete HAProxy-Owner-Arbeit keinen
callback-eigenen Entscheidungstext nach der Callback-Rückkehr behält.
Common/MRC1-Headergrenzen müssen einschließlich C-String-Terminatoren exakt
bleiben.

### Technische Entscheidungen und geänderte Komponenten

- Envoy ext_proc akzeptiert nun einen ein-MiB-Response-Body zuzüglich 64-KiB
  begrenztem gRPC-Framing-Headroom (`1114112` Bytes) und behält das 64-KiB-
  Sendelimit. Eine bufconn-Regression sendet den vollständigen begrenzten Body
  durch den tatsächlichen gRPC-Server.
- Der Envoy-Composite-Verifier verwendet anonymes `O_TMPFILE`-Staging und
  behält bereits veröffentlichte owner-private Projection-Artefakte mit festen
  Namen nach einem späteren Fehler. Er versucht keinen nicht atomaren
  stat-then-unlink-Rollback eines Pfadnamens mehr, den ein Same-UID-Akteur
  ersetzen könnte.
- Der Stock-lighttpd-Sidecar erkennt den HTTP-Header-Terminator inkrementell
  in begrenzten Chunks und vermeidet wiederholte Full-Buffer-Scans. Er leitet
  begrenzte Nicht-Upgrade-`1xx`-Responses weiter, ruft P3 genau einmal nur für
  die finale Response auf und lehnt `101`-Upgrades weiterhin ab. Das
  englische/deutsche Stock-lighttpd-README-Paar dokumentiert nun diese
  sichtbare Protokollregel.
- HAProxy-Response-Companion-Callbacks erhalten begrenzten Session-Storage
  für Entscheidungstext. Ein verzögerter Owner-Task und sein kopiertes Ergebnis
  verwenden getrennten begrenzten Storage; Callback-Storage wird erst nach
  erfolgreichem Owner-Abschluss befüllt. Die Bridge akzeptiert die bestehenden
  Common/MRC1-Maxima für Header-Namen und -Werte zusammen mit ihren
  C-String-Terminatoren und behält Aggregate- und Count-Grenzen bei.

Die betroffenen Dateien sind die Common-Response-Companion-Transport-
Deklaration und ihr Test, Envoy-Observer/Projection und Tests, der
Stock-lighttpd-Sidecar und sein Test sowie HAProxy-Diagnosebridge, Backend,
Backend-Tests und die Lifetime-Regression für verzögerte Owner. Es wurden
keine Workflows, Scanner-Konfigurationen, Suppressions, Quality Gates,
Rulesets, Required Checks oder Branch-Regeln geändert.

### Sicherheitsauswirkung und Verifikation

Die betroffenen Sicherheitsgrenzen sind der private Response-Companion-
Owner-/Worker-Handoff, begrenztes Upstream-Response-Parsing und private
Projection-Ausgabe. Ein konkreter Pre-Fix-
AddressSanitizer/UndefinedBehaviorSanitizer-Harness reproduzierte einen
Heap-Use-after-Free, wenn ein Owner-Task nach einem Callback-Timeout
Entscheidungstext durch freigegebenen Callback-Storage schrieb. Die Reparatur
macht diesen Storage bis zu einer synchronen Kopie nach Abschluss task- und
result-eigen; derselbe Response-Header- und Response-EOS-Harness ist unter
beiden Sanitisern sauber. Die Projection-Änderung entfernt die Same-UID-
Replacement-/Deletion-Race, statt Output-Validierung zu schwächen oder einen
Ersatz zu löschen.

| Lokale Validierung | Tatsächliches Ergebnis |
| --- | --- |
| `pytest -q tests/test_haproxy_transaction_contract_binding.py` | Bestanden: 23 Tests, einschließlich des ASan/UBSan-Harness für verzögerten Owner. |
| HAProxy-MRC1-Overlay-, kombinierte SPOE/HTX- und Binding-Contract-Suite | Bestanden: 36 Tests. |
| Envoy-Projection- und Stock-lighttpd-Sidecar-Suite | Bestanden: 31 Tests; 16 External-Runtime-Tests übersprungen, weil ihre native Runtime nicht verfügbar ist. |
| `go test -race -count=1 ./...` in `connectors/envoy/ext_proc` | Bestanden: alle acht Packages. |
| Direkter C17-Syntaxabschluss, direkter HAProxy-Backend-ASan/UBSan-Test und `make -C connectors/haproxy check-htx-overlay` | Bestanden. |
| `pytest -q -p no:cacheprovider tests/test_bilingual_docs.py` und `make check-bilingual-docs` | Bestanden: 22 Tests; der Repository-Checker meldete `bilingual docs ok`. |
| `git diff --check` | Bestanden. |

### Runtime-Evidenz, nicht ausgeführte Checks und Restrisiko

Dies sind fokussierte Source-/Komponenten- und Sanitizer-Controls, keine neue
vollständige Native-Host-Evidenz. Der Successor-PR-Head ist beim Schreiben
dieses Nachtrags noch nicht gepusht; Exact-Successor-GitHub-Checks,
SonarQube-Cloud-Analyse und Hosted-Connector-Runtime-Zellen müssen erneut
laufen. Die Wrapper-Abfrage für den Pre-Successor-Head meldete null offene/
bestätigte SonarQube-Cloud-Issues und ein `OK` Quality Gate, aber dieses
Ergebnis wird nach einem Successor-Push stale. Der nur aggregierte
HAProxy-Hosted-Runtime-Fehler, die nicht verfügbare vollständige
Ten-Host-Matrix und der fehlende frische externe Codex-Review bleiben nicht
bestandene Evidenzlücken. Der PR bleibt Draft; weder ein Merge noch ein
`master`-Push wird beansprucht.

## 2026-08-28-Nachtrag zur Sonar-Remediation

### Motivation und begrenzte Änderung

Der erforderliche verwaltete Sonar-Wrapper
`/usr/local/bin/sonar-with-env` ist nun über seine verwaltete Umgebung
authentifiziert. Seine Abfrage von PR #344 bei
`8a35aa6a752a28ce2062945c2d36e8ee7c41574c` ergab ein `OK`-Quality-Gate,
aber zehn offene aufgabeneigene Code-Smell-Issues. Das explizite
Akzeptanzkriterium ist null offene Issues; deshalb gilt das grüne Gate allein
nicht als Abschluss.

Die Remediation macht ausschließlich P3/P4-Response-Companion-Callbacks
const-korrekt. Ihr begrenzter Decision-Scratch-Storage gehört nun zum
Worker-eigenen Session-State des Transports und wird bei Initialisierung,
CLAIM, CANCEL und RELEASE erneut gebunden. Ein P3/P4-Callback kann nur durch
diesen begrenzten Pointer schreiben, solange er synchron läuft; er kann weder
die Session-Capability ändern noch den Pointer behalten. HAProxy lehnt einen
fehlenden Scratch-Pointer vor dem Owner-Dispatch ab. Die bestehende
Task-/Result-Deep-Copy-Grenze bleibt für verzögerte Owner-Arbeit zuständig und
verhindert weiter die Verwendung von Callback-Storage nach einem Timeout.

Der gleiche fokussierte Patch führt außerdem eine verschachtelte
HAProxy-Result-Copy-Bedingung zusammen, ersetzt zwei verschachtelte
Stock-lighttpd-Header-Terminator-Ausdrücke durch explizite
Zustandsübergänge und teilt die unabhängigen Assertions, Blocking-, Fehler-
und Operation-Contract-Prüfungen des Backend-Test-Owners in Helper auf. Es
wurden kein Verhalten, Limit, keine Phasenreihenfolge, keine
Fail-open-/Fail-closed-Entscheidung, kein Workflow, Scanner, keine
Suppression, kein Quality Gate, keine Regel und kein Branch-Schutz geschwächt
oder geändert.

### Validierung und Kompatibilität

| Lokale Validierung | Tatsächliches Ergebnis |
| --- | --- |
| `pytest -q -p no:cacheprovider tests/test_haproxy_transaction_contract_binding.py` | Bestanden: 23 Tests, einschließlich der ASan/UBSan-Regression für verzögerten Owner. |
| Direkte C17-ASan/UBSan-Binärdatei für das HAProxy-Response-Companion-Backend | Bestanden, einschließlich des Fail-closed-Controls für fehlenden Decision-Storage. |
| `pytest -q -p no:cacheprovider connectors/lighttpd/tests/test_stock_sidecar_contract.py` | Bestanden: 16 Tests; 16 Native-Runtime-Tests übersprungen, weil diese Runtime nicht verfügbar ist. |
| C17-`-Wall -Wextra -Werror`-Syntaxchecks für Common-Transport, HAProxy-Backend/-Diagnoseruntime, Stock-lighttpd-Sidecar und Transport-Mock-Test | Bestanden. |
| `make check-haproxy-c17`, `make check-remaining-connectors-c17`, `make check-common-helpers-c17` und `make -C connectors/haproxy check-htx-overlay` | Bestanden. |

Die Änderung der P3/P4-Callback-Qualifizierer und der Ersatz des Inline-
Session-Members durch einen expliziten Scratch-Pointer sind für unabhängig
kompilierte externe Implementierungen dieser experimentellen Backend-Vtable
source-/ABI-inkompatibel. Interne Implementierungen und Mocks sind in diesem
PR aktualisiert. Externe Adapter müssen neu kompilieren und begrenzten
Scratch-Storage bereitstellen, bevor sie P3/P4 aufrufen; sie dürfen `const`
nicht wegcasten oder den Pointer behalten. Der Successor-Commit war zum
Zeitpunkt dieses Nachtrags noch nicht gepusht; deshalb muss die Wrapper-
Abfrage für genau diesen Remote-Head wiederholt werden, bevor null offene
Sonar-Issues beansprucht werden.

## 2026-08-28-Nachtrag zur Successor-Analyse

SonarQube Cloud analysierte den Successor
`f67395bf89f0ceb39b1629ed637b77bf07629bcd` mit `OK`-Quality-Gate und entfernte
acht der zehn früheren aufgabeneigenen Issues. Die exakte Analyse fand dennoch
zwei neue `c:S995`-Findings im HAProxy-Response-Companion-Backend-Test. Der
Follow-up ändert ausschließlich einen nur verglichenen Native-Transaction-
Parameter zu Pointer-zu-const und einen nur lesenden Fake-Owner-Parameter zu
Pointer-zu-const. Er ändert weder eine Produkt-API noch Testfall, Assertion,
Phase, Limit, Hostaktion, Scanner oder Quality Gate.

`pytest -q -p no:cacheprovider tests/test_haproxy_transaction_contract_binding.py`
bestand nach der Korrektur alle 23 Tests; auch der direkte C17-
`-Wall -Wextra -Werror`-Syntaxcheck und `git diff --check` bestanden. Die
nächste normale Successor-Auslieferung und ihre Exact-Head-Wrapper-Abfrage
bleiben erforderlich, bevor dieser Record null offene SonarQube-Cloud-Issues
beansprucht.

## 2026-08-29-Nachtrag zu Sonar-null und Traceability

### Scope und Implementierungsentscheidung

Dieser begrenzte Follow-up beseitigt nur echte von SonarQube Cloud gefundene
Duplikation und Testhelper-Komplexität. Commit
`d91a0df57daf5800fe3520c1f63e9f383c25d240` steuert identische
Envoy-Response-Header-Fälle tabellengesteuert, zentralisiert die gemeinsame
NGINX-Interventionsklassifizierung bei Beibehaltung jeder Hostaktion und
verwendet gleichwertiges Traefik-, lighttpd- und C-Transporttest-Setup wieder.
Commit `b2da4449672975f14d2c0953f7b779942af3122f` fasst danach die fünf
zusammengehörigen C-Transport-Setup-Werte in `mock_transport_setup` zusammen
und reduziert den Helper von zehn auf sechs Parameter. Er ändert weder ein
Connector-Protokoll noch P1--P4, Limits, Strict-/Safe-Verhalten, Callbacks,
Cancel, Cleanup oder produktives Source-Verhalten.

Es wurden kein Workflow, Ruleset, Required Check, keine Branch-Regel,
SonarQube-Einstellung, Exclusion, Suppression, Quality-Gate-Schwelle, kein
Testfall und keine `paths.env`-Datei geändert. Die Änderungen bleiben im
Parent-Repository; Framework- und MRTS-Source sowie Gitlinks bleiben
unverändert.

### Beobachtetes Exact-Head-SonarQube-Cloud-Ergebnis

SonarQube Cloud analysierte PR #344 bei
`b2da4449672975f14d2c0953f7b779942af3122f` am
`2026-08-29T10:05:19+0000`. Der verwaltete schreibgeschützte Wrapper
`/usr/local/bin/sonar-with-env` beobachtete alle geforderten Nullwerte:

| Metrik | Beobachtetes Ergebnis |
| --- | --- |
| Quality Gate | `OK` |
| Offene oder bestätigte Issues | `0` |
| Akzeptierte Issues | `0` |
| New-Code-Bugs | `0` |
| New-Code-Vulnerabilities | `0` |
| New-Code-Code-Smells | `0` |
| New-Code-Security-Hotspots | `0` |
| New-Code-Duplikatzeilen | `0` |
| Duplication on New Code | `0.0%` |

`new_coverage` wurde von der PR-Metrikabfrage nicht zurückgegeben; es wurde
keine Coverage-Datei entfernt, verborgen oder geändert. Das Quality Gate hat
keine fehlgeschlagene Coverage-Bedingung.

### Lokale Validierung und Sicherheitsgrenze

| Validierung | Tatsächliches Ergebnis |
| --- | --- |
| Direkter C17-Build von `response_companion_transport_test` mit `-Wall -Wextra -Werror` und Ausführung | Bestanden. |
| Common-Helper-, SDK-, Security-Contract-, Memory-Safety- und Flow-Integrity-Checks | Bestanden. |
| `make check-no-crs-source-normalization` | Bestanden: 124 Tests. |
| Envoy-Processor-Unit- und Race-Checks; Traefik-Observer-Unit- und Race-Checks | Bestanden. |
| Scoped NGINX-/lighttpd-Contracts | Bestanden: 32 Tests, ein erwarteter Stock-Sidecar-Loopback-Skip, weil lokale ModSecurity-Include-/Library-Pfade fehlen. |
| `git diff --check`, Go-Formatierung und Source-Tree-Bytecode-Inspektion | Bestanden. |

Ein unabhängiger fokussierter Review des C-Setup-Werte-Refactorings fand keine
Security-Regression: Callback-Binding, private `0700`-Socket-Verzeichnisse,
Timeout-Werte, Cancel-/Race-Assertions, Body-Payload-Ausschluss und
deterministisches Cleanup bleiben erhalten. NGINX C17 bleibt
`blocked_environment`, weil NGINX-Header/-Source lokal fehlen; sein
Common-Adoption-Check enthält weiterhin die zwei unveränderten dokumentierten
Body-Mapper-Assertions. Diese Einschränkungen gelten nicht als bestandene
Evidenz.

### Delivery-Grenze

Dieser gepaarte Dokumentationsnachtrag verschiebt selbst den PR-Head. Der
finale Remote-/PR-Head-SHA, Exact-Head-Hosted-Checks, das frische
SonarQube-Cloud-Ergebnis sowie der finale reguläre und Security-Codex-Review
werden deshalb nach diesem Dokumentationscommit erneut validiert. Um eine
selbstreferenzielle Commit-Schleife zu vermeiden, wird der finale SHA gemäß
der Repository-Traceability-Policy in der veränderlichen PR-Beschreibung und
der Task-Completion-Evidenz gebunden. PR #344 bleibt Draft und `UNSTABLE`;
dieser Record beansprucht weder einen Merge noch `verified_pr`.

## 2026-08-29-Nachtrag zur HAProxy-Hosted-Evidence-Projektion

### Motivation und Akzeptanzkriterien

Die bestehende HAProxy-Hosted-Runtime `with-crs/no-mrts` übersprang ihren
Evidence-Upload bewusst: Ihr Runtime-Root kann durch Prozesse mit derselben
Runtime-Identität verändert werden, daher würde dessen Kopie oder eine
Modusänderung keine vertrauenswürdige Upload-Grenze schaffen. Dieser begrenzte
Follow-up akzeptiert nur einen festen, erfolgreichen HAProxy-P2-Source-Receipt
und erzeugt nach Runtime-Cleanup ein neues kanonisches, begrenztes,
payloadfreies und secretfreies Metadatenpaket.

Die lokalen Akzeptanzkriterien sind strikte Source-Schema-/Pfad-/Typ-/Größen-/
Digest-Validierung, exakt die zwei Allowlist-Dateien
`haproxy-runtime-evidence.json` und `manifest.json`, ein getrennt besessenes
versiegeltes Staging-Paket sowie Checkout-Code, der niemals mit erhaltenem
Root-Privileg läuft. Die finale Abnahme verlangt zusätzlich, dass der exakte
gepushte PR-Head alle fünf Hosted-Runtime-Zellen abschließt, `Upload real
runtime evidence` als `success` zeigt, ein vom gemeinsamen Verifier
akzeptiertes Artefakt bereitstellt und die geforderten frischen externen
Checks und Reviews erhält.

### Technische Entscheidungen und Sicherheitsauswirkung

`ci/runtime/lifecycle/project-haproxy-runtime-evidence.py` verwendet nur die
Standardbibliothek und descriptor-relative `O_NOFOLLOW`-Reads, um Pfade,
Symlinks, Special Files, unerwartetes JSON, verbotene Metadatenkategorien und
nicht kanonische Ausgabe zurückzuweisen. Es entdeckt oder kopiert keinen
Runtime-Tree rekursiv. Der Harness schreibt den festen Receipt nach seinem
bestehenden Cleanup, statt Runtime-Ausgabe für den Upload bereitzustellen. Der
Workflow startet Runtime-, Source-Export-, Projektions-, Verifikations- und
finalen Summary-Code nur in einem privaten PID-/Mount-Namespace, nachdem
`setpriv` auf die vorgesehene unprivilegierte Identität mit `no_new_privs` und
gelöschten Capabilities/Gruppen abgegeben hat. Feste privilegierte Operationen
erzeugen, besitzen und versiegeln nur den Staging-Parent; sie führen kein
Checkout-Python aus und akzeptieren keine runtimekontrollierten Pfade.

Der untrusted Receipt passiert zuerst eine feste unprivilegierte
`head --bytes=16385`-Stream-Grenze und erreicht den Projektor danach nur über
Standardeingabe nach der Privilegabgabe. Der Projektor akzeptiert höchstens 16
KiB und weist das 16.385. Byte zurück; der Workflow sammelt damit keine
untrusted Receipt-Ausgabe in einer Shell-Variablen. Er ist kein Argument für
`sudo`, `unshare` oder `setpriv`.

Die exakten Git-Object-Checks binden jede Post-Runtime-Invocation an den
angeforderten Blob statt an einen Workspace-Pfad, den die vorangehende Runtime
ändern könnte. Sie beanspruchen nicht, dass PR-ausgewählter Code authentisiert
ist: Die Sicherheitseigenschaft ist, dass solcher Code sein Privileg bereits
verloren hat und im begrenzten Namespace läuft. Der finale Uploadpfad ist auf
die zwei erneut validierten Paketdateien begrenzt und behält
`if-no-files-found: error`.

Dies behebt die lokalen Findings `FND-PARENT-0987` (Checkout-Python war zuvor
über einen privilegierten Helper-Pfad erreichbar) und `FND-PARENT-0988` (ein
abgetrennter Runtime-Descendant konnte ein nur prozessgruppenbasiertes Cleanup
verlassen) auf Source- und Workflow-Contract-Ebene. Ihre Exact-Head-Hosted-
Validierung bleibt offen; keines der Findings wird als verified oder closed
erfasst.

### Geänderte Dateien und tatsächliche lokale Ergebnisse

Die Implementierung ändert den einen benannten Workflow, dessen finalen
Summary-Runner, den HAProxy-Smoke-Harness, den Projektor/Verifier sowie
fokussierte Projektor-, Harness-, Workflow-, CI-Security- und Runtime-Tests.
Dieses englische/deutsche Testing-Guide-Paar und dieses Change-Record-Paar
dokumentieren den neuen begrenzten Evidence-Vertrag. Es wurden keine Scanner-
Konfiguration, SonarQube-Einstellung, Exclusion, Suppression, Quality Gate,
Ruleset, Required Check, Branch-Regel, `paths.env`, Framework-, MRTS-,
`master`- oder Merge-Status geändert.

| Lokale Validierung | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte Projector-Unittest-Suite | Bestanden: 17 Tests; 9 Cross-Identity-Cases übersprungen, weil dieser Sandbox die erforderliche Host-Capability fehlt. |
| Fokussierte Harness-, Workflow- und CI-Security-Unittest-Suite (retained Python Environment) | Bestanden: 40 Tests. |
| `make check-ci-security-contract` | Bestanden: 125 Tests; 5 Host-Capability-Cases übersprungen. |
| `actionlint` für `.github/workflows/test-connectors-with-crs-no-mrts.yml` | Ohne Ausgabe bestanden. |
| `zizmor --offline .github/workflows/test-connectors-with-crs-no-mrts.yml` | Bestanden: `No findings to report. Good job!` |
| Unabhängiger Post-Patch-Security-Review | Kein konkreter verbleibender lokaler Root-Bypass-Pfad gefunden; er behielt Hosted-Namespace-/Cross-Identity-Ausführung als erforderliche Evidenz bei. |

### Runtime-Evidenz, nicht ausgeführte Checks und Restrisiko

Diese Ergebnisse sind nur lokale Source-, Contract- und statische Workflow-
Evidenz. Für diesen Nachtrag wurde noch keine finale Hosted-Runtime-Matrix
gestartet; es werden weder HAProxy-Artefakt, Secret-Scan-Ergebnis, CodeQL-
Ergebnis, finale SonarQube-Cloud-Abfrage noch frischer Exact-Head-regulärer/
Security-Review beansprucht. Das vorherige SonarQube-Cloud-Nullergebnis wird
stale, sobald diese Änderung den PR-Head verschiebt, und muss nach dem Push
über `/usr/local/bin/sonar-with-env` abgefragt werden.

Der lokale Sandbox kann die getrennten Hosted-Identitäten oder das erforderliche
`unshare`/`sudo`-Namespace-Verhalten nicht dynamisch beweisen. Der Workflow
prüft sie vorab und schlägt fehlgeschlossen fehl, statt zurückzufallen. PR #344
bleibt Draft und `UNSTABLE`; es gibt keinen `master`-Push, Merge, `verified_pr`
oder Produktions-Runtime-Claim.

## 2026-08-29-Nachtrag zu HAProxy-Upload-Leser und Sonar

### Root Cause und begrenzte Korrektur

Der Exact-Head-Hosted-Lauf `33260079101` belegte, dass der HAProxy-Runtime-
Schritt unter `set -u` abbrach, bevor er das Runtime-Target startete, weil
`SETUP_PYTHON_PATH` schrittlokal war. Der Runtime-Schritt erhält nun explizit
den direkten, action-besessenen `setup-python`-Output; er vertraut nicht dem
veränderbaren, über `GITHUB_ENV` exportierten Job-Level-Wert `PYTHON`.

Am selben Exact Head lag ein SonarQube-Cloud-Permissionsbefund für die
`0555`-Versiegelung des Evidence-Verzeichnisses vor. Das Paketverzeichnis
gehört jetzt der Evidence-UID, hat die Runtime-GID des Upload-Lesers als Gruppe
und wird mit `0550` versiegelt. Die zwei festen, payloadfreien Dateien behalten
die Evidence-Identität und `0444`; keine unbeteiligte Identität kann das
versiegelte Verzeichnis traversieren, während der Upload-Leser lesen, aber
nicht erstellen, ersetzen, umbenennen, unlinken, chmoden oder das Paket auf
andere Weise verändern kann. Dies vermeidet rekursive Kopie, ACL, Suppression
und einen privilegierten Checkout-Code-Pfad.

Die fokussierte Source-Korrektur entfernt außerdem die reproduzierten Sonar-
Regelmuster für redundante Exception-Typen, unsicheres Type Narrowing,
kognitive Komplexität, einen ungenutzten Summary-Parameter und einen
mehrdeutigen Exception-Test-Ausdruck. Sonar-Konfiguration, Exclusion,
Suppression, Quality Gate, CI-Anforderung, Ruleset, Branch-Regel und
`paths.env` blieben unverändert.

### Tatsächliche lokale Validierung

| Lokale Validierung | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte Projector-, Evidence-Workflow-, Harness- und CI-Security-Unittests | Bestanden: 59 Tests; 10 erwartete Cross-Identity-Skips, weil diese Sandbox die erforderlichen Identitäten nicht mappen kann. |
| Runtime-Workflow-Summary-Contract-Tests | Bestanden: 61 Tests. |
| `make check-ci-security-contract` | Bestanden: 125 Tests; 5 dokumentierte Host-Capability-Skips. |
| `actionlint`, `zizmor --offline`, `make check-bilingual-docs`, `make check-doc-links`, `sh -n` und `git diff --check` | Bestanden; zizmor meldete keine Findings. |
| Lokale Sonar-Agentic-Analyse | Nicht verfügbar: Die authentifizierte CLI meldet, dass Vortex für diese Organisation nicht verfügbar ist; dies ersetzt nicht die erforderliche PR-Analyse. |

### Verbleibende Exact-Head-Evidence

Der neue lokale Kandidat war beim Schreiben dieses Nachtrags noch nicht
committed oder gepusht. Daher werden weder Hosted-Runtime-/Upload-Ergebnis,
Artefaktinspektion, Secret-Scan- oder CodeQL-Ergebnis, SonarQube-Cloud-
Nullergebnis noch frischer regulärer und Security-Codex-Review beansprucht.
Diese Checks müssen auf dem exakten Successor-PR-Head erneut laufen, und PR
#344 bleibt bis dahin Draft.

## 2026-08-29-Nachtrag zu immutable Git-Blobs und begrenztem Cleanup

### Evidenzgebundene Korrektur

Der Exact-Head-Hosted-Lauf `33263212757` erreichte in den vier Nicht-HAProxy-
Zellen den finalen Summary-Schritt, endete jedoch mit Status `2`; HAProxy-
Projektor und -Verifier verwenden dasselbe Launcher-Muster. Die vier
eingebetteten Python-Launcher bildeten ihren Git-SHA-1-Preimage mit
druckbaren `b"\\0"`-Bytes statt mit Git's erforderlichem NUL-Trennbyte
`b"\0"`. Eine direkte Current-Blob-Berechnung reproduzierte, dass der korrekte
NUL-Preimage der Git-Object-ID entspricht, die druckbare Form dagegen nicht;
somit schlug jeder Launcher vor `exec(compile(...))` fehl. Die Korrektur ändert
nur diese vier Trennbyte-Literale. Object-ID-Check, 128-KiB-Source-Grenze,
sanitisierte Git-Umgebung, Namespace, Identity Drop, Capability Clearing und
fail-closed Shell-Verhalten bleiben unverändert.

Die HAProxy-Cleanup-Regression verwendet einen `setsid`-Leader mit einem
TERM-ignorierenden Nachfahren. Der vorherige reine Gruppen-TERM-Pfad ließ diese
Gruppe sichtbar und lieferte ein fehlgeschlagenes Cleanup zurück. Der Harness
gibt dem aufgezeichneten Leader nun ein begrenztes Grace-Fenster, wartet auf
ihn, sobald er beendet oder als reapbarer Zombie erkennbar ist, beendet danach
verbleibende Gruppenmitglieder und eskaliert erst nach einem weiteren
begrenzten Fenster auf `KILL`. Er weist weiterhin einen nicht beendbaren Leader
oder eine nicht leere Gruppe zurück und unterdrückt Receipt, Projektion und
Upload bei jedem Fehler. Der ergänzte `ps`-Preflight ist nur für den bereits
vorhandenen Evidence-Receipt-`setsid`-Modus erforderlich; er unterscheidet
einen beendeten, aber noch nicht gereapten Leader von einem weiterlaufenden
Leader, sodass normales erfolgreiches Cleanup nicht jedes begrenzte Fenster
verbraucht.

### Tatsächliche lokale Validierung

| Lokale Validierung | Tatsächliches Ergebnis |
| --- | --- |
| Immutable-Git-Blob-Workflow-Regression vor der Korrektur | Wie beabsichtigt fehlgeschlagen: Der Workflow enthielt null von vier korrekten NUL-Trennbytes. |
| Immutable-Git-Blob-Workflow-Regression nach der Korrektur | Bestanden. |
| Cleanup-Regression mit TERM-ignorierendem Nachfahren vor der Korrektur | Wie beabsichtigt fehlgeschlagen: `stubborn process group remains alive after cleanup`. |
| Fokussierte HAProxy-Cleanup-Harness-Suite nach der Korrektur | Bestanden: 6 Tests. |
| Fokussierte Projector-, Workflow-, Harness-, CI-Security- und Runtime-Summary-Suite | Bestanden: 122 Tests; 10 erwartete Cross-Identity-Skips. |

### Verbleibende Exact-Head-Evidenz

Dieser Successor ist beim Schreiben dieses Nachtrags noch lokal. Es werden
weder erfolgreiche Five-Cell-Hosted-Runtime, HAProxy-Artefakt-Upload/-Inspektion,
Secret Scanning, CodeQL, Successor-SonarQube-Cloud-Nullergebnis noch frischer
regulärer und Security-Codex-Review beansprucht. Diese Checks müssen an den
späteren exakten gepushten Head gebunden werden; PR #344 bleibt Draft, und
Scanner-, Quality-Gate-, Ruleset-, Required-Check-, `paths.env`-, `master`-
oder Merge-Änderungen sind nicht Teil dieser Arbeit.

## 2026-08-29-Nachtrag zur begrenzten HAProxy-Build-Target-Diagnose

### Aktueller Hosted-Status

Der Exact-Head-Five-Cell-Workflow
[`33266984528`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/33266984528)
lief auf `8757a8d1689d6cccd70327b681b9bb90f7e44433`. Apache, Envoy, Traefik
und lighttpd endeten erfolgreich. Der HAProxy-Job `99138670479` scheiterte
beim Vorbereiten der Runtime-Komponenten, noch vor Projektion, Verifikation,
Upload oder Artefakterzeugung. Seine bestehende sanitisierte Ausgabe belegt den
tatsächlichen Nonzero-Exit, enthält aber keine allowlistete Compiler-/Linker-
Klassifikation. Dieser Nachtrag schreibt den aktuellen Fehler daher nicht
einer früheren historischen Header-Diagnose zu.

### Begrenzte Korrektur und Sicherheitsgrenze

Der Provisioning-Helper liest nun ausschließlich GNU-Make-Fehlerfooter aus dem
erfassten `stderr`-Stream. Er akzeptiert genau zwei bestehende logische
Target-Namen — `build-modsecurity-binding` und `build-spoa-runtime` — oder
mappt die Output-Target-Schreibweise eines Footers nur dann, wenn sie
bytegenau dem intern abgeleiteten erwarteten Output-Pfad entspricht. Er gibt
höchstens ein festes Label `target_failure=<allowlisted-target>` aus.
Makefile-Pfade, Zeilennummern, Befehle, rohe Compiler-Ausgabe, beliebige
Targets, Secrets und alle target-ähnlichen Texte aus `stdout` werden verworfen.

Ein kontrollierter eigenständiger GNU-Make-Lauf bestätigt, dass ein
fehlschlagendes Prerequisite nur den File-Target-Footer und keinen
Phony-Goal-Footer liefern kann. Der exakte Vergleich mit dem erwarteten Pfad
erhält daher die kombinierte Invocation, deckt beide Make-Footer-Formen ab und
veröffentlicht den Pfad nicht.

Die Make-Invocation bleibt eine kombinierte Invocation; sie wird nicht allein
für Diagnosezwecke geteilt. Ein Fehler behält weiterhin seinen ursprünglichen
Status und Exit-Code, hält die rohe Build-Ausgabe privat und blockiert Receipt,
Projektor, Verifier und Upload unverändert. Das Label ist ausschließlich
Diagnosemetadaten, keine vertrauenswürdige Evidenz, und kann Cleanup,
Autorisierung oder Artefaktveröffentlichung nicht beeinflussen. Ein fehlerhaftes
Build-Rezept könnte auf `stderr` einen syntaktisch gültigen Footer fälschen;
dies kann nur die nächste Root-Cause-Untersuchung leiten, nicht die
Quellzuordnung beweisen.

Der unabhängige Review bewertete auch das numerische PID-Cleanup erneut. Die
historische Detached-Session-Bedingung bleibt in `FND-PARENT-0988` verfolgt.
Die Hosted-Runtime läuft vor dem separaten Owner-Staging in einem
verpflichtenden privaten PID-/Mount-Namespace mit `--kill-child=SIGKILL`. Ein
PID-/PGID-Wiederverwendungsszenario ist nicht reproduziert und bleibt auf
diesen Namespace begrenzt; es ist daher eine Verfügbarkeitsüberlegung und kein
neu validierter Cross-Stage-Integritätsbypass.

### Tatsächliche lokale Validierung und verbleibende Evidenz

| Lokale Validierung | Tatsächliches Ergebnis |
| --- | --- |
| Projector-, Evidence-Workflow-, Evidence-Harness- und Provisioning-Unittests | Bestanden: 93 Tests; 10 Cross-Identity-Tests übersprungen, weil diese Sandbox das erforderliche Hosted-Identity-Mapping nicht bereitstellt. |
| Security-Contract des Five-Cell-Runtime-Workflows | Bestanden: 1 Test. |
| Whitespace-Review | `git diff --check` bestanden. |
| Unabhängiger Post-Patch-Diagnose-/Security-Review | Keine Injection-, Pfadoffenlegungs-, Fail-open-, Cleanup- oder Upload-Grenzregression gefunden. |

Der nächste normale PR-Branch-Successor muss das Target in einem exakten
Hosted-Lauf benennen, bevor eine HAProxy-Build-Source-Korrektur erwogen wird.
Ein erfolgreicher finaler Exact Head erfordert weiterhin alle fünf
Runtime-Zellen, HAProxy-Projektion/Verifikation/Upload und Artefaktinspektion,
Secret Scanning, CodeQL, das vollständige SonarQube-Cloud-Nullziel sowie
frische reguläre und Security-Codex-Reviews. PR #344 bleibt Draft.

## 2026-08-29-Nachtrag zu begrenztem HAProxy-Diagnoseparser und Decoder

### SonarQube-Cloud-Remediation und Diagnosegrenze

Am exakten PR-#344-Head `1a6d711752d86033e8c0b959a73683e1125ff3bc` meldete
SonarQube Cloud einen offenen `python:S8786`-Befund im HAProxy-Make-Footer-
Parser. Das Quality Gate war `OK`, aber der offene Code Smell erfüllte das
verbindliche Nullziel des Users nicht. Die Regex wird durch einen
deterministischen ASCII-Parser für bestehenden Make-Präfix, optionalen
numerischen Job-Level, Footer-Delimiter, numerischen Exit-Code und optionalen
Location-Präfix ersetzt. Er behält die geschlossene Allowlist der zwei
logischen Targets und den exakten vertrauenswürdigen Outputpfad-Control. Er
gibt niemals erfassten Target- oder Pfadtext aus.

Das Diagnosescanning ist explizit pro Stream: `stderr` wird vor `stdout`
untersucht, pro Stream werden höchstens 512 Zeilen und 4096 Zeichen je Zeile
untersucht, und eine überlange untrusted Zeile stoppt diesen Stream. Erkannte
Resolver-, Compiler- und Linkerindikatoren werden nur auf feste Konstanten
abgebildet. Fehlerstatus, Exit-Code, Receipt, Cleanup, Projektion, Verifier,
Upload-Berechtigung und Event-Privacy-Controls bleiben unverändert.

Ein separater kontrollierter Child-Prozess zeigte eine Decodergrenze:
Ungültige Tooloutput-Bytes lösten zuvor `UnicodeDecodeError` aus, bevor der
HAProxy-Helfer sein Failed-Result zurückgeben konnte. `run_env` akzeptiert nun
eine optionale Decoding-Policy, aber nur `run_haproxy_binding_build` übergibt
`errors="replace"`. Andere Caller behalten striktes Decoding. Das exakte feste
Make-argv und der private Logpfad bleiben unverändert; das ursprüngliche
Nonzero-Ergebnis erreicht den bestehenden strukturierten Fehler- und
Cleanuppfad. Diese lokale Korrektur wird als `FND-PARENT-0990` bis zur
Exact-Delivered-Head-Hosted-Verifikation verfolgt.

### Root-Cause-Disziplin

Das vorherige Hosted-Target-Label `target_failure=build-modsecurity-binding`
ist keine Source-Cause-Diagnose. Ein unabhängiger Source-Review bestätigte,
dass die Binding-Common-Object-Schleife nicht die Response-Runtime-Source mit
ModSecurity-Headern kompiliert; die Response-Runtime-Schleife übergibt bereits
das aufgelöste Include-Verzeichnis. Es wird keine spekulative Makefile-
Include-Path-Änderung vorgenommen. Das nächste Exact-Head-Hosted-Ergebnis muss
eine feste allowlistete Ursache liefern, bevor eine HAProxy-Build-Source-,
Resolver-, Makefile-, Harness- oder Workflow-Reparatur erwogen wird.

### Tatsächliche lokale Validierung und verbleibende Evidenz

| Lokale Validierung | Tatsächliches Ergebnis |
| --- | --- |
| `tests.test_prepare_runtime_components` | Bestanden: 67 Tests, einschließlich deterministischer Footer-Grammatik/-Grenzen und Invalid-Text-Decoder-Regression/-Control. |
| HAProxy-Projector-/Workflow-/Harness-/Provisioning- plus ausgewählter Five-Cell-Contract | Bestanden: 99 Tests; 10 erwartete Cross-Identity-Skips. |
| `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract` | Bestanden: 125 Tests; 5 Host-Capability-Skips. |
| HAProxy-Resolver- und libModSecurity-Kompatibilitäts-Contracts | Bestanden: 18 Tests. |
| Python-Compile-Check | `python -m compileall -q ci/provisioning/components/prepare-runtime-components.py` bestanden. |
| Workflow-/Dokumentations-/Shell-Static-Checks | `actionlint`, `zizmor --offline`, Harness-`sh -n`, `make check-bilingual-docs` und 22 bilinguale Doc-Tests bestanden. |
| Whitespace-Review | `git diff --check` bestanden. |
| Unabhängiger Post-Fix-Security-Review | Kein konkreter Decoding-Bypass, Command-Injection, Raw-Output-Disclosure, Fail-open-, Cleanup-, Projektions- oder Upload-Regressionsbefund. |

Das bestehende `stdout=PIPE`/`stderr=PIPE`-Capture und die private Buildlog-
Menge werden durch diese enge Decoder-Remediation nicht begrenzt und bleiben
eine Hardening-Beobachtung. Es änderten sich keine Workflow-, Scanner-,
Quality-Gate-, Suppression-, Ruleset-, Required-Check-, `paths.env`-,
Framework-, MRTS-, `master`- oder Merge-Zustände. Der nächste normale
Successor benötigt Exact-Head-Hosted-HAProxy-Evidenz, SonarQube-Cloud-
Nullergebnisse und frische reguläre sowie Security-Codex-Reviews; PR #344
bleibt Draft.

## 2026-08-29-Nachtrag zur exakten Resolver-Ursachenkorrelation

### Exact-Head-Grenze und enge Diagnose

Am exakten PR-#344-Head `888482e81348850c6281f446c8cadbae48d6f6da` beendete
der Workflow
[`33274434129`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/33274434129)
Apache, Envoy, Traefik und lighttpd erfolgreich. Der HAProxy-Job
`99158566221` scheiterte im realen With-CRS/No-MRTS-Schritt vor Evidenz-
Projektion, Verifikation oder Upload. Eine autorisierte begrenzte Inspektion
behielt nur `target_failure=build-modsecurity-binding`,
`classification=resolver_error` und `build_step=modsecurity_resolver` in
einer externen payloadfreien Summary. Der rohe Download des 76.712-Byte-
Joblogs wurde mit Checksumme festgehalten und aus dem Task-Root gelöscht; er
ist weder Repository-Inhalt noch Evidenz einer Source-Ursache.

Der Provisioning-Helper ergänzt den festen Wert
`resolver_cause=unresolved_runtime_dependencies` nur dann, wenn eine
begrenzte `stderr`-Zeile nach dem Entfernen genau eines terminalen CRLF-
Carriage-Return der bestehenden statischen Fehlerzeile des Resolvers entspricht.
Er parst weder Pfad, Header, Tooloutput, Credential noch Suffix. Eine Zeile
mit jedem zusätzlichen Inhalt behält höchstens die bisherigen generischen
Resolver-Labels, und derselbe Text auf `stdout` kann die neue Ursache-Enum
nicht auswählen. Die Diagnose bleibt advisory: Ein
Build-Rezept kann weiterhin eine statisch wirkende Zeile ausgeben; daher
grenzt eine ausgegebene Enum die Folgeuntersuchung ein, beweist aber nicht den
zugrunde liegenden Resolver-Input, die Abhängigkeit oder den Source-Owner.

Der ursprüngliche Nonzero-Build-Result, transaktionales Cleanup, private
Raw-Log-Behandlung, Receipt-Berechtigung, Projektion, Verifier, Upload-Gate,
Workflow-Berechtigungen sowie alle Scanner- und Quality-Gate-Einstellungen
bleiben unverändert. Dieser Nachtrag beansprucht keine Resolver-, Makefile-,
Connector-, Harness- oder Workflow-Reparatur.

### Tatsächliche lokale Validierung und verbleibende Evidenz

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
tests.test_prepare_runtime_components` bestand 68 Tests. Die neue Regression
deckt die exakte `stderr`-Zeile, ein Credential-tragendes Suffix, dieselbe
Zeile auf `stdout` und einen unbekannten Resolver-Fehler ab; bestehende
Integrationstests erhalten Fehlerstatus, ursprünglichen Exit-Code und
Staging-Cleanup-Controls.

Die aktuelle Hosted-Summary enthielt die exakte statische Resolverzeile nicht;
die tatsächliche Unterursache ist daher weiterhin nicht belegt. Ein normaler
Successor benötigt ein eigenes Exact-Head-Hosted-Ergebnis, bevor eine
Resolver- oder Build-Reparatur erwogen werden kann. PR #344 bleibt Draft und
benötigt weiter erfolgreichen Hosted-HAProxy-Evidenz-Upload, finale
Scanner-/Sonar-Evidenz sowie frische reguläre und Security-Codex-Reviews.

## 2026-08-30 Kandidatenvalidierung und verbleibende Entscheidungsgrenze

### Aktueller Kandidat und Sicherheitsgrenze

Zum lokalen Validierungszeitpunkt dieses Change Records war der breitere
Successor-Kandidat noch weder gestaged, committed noch gepusht. Sein
HAProxy-Anteil ergänzt eine Descriptor-Open-Regression für eine symlinkte
Zwischenkomponente des Quellverzeichnisses; das Cleanup im Receipt-Modus
verwendet feste vertrauenswürdige Prozesstools und `/bin/rm`, propagiert Fehler
beim Result-Writer und beim Startup-Cleanup und weist jedes unerwartete
Process-Inspection-Ergebnis zurück. Diese Änderungen erhalten die bestehenden
Receipt-, Projektions-, Verifier- und Upload-Gates: Ein fehlgeschlagenes
Cleanup kann kein zulässiges Receipt erzeugen.

Der Kandidat enthält außerdem die enge `python:S3776`-Hilfsextraktion im
HAProxy-Diagnosepfad sowie zuvor geprüfte Envoy- und Traefik-Härtungen. Die
Envoy-Arbeit löst die unmittelbar beobachteten Fälle Unlink-on-Error,
unexpected-`Serve`, Shutdown-Deadline und Late-Accept. Sie beansprucht nicht,
die separate Pathname-UDS-Race für Substitution und finalen Unlink unter
derselben effektiven UID zu lösen. Dieses Restrisiko bleibt lokal als
`FND-PARENT-0991`, `P1`, `blocked` und `requires_user_decision` erfasst: Die
erforderliche restart-kompatible UDS-Topologie kann nicht implizit sicher
ausgewählt werden. `FND-PARENT-0992`, der HAProxy-Receipt-Befund zur
Command-Resolution beim Cleanup, ist lokal behoben und wartet auf die
Hosted-Verifikation am exakten ausgelieferten Head.

Am exakten Remote-PR-Head `c1a9a80aa33959e418ac9467278a7685cc51399a`
scheiterte der Hosted-Workflow
[`33276652544`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/33276652544)
im HAProxy-Job `99164435759` während des libModSecurity-Resolvers, vor
Projektion, Verifikation oder `Upload real runtime evidence`. Das bekannte
Result ist `target_failure=build-modsecurity-binding`,
`classification=resolver_error` und `build_step=modsecurity_resolver`; es ist
keine Upload-Evidenz und rechtfertigt keine spekulative Makefile-Reparatur. Der
aktuelle SonarQube-Cloud-Readback für denselben Remote-Head enthält einen
offenen kritischen `python:S3776`-Befund (`AaBPeSvj3f23caWmipnJ`) in
`ci/provisioning/components/prepare-runtime-components.py`; für die noch
uncommittete Extraktion wird kein Nullbefund beansprucht.

Der Kandidat macht nun die bei zwei Paketdateien unvermeidliche Digest-Grenze
explizit, ohne einen Selbst-Digest zu erfinden: Nachdem der gemeinsame
Verifier beide festen Paketdateien erneut geöffnet und validiert hat, gibt er
einen kanonischen, mit Zeilenumbruch terminierten, höchstens 1-KiB großen
abgetrennten Record mit beiden SHA-256-Werten aus. Der Workflow erfasst diesen
Record außerhalb des Zweidateienpakets in einer festen root-owned-`0640`-Datei,
öffnet ihn mit `O_NOFOLLOW` erneut, weist nichtkanonisches JSON, doppelte
Schlüssel, nicht-ganzzahlige Schemaversionen, unerwartete Felder, unsichere
Ownership/Modus/Größe sowie alles außer den zwei festen Kleinbuchstaben-Digests
zurück und schreibt nur diese beiden validierten Werte in `GITHUB_OUTPUT`.
Der abgetrennte Record wird vor dem Upload entfernt; weder er noch ein
Runtime-Root ist Artefaktinput. Ein unabhängiger Post-Patch-Review fand in
diesem zusätzlichen Evidenzpfad keinen konkreten Bypass oder Regression.

### Tatsächliche lokale Validierung

| Lokale Validierung | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte HAProxy-Projector-Suite | Bestanden: 26 Tests; 11 erwartete Cross-Identity-Skips. Der Block-Device-Source-Test ist vorhanden, benötigt aber eine gemappte Cross-Identity-Fixture. |
| Python-Suite für Projector, Workflow-Contract, HAProxy-Harness, Provisioning, CI-Security und Traefik-Runtime-Security | Bestanden: 162 Tests; 11 erwartete Cross-Identity-Skips. |
| HAProxy-Receipt-Harness-Syntax und direkte Contract-Suite | Bestanden: `sh -n` und 14 Tests, einschließlich PATH-geschattetem `rm`, stale Startup-Cleanup, Result-Writer-Fehler und Process-Group-Controls. |
| Envoy-ext_proc-Observer | Mit einem kurzen isolierten Unix-Socket-Temporary-Root bestanden: `go test -race -count=1 ./...` über acht Packages und `go vet ./...`. |
| Traefik-Response-Observer | Mit einem kurzen isolierten Unix-Socket-Temporary-Root bestanden: `go test -race -count=1 ./...` und `go vet ./...`. |
| Statische Hosted-Workflow-Controls | Workflow-YAML-Validierung, `actionlint` und `zizmor --offline` bestanden. |
| Formatierung und Whitespace | `gofmt -d` für die geänderten Envoy-Dateien und `git diff --check` bestanden. |

Ein früherer Go-Testversuch mit einem zu tiefen Temporary-Verzeichnis schlug
fehl, bevor die relevanten Unix-Socket-Tests starteten (`bind: invalid argument`);
er zählt nicht als erfolgreicher Test. Die obigen Wiederholungen mit kurzem
Root sind die dokumentierte Evidenz.

### Delivery-Status und verbleibende Blocker

Der HAProxy-Runtime-Evidence-Workflow ist die eine ausdrücklich autorisierte
Workflow-Änderung dieses Kandidaten. Scanner, Quality Gate, Ruleset,
Required Check, `paths.env`, `master` und ein Merge wurden nicht geändert.
PR #344 bleibt Draft.
Die verbleibenden Delivery-Blocker sind: eine explizite Envoy-UDS-
Ownership-/Restart-Topologieentscheidung für `FND-PARENT-0991`; eine
source-spezifische Diagnose oder ein neuer erfolgreicher Hosted-Run für den
HAProxy-Resolverfehler; ein gepushtes SonarQube-Cloud-Nullergebnis am exakten
Head; danach die geforderte Artefakt-, Scanner- sowie reguläre und
Security-Codex-Review-Evidenz am exakten Head. Vor deren Vorliegen auf einem
letzten unveränderten Head wird kein finaler Hosted-Erfolg beansprucht.

## 2026-08-30 Beobachtung nach Auslieferung und Successor-Korrektur

Die autorisierte HAProxy-Evidence-Publication-Korrektur wurde als
`74aab90978107e0f104b4441a476dfa2d6a53279` committed und normal gepusht. Der
Exact-Head-Workflow
[`33285597376`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/33285597376)
bestand für Apache, Envoy, Traefik und lighttpd. HAProxy scheiterte in seinem
realen Runtime-Schritt vor Projektion, Verifikation oder Upload; daher wurde
sein Evidence-Upload fail-closed übersprungen und kein Artefakt-/Upload-Erfolg
behauptet.

Der Exact-Head-SonarQube-Cloud-Readback meldete zwei offene Issues:
`python:S5778` bei `tests/test_haproxy_evidence_projection.py:323` und
`python:S3776` bei
`ci/provisioning/components/prepare-runtime-components.py:9195`. Die lokale
S5778-Test-only-Anpassung erhält den Projector-Call; die lokale S3776-
Helper-Extraktion erhält das begrenzte stderr-first-/Fixed-Label-
Diagnostic-Verhalten. Keiner der beiden Punkte ist bereits ein Remote-Sonar-
Ergebnis.

`FND-PARENT-0993` dokumentiert und korrigiert einen lokalen Traefik-
forwardAuth-P3-Kompatibilitätsdefekt. Der C-Adapter übergibt jetzt Commons
Total-Header-Limit unverändert, während der Go-Observer die tatsächliche
MRC1-Framegröße durchsetzt. Seine Observer-Headergrenze ist von 128 auf die
256 von Common angeglichen; Controls decken 256 akzeptiert, 257 abgelehnt,
exakten 65.536-Byte-Payload akzeptiert, ein Byte mehr abgelehnt und einen
sparse Common-validen 65.204-Byte-Frame ab. Die fokussierte Python-Suite
bestand 16 Tests, `go test -race -count=1 ./...` und `go vet ./...` bestanden,
und die kombinierte betroffene Python-Suite bestand 162 Tests mit 11
expliziten Cross-Identity-Skips. Ein nativer C-Build wurde nicht ausgeführt,
weil diesem Checkout ein lokales libModSecurity-Include-/Library-Paar fehlt;
die exakte Hosted-Runtime bleibt der relevante Buildnachweis.

`FND-PARENT-0991` bleibt bewusst unstaged, bis die explizite Envoy-Pathname-
UDS-Topologieentscheidung vorliegt. PR #344 bleibt Draft; dieses Addendum
ändert weder `paths.env` noch Scanner, Quality Gate, Ruleset, Required Check,
`master` oder einen Merge.

## 2026-08-30 Begrenzter HAProxy-Resolver-Sentinel-Nachtrag

Am exakten Head `eabf2b07ed4e5f317e2435d5f40e5b48d84f92a1` ist der Workflow
[`33288804917`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/33288804917)
beendet. Apache, lighttpd und Traefik waren erfolgreich; Envoy und HAProxy
schlugen fehl. HAProxy erreichte erneut den realen Runtime-Schritt nach seiner
Evidence-Boundary-Vorbereitung, veröffentlichte aber vor dem Fehler nur
`target_failure=build-modsecurity-binding`, `classification=resolver_error`
und `build_step=modsecurity_resolver`. Projektion, Verifikation, Upload und
ein HAProxy-Artefakt liefen nicht. Das ist ein Release-Blocker, kein
Source-Cause-Ergebnis.

Der Successor-Kandidat gibt dem Resolver einen geschlossenen maschinenlesbaren
Kanal. Jeder kontrollierte `blocked`-Zweig gibt zuerst genau eine literale
Zeile `BLOCKED: HAProxy libModSecurity resolver: sentinel=<cause>` aus der
festen Allowlist von 22 Werten aus, behält anschließend seine bisherige
Detailzeile für Menschen und den Exit-Status `77`. Sieben additive Ursachen
benennen jede nichtleere Fehlermenge des festen öffentlichen Trios
(`modsecurity.h`, `rules_set.h` und `transaction.h`); die defensive Ursache
`headers_missing` bleibt der Fallback für einen nicht-exakten Zustand. Ein
unbekannter interner Code wird mit demselben Nonzero-Exit zurückgewiesen. Die
Legacy-Detailzeile wird nicht als Ursache geparst.

Der Python-Recognizer ordnet nur eine vollständige, begrenzte `stderr`-
Sentinel-Zeile festen Diagnosen `classification=resolver_error`,
`build_step=modsecurity_resolver` und
`resolver_cause=<allowlisted-value>` zu. Er akzeptiert die bestehende
Normalisierung eines einzigen terminalen CRLF, weist jedoch Suffix, zweites
Carriage Return, unbekannten Wert, überlange Zeile sowie denselben Text auf
`stdout` für die Ursachen-Korrelation zurück. Diese Fälle behalten höchstens
generische Resolver-Labels. Bei `GITHUB_ACTIONS=true` gibt genau eine erkannte
Ursache zusätzlich ausschließlich die feste Annotation
`::error title=HAProxy resolver diagnostic::resolver_cause=…` aus; kein
Rohpfad, Header, Body, Token, Command oder Tooloutput erreicht sie. Die
Annotation kann Buildstatus, Cleanup, Receipt-Berechtigung, Projektion,
Verifikation, Upload, Scanner oder Quality-Gate nicht ändern.

Die tatsächliche lokale Validierung dieses noch uncommitteten Kandidaten
bestand: Resolver-Shellsyntax; ein Python-Syntaxcheck im Speicher; 14
fokussierte Resolver-Tests; und 71 fokussierte Provisioning-Tests. Letztere
decken alle Sentinel, CRLF, Suffix-, stdout-, unbekannte und überlange
Zurückweisungen, einen zurückgewiesenen unbekannten internen Code, die
Nichtweitergabe privater Ausgabe sowie das exakte Annotationsverhalten ab. Der
Kandidat hat noch keinen Hosted-Run erzeugt; er belegt daher weder die
HAProxy-Root-Cause noch eine erfolgreiche Evidence-Publication.

## 2026-08-30 HAProxy-Cache-Vollständigkeit und MRC1-P3-Framing

Der gehostete HAProxy-Resolver meldete die begrenzte generische Ursache
`resolver_cause=headers_missing`. Der Resolver verlangt das öffentliche
v3-Trio `modsecurity.h`, `rules_set.h` und `transaction.h`, während das
Readiness-Prädikat des Shared Cache bisher einen Prefix mit nur
`modsecurity.h` und der Library akzeptierte. Der Parent-Cache-Publisher
verwendet nun dasselbe Drei-Header-Prädikat sowohl vor dem Veröffentlichen der
Source-Build-Ausgabe als auch vor der Wiederverwendung eines veröffentlichten
Prefix. Ein Marker-valider, aber unvollständiger Prefix wird damit verworfen
und neu gebaut, statt still den HAProxy-Resolver zu erreichen.

MRC1 behält seine generischen Frame- und logischen Namens-/Wertaggregatlimits
von 65.536 Bytes. Ausschließlich P3 `RESPONSE_HEADERS` wird opcode-bewusst:
Ein C-Peer darf einen Payload von höchstens 66.630 Bytes empfangen oder senden, genug für
das bestehende 64-Byte-HTTP-Versionmaximum, 256 Vier-Byte-Feldpräfixe und das
unveränderte logische 65.536-Byte-Aggregat. Andere Opcodes bleiben bei 65.536
Bytes. Die HTTP/1.1-Observer von Envoy und Traefik emittieren höchstens 66.574
P3-Payload-Bytes und weisen weiterhin mehr als 256 Felder oder ein Byte über dem
logischen Aggregat zurück; dies korrigiert Framing-Kapazität, erweitert jedoch
weder Phasen noch Header-Policy.

Der gemeinsame C-Transport behandelt diese Common-Count- und Aggregatgrenzen
als nicht verhandelbar: Initialisierung und Start weisen Counts außerhalb von
`1..256` und Aggregat-Byte-Grenzen außerhalb von `1..65,536` zurück, und der
Decoder wiederholt beide harten Grenzen vor jedem Backend-Header-Callback. Das
gilt auch, wenn die öffentliche Konfiguration nach der Initialisierung geändert
wird. Raw-P3-Controls weisen einen 257-Feld-Frame und ein 65,537-Byte-Aggregat
vor der Backend-Verarbeitung zurück; der reguläre Exact-Limit-P3-/Cancel-Control
bleibt akzeptiert und räumt deterministisch auf.

| Lokale Validierung | Tatsächliches Ergebnis |
| --- | --- |
| ModSecurity-Cache-Contract | Bestanden: 45 Tests, einschließlich vollständiger-Prefix-Reuse und deterministischem Rebuild nach dem Entfernen jedes erforderlichen öffentlichen Headers bei weiterhin validen Cache-Markern. |
| Provisioning- und HAProxy-Resolver-Contracts | Bestanden: 70 Provisioning-Tests und 14 Resolver-Tests. |
| Direkte C17-MRC1-Transportintegration | Bestanden mit `-std=c17 -Wall -Wextra -Werror`: 256 P3-Felder mit exakt 65.536 logischen Bytes werden akzeptiert, danach führt Cancel deterministisches Cleanup aus. |
| Envoy- und Traefik-Response-Observer | Bestanden: fokussiertes `go test -race -count=1` plus `go vet` mit kurzem task-eigenen Unix-Socket-Temporary-Root. |

Zum Zeitpunkt dieser lokalen Validierung hatte der Kandidat noch keinen
Successor-Hosted-Run erzeugt. Dieser Nachtrag behauptet nicht, dass allein die
Cache-Korrektur die gehostete HAProxy-Root-Cause beweist oder dass die
HAProxy-Evidence-Publication erfolgreich war. Kein Workflow, Scanner, Quality
Gate, Ruleset, Required Check, `paths.env`, `master` oder Merge ist Teil dieses
Nachtrags.

## 2026-08-30 Response-Companion-Listener-Recovery

### Motivation und Akzeptanzkriterien

`FND-PARENT-0997` erfasst einen reproduzierten gemeinsamen Lifecycle-Defekt:
Ein terminaler Common-Listener-`poll`- oder `accept4`-Exit löschte
`listener.running`, aber ein aufruferverwaltetes Ready-Flag konnte einen
späteren Envoy-ext_authz- oder Traefik-forwardAuth-Startaufruf weiterhin
erfolgreich machen. Die direkte HAProxy-SPOE/SPOP-native-HTX-Route hatte vor
dem Ownership-Übergang an das begrenzte Response-Backend keine gleichwertige
Live-Listener-Prüfung.

Die Akzeptanzkriterien sind, dass jeder opake P2-zu-P3/P4-Handoff einen
lebenden privaten Listener und Ablauf-Owner besitzt, ein beendeter Listener
vor einem frischen Start vollständig bereinigt wird, unvollständiger Cleanup
vor Ownership-Übergang fehlgeschlossen endet, normaler Live-Listener-Startup
akzeptiert bleibt und die direkte HAProxy-Reihenfolge von einer Regression
abgedeckt ist. Exact-Delivered-Head-Hosted-, SonarQube-Cloud- und Review-
Evidenz bleiben nach dem normalen Successor erforderlich.

### Technische Entscheidung und Security-Auswirkung

Der gemeinsame Helper
`msconnector_response_companion_transport_ensure_running` ist der einzige
Lifecycle-Seam. Er weist einen Transport ab, dessen Stopping-Zustand
unvollständigen Cleanup bedeutet, joint und bereinigt einen beendeten früheren
Listener und startet einen frischen privaten UDS-Listener. `ensure_started`
delegiert für Envoy und Traefik an ihn. HAProxy ruft ihn vor
`haproxy_modsecurity_transaction_handoff_response_companion` und
`haproxy_spop_response_companion_handoff` auf. Ein von null verschiedener
`pthread_join`-Result ist nun Cleanup-Fehler, sodass der Transport gestoppt
bleibt und nicht wiederverwendet werden kann.

Die Änderung erhält Private-UDS-, Peer-Identity-, begrenzte-Worker-, opake-
Handle-, TTL- und No-Payload-Event-Invarianten. Sie fügt keinen Netzwerk-
Endpunkt, Fallback oder Privileg hinzu. Unvollständiger Cleanup oder
Listener-Neustartfehler gibt den bestehenden fehlgeschlossenen Connector-Pfad
zurück, bevor ein Handle/Lease erzeugt werden kann. Der deterministische
Descriptor-Close-Test beweist den Lifecycle-Übergang, nicht eine Remote-Methode
für einen terminalen Kernel-Fehler; weder Autorisierungs-Bypass noch Fail-open-
Verhalten wurden beobachtet.

### Geänderte Dateien und Dokumentation

- `common/runtime/response_companion_transport.h`
- `common/runtime/response_companion_transport.c`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `tests/response_companion_transport_test.c`
- `tests/test_haproxy_transaction_contract_binding.py`
- `common/docs/transaction-phase-contract.md` und
  `common/docs/transaction-phase-contract.de.md`
- dieses englische/deutsche Change-Record-Paar

### Tests und tatsächliche Ergebnisse

| Validierung | Tatsächliches Ergebnis |
| --- | --- |
| Strikte C17-Listener-Recovery-Regression | Bestand mit `-std=c17 -Wall -Wextra -Werror`; nach erzwungenem terminalen Listener-Exit joint, startet und akzeptiert sie einen frischen privaten Client und entfernt den eigenen Socket. |
| Pre-Fix-Regression | Wie erwartet reproduziert: Exit `134` an der Assertion, dass ein Stale-Ready-Aufruf `listener.running` nicht false lassen darf. |
| HAProxy-Handoff-Contract | `python3 tests/test_haproxy_transaction_contract_binding.py` bestand; er beweist, dass `ensure_running` vor Transaktions-Ownership-Transfer und Backend-Handoff liegt. |
| Envoy-/Traefik-Companion-Contracts | `python3 -m unittest -v tests.test_envoy_transport_hardening_contract tests.test_traefik_transport_hardening_contract tests.test_traefik_forwardauth_p2_contract` bestand mit `39` Tests. |
| Common- und Adapter-Controls | `make check-common-helpers-c17 check-common-sdk-contract check-common-security-contract check-common-memory-safety check-common-flow-integrity` und `make check-adapter-contracts check-http-authorization-service-timeout` bestanden. |
| Dokumentation und Whitespace | `git diff --check`, `make check-bilingual-docs` und `make check-doc-links` bestanden gegen den finalen lokalen Kandidaten. |

### Runtime-Evidenz, nicht ausgeführte Checks und Einschränkungen

Die C-Regression ist ein lokaler Private-UDS-Runtime-Control. Sie beansprucht
weder eine deployte Envoy-, Traefik- oder HAProxy-Host-Runtime, noch existieren
für diesen uncommitteten Successor ein frischer Hosted-Check, ein
SonarQube-Cloud-Result oder ein Remote-Listener-Error-Trigger. Die direkte
`unittest`-Modulinvokation fand keine funktionalen HAProxy-Tests; daher wurde
der repository-native direkte Entry-Point der Datei verwendet; `pytest` ist
lokal nicht verfügbar. Keines dieser Ergebnisse wird als Produktfehler oder
als Regressionsevidenz behandelt.

### Finaler Review- und Delivery-Status

Der eine erlaubte unabhängige Post-Patch-Bypass-/Regression-Review fand die
direkte HAProxy-Sibling-Route. Sie wurde aus der Source bestätigt, in dieselbe
Remediation aufgenommen und alle obigen fokussierten Checks wurden erneut
ausgeführt; es wurde kein zweiter Review-Zyklus geöffnet. Zu diesem Zeitpunkt
der lokalen Validierung bleibt PR #344 Draft und enthält dieser Change Record
noch keine Successor-Delivery-Tatsache. Kein Workflow,
Scanner, Quality Gate, Ruleset, Required Check, `paths.env`, `master` oder
Merge ist enthalten.

## 2026-08-30 HAProxy-Preflight für nicht bereites ModSecurity

Der exakte Head `7f4f7a8a5060b4cc2d32a08116c66c95363146dc` erreichte die
gehostete Fünfzellen-Runtime-Matrix. Apache, Envoy, Traefik und lighttpd waren
erfolgreich; HAProxy scheiterte, nachdem die gemeinsame ModSecurity-Komponente
`modsecurity_build_failed` gemeldet hatte und der Resolver alle drei
öffentlichen Header als fehlend beobachtete. Dieses Ergebnis ist ein
Release-Blocker und kein Nachweis einer erfolgreichen HAProxy-Runtime-
Evidence-Publication.

Der Source-Trace fand eine Statusintegritätslücke im HAProxy-Preflight: Er
wies nur den literalen Zustand `blocked` zurück, während die kanonische Menge
bereiter Zustände exakt `present`, `built` und `reused` ist. Ein gemeinsamer
Record mit `failed`, `unknown`, fehlendem oder anderem nicht bereiten Status
konnte daher Host-Vorbereitung und Binding-Resolver erreichen. Der Resolver
blieb fail-closed, jedoch zu spät und mit vermeidbarer Gelegenheit für
hostabhängiges Auflösungsverhalten.

HAProxy weist nun jeden Zustand außerhalb von `READY_COMPONENT_STATUSES` vor
Cache-Reuse, Vorbereitung, Binding-Kompilierung, Linken oder umgebungsbasierter
Resolver-Fallback-Nutzung zurück. Es schreibt `blocked` und erhält den
Blocker-Grund der Quelle, mit dem bestehenden festen Fallback
`modsecurity_build_failed`. Die gemeinsamen Producer-/Cache-Prädikate, der
Resolver, Diagnostik und andere Connector-Preflights bleiben bei dieser engen
Korrektur unverändert.

Die direkte lokale Regression deckt `blocked`, `failed`, `unknown`, `corrupt`,
optional/nicht ausgewählt und fehlende Statuswerte sowie alle drei erlaubten
Zustände ab. Ein separater Sink-Test beweist, dass ein fehlgeschlagener
gemeinsamer Record weder HAProxy-Vorbereitung noch Binding-Build aufruft. Diese
beiden fokussierten Tests bestanden lokal; breitere Validierung und frische
Exact-Head-Hosted-Evidenz bleiben erforderlich, bevor PR #344 als verifiziert
gelten kann. Kein Workflow, Scanner, Quality Gate, Ruleset, Required Check,
`paths.env`, `master` oder Merge ist enthalten.

## 2026-08-30 Apache- und NGINX-Preflight-Parität für nicht bereites ModSecurity

Der nachfolgende Exact-Head-Review belegte dieselbe Statusintegritätslücke in
den zwei verbleibenden direkten Shared-ModSecurity-Konsumenten. Apache und
NGINX wiesen nur den literalen Zustand `blocked` zurück. Ein Record mit
`failed`, `unknown`, `corrupt`, einem optionalen/nicht ausgewählten Wert oder
ohne Status konnte daher ihre Cache-Reuse- und Host-Build-Fortsetzungen
erreichen. Der direkte Pre-Fix-Control lieferte für Apache und NGINX bei
`status=failed` jeweils `False`; auch der legitime Control `status=built`
lieferte jeweils `False`.

Beide Preflights verwenden jetzt dieselbe kanonische Allowlist wie HAProxy:
`READY_COMPONENT_STATUSES = {present, built, reused}`. Jeder Zustand außerhalb
dieser Menge schreibt `blocked`, erhält den Blocker-Grund der Quelle und nutzt
den bestehenden festen Fallback `modsecurity_build_failed`. Das Gate läuft vor
den Apache-Artifact-/Cache-Checks und `build_apache_source` sowie vor
NGINX-Cache-Reuse oder `nginx_prepare_or_reuse_runtime`; es kann damit aus
einer nicht bereiten gemeinsamen Komponente keinen bereit aussehenden
Host-Record veröffentlichen. Das gemeinsame Producer-/Cache-Schema, spätere
host-spezifische Preflights, Resolver-Verhalten, Transaktionsphasen und die
anderen acht Connectorlösungen bleiben unverändert.

Vier fokussierte Controls bestanden lokal: Apache und NGINX prüfen jeweils
alle sieben erfassten nicht bereiten Repräsentationen sowie die drei akzeptierten
Zustände; getrennte Apache-/NGINX-Sink-Controls beweisen, dass ein
fehlgeschlagener Shared-Record keine Host-Build-Fortsetzung aufruft. Der direkte
Post-Fix-Control liefert in beiden Funktionen für `status=failed` `True` und
für `status=built` `False`. Breitere Provisioning-/Cache-, Dokumentations- und
Exact-Successor-Hosted-Validierung bleiben erforderlich, bevor PR #344 als
verifiziert gilt. Kein Workflow, Scanner, Quality Gate, Ruleset, Required
Check, `paths.env`, `master` oder Merge ist enthalten.

## 2026-08-30 temporäre HAProxy-Komponentenfehlerklassifikation

### Motivation

Der isolierte HAProxy-Hosted-Runtime-Fehler endete bei einem generischen
privaten Expat- oder ModSecurity-Komponentenergebnis. Das ist keine ausreichende
Evidenz für eine Build-Umgebungs- oder Source-Korrektur. Diese temporäre
Diagnostik kann bei einem bewusst aktivierten manuellen Lauf genau eine feste
Klassifikation ausgeben, ohne ein rohes Buildlog zu veröffentlichen.

### Akzeptanzkriterien

Die Diagnostik ist standardmäßig ausgeschaltet, nur für das HAProxy-Target mit
seinem Evidence-Receipt nutzbar und gibt höchstens ein festes Tupel aus
Komponente, Build-Schritt, begrenztem Exit-Code und Klassifikation aus. Sie darf
keine Build-Ergebnisse, Records, Cleanup, Receipt-Berechtigung, Projektion,
Verifikation, Upload oder die Runtime-Sandbox ändern. Switch, Emitter und
dedizierte Tests werden nach einem aktivierten Dispatch in einem Successor
entfernt.

### Technische Entscheidungen

`workflow_dispatch` enthält einen Boolean-Input,
`haproxy_component_failure_diagnostics`, mit Standardwert `false`. Er wird nur
bei einem expliziten `true`-Dispatch zu
`RUNTIME_COMPONENT_FAILURE_DIAGNOSTICS=1` ausgewertet und nur innerhalb der
vorhandenen isolierten HAProxy-`env -i`-Umgebung weitergegeben. Der Provisioner
fordert zusätzlich `RUNTIME_COMPONENT_TARGET=haproxy` und
`HAPROXY_EVIDENCE_RECEIPT=1`.

Private Expat-/ModSecurity-Ausgabe wird nur im Speicher ausgewertet, um einen
statischen Allowlist-Wert auszuwählen. Die einzige Ausgabe hat die feste Form
`component=<enum> build_step=<enum> exit_code=<0..255|unavailable> classification=<enum>`.
Unbekannte Klassifikationen werden zu `unclassified`; unbekannte Komponenten
oder Schritte erzeugen keine Diagnostik. Bestehende Komponenten-Records
behalten ihr bisheriges Fehlerklassifikations- und Exit-Code-Verhalten.

### Sicherheitsauswirkung

Keine private Command-Ausgabe, kein Argument, Pfad, URL, Environment-Wert,
Header, Body, Credential, Token, Cookie oder Raw-Log wird ausgegeben oder zur
Evidence hinzugefügt. Die vorhandene `env -i`-, `unshare`-,
`setpriv --no-new-privs`-, Capability-Drop-, UID/GID-Isolation-, Cleanup-,
strikte Projektor-, Verifikator- und Fail-Closed-Upload-Grenze bleiben
unverändert. Ein unabhängiger Post-Patch-Sicherheitsreview fand keinen
Diagnostik-Leak und keine Sandbox-Regression.

### Geänderte Dateien

- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_prepare_runtime_components.py`
- `tests/test_ci_security_workflows.py`
- dieses englisch/deutsche Change-Record-Paar

### Tests und tatsächliche Ergebnisse

| Validierung | Tatsächliches Ergebnis |
| --- | --- |
| Fokussierte Diagnostik- und HAProxy-Workflow-Tests | Bestand: 5 Tests. |
| `tests.test_prepare_runtime_components` | Bestand: 81 Tests. |
| HAProxy-Workflow-Contract-Suites | Bestand: 38 Tests. |
| Runtime-, Projektions- und HAProxy-Harness-Contract-Suites | Bestand: 101 Tests; 11 umgebungsunterstützte Skips. |
| `actionlint` | Bestand für `.github/workflows/test-connectors-with-crs-no-mrts.yml`. |
| `zizmor` | Bestand für diesen Workflow; es meldete nur seinen Offline-Capability-Hinweis. |
| `git diff --check` | Bestand. |

### Runtime-Evidenz

Für diesen lokalen Kandidaten gibt es noch keinen aktivierten Diagnostik-
Dispatch, Commit, Push, Hosted-Runtime-Ergebnis, kein Artefakt und keine
Evidence-Publication. Die Diagnostik ist keine Produktreparatur und beweist
nicht die HAProxy-Ursache.

### Nicht ausgeführte Checks

`ruff` wurde nicht ausgeführt, weil lokal kein Executable verfügbar ist. Die
Checks für Zweisprachigkeit und Dokumentationslinks, der Delivery-Preflight
und die Hosted-/Manual-Dispatch-Checks sind zu diesem Zeitpunkt noch offen.

### Bekannte Einschränkungen

Das Tupel kann absichtlich keine Compiler-, Configure-, Linker- oder
Netzwerk-Nachricht über seine feste Klassifikation hinaus offenlegen. Ein
Ergebnis `unclassified` ist gültige Evidenz dafür, dass noch keine
source-gestützte Korrektur gerechtfertigt ist.

### Restrisiken

PR #344 bleibt Draft und ist auf eine sichere Exact-Head-Hosted-Diagnose und
anschließende Runtime-Verifikation blockiert. `FND-PARENT-0975` bleibt
`in_progress` / `blocked_missing_evidence`; das Preflight-
Statusintegritätsverhalten ist dort bereits abgedeckt und benötigt kein
dupliziertes Finding.

### Finaler Review-Status

Lokale Implementierung und unabhängiger Sicherheitsreview sind abgeschlossen.
Delivery, ein aktivierter begrenzter manueller Dispatch, vollständige
Entfernung des temporären Pfads und sämtliche Successor-Hosted-Verifikationen
sind noch offen. Keine Änderung an Workflow-Sicherheitskontrolle, Scanner,
Quality Gate, Ruleset, Required Check, `paths.env`, `master` oder Merge ist
enthalten.
