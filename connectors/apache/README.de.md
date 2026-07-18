# Apache-Connector

**Sprache:** [English](README.md) | Deutsch


Status: Migration der Adapter-eigenen Quelle abgeschlossen

Dieses Verzeichnis ist für einen Apache-Adapter für libmodsecurity v3 reserviert.

Jetzt implementiert:

- Dokumentation beobachteter lokaler Apache-Connector-Konzepte.
- Adaptereigenes Apache-Connector-Layout unter `connectors/apache/`, mit
  Produktivquelle unter `connectors/apache/src/`.
- Gemeinsam genutzte Direktivennamen-Metadaten von `common/include/msconnector/directives.h`.
- Ein PoC-Build-Vorbereitungshelfer in `modules/ModSecurity-test-Framework/ci/provisioning/prepare-apache-build.sh`.
- Ein lokaler Runtime-Smoke-Harness unter `connectors/apache/harness/`.
- Verwendung aller gemeinsam genutzten Minimalfälle unter `modules/ModSecurity-test-Framework/tests/cases/`.
- Verwendung von aus der Quelle abgeleiteten, gemeinsam importierten Fällen, einschließlich rohem JSON-Text,
  einfachem mehrteiligem Textfeld und Response-Body-Allow-Control-Smokes.
- Bei einem historischen, von der lokalen Quelle erstellten httpd-Lauf wurde das von YAML erwartete HTTP beobachtet
  Status für alle aktuellen gemeinsamen Minimalfälle am 15.05.2026. Es ist nicht aktuell
  kanonische Phase-4-Facettenbeweise.

Nicht implementiert:

- Keine gepflegte Neufassung des Apache-Moduls über Pfadbesitz und Herkunft hinaus
  Migration.
- Kein Anspruch darauf, dass der Apache-Connector über die dokumentierte Freigabe hinaus vollständig ist
  minimaler/importierter Smoke-Test.
- Keine vollständige RESPONSE_BODY-Aktion. Phase-4- und Strict-Mode-Verkabelung auf Quellebene
  sind keine kanonischen Laufzeitbeweise.

## Unterstützte Anweisungen

Der adaptereigene Apache-Connector registriert derzeit Folgendes:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_use_error_log on|off`
- `modsecurity_transaction_id <string>`
- `modsecurity_transaction_id_expr <apache-expression>`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`
- `modsecurity_phase4_body_limit <bytes>`

`modsecurity_transaction_id` akzeptiert eine statische Zeichenfolge und behält die vorhandene bei
statische Semantik. `modsecurity_transaction_id_expr` akzeptiert eine Apache-Zeichenfolge
Ausdruck, zum Beispiel `%{REQUEST_URI}`, und wertet ihn pro Anfrage aus. Die beiden
Direktiven schließen sich im selben Apache-Kontext gegenseitig aus; normal
Untergeordnete Kontextüberschreibungen gelten während der Konfigurationszusammenführung. Wenn keine der Anweisungen festgelegt ist,
Wenn der Ausdruck einen leeren Wert ergibt oder fehlschlägt, bleibt der Connector bestehen
den vorhandenen `UNIQUE_ID`-Fallback und erstellt dann eine Transaktion ohne
explizite ID, wenn `UNIQUE_ID` nicht vorhanden oder leer ist.

`modsecurity_use_error_log off` unterdrückt die Weiterleitung von Apache-Fehlerprotokollen vom
Nur libmodsecurity-Protokollrückruf. Es ändert nichts an der Überwachungsprotokollierung.
Interventionsverhalten, Anfrage- oder Antwortbehandlung, Hooks, Filter, Buckets,
oder Transaktionseigentum.

Die Phase-4-Direktiven sind begrenzte Laufzeitsteuerungen. Insbesondere ist
`modsecurity_phase4_content_types_file` ein veralteter Kompatibilitätsparser:
Er kann das Apache-Pre-Commit-Gate für alle Responses nicht einschränken.
`SecResponseBodyMimeType` wählt stattdessen die libModSecurity-Inspektion.
Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft; Strict-Mode-Verkabelung auf
Quellebene beweist keinen späten Abbruch.

