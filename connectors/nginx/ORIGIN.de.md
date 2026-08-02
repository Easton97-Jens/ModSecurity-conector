# Ursprungsübersicht des NGINX-Connectors

**Sprache:** [English](ORIGIN.md) | Deutsch

Status: adapter-owned source migration complete

Lokale Referenz: `<external-source-root>/ModSecurity-nginx`
Upstream-Quelle: https://github.com/owasp-modsecurity/ModSecurity-nginx
Source-Branch: `master`
Source-Commit: `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`
Source-Beschreibung: `v1.0.4-14-g9eb44fd`
Lizenz: Apache-2.0, aufbewahrt in `licenses/nginx/LICENSE`
Standard-Importpfad: `connectors/nginx`

| Repository | Lokale Referenz | Upstream | Beobachteter Commit | Beobachtete Version/Tag | Lizenz |
| --- | --- | --- | --- | --- | --- |
| ModSecurity-nginx | `<external-source-root>/ModSecurity-nginx` | https://github.com/owasp-modsecurity/ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | `v1.0.4-14-g9eb44fd` | Apache-2.0 |

Zentrale Attribution: `licenses/nginx/`

## Adapter-eigener Quellcode

NGINX baut nun aus einem materialisierten Quellbaum, der unter
`$BUILD_ROOT/nginx-build/connector-src` erzeugt wird. Das Modul `config` ist
adapter-eigen unter `connectors/nginx/config`, und produktiver Modulquellcode
ist adapter-eigen unter `connectors/nginx/src/`. Der frühere Referenzbaum
`connectors/nginx/upstream/` wurde in Phase 10 entfernt, nachdem die
Quellmigration, der Build des materialisierten Quellcodes und reale
NGINX-Smokes bestanden hatten.

