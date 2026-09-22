# PR #382: Checkliste für gemeinsames Connector-Verhalten

**Sprache:** [English](pr-382-checklist.md) | Deutsch

[Draft-PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382)
verwendet `fix/unified-native-results-events-20260921`, ausgehend von
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Aktualisiert: 2026-09-22.

**Stand: Implementierung läuft; noch nicht zum Mergen bereit.** Häkchen bei der
Implementierung bedeuten, dass der beschriebene Code vorhanden ist. Verifikation
wird getrennt erfasst und gilt nur für die genannte Revision und Testebene.
Quellcodetests, Workflow-Namen und sechs Testidentitäten beweisen keine sechs
laufenden Hosts.

Letzter Code-/Test-Prüfstand: `092dfd1c8937f9712c03da011e61f1e4eab31840`.
Der anschließende Dokumentationscommit benötigt eigene CI- und Sonar-Ergebnisse;
er erbt nicht den Erfolg eines früheren Heads.

Referenzen: [Vertrag und Migration](pr-382-event-contract.de.md) sowie
[Change Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.de.md).

## 1. Implementierung

- [x] I01: `common/include/msconnector/native_result.h` ergänzen: Direkte Byte-Append-Ergebnisse `0` und `1` dürfen fortfahren; andere Ergebnisse schlagen fehl. Phasenauswertung ist nur bei `1` erfolgreich. Eigene APR-, NGINX-, HTTP-, Common- und Datei-Lade-Verträge erhalten.
- [x] I02: Gemeinsame Append-/Finish-Prädikate in betroffenen Apache-Body-Filtern, HAProxy-Binding, Common Runtime und NGINX-Response-Body-Pfaden verwenden.
- [x] I03: Undokumentierte `msc_intervention()`-Rückgaben in Common Runtime und HAProxy zurückweisen; Bereinigung und Fehlerweitergabe erhalten.
- [x] I04: HAProxy-Response-Header-Bindingfehler auch bei disruptiver Entscheidung als Fehler erhalten.
- [x] I05: Dieselbe `event_protocol.h`-Ansicht für JSONL und Integritäts-Hash verwenden. Ursprüngliche Eingabevalidierung, Query-Redaktion, Zähler, Statusbeobachtungen und Transportflags erhalten.
- [x] I06: Technische Fehler in geänderten Apache-/Common-Ereignissen von Regelblockierungen unterscheiden; separate handgeschriebene Apache-JSON-Fallbacks entfernen.
- [x] I07: Typisierte NGINX-Response-Body-Fehlerereignisse ergänzen; erfolgreiches EOS nicht aus einem vor der Auswertung gesetzten Flag ableiten.
- [x] I08: `MSCONNECTOR_ERROR_MODSECURITY_FAILURE` auf `MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE` abbilden; andere Fehlerklassen erhalten.
- [ ] I09: Verbleibende native/API- und Request-Ereignispfade abschließen. Der erledigte NGINX-Teil unten beweist weder vollständige Request-Ereigniskonsistenz noch alle Integrationsrouten.
- [x] I09a: NGINX-Byte-Append akzeptiert gültige Teilübernahme; Datei-Laden behält die eigene strikte Rückgabeprüfung und kumulative Grenze. Request-Phasen erst nach nativem Erfolg abschließen und erneute Aufrufe nach Request-Fehlern terminal halten. Bis `fcbaca03` implementiert, in V13 geprüft.
- [ ] I10: Profilübergreifende Konsistenz von `off`/`safe`/`strict` einschließlich nativer und Hostfehler abschließen.
- [x] I10a: Negative späte NGINX-Interventionen und Phasen-/Steuerungsfehler bleiben technische Fehler vor der Safe-/Strict-Regelentscheidung. In `52445b18` implementiert, in V14 geprüft.
- [ ] I11: Konsistenz vom Erzeuger bis zur Ausgabe über alle Routen abschließen: Ereignis-IDs, Ursachen, angeforderte/beobachtete Aktionen, doppelte terminale Einträge sowie Öffnungs-/Schreib-/Kurzschreib-/Serialisierungsfehler.
- [x] I11a: Bekannte Regel-/Fehlerereignisse behandeln NULL, leere und `not_observable`-Transportwerte als fehlenden Nachweis. Unbeobachtete `actual_action` bleibt leer; unbeobachtete Regelinterventionen verwenden neutrales `MSCONN_EVENT_ENGINE_DECISION`. Nachweisfelder und Anwendungsereignisse bleiben erhalten.
- [x] I11b: Verpflichtende NGINX-Phase-4-Logfehler bleiben terminal. Deaktivierte/ungültige Ausgaben prüfen, terminale Schreibversuche begrenzen und nur synchron erzeugte Core-Fehlerantworten beim Wiedereintritt zulassen. Dies belegt keine globale Gleichheit der Logausgaben.
- [ ] I12: Direkte, Companion-, Middleware- und Sidecar-Routen getrennt prüfen; Fähigkeiten nicht aus gemeinsamem Parser oder Familiennamen ableiten.
- [x] I13: Begrenzte HAProxy-Rule-ID-Dekodierung und abhängigkeitsgeordnete Bereinigung auslagern, ohne Phasenreihenfolge, Interventionsabfrage oder Ressourcenbesitz zu ändern.
- [x] I14: NGINX-Chain-Checker und isolierte Mutationstests an den tatsächlichen terminalen Helfer anpassen; 96 vorhandene Tests erhalten und vier Regressionen ergänzen.
- [x] I15: HAProxy-Rule-ID-Adoption-Prüfungen an ausgelagerten Dekodierer und Aufrufstelle anpassen; acht isolierte Regressionstests in PR-Lint ergänzen. Dieser Schritt ändert kein natives Laufzeitverhalten.

