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
| `connectors/nginx/src/ngx_http_modsecurity_body_filter.c` | `src/ngx_http_modsecurity_body_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac`; PR #384 `65de4cd8739209f22d924d85548bd012a4d94607`; PR #385 `471a2a54843bb8f560758a7e75b146db2243ab29`; PR #386 `a7fd4fcc18dc442b1b093d253f457b9317b7f588`; Parent FND-PARENT-0080 | Apache-2.0 | NGINX-Integration für Response-/Body-Filter plus Phase-4-, Final-Processing-, Redirect-Body-Replacement-, Terminal-Loop-Behandlung und wiederhergestellte begrenzte Aufnahme vor dem Connector-Scope-Action-Mapping |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | `src/ngx_http_modsecurity_common.h` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac`; PR #385 `471a2a54843bb8f560758a7e75b146db2243ab29` | Apache-2.0 | Gemeinsame NGINX-Connector-Deklarationen plus Phase-4-Felder und Response-Replacement-State |
| `connectors/nginx/src/ngx_http_modsecurity_header_filter.c` | `src/ngx_http_modsecurity_header_filter.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #384 `65de4cd8739209f22d924d85548bd012a4d94607`; PR #385 `471a2a54843bb8f560758a7e75b146db2243ab29`; PR #386 `a7fd4fcc18dc442b1b093d253f457b9317b7f588` | Apache-2.0 | NGINX-Header-Filter-Integration plus ausgewählte Intervention-, Protocol-/Header-, Redirect- und Registration-Härtung |
| `connectors/nginx/src/ngx_http_modsecurity_log.c` | `src/ngx_http_modsecurity_log.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | none | Apache-2.0 | NGINX-Integration in der Log-Phase |
| `connectors/nginx/src/ngx_http_modsecurity_module.c` | `src/ngx_http_modsecurity_module.c` | ModSecurity-nginx | `9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846` | PR #377 `3d72b004ff27a78ea19c6b945870e2cae62a97ac`; PR #384 `65de4cd8739209f22d924d85548bd012a4d94607`; PR #385 `471a2a54843bb8f560758a7e75b146db2243ab29` | Apache-2.0 | NGINX-Modul-Einstiegspunkt/Konfiguration plus Phase-4-Direktiven, Transaction-Lifecycle- und Redirect-Response-Behandlung |
| `connectors/nginx/src/ddebug.h` | `src/ddebug.h` | repository-eigener Kompatibilitäts-Header | n/a | ersetzt importierten Upstream-Debug-Helper | Apache-2.0-kompatibler Projektcode | Hält die NGINX-Modul-Build-Abhängigkeit erfüllt, ohne den importierten Debug-Helper in `upstream/` aufzubewahren |
| `connectors/nginx/metadata.c` | n/a | repository-eigene Adapter-Metadaten | n/a | none | Apache-2.0-kompatibler Projektcode | Ursprungsmetadaten für Report-/Build-Zusammenfassungen |
| `connectors/nginx/metadata.h` | n/a | repository-eigene Adapter-Metadaten | n/a | none | Apache-2.0-kompatibler Projektcode | Ursprungsmetadaten für Report-/Build-Zusammenfassungen |
| `connectors/nginx/SOURCE_MAP.json` | n/a | repository-eigenes Provenienzmanifest | n/a | zeichnet Basis, PR #377, ausgewählte PRs #384--#386, die abgegrenzte Disposition von #387/#388/#389 sowie Parent-/Finding-Evidenzgrenzen auf | Apache-2.0-kompatible Projektmetadaten | Quellmigrations- und PR-Provenienzübersicht |

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
| [PR #385](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/385) | `471a2a54843bb8f560758a7e75b146db2243ab29` | Wählt Response-Header-Fidelity und Phase-3-Redirect-Replacement: `Location` bleibt erhalten, verworfene Entity-Metadaten werden gelöscht und der ersetzte Body wird verworfen. Der Parent-Task unterdrückt zusätzlich fiktive synthetische `Connection`-/`Keep-Alive`-Header für natives HTTP/3 neben dem ausgewählten Negotiated-Protocol-Mapping; dies ist task-lokale Härtung, keine Live-HTTP/3-Evidence. |
| [PR #386](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/386) | `a7fd4fcc18dc442b1b093d253f457b9317b7f588` | Wählt wertfreie Warning-Sichtbarkeit für Header-Registration-Fehler, Empty-Address-Guards und einen terminalen Body-Filter-Stopp, der die verbleibende NGINX-Chain weiterleitet. |
| [PR #387](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/387) | `4c1f0362ca0f25ef216ce59cad5fa6c9703c1438` | Wählt die Test-Design-Richtung für einen Parent-eigenen opt-in bounded native soak (`make soak-nginx`) und eine opt-in H1-Memcheck-Diagnose (`make memcheck-nginx`) über den vorhandenen Harness. Beide bleiben außerhalb von Default-Smoke/Test/CI und schreiben begrenzte payload-freie Summaries. Der source-gesteuerte Soak-Selektor lässt zwischen einer und acht eindeutige IDs aus seinem expliziten kanonischen Katalog zu und weist leere, doppelte oder außerhalb des Katalogs liegende Selektionen vor der Case-Discovery ab. Upstream-Dockerfiles, Workflows, Valgrind-/Helgrind-Konfiguration und Soak-Tooling werden nicht importiert. Die direkte H1-Diagnose nach der Suppression unten ist nur innerhalb ihres begrenzten nicht kanonischen Scopes clean; es wird kein kanonischer Memcheck-, Helgrind- oder Soak-Erfolg behauptet. |

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

### Direkte H1-Memcheck-Evidenz und lokale Suppression

Die initiale direkte H1-Valgrind-Memcheck-Diagnose beobachtete eine 8-Byte-
`definitely-lost`-NGINX-Core-Worker-Exit-Allocation. Das ist kein Connector-
oder ModSecurity-Sicherheitsfinding. Der exakt generierte Stack wurde gegen ein
unabhängig SHA-verifiziertes offizielles `nginx-1.31.2`-Archiv geprüft
(beobachtetes SHA-256-Präfix/-Suffix `af2a957...473c`).

Das begrenzte direkte H1-O7-Artifact nach der Suppression
`direct-nginx-h1-memcheck-suppressed-20260801T234500Z-c8d9e0f1` ist nur
innerhalb dieser direkten Diagnosegrenze clean: `status=clean`, `complete=1`,
`errors_detected=0`, `error_count=0`, `definitely_lost_bytes=0`,
`indirectly_lost_bytes=0`, `possibly_lost_bytes=28160` und
`still_reachable_bytes=329918`. Der ausgewählte Connector-geladene gutartige
Fall schloss `48` Requests mit `request_failures=0`,
`worker_summary_failures=0` und `server_alive=1` ab. Der isolierte Lifecycle
zeichnete `shutdown=graceful`, `wait=exited`, `wrapper_exit_code=0` und
`containment=isolated` auf; es blieben kein NGINX- oder Valgrind-Prozess,
keine `nginx.pid` und keine Testport-Bindung zurück.

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
verwendet, nachdem alle drei Laufzeit-Identitätsgates bestanden sind: Das
ausgewählte `NGINX_BINARY` entspricht `$NGINX_PREFIX/sbin/nginx`; die
`nginx -v`-Ausgabe lautet exakt `nginx version: nginx/1.31.2`; und
`$NGINX_BUILD_DIR/verified-archives/nginx-1.31.2.tar.gz` hat die
source-controlled SHA-256
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`.
Außerhalb des Memcheck-Modus behalten normale Harness-Aufrufe das bestehende
vom Aufrufer gewählte `NGINX_BINARY`-Override-Verhalten bei.

Diese direkte H1-Diagnose bleibt nicht kanonisch. Kanonisches Provisioning und
Lifecycle-Containment einschließlich der Worker-sichtbaren Docroot-Projektion
bleiben in Arbeit; daher belegt dieses direkte Ergebnis keinen Erfolg für
`runtime-smoke-nginx`, H2/H3, Remote-Rule, Remote-CI, SonarQube, Pull Request
oder Delivery.

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