| Adapter-eigener Pfad | Ursprünglicher Upstream-Pfad | Repository | Basis-Commit | Zusätzliche Provenienz | Lizenz | Importgrund |
| --- | --- | --- | --- | --- | --- | --- |
| `connectors/nginx/config` | `config` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX-Dynamic-Module-Build-Metadaten |
| `connectors/nginx/src/ngx_http_modsecurity_access.c` | `src/ngx_http_modsecurity_access.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #384 `65de4cd8739209f22d924d85548bd012a4d94607`; PR #386 `a7fd4fcc18dc442b1b093d253f457b9317b7f588` | Apache-2.0 | NGINX-Integration in der Access-Phase plus ausgewählte Final-Processing-, ProcessPartial-kompatible, Address- und Header-Registration-Behandlung |
| `connectors/nginx/src/ngx_http_modsecurity_body_filter.c` | `src/ngx_http_modsecurity_body_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac`; PR #384 `65de4cd8739209f22d924d85548bd012a4d94607`; PR #385 `471a2a54843bb8f560758a7e75b146db2243ab29`; PR #386 `a7fd4fcc18dc442b1b093d253f457b9317b7f588`; Parent FND-PARENT-0080; Parent-Phase-3-Gate für connector-eigene `Location`-Provenance | Apache-2.0 | NGINX-Integration für Response-/Body-Filter plus Phase-4-, Final-Processing-, Redirect-Body-Replacement nur nach connector-eigener `Location`-Provenance, Terminal-Loop-Behandlung und wiederhergestellte begrenzte Aufnahme vor dem Connector-Scope-Action-Mapping |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | `src/ngx_http_modsecurity_common.h` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac`; PR #385 `471a2a54843bb8f560758a7e75b146db2243ab29`; Parent-Phase-3-State für connector-eigene `Location`-Provenance | Apache-2.0 | Gemeinsame NGINX-Connector-Deklarationen plus Phase-4-Felder und Response-Replacement-State, der eine Connector-installierte `Location` von einer Upstream-`Location` unterscheidet |
| `connectors/nginx/src/ngx_http_modsecurity_header_filter.c` | `src/ngx_http_modsecurity_header_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #384 `65de4cd8739209f22d924d85548bd012a4d94607`; PR #385 `471a2a54843bb8f560758a7e75b146db2243ab29`; PR #386 `a7fd4fcc18dc442b1b093d253f457b9317b7f588`; Parent-Phase-3-Gate für connector-eigene `Location`-Provenance | Apache-2.0 | NGINX-Header-Filter-Integration plus ausgewählte Intervention-, Protocol-/Header-, Redirect- und Registration-Härtung; eine Status-only-Intervention mit Upstream-`Location` finalisiert statt die Response zu ersetzen |
| `connectors/nginx/src/ngx_http_modsecurity_log.c` | `src/ngx_http_modsecurity_log.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX-Integration in der Log-Phase |
| `connectors/nginx/src/ngx_http_modsecurity_module.c` | `src/ngx_http_modsecurity_module.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac`; PR #384 `65de4cd8739209f22d924d85548bd012a4d94607`; PR #385 `471a2a54843bb8f560758a7e75b146db2243ab29`; Parent-Redirect-URL-CR/LF-Ablehnung | Apache-2.0 | NGINX-Modul-Einstiegspunkt/Konfiguration plus Phase-4-Direktiven, Transaction-Lifecycle- und Redirect-Response-Behandlung, die bei CR oder LF in einer Redirect-URL fail-closed fehlschlägt, bevor ein Buffer alloziert oder `Location` installiert wird |
| `connectors/nginx/src/ddebug.h` | `src/ddebug.h` | repository-eigener Kompatibilitäts-Header | n/a | ersetzt importierten Upstream-Debug-Helper | Apache-2.0-kompatibler Projektcode | Hält die NGINX-Modul-Build-Abhängigkeit erfüllt, ohne den importierten Debug-Helper in `upstream/` aufzubewahren |
| `connectors/nginx/metadata.c` | n/a | repository-eigene Adapter-Metadaten | n/a | none | Apache-2.0-kompatibler Projektcode | Ursprungsmetadaten für Report-/Build-Zusammenfassungen |
| `connectors/nginx/metadata.h` | n/a | repository-eigene Adapter-Metadaten | n/a | none | Apache-2.0-kompatibler Projektcode | Ursprungsmetadaten für Report-/Build-Zusammenfassungen |
| `connectors/nginx/harness/run_nginx_smoke.sh` | n/a | repository-eigener Parent-Harness | n/a | Parent-Root-only-Distinct-Worker-, private-Output- und Worker-Leaf-Ownership-Härtung | Apache-2.0-kompatible Projekt-Support-Datei | Direkter NGINX-Harness mit `NGINX_MEMCHECK_EVIDENCE_DIR` privat unter `LOG_DIR/memcheck-evidence/<case>` und nur worker-eigenen State-/Server-Access-/Error-/Audit-Leaves unter dem Worker-traversierbaren Harness-Root |
| `connectors/nginx/SOURCE_MAP.json` | n/a | repository-eigenes Provenienzmanifest | n/a | zeichnet Basis, PR #377, ausgewählte PRs #384--#386, die abgegrenzte Disposition von #387/#388/#389 sowie Parent-/Finding-Evidenzgrenzen einschließlich aktueller Response- und Harness-Härtung auf | Apache-2.0-kompatible Projektmetadaten | Quellmigrations- und PR-Provenienzübersicht |

## Layout-Verschiebungen in Phase 13

| Früherer Pfad | Aktueller Pfad | Materialisierter Pfad |
| --- | --- | --- |
| `connectors/nginx/src/config` | `connectors/nginx/config` | `config` |
| `connectors/nginx/src/metadata.*` | `connectors/nginx/metadata.*` | not materialized |
| `connectors/nginx/src/SOURCE_MAP.json` | `connectors/nginx/SOURCE_MAP.json` | not materialized |
| `connectors/nginx/src/README.md` | `connectors/nginx/README.md` und Dokumentation | not materialized |

## Aufnahme von PR #377

PR: https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377

Beobachteter PR-Head-Commit: `3d72b004ff27a78ea19c6b945870e2cae62a97ac`