## 2. Verifikation

- [x] V01: Rückgabetypen erzeugter C-Testdateien reparieren, ohne Compilerwarnungen oder Assertions abzuschalten.
- [x] V02: Ursprünglicher Native-/Event-Schritt bestand für `4f94f33d852f026e703f3237ed98826ae305719a` in [Lauf 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389).
- [x] V03: Kompilierte Tests des nativen Fehlerklassifizierers und CI-Anbindung ergänzen.
- [x] V04: NGINX-Quellcodeprüfungen für terminale Fehler, keine zweite Antwort nach Commit und keine Erfolgszählung nach fehlgeschlagenem Append erhalten.
- [x] V05: Fokussierte Native-/Event-/Klassifikations-/Beobachtungs-/Sonar-Prüfungstests und Phase-4-/Sicherheitsprüfungen bestanden am letzten Prüfstand; siehe Nachweistabelle. Frühere Ergebnisse für `039b7f12` bleiben historisch und sind kein End-Head-Nachweis.
- [ ] V06: Gemeinsame Adoption-/Mutationsverifikation des endgültigen Heads abschließen; eingegrenzte Reparaturen und Nachweise folgen unten.
- [x] V06a: Apache-Helferprüfungen und 16 Negativmutationen bestanden für `1709e1de` in [Job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579). Die Workflows `test-apache` und `test-common` bestanden auch für `092dfd1c`; dies belegt kein Live-Apache-Verhalten.
- [x] V06b: Alle 100 NGINX-Adoption-/Mutationstests bestanden für `f7aa2f2c` in [Job 106645456958](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836181/job/106645456958); der Schritt bestand erneut für `092dfd1c`. Exakte `FAIL:`-Diagnosen und Prüfungen der privaten Header-Testkopie bleiben vorgeschrieben.
- [ ] V07: Alle erforderlichen Prüfungen und Reviews des späteren Freigabe-Heads bestehen. Ausstehende Analysen und Laufzeitjobs sind keine grünen Nachweise.
- [ ] V08: Gleiche echte Hostfälle für Engine-`ProcessPartial`, Reject/Interventionen, leere Antworten, mehrere Chunks/ein EOS, explizite CSV-MIME-Auswahl, optionale Budgets und Engine-Fehler ausführen.
- [ ] V09: Späte Safe-/Strict-Ergebnisse und Fehler vor/nach Commit je unterstütztem Transport prüfen, einschließlich Client-Bytes, Abbruch/Reset, benachbarter Streams, Bereinigung und JSONL.
- [ ] V10: Metadatenlogs echter Routen, ungültige/übergroße Eingaben, fehlende Beobachtungen und fehlerhafte Ausgaben vergleichen.
- [x] V11: Beobachtungsregressionen gegen echten Common-JSONL-/Hash-Code kompilieren, einschließlich Redaktion und erhaltener Nachweise. Familiennamen in Testdateien sind keine unabhängigen Hostläufe.
- [x] V12: Acht kompilierte HAProxy-Auswertungs-/Bereinigungs-/Rule-ID-Tests und Binding-Compile-/Link-Prüfungen bestanden für `039b7f12` in [Job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189).
- [x] V13: Neun NGINX-Request-/Datei-Rückgaberegressionen bestanden für `092dfd1c`. Kontrollierte native/Host-Schnittstellen, kein Integrationstest des nativen Dateilesers.
- [x] V14: Neun NGINX-Spätfehler-/Wiedereintrittsregressionen bestanden für `092dfd1c`. Kontrollierte Host-/Log-Schnittstellen, keine vollständige HTTP-Transportmatrix.
- [x] V15: Acht HAProxy-Adoption-Regressionsprüfungen bestanden für `092dfd1c`: akzeptierter Ausgangsstand, Initialisierung, fehlgeschlagene/Null-Extraktion, Konvertierungsgrenzen, Kommentare, vorzeitige Rückgabe und fehlender Helferaufruf.

