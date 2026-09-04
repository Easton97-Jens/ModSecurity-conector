# HAProxy-Connector

**Sprache:** [English](README.md) | Deutsch


Status: teilweise; Historische SPOA-Laufzeitdatensätze fördern keine kanonische Version
Phase-4-Fähigkeiten.
Laufzeitstatus: Das Repository enthält eine Live-YAML-Ausführungsverkabelung
HAProxy, SPOA/SPOP und ein Repo-erstellter `haproxy-modsecurity-spoa`-Agent.
Beweise auf Anfrageseite sind von Beweisen auf Antwortbasis und verspäteter Intervention getrennt
Beweise. `RESPONSE_BODY` bleibt nicht hochgestuft.
Vorlagenausrichtung: Gerüstausgerichtet plus lokaler SPOA-Agent-Starter/Laufzeit.

Dieser Connector enthält Repository-eigene Metadaten, einen lokalen HAProxy SPOA-Agenten
Starter, eine Produktions-SPOP-Laufzeitumgebung und eine lokale libmodsecurity-Bindung. Die
Der Produktionsagent lädt ModSecurity-Regeln einmal und erstellt Transaktionen mit dem
HAProxy `unique-id` behält den begrenzten Transaktionsstatus für seine Anfrage bei und
optionale Antwort-Header-Phasen, gibt aus
Entscheidungs-JSONL und gibt typisierte SPOE-ACK-Variablen für die HAProxy-Durchsetzung zurück.
Der SPOP-Listener besitzt keinen authentifizierten Transport und ist absichtlich
auf `127.0.0.1` beschränkt; Remote- oder Wildcard-Binds werden nicht unterstützt
und fail-closed abgewiesen.
`make smoke-haproxy` listet gemeinsam genutzte Framework-YAML-Fälle mit `case_cli.py` auf.
In jedem Fall werden HAProxy und der Produktions-SPOA-Agent gestartet
Backend, sendet die Fallanfrage mit Curl, bestätigt den beobachteten Status und
schreibt die standardmäßigen HAProxy-Zusammenfassungsartefakte.

`make runtime-matrix-haproxy` nutzt Live-Zusammenfassungsbeweise aus der Aufteilung
No-CRS- und With-CRS-HAProxy-Läufe. PASS/FAIL-Zeilen müssen vom Live-HAProxy stammen
Ausführung; Strukturell nicht zuordbare Zeilen verwenden `NOT_EXECUTABLE` und real
Umgebungs-/Build-/Laufzeitblocker verwenden `BLOCKED`.

Die bewährten anforderungsseitigen Variablen sind `REQUEST_URI`, `REQUEST_HEADERS`,
`REQUEST_HEADERS_NAMES`, `ARGS`, `ARGS_NAMES`, `REQUEST_COOKIES`,
`REQUEST_COOKIES_NAMES`, `REQUEST_BODY`, `FILES` und `XML`. URL-kodiert,
Die Abdeckung von JSON-, XML-, Multipart- und CRS-SQLi-Anomalie-Anfragetexten ist live
Beweise, begrenzt durch HAProxy-Anforderungspufferung, SPOE-Framegröße und konfiguriert
Grenzwerte für Anforderungstexte. Antwort-Header- und Audit-Log-Pfade verwenden SPOE-Antwort
Nachrichten. Für den gesamten Lebenszyklus wird ein separates HTX-Beobachter-Overlay ausgewählt
Profil über `full-lifecycle-haproxy-htx` und verfügt über einen dedizierten Real-Host
Transportrauch für inkrementelle Anfrage- und Antwortblöcke. Es bleibt
unterscheidet sich vom aktiven SPOP-Kompatibilitätspfad und ist kein kanonischer Beweis
für Durchsetzung, strikten Abbruch oder vollständige `RESPONSE_BODY`-Unterstützung.

## Globaler Vertrag

Siehe den kanonischen [Connector-Vertrag](../../docs/connectors/README.de.md)
und den [Test-/Evidence-Guide](../../docs/testing-and-evidence.de.md).

Gemeinsam genutzte konnektorneutrale Datenformen, die vom Starter verwendet werden:

- `common/include/msconnector/origin.h`
- `common/include/msconnector/request.h`
- `common/include/msconnector/intervention.h`
- `common/include/msconnector/status.h`
- `common/src/intervention.c`

## HAProxy-spezifischer Zustand

- Herkunft/Lizenz: nur für Starter dokumentiert, die von Repo-Autoren erstellt wurden; Upstream-HAProxy
  Die Anschlussquelle ist nicht ausgewählt.