Die PR-Quelländerungen wurden nur auf adapter-eigene NGINX-Quelldateien
angewendet:

- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_module.c`

Die importierten PR-Tests/-Dokumentation wurden nicht in die aktive Smoke-Suite
kopiert. Phase 4 / `RESPONSE_BODY` bleibt nicht hochgestuft; die unten
aufgezeichnete fokussierte reine-NGINX-Evidenz fügt `RESPONSE_BODY` nicht zu
`verified_variables` hinzu und ersetzt keine separate Apache+NGINX-Real-World-
Promotion.

## Selektive Aufnahme der PRs #384--#387

Die importierte Basis bleibt `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846`, und
die frühere lokale PR-#377-Provenienz bleibt
`3d72b004ff27a78ea19c6b945870e2cae62a97ac`. Das folgende Upstream-Material
wird selektiv in den adapter-eigenen Parent-Source übernommen; dies behauptet
weder, dass die Upstream-Pull-Requests gemergt sind, noch dass ihre
Test-Evidence in diesem Repository lief.

| Upstream-Input | Beobachteter Head | Parent-Auswahl |
| --- | --- | --- |
| [PR #384](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/384) | `65de4cd8739209f22d924d85548bd012a4d94607` | Behält Fail-Closed-Behandlung für eindeutiges finales Request-/Response-Processing und unsichere Intervention-Fehler bei. `msc_append_request_body()`, `msc_request_body_from_file()` und `msc_append_response_body()` bleiben nicht fatal, weil `ProcessPartial` dasselbe Rückgabesignal für beabsichtigte Trunkierung verwendet; das nachfolgende finale Processing bleibt für die Inspection verantwortlich. |
| [PR #385](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/385) | `471a2a54843bb8f560758a7e75b146db2243ab29` | Wählt Response-Header-Fidelity und Phase-3-Redirect-Replacement: `Location` bleibt erhalten, verworfene Entity-Metadaten werden gelöscht und der ersetzte Body wird verworfen. Das Parent-Follow-up behandelt Replacement nur dann als gültig, wenn der Connector sein eigenes `Location` installiert hat; ein Upstream-`Location` bei einer Status-only-Intervention finalisiert stattdessen die Response. Redirect-URLs mit CR oder LF schlagen fail-closed fehl, bevor ein Buffer alloziert oder `Location` installiert wird. Der Parent unterdrückt außerdem fiktive synthetische `Connection`-/`Keep-Alive`-Header für natives HTTP/3 neben dem ausgewählten Negotiated-Protocol-Mapping; diese Controls sind task-lokal, keine Live-HTTP/3-Evidence. |
| [PR #386](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/386) | `a7fd4fcc18dc442b1b093d253f457b9317b7f588` | Wählt wertfreie Warning-Sichtbarkeit für Header-Registration-Fehler, Empty-Address-Guards und einen terminalen Body-Filter-Stopp, der die verbleibende NGINX-Chain weiterleitet. |
| [PR #387](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/387) | `4c1f0362ca0f25ef216ce59cad5fa6c9703c1438` | Wählt die Test-Design-Richtung für einen Parent-eigenen opt-in bounded native soak (`make soak-nginx`) und eine opt-in H1-Memcheck-Diagnose (`make memcheck-nginx`) über den vorhandenen Harness. Beide bleiben außerhalb von Default-Smoke/Test/CI und schreiben begrenzte payload-freie Summaries. Der source-gesteuerte Soak-Selektor lässt zwischen einer und acht eindeutige IDs aus seinem expliziten kanonischen Katalog zu und weist leere, doppelte oder außerhalb des Katalogs liegende Selektionen vor der Case-Discovery ab. Upstream-Dockerfiles, Workflows, Valgrind-/Helgrind-Konfiguration und Soak-Tooling werden nicht importiert. Das erhaltene direkte H1-Artifact unten ist Pre-Hardening und nicht kanonisch, kein finaler Nachweis; es wird kein kanonischer Memcheck-, Helgrind- oder Soak-Erfolg behauptet. |

### Wiederherstellung der Parent-Phase-4-Content-Type-Aufnahme

Diese Task stellt eine vor der Task bestehende Parent-Regression im Body-Filter
wieder her: Begrenzte Response-Bytes erreichen ModSecurity unabhängig vom
konfigurierten Connector-Content-Type-Scope. Der Scope wird beim Mapping einer
erkannten Intervention angewendet; eine außerhalb des Scopes liegende
Intervention wird zu `log_only` mit `content_type_not_in_scope`. Die Reparatur
schwächt die ausgewählte #384-Final-Processing-Grenze nicht: Ein finales
`msc_process_response_body()`-Ergebnis ungleich `1` bleibt fail-closed,
während `ProcessPartial`-Append-/From-File-Verhalten absichtlich nicht fatal
bleibt.

### Parent-Phase-3-Response-Replacement-Härtung

Dieses Parent-only-Follow-up ist keine Upstream-Attributionsbehauptung. Eine
Phase-3-Response wird nur ersetzt, wenn der Connector-Redirect-Helper sein
eigenes `Location` installiert und
`intervention_redirect_location_installed` gesetzt hat; eine erhaltene
Upstream-`Location` bei einer Status-only-Intervention folgt stattdessen der
NGINX-Finalisierung. Eine Redirect-URL mit CR oder LF schlägt mit
`NGX_HTTP_BAD_REQUEST` fail-closed fehl, bevor ein Response-Buffer alloziert
oder `Location` installiert wird.

### Parent-Härtung des direkten Harness und der Memcheck-Evidence

Auch diese Parent-only-Harness-Arbeit ist kein Upstream-Import. Der direkte
Harness erfordert Root-Ausführung und schlägt fail-closed fehl, sofern root
`NGINX_WORKER_USER` nicht als separates lokales Konto lösen und verifizieren,
dessen Gruppe auflösen und `user <resolved-user> <resolved-group>;` in der
generierten NGINX-Konfiguration rendern kann. Root-eigene private
Runtime-/Harness-Ausgabe, `NGINX_PHASE4_LOG_FILE` und
`NGINX_MEMCHECK_EVIDENCE_DIR` bleiben von `NGINX_WORKER_STATE_ROOT` und den
Access-/Error-/Audit-Leaves von `NGINX_SERVER_LOG_ROOT` getrennt. Der Memcheck-
Evidence-Pfad liegt privat unter `LOG_DIR/memcheck-evidence/<case>`; nur die
getrennten `worker-state`- und `server-logs`-Bäume liegen unter dem
Worker-traversierbaren Harness-Root.
Die unten beschriebene Opt-in-Docroot-Projektion ist eine getrennte root-eigene
statische Grenze, kein weiterer worker-eigener Harness-Output.

Der Parent-Memcheck-Summarizer akzeptiert cleane Evidence nur aus effektive-
UID-eigenen echten Root-/Parent-Verzeichnissen, die nicht für Gruppe oder
Andere beschreibbar sind. Metadata, Logs und Outputs müssen direkte Kinder
sein; Eingaben müssen private Regular-Dateien mit einem Link sein, die mit
No-Follow-Schutz geöffnet und beim Lesen auf Ersetzung geprüft werden.
Unsichere Evidence wird abgelehnt oder unvollständig, nicht clean.

Der erhaltene Beleg
`$RUN/evidence/direct-nginx-h1-memcheck-evidence-remediation-20260801.md`
(SHA-256
`37f01fe3d1851d43ae21d2b705b02bf01f204ff5cb19b41354e5b801a4b158a8`)
zeichnet `passed_noncanonical_diagnostic` für einen begrenzten dreisekündigen
`allow_without_marker`-No-CRS-H1-Fall unter bewusster `umask 022` auf. Der
Root-Lauf verwendete den separaten verifizierten Worker `nobody`, private
Mode-`0700`-Ausgabe sowie Mode-`0700`-Worker-State-/Server-Log-Leaves im
Eigentum von `nobody:nogroup`. Der Summarizer akzeptierte zwei private
Valgrind-Eingaben, schrieb Role-/Lifecycle-/JSON-/Text-Outputs im Modus `0600`
und zeichnete 28 Requests ohne Request- oder Worker-Summary-Fehler sowie eine
vollständige cleane Summary mit null Fehlern und null definitiv/indirekt
verlorenen Bytes auf.

Dies ist direkte Runtime-Evidence für die remediierte Harness-/Evidence-Grenze,
nicht für das aktuelle C-Redirect-Verhalten: Der Beleg nutzt das erhaltene
SHA-verifizierte NGINX-`1.31.2`-`pre-current-C`-Diagnose-Artifact. Ein
separater frischer C-Source-Build validierte den vorherigen C-Code, aber dieser
Beleg führt diesen Code nicht aus. Der exakte finale Security-Scan und finale
PR-Head-CI/Sonar-Evidence bleiben ausstehend.

### Parent-NGINX-Harness-Output-Path-Authority

Diese Parent-only-Remediation zeichnet `FND-PARENT-0084` als `validated` mit
der Task-Remediation `in_progress` auf; sie ist kein Upstream-Import. Vor jedem
root-Harness-`mkdir`, Installieren, `chown`, `chmod`, `rm` oder jeder Output-
Redirection müssen alle generischen/privaten Bootstrap-, Parent-Multi-Case- und
Work-/Output-Roots pro Case als strikte Nachkommen von `VERIFIED_RUN_ROOT`
validieren. Konfigurierbare Diagnostic-, Worker-Preflight-, Protocol-Artifact-,
Lifecycle-Evidence- sowie Curl-Response-/Error-Outputs durchlaufen dasselbe
Authority-Gate. `/dev/null` ist der einzige explizite interne Bounded-Soak-Sink.

Die einzige bewusst enge Ausnahme ist Opt-in `NGINX_DOCROOT_PROJECTION=1`.
`NGINX_DOCROOT_PROJECTION_PARENT` ist ein explizit im Manifest vorregistrierter
externer Parent außerhalb der privaten Runtime-Roots. Er muss bereits
existieren, root-eigen und symlink-frei sein, Lese- oder Schreibzugriff für
Gruppe/Andere verweigern und in einer `0711`-sicheren Form für den Worker
traversierbar sein; auch seine Ancestors müssen traversierbar sein.
`NGINX_DOCROOT_PROJECTION_ROOT` muss sein exaktes frisches direktes statisches
Kind sein. Der Projection-Helper validiert den Parent und erzeugt nur dieses
Kind, kopiert die allowlisteten statischen Dateien und macht das Kind für den
Worker traversierbar. Das generische Harness-Ownership-/Mode-Setup führt auf
dem externen Parent niemals `chown` oder `chmod` aus; kein generischer Output
ist dort autorisiert.

Der erhaltene Parent-Beleg
`$RUN/evidence/nginx-harness-path-authority-remediation-20260801.md`
(SHA-256
`e1b09454d3dc823b78d83bdae960d431951b432cad57aa05df4434a8bd905c7b`)
zeichnet einen realen Parent-Multi-Case-(`RUN_ONE_CASE=0`)-`LOG_DIR=/etc`-
Negativtest auf. Er endete vor der normalen Runtime-Assertion mit `77`; `/etc`
war unmittelbar davor und danach im Modus `0755`, Eigentümer/Gruppe `0:0`, und
es entstanden kein System-Output, NGINX-Prozess oder Listener. Die fokussierte
Authority-Suite bestand 5/5 für Out-of-Root-, Sibling-/Symlink-Escape- und
In-Root-Controls.

Dieser Beleg validiert nur die Output-Path-Grenze. Die `PYTHON`-/`PATH`-
Launch-Resolution bleibt eine vertrauenswürdige Operator-/CI-Annahme außerhalb
dieses Findings. Die kanonische Runtime bleibt blockiert, und der frische
C-Build validiert vorherigen C-Code statt dieser Shell-Harness-Härtung; finale
Security-Scan- und PR-Head-Evidence bleiben ausstehend. Der erhaltene Generic-
Path-Beleg promoviert die neue Projection-Ausnahme nicht zu kanonischer
Runtime-Evidence.

Die fokussierte Task-Evidence ist absichtlich enger als Promotion-Evidence.
Der strikte isolierte Rebuild sowie C17, C23 und c2y bestanden; die neu
materialisierte Build-Source-SHA entsprach dem Task-Filter; und der ausgewählte
native H1-Out-of-Scope-Fall ohne CRS und ohne MRTS bestand. Die Korrektur im
Task-Worktree ist kein kanonischer Finding-Abschluss: FND-PARENT-0080 bleibt
als `validated` aufgezeichnet, weil aktuelles `master` das frühere Verhalten
enthält. Diese Ursprungsübersicht schließt es nicht und behauptet keinen
finalen integrierten Task-Head.

Die ausgewählten Parent-Safe-/Strict-Ergebnisse wurden ebenfalls beobachtet:
Safe behielt `log_only` bei unverändertem bereits sichtbarem Status, und Strict
verwendete nach dem Commit `abort_connection`. Der vollständige ausgewählte
Runner endet dennoch nichtnull, weil read-only-Framework-Fixture-Assertions den
Safe-Modus als Reason erwarten und zugleich einen stabilen `403`/eine obsolete
Action trotz Strict-Connection-Abort erwarten. FND-FRAMEWORK-0058 ist daher
hier `blocked` und `out_of_scope`; es wird keine Framework-Änderung behauptet.

Die Phase-4-Modi bleiben durch diese Aufnahme unverändert: Safe Late Handling
zeichnet `log_only` bei unverändertem bereits sichtbarem Status auf, während
Strict Late Handling `abort_connection` statt einer erfundenen zweiten Response
verwendet. Die obigen fokussierten H1-Beobachtungen belegen keine kanonische
Lifecycle-, Transport- oder breite Promotion-Evidence.

### Erhaltene Pre-Hardening-H1-Memcheck-Evidenz und lokale Suppression

Die initiale direkte H1-Valgrind-Memcheck-Diagnose beobachtete eine 8-Byte-
`definitely-lost`-NGINX-Core-Worker-Exit-Allocation. Das ist kein Connector-
oder ModSecurity-Sicherheitsfinding. Der exakt generierte Stack wurde gegen ein
unabhängig SHA-verifiziertes offizielles `nginx-1.31.2`-Archiv geprüft
(beobachtetes SHA-256-Präfix/-Suffix `af2a957...473c`).

Das erhaltene Pre-Hardening-direkte-H1-O7-Artifact nach der Suppression
`direct-nginx-h1-memcheck-suppressed-20260801T234500Z-c8d9e0f1` zeichnete nur
innerhalb seiner damaligen direkten Diagnosegrenze ein cleanes Ergebnis auf:
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

`connectors/nginx/harness/valgrind-nginx-core-1.31.2.supp` ist eine lokale,
source-controlled Task-Datei; sie wird nicht aus Upstream kopiert. Sie matcht
nur `Memcheck:Leak` mit `match-leak-kinds: definite` und diesen exakten
NGINX-Core-Stack:

```text
malloc -> ngx_alloc -> ngx_set_environment -> ngx_worker_process_init
-> ngx_worker_process_cycle -> ngx_spawn_process
-> ngx_start_worker_processes -> ngx_master_process_cycle -> main
```

Das Artifact zeichnet `suppressed: 1 from 1` auf. Mögliche Verluste bleiben in
der payload-freien Summary sichtbar, statt unterdrückt zu werden. Ein
veränderter Stack, eine Connector-/libmodsecurity-Diagnose oder eine
Invalid-Access-Diagnose kann diese lokale Suppression nicht matchen und bleibt
ein fehlschlagendes Memcheck-Ergebnis.

Diese source-controlled Suppression wird nur im opt-in-Modus `NGINX_MEMCHECK=1`
verwendet, nachdem root die separate Worker-Identity und alle drei
Binary-/Archive-Identitätsgates verifiziert hat: Das ausgewählte
`NGINX_BINARY` entspricht `$NGINX_PREFIX/sbin/nginx`; die `nginx -v`-Ausgabe
lautet exakt `nginx version: nginx/1.31.2`; und
`$NGINX_BUILD_DIR/verified-archives/nginx-1.31.2.tar.gz` hat die
source-controlled SHA-256
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`.
Außerhalb des Memcheck-Modus behalten normale Harness-Aufrufe das bestehende
vom Aufrufer gewählte `NGINX_BINARY`-Override-Verhalten bei.

