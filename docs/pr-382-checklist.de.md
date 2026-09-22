# PR #382: Checkliste für gemeinsames Connector-Verhalten

**Sprache:** [English](pr-382-checklist.md) | Deutsch

[Draft-PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382),
Branch `fix/unified-native-results-events-20260921`, Basis
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Aktualisiert: 2026-09-22.

**Implementierung läuft weiter; noch nicht zum Mergen bereit.** Implementierung
und Verifikation sind getrennt. Jedes Ergebnis gilt nur für die genannte Revision
und Testebene, nicht für alle Live-Hosts oder einen späteren Commit.

Code-/Test-Prüfstand: `47714de09bf1f9326862447f794194045828f29d`.
Letzte bestätigte Sonar-Null-Revision: `47714de09bf1f9326862447f794194045828f29d`.
Ein folgender Dokumentationscommit benötigt eigene CI-/Sonar-Bestätigung.
Die vier Hauptpunkte I09-I12 bleiben offen: erledigte Teilbereiche beweisen
keinen Abschluss aller nativen APIs, physischen Ausgaben und Integrationsrouten.

Referenzen: [Vertrag und Migration](pr-382-event-contract.de.md) und
[Change Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.de.md).

## 1. Implementierung

- [x] I01: Gemeinsame native Helfer akzeptieren nur `0`/`1` für direktes Byte-Append und nur `1` für Phasenerfolg. Eigene APR-, NGINX-, HTTP-, Common- und Datei-Lade-Verträge bleiben erhalten.
- [x] I02: Gemeinsame Prädikate in betroffenen Apache-Body-Filtern, HAProxy-Binding, Common Runtime und NGINX-Antwortpfaden.
- [x] I03: Common-/HAProxy-Interventionsrückgaben mit Bereinigung und Fehlerweitergabe validieren.
- [x] I04: HAProxy-Response-Header-Bindingfehler auch bei disruptiver Entscheidung erhalten.
- [x] I05: Kanonische Ereignisansicht für JSONL/Hash, ursprüngliche Eingabevalidierung und Query-Redaktion; Zähler und Beobachtungen erhalten.
- [x] I06: Technische Fehler von Regelblockierungen in geänderten Apache-/Common-Ereignissen trennen; handgeschriebene Apache-JSON-Fallbacks entfernen.
- [x] I07: Typisierte NGINX-Response-Body-Fehlerereignisse; erfolgreiches EOS nicht aus einem vor der Auswertung gesetzten Flag ableiten.
- [x] I08: Nativen Engine-Fehler auf ungültige Engine-Antwort abbilden und andere Fehlerklassen erhalten.
- [ ] I09: Verbleibende native/API- und typisierte Request-Ereignispfade abschließen; der NGINX-Teil unten ist keine vollständige Request-Ereigniskonsistenz.
- [x] I09a: NGINX-Teilübernahme von Bytes, separate strikte Datei-Rückgabebehandlung, kumulative Datei-/Body-Grenzen, Phasenabschluss nur nach Erfolg und terminaler Wiedereintritt nach Request-Fehlern. Bis `fcbaca03` implementiert; V13-Tests.
- [x] I09b: Typisierte NGINX-Request-Fehler erhalten erste Ursache/Status und einen Ereignisversuch, trennen Host-/URI-Fehler von echten Regeln und erlauben fehlenden Speicher bei gültigem leerem Body. Native Interventionsabfrage prüft exakte Rückgaben vor Klassifikation und Bereinigung. Bei `7fe606c5` vorhanden; erneute V17-Nachweise.
- [x] I09c: Nativer NGINX-Auditabschluss akzeptiert nur eins, markiert den Versuch vor Callbacks, erhält fehlgeschlagene Ergebnisse beim Wiedereintritt und bewahrt frühere Ursachen. Fehlender nativer Zustand erreicht die Engine nicht; kanonischer Abschlussfehler bleibt trotz erfolgreichen nativen Loggings ein Fehler. In `47714de0` implementiert; V17-Nachweis.
- [ ] I10: Profilübergreifende `off`-/`safe`-/`strict`-Konsistenz einschließlich nativer und Hostfehler abschließen.
- [x] I10a: Negative späte NGINX-Interventionen und Phasen-/Steuerungsfehler bleiben technische Fehler vor der Safe-/Strict-Regelentscheidung. In `52445b18` implementiert; V14-Tests.
- [x] I10b: Common-Fehlerstatus hat Vorrang; technische Fehler führen vor Antwortbeginn zur Ablehnung und danach zum I/O-Stopp, nicht zu erfolgreichem Safe-Log-only. Echte Common-Tests prüfen fünf Fehlerklassen über zehn registrierte Profile, zwei Vertragsmodi und beide Commit-Zustände. Das beweist für sich noch keine Adapter-I/O.
- [x] I10c: Echter NGINX-Collector/Dispatcher/P4-Aufrufer trennt gültige späte Safe-/Strict-Regeln von ungültigen nativen Rückgaben, erhält den nativen Off-Pfad und die Bereinigung. Fehlende echte Testabhängigkeit `http_status.c` in `1ce569e1` ergänzt, ohne die zehn ursprünglichen Assertions abzuschwächen.
- [ ] I11: Erzeuger-/Ausgabeparität abschließen: Ereignis-IDs/Ursachen, angeforderte/beobachtete Aktionen, doppelte terminale Ereignisse und Log-Öffnungs-/Schreib-/Kurzschreib-/Serialisierungsfehler.
- [x] I11a: NULL, leere und `not_observable`-Transportwerte sind fehlende Nachweise für bekannte Regel-/Fehlerereignisse. Unbeobachtete `actual_action` bleibt leer; neutrales `MSCONN_EVENT_ENGINE_DECISION` für unbeobachtete Regelinterventionen; Anwendungsereignisse und Nachweisfelder bleiben erhalten.
- [x] I11b: Verpflichtende NGINX-Phase-4-Logfehler bleiben terminal; deaktivierte/ungültige Ausgaben prüfen, terminale Schreibversuche und synchronen Core-Fehlerantwort-Wiedereintritt begrenzen. Dies belegt keine globale Ausgabegleichheit.
- [x] I11c: Fehlende-Beobachtung-Grenze auf Body-Limit-, Unsupported-Capability-, Client-Cancel- und Upstream-Disconnect-Ereignisse anwenden. Kategorie, phasenspezifische Ursache, beobachtete Kontrollen und Quelldaten erhalten. Echte JSONL-/Hash-Tests enthalten eine kompilierte Negativkontrolle mit entfernter Prüfung. In `3730eaa0` implementiert; V18-Nachweis.
- [ ] I12: Direkte, Companion-, Middleware- und Sidecar-Routen getrennt prüfen; Fähigkeit nicht aus Parser oder Familiennamen ableiten.
- [x] I13: Begrenzten HAProxy-Rule-ID-Dekodierer und abhängigkeitsgeordnete Bereinigung ohne geänderte Phasenreihenfolge oder Besitzverhältnisse auslagern.
- [x] I14: NGINX-Checker und isolierte Testkopien folgen dem terminalen Helfer; 96 Tests erhalten und vier Regressionen ergänzen.
- [x] I15: HAProxy-Checker folgt tatsächlichem begrenztem Dekodierer und Aufrufstelle; acht isolierte Regressionen in PR-Lint ergänzen. Keine native Laufzeitänderung in diesem Schritt.

