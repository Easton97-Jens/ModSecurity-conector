# Change Record CR-20260919-readiness-b-shared-remediation: Gemeinsame Readiness-B-Remediation

**Sprache:** [English](CR-20260919-readiness-b-shared-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260919-readiness-b-shared-remediation |
| Datum (UTC) | 2026-09-19 |
| Basis-Revision | `e475baabf0787cbc804f176ae998b62156892825` |
| Scope | Ausschließlich gemeinsame Parent-Connector-Remediation, direkt betroffene Tests und gekoppelte Dokumentation. Keine Framework-, MRTS-, Gitlink-, Dependency-, Regelprofil-, Scanner-, Quality-Gate-, Workflow- oder Merge-Änderung ist enthalten. |
| Delivery-Status | Draft-PR [#370](https://github.com/Easton97-Jens/ModSecurity-conector/pull/370) von `agent/readiness-b-ten-integrations-20260919`; kein Merge ist autorisiert. Das vorherige Korrekturinkrement erreichte `18303495bc9bdb64cef74aae0f39e40d29ca5492`; dessen gehosteter Apache-Lauf `35445064987` auf exakt diesem Head bestand den Final-Status-P2-Control. Die Envoy-Korrektur dieses Records besitzt nur Source-, Fixture-, C17-, Build- und Konfigurations-Evidenz; exakter aktueller Head und Hosted-Check-Status müssen bei der Auslieferung verifiziert werden und werden hier nicht abgeleitet. |
| Policy-Auflösung | Die Parent-Traceability-Policy verlangt dieses gekoppelte Record-Paar für die nicht triviale versionierte Arbeit; der etablierte Archivindex wird aktualisiert. |

## Motivation und Problemstellung

Die angeforderte Readiness-Prüfung über zehn Integrationen legte gemeinsam
behebbare Lücken offen, lieferte aber keine ausreichende vollständige Runtime-
Evidenz, um jeden Pfad auf Praxisreife B hochzustufen. Diese Änderung nimmt
enge Parent-eigene Korrekturen vor und bewahrt die Trennung zwischen Source- /
Contract-Evidenz und vollständiger Evidenz zu Host, Protokoll, Regelprofil,
Restart, Lifecycle und Observability.

Der exakte gehostete Apache-Bootstrap-Fehler identifiziert nun einen weiteren
Parent-eigenen P2-Availability-Defekt: Seine initiale Apache-Directory-
Konfiguration erreicht den Input-Filter mit ungesetztem Common-Request-Body-
Limit/Aktion, sodass der Common-Planner einen kleinen Body abweist, bevor
libModSecurity die P2-Regel auswerten kann. Die Korrektur muss eine endliche,
reject-by-default-Grenze bewahren, statt das daraus resultierende `413`
umzucodieren, ein Null-Limit als unbegrenzt zu behandeln oder eine nicht
unterstützte Aktion zu akzeptieren.

Die Envoy-HTTP-`ext_authz`-Quelle hatte außerdem zwei begrenzte,
Parent-eigene Vertragslücken: Der Response-Phase-Smoke wählte eine P1-only-
Regeldatei und seine Fixture emittierte nicht die von den Companion-Regeln
erwarteten P3/P4-Signale; seine HTTP-Autorisierungsanfrage nutzte ein
Callback-`path_prefix`, während das C-Profil client-kontrollierte URI-Hint-
Header bevorzugen konnte. Die Korrektur stellt die passende Fixture wieder her
und bindet P3 an den geschützten Pfad, ohne einem URI-Override zu vertrauen.
Sie ist kein Nachweis eines beobachteten Remote-Bypass und kein Ersatz für
einen echten Envoy-Host-Lauf.

## Akzeptanzkriterien

1. Die scoped Parent-eigenen Korrektheits- und Provenance-Lücken beheben, ohne
   Fail-Closed-, Ownership- oder Endpoint-Validation-Controls zu schwächen.
2. Unveränderliche Expat-Revisionsauswahl, Archive-Extraction-Ownership,
   Apache-APXS-Output-Platzierung und Peer-/lokale Endpoint-Provenance
   explizit und testbar halten.
3. Vollständige englisch/deutsche Dokumentation und dieses gekoppelte Change-
   Record-Paar pflegen.
4. Den tatsächlichen Reifegrad wahrheitsgemäß berichten: Diese scoped
   Remediation allein weist keine Praxisreife B für alle zehn Pfade nach.
5. Für das begrenzte Apache-Bootstrap-Profil getrennte Controls für einen
   kleinen P2-Regelblock (`403`), eine echte Over-Limit-Ablehnung (`413` ohne
   Handler-Inhalt) und einen Allow-Follow-up im selben Prozess (`200`) halten.
6. Für das Envoy-`ext_authz`-Smoke-Profil die passende P1/P3/P4-Fixture nur
   bei opt-in Response-Smoke und ungesetzter `RULES_FILE` wählen, P3 an
   `/phase3-block` plus den Upstream-Header binden und sicherstellen, dass kein
   vom Client gelieferter Original-URI-Hint das Policy-Ziel wählen kann.

## Implementierungsentscheidung und Begründung

- Der Expat-Component-Resolver verlangt in strikten und nicht strikten Pfaden
  unveränderliche vollständige Git-Objekt-IDs; veränderliche Referenzen und
  die Ersetzung durch das neueste Release gelten nicht als Pin-Evidenz.
- `TAR_OPTIONS="--no-same-owner"` wird für die NGINX-Source-Extraction
  erzwungen, damit Archivmetadaten während eines nicht privilegierten
  Handovers keine Ownership ändern können.
- Der Apache-APXS-Wrapper staged Profile-Registry-Inputs unter einem vom
  Aufrufer bereitgestellten externen Build-Root. Checkout-/Root-Symlinks und
  ein bereits vorhandenes symlinked `connectors`-Stage-Child werden vor dem
  Kopieren erzeugter Inputs abgelehnt.
- Stock-Lighttpd leitet Client-/Server-Endpoint-Metadaten mit `getpeername`
  und `getsockname` aus dem akzeptierten Sidecar-TCP-Socket ab; Unix-Domain-
  Sockets und unbrauchbare Endpoints werden abgewiesen, statt Request-Host-
  Metadaten zu verwenden.
- Das native Traefik leitet den Server-Endpoint aus `http.LocalAddrContextKey`
  ab; Request-`Host` bleibt Request-Metadatum und wird nicht als lokaler
  Engine-Endpoint vertraut.
- Nur der Apache-Input-Filter-Verbrauch eines Request-Body-Limits von null oder
  einer ungesetzten/nicht unterstützten Body-Limit-Aktion wird zum endlichen
  Common-Default von `1048576` Byte und zur Aktion `reject` aufgelöst. Dies
  bewahrt eine gemergte explizite Policy, wendet Defaults nicht bei der Per-
  Directory-Erzeugung an, legt keine neue Apache-Direktivenfläche offen und
  erlaubt keine Teilinspektion.
- Die isolierte Apache-Bootstrap-Fixture erhält einen festen synthetischen
  P2-Body-Marker, serielles `RelevantOnly`-Audit-Logging mit `ABFZ`, eine
  Assertion zum Ausschluss des rohen Markers, einen begrenzten Over-Limit-Body
  von 1049600 Byte, der `413` vor statischem Handler-Inhalt liefern muss, und
  einen Allow-Follow-up im selben Prozess. Dies ist ein begrenzter Regressions-
  /Harness-Control, kein Nachweis der vollständigen historischen FND-1098-
  Terminalsequenz oder der Apache-B-Reife.
- Der timing-abhängige Stock-Lighttpd-Loopback-TCP-Reset-Test wird durch einen
  kompilierten Source-Contract-Harness ersetzt. Eine statische Assertion
  verankert den P2-Zweig nach `finish_request_body` an
  `sidecar_finish_decision`; der Harness ruft diese produktive Terminalfunktion
  danach mit einer konstruierten P2-Decision auf und prüft echte
  Abort-Host-Action, Regelkorrelation und Transaction-Finalisierung. Er führt
  nicht dynamisch die vollständige P2-Pipeline aus.
- Der Envoy-Response-Phase-Default wählt die vorhandene
  `modsecurity_response_companion_smoke.conf` nur, wenn der Bediener keine
  `RULES_FILE` gesetzt hat; andernfalls bleibt die gezielte Request-only-
  Fixture erhalten. Die P3-Regel verkettet das exakte geschützte Request-Ziel
  `/phase3-block` mit dem servererzeugten Response-Header
  `X-Modsec-Upstream: block`; die Fixture liefert diesen Header und den
  begrenzten P4-Marker.
- Das HTTP-`ext_authz`-Callback-`path_prefix` und die Original-URI-Header-
  Präferenzen des Profils werden entfernt. Die Envoy-Vorlage schließt
  `x-envoy-original-path`, `x-forwarded-uri` und `x-original-uri` als
  Defense-in-depth aus der Autorisierungsanfrage aus; das C-Profil konsumiert
  unabhängig davon keinen dieser Header. Diese Korrektur dekodiert oder
  normalisiert das Request-Ziel nicht.

## Security-Auswirkung

Diese Arbeit betrifft Supply-Chain-Pinning, Archive-Ownership, externe
Build-Output-Grenzen und Provenance von nicht vertrauenswürdigen HTTP-
Endpoints. Die Korrekturen bewahren Fail-Closed-Verhalten bei fehlenden oder
fehlerhaften Endpoints und verhindern, dass request-kontrollierte Host-
Metadaten zu einem lokalen UDS-/Engine-Endpoint werden. Die neue Apache-P2-
Fixture beschränkt serielle Audit-Parts bewusst auf `ABFZ`
und weist die Speicherung ihres festen synthetischen Request-Body-Markers
zurück. Sie ändert weder die produktive Audit-Konfiguration noch autorisiert
sie das Logging von Request-Bodys. Das fokussierte Review ergab keinen
validierten Sicherheitsbefund in diesen begrenzten Harness- und Availability-
Änderungen. Die Apache-Korrektur hält jeden nichtleeren Body innerhalb einer
endlichen Grenze und nutzt `reject` bei einem initialen Null-Limit oder einer
nicht unterstützten Aktion; sie erzeugt weder einen unbegrenzten Pfad noch
legt sie Teilinspektion offen, die einen uninspektierten Tail weiterreichen
könnte. Die konstruierte Lighttpd-Decision bleibt eine explizite Evidenzgrenze.
Die Envoy-Korrektur entfernt client-kontrollierte URI-Header aus dem
Policy-Input des Autorisierungsdienstes, statt sie lediglich neu zu priorisieren.
Die Vorlage blockiert dieselben Namen auch bei einer zukünftigen Änderung der
Header-Allow-List, und die Null-Anzahl des Profils bleibt unabhängig von der
Vorlagendurchsetzung sicher. Ihre Response-Fixture trägt nur statische Marker;
das Event-Modell bleibt payload-frei.
Die Korrekturen schließen weder
das separat verfolgte Same-UID-UDS-Pathname-Replacement-Risiko
(`FND-PARENT-0015`) noch weisen sie eine wirksame Regelprofilabdeckung für die
2026-`t:hexDecode`-Advisory-Bedingung nach.

## Geänderte Dateien

- `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`
- `ci/provisioning/components/prepare-runtime-components.py`
- `connectors/apache/build/apxs-wrapper.in`
- `connectors/apache/src/msc_filters.c`
- `connectors/apache/README.md`
- `connectors/apache/README.de.md`
- `connectors/envoy/src/envoy_ext_authz_service_main.c`
- `connectors/envoy/config/envoy-ext-authz-smoke.yaml.in`
- `connectors/envoy/harness/run_envoy_connector_runtime.sh`
- `connectors/envoy/harness/envoy_smoke_helper.py`
- `connectors/envoy/README.md`
- `connectors/envoy/README.de.md`
- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `connectors/lighttpd/tests/test_stock_sidecar_contract.py`
- `connectors/lighttpd/README.md`
- `connectors/lighttpd/README.de.md`
- `connectors/traefik/native_middleware/middleware.go`
- `connectors/traefik/native_middleware/engine_uds_test.go`
- `connectors/traefik/native_middleware/middleware_test.go`
- `connectors/traefik/native_middleware/README.md`
- `connectors/traefik/native_middleware/README.de.md`
- `docs/reference/variables.md`
- `docs/reference/variables.de.md`
- `common/rules/modsecurity_response_companion_smoke.conf`
- `tests/test_prepare_runtime_components.py`
- `tests/test_apache_request_transaction_cleanup.py`
- `tests/test_apache_apxs_profile_registry_staging.py`
- `tests/test_envoy_transport_hardening_contract.py`
- `reports/audits/change-records/CR-20260919-readiness-b-shared-remediation.md`
- `reports/audits/change-records/CR-20260919-readiness-b-shared-remediation.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Tests und tatsächliche lokale Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| `tests.test_prepare_runtime_components` | Bestanden: 90 Tests; fünf Framework-HEAD-Mismatch-Fälle wurden übersprungen. |
| `tests.test_apache_request_transaction_cleanup` | Bestanden. |
| `tests.test_apache_apxs_profile_registry_staging` | Bestanden: 5 Fälle. |
| `tests.test_apache_request_transaction_cleanup` und `tests.test_apache_apxs_profile_registry_staging` nach dem P2-Bootstrap-Harness-Update | Bestanden: 24 Fälle, einschließlich eines statischen P2-/Audit-/No-Raw-Marker-/Follow-up-Harness-Contracts. |
| `tests.test_apache_request_transaction_cleanup` nach dem P2-Policy-Fallback und Over-Limit-Control | Bestanden: 21 Fälle, einschließlich finiter Default-/Reject-Source-Wiring- und Marker-/Over-Limit-/Follow-up-Harness-Reihenfolge. |
| `sh -n ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh` | Bestanden. |
| `ci/checks/connectors/apache/check-apache-common-adoption.py` und `tests.test_apache_common_adoption` | Bestanden: Apache-P2-Struktur-/Adoption-Checks und 12 fokussierte Python-Fälle. |
| `make check-common-helpers-c17` | Bestanden mit dem Common-Body-Policy-Helper-Smoke in einem task-eigenen externen Build-Root. |
| `make check-apache-c17` mit `CC=cc` und `CC=clang` | Zweimal bestanden mit expliziter `-std=c17 -Wall -Wextra -Werror`-Kompilierung in getrennten task-eigenen externen Output-Roots. |
| Finaler Apache-Autotools-Host-Lauf nach Hardening mit den gecachten nicht privilegierten Apache-/libModSecurity-Inputs | Lokal bestanden: Modul-Laden, Allow-/Block-Verhalten und die dokumentierten Transaction-ID-Controls wurden abgeschlossen. Dies ist begrenzte lokale Host-Evidenz, keine Evidenz für jeden Connector- oder Protokollpfad. |
| Aktueller Apache-P2-Bootstrap-Host-Control | Vor `httpd`-Start blockiert: `chown` der task-eigenen nicht privilegierten Runtime-Verzeichnisse/-Dateien lieferte auf dem aktuellen idgemappten Dateisystem `EINVAL`. Es wurde kein Root-Worker-Ersatz verwendet. |
| HAProxy-SPOP-zu-HTX-Combined-bounded-Host-Lauf | Lokal als nicht privilegierter isolierter Pfad mit dem source-gebauten aktuellen SPOP-Adapter und HAProxy HTX bestanden. Dies ist begrenzte Evidenz für diesen Combined-Pfad, keine Standalone-HTX-Evidenz und keine vollständige B-Klassen-G2–G6-/54-Fälle-Evidenz. |
| `connectors/lighttpd/tests/test_stock_sidecar_contract.py` mit `CC=clang` | Bestanden: 18 Tests. |
| `connectors/lighttpd/tests/test_stock_sidecar_contract.py` mit `CC=cc` | Bestanden: 18 Tests. |
| `connectors.lighttpd.tests.test_stock_sidecar_contract.StockSidecarSourceContractTest` nach dem deterministischen P2-Delivery-Failure-Ersatz | Bestanden: 19 Tests. Er verankert statisch den P2-Zweig nach `finish_request_body` und führt den Terminal-Handoff mit einer konstruierten Decision aus; dies ist kein dynamischer P2- oder Stock-Host-Runtime-Nachweis. |
| Aktueller Stock-Sidecar-`c:S1820`-Refaktor | Der C17-Build und 20 `StockSidecarSourceContractTest`-Fälle bestanden mit `cc`; der C17-Build bestand mit `clang`. Die vollständige lokale 35-Fälle-Suite hatte 34 bestandene Fälle und einen `runtime_identity`-Fehler (`runtime-begin-smoke` beendete sich ohne stderr mit 1). Dieses Binary wird ohne `stock_sidecar.c` gebaut, daher ist dies ein separater Fehler und kein als bestanden gewerteter Nachweis für diesen Refaktor. |
| `python3 -m py_compile ci/provisioning/components/prepare-runtime-components.py` | Nach den zwei minimalen `python:S1172`-Signaturentfernungen bestanden. |
| Aktuelle SonarQubeCloud-PR-#370-Issue-Prüfung | Vor diesem Inkrement meldete der Dienst drei task-eigene offene Issues: ein `c:S1820` und zwei `python:S1172`. Die lokalen Korrekturen sind oben abgedeckt; null offene Issues bleibt ein unverifiziertes Delivery-Gate, bis die Analyse des aktuellen PR-Heads abgeschlossen ist. |
| Natives Traefik-Go-Modul `go test -mod=readonly ./...` | Bestanden. |
| Natives Traefik `go vet ./...` und `gofmt -d`-Review | Bestanden; `gofmt -d` erzeugte keinen Diff. |
| Natives Traefik `FuzzUDSFrameAndResult` für 15 Sekunden | Bestanden. |
| `tests.test_envoy_transport_hardening_contract` | Bestanden: 28 Tests, einschließlich der Regression-Contracts für Response-Default, P3/P4-Fixture, URI-Header und unsicheren Runtime-Root. |
| `make check-remaining-connectors-c17` mit `CC=cc` und `CC=clang` | Zweimal bestanden; der geänderte Envoy-C-Profilcode wurde unter C17 mit Warnings als Fehlern kompiliert. |
| Envoy-Connector-Build und Response-Companion-Regel-Konfigurationscheck | Gegen den gecachten libModSecurity-Prefix in einem task-eigenen externen Build-Root bestanden; libModSecurity akzeptierte die verkettete P3-Regel. |
| `git diff --check` während der scoped Implementierung | Bestanden. |
| `make check-variable-documentation` | Bestanden: 100 dokumentierte Variablenreferenzen gescannt. |
| `make check-bilingual-docs` und `make check-doc-links` | Ausschließlich durch den nicht materialisierten Framework-Gitlink blockiert; jedes ausgegebene Ziel liegt unter `modules/ModSecurity-test-Framework`. |

## Ausgeführte Befehle

Alle Befehle wurden über den Repository-RTK-Proxy ausgeführt. Die beobachtete
lokale Validierung umfasste die fokussierten Python-Auswahlen
`tests.test_prepare_runtime_components`,
`tests.test_apache_request_transaction_cleanup` und
`tests.test_apache_apxs_profile_registry_staging`; den Apache-Autotools-
Bootstrap-Check; `connectors/lighttpd/tests/test_stock_sidecar_contract.py`
mit `CC=clang` und `CC=cc`; sowie die nativen Traefik-Befehle
`go test -mod=readonly ./...`, `go vet ./...`, `gofmt -d` und den
15-sekündigen `FuzzUDSFrameAndResult`-Lauf. Der ausgeführte HAProxy-Host-
Control war `connectors/haproxy/harness/combined_spop_htx/run_combined_spop_htx.sh`
mit einem isolierten nicht privilegierten Runtime-Root und dem aktuellen
Combined-SPOP-zu-HTX-Pfad. `git diff --check` und
`make check-variable-documentation` bestanden während der scoped Arbeit. Die
repositoryweiten Bilingual-/Link-Targets wurden ausgeführt, sind aber
ausschließlich durch den separat besessenen, nicht materialisierten Framework-
Gitlink blockiert. Die obige Tabelle hält die tatsächlich beobachteten
Ergebnisse fest; kein unbeobachteter Hosted- oder Produktionsbefehl wird als
ausgeführt dargestellt.

Die Follow-up-Validierung führte `sh -n
ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`, `python3 -m
unittest -v tests.test_apache_request_transaction_cleanup
tests.test_apache_apxs_profile_registry_staging` und `python3 -m unittest -v
connectors.lighttpd.tests.test_stock_sidecar_contract.StockSidecarSourceContractTest`
aus. Der versuchte begrenzte nicht privilegierte Apache-P2-Bootstrap erreichte
die Konfigurationssyntax, stoppte jedoch vor dem Serverstart, als der Ownership-
Handoff des task-eigenen Runtime-Roots `EINVAL` lieferte; er wird als blockiert
und nicht als bestanden dokumentiert.

Nach dem gehosteten Apache-Fehler auf
`466a776347e35405e9875190ae9912a827e56f6a` lief die lokale Follow-up-
Validierung mit `python3 -m unittest -v
tests.test_apache_request_transaction_cleanup`, `sh -n
ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`,
`ci/checks/connectors/apache/check-apache-common-adoption.py`, `python3 -m
unittest -v tests.test_apache_common_adoption`, `make
check-common-helpers-c17` sowie `make check-apache-c17` mit `CC=cc` und
`CC=clang`. Die C-Outputs und Common-Helper-Outputs wurden in den registrierten
task-eigenen externen Run-Root geleitet. Alle aufgeführten lokalen Checks
bestanden; keiner ersetzt den ausstehenden korrigierten Exact-Head-Host-Lauf.

Der gehostete Apache-Bootstrap auf exaktem Head
`56b838ce1fe681e47c8fd3df326dccab8a1c4405` erreichte die Over-Limit-P2-
Assertion, las mit seinem Parser der ersten Header-Zeile jedoch `100 Continue`.
Ein großer HTTP/1.1-Upload kann diese Zwischenantwort vor seinem finalen Status
erhalten; daher weist die Harness-Beobachtung weder ein finales `413` noch
einen neuen Source-Policy-Fehler nach. Die Korrektur behält Header- und
Response-Artefakte, erfasst aber curls finales `%{http_code}`; ihr Exact-Head-
Hosted-Nachfolger auf `18303495bc9bdb64cef74aae0f39e40d29ca5492` bestand Lauf
`35445064987`, einschließlich finalem `413`, fehlendem Handler-Inhalt und
Same-Process-Allow-Follow-up.

Der Envoy-Follow-up führte das vollständige Modul
`tests.test_envoy_transport_hardening_contract`, Shell-Syntaxchecks,
C17-Sourcechecks mit `cc` und `clang`, einen vollständigen Connector-Build
gegen den gecachten libModSecurity-Prefix und einen `ext_authz`-
Konfigurationsload mit
`common/rules/modsecurity_response_companion_smoke.conf` aus. Der erste
Regelload zeigte eine fehlende explizite Aktionsliste der zweiten verketteten
Regel; nach Ergänzung von `t:none` bestand derselbe echte libModSecurity-Load.
Es war keine Envoy-Binärdatei vorhanden, deshalb wurden weder Listener noch
generiertes YAML, Downstream-URI, Spoofing oder P3/P4-Host-Assertion gestartet.

## Runtime-Evidence

Der finale Apache-Bootstrap- und der HAProxy-SPOP-zu-HTX-Combined-Lauf sind
tatsächliche lokale nicht privilegierte Host-Evidenz innerhalb ihrer begrenzten
Fixtures. Der HAProxy-Lauf startet Standalone-HTX nicht erneut und deckt weder
die vollständigen B-Klassen-G2–G6 noch die 54-Fälle-Matrix ab. Die Lighttpd-
und Traefik-Ergebnisse sind Source-, Contract- und Go-Modul-Evidenz; sie
ersetzen keinen unabhängig gestarteten Produktivhost mit den erforderlichen
Regeln, Lifecycle-Controls, Logs, Metriken, Restart-, HTTP/1.1-, HTTP/2- und
HTTP/3-Evidenz. Es wird nicht behauptet, dass nun alle zehn Integrationspfade
B-Klassen-Runtime-Evidenz besitzen.

Der gehostete Apache-Bootstrap auf exaktem Head
`466a776347e35405e9875190ae9912a827e56f6a` baute das aktuelle Modul,
absolvierte Konfigurations-/Modul-Ladechecks und reproduzierte dann den kleinen
P2-Marker als `413` statt `403`. Das ist echte negative Host-Evidenz für den
Pre-Correction-Source und identifiziert die erste Terminalbedingung; es ist
kein bestandener Apache-Runtime-Claim. Der lokale P2-Host-Versuch bleibt vor
dem Start durch `chown(...)=EINVAL` blockiert; der nachfolgende Hosted-Lauf auf
exaktem Head bestand den begrenzten Control. Der Lighttpd-Harness führt ebenso
nicht dynamisch `finish_request_body` aus und weist nicht den vollständigen
P2-Pfad nach.

Der folgende gehostete Bootstrap auf
`56b838ce1fe681e47c8fd3df326dccab8a1c4405` führte den Over-Limit-Request aus,
beendete seine Assertion aber beim Zwischen-`100 Continue` statt beim finalen
Response. Dies ist ein Harness-Parsing-Fehler, keine Evidenz für ein finales
`413` und keine Widerlegung der finiten/reject-Source-Korrektur. Der nächste
Nachfolger auf exaktem Head `18303495bc9bdb64cef74aae0f39e40d29ca5492`
bestand Hosted-Lauf `35445064987`, einschließlich finalem `413`, fehlendem
Handler-Inhalt und Same-Process-Follow-up. Dies bleibt begrenzte Apache-P2-
Evidenz, keine Zehn-Pfad- oder vollständige Apache-B-Hochstufung.

Die Envoy-Korrektur besitzt keine echte Envoy-Host-Evidenz. Sie validiert die
Response-Companion-Regeldatei und den Source-/Harness-Vertrag, beweist aber
weder generiertes YAML noch die geschützte URI einschließlich Query/
Percent-Encoding, URI-Hint-Spoofing-Resistenz durch Envoy,
Response-Companion-Korrelation oder P3/P4-Host-Aktionen.

## Nicht ausgeführte Prüfungen mit Begründung

- Eine vollständige Evidenzmatrix für zehn Pfade, einschließlich aller
  erforderlichen Protokoll- und Lifecycle-Dimensionen, ist bei diesem Record-
  Snapshot nicht abgeschlossen.
- Wirksames externes Regelprofil-Testing für die `t:hexDecode`-Advisory-
  Bedingung ist nicht gelaufen; Checked-in-Source-Inspektion kann die
  verwendeten Regeln eines Deployments nicht beweisen.
- Vollständige Host-Evidenz für NGINX, beide Envoy-Pfade, Standalone-HAProxy-
  HTX, Traefik-forwardAuth, Stock-Lighttpd und gepatchtes Lighttpd wird hier
  nicht behauptet. Der Combined-HAProxy-SPOP-zu-HTX-Lauf bleibt unterhalb
  vollständiger B-Klassen-G2–G6- und 54-Fälle-Evidenz.
- Der korrigierte Exact-Head-Hosted-Apache-Control bestand, doch der aktuelle
  Envoy-Source-Head hat keinen Hosted- oder Real-Host-Lauf: Die angeheftete
  Envoy-Binärdatei und attestierte Host-Inputs sind nicht verfügbar. URI-
  Query-/Encoding- und Spoofing-Fälle bleiben daher erforderliche
  Host-Controls. Aktuelle CI, SonarQube Cloud, Review, Mergeability und finale
  PR-Ergebnisse dürfen nicht aus lokalen Checks abgeleitet werden. Die
  Voraussetzungen der repositoryweiten Bilingual-/Link-Targets sind ebenso
  durch den separat besessenen nicht materialisierten Framework-Gitlink
  blockiert.
- Die aktuelle lokale Stock-Sidecar-Suite ist nicht vollständig grün: 34 von
  35 Fällen bestanden, während
  `test_runtime_identity_smoke_accepts_the_canonical_profile` bei
  `runtime-begin-smoke` Exit 1 ohne stderr beobachtete. Dieses unabhängig
  gebaute Binary kompiliert nicht `stock_sidecar.c`; der Fehler gilt nicht als
  Validierung des `c:S1820`-Refaktors und bleibt ein separater Diagnosepunkt.
- Der aktuelle Apache-P2-Bootstrap-Host-Control lief nicht vollständig, weil
  der notwendige `www-data`-Ownership-Handoff des Task-Roots auf dem aktuellen
  idgemappten Dateisystem mit `EINVAL` fehlschlägt. Ein Root-Worker-Ersatz ist
  verboten.

## Bekannte Einschränkungen

Das angeforderte Ergebnis — nachgewiesene B-Reife für alle zehn
Integrationspfade — ist bei diesem Snapshot nicht erreicht. Die Korrekturen
beheben nur die aufgeführten gemeinsamen Lücken. FND-PARENT-0015 bleibt offen,
Host-/Runtime-Voraussetzungen sind für mehrere Pfade blockiert oder nicht
verifiziert, und das wirksame Regelprofil zur Bewertung der `t:hexDecode`-
Bedingung wurde nicht bereitgestellt.

## Verbleibende Risiken

Die korrigierte Endpoint-Behandlung kann nicht selbst beweisen, dass jeder
Embedding-Host eine vertrauenswürdige lokale Adresse liefert. Die Local-
Address-Validierung schlägt daher fail-closed fehl. Archive- und APXS-
Korrekturen ersetzen keinen frischen Host-Build für jede unterstützte
Deployment-Konfiguration. Für die Advisory-Bedingung wird ohne das tatsächlich
aktivierte Regelprofil weder ein verwundbarer noch ein betroffener Status
behauptet.

## Finaler Diff- und Review-Status

Dies ist ein partieller Parent-only-Remediation-Record. Er beschreibt
beobachtete lokale Evidenz, einen gehosteten Pre-Correction-Fehler und bekannte
Grenzen, zertifiziert aber weder das Zehn-Pfad-B-Ziel noch ein Release, ein
Hosted-Qualitätsergebnis oder einen Merge. Finaler Scoped-Diff und source-
lokale Dokumentationschecks wurden abgeglichen; der Envoy-Source-/Harness-
Repair benötigt weiterhin Real-Host-Evidenz. Repositoryweite
Dokumentations-Targets bleiben wahrheitsgemäß durch den fehlenden Framework-
Gitlink blockiert. Der offene Draft-PR ist
[#370](https://github.com/Easton97-Jens/ModSecurity-conector/pull/370). Die
verbleibende Runtime-Evidenz bleibt Follow-up-Pflicht.

## Nachweis der C-Follow-up-Regression — 2026-09-19

Dieses Parent-only- und test-only-Follow-up macht den fokussierten C-
Companion-Test wahrheitsgemäß und schützt unmittelbar den gepufferten
`traefik-forwardauth`-Lebenszyklus. Es ändert weder Common-Runtime-Verhalten,
eine Traefik-Konfiguration, eine Host-Binärdatei noch eine Reifeeinstufung.

- Das Test-Fixture erstellt sein privates Event-Verzeichnis nun aus einem
  absoluten Arbeitsverzeichnis-Pfad. Die Test-Binärdatei läuft aus ihrem
  registrierten externen Build-Child; damit bleibt die beabsichtigte Ablehnung
  relativer/no-follow-Parent-Komponenten durch den Produkt-Event-Sink erhalten.
- Ein begrenztes rohes ungültiges Client-Adressbyte (`0x80`) wird korrekt als
  `\u0080` JSON-escaped, als ein Event ohne rohes ungültiges Byte geschrieben
  und von einer Transaktion gefolgt, deren `previous_event_hash` dem ersten
  Event-Hash entspricht. Eine 63-Byte-Adresse mit Escape-Expansion schlägt
  stattdessen mit `MSCONNECTOR_ERROR_EVENT_TOO_LARGE` vor einem Write oder
  Hash-Chain-Advance fehl; ein nachfolgendes gewöhnliches Event beginnt mit
  `previous_event_hash` null.
- Das exakte `traefik-forwardauth`-Profil im `forwardAuth`-`buffered`-Modus
  besitzt nun direkte C-Abdeckung für explizit leere und begrenzt nicht
  leere Bodies. Der Test prüft abgeschlossene P2-Metadaten/-Zähler, `P1|P2`,
  keine Kürzung, die Ablehnung einer zweiten P2-Finalisierung, opake
  Response-Companion-Übergabe und P3/P4-Abschluss. Ein nicht leerer
  Null-Body-Pointer wird fail-closed abgelehnt.

Strikte C17-Full-Test-Builds und -Ausführungen bestanden mit `cc` und `clang`,
mit `-Wall -Wextra -Werror`, task-owned externem Output und 120-Sekunden-
Limits. `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
tests.test_traefik_forwardauth_p2_contract` bestand 7/7; `make
check-common-security-contract` und `git diff --check` bestanden. Unabhängige
Security- und Test-Reviews fanden keinen plausiblen Befund in diesem Testdiff.

Dies ist ausschließlich Common-Runtime-Regressions-Evidenz: Der Test umgeht
absichtlich Traefik-HTTP-Parsing und beweist daher weder `Content-Length`-
Verhalten noch ein tatsächliches Traefik-Host-Ergebnis oder B-Klassen-Reife.

## Korrektur der NGINX-Native-Receipt-Identität — 2026-09-19

Der Exact-Head-NGINX-Workflow, der Archiv-Digest und die gemeinsame
Fixture-Quellwurzel binden NGINX `1.31.5`, doch sowohl der separat erzeugte
native Response-Body-Buffer- als auch der P3-Header-Receipt deklarierten
fälschlich `1.31.4`. Dies war ein Evidenz-Identitätsfehler: Er änderte weder
die gebaute Binärdatei noch Connector-Verhalten, Request-Verarbeitung oder die
vorhandenen begrenzten Fixture-Ergebnisse, verhinderte aber die Verwendung
dieser Receipts als präzise G1-Identitätsnachweise.

Das gemeinsame Fixture besitzt nun genau ein `EXPECTED_NGINX_VERSION =
"1.31.5"`, leitet seine erwartete Quellwurzel daraus ab und beide
Receipt-Writer schreiben dieselbe Konstante. Neue fokussierte Assertions
schlugen zunächst fehl, weil die Versionsidentität fehlte oder veraltet war;
nach der Korrektur bestand der Body-Buffer-Fixture-Vertrag 8/8 und der
P3-Header-Fixture-Vertrag 4/4. Die betroffene NGINX-Contract-Suite bestand 48
Tests, mit drei erwarteten Skips ausschließlich durch den separaten
Framework-Gitlink-HEAD-Mismatch; `git diff --check` bestand.

Die Korrektur besitzt noch keinen frischen Hosted-Receipt, schließt NGINX
G2--G9 nicht und stuft NGINX nicht auf B hoch. Bestehende Non-root-Worker-,
No-follow-Pfad-, Body-Boundary-, Fail-closed-Error- und Cleanup-Controls
bleiben unverändert.