Primäre lokale Referenz: `<external-source-root>/ModSecurity-apache`.
Upstream-Quelle: https://github.com/owasp-modsecurity/ModSecurity-apache.

Das Build-Layout im Besitz des Apache-Adapters befindet sich unter `connectors/apache/` und ist
materialisiert zu `$BUILD_ROOT/apache-build/connector-src` vor Autotools/APXS
Builds laufen. Der frühere `connectors/apache/upstream/`-Baum wurde nach dem entfernt
Phase 11 materialisierte sich und der Apache-Smoke-Test verging. Phase 13 hält
`connectors/apache/src/` beschränkt auf produktive C-Quellen; Build-Dateien live unter
Das Connector-Stammverzeichnis, unter dem die Testvorlagen von Autotools gespeichert sind
`modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/`, und dauerhafte Namensnennung lebt darin
`licenses/apache/`, `connectors/apache/ORIGIN.md` und
`connectors/apache/SOURCE_MAP.json`.

Build- und Laufzeitartefakte müssen unter `BUILD_ROOT` bleiben, lokal standardmäßig auf
`/src/ModSecurity-conector-build`.

## Eigentums- und Laufzeitansprüche testen

Ausführbare Apache-Connector-Tests werden nicht im Framework-Modul verwaltet
unter `connectors/apache/tests`. Der lokale Connector-Testordner wurde entfernt
und darf nicht wieder eingeführt werden.

Relevante Framework-Pfade:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Historisch generierte Beweise bewahren Apache `partial` auf:

- Standard-Laufzeitrauch: `54/54 PASS`.
- Alle Laufzeitbeweise erzwingen: `133 Versuche / 100 PASS / 27 FAIL /
  0 BLOCKIERT / 6 NOT_EXECUTABLE`.

## Abdeckungs-/Laufzeit-Entscheidungsmatrix

Siehe den [kanonischen Apache-Guide](../../docs/connectors/apache.de.md) für
die Evidence-Grenze und die aktuelle Konfigurationsreferenz.

Apache bleibt derzeit `partial`: Standardrauch ist sauber, erzwingt alle Beweise
Zeichnet weiterhin FAIL- und NOT_EXECUTABLE-Zeilen auf, generierte Abdeckungsberichte jedoch nicht
automatische Laufzeithochstufung und RESPONSE_BODY bleibt nicht hochgestuft.

Siehe [Konfiguration](../../docs/configuration.de.md) und
`connectors/apache/harness/README.md`.

## Gemeinsame SDK-Einführungsgrenze

Der Apache-Connector bettet jetzt `msconnector_config` für Connector-Neutral ein
Konfigurationswerte, verwendet allgemeine Direktivennamen/Parser-Helfer für die
übernommene Richtlinien und enthält Apache-eigene Request/Response-Mapper-Fassaden
die von `request_rec` abgeleitete Metadaten anhand des Common Mappers validieren
Verträge. Phase-4-Metadatenereignisse werden nur über die allgemeinen Metadaten geschrieben
`msconnector_event` JSONL-Pfad; Nutzlasten für Anforderungs- und Antworttexte sind nicht vorhanden
in diese Ereignisaufzeichnungen geschrieben.

Apache-spezifischer Code verbleibt im Apache-Connector: `command_rec`
Registrierung, `request_rec` Zugang, Haken, Filter, APR-Pools, Eimerbrigaden,
APLOG-Protokollierung, Rückkehrcode-Zuordnung und APXS/Autotools-Build-Eingaben.

Diese Common SDK-Einführung erhebt keinen Anspruch auf Produktionsbereitschaft, CRS-Abdeckung,
vollständige Matrixabdeckung oder neues Laufzeitüberprüfungsverhalten.

## Kanonische Phase-4-Grenze