### Konkrete verbleibende Implementierungsgrenzen

| Hauptpunkt | Verbleibende Grenze |
| --- | --- |
| I09 | Übrige native/Host-Fehlerausgänge außerhalb der abgeschlossenen NGINX-Pfade prüfen, einschließlich bislang nur durch Hostdiagnosen gemeldeter Fehler. Ein geprüftes natives Prädikat ist nicht automatisch ein typisiertes Ereignis bei jedem Aufrufer. |
| I10 | Für jeden nativen, Companion- und Middleware-Fehler das Erreichen des tatsächlichen Host-Steuerungspfads ohne erfolgreichen Policy-Rückfall prüfen. Common-Profiltests allein belegen dies nicht. |
| I11 | Apaches `apache_intervention_write_event()` und seine void-Ereignisaufrufer warnen bei Ausgabefehlern weiterhin ohne Rückgabe durch den vollständigen Hostablauf. Der Common-Ereignisabschluss von HAProxy SPOP ignoriert weiterhin den Erfolg von `fputs()`. Der Failed-Write-Marker der Common Runtime meldet frühere Ausgabefehler derzeit als Serialisierungs-/Ereignisgrößenfehler statt mit ursprünglicher I/O-Klasse. Dafür fehlen Quellcodeänderungen und Fehlerinjektionstests, nicht nur Dokumentation. |
| I12 | Getrennte Prüfungen aller direkten/Companion-/Middleware-/Sidecar-Routen einschließlich physischer Ausgaben und Host-Commit-/Abschlussbehandlung vervollständigen. Eine reine Request-Route nicht ohne ihren Companion als Response-vollständig markieren. |

