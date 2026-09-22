# PR #382: Checkliste für gemeinsames Connector-Verhalten

**Sprache:** [English](pr-382-checklist.md) | Deutsch

[Draft-PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382)
verwendet `fix/unified-native-results-events-20260921`, ausgehend von
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Aktualisiert: 2026-09-22.

**Stand: Implementierung läuft; noch nicht zum Mergen bereit.** Ein Häkchen bei
Implementierung bedeutet, dass der beschriebene Code vorhanden ist, nicht, dass
jeder Host einen Integrationstest bestanden hat. Die Verifikation hat eigene
Häkchen. Nachweise gelten nur für die genannte Revision und Testebene. Erfolge
anderer Connectoren, frühere grüne Prüfungen und erzeugte Berichte ersetzen
keine fehlenden Laufzeitnachweise.

Vertrags- und Migrationsreferenz: [native Rückgaben und Ereignisse](pr-382-event-contract.de.md).

## 1. Implementierung

- [x] I01: `common/include/msconnector/native_result.h` ergänzen: Direkte Byte-Append-Ergebnisse `0` und `1` dürfen fortfahren; andere Ergebnisse schlagen fehl. Eine Phasenauswertung ist nur bei `1` erfolgreich. Dies gilt nicht für APR-/NGINX-/HTTP-/Common-Rückgaben oder Datei-Lade-APIs.
- [x] I02: Die gemeinsamen Append-/Finish-Prädikate in betroffenen Apache-Body-Filtern, HAProxy-Binding, Common Runtime und NGINX-Response-Body-Pfad verwenden.
- [x] I03: Undokumentierte `msc_intervention()`-Rückgaben in Common Runtime und HAProxy-Binding zurückweisen; Bereinigung und Fehlerweitergabe erhalten.
- [x] I04: Einen HAProxy-Response-Header-Bindingfehler auch bei einer zusätzlich disruptiven Entscheidung als Fehler erhalten.
- [x] I05: `event_protocol.h` für dieselbe kanonische JSONL- und Integritäts-Hash-Ansicht verwenden. Ursprüngliche Eingabevalidierung, Query-Redaktion, Bytezähler, Statusbeobachtungen und Transportflags erhalten.
- [x] I06: Technische Fehler in geänderten Apache-/Common-Ereignispfaden von Regelblockierungen unterscheiden; separate handgeschriebene Apache-JSON-Fallbacks entfernen.
- [x] I07: Typisierte NGINX-Response-Body-Fehlerereignisse ergänzen. Erfolgreiches EOS nicht aus einem vor nativer Auswertung gesetzten Flag ableiten.
- [x] I08: `MSCONNECTOR_ERROR_MODSECURITY_FAILURE` in `common/src/modsecurity_engine.c` auf `MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE` abbilden; andere Fehlerklassen erhalten.
- [ ] I09: NGINX-Request-Body-/Dateipfade und verbleibende native API-Pfade abschließen, ohne I/O-Fehler mit `ProcessPartial` zu verwechseln.
- [ ] I10: Profilübergreifenden Vergleich von `off`/`safe`/`strict` abschließen. Insbesondere darf kein technischer Fehler zu einer erfolgreichen Safe-`log_only`-Entscheidung werden.
- [ ] I11: Konsistenz vom Erzeuger bis zur Ausgabe abschließen: Ereignis-IDs, Ursachen, angeforderte gegenüber beobachteten Aktionen, doppelte terminale Einträge und Fehler beim Öffnen, Schreiben, verkürzten Schreiben und Serialisieren.
- [x] I11a: Bei bekannten Regel-/technischen Fehlerereignissen NULL, leere und `not_observable`-Transportergebnisse als fehlende Beobachtung behandeln. Unbeobachtete `actual_action` leeren; bei unbeobachteten Regelinterventionen eine neutrale `MSCONN_EVENT_ENGINE_DECISION`-Meldung verwenden. Ursprüngliche Nachweisfelder und Anwendungsereignisse erhalten.
- [ ] I12: Alle direkten, Companion-, Middleware- und Sidecar-Pfade getrennt prüfen; Unterstützung nicht aus gemeinsamem Parser oder Familiennamen ableiten.
- [x] I13: HAProxy-Interventions-/Auswertungskomplexität durch ausgelagerte begrenzte Rule-ID-Dekodierung und abhängigkeitsgeordnete Bereinigung reduzieren. Interventionsabfrage, Phasenreihenfolge, Logging und Ressourcenbesitz erhalten.

