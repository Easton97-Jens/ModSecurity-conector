# NGINX-Connector

**Sprache:** [English](README.md) | Deutsch


Status: Adaptereigene Quellmigration

Dieses Verzeichnis enthält den NGINX-Proof-of-Concept-Harness, den adaptereigenen NGINX
Connector-Quelle und Upstream-Attributionsdateien für ModSecurity-nginx
Connector. Es wird immer noch durch Smoke-Test aus der realen Welt und nicht durch eine Produktion bestätigt
Unterhaltsanspruch.

Jetzt implementiert:

- Dokumentation der beobachteten lokalen NGINX-Connector-Konzepte.
- Adaptereigene Quelle unter `src/`, plus `config` auf Root-Ebene und Metadaten,
  abgeleitet vom ModSecurity-nginx-Basis-Commit
  `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`.
- Gemeinsam genutzte Direktivennamen-Metadaten von `common/include/msconnector/directives.h`.
- Gemeinsame Options-/Standardmetadaten für die Aktivierung, Fehlerprotokollweiterleitung usw
  Phase-4-Modus von `common/include/msconnector/options.h`.
- `modsecurity_use_error_log off` unterdrückt auch native libModSecurity-
  Callback-Meldungen im NGINX-Fehlerlog; WAF-Auswertung und Event-JSONL-Ausgabe
  bleiben getrennte Funktionen.
- Ausgewählte Quelländerungen von ModSecurity-nginx PR #377
  (https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377) angewendet auf
  Adaptereigene Quelle für die Handhabung von Phase 4/späten Interventionen.
- Ein connector-spezifischer Laufzeitkabelbaum unter `harness/`.
- Gemeinsamer YAML-Fallverbrauch über `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.
- Von der Quelle abgeleitete, gemeinsam genutzte, importierte Fälle für den Roh-JSON-Körperabgleich, einfach
  mehrteiliger Textfeldabgleich und Antworttext-Passthrough.

Nicht implementiert:

- Keine umfassende Umschreibung des NGINX-Moduls über die kontrollierte, adaptereigene Migration hinaus.
- Keine vollständige NGINX-Regressionssuite.
- Es wird keine breite Runtime-Promotion behauptet. Ein ausgewählter nativer
  H1-Phase-4-Out-of-Scope-Fall ohne CRS und ohne MRTS bestand in der
  fokussierten Task-Evidence; dieses Ergebnis belegt weder den kanonischen
  Lifecycle noch eine vollständige Matrix oder Transport-Coverage.
- Es wird kein Anspruch auf eine vollständige Response-Body-Promotion erhoben. Phase 4 / RESPONSE_BODY bleibt bestehen
  nicht gefördert; Die Strict-Mode-Verkabelung auf Quellenebene ist keine kanonische Laufzeit
  Beweise.
- Dieses Source-/Provenance-Update behauptet kein HTTP/2-, HTTP/3-, Remote-
  Rule-, Helgrind- oder kanonisches Memcheck-Ergebnis. Das erhaltene direkte
  H1-Memcheck-Artifact nach der Suppression ist Pre-Hardening-, nicht
  kanonische historische Evidence und kein finaler Nachweis für den aktuellen
  Connector oder Harness.

## Selektive Upstream-Sicherheitsaufnahme

Der adapter-eigene Source behält die Upstream-Basis
`9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` und das frühere lokale
Phase-4-Overlay aus PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac`.
Die aktuelle selektive Aufnahme ist pro Datei in [der Ursprungsübersicht](ORIGIN.de.md)
und in [`SOURCE_MAP.json`](SOURCE_MAP.json) aufgezeichnet:

- [PR #384](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/384)
  bei `65de4cd8739209f22d924d85548bd012a4d94607` unterscheidet finales
  Body-Processing von partieller Aufnahme. Fehler bei finalem
  `msc_process_request_body()`/`msc_process_response_body()` sind fail-closed,
  während `msc_append_request_body()`, `msc_request_body_from_file()` und
  `msc_append_response_body()` nicht fatales `ProcessPartial` beibehalten,
  weil dieses Rückgabesignal eine Engine-seitige Limitbehandlung bezeichnen
  kann. Diese Kompatibilität ist vom Connector-eigenen Phase-4-Body-Budget
  getrennt: Ein über dem Limit liegender aktueller Buffer wird abgewiesen,
  bevor er downstream weitergereicht werden kann.
- [PR #385](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/385)
  bei `471a2a54843bb8f560758a7e75b146db2243ab29` liefert ausgewählte
  Response-Header- und Pre-Commit-Redirect-Replacement-Behandlung. Eine
  task-lokale Erweiterung erfordert connector-eigene `Location`-Provenance,
  bevor sie Phase-3-Output als Response-Replacement behandelt, weist Redirect-
  URL-CR/LF vor der Installation zurück und unterdrückt fiktive synthetische
  `Connection`-/`Keep-Alive`-Felder bei nativem HTTP/3 ebenso wie bei HTTP/2;
  diese Source-Level-Änderungen sind kein HTTP/2- oder HTTP/3-Runtime-Nachweis.
- [PR #386](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/386)
  bei `a7fd4fcc18dc442b1b093d253f457b9317b7f588` liefert ausgewählte wertfreie
  Header-Registration-Warnings, Empty-Address-Guards und terminales
  Body-Filter-Forwarding.
- [PR #387](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/387)
  bei `4c1f0362ca0f25ef216ce59cad5fa6c9703c1438` prägt den Parent-eigenen
  opt-in bounded native soak (`make soak-nginx`) und die H1-Memcheck-Diagnose
  (`make memcheck-nginx`) über den vorhandenen Harness. Beide bleiben außerhalb
  von Default-Smoke/Test/CI und schreiben begrenzte payload-freie Summaries.
  Der source-gesteuerte Soak-Selektor lässt zwischen einer und acht eindeutige
  IDs aus seinem expliziten kanonischen Katalog zu und weist leere,
  doppelte oder außerhalb des Katalogs liegende Selektionen vor der
  Case-Discovery ab. Upstream-Dockerfiles,
  Workflows, Valgrind-/Helgrind-Konfiguration und Tooling werden
  nicht importiert. Das erhaltene direkte H1-Artifact nach der Suppression
  unten ist Pre-Hardening und nicht kanonisch; es wird kein kanonisches
  Memcheck-, Helgrind- oder Soak-Ergebnis behauptet.

Die Aufnahme ändert nicht das dokumentierte Phase-4-Result-Modell: Ein Safe
Late Result ist `log_only` mit unverändertem sichtbarem Status, während ein
Strict Late Result nach Commit `abort_connection` statt einer erfundenen
zweiten Response ist.

Sie stellt außerdem eine vor der Task bestehende Parent-Regression bei der
Content-Type-Aufnahme wieder her. Begrenzte Response-Bytes erreichen
ModSecurity jetzt unabhängig vom konfigurierten Connector-Content-Type-Scope;
erkennt diese Inspection eine außerhalb des Scopes liegende Intervention, mappt
der Connector sie zu `log_only` mit `content_type_not_in_scope`. Das lockert
#384 nicht: Finales `msc_process_response_body()`-Processing bleibt bei einem
Ergebnis ungleich `1` fail-closed, während Append-/From-File-
`ProcessPartial`-Handling für akzeptierte Engine-Chunks absichtlich nicht fatal
bleibt. Das Connector-`modsecurity_phase4_body_limit` verwendet vor dem
Forwarding jedes im Scope liegenden Memory- oder File-Buffers den Common-
Reject-Plan; ein über dem Limit liegender Buffer kann daher keinen
uninspektierten Tail freigeben.

Der strikte isolierte Rebuild sowie C17, C23 und c2y bestanden, und die neu
materialisierte Build-Source-SHA entsprach dem Task-Filter. Der ausgewählte
native H1-Out-of-Scope-Fall ohne CRS und ohne MRTS bestand. Die ausgewählten
Parent-Safe-/Strict-Ergebnisse wurden als `log_only` bei unverändertem
sichtbarem Status beziehungsweise `abort_connection` nach Commit beobachtet,
aber der vollständige ausgewählte Runner endet wegen read-only-Framework-
Fixture-Widersprüchen nichtnull (`FND-FRAMEWORK-0058`,
`blocked`/`out_of_scope`): Safe erwartet den Modus als Reason, während Strict
zugleich einen stabilen `403`/eine obsolete Action trotz Connection-Abort
erwartet. Es wird keine Framework-Änderung behauptet. Diese fokussierten
Beobachtungen belegen weder H2/H3, Remote-Rule, Soak, einen cleanen kanonischen
Memcheck noch Delivery.

### Parent-Response- und Harness-Härtung

Die aktuelle Parent-only-Phase-3-Härtung behandelt eine Response nur dann als
ersetzt, wenn `intervention_redirect_location_installed` festhält, dass der
Connector-Redirect-Helper sein eigenes `Location` installiert hat. Ein bereits
vorhandenes Upstream-`Location` bei einer Status-only-Intervention reicht nicht
aus und verwendet stattdessen die NGINX-Finalisierung. Eine Redirect-URL mit
CR oder LF schlägt mit `NGX_HTTP_BAD_REQUEST` fail-closed fehl, bevor ein
Buffer alloziert oder `Location` installiert wird.

Der direkte Harness erfordert eine Root-Ausführung und schlägt fail-closed
fehl, sofern root `NGINX_WORKER_USER` nicht als separates lokales Konto lösen
und verifizieren sowie dessen Gruppe auflösen kann. Er rendert
`user <resolved-user> <resolved-group>;` explizit in der generierten
NGINX-Konfiguration. Er trennt root-eigenes privates Runtime-Material,
Harness-Logs einschließlich `NGINX_PHASE4_LOG_FILE` und
`NGINX_MEMCHECK_EVIDENCE_DIR` von den einzigen worker-eigenen Pfaden:
`NGINX_WORKER_STATE_ROOT` sowie den Access-/Error-/Audit-Leaves von
`NGINX_SERVER_LOG_ROOT`. Überlappende Pfade oder Worker-Sichtbarkeit privater
Ausgabe blockieren den Harness. `NGINX_MEMCHECK_EVIDENCE_DIR` liegt privat
unter `LOG_DIR/memcheck-evidence/<case>`; nur die getrennten `worker-state`-
und `server-logs`-Bäume liegen unter dem Worker-traversierbaren Harness-Root.
Die unten beschriebene Opt-in-Docroot-Projektion ist eine getrennte root-eigene
statische Grenze, kein weiterer worker-eigener Harness-Output.

Der Memcheck-Summarizer behandelt Evidence nur als vertrauenswürdig, wenn ihr
Root und Parent effektive-UID-eigene echte Verzeichnisse sind, die nicht für
Gruppe oder Andere beschreibbar sind, jeder Metadata-/Log-/Output-Pfad ein
direktes Kind ist und jede Eingabe eine private Regular-Datei mit einem Link
ist, die mit No-Follow-Schutz geöffnet und beim Lesen auf Ersetzung geprüft
wird. Unsichere Evidence wird abgelehnt oder als unvollständig markiert,
anstatt zu einem cleanen Ergebnis promotet zu werden.

Der erhaltene Beleg
`$RUN/evidence/direct-nginx-h1-memcheck-evidence-remediation-20260801.md`
(SHA-256
`37f01fe3d1851d43ae21d2b705b02bf01f204ff5cb19b41354e5b801a4b158a8`)
zeichnet `passed_noncanonical_diagnostic` für einen begrenzten dreisekündigen
`allow_without_marker`-No-CRS-H1-Fall unter bewusster `umask 022` auf. Der
Root-Lauf verwendete den separaten verifizierten Worker `nobody`, hielt den
privaten Output-Root im Modus `0700` und Worker-State-/Server-Log-Leaves im
Modus `0700` und Eigentum von `nobody:nogroup`; der Summarizer akzeptierte zwei
private Valgrind-Eingaben und schrieb seine Role-, Lifecycle-, JSON- und Text-
Outputs im Modus `0600`. Seine 28 Requests hatten keine Request- oder Worker-
Summary-Fehler, und die cleane vollständige Summary hatte null Fehler sowie
null definitiv oder indirekt verlorene Bytes.

Dies ist direkte Runtime-Evidence für die remediierte Harness-/Evidence-Grenze,
nicht für das aktuelle C-Redirect-Verhalten: Der Beleg nutzt das erhaltene
SHA-verifizierte NGINX-`1.31.2`-`pre-current-C`-Diagnose-Artifact. Ein
separater frischer C-Source-Build validierte den vorherigen C-Code, aber dieser
Beleg führt diesen Code nicht aus. Der exakte finale Security-Scan und finale
PR-Head-CI/Sonar-Evidence bleiben ausstehend.

### Parent-NGINX-Harness-Output-Path-Authority

`FND-PARENT-0084` ist `validated`; seine Parent-Task-Remediation ist
`in_progress`. Vor jedem root-Harness-`mkdir`, Installieren, `chown`, `chmod`,
`rm` oder jeder Output-Redirection müssen alle generischen/privaten Bootstrap-,
Parent-Multi-Case- und Work-/Output-Roots pro Case als strikte Nachkommen von
`VERIFIED_RUN_ROOT` validieren. Dasselbe Authority-Gate beschränkt
konfigurierbare Diagnostic-, Worker-Preflight-, Protocol-Artifact-, Lifecycle-
Evidence- sowie Curl-Response-/Error-Output-Pfade. `/dev/null` ist nur als
interner Bounded-Soak-Sink des Harness erlaubt.

Die einzige bewusst enge Ausnahme ist Opt-in `NGINX_DOCROOT_PROJECTION=1`.
Sein `NGINX_DOCROOT_PROJECTION_PARENT` ist ein expliziter externer Parent, den
ein vertrauenswürdiger Lifecycle-/Operator-Caller außerhalb der privaten
Runtime-Roots übergibt: Er muss bereits existieren, root-eigen, symlink-frei,
für Gruppe oder Andere weder beschreibbar noch lesbar und in einer
`0711`-sicheren Form für den Worker traversierbar sein; auch seine Ancestors
müssen traversierbar sein. Der Harness validiert diese strukturellen
Eigenschaften, schlägt aber kein Lifecycle-Manifest für die beiden
Projection-Werte nach und erzwingt keine Manifest-Registrierung.
`NGINX_DOCROOT_PROJECTION_ROOT` muss das exakte frische direkte statische Kind
sein. Der Projection-Helper validiert den Parent und erzeugt nur dieses Kind,
kopiert die allowlisteten statischen Dateien und macht das Kind für den Worker
traversierbar; das generische Harness-Ownership-/Mode-Setup führt auf dem
externen Parent niemals `chown` oder `chmod` aus. Kein generischer Harness-
Output ist dort autorisiert.

Der erhaltene Beleg
`$RUN/evidence/nginx-harness-path-authority-remediation-20260801.md`
(SHA-256
`e1b09454d3dc823b78d83bdae960d431951b432cad57aa05df4434a8bd905c7b`)
zeichnet einen realen Parent-Multi-Case-(`RUN_ONE_CASE=0`)-Negativtest mit
`LOG_DIR=/etc` auf: Der Harness endete vor der normalen Runtime-Assertion mit
`77`, und `/etc` blieb im Modus `0755`, Eigentümer/Gruppe `0:0`, ohne erzeugten
System-Output, NGINX-Prozess oder Listener.

Dieser Beleg beweist nur Output-Path-Authority. Das konfigurierbare `PYTHON`-
und `PATH`-Launch-Modell bleibt eine vertrauenswürdige Operator-/CI-Annahme
außerhalb dieses Findings. Die kanonische Runtime bleibt blockiert, und der
frische C-Build validiert vorherigen C-Code statt dieses Shell-Harness-
Controls; der erhaltene Generic-Path-Beleg promoviert die neue Projection-
Ausnahme nicht zu kanonischer Runtime-Evidence. Beides ersetzt weder den
finalen Security-Scan noch PR-Head-Evidence.

### Erhaltene Pre-Hardening-H1-Memcheck-Diagnose

Der initiale direkte H1-Valgrind-Lauf beobachtete eine 8-Byte-
`definitely-lost`-Allocation auf dem NGINX-Core-Worker-Exit-Pfad. Das ist kein
Connector- oder ModSecurity-Sicherheitsfehler. Der exakt generierte Stack wurde
gegen ein unabhängig SHA-verifiziertes offizielles `nginx-1.31.2`-Archiv
geprüft (beobachtetes SHA-256-Präfix/-Suffix `af2a957...473c`).

Das erhaltene Pre-Hardening-direkte-H1-O7-Artifact nach der Suppression
`direct-nginx-h1-memcheck-suppressed-20260801T234500Z-c8d9e0f1` zeichnete nur
innerhalb seiner damaligen begrenzten Diagnosegrenze ein cleanes Ergebnis auf:
`status=clean`, `complete=1`, `errors_detected=0`, `error_count=0`,
`definitely_lost_bytes=0`, `indirectly_lost_bytes=0`,
`possibly_lost_bytes=28160` und `still_reachable_bytes=329918`. Der
ausgewählte Connector-geladene gutartige Fall zeichnete `48` abgeschlossene
Requests mit `request_failures=0`, `worker_summary_failures=0` und
`server_alive=1` auf. Der isolierte Lifecycle zeichnete
`shutdown=graceful`, `wait=exited`, `wrapper_exit_code=0` und
`containment=isolated` auf; es blieben kein NGINX- oder Valgrind-Prozess,
keine `nginx.pid` und keine Testport-Bindung zurück. Diese historischen Werte
bleiben nur zur Provenance erhalten und sind nach der aktuellen Root-/Worker-
und Evidence-Trust-Härtung kein finaler Nachweis.

Die source-controlled lokale Datei
[`harness/valgrind-nginx-core-1.31.2.supp`](harness/valgrind-nginx-core-1.31.2.supp)
wird nicht aus Upstream kopiert. Sie matcht nur einen definiten
`Memcheck:Leak` auf `malloc -> ngx_alloc -> ngx_set_environment ->
ngx_worker_process_init -> ngx_worker_process_cycle -> ngx_spawn_process ->
ngx_start_worker_processes -> ngx_master_process_cycle -> main`. Das Artifact
zeichnet `suppressed: 1 from 1` auf. Mögliche Verluste bleiben in der payload-
freien Summary sichtbar, statt unterdrückt zu werden. Ein veränderter Stack,
eine Connector-/libmodsecurity-Diagnose oder eine Invalid-Access-Diagnose matcht
nicht und bleibt fehlschlagend.

Die source-controlled Suppression wird nur im opt-in-Modus `NGINX_MEMCHECK=1`
verwendet, nachdem die Distinct-Worker-Prüfung bei Root-Ausführung und alle
drei Binary-/Archive-Identitätsgates bestanden sind: Das ausgewählte
`NGINX_BINARY` entspricht `$NGINX_PREFIX/sbin/nginx`; die `nginx -v`-Ausgabe
lautet exakt `nginx version: nginx/1.31.2`; und
`$NGINX_BUILD_DIR/verified-archives/nginx-1.31.2.tar.gz` hat die
source-controlled SHA-256
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`.
Außerhalb des Memcheck-Modus behalten normale Harness-Aufrufe das bestehende
vom Aufrufer gewählte `NGINX_BINARY`-Override-Verhalten bei.

Diese erhaltene Diagnose bleibt Pre-Hardening und nicht kanonisch, solange
kanonisches Provisioning/Lifecycle-Containment und die Worker-sichtbare
Docroot-Projektion in Arbeit sind. Sie belegt keinen Erfolg für
`runtime-smoke-nginx`, H2/H3, Remote-CI, SonarQube, Pull Request oder Delivery.
Der separate erhaltene Remediation-Beleg oben deckt nur die Harness-/Evidence-
Grenze mit einem `pre-current-C`-Artifact ab. Ein separater frischer C-Build
validierte vorherigen C-Code, aber keiner der Belege ersetzt den exakten finalen
Security-Scan oder die finale PR-Head-CI/Sonar-Evidence.

## Unterstützte Anweisungen

Der adaptereigene NGINX-Connector registriert derzeit Folgendes:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_transaction_id`
- `modsecurity_use_error_log on|off`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`
- `modsecurity_phase4_body_limit <bytes>` (positives effektives Limit; ein
  über dem Limit liegender aktueller Buffer wird vor dem Downstream-Forwarding
  abgewiesen)

`modsecurity_transaction_id` verwendet einen komplexen NGINX-Wert und kann ihn auswerten
Variablen pro Anfrage. `modsecurity_transaction_id_expr` im Apache-Stil ist dies nicht
registriert für NGINX; Verwenden Sie `modsecurity_transaction_id` mit NGINX-Variablen
stattdessen. Die Anweisungen der Phase 4 sind begrenzte Laufzeitsteuerungen.
Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft. Die obigen fokussierten H1-
Beobachtungen belegen kein breites Late-Abort- oder kanonisches Lifecycle-
Ergebnis.

Primäre lokale Referenz: `<external-source-root>/ModSecurity-nginx`.
Upstream-Quelle: https://github.com/owasp-modsecurity/ModSecurity-nginx.

Das Adapter-eigene Build-Layout befindet sich unter `connectors/nginx/`: Modul `config`
ist bei `connectors/nginx/config`, produktive Quellen sind unter
`connectors/nginx/src/` und Support-Metadaten befinden sich im Connector-Stammverzeichnis. Die
Das frühere Verzeichnis `connectors/nginx/upstream/` wurde danach entfernt
Materialized-Source-NGINX-Builds und Smokes bestanden. Die dauerhafte Zuschreibung bleibt erhalten
`licenses/nginx/`, `connectors/nginx/ORIGIN.md` und
`connectors/nginx/SOURCE_MAP.json`.

Der Build-Helfer ist `modules/ModSecurity-test-Framework/ci/provisioning/prepare-nginx-build.sh`. Für das Monorepo ist es die Standardeinstellung
materialisiert `$BUILD_ROOT/nginx-build/connector-src` aus dem Besitz des Adapters
Nur die Dateien `connectors/nginx/config` und `connectors/nginx/src` werden dann erstellt
Connector als dynamisches NGINX-Modul gegen einen offiziellen `nginx/nginx` GitHub
Release-Archiv. Explizit
`MODSECURITY_NGINX_SOURCE_DIR`-Überschreibungen verwenden weiterhin eine bereinigte externe Quelle
kopieren.

## Gepinnte Release-Provenance für Full-Smoke

Der Parent-Full-Smoke-Workflow baut das ausgewählte direkte GitHub-Release-Asset
mit diesem atomaren Tupel:

```sh
BUILD_NGINX_FROM_SOURCE=1
# Framework-synchronized NGINX release tuple; do not duplicate it here.
NGINX_REQUIRE_PINNED_PROVENANCE=1
```

Er löst die direkte Release-Asset-URL aus dem festen Repository, Tag und
Asset-Namen auf. Der Full-Smoke-Resolver weist `latest` und
`/releases/latest` vor jeder Cache-, Netzwerk-, Download- oder
Extraktionsoperation ab. Seine Cache-Identität bindet das vollständige
Provenance-Tupel einschließlich Tag-/Ref-Gleichheit und SHA-256; spätere
Updates müssen jeden Tupelwert atomar ändern und überprüfen.
`NGINX_REQUIRE_PINNED_PROVENANCE=1` weist geerbte native Binary-/Modul-Overrides
ab, sodass ein System- oder MRTS-NGINX-Binary nicht als Full-Smoke-Evidence
akzeptiert wird.

Ein Managed-Full-Smoke-Runtime-Evidence-Record muss Release, Ref und Asset;
erwartete und tatsächliche Archiv-SHA-256-Werte; Source-Version und
Verzeichnis; Binary-Pfad, SHA-256 und Versions-Readback; Configure-Argumente;
Build-, Framework- und Parent-IDs; sowie die Erstellungszeit identifizieren.
Dies ist das erforderliche Evidence-Schema und keine Behauptung, dass ein
aktueller Runtime-Record existiert.

Der aktuelle NGINX-Common- und Profile-Registry-Build-Vertrag besteht aus:

```sh
MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include
MSCONNECTOR_PROFILE_REGISTRY_ROOT=$CONNECTOR_ROOT
```

`connectors/nginx/config` verwendet diese Werte beim Erstellen der
NGINX-Include-Pfade. Der verwaltete Exact-Head-Build ersetzt
`MSCONNECTOR_PROFILE_REGISTRY_ROOT` durch seine an die Cache-Identität gebundene
gestagte Root; direkte Source-Builds verwenden die oben gezeigte kanonische
Checkout-Root.

Historisch beobachtet am 15.05.2026: `NGINX_RELEASE_TAG=latest` gelöst zu
`release-1.31.0`, gebaut `nginx/1.31.0`, gebaut
`ngx_http_modsecurity_module.so` und der Harness beobachteten die YAML-Erwartungen
HTTP-Status für alle aktuell freigegebenen Minimalfälle. Dies ist nicht aktuell kanonisch
Phase-4-Facettenbeweise und keine akzeptierte Full-Smoke-Provenance-Einstellung.

## Eigentums- und Laufzeitansprüche testen

Ausführbare NGINX-Connector-Tests werden nicht im Framework-Modul verwaltet
unter `connectors/nginx/tests`. Der lokale Connector-Testordner wurde entfernt und
darf nicht wieder eingeführt werden.

Relevante Framework-Pfade:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Historisch generierte Beweise halten NGINX `partial` fest:

- Standard-Laufzeitrauch: `60/60 PASS`.
- Alle Laufzeitbeweise erzwingen: `140 Versuche / 95 PASS / 39 FAIL /
  0 BLOCKIERT / 6 NOT_EXECUTABLE`.

## Abdeckungs-/Laufzeit-Entscheidungsmatrix

Siehe den [kanonischen NGINX-Guide](../../docs/connectors/nginx.de.md) für die
Evidence-Grenze und die aktuelle Konfigurationsreferenz.

NGINX bleibt derzeit `partial`: Standardrauch ist sauber, erzwingt alle Beweise
Zeichnet weiterhin FAIL- und NOT_EXECUTABLE-Zeilen auf, generierte Abdeckungsberichte jedoch nicht
automatische Laufzeithochstufung und RESPONSE_BODY bleibt nicht hochgestuft.

Siehe [Konfiguration](../../docs/configuration.de.md) für die aktuelle
Apache/NGINX-Direktivenmatrix.

## Allgemeiner SDK-Einführungsbereich

NGINX bildet jetzt konnektorneutrale Semantik über `common/` für die Konfiguration ab,
Direktivennamen/Spezifikationen/Adapter, Request/Response-Mapper-Verträge, Header
Hilfsprogramme, ereignis-/grenzwertbezogene Verträge und C-Standard-Prüfungen wurden implementiert.
Der Besitz der NGINX-spezifischen API bleibt in `ngx_command_t`, `ngx_http_request_t`,
`ngx_chain_t`/`ngx_buf_t`, Zugriffs-/Header-/Body-Filter, Pools, Rückgabecodes und
Modulbaukleber. Die C17-Prüfung ist nur kompilierbar und meldet `BLOCKED`/exit 77
wenn NGINX- oder libmodsecurity-Header nicht verfügbar sind; optional C23/Future-C
Überprüfungen hängen von der Compiler-Unterstützung ab. Keine Produktion, CRS, Vollmatrix oder Laufzeit
Hier wird eine Verifizierung beansprucht.

NGINX-Common-SDK-Modul-Builds, die einen kopierten Connector-Quellbaum verwenden, müssen `MSCONNECTOR_COMMON_SRC` (oder `CONNECTOR_COMMON_SRC` / `COMMON_SRC_ROOT`) auf das Stammverzeichnis der gemeinsamen Quelle des Repositorys setzen; `MSCONNECTOR_COMMON_INC` bleibt der Common-Include-Root. Sie müssen außerdem `MSCONNECTOR_PROFILE_REGISTRY_ROOT` auf eine Root setzen, die `connectors/profile_registry.c` und `connectors/profile_registry.h` enthält. Der verwaltete Exact-Head-Koordinator stellt eine an die Cache-Identität gebundene gestagte Root bereit. Wenn die Variable nicht gesetzt ist, greift die Konfiguration nur dann auf `$ngx_addon_dir/../..` zurück, wenn dort beide Registry-Dateien existieren; dieser Fallback gilt für direkte Checkout-Builds, nicht für kopierte Trees.

## Kanonische Phase-4-Grenze

NGINX verwendet einen begrenzten nativen Antworttextfilter.  Seine Anwesenheit beweist nicht
entweder eine echte Phase-4-Regelauswertung oder ein veränderlicher Antwortstatus am
Moment des Eingreifens.  `phase4_pre_commit_deny` ist also
`not_implemented`: Die native Phase-4-Entscheidung wird im Körperfilter getroffen.
nach dem Antwort-Header-Pfad.  `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `late_intervention`, `late_intervention_log_only`,
`late_intervention_abort` und `late_intervention_status_metadata` bleiben bestehen
`implemented_not_asserted`, bis ein aktueller kanonischer Real-Host-Lauf das beweist
individuelles Verhalten.

Für einen file-only-NGINX-Buffer liest der Filter den sichtbaren Bereich
`file_pos..file_last` über genau einen wiederverwendeten 32-KiB-Scratch-Buffer
und bietet jeden begrenzten Chunk P4 genau einmal an. NGINXs speichermaßgebliche
Buffer-Semantik verhindert, dass ein gemischter Memory-/File-Buffer doppelt
gezählt wird. Ungültige Metadaten, ein Allokationsfehler sowie eine kurze oder
fehlgeschlagene Dateilesung liefern einen Connector-Fehler, bevor die aktuelle
Chain weitergeleitet wird; weder Scratch-Bytes noch Response-Payloads gelangen
in Event-JSONL.

Eine Regelübereinstimmung muss unabhängig von einem sichtbaren 403 gemeldet werden. Kanonisch
Ereignisse behalten den ursprünglichen Hoststatus, den angeforderten WAF-Status und den sichtbaren Client bei
Status, angeforderte Aktion, tatsächliche Aktion, Header-/Commit-Timing und Verbindung
Ergebnis abbrechen.  Dieser NGINX-Body-Filter-Pfad beansprucht keine Pre-Commit-Deny. A
Das sichere Ergebnis nach dem Commit ist `log_only` mit einem unveränderten sichtbaren Status. a
Das strikte Ergebnis ist `abort_connection` mit einem bereits sichtbaren Status und einem
bestätigter Verbindungsabbruch.  Es handelt sich auch nicht um einen getarnten erfolgreichen 403-Fall.

Die kanonischen Phase-4-Fälle sind evidenzbasiert und umfassen Regelbeobachtung,
Pre-Commit-Verweigerung, sichere Protokollierung, strikter Abbruch und Status-/Aktionsmetadaten.  Nein
Die Nutzlast des Antworttextes kann in ein Ereignis oder einen Bericht eingegeben werden.

Der Final-Processing-Guard bleibt bewusst enger als die Engine-Append-
Behandlung: `ProcessPartial` bei Append/From-File erzeugt für sich keinen
generischen 500-Pfad. Davon getrennt verwendet das Connector-eigene
Phase-4-Body-Limit begrenzte Ablehnung vor dem Forwarding eines übergroßen
aktuellen Buffers. Eine Partial-Body-Limitentscheidung kann damit weder einen
uninspektierten Downstream-Tail noch eine Late-Intervention-Behauptung erzeugen.