## 2. Verifikation

- [x] V01: Erzeugte C-Rückgabetypen ohne Abschalten von Warnungen/Assertions reparieren.
- [x] V02: Ursprünglicher Native-/Event-Schritt bestand für `4f94f33d` in [Lauf 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389).
- [x] V03: Kompilierte native Fehlerklassifikationsregressionen und CI-Anbindung ergänzen.
- [x] V04: Quellcodeprüfungen für terminale Fehler, keine zweite Antwort nach Commit und keine Erfolgszählung nach fehlgeschlagenem Append erhalten.
- [x] V05: Fokussierte Native-/Event-/Klassifikations-/Beobachtungs-/Gate-Unit-Tests und Phase-4-/Sicherheitsprüfungen bestanden für `092dfd1c`; siehe historische Nachweistabelle.
- [ ] V06: Gemeinsame Adoption-/Mutationsverifikation des endgültigen Freigabe-Heads abschließen.
- [x] V06a: Apache-Helferprüfungen und 16 Negativmutationen bestanden für `1709e1de` in [Job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579). `test-apache` und `test-common` bestanden für `092dfd1c`; dies sind keine Live-Apache-Nachweise.
- [x] V06b: Alle 100 NGINX-Adoption-Tests bestanden für `f7aa2f2c` in [Job 106645456958](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836181/job/106645456958) sowie erneut für `092dfd1c`.
- [ ] V07: Jede erforderliche Prüfung und Review des endgültigen Freigabe-Heads bestehen.
- [ ] V07a: Unabhängigen Secret-Scan-Fund für `91f07e12` aus [Job 106651564952](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35698779824/job/106651564952) klären. Das verfügbare Protokoll meldet einen Fund ohne Stelle; keine Einstufung als Fehlalarm oder Ausnahme ist genehmigt. Der Secret-Scan-Workflow schlägt auch bei `47714de0` fehl.
- [ ] V08: Gleiche echte Hostfälle für Engine-ProcessPartial/Reject, leere Antworten, mehrere Chunks/ein EOS, CSV-MIME, Budgets und native Fehler ausführen.
- [ ] V09: Unterstützte späte Safe-/Strict-Ergebnisse und Fehler vor/nach Commit, Client-Bytes, Resets, benachbarte Streams und Bereinigung prüfen.
- [ ] V10: Metadatenlogs echter Routen, ungültige/übergroße Eingaben, fehlende Beobachtungen und fehlerhafte Ausgaben vergleichen.
- [x] V11: Kompilierte echte Common-JSONL-/Hash-Beobachtungstests erhalten Redaktion/Nachweise; sechs Testnamen sind keine sechs Hostläufe.
- [x] V12: Acht kompilierte HAProxy-Helfertests und Binding-Compile-/Link-Prüfungen bestanden für `039b7f12` in [Job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189).
- [x] V13: Neun NGINX-Request-/Datei-Rückgabetests bestanden für `092dfd1c`, mit kontrollierten Host-/nativen Schnittstellen, nicht als nativer Dateileser-Integrationstest.
- [x] V14: Neun NGINX-Spätfehler-/Wiedereintrittstests bestanden für `092dfd1c`, keine vollständige HTTP-Transportmatrix.
- [x] V15: Acht HAProxy-Adoption-Tests bestanden für `092dfd1c`, einschließlich akzeptiertem Ausgangsstand und unsicheren Dekodierer-/Aufrufmutationen.
- [x] V16: Zweisprachige Change-Record-/Vorlagenprüfung bestand erneut bei `47714de0` im unten verlinkten aktuellen Nachweisjob; kein Dokumentationsprüfer wurde abgeschwächt.
- [x] V17: Bei `47714de0` bestand der Request-/Native-Schritt alle fünf Module: Request-Rückgaben, typisierte Request-Fehler, Kontextzählung, zehn echte Interventionskettentests und acht neue native Logging-Tests. Der fehlgeschlagene Aufbau der nativen Kette bei `7fe606c5` wurde durch Verlinkung der tatsächlichen HTTP-Status-Implementierung korrigiert.
- [x] V18: Bei `47714de0` bestand der erweiterte Common-/Native-/Event-/Profilschritt einschließlich zehn Beobachtungstests und kompilierter Nicht-Regel-Negativkontrolle mit entfernter Prüfung. Spätfehler- und Phase-4-/Sicherheitsschritte bestanden separat.

