# PR #382: Checkliste für gemeinsames Connector-Verhalten

**Sprache:** Deutsch | [English](pr-382-checklist.md)

[Draft-PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382)
verwendet `fix/unified-native-results-events-20260921`, ausgehend von
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Aktualisiert: 2026-09-21.

**Stand: Implementierung läuft; noch nicht zum Mergen bereit.** Ein Häkchen unter
Implementierung bedeutet, dass der beschriebene Code vorhanden ist, nicht, dass
jeder Host einen Integrationstest bestanden hat. Die Verifikation hat eine eigene
Checkliste. Ein vorhandener Job, ein gestarteter Build oder ein erfolgreicher
anderer Connector genügt nicht für ein Häkchen. Jedes Testergebnis gilt nur für
die ausdrücklich genannte Revision und Testebene.

## 1. Implementierung

- [x] I01: `common/include/msconnector/native_result.h` ergänzen: Direkte Byte-Append-Ergebnisse `0` und `1` dürfen fortfahren; andere Ergebnisse schlagen fehl. Eine Phasenauswertung ist nur bei `1` erfolgreich. Die Append-Regel gilt nicht für APR-/NGINX-/HTTP-/Common-Rückgaben oder Datei-Lade-APIs.
- [x] I02: Die gemeinsamen Append-/Finish-Prädikate in den betroffenen Apache-Body-Filtern, im HAProxy-Binding, in der Common Runtime und im NGINX-Response-Body-Pfad verwenden.
- [x] I03: Nicht dokumentierte Rückgaben von `msc_intervention()` in Common Runtime und HAProxy-Binding zurückweisen; Bereinigung und Fehlerweitergabe beibehalten.
- [x] I04: Einen Fehler des HAProxy-Response-Header-Bindings auch dann als Fehler erhalten, wenn die Entscheidung zusätzlich disruptiv ist.
- [x] I05: `event_protocol.h` ergänzen und dieselbe kanonische Ereignisdarstellung für JSONL-Writer und Integritäts-Hash verwenden. Ursprüngliche Eingabevalidierung, Query-Redaktion, Bytezähler, Statusbeobachtungen und Transportflags erhalten.
- [x] I06: Technische Fehler in den geänderten Apache-/Common-Ereignispfaden von Regelblockierungen unterscheiden; die separaten handgeschriebenen JSON-Fallback-Datensätze von Apache entfernen.
- [x] I07: Typisierte NGINX-Response-Body-Fehlerereignisse ergänzen. Erfolgreiches EOS nicht aus einem vor der nativen Auswertung gesetzten Flag ableiten.
- [x] I08: `MSCONNECTOR_ERROR_MODSECURITY_FAILURE` in `common/src/modsecurity_engine.c` auf `MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE` abbilden; getrennte Klassen für Hostfehler, Timeout, nicht verfügbare Engine, Protokoll und Body-Limit erhalten.
- [ ] I09: NGINX-Request-Body-/Dateipfade und verbleibende native API-Pfade abschließen, ohne einen I/O-Fehler mit `ProcessPartial` zu verwechseln.
- [ ] I10: Den profilübergreifenden Vergleich von `off`/`safe`/`strict` abschließen. Insbesondere darf kein technischer Fehler zu einer erfolgreichen Safe-`log_only`-Entscheidung werden.
- [ ] I11: Fehler-/Logging-Vergleich vom Ereigniserzeuger bis zur Ausgabe abschließen: Ereignis-IDs, Ursachen, angeforderte gegenüber beobachteten Aktionen, doppelte terminale Ereignisse sowie Fehler beim Öffnen, Schreiben, verkürzten Schreiben und Serialisieren von Logs.
- [ ] I12: Alle direkten, Companion-, Middleware- und Sidecar-Pfade getrennt prüfen; Unterstützung nicht aus einem gemeinsamen Parser oder Connector-Familiennamen ableiten.

## 2. Verifikation

- [x] V01: Doppelte C-Rückgabetypen in erzeugten Testdateien korrigieren. `function_definition()` enthält den Rückgabetyp bei den extrahierten Common-Definitionen bereits.
- [x] V02: Einen erfolgreichen CI-Schritt `Verify native results and common event protocol` für `4f94f33d852f026e703f3237ed98826ae305719a` in [Lauf 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389) nachweisen. Dieser prüft kompilierte Helfer, echten Serializer-/Hash-Code, extrahierte Runtime-Callbacks und Quellcode-Anbindung, nicht sechs laufende Hosts.
- [x] V03: `tests/test_native_error_classification.py` ergänzen und an den bestehenden fokussierten Lint-Schritt anbinden. Die kompilierte Testdatei prüft den echten Klassifizierer mit protokollierenden Uhr-/Contract-Testobjekten.
- [x] V04: Die NGINX-Upstream-Quellcodeprüfungen an die gemeinsamen Prädikate anpassen; explizite Prüfungen auf terminalen Fehler, Abbruch vor Rückgabe, keine Ersatzantwort nach Commit und keine erfolgreiche Bytezählung bei Append-Fehler beibehalten.
- [ ] V05: Einen erfolgreichen Lauf beider fokussierter Common-Testmodule und der Phase-4-/NGINX-Sicherheitstestgruppe auf der aktuellen Revision dokumentieren.
- [ ] V06: Apache-Adoption-Prüfungen und NGINX-Adoption-/Mutationstests korrigieren und erneut ausführen. Negative Mutationsabdeckung erhalten; Prüfungen nicht für einen grünen Status abschalten.
- [ ] V07: Alle erforderlichen Prüfungen des aktuellen PR-Heads bestehen und relevante Review-/Sonar-Befunde beheben. Frühere grüne Prüfungen sind kein Nachweis für den aktuellen Head.
- [ ] V08: Identische echte Host-Fälle für Engine-`ProcessPartial`, Engine-Reject/Interventionen, leere Antwort, mehrere Chunks und ein EOS, aktivierten CSV-MIME-Typ, optionales Connector-Budget und Engine-Fehler ausführen.
- [ ] V09: Späte Safe-/Strict-Ergebnisse und Fehler vor/nach Commit je unterstütztem Transport prüfen. Client-Bytes, Abbruch/Reset, Überleben benachbarter Streams, Bereinigung und passende JSONL-Ereignisse statt nur des HTTP-Status beobachten.
- [ ] V10: Metadaten-Logeinträge jeder echten Integrationsroute vergleichen, einschließlich ungültiger/übergroßer Metadaten, fehlerhafter Ausgaben und fehlender Transportbeobachtungen.