## 2. Verifikation

- [x] V01: Doppelte C-Rückgabetypen in erzeugten Testdateien reparieren; Compilerwarnungen und Assertions erhalten.
- [x] V02: Ursprünglichen Native-Result-/Event-Protocol-Schritt für `4f94f33d852f026e703f3237ed98826ae305719a` in [Lauf 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389) nachweisen.
- [x] V03: Kompilierte `tests/test_native_error_classification.py` ergänzen und in den fokussierten CI-Schritt einbinden.
- [x] V04: NGINX-Upstream-Quellcodeprüfungen für gemeinsame Prädikate anpassen; terminalen Fehler, Abbruch vor Rückgabe, keine Ersatzantwort nach Commit und keine erfolgreiche Bytezählung bei Append-Fehler weiter verlangen.
- [x] V05: Erweiterte Common-/Native-Result-/Fehler-/Beobachtungs-/Sonar-Gate-Tests und Phase-4-/NGINX-Quellcodesicherheitstests für `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` in [Lauf 35634888258, Job 106449766690](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888258/job/106449766690) bestätigen. Diese Einzelschritte bestanden; der Gesamtjob scheiterte an NGINX-Adoption-Mutationen.
- [ ] V06: Apache- und NGINX-Adoption-/Mutationsreparaturen vollständig abschließen.
- [x] V06a: Apache-Helfer-Adoption-Prüfungen reparieren und vorhandene Negativmutationen erhalten. Invertierte Append-/Phasenbedingungen, fehlende Serialisierungsrückgabe und falsche Regelblockierung technischer Fehler ergänzen. Alle 16 Mutationstests und eingegrenzten Prüfungen bestanden für `1709e1def4706f0124d56fc687b3faf1fd8e2946` in [Lauf 35633647191, Job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579); der Job scheiterte danach am NGINX-Checker. Eine spätere semantisch gleiche lineare Statusprüfung gehört zu `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` und benötigt ihre eigene vollständige Validierung.
- [x] V06b: NGINX-Chain-Fehlerprüfung und veraltete Mutationsfragmente reparieren. Tatsächlichen privaten Phase-4-Fehlerheader in isolierte Testkopien übernehmen, alle 96 vorhandenen Tests erhalten, vier Regressionen ergänzen und exakte `FAIL:`-Diagnosen verlangen. Der vollständige Mutationsschritt bestand für `f7aa2f2ccf929f226a6b0ad7b9ff0700b71c367d` in [Lauf 35696836181, Job 106645456958](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836181/job/106645456958). Der gesamte Lint-Job scheiterte später; siehe datierte Fortsetzung unten.
- [ ] V07: Alle erforderlichen Prüfungen und Reviews des endgültigen PR-Heads bestehen. Die Gesamt-CI ist nicht grün.
- [ ] V08: Gleiche echte Host-Fälle für Engine-`ProcessPartial`, Engine-Reject/Interventionen, leere Antworten, mehrere Chunks mit einem EOS, explizite CSV-MIME-Auswahl, optionale Budgets und Engine-Fehler ausführen.
- [ ] V09: Späte Safe-/Strict-Ergebnisse und Fehler vor/nach Commit je unterstütztem Transport prüfen; Client-Bytes, Abbruch/Reset, Überleben benachbarter Streams, Bereinigung und JSONL statt nur HTTP-Status beobachten.
- [ ] V10: Metadatenlogs jeder echten Integrationsroute vergleichen, einschließlich ungültiger/übergroßer Metadaten, fehlerhafter Ausgaben und fehlender Transportbeobachtungen.
- [x] V11: `tests/test_event_transport_observation.py` gegen echten Common-JSONL-/Hash-Code kompilieren und ausführen. Geprüft werden fehlende Beobachtung, erhaltene Nachweise, Idempotenz, Redaktion und beobachtete Safe-/Abbruchkontrollen. Sechs Familiennamen sind Testidentitäten, keine sechs laufenden Hosts.
- [x] V12: Alle acht extrahierten HAProxy-Auswertungs-/Bereinigungs-/Rule-ID-Tests sowie die bestehende Compile-/Link-Kompatibilitätsprüfung für `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` in [Lauf 35634888103, Job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189) ausführen.

