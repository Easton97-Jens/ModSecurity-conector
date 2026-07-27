# Change Record: Parent-Report-Präsentationsliterale für SonarQube Cloud S1192

**Sprache:** [English](CR-20260727-sonar-report-presentation-literals.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-report-presentation-literals |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S1192`-Code-Smells AZ7HxAmX_i61V0DF6_GJ, AZ7HxAmX_i61V0DF6_GK und AZ7HxAoH_i61V0DF6_Gy. |
| Grenze | Parent-Markdown-Renderer und ein Parent-In-Memory-Renderer-Test, dieses englisch/deutsche Change-Record-Paar und dessen Indizes. Report-Eingaben, Report-Pfade, Evidence, Klassifikation, Request-/Rule-/Status-Semantik, Scanner-Konfiguration, Quality Gates, Suppressions, externer Sonar-Status, GitHub-Status, Framework/MRTS-Inhalt und Delivery bleiben unverändert. |

## Motivation und Problemstellung

Zwei Report-Renderer wiederholten stabile Markdown-Präsentationsliterale.
Sonar-Regel `python:S1192` meldet drei solche aktuellen Befunde.
Moduleigene Konstanten machen die jeweiligen Präsentationsverträge explizit,
ohne zu ändern, wie einer der Reports Eingaben liest, Evidence klassifiziert
oder Ausgaben schreibt.

## Akzeptanzkriterien

- Nur die zwei Body-Processor-Tabellenkonstanten und die Rule-Chain-Leerzeilen-
  Konstante definieren.
- Nur die doppelten Renderer-Literale ersetzen.
- Die exakten Markdown-Bytes und die drei relevanten Vorkommen jedes Renderers
  bewahren.
- Nur In-Memory-Renderer-Eingaben ausführen; keine Report-Generator-Mains,
  Dateiausgaben, Connector-Runtime, Framework oder MRTS ausführen.
- Englisches/deutsches Change-Record-Paar und Indizes pflegen, danach
  Dokumentationspaar- und Diff-Hygiene-Validierung ausführen.

## Implementierungsentscheidung und Begründung

`DISTRIBUTION_TABLE_HEADER` und `DISTRIBUTION_TABLE_SEPARATOR` bewahren die
zwei Body-Processor-Tabellenzeilen in allen drei ausgewählten Subclustern.
`NO_ROWS_MARKDOWN` bewahrt die drei Rule-Chain-Leerlisten-Zeilen. Der
fokussierte Test baut Zero-Row-Report-Dictionaries im Speicher und prüft die
exakten Konstanten-Bytes sowie die Vorkommenszahlen; er ruft absichtlich weder
`main()` eines Generators noch Pfad-/Evidence-Funktionen auf.

## Geänderte Dateien

- `ci/evidence/reports/generate-body-processor-analysis.py`
- `ci/evidence/reports/generate-rule-chain-semantics-analysis.py`
- `tests/test_report_presentation_literals.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- `rtk proxy env TMPDIR=<task-owned evidence root> PYTHONDONTWRITEBYTECODE=1
  PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest
  tests.test_report_presentation_literals` bestand nach der Änderung: 2 Tests
  in 0.001s.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -c <AST-Exaktkonstanten-Prädikat>` bestand.
- Die erste fokussierte Assertion zählte einen Tabellentrenner global; andere
  absichtlich unveränderte Tabellen verwenden ihn ebenfalls. Der korrigierte
  Test zählt das exakte Header-/Separator-Paar. Das war eine Reparatur der
  Testannahme, kein Produktfehler.
- Der Dokumentationspaar-Validator und `rtk proxy git diff --check` werden
  ausgeführt, nachdem dieses Paar angelegt ist; dieses Record behauptet kein
  unbeobachtetes CI-, Runtime-, Review- oder Delivery-Ergebnis.

## Security-Auswirkung

`not_applicable` für den Produkt-Diff: Die Änderung ist auf statische
Markdown-Anzeigeliterale begrenzt. Sie ändert keine Eingabelektüre,
Path-Containment-, Evidence-Validierungs-, Request-/Rule-/Status-Semantik,
Subprocess-, Netzwerk- oder Publication-Logik. Bestehende Report-Pfad- und
Text-Sanitization-Controls werden nicht verändert.

## Runtime-Evidence

Es wurde keine Connector-, Report-Generator-Main-, Output-Writer-, Framework-,
MRTS- oder Host-Runtime ausgeführt. Der fokussierte Test wertet beide Renderer
nur mit In-Memory-Zero-Row-Report-Objekten aus.

## Bekannte Einschränkungen

Der lokale Interpreter ist Python 3.14.4, während der CI-Version-File-Vertrag
Python 3.14.6 verlangt; das Ergebnis ist daher same-minor lokale Evidence.
Dieser Batch behandelt drei aktuelle Code-Smells; der öffentliche Projekt-
Endpunkt meldet weiter 1.125 `OPEN`-Issues und dieser uncommittete Kandidat
ändert keinen externen Sonar-Status.

## Verbleibende Risiken

Ein unerwarteter Renderer-Consumer könnte byte-exakte Ausgabe erwarten. Die
Konstanten werden auf ihre exakten früheren Strings geprüft und der fokussierte
Render-Test bewahrt alle drei ausgewählten Header-/Leerzeilen-Vorkommen. Eine
Sonar-Analyse auf einem exakten ausgelieferten Head bleibt erforderlich, bevor
die aufgeführten Keys extern als behoben behandelt werden können.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Report-Generierung ist absichtlich ausgeschlossen: Sie kann
  Evidence lesen oder schreiben und benötigt Runtime-/Framework-Eingaben
  außerhalb dieses reinen Präsentationsbatches.
- Vollständige Dokumentations-/Link-Checks liegen außerhalb dieses kleinen
  Batches; frühere vollständige Läufe sind wegen des absichtlich nicht
  initialisierten Framework-Gitlinks blockiert, nicht wegen dieser Renderer.
- Es gab keine GitHub-CI, keine SonarQube-Cloud-PR-Analyse, kein Review,
  keinen Pull Request, keinen Merge und kein Default-Branch-Update.

## Finaler Diff- und Review-Status

Der B18-Kandidat ist lokal, uncommittet und ungepusht. Es gibt keine Delivery-,
Framework- oder MRTS-Action.
