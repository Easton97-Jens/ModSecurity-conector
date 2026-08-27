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
