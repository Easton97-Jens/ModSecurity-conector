# Plan zum Ersetzen und Reduzieren

**Sprache:** [English](replace-and-reduce-plan.md) | Deutsch

Status: Phase 12 der Apache-Quellenbereinigung abgeschlossen

Dieser Plan erfasst Kandidaten für den Ersatz kleiner importierter Anschlussquellen
Stücke mit Repo-eigenem Code. Ein Ersatz ist nur zulässig, wenn er dies vermeidet
Server-hook/filter/body/lifecycle-Semantik und sorgt dafür, dass Smoke aus der realen Welt weitergeht.

## Kandidatenentscheidungen

| Kandidat | Quelle | Risiko | Smokeabdeckung | Ersatzstrategie | Entscheidung |
| --- | --- | --- | --- | --- | --- |
| NGINX-Debug-Kompatibilitätsmakros | `connectors/nginx/upstream/src/ddebug.h` | Niedrig. Das Standardverhalten sind No-Op-Debug-Makros; Es wird als Build-Abhängigkeit aufgeführt, besitzt jedoch keine Requests-, Antwort-, Transaktions- oder Textsemantik. | Kompilierung des NGINX-Moduls plus vollständiges Apache/NGINX `smoke-all`; Debug-fähige Builds bleiben eine zukünftige explizite Prüfung. | Fügen Sie `connectors/nginx/src/ddebug.h` hinzu, das dem Repo gehört, kopieren Sie es nur dann in den generierten NGINX-Connector-Build-Baum, wenn in der kopierten Quelle `src/ddebug.h` fehlt, und entfernen Sie dann die importierte Upstream-Kopie. | Jetzt ersetzen |
| Apache-Fehler-Bucket-Helfer | `connectors/apache/src/msc_utils.c` `send_error_bucket()` | Hoch. Es erstellt Apache-Buckets, legt die Statuszeile fest und beeinflusst das Antwortverhalten der Filterkette. | Wird indirekt durch das Blockieren von Smokes abgedeckt, aber ein Ersatz würde die Apache-Ausgabesemantik beeinträchtigen. | Bleiben Sie im Besitz des Adapters, aber connectorspezifisch. Erneuter Besuch nur bei Anzeichen von Smoke. | verschieben |
| Apache `id()`-Helfer | `connectors/apache/src/msc_utils.c` | Geringes Coderisiko, aber kein funktionaler Ersatzbedarf; Durch die Entfernung würde der Code des Apache-Dienstprogramms ohne Verhaltensgewinn bearbeitet. | Nicht sinnvoll abgedeckt, da es unbenutzt erscheint. | Belassen Sie die Apache-Quelle im Besitz des Adapters, bis ein dedizierter Bereinigungsnachweis keine build/runtime-Auswirkung zeigt. | aufschieben / möglicherweise veraltet |
| Handhabung von Apache-Eingriffen | `connectors/apache/src/mod_security3.c` | Hoch. Übersetzt libmodsecurity-Eingriffe in Apache HTTP-Verhalten und Weiterleitungen. | Wird von vielen 403/401/302-Räuchern abgedeckt, aber das Verhalten ist Produktionspfad. | Nur Dokument. Die Form „Daten extrahieren“ wird bereits durch allgemeine Metadaten-Helfer dargestellt. | verschieben |
| NGINX-Interventionsbehandlung | `connectors/nginx/src/ngx_http_modsecurity_module.c` | Hoch. Verbunden mit der Finalisierung von NGINX-Anfragen, Umleitungsheadern, früher Protokollierung und Statusaktualisierungen. | Wird von vielen blocking/redirect-Räuchern abgedeckt, aber das Verhalten ist Produktionspfad. | Bleiben Sie im Besitz des Adapters, aber connectorspezifisch. Keine gemeinsame Extraktion, bis ein dediziertes NGINX-Adapterdesign vorhanden ist. | verschieben |
| NGINX-Protokollrückruf | `connectors/nginx/src/ngx_http_modsecurity_log.c` | Mittel bis hoch. Die Connector-spezifische Protokollphase und das Prüfverhalten werden weiterhin aktiv nachverfolgt. | Audit-Log-Smokes decken stabile Felder ab, aber `nolog` bleibt früherer erwarteter Fehler. | Bleiben Sie im Besitz des Adapters, aber connectorspezifisch. | verschieben |
| Rules/config wird geladen | Apache `src/msc_config.*`, NGINX `src/ngx_http_modsecurity_module.c` | Hoch. Serverspezifisches Parsen der Konfiguration und Besitz des libmodsecurity-Regelsatzes. | Build- und Smoke-Setup hängen davon ab. | Connectorspezifisch bleiben. | verschieben |
| Request/response-Filter | Apache-Filter, NGINX access/header/body-Filter | Hoch. Besitzt direkt den Verbindungsdatenpfad und `RESPONSE_BODY` bleibt der ehemalige expected-failure/mapped-only. | Smoke in der realen Welt deckt aktive Variablen ab, aber das Blockieren des Response Bodys der Phase 4 ist kein stabiler allgemeiner PASS. | Bleiben Sie Upstream. | verschieben |

