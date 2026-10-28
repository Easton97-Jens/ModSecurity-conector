# MRTS-Paketanbindung

**Sprache:** [English](mrts-package-integration.md) | Deutsch

Der native MRTS-Aufrufer verwendet die Framework-Paketschnittstelle unter
`ci/provisioning/mrts-package.py`. MRTS bleibt ein gepinnter, schreibgeschützter
Generator: Dieser Auftrag ändert weder MRTS-Quellen noch einen der beiden
Repository-Gitlinks. Der allgemeine Testumzug bleibt ein eigener Auftrag.

## Vorbereitung und private Übergabe

Explizite Pfade für `FRAMEWORK_ROOT`, `MRTS_ROOT`, `CONNECTOR_ROOT` und einen
externen `BUILD_ROOT` übergeben. Das Framework-CLI unterstützt `prepare`,
`verify` und `materialize`, jeweils mit `--framework-root`, `--mrts-root`,
`--connector-root`, `--build-root`, `--package-root` und
`--include-feature-demo 0|1`. Alle Aktionen akzeptieren
`--upstream-definitions` und `--feature-demo-definitions`; der native Aufrufer
gibt gesetzte `MRTS_UPSTREAM_DEFINITIONS` und `MRTS_FEATURE_DEMO_DEFINITIONS`
konsistent weiter. `materialize`
verlangt zusätzlich einen neuen `--output-root` unter `--build-root` und
akzeptiert `--port` für das private Requestziel.

Das Framework führt Generierung, strengen Import/Validierung und `mrts.load`
vor der Veröffentlichung im Staging aus. Sein Manifest bindet Revisionen,
ausgewählte Korpora, eindeutige Fall-IDs, Definitionen, Artefakthashes und
Vorbereitungsstatus. Demo-Flag `0` schließt optionale Demo-Generierung und
strengen Import aus; Flag `1` validiert Demoinhalte und Regel-ID-Kollisionen.
Numerische Headernamen und YAML-Sonderstrings behalten ihren Typ bei Import
und Materialisierung.

`run-mrts-native-full.sh` bereitet pro Aufruf ein Paket vor und prüft es vor
der Wiederverwendung durch ein weiteres Ziel. Bei
`MODSECURITY_MRTS_PREPARED=1` ist ein expliziter `MRTS_PACKAGE_ROOT` erforderlich
und wird geprüft; das Flag allein reicht nicht. Das Standardpaket liegt in
einem neuen privaten Unterverzeichnis von `MRTS_BUILD_ROOT`.
Jedes Ziel erhält `$MRTS_NATIVE_ROOT/<target>/package`; FTW-Ports und Load-Pfade
gehören zu dieser Kopie. Das gemeinsame Paket bleibt unverändert. Fehler bei
Vorbereitung oder Materialisierung stoppen das Ziel vor der Hostausführung.
Der native Runner kombiniert nur ausgewählte private FTW-Unterbäume unter
`<target>/selected-ftw/<corpus>` und bindet jede ausgewählte Korpus-Load-Datei
ein; korpusspezifische Zähler und Ergebnisse bleiben im Ergebnis-JSON erhalten.

## Ergebnisintegrität und Ausgabe

Natives go-ftw verwendet `--output json --file <target>/go-ftw.json`. Der
gemeinsame Framework-Ergebnisleser zählt explizite Ergebnisse für eindeutige
ausgewählte FTW-Fall-IDs: Auswahl, Ausführung, PASS, FAIL, übersprungene,
ignorierte, erzwungene und fehlende Ergebnisse. Doppelte/widersprüchliche IDs,
unbekannte Ergebnisse und inkonsistente Summen sind Fehler; erzwungenes PASS
ist kein beobachtetes Runtime-PASS. Ein erfolgreicher Prozessabschluss ersetzt
keine fehlenden Ergebnisse. Leere Pflichtauswahlen, übersprungene oder fehlende
Pflichtfälle erzeugen `INCOMPLETE`; Writerfehler werden als Ausführungsfehler
weitergegeben.
Auch Apache-Einzelfall- und Fallloop-Aufrufer stoppen bei fehlgeschlagener
Ergebnisveröffentlichung vor der PASS-Ausgabe. Dies schließt den erforderlichen
generischen Apache-MRTS-Fehlerpfad ohne Änderung des ausgewählten CRS-
Veröffentlichungsvertrags.

Der native Bericht prüft private FTW-Auswahl und strukturiertes Ergebnis erneut;
alte Logsummen können keine PASS-Zahlen erzeugen. Die Berichtszähler trennen
Auswahl und Ausführung. Paketvorbereitung beweist kein Hostverhalten. Native
MRTS-Evidence bleibt von Connectorqualifikation getrennt.

`MRTS_NATIVE_ROOT` muss unter `BUILD_ROOT` liegen. `MRTS_NATIVE_REPORT_ROOT`
verwendet standardmäßig `$MRTS_NATIVE_ROOT/reports` und muss ebenfalls unter
`BUILD_ROOT` bleiben. Generierte Berichte entstehen unter
`$MRTS_NATIVE_REPORT_ROOT/reports/testing/generated/`, außerhalb des
Quellcheckouts. Build-/Log-/Runtime-Roots müssen in erlaubtem externem Speicher
liegen. Dieser Änderung bedarf keiner vollständigen historischen MRTS- oder
H2/H3-Matrix.

## Integrationsreihenfolge und Kompatibilität

1. Den eigenständigen Framework-MRTS-Paket-PR und seine gezielten Tests prüfen.
2. Framework nur mit separater Merge-Autorisierung integrieren.
3. In einem separat autorisierten Parent-Pin-Auftrag den geprüften
   Framework-`master`-SHA mit Paketschnittstelle wählen. MRTS-Pin erhalten.
4. Den nativen Parent-Aufrufer mit verfügbarer Abhängigkeit integrieren. Für
   lokale Prüfung über beide PRs den vorgeschlagenen Framework-Checkout
   explizit über `FRAMEWORK_ROOT` wählen; dies aktualisiert keinen Parent-Gitlink.

Der aktuelle Parent-Pin enthält diese Schnittstelle noch nicht; der Aufrufer-PR
ist deshalb abhängig und bleibt bis Framework-Integration und explizitem
Pin-Update Draft. Der Testumzug kann denselben Parent-Einstiegspunkt oder das
generierte On-Demand-Archiv berühren; diese Schnittstellen abgleichen, ohne
den Importer zu kopieren oder den Korpus erneut zu verschieben. HTTP/2, HTTP/3,
Coverage und Erweiterungen der Abhängigkeitsmatrix bleiben eigene Arbeiten.

Der [Parent Change Record](../../reports/audits/change-records/CR-20261028-mrts-package-integration.de.md)
enthält tatsächlich ausgeführte Prüfungen und Runtime-Einschränkungen.