- Metadaten: `metadata.c` und `metadata.h` vorhanden.
- Build: Metadatenobjekt und lokaler SPOA-Agent-Starter-Build sind vorhanden.
- Selbsttest: lokaler Starter-Selbsttest vorhanden; Es startet HAProxy nicht.
- SPOP-Laufzeit: erstellbar und selbsttestbar unter
  `/src/ModSecurity-conector-build/haproxy-spoa-runtime/` as
  `haproxy-modsecurity-spoa`; Der Harness und normale Bereitstellungen nutzen dies ebenfalls
  binärer Pfad.
- ModSecurity-Bindungsselbsttest: erstellbar und selbsttestbar unter
  `/src/ModSecurity-conector-build/haproxy-modsecurity-binding/`; verifiziert
  Phase-1-Header-Blockierung und Anhängen/Verarbeiten des Anforderungstexts in Bearbeitung.
- Harness: `make smoke-haproxy` überprüft Live-HAProxy auf SPOA/SPOP
  Durchsetzung von libmodsecurity für Shared-Framework-YAML-Fälle.
- Entscheidungsnachweise: Einzelfall `decision.jsonl`, HAProxy-Protokolle, SPOA-Protokolle, Audit
  Protokolle, beobachteter Status und normalisiertes `result.json`.
- RESPONSE_BODY-Blockierung: nicht im aktiven SPOP-Harness implementiert; die
  Das frühere `wait-for-body`-Beispiel ist deaktiviert. Die native HTX-Precommit-Route lautet
  Wird nur vom Full-Lifecycle-Profil ausgewählt, prüft P1/P3-Hostantworten und
  fördert nicht die Fähigkeit des Antwortkörpers.

### SPOP-Korrelationsgrenze der Request-ID

`request_id` ist ein Korrelationsschlüssel, kein Display-String. Die
Produktions-SPOP-Runtime validiert die ursprünglichen längenbegrenzten Bytes
vor ihrer C-String-Kopie: leere, eingebettete-NUL-, Control-Byte-, Nicht-ASCII-
und zu lange Werte werden abgewiesen. Damit kann `A\0X` an der
Transaktions-Cache-Grenze nicht zu `A` kollabieren, während eine nichtleere
druckbare ASCII-ID einschließlich der normalen UUID-Form zulässig bleibt. Eine
fehlerhafte `request_id` lässt die Notification-Extraktion fehlschlagen und
kann keine Transaktion erzeugen, ersetzen oder claimen.

## Build-Starter

Für die vollständige Repository-gestützte HAProxy-Kompilierung und lokale Verifizierung
Flow finden Sie im Root-Leitfaden: [`docs/build/compilers/haproxy.de.md`](../../docs/build/compilers/haproxy.de.md).
Die folgenden Connector-lokalen Hinweise beschreiben nur den Status und den Zielbereich.

Unterstützte lokale Build-Ziele:

```sh
make -C connectors/haproxy build-metadata
make -C connectors/haproxy build-spoa-starter
make -C connectors/haproxy build-starter
make -C connectors/haproxy self-test-spoa
make -C connectors/haproxy self-test
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-spoa-runtime
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding-crs
```

`build-spoa-starter` kompiliert eine lokale Binärdatei, die ihre Einschränkungen beschreiben kann
und führen Sie einen synthetischen Selbsttest zur Entscheidung „Zulassen/Blockieren“ durch. Es kompiliert HAProxy nicht,
kompiliert kein HAProxy-Modul, analysiert keine SPOP-Frames und wird nicht als ausgeführt
verifizierter SPOA-Server und verknüpft libmodsecurity nicht.

`build-spoa-runtime` kompiliert `haproxy-modsecurity-spoa`. Sein Selbsttest ist
Nachweis der Protokollkompatibilität; `make smoke-haproxy` ist das Live-Gate, das
startet HAProxy gegen diesen Produktionsagenten und führt Framework-YAML-Fälle aus.

`build-modsecurity-binding` überprüft zunächst die lokale libmodsecurity C-API
Signaturen durch eine kompilierte Sonde und erstellt dann eine kleine Selbsttest-Binärdatei.
`self-test-modsecurity-binding` beweist die In-Process-Phase-1-Header-Blockierung und
Request-Body-Rule-Verarbeitung sowie Request-/Response-Body-Wrapper-Lifecycle-
Guards für einen Nichtnull-Längen-Nullpointer, Append nach EOS und doppelte
Finalisierung. Diese Wrapper-Kontrollen sind nur Selbsttest-Evidenz: Sie
beweisen weder Live-HAProxy-Enforcement noch eine positive
`RESPONSE_BODY`-Intervention. `make smoke-haproxy` ist für Live-HAProxy-
Laufzeitbeweise erforderlich.

