# Phase-4-Budget, native Fehler und NULL-Prüfungen

**Sprache:** [English](CR-20260920-phase4-all-connector-budget.md) | Deutsch

Change ID: `CR-20260920-phase4-all-connector-budget`
Datum: 2026-09-20
Basisrevision: `785a620de7b1c6b566a73eed642457eeb8419bb4`

## Motivation

Die gewünschte Budget-Regel gilt für alle Connector-Familien: Das zusätzliche
kumulierte Phase-4-Inspection-Budget greift nur in `safe` und `strict`; `off`
behält konfigurierte Engine-Inspection und native Fehlerbehandlung bei.
NGINX behandelt negative Interventionsergebnisse wieder wie vor Upstream-
PR #377. Fehlende NULL-Prüfungen und veraltete README-Aussagen werden korrigiert.

## Akzeptanzkriterien

Body-Planer und sekundäre Vertrags-/Vorprüfungen verwenden denselben Modus.
`off` kann mehr als das konfigurierte zusätzliche Inspection-Budget aufnehmen;
die Zähler bleiben geprüft. Aktive Budgets erlauben exakt die Grenze und
bewahren das bisherige Verhalten bei Überschreitung. Negative native Ergebnisse
rufen in NGINX `off` den `ngx_http_filter_finalize_request` mit
`NGX_HTTP_INTERNAL_SERVER_ERROR` auf. Fehlende Konfiguration wird nicht
dereferenziert. Unabhängige Engine-, Speicher-, Nachrichten-/Frame- und
Transportschutzmaßnahmen bleiben aktiv.

## Technische Entscheidungen

Ein reiner Common-Header liefert das effektive kumulierte Budget. `off`
verwendet `SIZE_MAX` nur als arithmetische Obergrenze, nie als Allokationsgröße.
Apache, HAProxy Native/HTX und Common Runtime verwenden ihn an den betreffenden
Prüfstellen. NGINX besitzt einen expliziten Off-Planer und eine entsprechende
Metadatenobergrenze. Common Runtime deckt direkte und Response-Companion-
Aufnahme ab. Die Go-Vorprüfung von Envoy liest eine optionale Capability der
geladenen Common Engine, nicht deren unabhängige Late-Action-Einstellung.
Die Content-Length-Vorprüfung des lighttpd-Streaming-Pfads folgt dem Modus;
die gepufferte Kapazitätsprüfung bleibt erhalten. `process_partial` kann
einen Zählerüberlauf in `off` nicht verbergen.

NGINX verwendet die frühere Finalisierung negativer Werte nur in `off`;
andere Integrationen behalten ihre bestehenden APR-/Common-/Host-Konventionen.
NULL-Prüfungen betreffen NGINX, Apache, Common-Logging und Traefik.
Bestehende Guards der Envoy-Bridge bleiben unverändert.

## Sicherheitsauswirkung

Absichtlich entfällt nur das zusätzliche kumulierte P4-Limit in `off`.
Engine-Inspection/-Einstellungen, native Fehler, Zählerüberläufe, Datei-
Metadaten-/Read-Prüfungen, feste Lesepuffer, Request-Budgets, begrenzte
Allokationen, gRPC-Chunk-Größen und Companion-Transportlimits bleiben erhalten.
Keine ununterstützte Response-Route oder Strict-Abort-Fähigkeit wird hochgestuft.

## Geänderte Dateien

