# NGINX-Connector

**Sprache:** [English](README.md) | Deutsch


Status: Adaptereigene Quellmigration

Dieses Verzeichnis enthält den NGINX-Proof-of-Concept-Harness, die adaptereigene
NGINX-Connector-Quelle und Upstream-Attributionsdateien für den
ModSecurity-nginx-Connector. Es wird weiterhin durch reale Smoke-Tests
validiert und erhebt keinen Anspruch auf Produktionssupport.

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
#384 nicht: Final-Processing und Response-Body-Aufnahme bleiben bei einem
Ergebnis ungleich `1` fail-closed. Die Aufnahme des Request-Bodys aus dem
Speicher oder aus einer Datei verwendet denselben strikten Rückgabevertrag.
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
- `modsecurity_rules_remote` (abgelehnt: Remote-Regelladen ist durch die gemeinsame Sicherheitsrichtlinie deaktiviert)
- `modsecurity_transaction_id`
- `modsecurity_use_error_log on|off`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>` (nativer P4-JSONL-Sink; der dem Connector
  gehörende Deskriptor wird über den Common-No-Follow-Helper geöffnet und
  verlangt ein sicheres Elternverzeichnis, ein reguläres Blatt, geeignete
  Eigentümer und den privaten Modus `0600`)
- `modsecurity_phase4_body_limit <bytes>` (positives effektives Limit; ein
  über dem Limit liegender aktueller Buffer wird vor dem Downstream-Forwarding
  abgewiesen)

`modsecurity_phase4_body_limit` hat standardmäßig 1048576 Byte (1 MiB). Der
Common-Konfigurationsvalidator lehnt einen gewählten Wert über 10485760 Byte
(10 MiB) ab, sodass ein nativer Response-Filter kein unbeschränktes
Phase-4-Bytebudget erhalten kann.

Wenn `modsecurity_phase4_content_types_file` konfiguriert ist, öffnet und
prüft das native Modul den Deskriptor, akzeptiert nur eine reguläre Datei,
begrenzt sie auf 64 KiB und weist verkürzte Reads ab. FIFOs, Geräte, Sockets,
Verzeichnisse und übergroße Dateien können `nginx -t` daher nicht in einen
unbeschränkten oder blockierenden Konfigurations-Read unter POSIX führen. Die
Direktive schlägt unter Win32 fail-closed fehl, weil dessen Datei-API nicht
denselben Regular-File-/Nichtblockierungs-Vertrag herstellen kann.

Native NGINX-Phase-4-Event-Dateien sind nur über den beim Konfigurationsladen
erzeugten, dem Connector gehörenden Deskriptor verfügbar. Die generische
`cycle->open_files`-Registrierung wird nicht verwendet: unsichere Symlink- oder
nicht reguläre Ziele, unsichere Eltern/Eigentümer und unsichere Modi schlagen
fail-closed fehl. Ein normales Konfigurations-Reload öffnet für den neuen Zyklus
einen sicheren Deskriptor und ist der unterstützte Rotationsweg. Das generische
NGINX-`USR1`-Erneutöffnen wird für Rotation bewusst nicht unterstützt, weil es
diesen No-Follow-Vertrag nicht erhalten kann. Der Laufzeitnachweis für den
Functional-A-Pfad wird separat geführt; Protected-B-Attestierung und die externe
Abhängigkeit FND-PARENT-1036 werden hier nicht behauptet. Der Event-Pfad
der Common-Runtime bleibt durch seine eigene sichere Descriptor-Policy geregelt;
die NGINX-Direktive fällt nicht still auf diesen Pfad zurück.

`modsecurity_transaction_id` verwendet einen komplexen NGINX-Wert und kann
Variablen pro Anfrage auswerten. Das Apache-artige
`modsecurity_transaction_id_expr` ist für NGINX nicht registriert; verwenden
Sie stattdessen `modsecurity_transaction_id` mit NGINX-Variablen. Die
Phase-4-Direktiven sind begrenzte Laufzeitsteuerungen.
Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft. Die obigen fokussierten H1-
Beobachtungen belegen kein breites Late-Abort- oder kanonisches Lifecycle-
Ergebnis.

Primäre lokale Referenz: `<external-source-root>/ModSecurity-nginx`.
Upstream-Quelle: https://github.com/owasp-modsecurity/ModSecurity-nginx.

Das adaptereigene Build-Layout befindet sich unter `connectors/nginx/`: Das
Modul `config` liegt unter `connectors/nginx/config`, produktive Quellen unter
`connectors/nginx/src/`, und Support-Metadaten liegen im Connector-Stammverzeichnis.
Das frühere Verzeichnis `connectors/nginx/upstream/` wurde entfernt, nachdem
materialisierte NGINX-Builds und Smokes bestanden hatten. Die dauerhafte
Attribution bleibt in `licenses/nginx/`, `connectors/nginx/ORIGIN.md` und
`connectors/nginx/SOURCE_MAP.json`.

Der Build-Helfer ist
`modules/ModSecurity-test-Framework/ci/provisioning/prepare-nginx-build.sh`.
Im Monorepo-Standard materialisiert er
`$BUILD_ROOT/nginx-build/connector-src` ausschließlich aus den adaptereigenen
Dateien `connectors/nginx/config` und `connectors/nginx/src` und baut den
Connector dann als dynamisches NGINX-Modul gegen ein offizielles
`nginx/nginx`-GitHub-Release-Archiv. Explizite
`MODSECURITY_NGINX_SOURCE_DIR`-Overrides verwenden weiterhin eine bereinigte
externe Source-Kopie.

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

NGINX bleibt derzeit `partial`: Der Standard-Smoke ist sauber, die
Force-all-Evidence zeichnet weiterhin FAIL- und NOT_EXECUTABLE-Zeilen auf,
die generierte Abdeckungsberichterstattung bewirkt keine automatische
Runtime-Hochstufung, und RESPONSE_BODY bleibt nicht hochgestuft.

Siehe [Konfiguration](../../docs/configuration.de.md) für die aktuelle
Apache/NGINX-Direktivenmatrix.

## Allgemeiner SDK-Einführungsbereich

NGINX bildet, soweit implementiert, connectorneutrale Semantik über `common/`
ab: Konfiguration, Direktivennamen/Spezifikationen/Adapter,
Request/Response-Mapper-Verträge, Header-Helper, ereignis- und limitbezogene
Verträge sowie C-Standard-Prüfungen. Die NGINX-spezifische API bleibt in
`ngx_command_t`, `ngx_http_request_t`, `ngx_chain_t`/`ngx_buf_t`,
Access-/Header-/Body-Filtern, Pools, Rückgabecodes und Modulbaukleber
verantwortet. Die C17-Prüfung ist compile-only und meldet `BLOCKED`/exit 77,
wenn NGINX- oder libmodsecurity-Header nicht verfügbar sind; optionale
C23/Future-C-Prüfungen hängen von der Compiler-Unterstützung ab. Hier wird
keine Produktions-, CRS-, Vollmatrix- oder Runtime-Verifikation behauptet.

NGINX-Common-SDK-Modul-Builds, die einen kopierten Connector-Quellbaum verwenden, müssen `MSCONNECTOR_COMMON_SRC` (oder `CONNECTOR_COMMON_SRC` / `COMMON_SRC_ROOT`) auf das Stammverzeichnis der gemeinsamen Quelle des Repositorys setzen; `MSCONNECTOR_COMMON_INC` bleibt der Common-Include-Root. Sie müssen außerdem `MSCONNECTOR_PROFILE_REGISTRY_ROOT` auf eine Root setzen, die `connectors/profile_registry.c` und `connectors/profile_registry.h` enthält. Der verwaltete Exact-Head-Koordinator stellt eine an die Cache-Identität gebundene gestagte Root bereit. Wenn die Variable nicht gesetzt ist, greift die Konfiguration nur dann auf `$ngx_addon_dir/../..` zurück, wenn dort beide Registry-Dateien existieren; dieser Fallback gilt für direkte Checkout-Builds, nicht für kopierte Trees.

## Kanonische Phase-4-Grenze

NGINX verwendet einen begrenzten nativen Response-Body-Filter. Seine
Anwesenheit beweist weder eine tatsächliche Phase-4-Regelauswertung noch einen
veränderlichen Response-Status zum Zeitpunkt der Intervention.
`phase4_pre_commit_deny` ist daher `not_implemented`: Die native
Phase-4-Entscheidung wird im Body-Filter nach dem Response-Header-Pfad
getroffen. `response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`late_intervention`, `late_intervention_log_only`, `late_intervention_abort`
und `late_intervention_status_metadata` bleiben `implemented_not_asserted`,
bis ein aktueller kanonischer Real-Host-Lauf das jeweilige Verhalten beweist.