## 3. Sonar-Null-Befund-Vorgabe

- [x] S01: Nur lesende exakte Head-/Anbieter-Null-Prüfung erhalten; fehlende, veraltete, mehrdeutige, unfertige und positive Ergebnisse zurückweisen.
- [x] S02: Negative Gate-Tests und jobbezogenes `checks: read` erhalten; keine Scanner-Ausnahmen, akzeptierten Issues oder schwächeren Regeln.
- [x] S03: Historische Analyse von `039b7f12` meldete 0 neue/akzeptierte Issues, Hotspots und Annotationen in [Check 106450287547](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106450287547).
- [x] S03a: Exakte Head-Null-Prüfung bestand für `f7aa2f2c` im V06b-Job.
- [x] S03b: [Check 106651947571](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106651947571) bestätigt 0 neue Issues, 0 akzeptierte Issues, 0 Hotspots und 0 Annotationen für `91f07e124fe09056dc46dc59d65693f406b4b1a1`.
- [x] S03c: [Check 106837589312](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106837589312) bestätigt dieselben vier Null-Zähler für exakt `47714de09bf1f9326862447f794194045828f29d`.
- [ ] S04: Frische exakte Sonar-Null-Prüfung für jede spätere Lieferung einschließlich Dokumentationsänderungen bestätigen. Keine frühere Analyse erfüllt eine spätere SHA.

Sonar meldet für `47714de0` 0.1% Duplikation im neuen Code und 0.0% Coverage.
Befunde, Duplikation und Coverage sind getrennte Kennzahlen. Sonar null erledigt
weder V07a noch beweist es null historische Issues im gesamten Projekt.

## 4. Stand je Familie

| Familie | Implementierter Teil | Offen |
| --- | --- | --- |
| Apache | Body-Prädikate, typisierte Fehler, Helfer-Adoption-/Negativprüfungen | Weitergabe physischer Ausgabefehler und native Host-/Log-Matrix des End-Heads |
| NGINX | Typisierte Request-/Response-Fehler, native Collector-Validierung, eigene Dateibehandlung, Spätfehler-/Wiedereintrittsschutz, einmaliger nativer Auditabschluss | Übriger Ausgaben-/Erzeugervergleich und echte Transportnachweise |
| HAProxy | Binding-Rückgaben, Fehlerweitergabe, Rule-ID-/Bereinigungshilfen, Adoption-Tests | Weitergabe von SPOP-Ereignisschreibfehlern und getrennte HTX-/SPOE-/Companion-Verhaltens-/Log-Nachweise |
| Envoy | Korrekte native Rückgaben und Fehlerpolicy über Common Runtime | Erhalt ursprünglicher Ausgabefehler und getrennte ext_proc-/ext_authz-Companion-Verifikation |
| Traefik | Korrekte native Rückgaben und Fehlerpolicy über Common Runtime | Erhalt ursprünglicher Ausgabefehler und Middleware-/UDS-/forwardAuth-Companion-Verifikation |
| lighttpd | Korrekte native Rückgaben und Fehlerpolicy über Common Runtime | Erhalt ursprünglicher Ausgabefehler und Sidecar-/nativer-/gepatchter Profilvergleich |

Nicht unterstützte Strict-Profile bleiben nicht unterstützt. Gemeinsame Semantik
bedeutet keine identischen Host-Zahlen, nativen Log-Präfixe oder erfundene Abbruchfähigkeit.

## 5. Dokumentation und Lieferung