## libModSecurity-Kompatibilitätsvertrag

Das gemeinsame HAProxy-Binding unterstützt `libModSecurity >= 3.0.14`; `3.0.14`
bleibt die unterstützte Mindestversion. Das ausgewählte Include-Verzeichnis und
das Library-Verzeichnis müssen eine bewusst ausgewählte Installation
beschreiben. Das Binding kompiliert und **linkt** zuerst seine erforderliche
öffentliche Baseline-C-API gegen dieses Paar. Ein Baseline-Fehler beendet den
Build mit dieser Diagnose:

```text
The HAProxy connector requires the public libModSecurity API available in version 3.0.14 or newer. The detected headers and library do not provide the required baseline API or do not match.
```

`msc_get_rules_messages_rule_ids` gehört nicht zur Baseline. Seine exakte
Deklaration wird in einem separaten Probe gegen dasselbe ausgewählte Paar
kompiliert und sein Symbol gelinkt. Nur ein erfolgreicher Compile-und-Link-
Probe setzt `HAPROXY_HAVE_MSC_GET_RULES_MESSAGES_RULE_IDS=1`; es werden weder
eine Entscheidung allein anhand einer Versionsnummer noch eine manuelle
Deklaration oder eine Runtime-Symbolauflösung verwendet. Der Build zeichnet
`HAPROXY_MODSECURITY_RULE_IDS_API=available|unavailable` und die zugehörigen
kontrollierten Compiler-Flags in
`haproxy-modsecurity-binding/paths.env` auf und propagiert das Ergebnis sowohl
in die SPOP-Laufzeit als auch in den separaten HTX-Overlay-Build.

Wenn die optionale API nicht verfügbar ist, wird eine Rule-ID nur dann als
begrenzte diagnostische Metadaten aus einem Interventionslog gewonnen, wenn
dies möglich ist. Eine nicht intervenierende Transaktion kann deshalb
`rule_id=0` melden. `msc_intervention` bleibt die alleinige Quelle für
Disruptive-State, Status, Redirect-/Deny-Aktion und Cleanup; fehlende
Rule-ID-Metadaten ändern niemals eine HTX- oder SPOP-Sicherheitsentscheidung
und erzeugen kein Allow-by-default-Verhalten.

Verwenden Sie für einen lokalen Build explizite, passende Pfade:

```sh
BUILD_ROOT=/external/task-root \
MODSECURITY_INCLUDE_DIR=/selected/include \
MODSECURITY_LIB_DIR=/selected/lib \
MODSECURITY_INCLUDE_CANDIDATES=/selected/include \
MODSECURITY_LIB_CANDIDATES=/selected/lib \
make -C connectors/haproxy build-modsecurity-binding build-spoa-runtime
```

Führen Sie `make -C connectors/haproxy self-test-modsecurity-binding` für die
In-Process-Binding-Kontrollen aus. `make smoke-haproxy` bleibt das getrennte
Live-SPOP-Gate, während `make -C connectors/haproxy runtime-smoke-haproxy-htx`
das getrennte native HTX-Build- und Host-Smoke-Gate bleibt; keiner der beiden
Pfade ersetzt den anderen.

## Tests

Es wird kein lokaler Ordner `connectors/haproxy/tests` verwendet. Ausführbare Laufzeittests sind
Framework-eigene.