## 3. Sonar-Null-Befund-Vorgabe

- [x] S01: Nur lesende exakte Head-Null-Prüfung erhalten. Veraltete, fehlende, mehrdeutige, unfertige oder positive Befunde können nicht bestehen.
- [x] S02: Negative Gate-Tests und jobbezogenes `checks: read` erhalten; keine Scanner-Ausnahmen, akzeptierten Issues oder abgeschwächten Regeln.
- [x] S03: Historische Analyse von `039b7f12` meldete 0 neue Issues, 0 akzeptierte Issues, 0 Security Hotspots und 0 Annotationen in [Check 106450287547](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106450287547).
- [x] S03a: Exakte Head-Null-Prüfung bestand für `f7aa2f2c` im V06b-Job.
- [ ] S04: Für jede spätere Lieferung einschließlich abschließendem Dokumentationshead frischen exakten Sonar-Null-Nachweis einholen. Beim Erstellen dieses Dokuments war die neueste Analyse noch nicht bestätigt; S03/S03a nicht als Ergebnis eines späteren Heads verwenden.

Null Befunde bedeutet weder null historische Projekt-Issues noch null Duplikation
oder gemessene vollständige Testabdeckung. Diese Kennzahlen sind bei Verfügbarkeit
getrennt anzugeben.

## 4. Stand je Familie

| Familie | Implementierter Teil | Noch erforderlich |
| --- | --- | --- |
| Apache | Body-Prädikate, typisierte Fehler, Adoption-Prüfungen und Negativmutationen | End-Head-Prüfungen und native Host-/Log-Regressionsmatrix |
| NGINX | Request-/Response-Prädikate, eigene Datei-Rückgabebehandlung, Schutz bei späten technischen Fehlern/Wiedereintritt, Phase-4-Fehlerereignisse, reparierte Adoption-Tests | Vollständige typisierte Request-Ereignisse und übrige Routen-/Ausgabebehandlung; echte Host-/Transportnachweise |
| HAProxy | Binding-Prädikate, erhaltene Fehler, begrenzte Rule-ID-/Bereinigungshilfen und helferbezogene Adoption-Tests | Getrennte Verhaltens-/Ereignisnachweise für HTX und SPOE/SPOP/Companion |
| Envoy | Korrekte native Rückgaben über Common Runtime | Getrennte Verifikation von ext_proc und ext_authz/Response-Companion |
| Traefik | Korrekte native Rückgaben über Common Runtime | Verifikation von nativer Middleware/UDS und forwardAuth/Response-Companion |
| lighttpd | Korrekte native Rückgaben über Common Runtime | Getrennte Verifikation von Sidecar und nativen/gepatchten Profilen |

