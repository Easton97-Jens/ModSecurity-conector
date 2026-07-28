# Change Record: Parent-Lighttpd-Harness-JSONL-Validierungs-Deduplizierungskandidat

**Sprache:** [English](CR-20260727-sonar-lighttpd-harness-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-lighttpd-harness-duplication |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Lokaler Parent-Kandidat für den erhaltenen 22+22 duplizierten Parser-/Normalizer-Quelltextblock. Es wird kein externes SonarQube-Cloud-Issue, Quality Gate oder Erfolgsergebnis behauptet. |
| Grenze | Ausschließlich Parent-Lighttpd-Harness-Quelltext/-Tests, dieses englisch/deutsche Change-Record-Paar und seine Indizes. Framework, MRTS, Gitlinks, Scanner-Konfiguration, Suppressions und externer Issue-Status bleiben unverändert. |
| Framework-Beobachtung | Read-only `git submodule status modules/ModSecurity-test-Framework` beobachtete `47e50e7bc43ba7a3b5bad1a9448111794f664cc0 modules/ModSecurity-test-Framework (heads/master)` am Parent-Gitlink. Es wird keine Framework-Source-, Gitlink- oder Delivery-Änderung behauptet. |
| Delivery-Status | `Draft` Delivery steht aus; der beobachtete Kandidat ist lokal und unstaged. Es werden kein Commit, Push, Pull Request, GitHub CI, gehostete SonarQube-Cloud-Analyse oder Merge behauptet. |

## Motivation und Problemstellung

`connectors/lighttpd/harness/write_patched_first_byte_metadata.py` und
`connectors/lighttpd/harness/write_patched_lifecycle_results.py` enthielten
den gleichen 22+22 duplizierten JSONL-Parser-/Normalizer-Quelltextblock. Der
lokale Kandidat teilt nur JSONL-Objektladen, P4-Phasenaliase und die bestehende
nichtnegative `int()`-Koezierung. Er erweitert weder den P4-Event-Vertrag noch
ändert er die Output-Schemas der Aufrufer.

Die betroffene Eingabe ist lokale JSONL-Evidence. Leere Zeilen werden weiter
ignoriert; jede nichtleere Zeile muss zu einem JSON-Objekt dekodieren. Der
Kandidat zentralisiert diese primitive Behandlung, ohne fehlerhafte,
nichtobjektartige oder ungültige Zählereingaben in Erfolgsfälle zu überführen.

## Akzeptanzkriterien

- Nur den gleichwertigen 22+22 Parser-/Normalizer-Block durch die geteilten
  Helper `load_events`, `phase_is_four` und `nonnegative` ersetzen.
- Die Fehlerformulierung jedes Aufrufers über sein lokales `NON_OBJECT_ERROR`-
  Template erhalten: `"{path}:{line_number}: event must be an object"` und
  `"{path}:{line_number} is not an object"`.
- Unterschiedliche lokale P4-Selektoren in `safe_host_action` und
  `safe_phase4_events` erhalten; kein Selektor wird geteilt oder gelockert.
- Fehlerhafte JSONL, Nichtobjekt-Records, Boolean- und negative Zähler,
  `body_bytes_inspected` größer als `body_bytes_seen` sowie null, falsche oder
  mehrere P4-Kandidaten als Fehler beibehalten.
- Englische/deutsche Change Records und Indizes gleichwertig halten,
  beobachtete lokale Source-, Lifecycle-Contract-, Dokumentations- und
  Whitespace-Validierung festhalten und nicht beobachtete Runtime-, gehostete
  und Delivery-Ergebnisse wahrheitsgemäß darstellen.

## Implementierungsentscheidung und Begründung

Der Kandidat fügt
`connectors/lighttpd/harness/patched_event_validation.py` für die drei
gleichwertigen Primitive hinzu. `phase_is_four` behält die bestehenden Aliase
`4`, `phase4` und `response_body`, einschließlich der bestehenden
Bindestrich-zu-Unterstrich-Normalisierung. `nonnegative` weist weiterhin
`bool` und negative Werte zurück und verwendet für andere akzeptierte Werte
die bestehende `int()`-Konvertierung; fraktionale Koezierung wird durch diese
Deduplizierung daher nicht geändert.

`load_events` akzeptiert das aufrufergesteuerte `non_object_error`-Template,
statt neuen Text auszuwählen. Es ruft weiterhin `json.loads` direkt auf,
sodass fehlerhafte JSONL weiterhin den Parserfehler zeigt. Die P4-Prädikate
bleiben in ihren jeweiligen Writern, weil ihre erforderlichen Felder nicht
identisch sind.

`connectors/lighttpd/tests/test_patched_event_validation.py` ist im lokalen
Kandidaten als direkter Regressionstest für Aliase, Schemas, Parser- und
Nichtobjektfehler, Zählereinschränkungen und Kandidatenkardinalität vorhanden.
Dieser Record behandelt die Existenz des Tests nicht als ausgeführtes
Source-Testergebnis. Die primäre Implementierungsvalidierung führte dieses
Modul anschließend zusammen mit
`connectors.lighttpd.tests.test_patched_host_contract` aus; das beobachtete
Ergebnis wird unter `## Ausgeführte Befehle` festgehalten und nicht aus der
Existenz des Tests abgeleitet.

## Geänderte Dateien

- `connectors/lighttpd/harness/patched_event_validation.py` — neuer geteilter
  JSONL- und Primitive-Validierungs-Helper-Kandidat.
- `connectors/lighttpd/harness/write_patched_first_byte_metadata.py` —
  importiert die geteilten Primitive und behält `safe_host_action` sowie seine
  Diagnose bei.
- `connectors/lighttpd/harness/write_patched_lifecycle_results.py` —
  importiert die geteilten Primitive und behält `safe_phase4_events` sowie
  seine Diagnose bei.
- `connectors/lighttpd/tests/test_patched_event_validation.py` — lokaler
  direkter Regressionstestkandidat.
- `reports/audits/change-records/CR-20260727-sonar-lighttpd-harness-duplication.md`
  und `reports/audits/change-records/CR-20260727-sonar-lighttpd-harness-duplication.de.md`
  — dieses vollständige Change-Record-Paar.
- `reports/audits/change-records/README.md` und
  `reports/audits/change-records/README.de.md` — synchronisierte Indexeinträge.

## Ausgeführte Befehle

Die folgenden lokalen Ergebnisse wurden für diesen Kandidaten beobachtet. Die
Source- und Lifecycle-Contract-Suiten wurden durch die primäre
Implementierungsarbeit abgeschlossen; dieses Dokumentations-Follow-up hält
ihre tatsächlichen Ergebnisse fest, statt sie als Ausführung des
Dokumentations-Workers zu behaupten.

- `rtk proxy git status --short` — beobachtete den lokalen Source-/Test-Kandidaten
  als unstaged, bevor dieses Dokumentationspaar hinzugefügt wurde.
- `rtk proxy git submodule status modules/ModSecurity-test-Framework` —
  beobachtete den in `## Identität` festgehaltenen read-only Parent-Gitlink-Zustand.
- `python -m unittest -v connectors.lighttpd.tests.test_patched_event_validation connectors.lighttpd.tests.test_patched_host_contract`
  — `passed`; 20 Tests bestanden.
- `python -m unittest -v tests.test_full_lifecycle_evidence tests.test_collect_no_crs_source`
  — `passed`; 51 Tests bestanden.
- `make check-bilingual-docs check-doc-links` — `passed`.
- `git diff --check` — `passed`; kein Whitespace-Fehler.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_bilingual_docs`
  — `passed`; die Ausgabe meldete `Ran 14 tests` und `OK`.

## Security-Auswirkung

Sicherheitsklassifikation: `not_applicable` als neues Security-Finding. Ein
fokussiertes Security-Review dieses Kandidaten beobachtete kein neues
validiertes oder plausibles Finding. Diese Dokumentationsarbeit ändert keine
Sicherheitskontrolle. Der beobachtete Kandidat erhält die fail-closed lokale
JSONL-Dateigrenze: Fehlerhafte Eingabe bleibt ein Parserfehler,
Nichtobjekt-Eingabe behält aufrufergesteuerte Diagnosen, Boolean-/negative
Zähler schlagen fehl, Over-Inspection schlägt fehl und die P4-Selektoren
verlangen genau ein passendes Event. Die unterschiedlichen Selektoren bleiben
lokal, statt zu einer breiteren geteilten Akzeptanzregel zu werden.

## Runtime-Evidence

`not_applicable`: Durch diese dokumentationsbezogene Arbeit wurde kein
Connector-Service, Live-Host, Framework oder MRTS-Runtime gestartet. Der
Record berichtet statisches lokales Kandidatenverhalten sowie beobachtete
lokale Source-, Lifecycle-Contract- und Dokumentationsvalidierung; er
behauptet kein Runtime-Verhalten.

## Bekannte Einschränkungen

Primäre Source- und Lifecycle-Contract-Validierung steht nicht mehr aus: Die
beiden Suiten unter `## Ausgeführte Befehle` bestanden jeweils 20 bzw. 51
Tests. Dieses Dokumentations-Follow-up startete keinen Connector-Runtime-,
Framework- oder MRTS-Test unabhängig. Der Kandidat wartet weiter auf einen
autorisierten `Draft` Commit und spätere Delivery. Der Record kann kein
SonarQube-Cloud-Deduplizierungsergebnis etablieren, bis ein exakter
ausgelieferter Head analysiert wurde.

## Verbleibende Risiken

Spätere Änderungen an einem lokalen P4-Selektor, einer Aufruferdiagnose oder
der Zählerkonvertierung können erneut Verhaltensdivergenz erzeugen. Gehostete
Analyse, CI/Review sowie `Draft` Commit/Delivery stehen aus und dürfen nur
anhand später beobachteter Evidence festgehalten werden.

## Nicht ausgeführte Prüfungen mit Begründung

- Connector-Runtime-, Framework- und MRTS-Tests: `not_run`; sie liegen
  außerhalb dieses Parent-Dokumentationsumfangs.
- SonarQube-Cloud-Analyse, GitHub CI, Commit, Push, Pull Request und Merge:
  `not_run`; keine Delivery- oder gehostete Aktion ist erfolgt oder für diesen
  Worker autorisiert.

## Finaler Diff- und Review-Status

Die beobachtete lokale Validierung ist `passed` für die fokussierte
Lighttpd-Source-Suite (20 Tests), Lifecycle-Contract-Suite (51 Tests),
`make check-bilingual-docs check-doc-links` und `git diff --check`, nachdem
dieses Paar und beide Indexeinträge aktualisiert wurden. Der Produktkandidat
ist lokal und unstaged; ein autorisierter `Draft` Commit und nachfolgende
Delivery stehen aus. Es werden kein Commit, Push, Pull Request, GitHub CI,
gehostete SonarQube-Cloud-Analyse oder Merge behauptet.