## 3. Sonar-Null-Befund-Vorgabe

- [x] S01: Eine exakte Head-bezogene, nur lesende Null-Befund-Prüfung ergänzen, statt ein grünes Quality Gate mit Befunden zu akzeptieren. Fehlende, veraltete, mehrdeutige oder unfertige Nachweise können nicht bestehen.
- [x] S02: Die Prüfung testen, einschließlich ungültiger Identität vor Netzwerkzugriff, sicherer begrenzter Annotation-Ausgabe, falschem Anbieter, unfertiger Analyse und positiven Befundzählern. `checks: read` auf Jobebene belassen.
- [x] S03: Für `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` **0 neue Issues, 0 akzeptierte Issues, 0 Security Hotspots und 0 Annotationen** in [Sonar-Check 106450287547](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106450287547) bestätigen. Die exakte Head-bezogene Null-Befund-CI-Prüfung bestand ebenfalls im V05-Job. Für dieses Ergebnis wurden keine Issues akzeptiert, verborgen oder ausgenommen.
- [x] S03a: Dieselben vier Null-Zähler für `f7aa2f2ccf929f226a6b0ad7b9ff0700b71c367d` in [Sonar-Check 106645541548](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106645541548) bestätigen. Die exakte Head-bezogene Null-Befund-Prüfung bestand im V06b-Job.
- [ ] S04: Nach jeder weiteren Änderung, einschließlich des abschließenden Dokumentationscommits, die exakte Head-bezogene Null-Prüfung wiederholen. Endgültigen Head-Nachweis von S03 und S03a trennen.

Dies ist der neue Code betreffende PR-Befundbestand, keine Behauptung, dass der
historische Projektbestand oder die gemessene Testabdeckungslücke null ist.
Sonar meldete 0.0% Coverage für neuen Code; kompilierte Tests sind eigene Nachweise.

## 4. Stand je Familie

| Familie | Implementierter Teil | Noch erforderlich |
| --- | --- | --- |
| Apache | Body-Prädikate, typisierte Ereignisse, angepasste Adoption-Prüfungen und Negativmutationen | Vollständige Prüfungen des End-Heads und native Host-/Logregressionen |
| NGINX | Response-Prädikate, typisierte Fehlerereignisse und reparierte Adoption-/Mutationstests | Verbleibender Request-/Ereignis- und Routenabschluss, separate Syntaxprüfung, Host-/Transportregressionen |
| HAProxy | Direkte Binding-Prädikate, Fehlerweitergabe, begrenzte Rule-ID-/Bereinigungsstruktur | Getrennte Verhaltens-/Ereignisnachweise für HTX und SPOE/SPOP/Companion |
| Envoy | Native Rückgabekorrektur über Common Runtime | Getrennte Verifikation von ext_proc und ext_authz/Response-Companion |
| Traefik | Native Rückgabekorrektur über Common Runtime | Verifikation von nativer Middleware/UDS und forwardAuth/Response-Companion |
| lighttpd | Native Rückgabekorrektur über Common Runtime | Getrennte Verifikation von Sidecar und nativen/gepatchten Profilen |

Nicht unterstützte Strict-Profile bleiben nicht unterstützt, bis echte
Hostfähigkeit implementiert und getestet ist. Gemeinsame Semantik bedeutet
weder identische Host-Rückgabezahlen noch Log-Präfixe oder erfundene
Abbruch-/Resetfähigkeiten.

## 5. Dokumentation und Lieferung

- [x] D01: Arbeit in Draft-PR #382 belassen; kein Merge oder direkter `master`-Push.
- [x] D02: Vollständige EN/DE-Checklisten mit getrenntem Implementierungs-/Verifikationsstand pflegen.
- [ ] D03: Alle betroffenen Connector-Anleitungen, Beispiele und Kompatibilitäts-/Versionierungsprüfungen vor der Freigabe vervollständigen.
- [x] D03a: Zweisprachige Native-Result-/Event-Vertragsanleitung mit fehlender Beobachtung, Migrationshinweisen für Auswerter, Integritäts-Hash-Kompatibilitätswarnungen und Sonar-Null-Vorgabe ergänzen.
- [x] D04: Zweisprachigen [Change Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.de.md) und PR-Fortschritt mit tatsächlichen revisionsgebundenen Ergebnissen aktualisieren.
- [ ] D05: Abschließende Dokumentations-/Link-/Diff-Prüfungen und alle Prüfungen des endgültigen Heads fertigstellen. Branch- und PR-Head bei Übergabe abgleichen.