Nicht unterstützte Strict-Profile bleiben nicht unterstützt. Gemeinsame Semantik
bedeutet keine identischen Host-Rückgabezahlen, nativen Log-Präfixe oder erfundene
Abbruchfähigkeit.

## 5. Dokumentation und Lieferung

- [x] D01: Arbeit bleibt in Draft-PR #382; kein Merge oder direkter Master-Push.
- [x] D02: Zweisprachige EN/DE-Checklisten mit getrenntem Implementierungs-/Verifikationsstand pflegen.
- [ ] D03: Betroffene Connector-Anleitungen, Beispiele und Kompatibilitäts-/Versionierungsprüfung vor Freigabe abschließen.
- [x] D03a: Zweisprachigen Native-/Event-Vertrag und Migrationshinweise einschließlich Warnungen zur Auswerter-/Integritäts-Hash-Kompatibilität pflegen.
- [x] D04: Change Record und Checkliste mit tatsächlichen Commits und CI abgleichen; revisionsgebundene historische Nachweise erhalten.
- [ ] D05: Alle abschließenden Dokumentations-/Link-/Diff-/CI-Prüfungen fertigstellen und PR-/Branch-Heads bei Übergabe abgleichen.

## Zuletzt beobachtete Nachweise: 2026-09-22

[Lint-Job 106648735070](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893254/job/106648735070)
für `092dfd1c8937f9712c03da011e61f1e4eab31840` bestand folgende Einzelschritte:

| Befehl oder Gruppe | Ergebnis | Ebene |
| --- | --- | --- |
| Native Rückgaben, Ereignisse, Klassifikation, Beobachtungen und Sonar-Gate-Unit-Tests | Bestanden | 29 fokussierte Tests; nicht die entfernte Analyse selbst |
| `python -m unittest -v tests.test_nginx_request_native_results` | Bestanden | 9 Tests mit kontrollierten nativen/Host-Schnittstellen |
| `python -m unittest -v tests.test_nginx_late_error_results` | Bestanden | 9 kontrollierte Spätfehlertests |
| Phase-4-Migration und NGINX-Quellcodesicherheit | Bestanden | 33 Quellcode-Vertragstests |
| `python -m unittest -v tests.test_nginx_common_adoption` | Bestanden | 100 isolierte Adoption-/Mutationstests |
| `python -m unittest -v tests.test_haproxy_adoption_rule_id` | Bestanden | 8 isolierte Checker-Tests |
| Konfigurationsregressionen/-generierung/-semantik | Bestanden | Prüfung von Quellcode und erzeugter Referenz |

Der vorherige Lint-Fehler bei `f7aa2f2c` wurde auf zwei veraltete Schreibweisenprüfungen
für HAProxy-Rule-IDs zurückgeführt. Commit `092dfd1c` repariert diese Prüfungen und
ergänzt Negativtests; er unterdrückt keine Prüfung. Der NGINX-Syntax-/Trockenlaufschritt
in [Job 106648735305](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893302/job/106648735305)
sowie `test-common`, `test-apache` und `quick-framework-check` bestanden ebenfalls
an diesem Prüfstand. Diese Ergebnisse ersetzen ältere Fehlerbeschreibungen der
genannten Prüfungen, nicht die offenen Live-Host- oder End-Head-Anforderungen.

Beim Vorbereiten der Dokumentation standen die entfernte Sonar-Bestätigung und
das Gesamtergebnis des Lint-Jobs noch aus. Spätere Ergebnisse gehören zu ihrer
tatsächlichen SHA und sind aus GitHub abzulesen, nicht hieraus abzuleiten.
Wegen des fehlenden vorgeschriebenen RTK-Ausführungswrappers wurden keine lokalen
Projektbefehle, nativen Builds oder lokalen `git diff --check` ausgeführt.
Eine vollständige Laufzeitmatrix für sechs Familien wird nicht behauptet.