## 3. Stand je Familie

| Familie | Implementierter Teil | Noch erforderlich |
| --- | --- | --- |
| Apache | Body-Append-/Finish-Prädikate und geänderte Fehler-/Ereignisbehandlung | Adoption-Prüfungen, vollständiger nativer Build und Host-/Log-Regressionstests |
| NGINX | Response-Body-Prädikate und typisiertes Fehlerereignis | Verbleibende Request-/Dateipfade, Adoption-Mutationen, Host-/Transportregressionen |
| HAProxy | Prädikate des direkten Bindings und Fehler-/Interventionsweitergabe | Getrennter Verhaltens- und Ereignisnachweis für HTX und SPOE/SPOP/Companion |
| Envoy | Native Rückgabekorrektur über Common Runtime | Getrennte Verifikation von ext_proc und ext_authz/Response-Companion |
| Traefik | Native Rückgabekorrektur über Common Runtime | Verifikation von nativer Middleware/UDS und forwardAuth/Response-Companion |
| lighttpd | Native Rückgabekorrektur über Common Runtime | Getrennte Verifikation von Sidecar und nativen/gepatchten Profilen |

Nicht unterstützte Strict-Profile bleiben nicht unterstützt, solange keine echte
Hostfähigkeit implementiert und getestet ist. Gleiche Semantik bedeutet weder
identische Host-API-Rückgabezahlen noch identische Präfixe der Logziele oder
erfundene Abbruchfähigkeiten.

## 4. Dokumentation und Lieferung

- [x] D01: Arbeit in Draft-PR #382 belassen; nicht mergen oder direkt nach `master` pushen.
- [x] D02: Diese englische/deutsche Checkliste mit gegenseitigen Links und getrenntem Implementierungs-/Verifikationsstand ergänzen.
- [ ] D03: Gemeinsame Vertrags-/Migrationsdokumentation, Logbeispiele und betroffene Connector-Anleitungen auf EN/DE vervollständigen.
- [ ] D04: Zweisprachigen Change Record mit tatsächlichen Ergebnissen ergänzen und die PR-Beschreibung an den aktuellen Diff anpassen.
- [ ] D05: Neue Dokumentationspaare, Links, begrenzten Diff sowie abschließende Gleichheit von Branch-/PR-Head prüfen.

## Bekannte Blocker und Nachweisgrenzen

Für `4f94f33d852f026e703f3237ed98826ae305719a` bestand der fokussierte
Native-/Event-Schritt, der gesamte Lint-Workflow schlug aber weiterhin fehl.
Alte NGINX-Quellcodeprüfungen erwarteten `ret != 1` und einen direkten
`< 0`-Append-Vergleich. Diese Prüfungen wurden anschließend angepasst; ihr
nächstes CI-Ergebnis muss hier noch eingetragen werden. Der NGINX-Adoption-
Checker samt Mutationstests und die Apache-Adoption-Prüfungen müssen ebenfalls
an die geänderten Pfade angepasst werden. Sie bleiben offen und sind keine
akzeptierten Fehler.

Während dieser Fortsetzung wurde kein lokaler nativer Host-Build und keine
vollständige HTTP-Matrix für sechs Familien ausgeführt. Der lokale Wrapper für
Projektbefehle war nicht verfügbar; GitHub CI liefert die Ausführungsnachweise.
Eine Testdatei mit sechs Connector-Namen ist kein Nachweis für sechs
Hostintegrationen; ein erfolgreiches Quality Gate ist kein Laufzeitnachweis.

## Aktualisierungsregel

Vor einem Verifikationshäkchen `[x]` den genauen Commit, Befehl, Lauf-/Joblink
und erfolgreichen Endstatus festhalten. Die deutsche Fassung gleichwertig
pflegen. Eine spätere Verhaltensänderung braucht neue Validierung; historische
Nachweise müssen als historisch erkennbar bleiben. Änderungen an Framework/MRTS,
Abhängigkeiten, Sicherheitsprüfungen oder Merge-Status liegen außerhalb dieser
PR-Fortsetzung.
