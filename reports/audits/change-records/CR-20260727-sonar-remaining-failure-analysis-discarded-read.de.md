# Change Record: Parent-Remaining-Failure-Analyse-Bereinigung verworfener Lesezugriffe für SonarQube Cloud S1481

**Sprache:** [English](CR-20260727-sonar-remaining-failure-analysis-discarded-read.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-remaining-failure-analysis-discarded-read |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent-SonarQube-Cloud-`python:S1481`-Code-Smell AZ7HxAnC_i61V0DF6_Gg (Inventory-Zeile 568). |
| Grenze | Parent-Remaining-Failure-Report-Generator- und Parent-Test-Quelltext, dieses englisch/deutsche Change-Record-Paar und dessen Indizes. Framework/MRTS-Repository-Inhalt und Gitlinks, Report-Felder, Path-Validation-Controls, Scanner-Konfiguration, Quality Gates, Suppressions, externer Sonar-Status, GitHub-Status und Delivery bleiben unverändert. |

## Motivation und Problemstellung

`category_rollup(...)` baute eine `examples`-Liste und verwarf sie sofort.
Ihre rechte Seite rief `case_group_summary(...)` und danach
`example_entry(...)` auf und wiederholte dadurch Evidence-/Case-Datei-/YAML-
Lesezugriffe, obwohl das unabhängig erzeugte Feld `typical_examples` die
einzige Report-Ausgabe ist. Der Sonar-`S1481`-Befund brauchte daher einen
Verhaltensreview statt einer blinden Dead-Local-Löschung.

## Akzeptanzkriterien

- Nur die verworfene `examples`-Zuweisung entfernen.
- `typical_examples`, Category-Counts, Reihenfolge und Report-Felder bewahren.
- Eine Baseline herstellen, die den verworfenen Summary-Lesezugriff zeigt.
- Fokussierte Parent-only-Coverage hinzufügen, die diesen Pfad ablehnt und den
  Output verifiziert.
- Schreibfreie Syntax-/AST-, Dokumentationspaar- und Diff-Hygiene-Checks
  bestehen lassen.

## Implementierungsentscheidung und Begründung

Der Report erzeugt `typical_examples` bereits über eine separate
`example_entry(...)`-Comprehension. Die gelöschte Liste wurde weder
zurückgegeben noch gelesen. Eine gemockte Baseline zeigte einen redundanten
`case_group_summary(...)`-Aufruf für eine gefüllte Category. Der neue
fokussierte Test macht diesen Aufruf zum Fehler und bestätigt, dass die
ausgewählte Category weiter ein typisches Beispiel sowie denselben Count
liefert. Die Änderung entfernt zusätzliche Lese-/Parse-Arbeit, nicht die
Report-Ausgabe.

## Geänderte Dateien

- `ci/evidence/reports/generate-remaining-failure-analysis.py`
- `tests/test_remaining_failure_analysis.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -c <gemocktes Baseline-category_rollup-Prädikat>` bestand vor der
  Änderung und bestätigte den verworfenen Summary-Leseaufruf sowie erhaltenen
  Output.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -m unittest -v tests.test_remaining_failure_analysis` bestand
  nach der Änderung: 1 Test in 0.002s.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv
  python> -B -c <Post-Edit-Syntax- und verworfener-Lesezugriff-AST-Prädikat>`
  bestand.
- Der Dokumentationspaar-Validator, `tests.test_bilingual_docs` und
  `rtk proxy git diff --check` werden ausgeführt, nachdem dieses Paar angelegt
  ist; dieses Record behauptet kein unbeobachtetes CI-, Runtime-, Review- oder
  Delivery-Ergebnis.

## Security-Auswirkung

`not_applicable` für den Produkt-Diff: Die entfernte Arbeit war ein
verworfener, doppelter Safe-Reading-/Parsing-Pfad und keine Path-Validation-,
Ownership-, Symlink-, Publication- oder Access-Control-Entscheidung. Der
erhaltene `typical_examples`-Pfad nutzt weiter das vorhandene Report-
Helper-Verhalten, und der fokussierte Test verwendet Mocks ohne Framework/MRTS-
Daten zu konsumieren.

## Runtime-Evidence

Es wurde keine Connector-, NGINX-, CRS-, MRTS-, Native-libmodsecurity- oder
Report-Generation-Runtime ausgeführt. Der Test prüft einen In-Memory-
Parent-Generator-Vertrag; er behauptet keine Runtime-Evidence oder aus realen
Inputs abgeleitete Ausgabe.

## Bekannte Einschränkungen

Der lokale Interpreter ist Python 3.14.4, während der CI-Version-File-Vertrag
Python 3.14.6 verlangt; das fokussierte Ergebnis ist daher same-minor lokale
Evidence. Die Änderung eliminiert absichtlich extern beobachtbares redundantes
Datei-Lese-Timing; sie bewahrt diese irrelevante Nebenwirkung nicht. Der
öffentliche Projekt-Endpunkt meldet weiter 1.125 `OPEN`-Issues und dieser
uncommittete Kandidat ändert keinen externen Sonar-Status.

## Verbleibende Risiken

Ein undokumentierter Consumer könnte sich auf redundantes Lese-Timing oder
einen unterdrückten Malformed-Input-Parse verlassen haben. Baseline und
fokussierter Test beweisen den ausgewählten Output-Vertrag, aber eine
Sonar-Analyse auf einem exakten ausgelieferten Head bleibt erforderlich, bevor
der Key extern als behoben behandelt werden kann.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Report-Generation, Connector-Builds, NGINX/CRS/MRTS-Matrizen
  und Framework/MRTS-Checks werden nicht ausgeführt, da diese fokussierte
  Parent-Bereinigung sonst nicht verwandte Runtime-Inputs konsumieren würde.
- Es gab keine GitHub-CI, keine SonarQube-Cloud-PR-Analyse, kein Review,
  keinen Pull Request, keinen Merge und kein Default-Branch-Update.

## Finaler Diff- und Review-Status

Der B15-Kandidat ist lokal, uncommittet und ungepusht. Es gibt keine Delivery-,
Framework- oder MRTS-Action.
