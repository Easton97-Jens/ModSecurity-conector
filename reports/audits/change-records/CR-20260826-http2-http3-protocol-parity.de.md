# Change Record: HTTP/2- und HTTP/3-Protokollparitäts-Workstream

**Sprache:** [English](CR-20260826-http2-http3-protocol-parity.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260826-http2-http3-protocol-parity` |
| Datum (UTC) | 2026-08-26 |
| Basis-Revision | `6ccfd8de555855ac540fc4d3d9e330f82d5e8cff` |
| Delivery-Status | Als `5e7b34d1887984f74d061872d7652a3f71d87856` committed, nach `feature/http2-http3-protocol-parity` gepusht und durch Draft-PR [#348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348) vertreten; lokaler, Remote- und PR-Head stimmten bei der initialen Delivery-Verifikation überein. Kein Merge. |

## Motivation und Problemstellung

Dieser unabhängige Parent-Workstream dokumentiert Evidence für HTTP/2- und
HTTP/3-Lifecycle-Parität über Apache, NGINX, HAProxy, Envoy, Traefik und
lighttpd, während HTTP/1.1 als Regressions-Baseline erhalten bleibt. Er ist
noch nicht abgeschlossen und keine Abschlussbehauptung.

## Akzeptanzkriterien

- Protokoll-, Stream-Identitäts-, Commit-, EOS- und
  Late-Intervention-Status für jeden ausgewählten Connector getrennt halten.
- `unknown`, H1, H2 und H3 im neutralen Common-Contract modellieren, ohne
  dieses Modell zu Adapter-Nachweis zu erheben.
- H3 unabhängig erfassen und H3-Runtime niemals ohne echten Traffic behaupten.
- Bei fehlender Runtime-Evidence die Formulierung source-level fixed / runtime
  not verified bewahren.
- Gleichwertige englische und deutsche Dokumentation und Traceability pflegen.

## Implementierungsentscheidung und Begründung

Common besitzt ein neutrales Protokoll-/Late-Intervention-Modell für `unknown`,
H1, H2 und H3, einschließlich Stream-Identität, Commit/EOS und
Stream-Reset-Auswahl. Dies beweist nicht, dass alle Adapter es verwenden.

Apache P3 leitet das Protokoll jetzt aus `ap_get_protocol(r->connection)` plus
kanonischem HTTP/1-`r->proto_num` ab; unbekanntes Protokoll schlägt fail closed
fehl. Common gibt für H2-Stream-ID 0 oder ein frei gesetztes `STREAM_RESET`
konservativ keinen Stream-Reset aus. NGINX erzeugt für H2-Streams kein
`Transfer-Encoding` mehr und besitzt einen geschützten H3-Pfad. Traefik markiert
`responseIncomplete` bei Host-, Engine-, Commit- und Source-Fehlern, darunter
ein nach Commit fehlgeschlagener EOS-Callback in `finish()` sowie
fehlgeschriebene oder nicht bestätigte Pre-Commit-Deny-/Fehlerantworten, und
unterdrückt falsches EOS sowie normales FINISH. Ein initiales `(0,nil)`
ReaderFrom delegiert nicht vor Pre-Commit-Kontrollen; es wird kein falsches
EOS- oder normales FINISH-Verhalten behauptet. Ein Pre-Commit-EOS-Enginefehler
markiert den Abschluss trotz eines sichtbaren Fallbacks als unvollständig.
Fehlende Applied- oder Late-Log-Only-Acknowledgements markieren den Abschluss
ebenfalls als unvollständig; normales FINISH wird nicht behauptet. Bei
Late-Log-Only-Ack-Fehlern erzeugt auch der delegierte ReaderFrom-EOF-Pfad kein
synthetisches EOS. Die
vollständige unabhängige Statusmatrix wird in `docs/protocol-parity.md` und
seiner deutschen Begleitdatei gepflegt.

## Security-Auswirkung

Die Grenze umfasst nicht vertrauenswürdigen Protokoll-, Stream-,
Response-Body-, EOS- und Late-Intervention-Zustand. Die dokumentierten
Änderungen bewahren das angegebene fail-closed-Verhalten und unterscheiden
Source-Evidence von Runtime-Evidence. Kein Security-Finding ist vollständig
verifiziert; die zutreffende Formulierung ist source-level fixed / runtime not
verified.

## Geänderte Dateien

- `docs/protocol-parity.md`
- `docs/protocol-parity.de.md`
- `ci/checks/common/check-common-helpers.sh`
- `common/include/msconnector/late_intervention.h`
- `common/src/late_intervention.c`
- `connectors/apache/src/msc_filters.c`
- `tests/test_apache_phase4_response_regression_wiring.py`
- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `tests/test_nginx_upstream_security_contract.py`
- `connectors/traefik/native_middleware/middleware.go`
- `connectors/traefik/native_middleware/middleware_test.go`
- `connectors/envoy/Makefile`
- `connectors/envoy/README.md`
- `connectors/envoy/README.de.md`
- `connectors/envoy/capabilities.json`
- `connectors/envoy/config/envoy-ext-proc-streaming.yaml.in`
- `connectors/envoy/config/prepare_envoy_ext_proc_config.sh`
- `connectors/envoy/ext_proc/internal/processor/processor.go`
- `connectors/envoy/ext_proc/internal/processor/processor_test.go`
- `tests/test_envoy_transport_hardening_contract.py`
- `reports/audits/change-records/CR-20260826-http2-http3-protocol-parity.md`
- `reports/audits/change-records/CR-20260826-http2-http3-protocol-parity.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

Das Framework-Submodul ist nicht initialisiert und wurde nicht geändert. MRTS
wurde nicht angefasst.

## Ausgeführte Befehle

Die Befehle und PASS-Ergebnisse in den folgenden Abschnitten von 2026-08 sind
historisch. Sie wurden nicht erneut ausgeführt oder auf die zusammengeführte
Revision vom 2026-10-24 übertragen. Die Aktualisierung vom 2026-10-24 nutzte
nur Quellreview, Go-Formatierung, JSON-/Python-Syntax-, Konfliktmarker-,
Git-Index- und Diff-Integritätsprüfung. Funktionstests, Builds,
Laufzeitverkehr und CI-Grünstatus sind durch den aktuellen Benutzerauftrag
zurückgestellt.

Der strukturelle Change-Record-Vertrag bestand. Der bilinguale
Dokumentationschecker meldet 22 bestehende fehlende Links in den nicht
initialisierten Framework-Checkout und keinen neuen task-eigenen Linkfehler.
Das vollständige Dokumentationslink-Target benötigt diese Abhängigkeit und
wurde nicht ausgeführt. Der Task-Diff gegen aktuellen Master hat keine
Whitespace-Fehler; die Prüfung des übernommenen Master-Deltas gegen die alte
PR-Basis meldet außerdem zwei bereits bestehende Leerzeilen am Dateiende in
Master-eigenen lokalen Inheritance-Templates, die unverändert erhalten wurden.

- `curl --http3` — beendet sich mit `2`.
- `rtk proxy env TMPDIR=<registered-run>/tmp GOCACHE=<registered-run>/build/gocache GOMODCACHE=<registered-run>/build/gomodcache GOPATH=<registered-run>/build/gopath GOTOOLCHAIN=local GOFLAGS=-mod=readonly GOPROXY=off go test -run 'Test(EngineErrorAfterCommittedResponseDoesNotInventResponseEOS|IncompleteHostWriteDoesNotInventResponseEOS|LateResponseDecisionDoesNotReplaceCommittedResponse|ReadFromEngineEOSErrorAfterHostCommitDoesNotWriteFailure|ReadFromInitialSourceErrorDoesNotInventResponseEOS)$' .` — bestanden (fokussierte Post-Patch-Go-Auswahl).

Die folgenden gelieferten Testergebnisse werden ohne erfundene Befehlszeilen
aufgezeichnet:

- 28 ausgewählte Python-Tests bestanden (Apache/NGINX/C/C++-Gruppe).
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v tests.test_apache_phase4_response_regression_wiring tests.test_nginx_upstream_security_contract tests.test_nginx_protocol_harness_contract tests.test_transport_lifecycle_artifacts tests.test_runtime_observation_contract` — bestanden (98 Tests, 1 erwarteter Framework-Identity-Skip).
- Frühere Baselines: 20 passed/3 skipped und 39 passed/2 skipped.
- Capability-Gruppe 93 hatte einen erwarteten Environment-Fehler wegen des
  fehlenden, nicht initialisierten Framework-Validators.
- Common C17 bestand.
- Common SDK/adapter/security checks bestanden.
- Apache C17 bestand.
- Apache fokussierter statischer Test bestand.
- NGINX statischer Test bestand.
- Traefik fokussierter Go-Test bestand; die erste Pre-Fix-Reproduktion schlug
  fehl.
- Die ursprüngliche direkte Post-Commit-Engine-Error-Reproduktion und die neue
  Initial-`ReadFrom`-Source-Error-Reproduktion schlugen vor der Reparatur fehl.
- NGINX native C17-Kompilierung war wegen fehlender NGINX-Header blockiert.
- Explizites task-worktree `make protocol-client` — mit Exit `2` beendet, weil
  der nicht initialisierte Framework-Gitlink kein `protocol-client`-Target hat.
- Apache statischer Test — bestanden.
- Apache C17 — bestanden.
- Common C17 helper — bestanden.
- Traefik-Pakettest — bestanden.
- Vier fokussierte Go-Regressionen schlugen absichtlich vor dem Fix fehl und
  bestanden danach.
- Drei test-first Go-Regressionen schlugen absichtlich vor dem Fix fehl und
  bestanden danach.
- Ein neuer test-first ReaderFrom-Regressionsfall schlug vor dem Guard fehl und
  besteht danach.

## Follow-up-SonarQube-Cloud-Remediation — 2026-08-27

Der exakte vorherige Draft-PR-#348-Head
`9e4cea8dfa9eff6dd4a48051f1500306f02e0f4d` hat den fehlgeschlagenen
SonarQube-Cloud-Check-Run `98318846059`: Issue `AaA_yqaofjcmWz1J_WHw`, Regel
`go:S3776`, markiert `TestReadFromInitialSourceErrorDoesNotInventResponseEOS`
bei `connectors/traefik/native_middleware/middleware_test.go:442` mit
kognitiver Komplexität `23`, obwohl `15` erlaubt sind. Der exakte aktuelle
Befund wird als FND-SONAR-0068 getrackt; er ist ein task-eigener
Wartbarkeits-Delivery-Blocker, kein Security-Finding.

Nur der vorhandene Table-Subtest-Body wurde in die test-lokale `t.Helper()`-
Funktion `assertInitialSourceErrorDoesNotInventResponseEOS` extrahiert.
`before_body`, `after_body`, Source-Error-Propagation, Response-Body-Checks,
der Closed-Transaction-Response-EOS-Guard und der Response-Body-Call-EOS-Guard
bleiben unverändert. Kein produktiver Source-Code, keine Protokoll-Assertion,
Scanner-Konfiguration, Quality Gate, Regel, Suppression, `NOSONAR`, Exclusion
oder False-Positive-Status änderte sich.

- `rtk proxy env GOCACHE=<task-owned-cache> GOTOOLCHAIN=local GOWORK=off GOPROXY=off GOSUMDB=off go test -mod=readonly . -run '^TestReadFromInitialSourceErrorDoesNotInventResponseEOS$' -count=1` — bestanden.
- `rtk proxy env GOCACHE=<task-owned-cache> GOTOOLCHAIN=local GOWORK=off GOPROXY=off GOSUMDB=off go test -mod=readonly . -count=1` — bestanden.
- `rtk proxy env GOCACHE=<task-owned-cache> GOTOOLCHAIN=local GOWORK=off GOPROXY=off GOSUMDB=off go vet -mod=readonly .` — bestanden.
- `rtk proxy gofmt -d middleware_test.go` — ohne Diff bestanden.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` und `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-doc-links` — nur durch fehlende Framework-Submodule-Link-Ziele im nicht initialisierten Parent-Gitlink blockiert (Exit `2`); keiner meldete einen geänderten Change-Record-Defekt.
- Zielgerichtete Change-Record-Pair-/Strukturvalidierung mit `ci/checks/documentation/check-bilingual-docs.py` — bestanden.
- `rtk proxy git diff --check` — bestanden.

Die Go-Befehle liefen in `connectors/traefik/native_middleware` mit einem
registrierten externen Cache und deaktivierter Modul-/Netzwerk-Akquisition;
Dokumentations- und Diff-Checks liefen aus dem Parent-Task-Worktree. Die
Exact-Successor-SonarQube-Cloud-Evidenz bleibt ausstehend, bis der fokussierte
Follow-up-Commit gepusht ist; hier wird kein Successor-Quality-Gate behauptet.

## Successor-SonarQube-Cloud-Duplikationsremediation — 2026-08-27

Der erste normale Successor, `1b8da7ff02489efc1b2bb2b37be46daa20d26cb4`, ist
gepusht und der übereinstimmende lokale, Remote- und Draft-PR-#348-Head. Sein
exakter SonarQube-Cloud-Check-Run `98507227257` hat keine GitHub-Annotationen
und die Suche nach ungelösten PR-Issues liefert null Ergebnisse; das
ursprüngliche `go:S3776`-Target reproduziert daher nicht mehr. Das Quality Gate
scheitert dennoch unabhängig an `new_duplicated_lines_density`:
`7.789678675754625%` / 80 neue doppelte Zeilen über sieben Blöcke, obwohl
`<= 3%` erforderlich ist.

Diese getrennte, task-eigene Testduplikation wird als FND-SONAR-0069 getrackt.
Ihre Evidenz identifiziert ausschließlich
`connectors/traefik/native_middleware/middleware_test.go`: Die Inline-Fixtures
für Pre-Commit-Commit-/Evaluation-/Acknowledgement-Errors und die Fixtures für
Direct-Write-/ReaderFrom-Late-Acknowledgement teilen wiederholtes Setup und
Incomplete-Response-Checks. Der neue lokale test-only-Refactor führt
`newDeniedResponseRecording`, `newLateAcknowledgementErrorTransaction`,
`serveResponseScenario` und `assertResponseIncomplete` ein; jedes benannte
Szenario, seine individuelle Fehlerquelle, der Direct-Write-/ReaderFrom-Pfad,
der No-Invented-Response-EOS-Guard und die `log_only`-Assertion bleiben
erhalten. Kein Produktionsquelltext, keine Scanner-Konfiguration, kein Quality
Gate, keine Regel, Suppression, `NOSONAR`, Exclusion, False-Positive-Status,
Framework-Gitlink, MRTS-Quelltext oder Merge änderte sich.

- Die fünf direkt betroffenen benannten Go-Tests bestanden vor und nach der
  Helper-Extraktion mit registriertem externem Cache und deaktivierter
  Modul-/Netzwerk-Akquisition.
- Package `go test -mod=readonly .`, `go vet -mod=readonly .`, `gofmt -d` und
  `git diff --check` bestanden nach der Extraktion.

Der normale Commit auf demselben Branch
`35c6b339da9144578b800a3877fded414f24fe31` wurde ohne History-Rewrite gepusht;
sein lokaler, Remote- und PR-Head stimmen überein. Der exakte SonarQube-Cloud-
Check `98514348339` bestand mit null Annotationen, null ungelösten Issues, null
neuen doppelten Zeilen/Blöcken und `0.0%` New-Code-Duplikation. FND-SONAR-0068
und FND-SONAR-0069 sind an diesem Draft-PR-Head `fixed`, bis zur
Post-Merge-Current-Master-Verifikation und Originalreproduktion. Dies behauptet
weder einen Merge noch vollständige H2/H3-/Runtime-Evidence.

## Envoy-Downstream-H1/H2-Profil und Metadaten-Härtung — 2026-08-27

Der ext_proc-Materializer wählt über
`EXT_PROC_DOWNSTREAM_PROTOCOL` jetzt ausschließlich `http1` (Vorgabe)
oder `h2`; ein unbekanntes Profil endet mit Status `2`. Das Rendering `http1`
kündigt ausschließlich ALPN `http/1.1` mit dem HTTP/1-HCM-Codec an. Das
Rendering `h2` kündigt ausschließlich ALPN `h2` mit dem HTTP/2-HCM-Codec und
`http2_protocol_options` an. `EXT_PROC_DOWNSTREAM_PROTOCOL` macht dieselbe
Auswahl über das Connector-Make-Target verfügbar. Dies ist ein
statischer/Profil-Contract, keine Client- oder Host-Aussage.

Die direkte `ext_proc`-Request-Header-Adaptergrenze bewahrt jetzt den
gelieferten Metadatenwert `HTTP/2` und weist doppelte, großgeschriebene und
nicht unterstützte Request-Pseudo-Header, ungültige Headernamen, CR/LF/NUL-
Headerwerte, Connection-spezifische Header für moderne Protokolle sowie
ungültige `TE`-Werte zurück, wenn das gelieferte Downstream-Protokoll HTTP/2
oder HTTP/3 ist. Die test-first-fokussierte Go-Auswahl schlug vor dem Guard
fehl und bestand danach. Der fokussierte Materializer-Contract und `sh -n`
bestanden.

Das bekannte Non-Loopback-Plaintext-ext_proc-Admission-Risiko bleibt als
FND-PARENT-0135 getrackt; dieses Increment fügt weder mTLS, Listener-
Admission-Control noch Raw-Lifecycle-Artifact-Protokollkorrelations-
Enforcement hinzu. Kein neuer Befund wird geschlossen oder hochgestuft.
Envoy-Config-Load, ein verwalteter H2-Client, ausgehandeltes ALPN,
Multiplexing, Reset-Verhalten und H3 bleiben nicht ausgeübt.

## Envoy-Helper-Extraktion zur Sonar-Remediation — 2026-08-27

Am aktuellen Pre-Remediation-Draft-PR-#348-Head
`1ecf2353e14832424cd492efa9919cb3c4418727` meldet SonarQube Cloud den
task-eigenen `go:S3776`-Befund `AaBDdUxoMD5aIOx72SVh`: Die Envoy-Request-
Metadata-Funktion hat kognitive Komplexität `33` bei erlaubten `15`.
FND-SONAR-0070 verfolgt ihn als Wartbarkeits-Delivery-Blocker, nicht als neu
behaupteten Sicherheits-Schweregrad.

Der enge Follow-up extrahiert Request-Metadata-State-, Pseudo-Header-,
gewöhnliche-Header-, Finalisierungs- und Attribut-Helper und erhält dabei den
vorhandenen Validierungspfad und das Fehlerverhalten. Fokussierte Metadata-
Tests, die vollständige Envoy-ext_proc-Go-Suite, `go vet`, Format-/Diff-Checks,
der Transport-Contract, Dokumentations-Checks, Shell-/JSON-Checks und
Konfigurationsreferenz-Checks bestanden. Ein frischer versiegelter
quellcodebasierter Security-Diff-Scan deckt die eine geänderte Produktdatei
vollständig ab und hat keine reportable neuen Befunde.

Der normale Successor `07a9d19cc3f1ee832c170d5cfc55cdd607349a66` stimmt mit
dem lokalen, Remote- und offenen Draft-PR-#348-Head überein. Sein
`SonarCloud Code Analysis`-Check `98552049461` bestand, das PR-Quality-Gate ist
`OK` und die Suche nach ungelösten Issues liefert null Ergebnisse, einschließlich
keines `AaBDdUxoMD5aIOx72SVh`-Targets. FND-SONAR-0070 ist an diesem Draft-PR-
Head fixed bis zur Post-Merge-Current-Master-Verifikation und Originalreproduktion.
Dieser Source-Review behauptet weder Envoy-Configuration-Loading noch
ausgehandeltes ALPN, H2-Multiplexing oder H3-Runtime-Evidenz und schließt
FND-PARENT-0135 nicht.

## Runtime-Evidence

curl hat HTTP/2, aber kein HTTP/3. `curl --http3` beendet sich mit `2`.
H3-Runtime ist `runtime_skipped_missing_client` und nicht verifiziert. Es wird
keine H2/H3-Traffic-Behauptung aufgestellt. Die tatsächliche
Traefik-H2/H3-Runtime wurde nicht ausgeführt.

## Nicht ausgeführte Prüfungen mit Begründung

Für diesen Dokumentations-Record wurden keine weiteren Befehle oder Ergebnisse
geliefert. Unbekannte Source-, Build-, Contract-, Runtime-, P1-, P2-, P3-, P4-
und Late-Intervention-Dimensionen bleiben wie in der Matrix als `not_run` oder
`blocked` ausgewiesen. Die versehentliche anfängliche Ausgabe im gemeinsamen
Build-Verzeichnis wird nur als lokale Storage-Beschränkung erfasst; sie ist
keine Protokoll- oder Runtime-Evidence.

## Bekannte Einschränkungen

Das Framework-Submodul ist nicht initialisiert. H3 fehlt in dieser Umgebung ein
Client. Für die Matrix ist keine Connector-Runtime-Evidence etabliert,
einschließlich H2/H3-Traffic. Die native NGINX-C17-Kompilierung bleibt wegen
fehlender NGINX-Header blockiert.

## Verbleibende Risiken

Das neutrale Common-Modell wird möglicherweise noch nicht von jedem Adapter
verwendet. Source-Level-Fixes wurden nicht zu Runtime-Verifikation erhoben.
Kein Security-Finding ist vollständig verifiziert.

## Finaler Diff- und Review-Status

**Anschließende Aktualisierung am 2026-10-30:** Parent-Master rückte erneut
auf `ee1345f17c5390fd2341751e88fc510c7e7b580c` vor (#433). Er wird ohne
History-Rewrite des veröffentlichten Heads `096170f7` (59 erfolgreiche Checks,
fünf Skips) in den Task-Branch integriert. Der einzige generierte Archivkonflikt
wird neu erzeugt; aktive Auswahl bleibt 100 und Connector-Produktcode unverändert.
Masters Framework-Pin `d3b47aec9410f7adc3bb40df1ea413c00c438e89` stimmt
mit dem Lock überein und enthält die Paket-/Ergebnis-API; die unten genannte
fehlende API ist damit überholt. MRTS-Pin unverändert. Gepaarte aktuelle Guides
und ein datierter Hinweis im historischen Paket-Record erhalten diese Trennung.
Separater Framework-Draft #143 bei `78b103f8` korrigiert die Annahme von
Protokoll-Abschlussdaten und ist nicht Teil des Parent-Pins. Bestehende gezielte
Integritäts-/Dokumentationschecks und frische Hosted-Prüfungen sind für den neuen
Parent-Head erforderlich. Dieses Increment schreibt keine Tests, Selektoren,
Hostqualifikation, MRTS-Änderung oder PR-nach-Master-Merge; bestehende Framework-
Tests kommen mit dessen Upstream-Pin hinzu.

**Aktualisierung vom 2026-10-30:** Der Benutzer setzt mit Integrität der
Integration als Scope und ohne neue Tests während des Testumbaus fort. Der
gesicherte Head `1dca1c8eabd17d71a3327ccf3f828c3c5cb8fa01` hat 59
Hosted-Prüfungen einschließlich Sonar bestanden, fünf wurden übersprungen.
Aktueller Master `ec18f9e92286379a2410e917f76e6a5502675804` wird durch
einen normalen Merge integriert. Der einzige Konflikt im Spezialistenarchiv
wird durch dessen Generator gelöst. Masters unveränderte Auswahl und erneuerter
Apache-Harness-Digest werden mit allen neun PR-Source-Bindings verbunden; alle
Digests stimmen. Das neu generierte Archiv hat 6228 On-demand-Definitionen;
die aktive Auswahl bleibt 100. Masters vier vorhandene Definitionen zur
Paketübergabe werden unverändert übernommen; kein Test oder Selektor wird in
diesem Increment neu angelegt. Produktseitige Protokolländerungen und Masters
Paket-/Ergebnis-Integritäts-Guards bleiben erhalten. Weder Framework- noch MRTS-
Gitlink ändert sich; die dokumentierte Abhängigkeit von einer späteren
Framework-API bleibt unqualifiziert. Validierung nutzt vorhandene
Konsistenzprüfungen und frisches Hosted-CI/Sonar; Server-Ergebnisse des neuen
Heads stehen bei Vorbereitung aus. Vollständige Protokoll-Laufzeitqualifikation
bleibt unvollständig.

**Aktualisierung vom 2026-10-28:** Der aktuelle CI-Reparaturauftrag hebt die
frühere Testzurückstellung auf. Der Branch übernimmt Master
`c5993ed9a7b59fc0bd58f105595ec79f596c88d6` mit erhaltenem veröffentlichtem
Head `ab3d4d27`. Sieben Merge-Konflikte in Apache, NGINX, Traefik und beiden
Archivindizes sind abgeglichen. Apache verbindet ausgehandeltes P3-Protokoll
mit der Native-Erfolgsprüfung; NGINX zählt den synthetischen Authority-Host
gegen das typisierte Client-Header-Limit; Traefik erhält geprüftes Close,
terminale Fehler, Abbruchverhalten und Unterdrückung falschen EOS/FINISH.

Alle fünf fehlgeschlagenen Struktur-/Lint-Jobs teilten das veraltete
Apache-Checker-Literal. Die korrigierten Apache-/NGINX-Guards bestehen direkt
und erhalten negative Umgehungsmutationen. Sonar-Issue
`AaF3fXFNfuQxuJn35iQJ` / `c:S859` wird durch Entfernen des Host-Namens-Casts
behoben, der `const` entfernt. Die fokussierte Auswahl besteht: 21
Python-Szenarien und 44 Traefik-Fälle mit Race-Detector. Eine veraltete
NGINX-Source-Assertion schlug zuerst fehl und bestand nach Korrektur ihrer
Erwartung. Python verwendete den vorhandenen lokalen Interpreter 3.14.4;
Hosted-Prüfungen für den aktuellen Head bleiben erforderlich. Acht
Source-Digests des aktiven Inventars sind ohne Änderung seiner 100 ausgewählten
Fälle erneuert; das Spezialistenarchiv ist durch seinen Quellgenerator neu
erzeugt. Inventar-Admission, Archivkonsistenz und Diff-Prüfungen bestehen.
Unabhängiges begrenztes Quellreview fand kein neues validiertes
Sicherheitsproblem. Hosted-CI- und Sonar-Ergebnisse des Successors stehen noch
aus; dies ist weder eine vollständige H1-/H2-/H3-Laufzeitqualifikation noch eine
Erlaubnis zum Merge nach Master.

Der erste Successor `2a6089c3` besteht erforderliches Sonar C++17 und alle fünf
reparierten Struktur-/Lint-Jobs. Sein Cast-Befund fehlt; zwei neue
`python:S1192`-Issues (`AaGD5oa6tqzpX64G6ssQ`, `AaGD5oa6tqzpX64G6ssR`)
werden durch gemeinsame Regex-Konstanten behoben; die acht betroffenen Apache-
Szenarien bestehen erneut. Der Fehlerpfad des C++20-Advisory-Issues
`AaGD49pqgIkAXNgRzIvR` / `c:S2259` widerspricht seiner aktuellen Quellansicht:
Ein expliziter Null-Return steht bereits vor der angeblichen Dereferenz.
Unabhängiges Review findet keinen erreichbaren Nullpfad. Eine minimale
Klarstellung verbindet die redundanten lighttpd-Fehler-Guards ohne
Verhaltensänderung zu einer NULL-first-Kurzschlussprüfung. Die zwei bestehenden
nativen Null-/Normalfälle bestehen; insgesamt sind es 67 unterschiedliche
ausgewählte Szenarien. Das neunte Source-Binding ist ohne Auswahländerung
erneuert. Bilingual-, Repository-Pfad- und Dokumentationslink-Prüfungen bestehen
nach Abhängigkeitssetup. Frische Hosted-Validierung des Successors bleibt
erforderlich; kein Server-Issue-Zustand oder Gate wird abgeschwächt.

**Aktualisierung vom 2026-10-24:** PR #348 wird vom alten Head
`81ccd883678c83dda8b4fee61a9acc8a4c4c633c` mit aktuellem `origin/master`
`42fd5a8e895aca3a36b09eb09fe5c7cf9c3399e3` durch einen normalen Merge
aktualisiert. Alle neun Konflikte sind abgeglichen: Envoy-Processor/-Test,
Traefik-Middleware/UDS/Tests, die Apache-Regressionsdefinitionsdatei und beide
Archivindizes. Aktuelle Master-Request-Body-Drains, Fehler-/Cleanup-Pfade,
Envoy-Hostpflicht, Dokumentation und Framework-Gitlink bleiben zusammen mit den
Protokolländerungen erhalten.

[Upstream-Issue #401](https://github.com/owasp-modsecurity/ModSecurity-nginx/issues/401)
ist als adaptereigene Änderung in
`connectors/nginx/src/ngx_http_modsecurity_common.h`,
`connectors/nginx/src/ngx_http_modsecurity_access.c` und
`connectors/nginx/src/ngx_http_modsecurity_mapper.c` integriert. Ein gemeinsamer
H3-only-Selektor stellt rohe empfangene Authority mit erhaltenem Port und
geklammerter IPv6-Form nur bereit, wenn kein expliziter Host existiert. Er
versorgt Common-Mapper, Hostname, native P1-Header und begrenzte Anzahl-/Byte-
Erfassung, ohne die NGINX-Headerliste zu verändern oder einen konfigurierten
Host zu erfinden. H3-Versionsmetadaten sind ausdrücklich `3.0`. Unabhängiges
Quellreview fand kein neues validiertes Sicherheitsproblem. Tests/Builds und
Runtime bleiben auf Benutzerwunsch `not_run`; dies ist weder eine Verified-PR-
noch eine Runtime-Abnahmebehauptung. Gepaarte Protokoll-, Connector- und
Ursprungsdokumentation sowie die maschinenlesbare Source Map halten denselben
Scope fest. Delivery nutzt den bestehenden Draft-PR und einen normalen Push;
kein PR-zu-Master-Merge ist autorisiert.

Die folgenden Absätze erhalten die historischen Delivery-Prüfpunkte.

Dies ist ein unabhängiger Draft-PR-Workstream. Die gepaarte Dokumentation und
der Change Record berichten ausschließlich beobachtete Ergebnisse. Commit
`5e7b34d1887984f74d061872d7652a3f71d87856` ist als
`feature/http2-http3-protocol-parity` gepusht und durch Draft-PR
[#348](https://github.com/Easton97-Jens/ModSecurity-conector/pull/348)
vertreten. Bei der initialen Delivery-Verifikation stimmten lokaler, Remote- und
PR-Head-SHA überein. CI-Prüfungen waren in Warteschlange oder in Ausführung und
werden nicht als bestanden behauptet. Kein Merge hat stattgefunden.

Das erste lokale Follow-up ist als
`1b8da7ff02489efc1b2bb2b37be46daa20d26cb4` gepusht; sein exakter Successor
löste das ursprüngliche `go:S3776`-Issue, scheiterte aber am unabhängigen
FND-SONAR-0069-Duplikations-Gate. Das zweite normale Follow-up
`35c6b339da9144578b800a3877fded414f24fe31` ist ebenfalls gepusht und sein
exakter SonarQube-Cloud-Check `98514348339` bestand sauber. Framework-Draft-PR
#112 ist getrennt; seine grünen Checks ändern weder Parent-Framework-Gitlink,
Parent-Delivery-Status noch MRTS-Scope.