- `common/include/msconnector/phase4_budget.h`
- `common/runtime/msconnector_runtime.c`
- `connectors/apache/README.de.md`
- `connectors/apache/README.md`
- `connectors/apache/src/msc_filters.c`
- `connectors/envoy/README.de.md`
- `connectors/envoy/README.md`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_budget.go`
- `connectors/envoy/ext_proc/internal/processor/phase4_budget_test.go`
- `connectors/envoy/ext_proc/internal/processor/processor.go`
- `connectors/haproxy/README.de.md`
- `connectors/haproxy/README.md`
- `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`
- `connectors/haproxy/src/haproxy_modsecurity_binding.c`
- `connectors/lighttpd/README.de.md`
- `connectors/lighttpd/README.md`
- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `connectors/nginx/README.de.md`
- `connectors/nginx/README.md`
- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `connectors/traefik/README.de.md`
- `connectors/traefik/README.md`
- `connectors/traefik/src/traefik_engine_service.c`
- `docs/phase4-mode-budget.de.md`
- `docs/phase4-mode-budget.md`
- `reports/audits/change-records/CR-20260920-phase4-all-connector-budget.de.md`
- `reports/audits/change-records/CR-20260920-phase4-all-connector-budget.md`
- `tests/test_nginx_phase4_mode_budget.py`
- `tests/test_phase4_all_connector_budget.py`
- `tests/test_phase4_envoy_budget.py`

## Tests und tatsächliche Ergebnisse

Über die Python-unittest-API in einem isolierten Quelltext-Arbeitsbereich
ausgeführt: `tests.test_nginx_phase4_mode_budget` und
`tests.test_phase4_all_connector_budget`: 30 Tests mit GCC bestanden; dieselben
30 mit Clang bestanden. Die C-Fixtures verwenden
`-std=c17 -Wall -Wextra -Werror`, tatsächlichen Helper-/Planer-/Branch-Code
und kleine Host-Doubles.
`tests.test_phase4_envoy_budget`: zwei Prüfungen bestanden, einschließlich
`go test -count=1 -v .` nur mit Standardbibliothek für tatsächlich extrahierte
Go-Funktionen und die hinzugefügten Go-Tabellentests. Das vollständige
Envoy-/CGo-Paket wird damit nicht gebaut.

Sieben Mutationskontrollen erzeugten jeweils einen erwarteten Assertion-Fehler:
gemeinsames Off-Budget, frühere NGINX-Finalisierung negativer Werte, sekundäres
NGINX-Metadatenbudget, sekundäres Apache-Metadatenbudget, HAProxy-HTX-Vorprüfung,
sekundäres Common-Runtime-Metadatenbudget und kumulierte Envoy-Vorprüfung.
Nach Wiederherstellung bestanden die finalen Tests erneut. Dies sind sieben
Kontrollen, nicht sieben Produktionsfehler.

Neue Patch-Zeilen enthalten keinen abschließenden Leerraum. Ein eigenständiger
Python-Validator im Lieferpaket prüft Diff-Kontexte und rekonstruierte
Dateihashes; damit wird kein ausgeführtes natives `git apply --check` behauptet.

## Laufzeitnachweise

Keine von laufenden NGINX-, httpd-, HAProxy-, Envoy-, Traefik- oder lighttpd-
Servern. Kein Erfolg für HTTP/1, HTTP/2, HTTP/3, Produktion, Sanitizer oder
Integration mit der echten Engine wird behauptet.

## Nicht ausgeführte Prüfungen

Repository-native RTK-verpackte Make-Prüfungen, vollständige Host-Builds,
vollständige Go-/CGo-Pakettests, komplette Regressionstests, kanonische
Bilingual-/Link-Prüfungen, CI des neuen Stands und SonarCloud. RTK und die native
Host-Umgebung waren nicht verfügbar. Keine Pakete/Toolchains wurden installiert
und keine Abhängigkeiten verändert.

## Bekannte Einschränkungen

Das Quellarchiv stammt von `da9b0bf7e06df77cc93ba45371454042740c5dd3`.
Alle neun geänderten vorhandenen produktiven Quelldateien wurden unabhängig
gegen GitHub-Blobs der gewählten Basis bytegenau geprüft. Die acht README-
Migrationsdeltas aus PR #380 bleiben in der Patch-Basis erhalten. Das ursprüngliche
Archiv wird nicht als vollständig aktueller Checkout dargestellt.
Die Vorbereitung lieferte zunächst ein lokales Änderungspaket. Dieser
Branch veröffentlicht die Quelldateien zum Draft-Review; CI des aktuellen
Stands und vollständige Host-Validierung bleiben separate Prüfungen. Dies ist
keine integrierte Änderung.

## Restrisiken

Host-spezifische Integration und Error-Page-Verhalten benötigen native
Regressionstests. Ein puffernder Kompatibilitätspfad kann eine zu große Response
auch in `off` wegen seiner unabhängigen Speichergrenze ablehnen.
Ununterstützte Strict-Abort-Profile bleiben ununterstützt. Framework/MRTS und
CI-/Sicherheitsgates werden nicht verändert.

## Abschließender Review-Status

Begrenzter Quelltext-Diff geprüft; isolierte Prüfungen bestanden bei der
Vorbereitung. Die Quelldateien werden zum Draft-Review eingereicht. Der PR
dokumentiert den aktuellen Head und CI-Stand; ein Merge oder eine
Produktionsfreigabe wird hier nicht behauptet.