Der Apache-Ausgabefilter ist ein EOS-only-All-Response-Enforcement-Gate. Er
hängt jeden Daten-Bucket inkrementell an libModSecurity an und speichert die
normalisierte Apache-Brigade über Filteraufrufe hinweg im Request-Pool. Kein
ursprüngliches Response-Byte wird weitergegeben — auch nicht bei einer leeren
Response, die nur aus EOS besteht — bevor das erste EOS eingetroffen ist,
`msc_process_response_body` abgeschlossen und die Intervention aufgelöst ist.
Das tauscht sichtbares progressives Response-Streaming bewusst gegen eine
vollständige Phase-4-Entscheidung ein; es ist keine Regelauswertung pro Chunk.

Der Connector kann die wirksame `SecResponseBodyMimeType`-Auswahl von
libModSecurity über die C-API nicht sicher abfragen. Deshalb gate't er jeden
Response-MIME-Typ. `SecResponseBodyMimeType` wählt weiterhin die Engine-
Inspektion, während das veraltete
`modsecurity_phase4_content_types_file` keinen uninspektierten Pass-through-
Pfad erzeugen kann. Das Standardlimit von
`modsecurity_phase4_body_limit` beträgt 1048576 Byte (1 MiB). Eine Response,
die es überschreitet, schlägt fail-closed fehl, bevor ein ursprüngliches
Response-Byte freigegeben wird; sie wird nicht teilweise verarbeitet und dann
gestreamt.

An der normalen Entscheidungsgrenze sind Apaches `r->sent_bodyct` und
`eos_sent` kein Commit-Nachweis: Upstream-Module können sie setzen, bevor
dieser Filter etwas freigegeben hat. Das Gate verwendet stattdessen seinen
eigenen Released-EOS-Zustand und Apaches `r->bytes_sent`. Ein normaler
Phase-4-Deny verwirft die gespeicherte ursprüngliche Brigade, erhält den
relevanten P3-Response-Zustand und gibt genau eine terminale Error-Response
aus, bevor ursprüngliche Ausgabe freigegeben werden kann. Bei Allow wird die
zurückgehaltene Brigade einschließlich EOS genau einmal synchron weitergereicht
und der Terminal-Output-Guard versiegelt; dadurch kann ein späterer Producer
weder Body noch EOS doppelt ausgeben. Fehler beim Speichern, Anhängen oder
Abschließen der Response verwerfen die zurückgehaltene Brigade und schlagen
fail-closed fehl; ein tatsächlich nach Commit auftretender Fehler bricht die
Verbindung ab.

`log_only` im Safe-/Minimal-Modus und `abort_connection` im Strict-Modus sind
nur defensive Late-Intervention-Fallbacks, wenn ein unabhängiger Commit-
Nachweis bereits existiert. Sie deuten einen normalen, noch gegateten
Phase-4-Deny nicht zu Log-only um und entfernen den Deny-Pfad vor Release
nicht.

Ein normaler `r->prev`-interner Redirect, einschließlich eines ErrorDocument
vor Output, schlägt fail-closed fehl, weil eine Transaktion, die Quell-URI,
Header und Body verarbeitet hat, über die öffentliche libModSecurity-C-API
nicht sicher an ein anderes Target/Ruleset gebunden werden kann. Die einzige
Ausnahme ist genau ein synchroner, von Apache Core markierter lokaler
ErrorDocument-Hop, während der Terminal-Guard `EMITTING` ist; er erfordert den
Apache-Marker `no_local_copy` und einen zu `REDIRECT_STATUS` passenden Status
des unmittelbaren Vorgängers, und der Guard lässt keinen zweiten Hop zu. So
kann genau ein legitimer terminaler Error-Body
ausgegeben werden, ohne einen gewöhnlichen Redirect-Bypass zu öffnen.

Das eingecheckte Manifest deklariert die quellenverkabelten Phase-4- und
Late-Intervention-Facetten bis zu aktueller Real-Host-Evidence als
`implemented_not_asserted`. Der fokussierte H1/H2-Evidence-Platzhalter ist
`ci/runtime/lifecycle/run-apache-phase4-response-regression.sh`; erst nach der
Ausführung werden dessen laufbezogene Artefakte erfasst. Dieser Source-Contract
bezeichnet weder H1 noch H2 als bestanden.
