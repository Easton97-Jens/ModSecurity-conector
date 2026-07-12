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
- Über Umgebungen hinaus, in denen der NGINX-Smoke-Runner aktiv ist, wird kein Laufzeitdurchlauf beansprucht
  Beobachtet das von YAML erwartete echte HTTP-Verhalten für die freigegebenen YAML-Fälle.
- Es wird kein Anspruch auf eine vollständige Response-Body-Promotion erhoben. Phase 4 / RESPONSE_BODY bleibt bestehen
  nicht gefördert; Die Strict-Mode-Verkabelung auf Quellenebene ist keine kanonische Laufzeit
  Beweise.

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
- `modsecurity_phase4_body_limit <bytes>`

`modsecurity_transaction_id` verwendet einen komplexen NGINX-Wert und kann ihn auswerten
Variablen pro Anfrage. `modsecurity_transaction_id_expr` im Apache-Stil ist dies nicht
registriert für NGINX; Verwenden Sie `modsecurity_transaction_id` mit NGINX-Variablen
stattdessen. Die Anweisungen der Phase 4 sind begrenzte Laufzeitsteuerungen.
Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft; Strict-Mode-Verkabelung auf Quellenebene
stellt kein Ergebnis für einen späten Abbruch dar.

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

Der aktuelle NGINX-Common-Header-Build-Vertrag besteht aus:

```sh
MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include
```

`connectors/nginx/config` verwendet diesen Wert beim Erstellen der
NGINX-Include-Pfade.

Historisch beobachtet am 15.05.2026: `NGINX_RELEASE_TAG=latest` gelöst zu
`release-1.31.0`, gebaut `nginx/1.31.0`, gebaut
`ngx_http_modsecurity_module.so` und der Harness beobachteten die YAML-Erwartungen
HTTP-Status für alle aktuell freigegebenen Minimalfälle. Dies ist nicht aktuell kanonisch
Phase-4-Facettenbeweise.

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

Siehe `docs/coverage-decision-matrix.md`.

NGINX bleibt derzeit `partial`: Standardrauch ist sauber, erzwingt alle Beweise
Zeichnet weiterhin FAIL- und NOT_EXECUTABLE-Zeilen auf, generierte Abdeckungsberichte jedoch nicht
automatische Laufzeithochstufung und RESPONSE_BODY bleibt nicht hochgestuft.

Siehe `docs/connectors/directive-parity.md` für den aktuellen Apache/NGINX
Direktivenmatrix.

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

NGINX Common SDK-Modul-Builds, die einen kopierten Connector-Quellbaum verwenden, müssen `MSCONNECTOR_COMMON_SRC` (oder `CONNECTOR_COMMON_SRC` / `COMMON_SRC_ROOT`) auf das Stammverzeichnis der gemeinsamen Quelle des Repositorys setzen; `MSCONNECTOR_COMMON_INC` bleibt der Common-Include-Root. Wenn diese Option nicht festgelegt ist, greift die Konfiguration nur dann auf `$ngx_addon_dir/../../common/src` zurück, wenn dieser Pfad vorhanden ist.

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