- [x] D01: Arbeit bleibt in Draft-PR #382; kein Merge oder Master-Push.
- [x] D02: EN/DE-Checkliste mit getrennter Implementierung und Verifikation pflegen.
- [ ] D03: Connector-Anleitungen/Beispiele und Kompatibilitäts-/Versionsprüfung abschließen.
- [x] D03a: Zweisprachigen Native-/Event-Vertrag und Auswerter-/Hash-Migrationswarnungen pflegen; die neuen Fortsetzungsberichte unten beschreiben zusätzliches Beobachtungs- und natives Auditverhalten.
- [x] D04: Checkliste und Change Records mit tatsächlichen Commits/Ergebnissen abgleichen; historische Nachweise im Bericht und in Git erhalten.
- [ ] D05: End-Head-Dokumentations-/Link-/Diff-/CI-Prüfungen und PR-/Branch-Abgleich abschließen.

## Aktuelle Fortsetzungsnachweise

[Lint-Job 106836835538](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35754528427/job/106836835538)
für `47714de09bf1f9326862447f794194045828f29d` bestand bei letzter Prüfung
Zweisprachigkeitsvalidierung sowie alle fokussierten Common-/Native-/Request-/
Logging-/Spätfehler-/Sicherheitsschritte. Diese Beobachtung belegte noch keinen
abschließenden Gesamtstatus des Jobs. Der frühere vollständige
[Lint-Lauf 35753875384](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35753875384)
bestand bei `1ce569e1afce55e17c767e1e06b0266874fe8c3e`; er belegt keine späteren
nativen Logging-Änderungen. Die physischen Ausgabelücken der Implementierungstabelle
bleiben unabhängig von grünen fokussierten Tests offen.

Fortsetzungsberichte:
[Beobachtungsparität](../reports/audits/change-records/CR-20260922-pr382-nonrule-observation.de.md),
[Verlinkung der nativen Kette](../reports/audits/change-records/CR-20260922-pr382-chain-link.de.md),
[natives Auditlogging](../reports/audits/change-records/CR-20260922-pr382-native-logging.de.md).
Ihre zum Vorbereitungszeitpunkt ausstehenden Ergebnisse werden nur durch die
konkreten revisionsgebundenen Nachweise oben ersetzt, nicht durch eine pauschale
Abschlussbehauptung.

## Historische revisionsgebundene Nachweise

[Lint-Job 106648735070](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893254/job/106648735070)
für `092dfd1c8937f9712c03da011e61f1e4eab31840` bestand folgende Einzelgruppen:

| Gruppe | Ergebnis | Ebene |
| --- | --- | --- |
| Native-/Event-/Klassifikations-/Beobachtungs-/Sonar-Gate-Unit-Tests | 29 bestanden | Nicht die entfernte Sonar-Analyse |
| NGINX-Request-/Datei-Rückgaben | 9 bestanden | Kontrollierte Host-/native Tests |
| NGINX-Spätfehler/Wiedereintritt | 9 bestanden | Kontrollierte Host-/Log-Tests |
| Phase-4- und NGINX-Sicherheitsverträge | 33 bestanden | Quellcodeverträge |
| NGINX-Adoption/Mutationen | 100 bestanden | Isolierte Quellcodemutationen |
| HAProxy-Rule-ID-Adoption | 8 bestanden | Isolierte Checker-Tests |
| Konfigurationsreferenzen | Bestanden | Regression/Generierung/Semantik |

`test-common`, `test-apache`, `quick-framework-check` und `test-nginx` bestanden
ebenfalls für `092dfd1c`; NGINX-Syntax-/Trockenlaufnachweise stehen in
[Job 106648735305](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893302/job/106648735305).
Der vorherige f7aa-Lint-Fehler entstand durch veraltete HAProxy-Prüfungen, in
`092dfd1c` ohne Unterdrückung repariert. Das folgende Dokumentationsupdate machte
V16 und den separaten V07a-Sicherheitsfund sichtbar. Sein Sonar-Ergebnis steht
getrennt in S03b; vollständig grüne Gesamt-CI wird nicht behauptet.

Wegen des fehlenden vorgeschriebenen RTK-Wrappers wurden keine lokalen
Projektbefehle/Builds oder lokalen `git diff --check` ausgeführt. Verifikation
nutzt GitHub-CI und entfernte Commitvergleiche. Vollständige Live-Host-/
Transportverifikation für sechs Familien bleibt offen.
