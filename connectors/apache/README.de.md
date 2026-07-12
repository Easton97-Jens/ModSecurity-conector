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
  Einfaches mehrteiliges Textfeld und Pass-Through-Smokes für den Antworttext.
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

Die Anweisungen der Phase 4 sind begrenzte Laufzeitsteuerungen. Phase 4 / RESPONSE_BODY
bleibt nicht befördert; Die Strict-Mode-Verkabelung auf Quellebene stellt keine Verbindung her
Ergebnis eines späten Abbruchs.

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

Siehe `docs/coverage-decision-matrix.md`.

Apache bleibt derzeit `partial`: Standardrauch ist sauber, erzwingt alle Beweise
Zeichnet weiterhin FAIL- und NOT_EXECUTABLE-Zeilen auf, generierte Abdeckungsberichte jedoch nicht
automatische Laufzeithochstufung und RESPONSE_BODY bleibt nicht hochgestuft.

Siehe `docs/connectors/directive-parity.md` und
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

Apache verwendet einen nativen httpd-Ausgabefilterpfad, der den aktuellen Bucket ausleiht.
leitet die aktuelle Brigade vor EOS weiter und beendet Phase 4 bei EOS.
Dabei handelt es sich um eine inkrementelle Aufnahme mit End-of-Stream-Auswertung, nicht pro Chunk
Regelauswertung. Das eingecheckte Manifest deklariert absichtlich
`response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata` als `implemented_not_asserted`.  Kein Strom
Kanonische Beweise für den realen Wirt fördern jede dieser Facetten.

`phase4_pre_commit_deny` ist bewusst `not_implemented`: die Körperentscheidung
wird bei EOS nach dem Antwort-Header-Pfad erstellt, sodass der native Host keinen hat
deterministischer, nicht festgeschriebener Antwortkörper-Entscheidungspunkt. Ein Verleugnungszweig in
Die Quelle ist keine Grundlage für den Anspruch auf eine sichtbare Phase-4-HTTP-Statusumschreibung.

Eine Phase-4-Regelübereinstimmung ist kein Beweis für einen für den Client sichtbaren 403. Ein kanonischer Fehler
Ereignis muss `original_http_status` behalten, angeforderter WAF-Status,
`visible_http_status`, `requested_action`, `actual_action`, Antwort-Commit
Metadaten und `connection_aborted` getrennt.  Vor der Zusage kann eine Ablehnung erfolgen
möglich; Nach der Festschreibung kann die gemeinsame Richtlinie nur noch `log_only` aufzeichnen
abgesicherten Modus oder `abort_connection` im strikten Modus.  Keines der beiden Ergebnisse kann sein
als erfolgreiche Pre-Commit-Verweigerung ohne übereinstimmende Host-Beweise gemeldet.

Die erforderlichen anwendbaren Fälle sind `phase4_rule_observed`,
`phase4_deny_after_commit_log_only`, `phase4_deny_after_commit_abort` und die
zwei Metadatenfälle. `phase4_deny_before_commit` bleibt hierfür unmarkiert
Host-Modell. Alle Fälle bleiben evidenzbasiert und werden nicht daraus abgeleitet
Quellenbeschreibung und Ereignisse enthalten nur Metadaten – niemals Antworttext
Nutzlasten.
