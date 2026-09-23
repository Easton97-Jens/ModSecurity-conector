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
- `modsecurity_rules_remote` (abgelehnt: Remote-Regelladen ist durch die gemeinsame Sicherheitsrichtlinie deaktiviert)
- `modsecurity_use_error_log on|off`
- `modsecurity_transaction_id <string>`
- `modsecurity_transaction_id_expr <apache-expression>`
- `modsecurity_phase4_mode off|safe|strict`
- `modsecurity_phase4_log <path>`
- `modsecurity_phase4_body_limit <bytes>`

`modsecurity_transaction_id` akzeptiert eine statische Zeichenfolge und behält die vorhandene bei
statische Semantik. `modsecurity_transaction_id_expr` akzeptiert eine Apache-Zeichenfolge
Ausdruck, zum Beispiel `%{REQUEST_URI}`, und wertet ihn pro Anfrage aus. Die beiden
Direktiven schließen sich im selben Apache-Kontext gegenseitig aus; normal
Untergeordnete Kontextüberschreibungen gelten während der Konfigurationszusammenführung. Wenn keine der Anweisungen festgelegt ist
oder der Ausdruck einen leeren Wert ergibt, verwendet der Connector weiter den
vorhandenen `UNIQUE_ID`-Fallback und erstellt dann eine Transaktion ohne
explizite ID, wenn `UNIQUE_ID` nicht vorhanden oder leer ist. Ein Laufzeitfehler
bei der Auswertung des Ausdrucks oder eine ungültige aufgelöste ID ist dagegen
ein Aufbaufehler für eine aktivierte primäre Anfrage: Der Connector liefert HTTP
500, schließt Keepalive und fällt nicht auf eine nicht untersuchte Anfrage
zurück.

`modsecurity_use_error_log off` unterdrückt die Weiterleitung von Apache-Fehlerprotokollen vom
Nur libmodsecurity-Protokollrückruf. Es ändert nichts an der Überwachungsprotokollierung.
Interventionsverhalten, Anfrage- oder Antwortbehandlung, Hooks, Filter, Buckets,
oder Transaktionseigentum.

Der Phase-4-Modus steuert die zusätzliche Interventionsbehandlung und in
`safe` und `strict` das kumulierte Body-Budget des Connectors. `off` lässt die
konfigurierte Engine-Inspection aktiv. Es gibt keine Connector-eigene
MIME-Allowlist; `SecResponseBodyMimeType` und `SecResponseBodyMimeTypesClear`
wählen die Inspection in libModSecurity. Phase 4 / RESPONSE_BODY bleibt
nicht hochgestuft; Strict-Mode-Verkabelung auf Quellebene beweist keinen
späten Abbruch.

Primäre lokale Referenz: `<external-source-root>/ModSecurity-apache`.
Upstream-Quelle: https://github.com/owasp-modsecurity/ModSecurity-apache.

Das Build-Layout im Besitz des Apache-Adapters befindet sich unter `connectors/apache/`.
Der Framework-eigene Regressionspfad materialisiert es zu
`$BUILD_ROOT/apache-build/connector-src`, bevor dieser getrennte Pfad seinen
Autotools/APXS-Build ausführt. Der frühere `connectors/apache/upstream/`-Baum
wurde nach dem materialisierten Build und Apache-Smoke-Test von Phase 11
entfernt. Phase 13 hält `connectors/apache/src/` auf produktive C-Quellen
beschränkt; Build-Dateien liegen im Connector-Stammverzeichnis, aufbewahrte
Autotools-Testvorlagen unter
`modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/`,
und dauerhafte Attribution unter `licenses/apache/`,
`connectors/apache/ORIGIN.md` und `connectors/apache/SOURCE_MAP.json`.

Build- und Laufzeitartefakte müssen unter `BUILD_ROOT` bleiben, lokal standardmäßig auf
`/src/ModSecurity-conector-build`.

## Reproduzierbarer Parent-Autotools-Bootstrap

Der Framework-Materializer ist ein separater Regressionsintegrationspfad. Ein
frischer Parent-Source-Checkout kann das Apache-Modul bootstrappen und bauen,
ohne Framework-Vorlagen zu materialisieren. Autoconf, Automake, einen
C-Compiler, `make`, Apache-Entwicklungsdateien einschließlich APXS,
libmodsecurity-Entwicklungsdateien, `curl` und `dd` installieren; bei einem
nicht systemweiten libmodsecurity-Prefix `MODSECURITY_PREFIX` darauf setzen.