Diese erhaltene direkte H1-Diagnose bleibt Pre-Hardening und nicht kanonisch.
Kanonisches Provisioning und Lifecycle-Containment einschließlich der Worker-
sichtbaren Docroot-Projektion bleiben in Arbeit; daher belegt sie keinen Erfolg
für `runtime-smoke-nginx`, H2/H3, Remote-Rule, Remote-CI, SonarQube, Pull
Request oder Delivery. Der separate erhaltene Remediation-Beleg oben deckt
nur die Harness-/Evidence-Grenze mit einem `pre-current-C`-Artifact ab; er
ersetzt nicht den exakten finalen Security-Scan oder die finale PR-Head-
CI/Sonar-Evidence. Ein separater frischer C-Build validierte vorherigen C-Code,
nicht diese nicht kanonische historische Diagnose oder den kanonischen
Lifecycle.

## Scope-Abgrenzung

- [#388](https://github.com/owasp-modsecurity/ModSecurity-nginx/issues/388) ist
  für diese Parent-Adapter-Source-Aufnahme `not_applicable`.
- [PR #389](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/389)
  ist für diesen Parent-only-NGINX-Connector-Task `out_of_scope`.

## Dauerhafte Attributionsdateien

| Attributionspfad | Ursprünglicher Pfad | Repository | Commit | Lizenz | Importgrund |
| --- | --- | --- | --- | --- | --- |
| `licenses/nginx/LICENSE` | `LICENSE` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Lizenztext für von NGINX abgeleiteten Adapter-Quellcode |
| `licenses/nginx/AUTHORS` | `AUTHORS` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream-Attribution |
| `licenses/nginx/CHANGES` | `CHANGES` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | Apache-2.0 | Upstream-Änderungskontext |

## Ausgeschlossene Upstream-Dateien

Das NGINX-Test-Harness, `.git`, `.github`, CI-Dateien, Release-Skripte,
Windows-Build-Dateien, rohe Upstream-Tests und Build-/Runtime-Artefakte werden
nicht importiert. Insbesondere bleiben die Upstream-PR-#387-Dockerfiles, der
Workflow, die Valgrind-/Helgrind-Konfiguration und das Soak-Skript
upstream-only. Die früheren Upstream-Dateien `config` und `src/*` wurden
nach `connectors/nginx/src/` migriert; das frühere Verzeichnis
`connectors/nginx/upstream/` wurde entfernt, nachdem Smokes des materialisierten
NGINX-Quellcodes bestanden hatten.

## Zentrale Attributionskopien

Die Upstream-Dateien `LICENSE`, `AUTHORS` und `CHANGES` von NGINX werden unter
`licenses/nginx/` für die repositoryweite Lizenzprüfung gespiegelt. Das
zentrale Lizenzverzeichnis ist die dauerhafte Attributionsquelle; diese
Ursprungsübersicht zeichnet auf, wie diese Dateien zum adapter-eigenen
Quellbaum gehören.

## Bereinigungsprüfung

Der aktuelle [Connector-Integrationsleitfaden](../../modules/ModSecurity-test-Framework/docs/connector-integration.de.md)
des Frameworks dokumentiert die anwendbare Quell-/Kataloggrenze.

`connectors/nginx/upstream/` wurde in Phase 10 entfernt. Künftige
NGINX-Quellreduktionen sollten `connectors/nginx/SOURCE_MAP.json`,
`licenses/nginx/` und diese Ursprungsübersicht aktualisieren und dann
nachweisen, dass `smoke-nginx` und `smoke-all` weiterhin bestehen.