Framework-eigene Pfade und Ziele zur Verwendung für zukünftige Beweise:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make runtime-matrix-haproxy`
- `make test-haproxy-no-crs`
- `make test-haproxy-with-crs`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

Nicht unterstützte oder derzeit nicht materialisierbare Zeilen werden als dokumentiert
`NOT_EXECUTABLE`. Dies gilt für Harness-, Abhängigkeits-, Build- und Laufzeitfehler
dokumentiert als `BLOCKED`. `RESPONSE_BODY`-Zeilen bleiben nicht ausgewählt/nicht implementiert
bis ein zukünftiger nativer Host-Response-Chunk-Pfad das Individuum beweist
Response-Body- und Late-Intervention-Facetten ohne `wait-for-body`.

## Gemeinsame SDK-Einführungsgrenze

Die HAProxy-Einführungsschicht bettet `msconnector_config` ein bzw. ordnet sie zu und verwendet allgemeine Richtlinienspezifikationen/Adapter, Parser-Grundelemente, Mapper-Verträge, Header-Helfer, Ereignis-JSONL-Helfer, Regel-ID-/Protokollbereinigungs-Grundelemente und globale Schutzstrukturen, sofern implementiert. HAProxy-spezifische SPOE/SPOP-Protokollverarbeitung, CFG-Glue, Prozesslebenszyklus, Socket-/Laufzeitverarbeitung, Frame-Parsing, Rückgabe-/Aktionskodierung, Protokollierungstransport und Build-Glue bleiben lokal.

C17-Kompilierungsnachweise sind über `make check-haproxy-c17` verfügbar; Optionale C23/Future-C-Prüfungen hängen von der Compiler-Unterstützung ab. Fehlende HAProxy/libmodsecurity-Header werden als `BLOCKED` mit Exit 77 gemeldet. Dies ist kein Produktions-, CRS-, Vollmatrix- oder Laufzeitverifizierungsanspruch.

## Kanonische Phase-4-Grenze

HAProxy verwendet den Repository-SPOE/SPOP-Agentenpfad für Anfragen und optional
Antwort-Header-Behandlung.  Seine alte begrenzte Antwortkörperprobe hing davon ab
`http-response wait-for-body`; Es ist absichtlich deaktiviert, da es sich um ein Beispiel handelt
wait ist keine echte Response-Chunk-API und würde gegen die niedrige Latenz verstoßen
Vertrag.  `response_body_buffered`, `phase4` und
`phase4_rule_evaluation` sind daher `not_implemented` in der Auswahl
SPOE/SPOP-Pfad, bis dieser Pfad einen nativen HTX/Filter-Adapter mit geborgtem verwendet
Antwortblöcke und ein explizites Ende des Streams. `phase4_pre_commit_deny`,
`late_intervention`, `late_intervention_log_only`,
`late_intervention_abort` und `late_intervention_status_metadata` sind ebenfalls vorhanden
`not_implemented`.

Der Agent serialisiert derzeit von der Richtlinie abgeleitete Pre-Commit-Felder, der Host jedoch
Der Läufer beobachtet keine für den Kunden sichtbare Phase-4-Verweigerung, den tatsächlichen Verpflichtungszeitpunkt,
oder ein Post-Commit-Antwortpunkt.  Es ist daher weder sicher noch implementiert
`log_only` ist noch strikt `abort_connection` und kann keine Semantik beanspruchen
Original-/Angefordert-/Sichtbarstatus-Metadaten.  Ein Agent-Timeout, ein Agent-Fehler,
oder eine generische HAProxy-Trennung ist kein Beweis für einen Abbruch durch eine späte Intervention.

### Verbindliche native-HTX-Response-Begleitkomponente

Die logische Lösung `haproxy-spoe-spop` benötigt für P3/P4 eine native
HTX-Response-Begleitkomponente. Sie muss dieselbe HAProxy-Unique-ID nutzen,
genau eine lebende Transaktion übernehmen, begrenzte Response-Header und
geliehene DATA-Slices weiterleiten und genau einmal am nativen `http_end`
abschließen. Fehlende oder doppelte Korrelation, Cancel, Timeout und Cleanup
müssen die Transaktion abbrechen; eine SPOP-Notification oder ein
`wait-for-body`-Sample ist niemals ein EOS-Signal.

Der produktive SPOP-Agent akzeptiert `response-companion=native-htx` nur mit
einem expliziten privaten Companion-Socket, passenden UID/GID-Werten und einem
begrenzten Response-Body-Limit größer null. Das implementierte kombinierte Profil
registriert den HTX-Request-Data-Filter nach P1, bindet das vom SPOP-Agenten
veröffentlichte opake Handle an `stream->uniq_id` und ruft die gemeinsamen
Response-Header-/DATA-/EOS-Callbacks aus den HAProxy-Filter-Hooks
`http_payload`/`http_end` auf. Fehlende, ungültige, abgelaufene oder doppelte
Handles bleiben Fail-Closed; der Standardpfad `response-companion=none` weist
Response-Body-Aktivierung weiterhin zurück, weil dort kein Response-EOS-
Transport vorhanden ist. Der repository-native Current-Source-MRC1-v2-
Hostharness prüft den kombinierten P1/P2-zu-P3/P4-Pfad lokal; ein externes
v1-Artefakt ist kein Ersatz, und dieses qualifizierte lokale Ergebnis ist keine
allgemeine Produktionsreifebehauptung. Interne Connector-, Protokoll-,
Timeout-, Unavailable- und Invalid-Engine-Response-Cleanups müssen die
entsprechende typisierte MRC1-Terminalursache verwenden und dürfen nicht als
geratener Client- oder Upstream-Disconnect erscheinen.

Der gemeinsame Fallsatz der Phase 4 bleibt evidenzgeschützt. Regelbeobachtung
ist getrennt von einem für den Client sichtbaren 403; die semantischen Fälle
für Pre-Commit, Late-Action und Statusmetadaten bleiben `NOT_EXECUTED`, bis
das fehlende Hostverhalten implementiert ist. Response-Body-Payloads dürfen
niemals in Ereignisse oder Berichte geschrieben werden.

## Natives HTX-Precommit-Overlay für das vollständige Lebenszyklusprofil

`htx-overlay/` enthält einen quellengebundenen, Framework-synchronisierten,
nativen HAProxy-HTX-Filter für die HTX-Rückrufe `http_payload` und `http_end`.
Er wird in einen entbehrlichen Upstream-Arbeitsbaum gebaut.
`full-lifecycle-haproxy-htx` wählt ihn aus, während die SPOE/SPOP-Laufzeit ein
getrennter Kompatibilitätspfad bleibt:

```sh
make -C connectors/haproxy check-htx-overlay
HAPROXY_HTX_SOURCE_DIR=/path/to/framework-synchronized-haproxy-source \
MODSECURITY_INCLUDE_DIR=/path/to/include \
MODSECURITY_LIB_DIR=/path/to/lib \
BUILD_ROOT=/srv/modsecurity-work/haproxy-htx-smoke \
make -C connectors/haproxy runtime-smoke-haproxy-htx
```

Der dedizierte Smoke-Test baut einen gepatchten, entbehrlichen,
Framework-synchronisierten HAProxy-Arbeitsbaum, lädt die kanonischen
No-CRS-Regeln des Frameworks, validiert die erzeugte
`filter modsecurity-htx`-Konfiguration und sendet echten lokalen Socket-
Verkehr. Er deckt eine normale Upstream-200, kanonische P1-Deny-Antworten für
Regel `1100001` (403) und `1100002` (429) sowie eine kanonische P3-Deny-
Antwort für Regel `1100201` (403) ab. Der P3-Fall beweist außerdem, dass eine
Upstream-Antwort einging, bevor die lokale Antwort sie ersetzte. Das Overlay
leitet nur die aktuell geliehenen `HTX_BLK_DATA`-Slices an die Bindung weiter
und beendet Phase 4 einmal bei Response-EOS. Es verwendet weder
`wait-for-body`/`res.body` noch behält es einen connector-eigenen
Response-Puffer. Die Evidenz bewahrt nur begrenzten Client-Status/
Byte-Anzahl, Upstream-Anzahl, Transaktions-ID, Phase, Regel-ID und
Aktionsmetadaten auf.

Für die Ein-Block-P2-Sonde (`1100101`) gibt `http_payload` geliehene Daten vor
der späteren `http_end`-Entscheidung zurück. Der Host-Runner zeichnet auf, ob
der Test-Upstream null oder eine Anfrage sah; keiner dieser Werte belegt ihre
Reihenfolge gegenüber dem für den Client sichtbaren 403. Der Filter verwendet
HAProxys normalen Reply-and-Close-Pfad ohne connector-eigenen Body-Puffer.
Dies ist kein Nachweis für inkrementelle Request-Weiterleitung oder eine
allgemeine Host-Puffergarantie. P4 (`1100301`) verwendet geliehene
Response-DATA und ein Response-EOS. Safe/minimal bewahrt Upstream-200/Body und
zeichnet `host_action=log_only` auf; Strict behält
`host_action=not_attempted`, weil kein client-sichtbares HAProxy-
Abbruchprimitiv belegt ist. Der Smoke-Test behauptet weder Umleitung noch
Post-Commit-Abbruch, First-Byte-Nachweis, Client-No-Full-Buffer-Nachweis,
Common-Runtime-Bridge oder andere Fähigkeitsförderung. Seine Zusammenfassung
behält bewusst `capability_promotion=not_permitted`; lokaler Hostnachweis darf
daher nicht als synthetische kanonische Förderung umklassifiziert werden.

Dieses Overlay wird nicht vom eingecheckten SPOP-Harness konfiguriert und ist
nur nicht hochgestufter kanonischer Hostnachweis. Es fördert daher **nicht**
die SPOE/SPOP-Fähigkeiten für Phase 4, Late-Intervention, No-Buffer oder
First-Byte.