Für einen file-only-NGINX-Buffer liest der Filter den sichtbaren Bereich
`file_pos..file_last` über genau einen wiederverwendeten 32-KiB-Scratch-Buffer
und bietet jeden begrenzten Chunk P4 genau einmal an. NGINXs speichermaßgebliche
Buffer-Semantik verhindert, dass ein gemischter Memory-/File-Buffer doppelt
gezählt wird. Ungültige Metadaten, ein Allokationsfehler sowie eine kurze oder
fehlgeschlagene Dateilesung liefern einen Connector-Fehler, bevor die aktuelle
Chain weitergeleitet wird; weder Scratch-Bytes noch Response-Payloads gelangen
in Event-JSONL.

`tests/run_nginx_body_buffer_fixture.py` ist eine reine Test-Fixture für die
native Grenzprüfung. Sie baut den ausgewählten sauberen Connector-Checkout und
eine separate reine Fixture in ein dediziertes NGINX-Test-Binary gegen die
gepinnte NGINX-Quelle neu und gibt echte Memory-, file-only- und gemischte
`ngx_buf_t`-Werte durch die installierte Filterkette aus. Ihr test-only Filter
steht unmittelbar vor dem statisch gelinkten Connector und zeichnet die echten
Flags an dieser Grenze auf. Für file-only- und injizierte File-Fehlerkontrollen
wählt er die file-only-Repräsentation dieses echten Buffers nur für den direkten
Connector-Aufruf und stellt die Upstream-Repräsentation vor der Rückkehr wieder
her; dies ist eine ausdrückliche Fixture-Grenze und keine Behauptung über jeden
Upstream-Output-Filter. Die Mixed-Kontrolle behält beide Repräsentationen und
verwendet unterschiedliches File-Backing: Die P4-Regel belegt die
memory-first-Inspektion, während der separat aufgezeichnete weitergeleitete Body
das NGINX-File-Backing bleibt. Ihre Testkonfiguration wählt das bestehende Limit
nur für Fälle innerhalb des Limits und für Reject-before-forwarding; sie ändert
keinen Produkt-Default. Ihr Allokationsfehlerfall verändert nur das Test-Binary:
Dieselbe test-only Grenze aktiviert einen Fixture-Wrapper für die bekannte
32-KiB-`ngx_pnalloc`-Scratch-Anfrage und zeichnet genau einen Wrapper-Treffer
auf. Weder Connector-Code noch ein Produktions-Fault-Injection-Schalter werden
verändert. Das zurückgehaltene Ergebnis enthält nur exakten Head,
Build-Identitäten, verifizierte Filterreihenfolge, Buffer-Flags, Längen,
begrenzte Forwarding-Hashes und Accounting-Werte—keine Response-Nutzlasten.