## Phase 4 Austausch

Der einzige Phase-4-Ersatz ist der NGINX-Debug-Kompatibilitätsheader. Der
Der Repo-eigene Header ist adapternah und nicht Common C. Er existiert, um den Import zu reduzieren
Referenzfläche ohne Kontakt zum Runtimeverhalten des Connectors.

Das Build-Skript kopiert den Repo-eigenen Header nur dann in `$BUILD_ROOT`, wenn der
Der ausgewählte Quellbaum des NGINX-Connectors stellt `src/ddebug.h` noch nicht bereit.
Dadurch bleiben explizite externe `MODSECURITY_NGINX_SOURCE_DIR`-Builds kompatibel
mit eigenem Upstream-Header.

## Phase 9 NGINX-Quellmigration

Phase 9 verschiebt das verbleibende NGINX-Modul `config` und die Quelldateien aus dem
Upstream-Referenzbaum in den adaptereigenen `connectors/nginx/src/`. Das ist ein
größere Build-Input-Besitzänderung als beim `ddebug.h`-Ersatz der Phase 4,
aber es handelt sich immer noch nicht um eine Common-Extraktion und es werden keine Hooks, Filter usw. zusammengeführt.
Körperhandhabung, Interventionssemantik oder Transaktionseigentum übergreifend
Anschlüsse.

| Kandidat | Quelle | Risiko | Testabdeckung | Ersatzstrategie | Entscheidung |
| --- | --- | --- | --- | --- | --- |
| Quellbaum des NGINX-Moduls | `connectors/nginx/upstream/config`, `connectors/nginx/upstream/src/*` | Medium. Bei den Dateien handelt es sich um produktiven Connector-Code, daher besteht die sichere Verschiebung nur im Besitz des Pfads und nicht im semantischen Umschreiben. | Frischer NGINX-Build aus materialisierten Quellen plus realer NGINX-Smoke; Mischrauch bleibt weiterhin erforderlich. | Verschieben Sie Dateien nach `connectors/nginx/src`, behalten Sie die Herkunft in `SOURCE_MAP.json` bei, materialisieren Sie adaptereigene Dateien in `$BUILD_ROOT/nginx-build/connector-src` und entfernen Sie Upstream-Kopien erst nach dem Smoke Pass. | Jetzt ersetzen |
| ModSecurity-nginx PR #377 Phase-4-Änderungen | PR #377 Körper filter/common header/module Quelle | Medium. Es betrifft Phase-4/spätes Interventionsverhalten. | Nur anwenden, wenn die NGINX-Quelle im Besitz des Adapters kompiliert wird und `smoke-nginx` erfolgreich ist. `probe-response-body` ist weiterhin evidenzbasiert. | Wenden Sie Quelländerungen separat auf Dateien an, die sich im Besitz des Adapters befinden, und dokumentieren Sie den Status des Response Bodys separat. | Quelle anwenden, keine `RESPONSE_BODY`-Werbung |

## Phase 10 NGINX Upstream-Referenzentfernung

In Phase 10 werden die verbleibenden `connectors/nginx/upstream/`-Namensnennungen entfernt
Baum. Dies ist kein Runtimeersatz: Die produktive NGINX-Quelle war bereits aktiv
unter `connectors/nginx/src` und die materialisierte Build-Quelle war bereits
generiert unter `$BUILD_ROOT/nginx-build/connector-src`.

| Kandidat | Quelle | Risiko | Testabdeckung | Ersatzstrategie | Entscheidung |
| --- | --- | --- | --- | --- | --- |
| NGINX verbleibende Upstream-Referenzdateien | `connectors/nginx/upstream/{LICENSE,AUTHORS,CHANGES,README.md}` | Niedrig, wenn die Zuordnung vollständig bleibt. Nach Phase 9 handelt es sich nicht mehr um Build-Inputs. | NGINX materialisierter Build, `smoke-nginx` und kombinierter `smoke-all`; Das Manifest darf keine NGINX `upstream-derived`-Einträge enthalten. | Entfernen Sie den lokalen Upstream-Baum und behalten Sie die dauerhafte Zuordnung in `licenses/nginx/`, `connectors/nginx/ORIGIN.md` und `connectors/nginx/SOURCE_MAP.json` bei. | Jetzt entfernen |

