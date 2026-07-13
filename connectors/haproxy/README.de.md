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

## Build-Starter

Für die vollständige Repository-gestützte HAProxy-Kompilierung und lokale Verifizierung
Flow finden Sie im Root-Leitfaden: [`docs/build/compilers/haproxy.md`](../../docs/build/compilers/haproxy.de.md).
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
Verarbeitung des Anfragetextes. `make smoke-haproxy` ist für Live-HAProxy erforderlich
Laufzeitbeweise.

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

Der gemeinsame Fallsatz der Phase 4 bleibt evidenzgeschützt. Regelbeobachtung ist
getrennt von einem für den Kunden sichtbaren 403; das semantische Pre-Commit, Late-Action und
Statusmetadatenfälle bleiben bis zu ihrem fehlenden Hostverhalten `NOT_EXECUTED`
umgesetzt wird. Antworttext-Nutzlasten dürfen niemals in Ereignisse oder geschrieben werden
Berichte.

## Natives HTX-Precommit-Overlay für das vollständige Lebenszyklusprofil

`htx-overlay/` enthält einen quellengebundenen HAProxy **3.2.21** nativen HTX-Filter für
die nativen HTX-Rückrufe `http_payload` und `http_end`. Es ist in eine eingebaut
Einweg-Upstream-Arbeitsbaum. `full-lifecycle-haproxy-htx` wählt es aus, während
die SPOE/SPOP-Laufzeit bleibt der separate Kompatibilitätspfad:

```sh
make -C connectors/haproxy check-htx-overlay
HAPROXY_HTX_SOURCE_DIR=/path/to/haproxy-3.2.21 \
MODSECURITY_INCLUDE_DIR=/path/to/include \
MODSECURITY_LIB_DIR=/path/to/lib \
BUILD_ROOT=/srv/modsecurity-work/haproxy-htx-smoke \
make -C connectors/haproxy runtime-smoke-haproxy-htx
```

Der dedizierte Smoke-Test baut einen gepatchten Einweg-HAProxy 3.2.21-Arbeitsbaum auf.
Lädt die kanonischen No-CRS-Regeln des Frameworks und validiert die generierten
`filter modsecurity-htx`-Konfiguration und sendet echten lokalen Socket-Verkehr.
Es handelt sich um normale Upstream-200, kanonische P1-Verweigerungsantworten für die Regel `1100001`
(403) und `1100002` (429) sowie eine kanonische P3-Verweigerungsantwort für die Regel `1100201`
(403). Der P3-Fall beweist auch, dass vor dem eine Upstream-Antwort eingegangen ist
Die lokale Antwort hat es ersetzt. Das Overlay leitet nur die aktuell geliehenen Daten weiter
`HTX_BLK_DATA` schneidet zur Bindung und beendet Phase 4 einmal bei Antwort-EOS.
Es verwendet weder `wait-for-body`/`res.body` noch behält es eine Connector-eigene Antwort bei
Puffer. Beweise behalten nur begrenzten Client-Status/Byte-Anzahl, Upstream-Anzahl,
Transaktions-ID, Phase, Regel-ID und Aktionsmetadaten.

Für die Ein-Block-P2-Sonde (`1100101`) gibt `http_payload` geliehene Daten zurück
vor der späteren Entscheidung `http_end`. Der Host-Läufer zeichnet auf, ob der Test durchgeführt wurde
Upstream sah keine oder eine Anfrage; Keiner der Werte legt ihre Reihenfolge fest
gegen den für den Client sichtbaren 403. Der Filter verwendet das normale Reply-and-Close von HAProxy
Pfad ohne Connector-eigenen Körperpuffer. Dies ist kein Beweis für einen Zuwachs
Anforderungsweiterleitung oder eine allgemeine Host-Puffer-Garantie. P4 (`1100301`) verwendet geliehene Daten
Antwortdaten und eine Antwort EOS. Sicher/minimal bewahrt den Upstream
200/Körper und Aufzeichnungen `host_action=log_only`; Strenge hält
`host_action=not_attempted`, da kein für den Client sichtbares HAProxy-Abbruchprimitiv vorhanden ist
ist bewiesen. Der Smoke-Test beansprucht keine Umleitung, keinen Post-Commit-Abbruch,
First-Byte-Proof, ein Client-No-Full-Buffer-Proof, eine Common Runtime Bridge oder eine andere
Fähigkeitsförderung. Seine Zusammenfassung bleibt bewusst erhalten
`capability_promotion=not_permitted`, daher kann kein lokaler Hostnachweis vorliegen
als synthetische kanonische Werbung umklassifiziert.

Dieses Overlay wird nicht vom eingecheckten SPOP-Harness konfiguriert und ist es auch
Nur nicht geförderte kanonische Host-Beweise. Deshalb wird **keine** Werbung gemacht
die SPOE/SPOP Phase-4, Late-Intervention, No-Buffer oder First-Byte
Fähigkeiten.
