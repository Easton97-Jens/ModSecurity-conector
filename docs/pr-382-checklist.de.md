# PR #382: Checkliste für gemeinsames Connector-Verhalten

**Sprache:** [English](pr-382-checklist.md) | Deutsch

[Draft-PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382)
verwendet `fix/unified-native-results-events-20260921`, ausgehend von
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Aktualisiert: 2026-09-21.

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
- [ ] V06b: NGINX-Chain-Fehlerprüfung und veraltete Mutationsfragmente reparieren. Negativabdeckung erhalten statt Diagnosen zu entfernen oder ungeprüfte Fehlerpfade zu akzeptieren.
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
- [ ] S04: Nach jeder weiteren Änderung, einschließlich des abschließenden Dokumentationscommits, die exakte Head-bezogene Null-Prüfung wiederholen. Endgültigen Head-Nachweis von S03 trennen.

Dies ist der neue Code betreffende PR-Befundbestand, keine Behauptung, dass der
historische Projektbestand oder die gemessene Testabdeckungslücke null ist.
Sonar meldete 0.0% Coverage für neuen Code; kompilierte Tests sind eigene Nachweise.

## 4. Stand je Familie

| Familie | Implementierter Teil | Noch erforderlich |
| --- | --- | --- |
| Apache | Body-Prädikate, typisierte Ereignisse, angepasste Adoption-Prüfungen und Negativmutationen | Vollständige Prüfungen des End-Heads und native Host-/Logregressionen |
| NGINX | Response-Prädikate und typisierte Fehlerereignisse | Request-/Datei- und späte Fehlerpfade, Adoption-Mutationen, Host-/Transportregressionen |
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

Der NGINX-Adoption-/Mutationsschritt bleibt fehlgeschlagen. Eine vollständige
Live-HTTP-/Transportmatrix für sechs Familien, ein lokaler nativer Build oder
ein lokales `git diff --check` werden nicht behauptet. Alle Testebenen und
offenen Punkte müssen ausdrücklich erkennbar bleiben.