## Phase 11 Apache-Quellmigration

Phase 11 verschiebt die Apache-Quelle, die Autotools/APXS-Eingaben und das erforderliche `.in`
Vorlagen aus dem Upstream-Referenzbaum in Adapter-eigene Vorlagen
`connectors/apache/src/`. Hierbei handelt es sich um eine Build-Input-Besitzänderung, nicht um eine
Verhalten umschreiben. Apache-Haken, Filter, Eimerbrigaden, request/response
Verarbeitung, Interventionsübersetzung, Transaktionseigentum und
Das Verhalten von `RESPONSE_BODY` bleibt Apache-spezifisch.

| Kandidat | Quelle | Risiko | Testabdeckung | Ersatzstrategie | Entscheidung |
| --- | --- | --- | --- | --- | --- |
| Apache-Modulquelle und Autotools-Baum | `connectors/apache/upstream/{autogen.sh,configure.ac,Makefile.am,build/*,src/*,tests/**/*.in,t/conf/extra.conf.in,LICENSE,AUTHORS,CHANGES}` | Medium/high, da das Autotools/APXS-Layout und die Apache-Filter produktiver Code sind, sodass der sichere Umzug nur der Pfadbesitz ist. | Frisch materialisierter Apache-Build plus realer Apache-Smoke; Mischrauch bleibt weiterhin erforderlich. | Verschieben Sie Dateien nach `connectors/apache/src`, behalten Sie die Herkunft in `SOURCE_MAP.json` bei, materialisieren Sie adaptereigene Dateien in `$BUILD_ROOT/apache-build/connector-src` und entfernen Sie Upstream-Kopien erst nach dem Smoke Pass. | Jetzt ersetzen |

## Phase 12 Apache-Quellenbereinigung

Phase 12 entfernt nur attribution/history/documentation-only-Dateien aus
`connectors/apache/src/`. Die erforderliche Autoconf-Quellenprüfung bleibt erhalten
Verschieben von `AC_CONFIG_SRCDIR` von `LICENSE` in die funktionale Quelldatei
`src/mod_security3.c`. Es wird kein Apache utility/runtime-Helfer ersetzt.

| Kandidat | Quelle | Risiko | Testabdeckung | Ersatzstrategie | Entscheidung |
| --- | --- | --- | --- | --- | --- |
| Apache attribution/history/docs-Dateien | `connectors/apache/src/{AUTHORS,CHANGES,LICENSE,README.md}` | Niedrig nach Änderung des Autoconf-Quellankers. Diese Dateien werden zur Runtime nicht kompiliert oder geladen. | Frisch materialisierter Apache-Build plus `smoke-apache`; Mischrauch bleibt weiterhin erforderlich. Das Manifest darf die entfernten Dateien nicht enthalten. | Entfernen Sie Duplikate im Quellbaum und behalten Sie die Zuordnung in den verschobenen Metadaten `licenses/apache/`, `connectors/apache/ORIGIN.md` und `SOURCE_MAP.json` bei. | Jetzt entfernen |
| Apache `id()`-Helfer in `src/msc_utils.c/.h` | Wenig Code, aber kein Verhaltensersatz erforderlich. | Vorhandene Smokeer üben es nicht aus, da keine Anrufer gefunden wurden. | Dokument als obsolete/deferred. | Bearbeiten Sie die Runtimequelle in dieser Bereinigungsphase nicht. | verschieben |
| Apache `send_error_bucket()` in `src/msc_utils.c` | Hoch. Es besitzt das Antwortverhalten von Apache bucket/error. | Blockierende Smokewolken decken Symptome ab, nicht jede Ausgangsfilterkante. | Connectorspezifisch bleiben. | Kein Ersatz in dieser Phase. | verschieben |

## Überprüfung der Phase 5

In Phase 5 wurde nach einem weiteren Ersatz mit geringem Risiko gesucht. Kein zweiter Kandidat
erfüllt die Ersetzungsregel: Jeder verbleibende Helfer ist entweder in a eingebettet
Produktionspfad request/response, gebunden an serverspezifischen config/lifecycle, oder
erfordert die Bearbeitung einer importierten Quelldatei, ohne dass ein funktionaler Ersatz erforderlich ist.