In einem sauberen Checkout unter `connectors/apache/` das Apache-Binary aus dem
gewählten APXS ableiten und die getrackten Autotools-Quellen verwenden:

```sh
APXS="${APXS:-$(command -v apxs || command -v apxs2)}"
test -x "$APXS"
HTTPD_BIN="${HTTPD_BIN:-$("$APXS" -q SBINDIR)/$("$APXS" -q PROGNAME)}"
MODSECURITY_PREFIX="${MODSECURITY_PREFIX:-/usr}"
APACHE_BUILD_ROOT="${APACHE_BUILD_ROOT:?set an absolute private build directory outside the checkout}"
case "$APACHE_BUILD_ROOT" in
    /*) ;;
    *) echo "APACHE_BUILD_ROOT must be absolute" >&2; exit 2 ;;
esac
mkdir -p "$APACHE_BUILD_ROOT/common-src" "$APACHE_BUILD_ROOT/profile-registry"
autoreconf --install
test -f configure
test -x configure
./configure --with-libmodsecurity="$MODSECURITY_PREFIX" --with-apxs="$APXS" --with-apache="$HTTPD_BIN"
MSCONNECTOR_COMMON_BUILD_SRC="$APACHE_BUILD_ROOT/common-src" \
MSCONNECTOR_PROFILE_REGISTRY_BUILD_ROOT="$APACHE_BUILD_ROOT/profile-registry" \
make
test -f src/.libs/mod_security3.so
```

`APACHE_BUILD_ROOT` muss zu einer privaten task-eigenen Directory außerhalb des
kanonischen Checkouts aufgelöst werden; sie darf weder der Checkout selbst noch
ein Symlink in ihn sein. Der Wrapper staged Common-Quellen und die
Profil-Registry dorthin, bevor APXS Compilerobjekte erzeugen kann. Ein direkter
APXS-Aufruf und eine In-Checkout-Stage-Root sind daher abgewiesene Controls und
keine unterstützten Build-Modi. Das Registry-Unterverzeichnis `connectors`
muss ebenfalls ein frisches Nicht-Symlink-Verzeichnis sein.

Der erwartete Modulausgabepfad lautet `src/.libs/mod_security3.so`. Zur
Validierung des vollständigen Frischquellpfads die fokussierte Prüfung vom
Parent-Root ausführen:

```sh
make check-apache-autotools-bootstrap
```

Sie erzeugt ein Source-Archiv, das nur getrackte Dateien enthält, führt die
obigen Befehle aus, validiert eine isolierte Loopback-Apache-Konfiguration,
lädt das mit Autotools gebaute Modul und prüft eine erlaubte Anfrage mit `200`
sowie eine ModSecurity-Regel mit `403`. Sie sendet außerdem einen festen
synthetischen P2-Request-Body-Marker und fordert `403`, einen nichtleeren
seriellen `RelevantOnly`-Audit-Record mit `ABFZ`-Teilen, der den rohen Marker
ausschließt, sendet danach einen begrenzten P2-Body von 1049600 Byte oberhalb
des Limits und fordert `413` ohne statischen Handler-Inhalt vor einem
`200`-Follow-up in demselben Prozess. Dies sind begrenzte Harness-Controls,
keine Aussage über ein vollständiges Regelprofil, eine Matrix oder B-Reife. In
einem sauberen Checkout, einschließlich CI, entspricht dieses Archiv exakt
`HEAD`. Bei einem lokalen
Pre-Commit-Lauf wendet die Prüfung nur `git diff HEAD` an, um getrackte
Änderungen zu prüfen; ungetrackte Dateien werden nie importiert. Der temporäre
ServerRoot und der nicht privilegierte Loopback-Port werden am Ende entfernt.
Ein direkter Befehl `apxs -c` ist kein Ersatz: das von Autotools erzeugte
`configure` und der anschließende `make`-Pfad sind erforderlich.

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

Wenn Apache den Input-Filter gegen seine initiale, noch nicht gemergte
Directory-Konfiguration aufruft, löst der Filter ein Request-Body-Limit von
null und eine ungesetzte oder nicht unterstützte Body-Limit-Aktion am
Verbrauchspunkt zum gleichen endlichen Common-Default von `1048576` Byte und
zur Aktion `reject` auf, die auch das Common-Konfigurations-Merging verwendet.
Das verhindert, dass ein kleiner nichtleerer Body als ungültiges Limit
behandelt wird, während die endliche Fail-Closed-Grenze erhalten bleibt. Es
legt keinen connector-lokalen Partial-Inspection-Modus offen und macht aus
einem regelgesteuerten P2-Block keine Body-Limit-Response.