Das GitHub-hosted-Functional-A-Gate veröffentlicht zusätzlich genau ein
begrenztes, payload-sicheres `result.json` erst nachdem beide echten
`modsecurity_use_error_log`-On-/Off-Zellen bestanden haben. Es enthält den
exakten Head, NGINX-Archiv-/Build-Identitäten, Redaction-/Truncation-/
Integrity-/Transaktionsfakten, die Raw-WAF-Canary-Beobachtung, Callback-Status
und Lifecycle-Fakten, aber keinen Raw-Log, Target, Canary, Nutzlast,
Transaktionskennung, Zeitstempel oder absoluten Pfad. Dies ist kandidaten-
eigene Integrations-Evidence und keine unabhängige Protected-Host-Attestation.

Eine Regelübereinstimmung muss unabhängig von einem sichtbaren 403 gemeldet
werden. Kanonische Ereignisse bewahren den ursprünglichen Host-Status, den
angeforderten WAF-Status, den sichtbaren Client-Status, die angeforderte und
die tatsächliche Aktion, Header-/Commit-Timing und das Ergebnis eines
Verbindungsabbruchs. Dieser NGINX-Body-Filter-Pfad beansprucht keine
Pre-Commit-Deny. Ein sicheres Post-Commit-Ergebnis ist `log_only` mit
unverändertem sichtbarem Status; ein striktes Ergebnis ist
`abort_connection` mit bereits sichtbarem Status und einem bestätigten
Verbindungsabbruch. Keines von beiden ist ein getarnter erfolgreicher
403-Fall.

Die kanonischen Phase-4-Fälle sind evidenzgebunden und umfassen
Regelbeobachtung, Pre-Commit-Deny, sicheres Log-only, strikten Abbruch sowie
Status-/Aktionsmetadaten. Keine Response-Body-Nutzlast darf in ein Ereignis
oder einen Bericht gelangen.

Final-Processing und Body-Ingestion verwenden denselben strikten nativen
Erfolgsvertrag: Jeder relevante libmodsecurity-Aufruf muss exakt `1` liefern.
Ein Aufnahmefehler einschließlich eines Rückgabewerts `0` führt zu einem
generischen fail-closed-`500`/Interventionspfad und wird nicht als nichtfatale
`ProcessPartial`-Limitentscheidung behandelt. So bleibt das bestehende
Safe/Strict-Phase-4-Result-Modell erhalten, ohne einen unvollständig
aufgenommenen Body stillschweigend an Final-Processing weiterzugeben.
Der Final-Processing-Guard bleibt bewusst enger als die Engine-Append-
Behandlung: `ProcessPartial` bei Append/From-File erzeugt für sich keinen
generischen 500-Pfad. Davon getrennt verwendet das Connector-eigene
Phase-4-Body-Limit begrenzte Ablehnung vor dem Forwarding eines übergroßen
aktuellen Buffers. Eine Partial-Body-Limitentscheidung kann damit weder einen
uninspektierten Downstream-Tail noch eine Late-Intervention-Behauptung erzeugen.