| Kandidat | Risiko | Abhängigkeiten | Auswirkungen auf die Runtime | Wirkung aufbauen | Testabdeckung | Entscheidung |
| --- | --- | --- | --- | --- | --- | --- |
| Apache `id()`-Helfer in `src/msc_utils.c/.h` | Niedrig als Code, aber unsicher als Ersetzungsziel, da beim Entfernen ein importiertes source/header-Paar bearbeitet wird, das auch Apache-Error-Bucket-Deklarationen besitzt. | C stdio/varargs und `msc_utils.h`; Es wurden keine Anrufer außerhalb des eigenen declaration/definition. gefunden | Keine bekannte Runtimenutzung. Das Entfernen würde das Verhalten nicht ersetzen; es würde nur den Upstream-Referenzcode mutieren. | Der Apache-Build toleriert möglicherweise das Entfernen, für den Nachweis wäre jedoch die direkte Bearbeitung der importierten Dateien erforderlich. | Keine sinnvolle Smokeabdeckung, da der Helfer unbenutzt ist. | veraltet / aufgeschoben |
| Apache `send_error_bucket()` in `src/msc_utils.c` | Hoch. Es erstellt Apache-Buckets, legt die Statuszeile fest, fügt EOS ein und leitet die Brigade entlang der Ausgabefilterkette weiter. | Apache request/filter/bucket-APIs und `msc_filters.c`-Fehlerpfade. | Direkte Apache response/error-Semantik. | Erforderlich für `msc_filters.c`; Für die Entfernung ist eine Repository-eigene Apache-Adapter-Implementierung erforderlich. | Blockierende Smokes decken Symptome ab, nicht jede Apache-Ausgangsfilterkante. | verschieben |
| NGINX `ngx_str_to_char()` in `src/ngx_http_modsecurity_module.c` | Mittel bis hoch. Es ist klein, wird aber zum Parsen von Konfigurationen und zum Zuordnen von Requestsmetadaten verwendet. | NGINX-Pools, `ngx_str_t`, Zuordnungsfehler-Sentinel, Konfigurations- und Zugriffshandleraufrufer. | Fordern Sie die Konvertierung von Metadaten und Konfigurationswerten an. | Wird in `ngx_http_modsecurity_common.h` verfügbar gemacht und über mehrere Modulquellen hinweg verwendet. | Aktive Smokes decken allgemeine Requestsmetadaten ab, jedoch nicht alle allocation/config-Randfälle. | verschieben |
| NGINX PCRE-Pool-Helfer in `src/ngx_http_modsecurity_module.c` | Hoch. Sie ersetzen vorübergehend PCRE-Zuweiser beim Laden von Regelsätzen. | NGINX-Pool-Lebenszyklus, globale PCRE-Allokator-Hooks, Laden von rules/config. | Config/lifecycle-Verhalten statt Datenpfad anfordern, aber ein Fehler könnte das Laden der Regeln destabilisieren. | Erforderlich für die Initialisierung der Modulkonfiguration. | Build und Smoke Evidencen, dass normale Regeln geladen werden, nicht Allokator-Edge-Fälle. | verschieben |
| NGINX-Response-Header-Resolver-Helfer in `src/ngx_http_modsecurity_header_filter.c` | Hoch. Sie normalisieren Antwortheader für libmodsecurity. | NGINX-Header-Filter-API, Antwort-Header-Strukturen, Filterreihenfolge. | Direkter Antwortpfad metadata/filter. | Erforderlich für die NGINX-Header-Filterquelle. | `response_header_basic` deckt einen echten Pfad ab; reicht nicht aus, um das gesamte Resolververhalten zu ersetzen. | verschieben |
| NGINX-Protokollrückruf in `src/ngx_http_modsecurity_log.c` | Mittel bis hoch. Das Verhalten von Audit/log ist evidenzsensitiv und `nolog` bleibt früherer erwarteter Fehler. | NGINX-Protokollierung, libmodsecurity-Protokollrückruf, Transaktionskontext. | Audit/log-Ausgabesemantik. | Erforderlich für die Protokollhandlerquelle. | Es gibt stabile Prüfungsfelder, aber die Abwesenheit von Prüfungen unterscheidet sich je nach Umgebung. | verschieben |

Das Ergebnis der Phase 5 ist daher eine dokumentierte Sperre. Der nächste Ersatz sollte
Beginnen Sie erst, nachdem eine Repo-eigene Adapterdatei für ein enges Verhalten vorhanden ist und
before/after Smoke aus der realen Welt Evidencet die Gleichwertigkeit.

## Phase-6-Adapterskelette

Phase 6 ersetzt keinen zusätzlichen Upstream-Runtimehelfer. Es fügt hinzu
Adaptereigene Metadatenskelette unter `connectors/apache/src/` und
`connectors/nginx/src/`, damit zukünftige Ersetzungs- und Reduzierungsarbeiten klar sind
Repo-eigene Landezone.

Diese Metadatendateien dienen vorerst nur der Validierung. Sie ändern weder Build noch
Runtimeverhalten für Apache- oder NGINX-Connector-Module. Das einzig validierte
Vorgeschaltete Oberflächenreduzierung bleibt der NGINX `ddebug.h`-Ersatz
Phase 4.