## Kanonische Phase-4-Grenze

Der Apache-Ausgabefilter bleibt für die Phase-4-Regelauswertung EOS-only, ist
nun aber ein progressiver Response-Pfad. Er hängt jeden Daten-Bucket genau
einmal an libModSecurity an, erhält FLUSH und Apache-Metadaten vor EOS, trennt
am ersten EOS und reicht das Präfix vor EOS sofort an den nächsten Filter
weiter. Er speichert keine vollständige normalisierte Brigade über Callbacks
hinweg. Nur das terminale EOS-Fragment wartet auf `msc_process_response_body`
und die Late-Action-Auflösung; es handelt sich nicht um Regelauswertung pro
Chunk.

Der Connector übergibt Response-Buckets unabhängig vom MIME-Typ an
libModSecurity; die eigene `SecResponseBodyMimeType`-Konfiguration der Engine
wählt die Inspection. Es gibt weder eine zweite Connector-MIME-Liste noch
eine MIME-basierte Herabstufung von Interventionen.

`modsecurity_phase4_body_limit` hat standardmäßig 1048576 Byte (1 MiB); der
konfigurierte Wert muss positiv sein und darf höchstens 10485760 Byte (10 MiB)
betragen. In `safe` und `strict` wird das kumulierte Limit geprüft, bevor der
nächste Daten-Bucket angehängt oder weitergegeben wird. Ein übergroßer Bucket
wird abgewiesen, nicht nur teilweise inspiziert und freigegeben. Frühere
progressive Bytes können den nächsten Filter bereits passiert haben und
lassen sich nicht umschreiben. In `off` wird dieses zusätzliche kumulierte
Budget nicht durchgesetzt; Engine-Limits, geprüfte Zähler und Lifecycle-/
Fehlerbehandlung bleiben aktiv. Es gibt keinen zusätzlichen Puffer für die
gesamte Response.

An der normalen Entscheidungsgrenze sind Apaches `r->sent_bodyct` und
`eos_sent` kein Commit-Nachweis: Upstream-Module können sie setzen, bevor
dieser Filter sein erstes Präfix weitergibt. Der Aufruf des nächsten Filters
ist die monotone Source-Commit-Grenze; ein separater Terminal-EOS-Guard und
Apaches `r->bytes_sent` bleiben als Metadaten erhalten. Ein Downstream-Fehler
nach progressivem Forwarding versiegelt das Phase-4-Gate, weil ein Body-Präfix
bereits sichtbar sein kann. P4 wird genau einmal bei EOS abgeschlossen;
doppelte terminale Ausgabe wird abgewiesen.

Off bewahrt die native Interventionsbehandlung. `log_only` im Safe-Modus
erhält ein bereits weitergereichtes Präfix.
Strict verwendet `abort_connection` nach einem disruptiven EOS-Ergebnis,
statt emittierte Bytes zu ersetzen. Weil die P4-Regelauswertung bei EOS
erfolgt, behauptet dieser progressive Pfad keinen verlässlichen P4-HTTP-Deny
oder Redirect vor Commit; P3 ist der Entscheidungspunkt für Response-Header
vor dem Commit.

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

## Phase-4-Modus und Inspection-Budget

Der Standardmodus ist `off`; erlaubt sind `off`, `safe` und `strict`.
Das zusätzliche kumulierte Phase-4-Inspection-Budget wird nur in `safe` und
`strict` durchgesetzt. `off` gibt Response-Daten weiterhin gemäß der
konfigurierten Inspection an libModSecurity weiter und macht weder
Regelinterventionen noch echte Engine-Fehler zu einem Erfolg. Die MIME-Auswahl
und eigenen Limits der Engine bleiben maßgeblich.

Dies gilt für native Integrationen und Response-Pfade über die Common Runtime.
Eine reine Request-Route benötigt für Phase 4 weiterhin den unterstützten
Response-Observer beziehungsweise Companion. Die Wahl eines Modus fügt keine
fehlende Response-Inspection hinzu.

Unabhängige Limits für Allokationen, gepufferte Responses, Nachrichten/Frames,
Timeouts und Transport gelten in jedem Modus weiter. Insbesondere kann ein
puffernder Sidecar auch in `off` eine Response ablehnen, die nicht in seinen
begrenzten Speicher passt. Das Weglassen des zusätzlichen Inspection-Budgets
erlaubt keine unbegrenzten Allokationen.

Der [connectorübergreifende Budget-Vertrag](../../docs/phase4-mode-budget.de.md)
beschreibt Geltungsbereich, Fehlerbehandlung und Grenzen der Validierung.