## Beobachtete Befehle und Ergebnisse

Die folgenden beiden Befehle bestanden als einzelne CI-Schritte für die V05-Revision:

```sh
python -m unittest -v tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_event_transport_observation tests.test_sonar_zero_gate
python -m unittest -v tests.test_phase4_migration_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract
```

Die folgenden Befehle bestanden für die V12-Revision:

```sh
python3 -m unittest -v tests.test_haproxy_binding_refactor
python3 tests/test_haproxy_libmodsecurity_compat.py
```

Die folgende exakte Head-Prüfung bestand für die S03-Revision:

```sh
python ci/checks/common/check-sonar-zero.py
```

## Fortsetzung 2026-09-22: NGINX-Adoption-Mutationen

Getestete Revision: `f7aa2f2ccf929f226a6b0ad7b9ff0700b71c367d`.
Dieser Schritt ändert nur den NGINX-Adoption-Checker und seine Mutationstests,
keinen Laufzeitcode, keine Workflows, Abhängigkeiten oder Sicherheitsrichtlinien.
Eine zwischenzeitlich eingegangene identische Checker-Korrektur unter
`7bd3b2355c84bc6bd630de6b19ea6115b5eb64f2` blieb erhalten; der Testkopie-Commit
baut ohne Force-Push darauf auf.

Im V06b-CI-Job bestand `python -m unittest -v tests.test_nginx_common_adoption`.
Neue Regressionen prüfen die byteidentische Kopie des privaten Headers, dessen
Fehlen, ein verbotenes Makro darin und verworfene Ergebnisse der terminalen
Fehlerweiterleitung. Negativfälle verlangen Exitstatus 1 und ihre genaue
`FAIL:`-Zeile; ein fremder Fehler oder passender `PASS:`-Text genügt nicht.
Request-Native-, Spätfehler-/Wiedereintritts-, Phase-4-/Sicherheits-,
Konfigurationsreferenz- und Sonar-Null-Schritte bestanden für diese Revision
 ebenfalls.

| Nachweisebene | Beobachtetes Ergebnis | Einschränkung |
| --- | --- | --- |
| Vollständiger NGINX-Adoption-/Mutationsschritt | `passed` im V06b-Job | Quellcodevertrag und isolierte Mutationen, kein echter Hostlauf |
| NGINX-Scaffold- und Common-Vertragsprüfungen | `passed` in [Lauf 35696836186, Job 106645456976](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836186/job/106645456976) | Danach scheiterte die separate native Syntax-/Regressionsprüfung |
| Native NGINX-Syntax-/Regressionsprüfung | `failed` im selben NGINX-Job | Eine Request-Body-Assertion erwartet noch `if (ret != 1)`; ihre Quelldatei wurde in diesem Schritt nicht repariert |
| Gesamt-Lint | `failed` im V06b-Job | Späterer Fehler bei `Run lightweight lint`; der bestandene Mutationsschritt belegt dessen Ursache nicht |
| Exakte Head-Sonar-Analyse | `passed`, vier Null-Zähler in S03a | Gilt nur für die getestete SHA, nicht für einen späteren Dokumentationshead |

V06b ist auf seiner genannten Nachweisebene abgeschlossen. V06 bleibt für die
vollständige gemeinsame Adoption-Validierung offen; V07 sowie Laufzeit-/Profil-
kriterien bleiben ebenfalls offen. Eine vollständige Live-HTTP-/Transportmatrix
für sechs Familien, ein lokaler nativer Build oder ein lokales `git diff --check`
werden nicht behauptet. Der vorgeschriebene lokale RTK-Ausführungspfad stand
nicht zur Verfügung; validiert wurde mit GitHub-CI. Ein späterer Dokumentations-
commit benötigt eigene frische Prüfungen, statt diese Ergebnisse zu übernehmen.
